import sys
from .es_conj import es_conj, es_conj_reg
from .es_noun import es_noun
from .es_adj import es_adj, es_adj_sup, es_adj_comp

@staticmethod
def es_compound_of(t,title):

    # TODO: temporarily generating proper form of

    mood = None
    if t.has("mood"):
        mood = str(t.get("mood").value)
        if mood in ["inf", "infinitive"]:
            mood = "infinitive"
        elif mood in ["part", "participle", "adv", "adverbial", "ger", "gerund", "gerundive", "gerundio", "present participle", "present-participle"]:
            mood = "gerund"
        elif mood in ["imp", "imperative"]:
            mood = "imp"
        else:
            mood = None

    person = None
    if mood == "imp" and t.has("person"):
        person = {"tú": "2s",
                "tu": "2s",
                "inf": "2s",
                "vos": "2sv",
                "vosotros": "2p",
                "v": "2p",
                "inf-pl": "2p",
                "nosotros": "1p",
                "usted": "2sf",
                "ud": "2sf",
                "f": "2sf",
                "ustedes": "2pf",
                "uds": "2pf",
                "f-pl": "2pf"}[str(t.get("person").value)]

    if mood == "imp":
        if not person:
            print(title, t, "imperative mood without a person")
        else:
            mood = f"imp_{person}"

    part1 = str(t.get(4).value) if t.has(4) else ""
    part2 = str(t.get(5).value) if t.has(5) else ""

    combo = part1+part2
    if mood and combo:
        return f'{mood}_comb_{combo} of "{t.get(1)}{t.get(2)}"'

    if t.has(5):
        return f'compound form of "{t.get(1)}{t.get(2)}"+"{t.get(4)}"+"{t.get(5)}"'
    if t.has(4):
        return f'compound form of "{t.get(1)}{t.get(2)}"+"{t.get(4)}"'

    if t.has(2):
        return f'compound form of "{t.get(1)}{t.get(2)}"'

    return ""

@staticmethod
def es_note_noun_common_gender_a(t,title):
    return ""

@staticmethod
def es_note_noun_mf(t,title):
    return ""

@staticmethod
def es_note_noun_f_starting_with_stressed_a(t,title):
    return ""

@staticmethod
def es_proper_noun(t,title):
    return ""

@staticmethod
def es_suffix(t,title):

    forms = []
    for p in ["f", "pl", "fpl"]:
        if t.has(p):
            forms.append(f"{p}={t.get(p).value}")

    if not forms:
        return ""

    return "; ".join(forms)



_es_verb_form_of_params = {
    "_alt_keys": {
        "num": "number",
        "pers": "person",
        "gen": "gender",
    },
    "mood": {
        "_alt_values": {
            "ind": "indicative",
            "subj": "subjunctive",
            "imp": "imperative",
            "cond": "conditional",
            "par": "participle",
            "part": "participle",
            "past participle": "participle",
            "past-participle": "participle",
            "adv": "gerund",
            "adverbial": "gerund",
            "ger": "gerund",
            "gerundio": "gerund",
            "present participle": "gerund",
            "present-participle": "gerund",
        }
    },
    "tense": {
        "_alt_values": {
            "pres": "present",
            "pret": "preterite",
            "preterit": "preterite",
            "imp": "imperfect",
            "fut": "future",
            "cond": "conditional",
        }
    },
    "number": {
        "_alt_values": {
            "sg": "s",
            "sing": "s",
            "singular": "s",
            "pl": "p",
            "plural": "p",
            "impersonal": "0"
        }
    },
    "person": {
        "_alt_values": {
            "first": "1",
            "first person": "1",
            "first-person": "1",
            "second": "2",
            "second person": "2",
            "second-person": "2",
            "third": "3",
            "third person": "3",
            "third-person": "3",
            "imp": "0",
            "impersonal": "0",
        }
    },
    "formal": {
        "_alt_values": {
            "yes": "y",
            "no": "n",
        }
    },
    "sense": {
        "_alt_values": {
            "+": "affirmative",
            "aff": "affirmative",
            "-": "negative",
            "neg": "negative",
        }
    },
    "sera": {},
    "gender": {},
    "particple": {},
    "voseo": {
        "_alt_values": {
            "yes": "y",
            "no": "n",
        }
    },
    "region": {},
}

_es_verb_tense_to_slot = {
    "present": "pres",
    "imperfect": "impf",
    "preterite": "pret",
    "future": "fut",
    "conditional": "cond",
}
_es_verb_mood_to_slot = {
    "gerund": "ger",
    "indicative": "ind",
    "subjunctive": "sub",
    "imperative": "imp",
    "conditional": "cond",
}

_es_verb_params = {k:v for k, v in _es_verb_form_of_params["_alt_keys"].items()}
_es_verb_params.update({k:k for k in _es_verb_form_of_params.keys() if not k.startswith("_")})

@staticmethod
def es_verb_form_of(t, title):

    #return f'inflection of "{t.get(1)}"'

    d = {}

    for p, pdest in _es_verb_params.items():
        v = str(t.get(p).value).strip() if t.has(p) else None
        if not v:
            continue
        v = _es_verb_form_of_params[pdest].get("_alt_values", {}).get(v, v)
        d[pdest] = v

    slot = ""

    if d.get("mood") == "participle":
        genpl = "".join([d.get("gender", "m"), d.get("number", "s")])
        assert genpl in ["ms", "mp", "fs", "fp"]
        slot = "pp_" + genpl
        return f'{slot} of "{t.get(1)}"'

    elif d.get("mood") == "gerund":
        slot = "gerund"
        return f'{slot} of "{t.get(1)}"'

    if d.get("sense", "") == "negative":
        slot += "neg_"

    if "tense" in d:
        if d.get("mood","") in ["indicative", "subjunctive"]:
            slot += _es_verb_tense_to_slot[d["tense"]] + "_"

    if "mood" in d:
        if d["mood"] != "indicative":
            slot += _es_verb_mood_to_slot[d["mood"]] + "_"

    if "sera" in d:
        if d["sera"] not in ["se", "ra"]:
            raise ValueError("sera no se or ra", d)
        if d["mood"] == "subjunctive" and d["tense"] == "imperfect":
            slot += d["sera"] + "_"
        else:
            # TODO: flag for cleanup
            pass

    if slot.rstrip("_") not in  {'cond', 'fut', 'fut_sub', 'gerund', 'imp', 'impf', 'impf_sub_ra', 'impf_sub_se', 'neg_imp', 'pp_fs', 'pp_fp', 'pp_ms', 'pp_mp', 'pres', 'pres_sub', 'pret'}:
        raise ValueError("bad slot", slot, d, t)

    person = "".join([d["person"], d["number"]])
    if d["person"] == "2":
        if d.get("voseo") == "y":
            person += "v"
        elif d.get("formal") == "y":
            person += "f"

    if person not in ["", "1s", "2s", "2sf", "2sv", "3s", "1p", "2p", "2pf", "3p"]:
        # haber, llover
        if person not in ["00", "0s", "0p"]:
            raise ValueError("bad person", person)

    if person:
        slot += person

    return f'{slot} of "{t.get(1)}"'
