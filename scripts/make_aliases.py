#!/usr/bin/python3

import argparse
import csv
import json
import sys
from enwiktionary_templates import get_handler

def main():
    parser = argparse.ArgumentParser(description='build template aliases from exported redirect data')
    parser.add_argument("redirects", help="redirects.tsv")
    args = parser.parse_args()

    aliases = {}

    prefix = ["Template:", "template:", "T:"]
    with open(args.redirects) as infile:
        for x in csv.reader(infile, delimiter="\t"):
            for p in prefix:
                if x[0].startswith(p):
                    alias = x[0].removeprefix(p)
                    target = x[1].replace("_", " ")
                    for _p in prefix:
                        if target.startswith(_p):
                            target = target.removeprefix(_p)
                            break

                    t_handler = get_handler(target, None, None)
                    a_handler = get_handler(alias, None, None)
                    if a_handler and t_handler:
                        if not any(alias.startswith(p) for p in ["R:", "RQ:"]):
                            print("DUP HANDLERS", [alias, target], file=sys.stderr)
                    elif a_handler:
                        print("HANDLES", alias, "but should handle", target, file=sys.stderr)
                    elif t_handler:
                        aliases[alias] = target

    print("ALIASES = " + json.dumps(aliases, sort_keys=True, indent=4))

if __name__ == "__main__":
    main()
