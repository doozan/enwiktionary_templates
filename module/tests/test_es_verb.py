import enwiktionary_templates.module.es_verb as M
import re

import requests
import urllib.parse
import sqlite3
import json
import os

def get_database():
    filename = "test.cache.db"

    if os.path.exists(filename):
        return sqlite3.connect(filename)

    db = sqlite3.connect(filename)
    db.execute("CREATE TABLE cache(key text, value text, UNIQUE(key))")
    return db

def get_url(url):
    db = get_database()
    res = list(db.execute("SELECT value FROM cache WHERE key=?", (url,)))
    if res:
        print(f"using cached value for {url}")
        return res[0][0]

    print(f"fetching {url}")
    r = requests.get(url)
    db.execute("INSERT INTO cache VALUES(?, ?)", (url, r.text))

    db.commit()
    db.close()
    return r.text

def get_wiki_forms(page, p1=""):

    url = "https://en.wiktionary.org/w/api.php?action=expandtemplates&format=json&prop=wikitext&text=" \
         + urllib.parse.quote("{{User:JeffDoozan/es-verb-generate-forms|" + f"{p1}|pagename={page}" + "|json=1}}")
    data = json.loads(get_url(url))

    template_json = data["expandtemplates"]["wikitext"]
    forms = json.loads(template_json)["forms"]
    return forms

def get_and_check_forms(page, p1=""):
    baseline = get_wiki_forms(page, p1)
    args = { 1: p1 }
    forms = M.do_generate_forms(args, None, {}, page)["forms"]
    compare(baseline, forms)
    return forms

def compare(baseline, generated):

    # modify baseline to match our keynames
#    orig_len = len(baseline)
#    baseline = {k.replace("imp_3s", "imp_2sf").replace("imp_3p", "imp_2pf"):v for k,v in baseline.items()}
#    assert len(baseline) == orig_len

    values_match = True
    for k in sorted(baseline.keys()):

        base_forms = [x["form"].replace("[","").replace("]", "") for x in baseline[k]]

        generated_forms = [x["form"].replace("[","").replace("]", "") for x in generated.get(k, [{"form": ""}])]
        if sorted(base_forms) != sorted(generated_forms):
            print("mismatched", k, base_forms, generated_forms)
            values_match = False
    assert values_match

    no_extra = True
    for k in sorted(generated.keys()):
        if k != "gerund_without_se" and "_comb_" not in k and k not in baseline:
            print("generated extra form", k, generated[k])
            no_extra = False
    assert no_extra



#added_combos = []
#for p1 in ["me", "te", "se", "nos", "os"]:
#    for p2 in ["lo", "la", "le", "los", "las", "les"]:
#        added_combos.append(p1+p2)
#extended_combos = tuple(added_combos)

def test_check_slots():
    assert len(M.verb_slots_basic) == 87
    assert len(M.verb_slots_combined) == 244
    assert len(M.all_verb_slots) == 331

#    assert len(list(x for x in M.verb_slots_combined.keys() if re.match(r".*_(.*)", x).group(1) not in extended_combos)) == 67
#    assert len(list(x for x in M.all_verb_slots.keys() if re.match(r".*_(.*)", x).group(1) not in extended_combos)) == 141

def test_generate_forms():
    args = { 1: None }
    d = {}
    from_headword = False

    forms = get_and_check_forms("hablar")
    forms = get_and_check_forms("absolver")
    forms = get_and_check_forms("adscribir")
    forms = get_and_check_forms("advenir")
    forms = get_and_check_forms("ir")
    forms = get_and_check_forms("merecer")
    forms = get_and_check_forms("rasguñar")
    forms = get_and_check_forms("aterir", "<no_pres_stressed>")
    forms = get_and_check_forms("acertar con", "acertar<ie> con")
    forms = get_and_check_forms("errar", "<ye[Spain],+[Latin America]>")
    forms = get_and_check_forms("subseguir", "<i>")
    forms = get_and_check_forms("descubrir")
    forms = get_and_check_forms("argüir")
    forms = get_and_check_forms("colorir", "<no_pres_stressed>")
    forms = get_and_check_forms("mostrar", "<ue>")
    forms = get_and_check_forms("salir")
    forms = get_and_check_forms("abalanzar")

    forms = get_and_check_forms("ababillarse")
    for k, forms in forms.items():
        for f in forms:
            if f["form"] == "ababíllense":
                print(k, f)

    forms = get_and_check_forms("tener")
    assert len(forms) == 318
    assert forms["pres_1p"][0]["form"] == "tenemos"
    assert forms["neg_imp_2s"][0]["form"] == "[[no]] [[tengas]]"

    forms = get_and_check_forms("erguir")
    assert sorted([
        forms["pres_sub_1p"][0]["form"],
        forms["pres_sub_1p"][1]["form"]]) == ["irgamos", "yergamos"]

    forms = get_and_check_forms("abajar")
    for k, forms in forms.items():
        for f in forms:
            if f["form"] == "abajarla":
                print(k, f)

    PAGENAME = "tener"
    args = { 1: None, "force_regular": True }
    forms = M.do_generate_forms(args, from_headword, d, PAGENAME)
    assert forms["forms"]["pres_1s"][0]["form"] == "teno"
