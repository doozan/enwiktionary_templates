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

import re

from .labeldata import data as labeldata

class Template():

    @staticmethod
    def _default(t, title):
        #print(f"{title} uses unknown template: {t}")
        return ""

    def a(t, title):
        #print(f"{title} uses bad template: {t}")
        return ""

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
    def es_compound_of(t,title):
        if t.has(5):
            return f"compound form of {t.get(1)}{t.get(2)}+{t.get(4)}+{t.get(5)}"
        if t.has(4):
            return f"compound form of {t.get(1)}{t.get(2)}+{t.get(4)}"

        if t.has(2):
            return f"compound form of {t.get(1)}{t.get(2)}"

        return ""

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
        display = ""
        gloss = ""
        if t.has(3):
            display = str(t.get(3))
        if not display and t.has(2):
            display = str(t.get(2))
        for p in ["gloss", "t", "4"]:
            if t.has(p):
                gloss = str(t.get(p).value)
        if gloss:
            gloss = " (" + str(gloss) + ")"

        return display+gloss

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
    def qualifier(t, title):
        params = [ str(p.value) for p in t.params if str(p.name).isdigit() ]
        return "(" + ", ".join(params) + ")"
    q = i = qual = qualifier

    @staticmethod
    def sense(t, title):
        return "(" + str(t.get(1)) + ")"
    s = sense

    @staticmethod
    def surname(t, title):
        return "surname"

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
    "attention",
    "attn",
    "C",
    "c",
    "categorize",
    "catlangname",
    "catlangcode",
    "cite",
    "cite-web",
    "cite news",
    "cln",
    "DEFAULTSORT",
    "ISBN",
    "rfclarify",
    "rfex",
    "top",
    "topics",
}

# Templates that just return the first paramater
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
    "overline",
    "pedia",
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

p2 = {
#    "lang",
    "cog",
#    "quote",
#    "w2",
}

prefix1 = {
    "native or resident of"
}

prefix1_with = {
    "es-verb form of": "inflection of",
}

# Templates that wrap the second paramater with text other than the template name
prefix2_with = {
    "abb": "abbreviation of",
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
    "clip": "clipping o",
    "clip of": "clipping of",
    "clipping": "clipping of",
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
    "ellipse of": "ellipsis of",
    "ellipsis": "ellipsis of",
    "el-Maniot dialect form of": "Maniot dialect form of",
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
    "honor alt case": "honorific alternative case of",
    "indeclinable": "indecl",
    "infl of": "inflection of",
    "init of": "initialism of",
    "io": "initialism of",
    "la-praenominal abbreviation of": "praenominal abbreviation of",
    "missp": "misspelling of",
    "obs form": "obsolete form of",
    "obs sp": "obsolete spelling of",
    "obs-sp": "obsolete spelling of",
    "obssp": "obsolete spelling of",
    "only-in": "only in",
    "onlyin": "only used in",
    "past participle": "past participle of",
    "pf.": "pf",
    "phrasal verb": "A component in at least one phrasal verb:",
    "pinof": "pinyin reading of",
    "pinread": "pinyin reading of",
    "plural": "p",
    "pronunciation spelling": "pronunciation spelling of",
    "pt-apocopic-verb": "apocopic (used preceding the pronouns lo, la, los or las) form of",
    "pt-verb-form-of": "verb form of",
    "rareform": "rare form of",
    "ru-abbrev of": "abbreviation of",
    "ru-acronym of": "acronym of",
    "ru-alt-ё": "alternative form of",
    "ru-initialism of": "initialism of",
    "ru-pre-reform": "pre-reform form of",
    "standspell": "standard spelling of",
    "stand sp": "standard spelling of",
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
prefix2 = {
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
    "clipping of",
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
    "ellipsis of",
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
    "feminine singular of",
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

replace_with = {
    "es-demonstrative-accent-usage": "The unaccented form can function as a pronoun if it can be unambiguously deduced as such from context."
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

    if name in prefix1_with:
        text = prefix1_with[name]
        return text + " " + str(t.get(1)).strip()

    if name in prefix2:
        return name + " " + str(t.get(2)).strip()

    if name in prefix2_with:
        text = prefix2_with[name]
        if not t.has(2):
            raise ValueError(t)
        return text + " " + str(t.get(2)).strip()

    if name == "&lit":
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

    name = re.sub(r"[\s-]", "_", str(t.name)).lower()
    handler = getattr(Template, name, getattr(Template, "_default"))
    return handler(t, title)

def expand_templates(wikt, title):
    for t in reversed(wikt.filter_templates()):
        new = expand_template(t, title)
#        print("old", t)
#        print("new", new)
        wikt.replace(t, new)
