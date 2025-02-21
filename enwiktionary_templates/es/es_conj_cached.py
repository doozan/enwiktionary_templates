#
# Copyright (c) 2020 Jeff Doozan
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import sys

import json
from ..cache import Cache
import enwiktionary_templates.module.es_common as com

#from .es_conj import es_conj as old_es_conj

def remove_links(text):
    return re.sub(r"\[\[([^|\[]+[|])?([^|\[]+)]]", r"\2", text)

def es_verb(t, title, database):
    # es-verb is aliased to this function, which is fine except
    # for a handful of pages (fazer) that still use the old-style
    # es-verb parameters.
    if any(p in t for p in ["pres","pret", "attn", "head"]):
        return ""

    data = es_conj(t, title, database)

    res = []
    for kv in data.split("; "):
        if re.match(r"^(pres_1s|pret_1s|pp_[mf][sp])=", kv):
            res.append(kv)

    return "; ".join(res)



def es_conj(t, title, database):
    cache = Cache(database)

    data = cache.get("es-conj", t, title)
    if not data:
        return ""

    # The lua module doesn't generate all possible forms of the verb
    # So we have to add them manually here

    data = remove_links(data)
    params = json.loads(data)

    slot_personal_clitics = {
        "inf": ["me", "te", "se", "nos", "os"],
        "gerund": ["me", "te", "se", "nos", "os"],
        "imp_2s": ["me", "te", "nos"],
        "imp_2sv": ["me", "te", "nos"],
        "imp_3s": ["me", "se", "nos"],
        "imp_1p": ["te", "nos", "os"],
        "imp_2p": ["me", "nos", "os"],
        "imp_3p": ["me", "se", "nos"],
    }
    third_person_object_clitics = ["lo", "la", "le", "los", "las", "les"]

    forms = {}
    for slot, slot_data in params.items():
        slot_forms = [f["form"] for f in slot_data]
        forms[slot] = slot_forms

        if "_comb_" in slot:
            splits = slot.split("_")
            clitic = splits.pop()
            base_slot = "_".join(splits)

            for clitic2 in third_person_object_clitics:

                if clitic in ["lo", "la", "los", "las"]:
                    continue

                if clitic == clitic2:
                    continue

                if clitic in ["le", "les"]:
                    if "se" not in "slot_personal_clitics":
                        continue
                    clitic1 = "se"
                else:
                    clitic1 = clitic

                new_slot = "_".join([base_slot] + [clitic1, clitic2])
                new_slot_forms = [add_clitic(f, clitic2, t.get(1, "")) for f in slot_forms]
                if any(f is not None for f in new_slot_forms):
                    forms[new_slot] = new_slot_forms


    # Generating missing forms from reflexive verbs
    if title.endswith("rse"):
        #print("ADDING EXTRA FORMS")
        forms["gerund_variant"] = [make_variant(f, "3s") for f in forms["gerund_3s"]]
        forms["infinitive_variant"] = [title.removesuffix("se")]

        for slot in ["1p", "2p", "2s", "2sv", "3p", "3s"]:
            if f"imp_{slot}" not in forms:
                continue
            variant_data = [make_variant(f, slot) for f in forms[f"imp_{slot}"]]
            variant_slot = f"imp_{slot}_variant"
            forms[variant_slot] = variant_data

    # check for v.strip() == v to fix bad some bad conjugations in "salir de Guatemala y meterse en Guatepeor" ['gerund_1p', ' de Guatemala y metiéndonos en Guatepeor']
    # as of 1/21/2025 only appears to affect the single page
    return "; ".join(f"{k}={'|'.join(vs)}" for k,vs in sorted(forms.items()) if all(v.strip() == v for v in vs))


def rfind(string, pattern):
    return re.search(pattern, string)

def rsub(string, pattern, replacement):
    return re.sub(pattern, replacement, string, 1)

AV = "[áéíóúý]" # accented vowel

_remove_accent = {
    "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ý": "y"
}
def remove_accent(syllable):
    return rsub(syllable, AV, lambda m: _remove_accent.get(m.group(0), m.group(0)))

_add_accent = {
    "a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "y": "ý"
}

def add_accent(syllable):
    # Don't do anything if syllable already stressed.
    if rfind(syllable, AV):
        return syllable

    # Prefer to accent an a/e/o in case of a diphthong or triphthong (the first one if for some reason
    # there are multiple, which should not occur with the standard syllabification algorithm);
    # otherwise, do the last i or u in case of a diphthong ui or iu.
    if rfind(syllable, "[aeo]"):
        return rsub(syllable, r"^(.*?)([aeo])", lambda m: m.group(1) + _add_accent[m.group(2)])

    return rsub(syllable, r"^(.*)([iu])", lambda m: m.group(1) + _add_accent[m.group(2)])

def make_variant(form, slot):

    syllables = com.syllabify(form)
    sylno = com.stressed_syllable(syllables)
    clitic = syllables.pop()
    needs_accent = com.accent_needed(syllables, sylno)
    if needs_accent:
        syllables[sylno] = com.add_accent_to_syllable(syllables[sylno])
    else:
        syllables[sylno] = com.remove_accent_from_syllable(syllables[sylno])

    new_form = "".join(syllables)
    if slot == "1p":
        new_form += "s"
    if slot == "2p":
        new_form = remove_accent(new_form) + "d"

    return clitic + " " + new_form


def add_clitic(base, clitic, text):

    if " " in text:
        verbs = [m.group(1) for m in re.finditer(r"\b(\w*([aeií]r|[aeií]rse))\b", text)]
        if len(verbs) == 0:
            verb_pos = 0
        elif len(verbs) == 1:
            pre_text, *_ = text.split(verbs[0])
            verb_pos = pre_text.count(" ")
        elif len(verbs) > 1:
            return None
            raise ValueError("can't find single verb", text, verbs)

    else:
        verb_pos = 0


    base_words = base.split(" ")
    verb = base_words[verb_pos]

    syllables = com.syllabify(verb)
    sylno = com.stressed_syllable(syllables)
    syllables.append(clitic)
    needs_accent = com.accent_needed(syllables, sylno)
    if needs_accent:
        syllables[sylno] = com.add_accent_to_syllable(syllables[sylno])
    else:
        syllables[sylno] = com.remove_accent_from_syllable(syllables[sylno])

    base_words[verb_pos] = "".join(syllables)

    return " ".join(base_words)
