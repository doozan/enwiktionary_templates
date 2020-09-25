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

    res = requests.get( url )
    json_data = res.json()
    revision = list(json_data['query']['pages'].values())[0]['revisions'][0]['revid']
    wikitext = list(json_data['query']['pages'].values())[0]['revisions'][0]['slots']['main']['*']
    return { "wikitext": wikitext, "revision": revision, "url": niceurl }

def dump_label_data():

    modules = [ "", "regional", "topical", "subvarieties" ]
    variables = [ "labels", "aliases" ]

    print("data = {}")
    for module in modules:
        target = "Module:labels/data"
        suffix = ""
        if module:
            target += "/" + module

        res = get_wikipage(target)

        for varname in variables:
            print(f"# Data from: {res['url']} (revision: {res['revision']}, scraped {datetime.datetime.now()})")
            pydata = luadata_to_python.convert(res["wikitext"], varname, f'data["{module}_{varname}"]', trim_newlines=True)
            print(pydata)

    for varname in variables:
        targets = [ f'**data["{module}_{varname}"]' for module in modules ]
        print(f'data["{varname}"] = {{', ", ".join(targets) + "}")

def main():
    parser = argparse.ArgumentParser(description='Scrape Module:labels data from wiktionary')
    args = parser.parse_args()

    dump_label_data()

main()
