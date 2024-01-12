#!/usr/bin/python3

import argparse
import multiprocessing
import os
import re
import sqlite3
import sys
import mwparserfromhell as mwparser

import json
import requests
import urllib.parse

from pathlib import Path

def get_default_cachedb():
    dbpath = Path("~/.enwiktionary_templates").expanduser()
    dbpath.mkdir(parents=True, exist_ok=True)
    return os.path.join(dbpath, "cache.db")

class Cache():

    TEMPLATES = {
        "es-verb": {},
        "es-conj": {},
    }


    def __init__(self, dbfile=None):

        if not dbfile:
            dbfile = get_default_cachedb()

        self.dbfile = dbfile
        existing = os.path.exists(dbfile)
        self.dbcon = sqlite3.connect(dbfile)
        #dbcon.execute('PRAGMA synchronous=OFF;')
        if not existing:
            self.dbcon.execute('''CREATE TABLE templates (page text, template text, params text, data text, date_retrieved integer(4), UNIQUE(page,template,params))''')


    def queue(self, page, template_name, param_str):
        if not template_name in self.TEMPLATES:
            raise ValueError(f"unhandled template: {template_name}")

        self.dbcon.execute("INSERT OR IGNORE INTO templates VALUES (?, ?, ?, NULL, NULL)", [page, template_name, param_str])
        self.dbcon.execute("COMMIT;")


    def get(self, page, text):

        template_name, param_str = self.parse_template(text)
        res = self.dbcon.execute(f"SELECT data FROM templates WHERE page=? and template=? and params=? LIMIT 1", (page, template_name, param_str,))

        try:
            return next(res)[0]
        except StopIteration:
            print("failed reading", page, text, file=sys.stderr)
            return ""


        # TODO: If this fails, download from site and cache?
        #data_str = self.download_data(page, template_name, param_str)
        #self.update(page, template_name, param_str, data_str)

    @classmethod
    def get_all_stale(cls, dbfile, limit=None):
        if not dbfile:
            dbfile = get_default_cachedb()

        dbcon = sqlite3.connect(dbfile)

        def get_template_last_modified(template_name):
            # TODO: get modified times from mediawiki
            return "1704480980";


        # buffer all rows because sqlite doesn't like running multi-threaded

        stale = []

        limit = f"LIMIT {limit}" if limit else ""

        for res in dbcon.execute(f"SELECT DISTINCT template FROM templates"):
            template_name = res[0]
            template_modified = get_template_last_modified(template_name)
            cur = dbcon.execute(f"SELECT page, template, params FROM templates WHERE template == ? AND date_retrieved IS NULL or date_retrieved < ? {limit} ORDER BY page", (template_name, template_modified))
            stale += cur.fetchall()

        return stale

    @classmethod
    def download_data(cls, page, template, param_str):
        data = cls.get_wiki_forms(page, template, param_str)
        data_str = json.dumps(data, ensure_ascii=False)
        return data_str

    def update(self, page, template, param_str, data_str):
        self.dbcon.execute("UPDATE templates SET data=?, date_retrieved=strftime('%s','now') WHERE page=? AND template = ? AND PARAMS = ?", [data_str, page, template, param_str])
        self.dbcon.execute("COMMIT;")

    def parse_template(self, text):
        """ Returns template_name, normalized_param_string """

        if not text.startswith("{{") and text.endswith("}}"):
            raise ValueError("Unexpected input")

        wiki = mwparser.parse(text)
        t = next(wiki.ifilter_templates(recursive=False))

        if not str(t) == text:
            raise ValueError("Supplied text is not a single template")

        template_name = t.name.strip()
        params = self.get_params(t)
        self.cleanup_params(template_name, params)
        param_str = self.params_to_str(params)
        return template_name, param_str


    def cleanup_params(self, template_name, params):

        # TODO: per-template cleanup

        for p in ["nocomb"]:
            if p in params:
                del params[p]

    @staticmethod
    def params_to_str(params):

        items = []
        for k, v in sorted(params.items()):
            if k.isdigit():
                while int(k) > len(items)+1:
                    items.append("")
                items.append(v)

        for k, v in sorted(params.items()):
            if k.isdigit():
                continue
            items.append(f"{k}={v}")

        return "|".join(items)

    @staticmethod
    def get_params(template):
        return { str(p.name).strip(): str(p.value).strip() for p in template.params }

    @staticmethod
    def get_wiki_forms(page, template, param_str=None):

        param_str = "|" + param_str if param_str else ""

        # TODO: per-template handling

        #print("expanding {{es-conj" + params_str + f"|pagename={page}|json=1" + "}}")

        url = "https://en.wiktionary.org/w/api.php?action=expandtemplates&format=json&prop=wikitext&text=" \
             + urllib.parse.quote("{{es-conj" + param_str + f"|pagename={page}|json=1" + "}}")
        res = requests.get(url)
        data = json.loads(res.text)

        template_json = data["expandtemplates"]["wikitext"]

        try:
            forms = json.loads(template_json)["forms"]
            #print("loaded", len(forms))
        except json.decoder.JSONDecodeError:
            print("non-json data returned", page, template)
            return None

        return forms




def iter_wxt(datafile, limit=None, show_progress=False):

    if not os.path.isfile(datafile):
        raise FileNotFoundError(f"Cannot open: {datafile}")

    from enwiktionary_wordlist.wikiextract import WikiExtractWithRev
    parser = WikiExtractWithRev.iter_articles_from_bz2(datafile)

    count = 0
    for entry in parser:

        if ":" in entry.title or "/" in entry.title:
            continue

        if not count % 1000 and show_progress:
            print(count, end = '\r', file=sys.stderr)

        if limit and count >= limit:
            break
        count += 1

        yield entry.text, entry.title




def scrape_templates(args):
    text, page = args

    if not any(t in text for t in Cache.TEMPLATES):
        return []

    wiki = mwparser.parse(text)

    res = []
    for t in wiki.ifilter_templates(matches=lambda x: x.name.strip() in Cache.TEMPLATES):
        params = Cache.get_params(t)

        for p in ["nocomb"]:
            if p in params:
                del params[p]

        param_str = Cache.params_to_str(params)
        #res.append((page, t.name.strip(), param_str))
        res.append((page, "es-conj", param_str))

    return res


def download_data(args):
    page, template, param_str = args
    data_str = Cache.download_data(page, template, param_str)
    return page, template, param_str, data_str


def main():
    parser = argparse.ArgumentParser(description="Cache all templates calls")
    parser.add_argument("--db", help="Local database cache", default=None)
    parser.add_argument("--wxt", help="Local database cache")
    parser.add_argument("--limit", type=int, help="Limit processing to first N articles")
    parser.add_argument("--progress", help="Display progress", action='store_true')
    parser.add_argument("-j", help="run N jobs in parallel (default = # CPUs - 1", type=int)
    parser.add_argument("--update", help="Download uncached and stale template calls", action='store_true')
    args = parser.parse_args()

    if not args.j:
        args.j = multiprocessing.cpu_count()-1

    if args.wxt:
        iter_entries = iter_wxt(args.wxt, args.limit, args.progress)

        if args.j > 1:
            pool = multiprocessing.Pool(args.j)
            iter_items = pool.imap_unordered(scrape_templates, iter_entries, 1000)
        else:
            iter_items = map(scrape_templates, iter_entries)

        cache = Cache(args.db)
        for results in iter_items:
            for page, template, param_str in results:
                cache.queue(page, template, param_str)

    if args.update:
        iter_entries = Cache.get_all_stale(args.db)

        if args.progress:
            print(f"Downloading {len(iter_entries)} entries")

        if args.j > 1:
            pool = multiprocessing.Pool(args.j)
            iter_items = pool.imap_unordered(download_data, iter_entries, 1)
        else:
            iter_items = map(download_data, iter_entries)

        cache = Cache(args.db)
        for page, template, param_str, data_str in iter_items:
            if args.progress:
                print("updating", page, template, param_str)
            cache.update(page, template, param_str, data_str)

if __name__ == "__main__":
    main()

