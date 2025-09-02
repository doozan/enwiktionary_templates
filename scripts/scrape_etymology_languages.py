#!/usr/bin/python3
# -*- python-mode -*-

import luadata_to_python
import requests
import json
import argparse
import datetime

def get_wikipage(page):
    url = 'https://en.wiktionary.org/w/api.php?action=query&prop=revisions&rvslots=*&rvprop=content|ids&format=json&titles=' + page
    niceurl = 'https://en.wiktionary.org/wiki/' + page

    headers = { 'User-Agent':  'AutoDooz/1.0 (https://github.com/doozan/wikibot; wiki@doozan.com)' }
    res = requests.get( url, headers=headers )
    json_data = res.json()
    revision = list(json_data['query']['pages'].values())[0]['revisions'][0]['revid']
    wikitext = list(json_data['query']['pages'].values())[0]['revisions'][0]['slots']['main']['*']
    return { "wikitext": wikitext, "revision": revision, "url": niceurl }

def dump_label_data():

    print("data = {}")
    target = "Module:etymology_languages/data"
    res = get_wikipage(target)

    print(f"# Data from: {res['url']} (revision: {res['revision']}, scraped {datetime.datetime.now()})")
    pydata = luadata_to_python.convert(res["wikitext"], "m", f'data', trim_newlines=True)
    print(pydata)

def main():
    parser = argparse.ArgumentParser(description='Scrape Module:etymology_languages/data from wiktionary')
    args = parser.parse_args()

    dump_label_data()

main()
