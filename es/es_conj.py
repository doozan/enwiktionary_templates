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
import enwiktionary_templates.module.es_verb as M
from ..get_template_params import get_template_params

def es_conj(t, title):
    #print(title, t, file=sys.stderr)
    args = get_template_params(t)
    # always generate all combined forms
    args.pop("nocomb",None)
    args[1] = args.pop('1', None)
    args["pagename"] = title

    forms = M.do_generate_forms(args, False, {}, title)
    joined = M.concat_forms(forms, {})
    joined = joined.replace("[[", "").replace("]]", "")
    items = []
    for i in joined.split("|"):
        if "," in i:
            k = re.match(r"(.*?)=.*", i).group(1)
            items.append(i)
            for v in i.split(",")[1:]:
                items.append(f"{k}={v}")
        else:
            items.append(i)
    return "; ".join(sorted(joined.split("|")))

"""
#from .paradigms import paradigms
#from .combined import _data as combined

_unstresstab = str.maketrans("áéíóú", "aeiou")
def unstress(word):
    return word.translate(_unstresstab)

def es_conj_ar(t, title):
    return es_conj(t, "-ar")

def es_conj_er(t, title):
    return es_conj(t, "-er")

def es_conj_ir(t, title):
    return es_conj(t, "-ir")

def es_conj_ír(t, title):
    return es_conj(t, "-ír")

def es_conj(t, ending):

    pattern = None
    reflexive = t.has("ref")
    if t.has("p"):
        pattern = str(t.get("p").value)
    stems = [ str(p.value).strip() for p in t.params if str(p.name).isdigit() ]

    inflections = inflect(stems, ending, pattern, reflexive)
    combined = inflect_combined(inflections, ending, pattern, reflexive)

    for formtype, forms in combined.items():
        for form in forms:
            if not form:
                continue

            if formtype not in inflections:
                inflections[formtype] = set()
            inflections[formtype].add(form)

            if "_acc_" not in formtype:
                continue
            if form[-2:] in [ "lo", "la" ]:
                continue
            if form[-3:] in ["los", "las"]:
                continue

            formtype = formtype.replace("_acc_", "_acc-dat_")

            if formtype not in inflections:
                inflections[formtype] = set()

            for indirect_pronoun in [ "lo", "la", "los", "las" ]:
                if form[-2:] == "le":
                    form_modified = form[:-2] + "se" + indirect_pronoun
                elif form[-3:] == "les":
                    form_modified = form[:-3] + "se" + indirect_pronoun
                else:
                    form_modified = form + indirect_pronoun

                # if original form is unstressed (eg, it only had two vowels: dame), add stress
                if not re.match("[áéíóú]", form_modified):
                    form_modified = create_accented_form(form_modified)
                inflections[formtype].add(form_modified)

    all_forms = set()
    for formtype, forms in inflections.items():
        formtype = str(formtype)
        for form in forms:
            if not form or form == "-":
                continue
            all_forms.add((formtype, form))

    return "; ".join([f"{k}={v}" for k,v in sorted(all_forms)])

vowels = {
    "a": "á",
    "e": "é",
    "i": "í",
    "o": "ó",
    "u": "ú"
    }
stressed_vowels = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u"
    }

def create_accented_form(form, ua_disyllabic=False):
    # create accented stem for reflexive verbs
    if not form:
        return form

    if "," in form:
        res = []
        for subform in form.split(","):
            res.append(create_accented_form(subform, ua_disyllabic))
        return ",".join(res)

    result = form

    vowel_count = 0
    for c in range(len(result)-1,-1,-1):
        v1 = result[c]
        if v1 not in vowels:
            continue

        vowel_count +=1

        # 'ue' or 'ua' count as 1 vowel, accent goes on e or a
        if c<len(result)-1:
            v2 = result[c+1]

            if v1 == 'u' and v2 == 'e':
                vowel_count -= 1

            if v1 == 'u' and v2 == 'a' and not ua_disyllabic:
                vowel_count -= 1

        # 'ai' or 'oi' counts as 1 vowel, accent goes on a or o
        if c>1:
            v3 = result[c-1]
            if v3 == 'a' and v1 == 'i':
                vowel_count -= 1
            if v3 == 'o' and v1 == 'i':
                vowel_count -= 1

        if vowel_count == 3:
            return result[:c] + vowels[v1] + result[c+1:]

    return result



def inflect(stems, ending, pattern="", reflexive=False):

    if pattern is None:
        pattern = ""

    if ending not in paradigms:
        print("Bad verb ending", stems,ending,pattern, file=sys.stderr)
        return {}

    if pattern and pattern not in paradigms[ending]:
        print("Bad verb pattern", stems,ending,pattern, file=sys.stderr)
        return {}

    pattern_data = paradigms[ending][pattern]

    # This has to be a deep copy, since we're overwriting values
    data = {k:v for k, v in paradigms[ending]['']['patterns'].items()}

    if reflexive:
        for k,v in paradigms[ending]['']['ref'].items():
            data[k] = v

        if pattern and 'ref' in pattern_data:
            for k,v in pattern_data['ref'].items():
                data[k] = v

    # Layer pattern data over base data
    if pattern:

        if 'replacement' in pattern_data:
            for pk,pv in pattern_data['replacement'].items():
                for dk,dv in data.items():
                    if dv:
                        data[dk] = dv.replace(str(pk), pv)

        for pk,pv in pattern_data['patterns'].items():
            if pv == '-':
                data[pk] = None
            else:
                data[pk] = pv

    if reflexive:
        for k in [63,65,68]:
            if not pattern_data.get("unstressed",{}).get(k):
                data[k] = create_accented_form(data[k])

    for dk,dv in data.items():
        if dv:
            if len(stems):
                for sk, sv in enumerate(stems,1):
                    dv = dv.replace(str(sk), sv)

            # Remove any stray placeholders in case there weren't enough stems provided
            dv = re.sub(r'[0-9]', '', dv)
            data[dk] = [ k.strip() for k in dv.split(',') ]
        else:
            data[dk] = [ None ]

    return data


def inflect_combined(forms, ending, pattern="", reflexive=False):

    if pattern is None:
        pattern = ""

    pattern_data = paradigms[ending][pattern]
    unstressed = pattern_data.get("unstressed", {})

    # This has to be a deep copy, since we're overwriting values
    data = {k:v for k, v in paradigms[ending]['']['patterns'].items()}

    result = {}
    aspects = ["acc", "dat"]

    for paradigm, paradigm_data in combined.items():
        for form in forms.get(paradigm_data["index"]):
            if reflexive and form.endswith("se"):
                form = form[:-2]
            for aspect in aspects:
                for k2, pronoun_table in enumerate(paradigm_data[aspect],1):

                    t = []
                    for k3, pronoun in enumerate(pronoun_table,1):
                        irregular = False
                        form_modified = form

                        stem_cuts = paradigm_data.get("stem_cuts",{}).get(k2)
                        if stem_cuts:
                            if len(stem_cuts) == 2:
                                form_modified = form_modified[stem_cuts[0]-1:stem_cuts[1]+1]
                            else:
                                if pronoun == stem_cuts[0]:
                                    form_modified = form_modified[stem_cuts[1]-1:stem_cuts[2]+1]

                        ending_irregularities = paradigm_data.get("ending_irregularities",{}).get(ending)
                        if ending_irregularities:
                            for pattern_data in ending_irregularities:
                                if aspect == pattern_data[0]:
                                    if k2 == pattern_data[1]:
                                        if pronoun == pattern_data[2]:
                                            form_modified = pattern_data[3](form_modified)

                        paradigm_irregularities = paradigm_data.get("paradigm_irregularities",{}).get(pattern)
                        if paradigm_irregularities:
                            for pattern_data in paradigm_irregularities:
                                if aspect == pattern_data[0]:
                                    if k2 == pattern_data[1]:
                                        if pronoun == pattern_data[2]:
                                            form_modified = pattern_data[3](form_modified)
                                            irregular = True

                        if unstressed:
                            if unstressed.get(paradigm_data["index"], False):
                                form_modified = unstress(form_modified)

                        if paradigm_data.get("paradigm_no_accent", {}).get(pattern):
                            form_modified = unstress(form_modified) + pronoun
                        else:
                            if not irregular:
                                if paradigm_data.get("accented_stem"):
                                    if paradigm_data.get("ua_disyllabic",{}).get(pattern):
                                        form_modified = create_accented_form(unstress(form_modified+pronoun), True)
                                    else:
                                        form_modified = create_accented_form(unstress(form_modified+pronoun), False)
                                else:
                                    form_modified = form_modified + pronoun
                        t += form_modified.split(", ")

                    if t:
                        parameter = paradigm + "_" + aspect + "_" + str(k2)
                        if parameter in result:
                            result[parameter] += t
                        else:
                            result[parameter] = t

    return result

"""
