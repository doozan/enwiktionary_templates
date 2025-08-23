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

from enwiktionary_templates.utils import get_template_params, params_to_str

def get_default_cachedb():
    dbpath = Path("~/.enwiktionary_templates").expanduser()
    dbpath.mkdir(parents=True, exist_ok=True)
    return os.path.join(dbpath, "cache.db")

class Cache():

    TEMPLATES = {
        # TODO: force refresh whenever certain pages have been modified
        "es-conj": { "name": "es-conj" },
        "es-verb": { "name": "es-conj" }, # es-conj is not a typo

        "+obj": { "name": "+obj"},

        "transclude": { "name": "transclude" },
        "tcl": { "name": "transclude" },

        "etymon": { "name": "etymon" },

        "demonym-adj": { "name": "demonym-adj" },
        "demonym-noun": { "name": "demonym-noun" },

    }

    TMPL_REGEX = r"{{\s*" + "|".join(re.escape(k) for k in TEMPLATES.keys()) + r"\s*[|}]"

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


    def get(self, template_name, params, page):

        clean_params = self.cleanup_params(template_name, params)
        if clean_params == -1:
            return ""

        param_str = params_to_str(clean_params, sort_params=True, inline_modifiers=True)

        res = self.dbcon.execute(f"SELECT data FROM templates WHERE page=? and template=? and params=? LIMIT 1", (page, template_name, param_str,))

        try:
            data = next(res)[0]
        except StopIteration:
            print("failed reading", page, template_name, param_str, file=sys.stderr)
            return ""


        if data == "ERROR":
            data = download_data([page, template_name, param_str])
            if data == "ERROR":
                raise ValueError("Error retrieving data for", page, template_name, param_str)
                self.update(page, template_name, param_str, data_str)

        return data


        # TODO: If this fails, download from site and cache?
        #data_str = self.download_data(page, template_name, param_str)
        #self.update(page, template_name, param_str, data_str)

    @classmethod
    def get_all_stale(cls, dbfile, limit=None):
        dbcon = sqlite3.connect(dbfile)

        def get_template_last_modified(template_name):
            # TODO: get modified times from mediawiki
            return 1704480980;


        # buffer all rows because sqlite doesn't like running multi-threaded

        stale = []

        limit = f"LIMIT {limit}" if limit else ""

        for res in dbcon.execute(f"SELECT DISTINCT template FROM templates"):
            template_name = res[0]
            template_modified = get_template_last_modified(template_name)
            print(f"SELECT page, template, params FROM templates WHERE template == ? AND date_retrieved IS NULL or date_retrieved < ? {limit} ORDER BY page", (template_name, template_modified))
            cur = dbcon.execute(f"SELECT page, template, params FROM templates WHERE template == ? AND date_retrieved IS NULL or date_retrieved < ? {limit} ORDER BY page", (template_name, template_modified))
            stale += cur.fetchall()
            print("scanning", template_name, len(stale))

        return stale

    def update(self, page, template, param_str, data_str):
        self.dbcon.execute("UPDATE templates SET data=?, date_retrieved=strftime('%s','now') WHERE page=? AND template = ? AND PARAMS = ?", [data_str, page, template, param_str])
        self.dbcon.execute("COMMIT;")

    @classmethod
    def cleanup_params(cls, template_name, params):
        if template_name == "etymon":
            # don't cache templates that don't generate text
            if "text" not in params:
                return -1

            # never generate tree
            if "tree" in params:
                del params["tree"]

        # TODO: per-template cleanup
        return {k:v for k,v in params.items() if k not in ["nocomb"]}


    @staticmethod
    def get_wiki_data(page, template_name, param_str=None):

        param_str = "|" + param_str if param_str else ""

        url = "https://en.wiktionary.org/w/api.php?action=expandtemplates&format=json&prop=wikitext&text=" \
             + urllib.parse.quote("{{" + template_name + param_str + "}}")

        tries = 10
        res = None
        while tries:
            try:
                res = requests.get(url)
            except requests.exceptions.RequestException as e:
                time.sleep(5)
            else:
                break
            tries -= 1

        if not res:
            return None

        data = json.loads(res.text)
        return data["expandtemplates"]["wikitext"]



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

    if not re.search(Cache.TMPL_REGEX, text):
        return []

    wiki = mwparser.parse(text)

    res = []
    for t in wiki.ifilter_templates(matches=lambda x: x.name.strip() in Cache.TEMPLATES):
        template_name = Cache.TEMPLATES[t.name.strip()]["name"]
        params = get_template_params(t)
        clean_params = Cache.cleanup_params(template_name, params)
        # don't cache templates that return -1 from cleanup_params
        if clean_params == -1:
            continue

        param_str = params_to_str(clean_params, sort_params=True)
        res.append((page, template_name, param_str))

    return res


def download_data(args):
    page, template, param_str = args

    params = param_str
    if template == "es-conj":
        params += "|" if params else ""
        params += f"pagename={page}|json=1"

    data_str = Cache.get_wiki_data(page, template, params)

    if data_str is None or 'scribunto-error' in data_str:
        data_str = "ERROR"

    else:
        data_str = cleanup_wiki_data(template, data_str)

    return page, template, param_str, data_str


def cleanup_wiki_data(template_name, data_str):
    if template_name == "es-conj":
        try:
            data_str = json.dumps(json.loads(data_str)["forms"], ensure_ascii=False)
        except json.decoder.JSONDecodeError:
            print("non-json data returned", page, template)
            return None

    elif template_name == "transclude":
        data_str = re.sub("<span.*?>", "", data_str).replace("</span>", "")

    return data_str



def main():
    parser = argparse.ArgumentParser(description="Cache all templates calls")
    parser.add_argument("--db", help="Local database cache", default=None)
    parser.add_argument("--wxt", help="Local database cache")
    parser.add_argument("--limit", type=int, help="Limit processing to first N articles")
    parser.add_argument("--progress", help="Display progress", action='store_true')
    parser.add_argument("-j", help="run N jobs in parallel (default = # CPUs - 1", type=int)
    parser.add_argument("--update", help="Download uncached and stale template calls", action='store_true')
    args = parser.parse_args()

    if not args.db:
        args.db = get_default_cachedb()

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
            if data_str == "ERROR":
                continue
            if args.progress:
                print("updating", page, template, param_str)
            cache.update(page, template, param_str, data_str)

if __name__ == "__main__":
    main()

