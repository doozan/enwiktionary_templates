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

from enwiktionary_parser.languages.all_ids import languages as all_langs
from .etydata import data as ety_langs
from .labeldata import data as labeldata
from .get_template_params import get_template_params

class Template():

    ##import enwiktionary_templates.es as _es
    lang2 = {}
    #lang2["es"] = _es

    from .es import es_compound_of, es_conj, es_noun, es_proper_noun, es_adj, es_adj_sup

    @staticmethod
    def _default(t, title):
        print(f"{title} uses unknown template: {t}", file=sys.stderr)
        return str(t)
        #return ""

    @staticmethod
    def _and_lit(t, template):
        res = []
        if t.has("qualifier"):
            res.append(str(t.get("qualifier")))
            res.append("Used other than with a figurative sense or idiom")
        else:
            res.append("used other than as an idiom")

        x = 2
        while t.has(x):
            val = str(t.get(x))
            alt = t.get("alt"+str(x-1)) if t.has("alt"+str(x-1)) else None
            if alt:
                res.append(f"[[{val}|{alt}]]")
            else:
                res.append(f"[[{val}]]")
            x+=1

        if t.has("nodot") and str(t.get("nodot")):
            return " ".join(res)
        else:
            dot = str(t.get("dot").value) if t.has("dot") else "."
            return " ".join(res) + dot

    @staticmethod
    def affix(t, title):
        res = []
        p = 2
        while t.has(p) and str(t.get(p).value):
            res.append(str(t.get(p).value))
            p += 1

        return " + ".join(res)

    af = affix
    compound = affix
    com = affix
    confix = affix
    blend = affix

    @staticmethod
    def back_formation(t, title):
        return Template.__etyl_misc_variant(t, title, "back formation of")

    @staticmethod
    def __lang2_etyl(t, title, pre_text=None):
        source = Template.__get_lang(str(t.get(2).value))
        display = next((str(t.get(p).value) for p in ["alt", "4", "3"] if t.has(p) and str(t.get(p).value)), None)
        gloss = next((str(t.get(p).value) for p in ["t", "gloss", "5"] if t.has(p) and str(t.get(p).value)), None)

        return Template.__format_etyl(t, pre_text, source, display, gloss)

    @staticmethod
    def learned_borrowing(t, title):
        return Template.__lang2_etyl(t, title, "learned borrowing from")
    lbor = learned_borrowing

    @staticmethod
    def semi_learned_borrowing(t, title):
        return Template.__lang2_etyl(t, title, "semi-learned borrowing from")
    slbor = semi_learned_borrowing

    @staticmethod
    def orthorgraphic_borrowing(t, title):
        return Template.__lang2_etyl(t, title, "orthographic borrowing from")
    obor = orthorgraphic_borrowing

    @staticmethod
    def semantic_loan(t, title):
        return Template.__lang2_etyl(t, title, "semantic loan from")
    sl = semantic_loan

    @staticmethod
    def unadapted_borrowing(t, title):
        return Template.__lang2_etyl(t, title, "unadapted borrowing from")
    ubor = unadapted_borrowing

    @staticmethod
    def calque(t, title):
        return Template.__lang2_etyl(t, title, "calque of")

    cal = calque
    clq = calque

    @staticmethod
    def clipping(t, title):
        return Template.__etyl_misc_variant(t, title, "clipping of")
    clip = clipping
    clipping_of = clipping

    @staticmethod
    def __get_lang(lang_id):
        lang_id = lang_id.strip('\n .')
        src_lang = all_langs.get(lang_id.lower())
        if not src_lang:
            src_lang = ety_langs.get(lang_id, {}).get("canonicalName")
        if not src_lang:
            src_lang = lang_id
        return src_lang

    @staticmethod
    def derived(t, title):
        return Template.__lang2_etyl(t, title)

    der = derived
    borrowed = derived
    bor = borrowed
    inherited = derived
    inh = derived

    @staticmethod
    def __etyl_misc_variant(t, title, pre_text):
        display = next((str(t.get(p).value) for p in ["alt", "2", "3"] if t.has(p) and str(t.get(p).value)), title)
        gloss = next((str(t.get(p).value) for p in ["gloss", "t", "4"] if t.has(p) and str(t.get(p).value)), None)
        return Template.__format_etyl(t, pre_text, None, display, gloss)

    @staticmethod
    def __format_etyl(t, pre_text, lang, display, gloss):
        res = []
        if not t.has("notext") and pre_text:
            if t.has("nocap"):
                res.append(f"{pre_text}")
            else:
                res.append(f"{pre_text.capitalize()}")

        if lang:
            res.append(lang)

        if display and display != "-":
            res.append(f'"{display}"')
        if gloss and gloss != "-":
            res.append("(“" + str(gloss) + "”)")

        return " ".join(res)

    @staticmethod
    def deverbal(t, title):
        return Template.__etyl_misc_variant(t, title, "deverbal of")

    @staticmethod
    def doublet(t, title):
        text = ""
        if not t.has("notext"):
            text = "Doublet of " if not t.has("nocap") else "doublet of "

        p = 2
        res = []
        while t.has(p) and str(t.get(p).value):
            res.append(str(t.get(p).value))
            p += 1

        return text + ", ".join(res)

    @staticmethod
    def ellipsis(t, title):
        return Template.__etyl_misc_variant(t, title, "ellipsis of")
    ellipsis_of = ellipsis

    @staticmethod
    def etyl(t, title):
        src_lang_id = str(t.get(1)).strip('\n .')
        src_lang = all_langs.get(src_lang_id.lower())
        if not src_lang:
            src_lang = ety_langs.get(src_lang_id, {}).get("canonicalName")
        if not src_lang:
            src_lang = src_lang_id

        return src_lang

    @staticmethod
    def u_es_false_friend(t, title):
        res = []
        if t.has("nocap"):
            res.append(title)
        else:
            res.append(title[0].upper() + title[1:])

        res.append("is a false friend and does not mean")

        if t.has("en"):
            if t.has("gloss"):
                res.append(str(t.get("en").value))
                res.append(f"in the sense of ''{t.get('gloss').value}''.")
            else:
                res.append(f"{t.get('en').value}.")

        elif t.has("gloss"):
            res.append(f"''{t.get('gloss').value}''")
            res.append("in Spanish.")
        else:
            res.append(f"the same as the English word for {title}.")

        if t.has(1):
            res.append("\nThe Spanish word for")
            if t.has("en"):
                res.append(str(t.get("en").value))
                if t.has("gloss"):
                    res.append(f"in that sense")
            else:
                res.append(title)

            res.append(f"is ''{t.get(1).value}''.")

        return " ".join(res)

    @staticmethod
    def frac(t, title):
        if t.has(3):
            return f"{t.get(1)} {t.get(2)}/{t.get(3)}"
        if t.has(2):
            return f"{t.get(1)}/{t.get(2)}"
        return f"1/{t.get(1)}"

    @staticmethod
    def form_of(t, title):
        return f"{t.get(2)} form of {t.get(3)}"

    @staticmethod
    def g(t, title):
        res = "{" + " or ".join(map(str.strip, map(str, t.params))) + "}"
        res = re.sub("p", "pl", res)
        res = re.sub("-", " ", res)
        return res

    @staticmethod
    def gloss(t, title):
        return "(" + ", ".join(map(str.strip, map(str, t.params))) + ")"
    gl = gloss

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

        if t.has("intr") and str(t.get("intr").value).strip():
            indtr += "[[Appendix:Glossary#intransitive|intransitive]], or "

        while t.has(i):
            val = str(t.get(i)).strip()
            if val.startswith("."):
                labels.append(val[1:])
            elif val == ";":
                andwith = True
                if not t.has("qual"+str(i-1)) or not str(t.get("qual"+str(i-1)).value).strip():
                    indtr += " and with "
                else:
                    indtr += " and " + str(t.get("qual"+str(i-1)).value).strip() + " with "
            else:
                if not first:
                    if andwith:
                        andwith = False
                    else:
                        indtr += " or "
                else:
                    if t.has("cop") and t.has("ditr"):
                        indtr += "[[Appendix:Glossary#ditransitive|ditransitive]], [[Appendix:Glossary#copulative|copulative]] with "
                    elif t.has("cop"):
                        indtr += "[[Appendix:Glossary#copulative|copulative}} with "
                    elif t.has("ditr"):
                        indtr += "[[Appendix:Glossary#ditransitive|ditransitive]] with the indirect object taking "
                    elif t.has("aux"):
                        indtr += "[[Appendix:Glossary#auxiliary|auxiliary]] with "
                    else:
                        indtr += "[[Appendix:Glossary#transitive|transitive]] with "
                    first = False
                if val.startswith("-"):
                    indtr += val[1:]
                else:
                    indtr += "'''[[" + val + "]]'''"

                if t.has("qual"+str(i-1)):
                    indtr += "(" + str(t.get("qual"+str(i-1)).value).strip() + ")"

            i += 1
        if t.has("direct") and str(t.get("direct").value).strip():
            if t.has("ditr") and str(t.get("ditr").value).strip():
                indtr += " or no preposition"
            else:
                indtr += " or with no preposition"
            if t.has("qualdirect") and str(t.get("qualdirect").value).strip():
                indtr += " (" + str(t.get("qualdirect").value).strip() + ")"

        if t.has("aux") and str(t.get("aux").value).strip():
            indtr += " and a verb in the " + str(t.get("aux").value).strip()
        elif t.has("cop") and t.has("ditr"):
            indtr += " for the second object"

        labels.append(indtr)
        res = Template._joinlabels(labels)
        if not res.strip():
            return ""
        return f"({res})"


    @staticmethod
    def label(t, title):
        labels = [ str(p.value).strip() for p in t.params if str(p.name).isdigit() and p.name != "1" ]
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
            if t.has(4):
                res += ": " + str(t.get(4))
            x = 5
            while t.has(x):
                res += ", " + str(t.get(x))
                x+=1

#        if t.get(2) in ["diacritic"]:


        return res

    @staticmethod
    def link(t, title):
        display = ""
        gloss = ""
        for p in ["2", "3", "tr"]:
            if t.has(p):
                text = str(t.get(p).value)
                if text:
                    display = str(t.get(p).value)
        #for p in ["gloss", "t", "4"]: # mbcompat, ignore t
        for p in ["gloss", "4"]:
            if t.has(p):
                gloss = str(t.get(p).value)
        if gloss:
            gloss = " (" + str(gloss) + ")"

        return str(display)+gloss
    l = ll = link

    @staticmethod
    def m(t, title):
        res = []
        display = None
        if t.has(3):
            display = str(t.get(3))
        if not display and t.has(2):
            display = str(t.get(2))

        if display:
            res.append("''" + display + "''")

        gloss = None
        for p in ["gloss", "t", "4"]:
            if t.has(p):
                gloss = str(t.get(p).value)
        if gloss:
            res.append("(“" + str(gloss) + "”)")

        return " ".join(res)
    mention = m

    @staticmethod
    def named_after(t, title):
        res = []
        if t.has('alt'):
            res.append(str(t.get('alt').value))
        else:
            if t.has("nocap"):
                res.append("named after")
            else:
                res.append("Named after")

        if t.has("alt"):
            res.append(str(t.get('alt').value))
        else:
            if t.has("nationality"):
                res.append(str(t.get('nationality').value))
            elif t.has("nat"):
                res.append(str(t.get('nat').value))
            if t.has("occupation"):
                res.append(str(t.get('occupation').value))
            elif t.has("occ"):
                res.append(str(t.get('occ').value))

        if t.has(2):
            res.append(str(t.get(2).value))
        else:
            res.append("an unknown person")

        if t.has("tr"):
            res.append("(" + str(t.get('tr').value) + ")")

        if t.has("born") or t.has("died"):
            lived = ""
            if t.has("born"):
                t.lived = str(t.get('born').value) + "-"
            else:
                t.lived = "?-"
            if t.has("died"):
                t.lived += "-" + str(t.get('died').value)

        return " ".join(res)

    @staticmethod
    def non_gloss_definition(t, title):
        return str(t.get(1))
    non_gloss = ngd = n_g = non_gloss_definition

    def place(t, title):
        if t.has(2) and str(t.get(2)):
            return title + " (" + str(t.get(2)) + ")"
        else:
            return title + " (place)"

    @staticmethod
    def pagename(t, title):
        return title

    @staticmethod
    def prefix(t, title):
        return f"{t.get(2)}- + {t.get(3)}"

    pre = prefix

    @staticmethod
    def onomatopoeic(t, title):
        if t.has("title"):
            return str(t.get("title").value)
        if t.has("notext"):
            return ""
        if t.has("nocap"):
            return "onomatopoeic"
        return "Onomatopoeic"

    onom = onomatopoeic

    @staticmethod
    def qualifier(t, title):
        params = [ str(p.value) for p in t.params if str(p.name).isdigit() ]
        return "(" + ", ".join(params) + ")"
    q = i = qual = qualifier

    @staticmethod
    def qf(t, title):
        return "(" + str(t.get(1)) + ")"

    @staticmethod
    def rebracketing(t, title):
        return Template.__etyl_misc_variant(t, title, "rebracketing of")

    @staticmethod
    def reduplication(t, title):
        return Template.__etyl_misc_variant(t, title, "reduplication of")

    @staticmethod
    def sense(t, title):
        return "(" + str(t.get(1)) + ")"
    s = sense

    @staticmethod
    def suffix(t, title):
        return f"{t.get(2)} + -{t.get(3)}"

    suf = suffix

    @staticmethod
    def surname(t, title):
        return "surname"

    @staticmethod
    def univerbation(t, title):
        res = [f"Univerbation of {t.get(2)}"]
        count = 3
        while t.has(count):
            res.append(str(t.get(count)))
            count += 1
        return " + ".join(res)

    @staticmethod
    def ux(t, title):
        res = []
        for p in (2,3,"t"):
            if t.has(p):
                res.append(str(t.get(p).value))
        return " ― ".join(res)
    eg = uxi = usex = ux

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
    "cite-book",
    "Cite book",
    "cite book",
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
    "es-adj-form",
    "es-adj form",
    "es-adj form of",
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
    "es-suffix",
    "es-verb",
    "es-verb-form",
    "ISBN",
    "nbsp",
    "nonlemma",
    "rfclarify",
    "rfex",
    "rfv-etym",
    "rfc-sense",
    "rfd-sense",
    "rfd-redundant",
    "rfm-sense",
    "rfquotek",
    "rfquote-sense",
    "rfv-sense",
    "tea room sense",
    "t2i-Egyd",
    "top",
    "topics",
    "U:es:relative pronouns",
    "Wikipedia",
    "wikipedia",
    "wp",
}

# Templates that just return the first parameter
p1 = {
    "def",
    "def-date",
    "defdt",
    "defdate",
    "en-phrase",
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
    "swp",
    "taxlink",
    "taxlink2",
    "taxlinknew",
    "unsupported",
    "upright",
    "vern",
    "w",
    "W",
    "wtorw",
    "zh-m",
}

# Templates that just return the second parameter
p2 = {
    "lang",
    "cog",
    "noncog",
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
    "es-verb form of": "inflection of",
    "pt-verb-form-of": "inflection of",
    "pt-apocopic-verb": "apocopic (used preceding the pronouns lo, la, los or las) form of",
}

# Templates that wrap the second parameter with text other than the template name
quote2_with = {
    "abb": "abbreviation of",
    "abbrev of": "abbreviation of",
    "abbreviation": "abbreviation of",
    "abbreviation-old": "old abbreviation of",
    "abbr of": "abbreviation of",
    "adj form of": "adjective form of",
    "altcaps": "alternative letter-case form of",
    "alt case": "alternative case form of",
    "altcase": "alternative letter-case form of",
    "alt form": "alternative form of",
    "alt-form": "alternative form of",
    "altform": "alternative form of",

    "alt form of": "alternative form of",
    "altname": "alternative name of",
    "alt sp": "alternative spelling of",
    "alt-sp": "alternative spelling of",
    "altspell": "alternative spelling of",
    "altspelling": "alternative spelling of",
    "ao": "abbreviation of",
    "back-form": "back formation from",
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
    "fr-post-1990": "post-1990 spelling of",
    "gerund of": "gerund of",
    "honor alt case": "honorific alternative case of",
    "infl of": "inflection of",
    "init of": "initialism of",
    "io": "initialism of",
    "la-praenominal abbreviation of": "praenominal abbreviation of",
    "missp": "misspelling of",
    "misspelling": "misspelling of",
    "noun form of": "inflection of",
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

# Templates that return template_name + second parameter
quote2 = {
    "abbreviation of",
    "acronym of",
    "agent noun of",
    "alternate form of",
    "alternate spelling of",
    "alternative capitalization of",
    "alternative case form of",
    "alternative form of",
    "alternative name of",
    "alternative plural of",
    "alternative spelling of",
    "alternative term for",
    "alternative typography of",
    "aphetic form of",
    "apocopic form of",
    "archaic form of",
    "archaic spelling of",
    "attributive form of",
    "attributive of",
    "augmentative of",
    "blend of",
    "causative of",
    "common misspelling of",
    "comparative form of",
    "comparative of",
    "construed with",
    "contraction of",
    "dated form of",
    "dated spelling of",
    "definite of",
    "definite singular of",
    "deliberate misspelling of",
    "diminutive of",
    "diminutive plural of",
    "early form of",
    "eggcorn of",
    "elongated form of",
    "endearing form of",
    "euphemistic form of",
    "euphemistic spelling of",
    "eye dialect",
    "eye dialect of",
    "eye-dialect of",
    "female equivalent of",
    "feminine equivalent of",
    "feminine noun of",
    "feminine of",
    "feminine plural of",
    "feminine plural past participle of",
    "feminine singular of",
    "feminine singular past participle of",
    "former name of",
    "frequentative of",
    "imperfective form of",
    "indefinite plural of",
    "inflection of",
    "informal form of",
    "informal spelling of",
    "initialism of",
    "iterative of",
    "late form of",
    "masculine noun of",
    "masculine of",
    "masculine plural of",
    "masculine singular past participle of",
    "masculine plural past participle of",
    "medieval spelling of",
    "misconstruction of",
    "misspelling of",
    "misspelling form of",
    "negative of",
    "neuter of",
    "neuter singular of",
    "nominalization of",
    "nonstandard form of",
    "nonstandard spelling of",
    "obsolete form of",
    "obsolete form of",
    "obsolete spelling of",
    "obsolete typography of",
    "only in",
    "only used in",
    "participle of",
    "past of",
    "past participle form of",
    "pejorative of",
    "perfective form of",
    "perfect participle of",
    "plural of",
    "present active participle of",
    "present participle of",
    "present of",
    "present tense of",
    "pronunciation respelling of",
    "pronunciation spelling of",
    "rare form of",
    "rare spelling of",
    "reflexive of",
    "second-person singular of",
    "second-person singular past of",
    "short for",
    "short for",
    "short form of",
    "short form of",
    "short of",
    "singulative of",
    "spelling of",
    "standard form of",
    "substantivisation of",
    "superlative form of",
    "superlative of",
    "superseded form of",
    "superseded spelling of",
    "supine of",
    "syncopic form of",
    "synonym of",
    "uncommon form of",
    "verbal noun of",
}

quote3 = {
    "form of",
}

replace_with = {
    "...": "[…]",
    "!": "|",
    "=": "=",
    "-a-o-e": "Gender-neutral e replaces the gendered endings/elements a and o.",
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
    "sup": "^",
    "unk": "Unknown",
    "unknown": "Unknown",
}

handlers = {
    'U:es:false friend': Template.u_es_false_friend,
    "&lit": Template._and_lit,
    "m+": Template.m,
}

def expand_template(t, title):
    name = str(t.name).strip() #.lower()

    if name == "1":
        return str(t.get(1)).capitalize().strip()
    if name in ignore or name.startswith("R:"):
        return ""
    if name in replace_with:
        return replace_with[name]
    if name in p1:
        return str(t.get(1)).strip()
    if name in p2:
        return str(t.get(2)).strip()

    if name in prefix1:
        return name + " " + str(t.get(1)).strip()

    if name in quote1_with:
        text = quote1_with[name]
        return text + ' "' + str(t.get(1)).strip() + '"'

    if name in quote2:
        return name + ' "' + str(t.get(2)).strip() + '"'

    if name in quote2_with:
        text = quote2_with[name]
        if not t.has(2):
            raise ValueError("missing paramater 2", t)
        return text + ' "' + str(t.get(2)).strip() + '"'

    if name in quote3:
        return name + ' "' + str(t.get(3)).strip() + '"'

    handler = None
    if name in handlers:
        handler = handlers[name]
    else:
        name = re.sub(r"[\s-]", "_", name.lower())
        if len(name) > 2 and name[2] == "_" and name[:2] in Template.lang2:
            lang_handler = getattr(Template.lang2[name[:2]], name)
            if lang_handler:
                return lang_handler(t, title)

        handler = getattr(Template, name, getattr(Template, "_default"))
    return handler(t, title)


def expand_templates(wikt, title):
    for t in reversed(wikt.filter_templates()):
        new = expand_template(t, title)
        new = new.replace("{{PAGENAME}}", str(title))
        wikt.replace(t, new)


def iter_templates(text):
    yield from mwparserfromhell.parse(text).ifilter_templates()
