#!/usr/bin/python3
# -*- python-mode -*-

import argparse
import json
import pprint
import requests
import subprocess

def get_wikipage(page_name):
    url = f"https://en.wiktionary.org/w/api.php"
    params = {
        'action': 'query',
        'prop': 'revisions',
        'rvslots': '*',
        'rvprop': 'content|ids',
        'format': 'json',
        'titles': page_name,
    }

    headers = { 'User-Agent':  'AutoDooz/1.0 (https://github.com/doozan/wikibot; wiki@doozan.com)' }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    wikitext = list(data['query']['pages'].values())[0]["revisions"][0]['slots']['main']['*']
    revision_id = list(data['query']['pages'].values())[0]["revisions"][0]['revid']

    return {
        "wikitext": wikitext,
        "revision": revision_id,
        "url": 'https://en.wiktionary.org/wiki/' + page_name
    }


def dump_label_data():

    modules = [ "", "qualifiers", "regional", "topical" ]


    labels = {}
    for module in modules:

        target = "Module:labels/data"
        suffix = ""
        if module:
            target += "/" + module

        res = get_wikipage(target)
        text = res["wikitext"]
        assert text.count("require(") == 1
        assert 'return require("Module:labels").finalize_data(labels)' in text

        with open("data.lua", "w") as outfile:
            old = 'return require("Module:labels").finalize_data(labels)'
            new = 'local cjson = require "cjson"\nprint(cjson.encode(labels))'
            text = text.replace(old, new)

            outfile.write(text)

        print(f"# Data from: {res['url']} (revision: {res['revision']})")

        lua_results = subprocess.check_output(["lua","data.lua"], encoding='utf-8')
        labels |= json.loads(lua_results)


    aliases = {}
    for label, item in labels.items():
        if "aliases" in item:
            for a in item.pop("aliases"):
                aliases[a] = label

    print("labels = ", pprint.pformat(labels, indent=4, compact=True, width=200))
    print("aliases = ", pprint.pformat(aliases, indent=4, compact=True, width=200))

def main():
    parser = argparse.ArgumentParser(description='Scrape Module:labels/data from wiktionary')
    args = parser.parse_args()

    dump_label_data()

main()
