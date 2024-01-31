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

def es_conj(t, title, database):
    return new_es_conj(t, title, database)

def test_es_conj(t, title, database):

    bad_endings = [ 'placer', 'scribir' ]
    bad_items = [ 'ir', 'trapazar', 'volar riata', 'volar verga' ]

    new = new_es_conj(t, title, database)

    if not new:
        return ""

    if title in bad_items:
        return new

    if any(title.endswith(x) for x in bad_endings):
        return new

    if template.count("<") > 1:
        return new

    old = old_es_conj(t, title)

#    assert "abstén" in old
#    print(old)
#    print("-----")
#    print(new)

    if old != new:
        old_items = old.split("; ")
        new_items = new.split("; ")

        new_data = {}
        old_data = {}

        for slot in new_items:
#            print("X", [title, slot], file=sys.stderr)
            slot_name, slot_value = slot.split("=")
            values = slot_value.split("|")
            new_data[slot_name] = values

        for slot in old_items:
            slot_name, slot_value = slot.split("=")
            if slot_name in old_data:
                old_data[slot_name].append(slot_value)
   #             print("DUP", slot_name, old_data[slot_name])
            else:
                old_data[slot_name] = [slot_value]

        #print("old", old_data["imp_2s"])
        #print("new", new_data["imp_2s"])

#        if (title.endswith("rse") or "rse" in str(template)) and not only_new and all(s.endswith("_non_reflexive") or s.endswith("_variant") for s in only_old):
#            return new


        only_old = old_data.keys() - new_data.keys()
        only_new = new_data.keys() - old_data.keys()



        if only_old:
            if only_new:
                print("Only new:", sorted(only_new), file=sys.stderr)

            if not all(s.endswith("_non_reflexive") or s.endswith("_variant") for s in only_old) and not only_new:
                print("Only old:", sorted(only_old), file=sys.stderr)
                raise ValueError("old/new mismatch", title, template, len(old_items), len(new_items))

        if only_new:
            print("Only new:", sorted(only_new), file=sys.stderr)
            raise ValueError("old/new mismatch", title, template, len(old_items), len(new_items))

        mismatched = False
        for k in new_data.keys():
            if sorted(old_data[k]) != sorted(new_data[k]):
                print(k, old_data[k], "!=", new_data[k], file=sys.stderr)
                mismatched = True

#        if mismatched:
#            raise ValueError("old/new mismatch", title, template)

    return new


def new_es_conj(t, title, database):
    cache = Cache(database)

    data = cache.get("es-conj", t, title)
    if not data:
        return ""

    # The lua module doesn't generate all possible forms of the verb
    # So we have to add them manually here

    data = data.replace("[[", "").replace("]]", "")
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

    return "; ".join(f"{k}={'|'.join(vs)}" for k,vs in sorted(forms.items()))


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
