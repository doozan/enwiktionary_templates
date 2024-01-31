#!/usr/bin/python3
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

"""
A "just enough" implementation of en.wiktionary.org templates to convert
templates to meaningful wikidata
"""

import mwparserfromhell
import re
import sys

from enwiktionary_parser.languages.all_ids import ALL_LANG_IDS
from .etydata import data as ety_langs
from .labeldata import data as labeldata
from .place import place
from .module.es_headword import make_plural as es_make_plural
from .utils import get_template_params
from .cache import Cache, get_default_cachedb

class Template():

    ##import enwiktionary_templates.es as _es
    lang2 = {}
    #lang2["es"] = _es

    from .es import es_compound_of, es_conj, es_noun, es_proper_noun, es_adj, es_adj_sup, es_adj_comp, es_suffix, es_verb_form_of

    @staticmethod
    def _form_of(t, title, text):
        res = [text]
        display = next((t[p] for p in [3, 2] if t.get(p)), None)
        res.append(f'"{display}"')
        gloss= next((t[p] for p in ["t", "gloss", 4] if t.get(p)), None)
        if gloss and gloss != "-":
            res.append("(“" + str(gloss) + "”)")
        return " ".join(res)

    @staticmethod
    def _and_lit(t, template):
        res = []
        if "qualifier" in t:
            res.append(t["qualifier"])
            res.append("used other than figuratively or idiomatically:")
        else:
            res.append("Used other than figuratively or idiomatically:")

        x = 2
        while x in t:
            if f"alt{x-1}" in t:
                res.append(t[f"alt{x-1}"])
            else:
                res.append(t[x])
            x+=1

        if t.get("nodot"):
            return " ".join(res)
        else:
            dot = t.get("dot", ".")
            return " ".join(res) + dot

    @staticmethod
    def abbrev(t, title):
        return Template.__etyl_misc_variant(t, title, "abbreviation")
    abbreviation = abbrev

    @staticmethod
    def acronym(t, title):
        return Template.__etyl_misc_variant(t, title, "acronym")

    @staticmethod
    def affix(t, title, start_idx=2):
        res = []

        p = start_idx
        while t.get(p):
            x = p-1
            val = []

            # Handle lang:word formatted values
            if ":" in t[p] and not t[p].startswith("["):
                lang_id, _, word = t[p].partition(":")
            else:
                lang_id = t.get(f"lang{x}")
                word = t[p]

            if lang_id:
                lang_name = Template._get_lang(lang_id)
                val.append(f'{lang_name} "{word}"')
            else:
                val.append(word)

            tr = t.get(f"tr{x}")
            gloss = next((t.get(p) for p in [f"t{x}", f"gloss{x}"] if t.get(p)), None)
            if tr or gloss:
                item = ["("]
                if tr:
                    item.append(tr)
                    if gloss:
                        item.append(", ")
                if gloss:
                    item.append('"')
                    item.append(gloss)
                    item.append('"')

                item.append(")")
                val.append("".join(item))

            res.append(" ".join(val))

            p += 1

        return " + ".join(res)

    af = affix
    compound = affix
    com = affix
    confix = affix
    con = affix
    circumfix = affix


    @staticmethod
    def ante(t, title):
        res = ["a."]
        res.append(t[1])
        if 2 in t:
            res.append(t.get(2))
        return " ".join(res)

    @staticmethod
    def ar_root(t, title):
        if "notext" in t:
            return ""

        res = []
        p = 2
        while t.get(p):
            res.append(t.get(p))
            p += 1

        return " ".join(res)

    @staticmethod
    def ar_tool_noun(t, title):
        if "lc" in t:
            return "tool noun"
        return "Tool noun"

    @staticmethod
    def _get_lang(lang_id):
        lang_id = lang_id.strip('\n .')
        src_lang = ALL_LANG_IDS.get(lang_id.lower())
        if not src_lang:
            src_lang = ety_langs.get(lang_id, {}).get("canonicalName")
        if not src_lang:
            src_lang = lang_id
        return src_lang

    @staticmethod
    def __format_etyl(t, pre_text, lang, display, gloss):
        res = []
        if "notext" not in t and pre_text:
            if "nocap" in t:
                res.append(f"{pre_text}")
            else:
                res.append(f"{pre_text.capitalize()}")

        if lang:
            res.append(lang)

        if display and display != "-":
            res.append(display)
        if gloss and gloss != "-":
            res.append("(“" + str(gloss) + "”)")

        return " ".join(res)

    @staticmethod
    def __lang2_etyl(t, title, pre_text=None, offset=1):
        source = Template._get_lang(t[1+offset])
        display = next((t.get(p) for p in ["alt", 3+offset, 2+offset] if t.get(p)), None)
        if display and display != "-":
            display = f'"{display}"'
        gloss = next((t.get(p) for p in ["t", "gloss", 4+offset] if t.get(p)), None)
        return Template.__format_etyl(t, pre_text, source, display, gloss)

    @staticmethod
    def __etyl_misc_variant(t, title, pre_text=None, separator="of"):
        display = next((t.get(p) for p in ["alt", 3, 2] if t.get(p)), None)
        if display and display != "-":
            display = f'{separator} "{display}"'
        gloss = next((t.get(p) for p in ["gloss", "t", 4] if t.get(p)), None)
        return Template.__format_etyl(t, pre_text, None, display, gloss)

    @staticmethod
    def back_formation(t, title):
        return Template.__etyl_misc_variant(t, title, "back formation", "from")
    back_form = back_formation
    bf = back_formation

    @staticmethod
    def blend_of(t, title):
        res = [] if "notext" in t else ["Blend of"]
        res.append(Template.affix(t, title))
        return " ".join(res)
    blend = blend_of

    @staticmethod
    def bor_(t, title):
        if "nocap" in t:
            return Template.__lang2_etyl(t, title, "borrowed from")
        else:
            return Template.__lang2_etyl(t, title, "Borrowed from")

    @staticmethod
    def calque(t, title):
        return Template.__lang2_etyl(t, title, "calque of")
    cal = calque
    clq = calque

    @staticmethod
    def century(t, title):
        if 2 in t:
            return f"{t[1]}c-{t[2]}c"
        return f"{t[1]}c"

    @staticmethod
    def clipping(t, title):
        return Template.__etyl_misc_variant(t, title, "clipping")
    clip = clipping
    clipping_of = clipping

    @staticmethod
    def coinage(t, title):
        lang = Template._get_lang(t[1])

        coiner = t.get("alt", t[2])

        res = []
        if "notext" not in t:
            if "nocap" in t:
                res.append("coined by")
            else:
                res.append("Coined by")

        if "nationality" in t:
            res.append(t["nationality"])
        elif "nat" in t:
            res.append(t["nat"])

        if "occupation" in t:
            res.append(t["occupation"])
        elif "occ" in t:
            res.append(t["occ"])
        # TODO: handle muliple occupations

        res.append(coiner)

        if "in" in t:
            res.append("in " + t["in"])

        return " ".join(res)
    coin = coinage

    @staticmethod
    def derived(t, title):
        return Template.__lang2_etyl(t, title)
    der = derived
    borrowed = derived
    bor = derived
    bor_lite = derived
    inherited = derived
    inh = derived
    inh_lite = derived
    der_lite = derived
    uder = derived
    der_ = derived

    def cognate(t, title):
        return Template.__lang2_etyl(t, title, offset=0)
    cognate = cognate
    cog = cognate
    nc = cognate
    ncog = cognate
    noncog = cognate
    cog_lite = cognate

    @staticmethod
    def deverbal(t, title):
        return Template.__etyl_misc_variant(t, title, "deverbal")

    @staticmethod
    def doublet(t, title):
        text = ""
        if not "notext" in t:
            text = "doublet of " if "nocap" in t else "Doublet of "

        p = 2
        res = []
        while t.get(p):
            res.append(t[p])
            p += 1

        return text + ", ".join(res)

    dbt = doublet

    @staticmethod
    def ellipsis(t, title):
        return Template.__etyl_misc_variant(t, title, "ellipsis")
    ellipsis_of = ellipsis

    @staticmethod
    def es_verb_obj(t, title):
        new_t = {}
        # generate plurals as needed
        for k,v in t.items():
            if isinstance(k, int):
                idx = "" if k == 1 else k-1
                if f"pl{idx}" in t:
                    new_t[k] = es_make_plural(v)[0]
                    continue
            new_t[k] = v
        res = ["Verb-object compound, composed of "]
        res.append(Template.affix(new_t, title, 1))

        if "lit" in t:
            res.append(f', literally "{t["lit"]}"')

        return "".join(res)

    @staticmethod
    def etyl(t, title):
        src_lang_id = t.get(1).strip('\n .')
        src_lang = ALL_LANG_IDS.get(src_lang_id.lower())
        if not src_lang:
            src_lang = ety_langs.get(src_lang_id, {}).get("canonicalName")
        if not src_lang:
            src_lang = src_lang_id

        return src_lang

    @staticmethod
    def etydate(t, title):

        offset = 1

        t1 = t.get(1)
        if t1 == "c":
            c = "c. "
            offset = 2
        else:
            c = ""

        if t.get(offset) == "r":
            date = f"{t[offset+1]}-{t[offset+2]}"
            offset += 3
        else:
            date = f"{t[offset]}"
            offset += 1

        if offset in t:
            return f"First attested in {c}{date}, but in common usage only as of {t[offset]}"

        return f"First attested in {c}{date}"


    @staticmethod
    def u_es_false_friend(t, title):
        res = []
        if "nocap" in t:
            res.append(title)
        else:
            res.append(title[0].upper() + title[1:])

        res.append(" is a false friend and does not mean")

        if "en" in t:
            if "gloss" in t:
                res.append(' ')
                res.append(t["en"])
                res.append(f" in the sense of ''{t['gloss']}''.")
            else:
                res.append(f" {t['en']}.")

        elif "gloss" in t:
            res.append(f" ''{t['gloss']}''")
            res.append(" in Spanish.")
        else:
            res.append(f" the same as the English word for {title}.")

        if 1 in t:
            res.append("\nThe Spanish word for")
            if "en" in t:
                res.append(' ')
                res.append(t["en"])
                if "gloss" in t:
                    res.append(f" in that sense")
            else:
                res.append(' ')
                res.append(title)

            res.append(f" is ''{t[1]}''")

            i = 2
            while f"es{i}" in t:
                res.append(f" or ''")
                res.append(t[f"es{i}"])
                res.append(f"''")
                i += 1

            res.append(".")

        return "".join(res)

    # Custom method, not used in en.wiktionary
    @staticmethod
    def forms(t, title):
        return "; ".join([f"form={f}" for f in t.values()])

    @staticmethod
    def frac(t, title):
        if 3 in t:
            return f"{t[1]} {t[2]}/{t[3]}"
        if 2 in t:
            return f"{t[1]}/{t[2]}"
        return f"1/{t[1]}"

    @staticmethod
    def form_of(t, title):
        form = t[2] if t[2] else "form"

        gloss = ""
        for p in ["gloss", "t", 5]:
            if p in t:
                gloss = " (" + t[p] + ")"

        return f'{form} of "{t[3]}"{gloss}'

    @staticmethod
    def g(t, title):
        res = "{" + " or ".join(t.values()) + "}"
        res = re.sub("p", "pl", res)
        res = re.sub("-", " ", res)
        return res

    @staticmethod
    def gloss(t, title):
        return "(" + ", ".join(t.values()) + ")"
    gl = gloss
    gloss_lite = gloss
    gl_lite = gloss

    @staticmethod
    def given_name(t, title):
        return "given name"

    @staticmethod
    def indtr(t, title):
        labels = []
        indtr = ""
        i = 2
        q = None
        first = True
        andwith = False

        if t.get("intr"):
            indtr += "[[Appendix:Glossary#intransitive|intransitive]], or "

        while i in t:
            val = t[i]
            if val.startswith("."):
                labels.append(val[1:])
            elif val == ";":
                andwith = True
                if not t.get(f"qual{i-1}"):
                    indtr += " and with "
                else:
                    indtr += " and " + t[f"qual{i-1}"] + " with "
            else:
                if not first:
                    if andwith:
                        andwith = False
                    else:
                        indtr += " or "
                else:
                    if "cop" in t and "ditr" in t:
                        indtr += "[[Appendix:Glossary#ditransitive|ditransitive]], [[Appendix:Glossary#copulative|copulative]] with "
                    elif "cop" in t:
                        indtr += "[[Appendix:Glossary#copulative|copulative}} with "
                    elif "ditr" in t:
                        indtr += "[[Appendix:Glossary#ditransitive|ditransitive]] with the indirect object taking "
                    elif "aux" in t:
                        indtr += "[[Appendix:Glossary#auxiliary|auxiliary]] with "
                    else:
                        indtr += "[[Appendix:Glossary#transitive|transitive]] with "
                    first = False
                if val.startswith("-"):
                    indtr += val[1:]
                else:
                    indtr += "'''[[" + val + "]]'''"

                if f"qual{i-1}" in t:
                    indtr += "(" + t[f"qual{i-1}"] + ")"

            i += 1
        if t.get("direct"):
            if t.get("ditr"):
                indtr += " or no preposition"
            else:
                indtr += " or with no preposition"
            if t.get("qualdirect"):
                indtr += " (" + t["qualdirect"] + ")"

        if t.get("aux"):
            indtr += " and a verb in the " + t["aux"]
        elif "cop" in t and "ditr" in t:
            indtr += " for the second object"

        labels.append(indtr)
        res = Template._joinlabels(labels)
        if not res.strip():
            return ""
        return f"({res})"

    inflection_pos_type = {
        "a": "adjective",
        "adj": "adjective",
        "adv": "adverb",
        "art": "article",
        "cnum": "cardinal numeral",
        "conj": "conjunction",
        "det": "determiner",
        "int": "interjection",
        "intj": "interjection",
        #"vi": "intransitive verb",
        "vi": "verb",
        "n": "noun",
        "num": "numeral",
        "onum": "ordinal numeral",
        "part": "participle",
        "pcl": "particle",
        "postp": "postposition",
        "pre": "preposition",
        "prep": "preposition",
        "pro": "pronoun",
        "pron": "pronoun",
        "pn": "proper noun",
        "proper": "proper noun",
        #"vti": "transitive and intransitive verb",
        "vti": "verb",
        #"vt": "transitive verb",
        "vt": "verb",
        "v": "verb",
        "vb": "verb",
    }

    @staticmethod
    def inflection_of(t, title):

        pos = None
        for k in ["POS", "p"]:
            if k in t:
                if pos:
                    print("ERROR: Multiple POS", title, t, file=sys.stderr)
                pos = Template.inflection_pos_type.get(t[k], t[k])

        if not pos:
            pos = "inflection"

        x = 4
        params = []
        while x in t:
            params.append(t[x])
            x+=1

        qualifiers = []

        if "n" in params:
            qualifiers.append("neuter")
        if "m" in params:
            if qualifiers:
                print("ERROR: double gender", title, t, file=sys.stderr)
            qualifiers.append("masculine")
        if "f" in params:
            if qualifiers:
                print("ERROR: double gender", title, t, file=sys.stderr)
            qualifiers.append("feminine")
        if "s" in params:
            qualifiers.append("singular")
        if "p" in params or "pl" in params:
            qualifiers.append("plural")

        if "inf" in params or "infinitive" in params:
            qualifiers.append("infinitive")


        if any(x in params for x in ["1", "2", "3"] if x in params):
            qualifiers = []

        if not qualifiers:
            qualifiers = ["inflection"]
            #qualifiers = [pos, "form"]


        res = qualifiers
        res.append("of")
        res.append('"' + t[2] + '"')

        if "t" in t:
            res.append("(" + t["t"] + ")")

        if "tr" in t:
            res.append("(" + t["tr"] + ")")

        return " ".join(res)

    infl_of = inflection_of

    @staticmethod
    def adj_form_of(t, title):
        t["p"] = "a"
        return Template.inflection_of(t, title)

    @staticmethod
    def noun_form_of(t, title):
        t["p"] = "n"
        return Template.inflection_of(t, title)

    @staticmethod
    def verb_form_of(t, title):
        t["p"] = "v"
        return Template.inflection_of(t, title)

    @staticmethod
    def inh_(t, title):
        if "nocap" in t:
            return Template.__lang2_etyl(t, title, "inherited from")
        else:
            return Template.__lang2_etyl(t, title, "Inherited from")

    @staticmethod
    def label(t, title):
        labels = [ v for k,v in t.items() if isinstance(k,int) and k > 1]
        res = Template._joinlabels(labels)
        if not res.strip():
            return ""

        return f"({res})"
    lb = lbl = label
    tlb = label

    @staticmethod
    def _joinlabels(labels, delimiter=",", spacer=" "):

        formatted = []
        omit_preComma = False
        omit_postComma = True
        omit_preSpace = False
        omit_postSpace = True

        for label in labels:
            omit_preComma = omit_postComma
            omit_postComma = False
            omit_preSpace = omit_postSpace
            omit_postSpace = False

            label = labeldata["aliases"].get(label, label)
            data = labeldata["labels"].get(label, {})
            label = data.get("display", label)

            comma = "" if omit_preComma or data.get("omit_preComma") else delimiter
            space = "" if omit_preSpace or data.get("omit_preSpace") else spacer
            omit_postComma = omit_postComma or data.get("omit_postComma")
            omit_postSpace = omit_postSpace or data.get("omit_postSpace")

            formatted.append(comma + space + label)
        return "".join(formatted)

    @staticmethod
    def latn_def(t, title):
        res = ""
        if t.get(2) in ["letter", "name", "diacritic"]:
            res = "letter"
            if 4 in t:
                res += ": " + t[4]
            x = 5
            while x in t:
                res += ", " + t[x]
                x+=1

#        if t.get(2) in ["diacritic"]:


        return res

    latn_def_lite = latn_def

    @staticmethod
    def learned_borrowing(t, title):
        return Template.__lang2_etyl(t, title, "learned borrowing from")
    lbor = learned_borrowing

    @staticmethod
    def link(t, title):
        display = ""
        gloss = ""
        for p in [2, 3, "tr"]:
            if p in t:
                text = t[p]
                if text:
                    display = t[p]
        #for p in ["gloss", "t", 4]: # mbcompat, ignore t
        for p in ["gloss", 4]:
            if p in t:
                gloss = t[p]
        if gloss:
            gloss = " (" + str(gloss) + ")"

        return str(display)+gloss
    l = link
    ll = link
    l_lite = link

    @staticmethod
    def m(t, title):
        res = []
        display = None
        if 3 in t:
            display = t[3]
        if not display and 2 in t:
            display = t[2]

        if display:
            res.append("''" + display + "''")

        gloss = None
        for p in ["gloss", "t", 4]:
            if t.get(p):
                gloss = t[p]
        if gloss:
            res.append("(“" + str(gloss) + "”)")

        return " ".join(res)
    mention = m
    m_lite = m

    @staticmethod
    def mention_gloss(t, title):
        return '"' + t[1] + '"'
    m_g = mention_gloss

    @staticmethod
    def named_after(t, title):
        res = []
        if "alt" in t:
            res.append(t['alt'])
        else:
            if "nocap" in t:
                res.append("named after")
            else:
                res.append("Named after")

        if "alt" in t:
            res.append(t['alt'])
        else:
            if "nationality" in t:
                res.append(t['nationality'])
            elif "nat" in t:
                res.append(t['nat'])
            if "occupation" in t:
                res.append(t['occupation'])
            elif "occ" in t:
                res.append(t['occ'])

        if 2 in t:
            res.append(t[2])
        else:
            res.append("an unknown person")

        if "tr" in t:
            res.append("(" + t['tr'] + ")")

        if "born" in t or "died" in t:
            lived = ""
            if "born" in t:
                lived = t['born']
            else:
                lived = "?"
            if "died" in t:
                lived += "-" + t['died']

        return " ".join(res)

    @staticmethod
    def non_gloss_definition(t, title):
        return t[1]
    non_gloss = ng = ngd = n_g = non_gloss_definition
    n_g_lite = non_gloss_definition

    @staticmethod
    def not_used(t, title):
        return "Not used"

    @staticmethod
    def nuclide(t, title):
        return f"{t[1]}/{t[2]}" + t.get(3, "")

    @staticmethod
    def onomatopoeic(t, title):
        if "title" in t:
            return t["title"]
        if "notext" in t:
            return ""
        if "nocap" in t:
            return "onomatopoeic"
        return "Onomatopoeic"
    onom = onomatopoeic

    @staticmethod
    def only_in(t, title):
        return f'Only used in "{t[2]}"'

    @staticmethod
    def orthorgraphic_borrowing(t, title):
        return Template.__lang2_etyl(t, title, "orthographic borrowing from")
    obor = orthorgraphic_borrowing

    @staticmethod
    def pagename(t, title):
        return title

    @staticmethod
    def partial_calque(t, title):
        return Template.__lang2_etyl(t, title, "partial calque of")
    pcal = partial_calque
    pclq = partial_calque

    @staticmethod
    def phono_semantic_matching(t, title):
        return Template.__lang2_etyl(t, title, "phono-semantic matching of")
    psm = phono_semantic_matching

    @staticmethod
    def place(t, title):
        return place(t, title)

    @staticmethod
    def prefix(t, title):
        res = []
        res.append(t[2])
        res.append("+")
        if 3 in t:
            res.append(t[3])
        return " ".join(res)
    pre = prefix

    @staticmethod
    def pseudo_loan(t, title):
        return Template.__lang2_etyl(t, title, "Pseudo-loan from")

    @staticmethod
    def qf(t, title):
        return "(" + t[1] + ")"

    @staticmethod
    def qflit(t, title):
        return "(literally: " + t[1] + ")"
    lit = qflit

    @staticmethod
    def qualifier(t, title):
        params = [ v for k,v in t.items() if isinstance(k,int) ]
        return "(" + ", ".join(params) + ")"
    q = i = qual = qualifier
    q_lite = qualifier

    @staticmethod
    def quoted_term(t, title):
        return '“' + t[1] + '”'

    @staticmethod
    def rebracketing(t, title):
        return Template.__etyl_misc_variant(t, title, "rebracketing")

    @staticmethod
    def reduplication(t, title):
        return Template.__etyl_misc_variant(t, title, "reduplication")

    @staticmethod
    def rel_top(t, title):
        if 1 in t:
            return "---- " + t[1] + " ----"
        else:
            return "----"

    @staticmethod
    def t(t, title):
        display = next((t.get(p) for p in ["alt", 2] if t.get(p)), None)

        gender_params = [ v for k,v in t.items() if isinstance(k, int) and k > 2 ]
        if gender_params:
            genders = " or ".join(gender_params)
            genders = re.sub("p", "pl", genders)
            genders = re.sub("-", " ", genders)

            return f"{display} ({genders})"

        return display
    t_ = t
    tt = t
    tt_ = t
    t_simple = t

    @staticmethod
    def t_check(t, title):
        return "(unverified) " + Template.t(t, title)
    t__check = t_check

    @staticmethod
    def t_needed(t, title):
        return ""

    @staticmethod
    def transliteration(t, title):
        return Template.__lang2_etyl(t, title, "transliteration of")
    trans = transliteration

    @staticmethod
    def translit_name(t, title):
        return Template.__lang2_etyl(t, title, "transliteration of") + f" {t['type']}"

    @staticmethod
    def semantic_loan(t, title):
        return Template.__lang2_etyl(t, title, "semantic loan from")
    sl = semantic_loan

    @staticmethod
    def semi_learned_borrowing(t, title):
        return Template.__lang2_etyl(t, title, "semi-learned borrowing from")
    slbor = semi_learned_borrowing

    @staticmethod
    def sense(t, title):
        return "(" + t[1] + ")"
    s = sense
    sense_lite = sense

    @staticmethod
    def sic(t, title):
        return "(sic)"

    @staticmethod
    def suffix(t, title):
        base = t.get(2, "")
        suf = t[3].lstrip("-")
        return f"{base} + -{suf}"

    suf = suffix

    @staticmethod
    def surface_analysis(t, title):
        return "By surface analysis, " + Template.affix(t, title)
    surf = surface_analysis

    @staticmethod
    def surname(t, title):
        return "surname"

    @staticmethod
    def unadapted_borrowing(t, title):
        return Template.__lang2_etyl(t, title, "unadapted borrowing from")
    ubor = unadapted_borrowing

    @staticmethod
    def _text(t, title, text):
        if "notext" in t:
            return ""
        if "title" in t:
            text = t["title"]
        if "nocap" in t:
            text = text.lower()
        return text

    @staticmethod
    def uncertain(t, title):
        return Template._text(t, title, "Uncertain")
    unc = uncertain

    @staticmethod
    def unknown(t, title):
        return Template._text(t, title, "Unknown")
    unk = unknown

    @staticmethod
    def univerbation(t, title):
        if not 2 in t:
            return "Univerbation"

        res = [f"Univerbation of {t[2]}"]
        count = 3
        while count in t:
            res.append(t[count])
            count += 1
        return " + ".join(res)

    @staticmethod
    def ux(t, title):
        res = []
        for p in (2,3,"t"):
            if p in t:
                res.append(t[p])
        return " ― ".join(res)
    eg = ux_lite = uxi = usex = ux

ignore = {
    ",",
    "a",
    "anchor",
    "attention",
    "attn",
    "C",
    "c",
    "categorize",
    "catlangname",
    "catlangcode",
    "cite",
    "cite-av",
    "Cite book",
    "cite-book",
    "cite book",
    "cite-journal",
    "cite journal",
    "cite-web",
    "cite web",
    "cite news",
    "cln",
    "colorbox",
    "color-panel",
    "color panel",
    "colour panel",
    "context",
    "DEFAULTSORT",
    "dercat",
    "elements",
    "en-noun",
    "en-adj",
    "en-verb",
    "en-proper noun",
    "en-adv",
    "en-interj",
    "en-plural noun",
    "en-prop",
    "en-proper-noun",
    "en-prefix",
    "en-ipl",
    "en-prep",
    "en-proverb",
    "en-cont",
    "en-pron",
    "en-PP",
    "en-intj",
    "en-ing form of",
    "en-suffix",
    "en-interjection",
    "en-pronoun",
    "en-adjective",
    "en-con",
    "en-det",
    "en-contraction",
    "en-preposition",
    "en-prep phrase",
    "en-adverb",
    "en-conjunction",
    "en-pp",
    "en-particle",
    "en-obsolete past participle of",
    "en-plural-noun",
    "en-symbol",
    "en-propn",
    "en-usage-verb-particle-solid",
    "en-part",
    "en-letter",
    "en-ing",
    "es-adj-inv",
    "es-adv",
    "es-adverb",
    "es-conjunction",
    "es-diacritical mark",
    "es-int",
    "es-intj",
    "es-interj",
    "es-interjection",
    "es-letter",
    "es-past participle",
    "es-past-participle",
    "es-phrase",
    "es-prefix",
    "es-prep",
    "es-preposition",
    "es-pronoun",
    "es-proverb",
    "es-prop",
    "es-punctuation mark",
    "es-unadapted",
    "es-verb",
    "etymid",
    "etystub",
    "ISBN",
    "lena",
    "nbsp",
    "nonlemma",
    "PIE word",
    "pl-adj",
    "pl-adv",
    "pl-noun",
    "pl-prep",
    "pl-proper noun",
    "pl-verb",
    "rel-bottom",
    "rfc",
    "rfclarify",
    "rfdef",
    "rfe",
    "rfex",
    "rfform",
    "rfv-etym",
    "rfc-sense",
    "rfd-sense",
    "rfd-redundant",
    "rfm-sense",
    "rfquotek",
    "rfquote-sense",
    "rfv-sense",
    "root",
    "senseid",
    "swp",
    "t2i-Egyd",
    "tea room sense",
    "top",
    "topics",
    "translation only",
    "trans-bottom"
    "trans-mid",
    "trans-top",
    "U:en:plurals of letters",
    "U:es:relative pronouns",
    "Wikipedia",
    "wikipedia",
    "word",
    "wp",
}

# Templates that just return the first parameter
p1 = {
    "def",
    "def-date",
    "defdt",
    "defdate",
    "en-phrase",
    "epinew",
    "glink",
    "glossary",
    "honoraltcaps",
    "IPAchar",
    "IPAfont",
    "ja-def",
    "ja-l",
    "ja-r",
    "keyword",
    "ko-inline",
    "ko-l",
    "n-g",
    "ngd",
    "nobold",
    "non gloss",
    "non-gloss",
    "non gloss definition",
    "non-gloss definition",
    "nowrap",
    "overline",
    "pedia",
    "pedialite",
    "pedlink",
    "sc",
    "smallcaps",
    "spelink",
    "sub",
    "taxlink",
    "taxlink2",
    "taxlinknew",
    "underline",
    "unsupported",
    "upright",
    "vern",
    "w",
    "W",
    "wtorw",
    "zh-l",
    "zh-m",
}

# Templates that just return the second parameter
p2 = {
    "lang",
#    "quote",
#    "w2",
}

prefix1 = {
    "native or resident of"
}

quote1_with = {
    "en-archaic second-person singular of": "archaic second-person singular of",
    "en-archaic second-person singular past of": "archaic second-person singular past of",
    "en-archaic third-person singular of": "archaic third-person singular of",
    "en-comparative of": "comparative form of",
    "en-irregular plural of": "irregular plural of",
    "en-past of": "simple past tense and past participle of",
    "en-simple past of": "simple past of",
    "en-superlative of": "superlative of",
    "en-third person singular of": "third person singular of",
    "en-third-person singular of": "third-person singular of",
    "fr-post-1990": "post-1990 spelling of",
    "fr-post-1990-plural": "post-1990 plural of",
    "pt-verb-form-of": "inflection of",
    "pt-verb form of": "inflection of",
    "pt-apocopic-verb": "apocopic (used preceding the pronouns lo, la, los or las) form of",
}

form_of_alt = {
    "abbr of": "abbreviation of",
    "altcaps": "alternative letter-case form of",
    "alt caps": "alternative letter-case form of",
    "alt case": "alternative letter-case form of",
    "altcase": "alternative letter-case form of",
    "alt form": "alternative form of",
    "alt-form": "alternative form of",
    "altform": "alternative form of",
    "alt form of": "alternative form of",
    "alternative form": "alternative form of",
    "altname": "alternative name of",
    "alt sp": "alternative spelling of",
    "alt sp of": "alternative spelling of",
    "alt-sp": "alternative spelling of",
    "altspell": "alternative spelling of",
    "altspelling": "alternative spelling of",
    "alt spelling of": "alternative spelling of",
    "ao": "abbreviation of",
    "aphetic form": "aphetic form of",
    "aug of": "augmentative of",
    "cmn-erhua form of": "Mandarin erhua form of",
    "cretan dialect form of": "Cretan dialect form of",
    "cs-imperfective form of": "imperfective form of",
    "de-du contraction": "Contraction of",
    "de-form-adj": "adjective form of",
    "de-form-noun": "noun form of",
    "de-inflected form of": "inflected form of",
    "de-umlautless spelling of": "nonstandard umlautless spelling of",
    "de-zu-infinitive of": "zu-infinitive of",
    "dim of": "diminutive of",
    "el-Cretan dialect form of": "Cretan dialect form of",
    "el-Cypriot dialect form of": "Cypriot dialect form of",
    "el-Italiot dialect form of": "Italiot dialect form of",
    "el-Maniot dialect form of": "Maniot dialect form of",
    "euphemism of": "euphemism of",
    "gerund of": "gerund of",
    "honor alt case": "honorific alternative case of",
    "init of": "initialism of",
    "io": "initialism of",
    "la-praenominal abbreviation of": "praenominal abbreviation of",
    "missp": "misspelling of",
    "misspelling": "misspelling of",
    "obs form": "obsolete form of",
    "obs sp": "obsolete spelling of",
    "obs-sp": "obsolete spelling of",
    "obssp": "obsolete spelling of",
    "only-in": "only in",
    "onlyin": "only used in",
    "past participle of": "past participle of",
    "past participle": "past participle of",
    "phrasal verb": "A component in at least one phrasal verb:",
    "pinof": "pinyin reading of",
    "pinread": "pinyin reading of",
    "pronunciation spelling": "pronunciation spelling of",
    "rareform": "rare form of",
    "rare form": "rare form of",
    "ru-abbrev of": "abbreviation of",
    "ru-acronym of": "acronym of",
    "ru-alt-ё": "alternative form of",
    "ru-initialism of": "initialism of",
    "ru-pre-reform": "pre-reform form of",
    "singular of": "inflection of",
    "standspell": "standard spelling of",
    "stand sp": "standard spelling of",
    "standard spelling of": "standard spelling of",
    "syn of": "synonym of",
    "syn-of": "synonym of",
    "synof": "synonym of",
    "synonym": "synonym of",
    "zh-abbrev": "abbreviation of",
    "zh-also": "⇒",
    "zh-alt-form": "alternative form of",
    "zh-altterm": "alternative form of",
    "zh-character component": "the Chinese character component",
    "zh-classifier": "classifier for",
    "zh-erhua form of": "erhua form of",
    "zh-misspelling": "misspelling of",
    "zh-only": "only used in",
    "zh-only used in": "only used in",
    "zh-original": "original form of",
    "zh-see": "see",
    "zh-short": "abbreviation of",
    "zh-used in": "used in",
    "zh-used": "only used in",
}

form_of = {
    "abbreviation of",
    "abstract noun of",
    "accusative of",
    "accusative plural of",
    "accusative singular of",
    "acronym of",
    "active participle of",
    "agent noun of",
    "alternative case form of",
    "alternative form of",
    "alternative plural of",
    "alternative reconstruction of",
    "alternative spelling of",
    "alternative typography of",
    "aphetic form of",
    "apocopic form of",
    "archaic form of",
    "archaic inflection of",
    "archaic spelling of",
    "aspirate mutation of",
    "attributive form of",
    "augmentative of",
    "broad form of",
    "causative of",
    "clipping of",
    "combining form of",
    "comparative of",
    "construed with",
    "contraction of",
    "dated form of",
    "dated spelling of",
    "dative of",
    "dative plural of",
    "dative singular of",
    "definite singular of",
    "definite plural of",
    "deliberate misspelling of",
    "diminutive of",
    "dual of",
    "eclipsis of",
    "eggcorn of",
    "elative of",
    "ellipsis of",
    "elongated form of",
    "endearing diminutive of",
    "endearing form of",
    "equative of",
    "euphemistic form of",
    "euphemistic spelling of",
    "eye dialect of",
    "female equivalent of",
    "feminine of",
    "feminine plural of",
    "feminine plural past participle of",
    "feminine singular of",
    "feminine singular past participle of",
    "former name of",
    "frequentative of",
    "future participle of",
    "genitive of",
    "genitive plural of",
    "genitive singular of",
    "gerund of",
    "h-prothesis of",
    "hard mutation of",
    "harmonic variant of",
    "honorific alternative case form of",
    "imperative of",
    "imperfective form of",
    "indefinite plural of",
    "informal form of",
    "informal spelling of",
    "initialism of",
    "iterative of",
    "lenition of",
    "masculine noun of",
    "masculine of",
    "masculine plural of",
    "masculine plural past participle of",
    "medieval spelling of",
    "men's speech form of",
    "misconstruction of",
    "misromanization of",
    "misspelling of",
    "mixed mutation of",
    "nasal mutation of",
    "negative of",
    "neuter plural of",
    "neuter singular of",
    "neuter singular past participle of",
    "nomen sacrum form of",
    "nominalization of",
    "nominative plural of",
    "nonstandard form of",
    "nonstandard spelling of",
    "nuqtaless form of",
    "obsolete form of",
    "obsolete spelling of",
    "obsolete typography of",
    "only used in",
    "participle of",
    "passive of",
    "passive participle of",
    "passive past tense of",
    "past active participle of",
    "past participle form of",
    "past participle of",
    "past passive participle of",
    "past tense of",
    "pejorative of",
    "perfect participle of",
    "perfective form of",
    "plural of",
    "present active participle of",
    "present participle of",
    "present tense of",
    "pronunciation spelling of",
    "pronunciation variant of",
    "rare form of",
    "rare spelling of",
    "reflexive of",
    "romanization of",
    "short for",
    "singular of",
    "singulative of",
    "slender form of",
    "soft mutation of",
    "spelling of",
    "standard form of",
    "standard spelling of",
    "superlative attributive of",
    "superlative of",
    "superlative predicative of",
    "superseded spelling of",
    "supine of",
    "syncopic form of",
    "synonym of",
    "t-prothesis of",
    "uncommon form of",
    "uncommon spelling of",
    "verbal noun of",
    "vocative plural of",
    "vocative singular of",
}

replace_with = {
    "...": "[…]",
    "!": "|",
    "=": "=",
    "-a-o-e": "Gender-neutral e replaces the gendered endings/elements a and o.",
    "-a-o-x": "Gender-neutral x replaces the gendered endings/elements a and o.",
    "AD": "C.E.",
    "A.D.": "C.E.",
    "BC": "B.C.E.",
    "B.C.": "B.C.E.",
    "BCE": "B.C.E.",
    "B.C.E.": "B.C.E.",
    "CE": "C.E.",
    "C.E.": "C.E.",
    "es-note-noun-common-gender-a": "The noun {{PAGENAME}} is like several other Spanish nouns with a human referent and ending in a. The masculine articles and adjectives are used when the referent is known to be male, a group of males, a group of mixed or unknown gender, or an individual of unknown or unspecified gender. The feminine articles and adjectives are used if the referent is known to be female or a group of females.",
    "es-note-noun-f-starting-with-stressed-a": "* The feminine noun {{PAGENAME}} is like other feminine nouns starting with a stressed ''a'' sound in that it takes the definite article ''el'' (normally reserved for masculine nouns) in the singular when there is no intervening adjective:\n:: ''el {{PAGENAME}}''\n* However, if an adjective, even one that begins with a stressed ''a'' sound such as ''alta'' or ''ancha'', intervenes between the article and the noun, the article reverts to ''la''.",
    "es-demonstrative-accent-usage": "The unaccented form can function as a pronoun if it can be unambiguously deduced as such from context.",
    "es-note-noun-mf": "The noun {{PAGENAME}} is like most Spanish nouns with a human referent.  The masculine forms are used when the referent is known to be male, a group of males, a group of mixed or unknown gender, or an individual of unknown or unspecified gender.  The feminine forms are used if the referent is known to be female or a group of females.",
    "nb...": " […]",
    "sup": "^",
    "unk": "Unknown",
    "unknown": "Unknown",
}

# Special case handles for templates with characters that won't resolve to good function_names
handlers = {
    'U:es:false friend': Template.u_es_false_friend,
    "&lit": Template._and_lit,
    "m+": Template.m,
}

def expand_template(template, title, transclude_senses={}, cache=None):
    name = str(template.name).strip() #.lower()

    t = get_template_params(template)

    if name == "1":
        display = t.get(1, title)
        return display.capitalize().strip()
    if name in ignore or name.startswith("R:"):
        return ""
    if name in replace_with:
        return replace_with[name]
    if name in p1:
        display = t.get(1, title)
        return display

    if name in p2:
        return t[2]

    if name in prefix1:
        return name + " " + t[1]

    if name in quote1_with:
        text = quote1_with[name]
        return text + ' "' + t[1] + '"'

    if name in form_of:
        return Template._form_of(t, title, name)

    if name in form_of_alt:
        return Template._form_of(t, title, form_of_alt[name])

    if name in ["transclude sense", "transclude", "tcl"]:
        page = t[2]
        senseids = t.get("id")
        if not senseids:
            print(f"{title} transcludes sense without id: {template}", file=sys.stderr)
            return str(template).replace("\n", "\\n")

        transcludes = [transclude_senses.get((page, sid.strip())) for sid in senseids.split(",")]
        if not transcludes or not all(t for t in transcludes):
            #raise ValueError(f"{title} transcludes unknown sense: {template}", transcludes, senseids.split(","))
            print(f"{title} transcludes unknown sense: {template}", file=sys.stderr)
            return str(template).replace("\n", "\\n")

        res = []
        for transcluded in transcludes:
            wikt = mwparserfromhell.parse(transcluded)
            expand_templates(wikt, page, cache=cache)
            transcluded_text = str(wikt)

            # handle labels
            if transcluded_text.startswith("(") and ") " in transcluded_text:
                labels, transcluded_text = transcluded_text[1:].split(") ", 1)
            else:
                labels = None

            if labels:
                res.append(f"({labels}) {page} ({transcluded_text})")
            else:
                res.append(f"{page} ({transcluded_text})")

        return res[0]
        return "\\n".join(res)

    handler = None
    if name in handlers:
        handler = handlers[name]
    else:
        clean_name = re.sub(r"[+\s-]", "_", name.lower())
        if len(clean_name) > 2 and clean_name[2] == "_" and clean_name[:2] in Template.lang2:
            lang_handler = getattr(Template.lang2[clean_name[:2]], clean_name)
            if lang_handler:
                return lang_handler(t, title)

        handler = getattr(Template, clean_name, None)

    if not handler:
        #with open("unknown_templates.txt", "a") as outfile:
        #    print(f"{t.name.strip()}", file=outfile)
        print(f"{title} uses unknown template: {template}", file=sys.stderr)
        return str(template).replace("\n", "\\n")
        return ""

    if name in Cache.TEMPLATES:
        if not cache:
            cache = get_default_cachedb()
            #print("Template cache not specified, using default:", cache, file=sys.stderr)
        return handler(t, title, cache)

    return handler(t, title)


def expand_templates(wikt, title, transclude_senses={}, cache=None):
    try:
        for t in reversed(wikt.filter_templates()):
            new = expand_template(t, title, transclude_senses, cache)
            new = new.replace("{{PAGENAME}}", str(title))
            wikt.replace(t, new)

    except Exception as ex:
        print(f"{title} failed processing: {wikt}", file=sys.stderr)
        raise ex


def iter_templates(text):
    yield from mwparserfromhell.parse(text).ifilter_templates()
