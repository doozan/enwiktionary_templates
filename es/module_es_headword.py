#
# Copyright (c) 2021 Jeff Doozan
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
Data and utilities for processing Spanish sections of enwiktionary

Based on https://en.wiktionary.org/wiki/Module%3Aes%2Dheadword
Revision 62271320, 21:09, 28 March 2021
"""

import re

pos_functions = {}


TEMPC1 = u'\uFFF1'
TEMPC2 = u'\uFFF2'
TEMPV1 = u'\uFFF3'
vowel = "aeiouáéíóúý" + TEMPV1
V = f"[{vowel}]"
SV = "[áéíóúý]" # stressed vowel
W = "[iyuw]" # glide
C = f"[^{vowel}.]"

suffix_categories = (
    "adjectives",
    "adverbs",
    "nouns",
    "verbs"
)

def rfind(string, pattern):
    return re.search(pattern, string)

def rmatch(string, pattern):
    return re.match(pattern, string)

def rsub(string, pattern, replacement):
    return re.sub(pattern, replacement, string)

def rsplit(string, pattern):
    return re.split(pattern, string)

# apply rsub() repeatedly until no change
def rsub_repeatedly(term, foo, bar):
    while True:
        new_term = rsub(term, foo, bar)
        if new_term == term:
            return term
        term = new_term

def is_stressed(word):
    return any(v for v in SV if v in word)

remove_stress = {
    "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ý": "y"
}
add_stress = {
    "a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "y": "ý"
}

allowed_special_indicators = (
    "first",
    "first-second",
    "first-last",
    "second",
    "last",
    "each",
)

prepositions = (
    "al?",
    "del?",
    "como",
    "con",
    "en",
    "para",
    "por",
)

def get_special_indicator(form):
    if "+" in form:
        form = rsub(form, r"^.*?\+", "")
        if not form in allowed_special_indicators:
            raise ValueError("Special inflection indicator beginning with '+' can only be ", indicators.sorted(), ": +", form)
        return form

# Syllabify a word. This implements the full syllabification algorithm, based on the corresponding code
# in [[Module:es-pronunc]]. This is more than is needed for the purpose of this module, which doesn't
# care so much about syllable boundaries, but won't hurt.
def syllabify(word):

    DIV = u'\uFFF4'

    word = DIV + word + DIV
    # gu/qu + front vowel; make sure we treat the u as a consonant; a following
    # i should not be treated as a consonant ([[alguien]] would become ''álguienes''
    # if pluralized)
    word = rsub(word, "([gq])u([eiéí])", r"\1" + TEMPC2 + r"\2")
    vowel_to_glide = { "i": TEMPC1, "u": TEMPC2 }
    # i and u between vowels should behave like consonants ([[paranoia]], [[baiano]], [[abreuense]],
    # [[alauita]], [[Malaui]], etc.)
    word = rsub_repeatedly(word, "(" + V + ")([iu])(" + V + ")",
        lambda m: m.group(1) + vowel_to_glide[m.group(2)] + m.group(3)
    )
    # y between consonants or after a consonant at the end of the word should behave like a vowel
    # ([[ankylosaurio]], [[cryptomeria]], [[brandy]], [[cherry]], etc.)
    word = rsub_repeatedly(word, "(" + C + ")y(" + C + ")",
        rf"\1{TEMPV1}\2")

    word = rsub_repeatedly(word, "(" + V + ")(" + C + W + "?" + V + ")", r"\1.\2")
    word = rsub_repeatedly(word, "(" + V + C + ")(" + C + V + ")", r"\1.\2")
    word = rsub_repeatedly(word, "(" + V + C + "+)(" + C + C + V + ")", r"\1.\2")
    word = rsub(word, "([pbcktdg])%.([lr])", r".\1\2")
    word = rsub_repeatedly(word, "(" + C + ")%.s(" + C + ")", r"\1s.\2")
    # Any aeo, or stressed iu, should be syllabically divided from a following aeo or stressed iu.
    word = rsub_repeatedly(word, "([aeoáéíóúý])([aeoáéíóúý])", r"\1.\2")
    word = rsub_repeatedly(word, "([ií])([ií])", r"\1.\2")
    word = rsub_repeatedly(word, "([uú])([uú])", r"\1.\2")
    word = rsub(word, DIV, "")
    word = rsub(word, TEMPC1, "i")
    word = rsub(word, TEMPC2, "u")
    word = rsub(word, TEMPV1, "y")
    return word


def add_endings(bases, endings):
    retval = []
    if isinstance(bases, str):
        bases = [bases]
    if isinstance(endings, str):
        endings = [endings]
    for base in bases:
        for ending in endings:
            retval.append(base + ending)
    return retval

def handle_multiword(form, special, inflect):
    if special == "first":
        m = rmatch(form, "^(.+?)( .*)$")
        if not m:
            raise ValueError("Special indicator 'first' can only be used with a multiword term: " + form)
        first, rest = m.groups()
        return add_endings(inflect(first), rest)
    elif special == "second":
        m = rmatch(form, "^([^ ]+ )([^ ]+)( .*)$")
        if not m:
            raise ValueError("Special indicator 'second' can only be used with a term with three or more words: " + form)
        first, second, rest = m.groups()
        return add_endings(add_endings({first}, inflect(second)), rest)
    elif special == "first-second":
        m = rmatch(form, "^([^ ]+)( )([^ ]+)( .*)$")
        if not first:
            raise ValueError("Special indicator 'first-second' can only be used with a term with three or more words: " + form)
        first, space, second, rest = m.groups()
        return add_endings(add_endings(add_endings(inflect(first), space), inflect(second)), rest)
    elif special == "each":
        terms = rsplit(form, " ")
        if len(terms) < 2:
            raise ValueError("Special indicator 'each' can only be used with a multiword term: " + form)

        for i, term in terms.items():
            terms[i] = inflect(term)
            if i > 1:
                terms[i] = add_endings(" ", terms[i])

        result = ""
        for term in terms:
            result = add_endings(result, term)

        return result
    elif special == "first-last":
        m = rmatch(form, "^(.+?)( .* )(.+?)$")
        if not m:
            m = rmatch(form, "^(.+?)( )(.*)$")
            if not m:
                raise ValueError("Special indicator 'first-last' can only be used with a multiword term: " + form)

        first, middle, last = m.groups()
        return add_endings(add_endings(inflect(first), middle), inflect(last))
    elif special == "last":
        m = rmatch(form, "^(.* )(.+?)$")
        if not m:
            ValueError("Special indicator 'last' can only be used with a multiword term: " + form)

        rest, last = m.groups()
        return add_endings(rest, inflect(last))
    elif special:
        ValueError("Unrecognized special=" + special)

    if " " in form:
        # check for prepositions in the middle of the word; do it this way so we can handle
        # more than one word before the preposition (and usually inflect each word)
        for prep in prepositions:
            m = rmatch(form, "^(.+?)( " + prep + ")( .*)$")
            if m:
                first, space_prep, rest = m.groups()
                return add_endings(inflect(first), space_prep + rest)

        # multiword expressions default to first-last
        return handle_multiword(form, "first-last", inflect)

def make_plural(form, special=None):

    print("make plural", form, special)
    retval = handle_multiword(form, special, make_plural)
    if retval:
        return retval

    # ends in unstressed vowel or á, é, ó
    if rfind(form, "[aeiouáéó]$"):
       return [form + "s"]

    # ends in í or ú
    if rfind(form, "[íú]$"):
        return [form + "s", form + "es"]

    # ends in a vowel + z
    if rfind(form, V + "z$"):
        return [ rsub(form, "z$", "ces") ]

    # ends in tz
    if rfind(form, "tz$"):
        return [form]

    syllables = rsplit(syllabify(form), r"\.")

    # ends in s or x with more than 1 syllable, last syllable unstressed
    if len(syllables) > 1 and rfind(form, "[sx]$") and not rfind(syllables[-1], SV):
        return [form]

    # ends in l, r, n, d, z, or j with 3 or more syllables, accented on third to last syllable
    if len(syllables) > 2 and rfind(form, "[lrndzj]$") and rfind(syllables[-3], SV):
        return [form]

    # ends in a stressed vowel + consonant
    if rfind(form, SV + C + "$"):
        # remove stress add + es
        return [ rsub(form, "(.)(.)$",
            lambda m: remove_stress[m.group(1)] + m.group(2) + "es") ]

    # ends in a vowel + y, l, r, n, d, j, s, x
    if rfind(form, "[aeiou][ylrndjsx]$"):
        # two or more syllables: add stress mark to plural; e.g. joven -> jóvenes
        if len(syllables) > 1 and rfind(form, "n$"):
            # don't do anything if syllable already stressed
            if not rfind(syllables[-2], SV):
                # prefer to accent an a/e/o in case of a diphthong or triphthong; otherwise, do the
                # last i or u in case of a diphthong ui or iu
                if rfind(syllables[-2], "[aeo]"):
                    syllables[-2] = syllables[-2].replace("a", "á")
                    syllables[-2] = syllables[-2].replace("e", "é")
                    syllables[-2] = syllables[-2].replace("o", "ó")
                else:
                    syllables[(syllables) - 1] = rsub(syllables[len(syllables) - 1], "^(.*)([iu])",
                        lambda m: m.group(1) + add_stress[m.group(2)])
            return ["".join(syllables) + "es"]

        return [form + "es"]

    # ends in a vowel + ch
    if rfind(form, "[aeiou]ch$"):
        return [form + "es"]

    # ends in two consonants
    if rfind(form, C + C + "$"):
        return [form + "s"]

    # ends in a vowel + consonant other than l, r, n, d, z, j, s, or x
    if rfind(form, "[aeiou][^aeioulrndzjsx]$"):
        return [form + "s"]


def make_feminine(form, special=None):
    retval = handle_multiword(form, special, make_feminine)
    if retval:
        if len(retval) != 1:
            raise ValueError("Internal error: Should have one return value for make_feminine: ", retval)
        return retval[1]

    if form.endswith("o"):
        retval = form[:-1] + "a"
        return retval

    def make_stem(form):
        return rsub(
            form,
            "^(.+)(.)(.)$",
            lambda m:
                m.group(1) + remove_stress.get(m.group(2), m.group(2)) + m.group(3))

    if rfind(form, "[áíó]n$") or rfind(form, "[éí]s$") or rfind(form, "[dtszxñ]or$") or rfind(form, "ol$"):
        # holgazán, comodín, bretón (not común); francés, kirguís (not mandamás);
        # volador, agricultor, defensor, avizor, flexor, señor (not posterior, bicolor, mayor, mejor, menor, peor);
        # español, mongol
        stem = make_stem(form)
        return stem + "a"

    return form

def make_masculine(form, special=None):
    retval = handle_multiword(form, special, make_masculine)
    if retval:
        if len(retval) != 1:
            raise ValueError("Internal error: Should have one return value for make_masculine: ", retval)
        return retval[1]

    if form.endswith("dora"):
        retval = form[:-1]
        return retval

    if form.endswith("a"):
        retval = form[:-1] + "o"
        return retval

    return form

# From https://en.wiktionary.org/wiki/Module%3Alinks
# Strips links: deletes category links,
# the targets of piped links,
# and all double square brackets.
def remove_links(text):
#     if type(text) == "table" then
#         text = text.args[1]

    if not text or text == "":
        return ""

    text = rsub(text, r"\[\[Category:[^|\]]*?\|?[^|\]]*?\]\]", "")
    text = rsub(text, r"\[\[[^|\]]*?\|", "")
    text = rsub(text, r"\[\[", "")
    text = rsub(text, r"\]\]", "")

    return text

def do_adjective(pagename, args={}, data={}, tracking_categories=[], is_superlative=False):
    feminines = []
    plurals = []
    masculine_plurals = []
    feminine_plurals = []

    if args.get("sp") and not allowed_special_indicators[args["sp"]]:
        raise ValueError("bad special inflection indictaor", args["sp"])

    print(data)

    if args.get("inv"):
        # invariable adjective
        # TODO: fix this
        #data["inflections"]["label"] = "invariable"
        pass
    else:
        lemma = remove_links(data["heads"][0]) if len(data.get("heads",[])) else pagename

        # Gather feminines.
        argsf = args.get("f", [])
        if len(argsf) == 0:
            argsf = ["+"]

        for f in argsf:
            if f == "+":
                # Generate default feminine.
                f = make_feminine(lemma, args.get("sp"))
            elif f == "#":
                f = lemma
            feminines.append(f)

        argspl = args.get("pl", [])
        argsmpl = args.get("mpl", [])
        argsfpl = args.get("fpl", [])
        if len(argspl) > 0 and (len(argsmpl) > 0 or len(argsfpl) > 0):
            raise ValueError("Can't specify both pl= and mpl=/fpl=")

        if len(feminines) == 1 and feminines[0] == lemma:
            # Feminine like the masculine; just generate a plural
            if len(argspl) == 0:
                argspl = ["+"]
        elif len(argspl) == 0:
            # Distinct masculine and feminine plurals
            if len(argsmpl) == 0:
                argsmpl = ["+"]
            if len(argsfpl) == 0:
                argsfpl = ["+"]

        for pl in argspl:
            if pl == "+":
                # Generate default plural.
                defpls = make_plural(lemma, args.get("sp"))
                if not defpls:
                    raise ValueError(f"Unable to generate default plural of '{lemma}'")
                for defpl in defpls:
                    plurals.append(defpl)
            elif pl == "#":
                plurals.append(lemma)
            else:
                plurals.append(pl)

        for mpl in argsmpl:
            if mpl == "+":
                # Generate default masculine plural.
                defpls = make_plural(lemma, args.get("sp"))
                if not defpls:
                    raise ValueError(f"Unable to generate default plural of '{lemma}'")
                for defpl in defpls:
                    masculine_plurals.append(defpl)
            elif mpl == "#":
                masculine_plurals.append(lemma)
            else:
                masculine_plurals.append(mpl)

        for fpl in argsfpl:
            if fpl == "+":
                for f in feminines:
                    # Generate default feminine plural.
                    defpls = make_plural(f, args.get("sp"))
                    if not defpls:
                        raise ValueError(f"Unable to generate default plural of '{f}'")
                    for defpl in defpls:
                        feminine_plurals.append(defpl)
            elif fpl == "#":
                feminine_plurals.append(lemma)
            else:
                feminine_plurals.append(fpl)

        #check_all_missing(feminines, "adjectives", tracking_categories)
        #check_all_missing(plurals, "adjectives", tracking_categories)
        #check_all_missing(masculine_plurals, "adjectives", tracking_categories)
        #check_all_missing(feminine_plurals, "adjectives", tracking_categories)

        # Make sure there are feminines given and not same as lemma.
        if len(feminines) == 1 and feminines[0] != lemma:
            item = {
                "label": "feminine",
                "accel": {"form": "f|s"},
                "": feminines
            }
            data["inflections"] = data.get("inflections", []) + [item]

        if len(plurals) > 0:
            item = {
                "label": "plural",
                "accel": {"form": "p"},
                "": plurals
            }
            data["inflections"] = data.get("inflections", []) + [item]

        if len(masculine_plurals) > 0:
            item = {
                "label": "masculine plural",
                "accel": {"form": "m|p"},
                "": masculine_plurals
            }
            data["inflections"] = data.get("inflections", []) + [item]

        if len(feminine_plurals) > 0:
            item = {
                "label": "feminine plural",
                "accel": {"form": "f|p"},
                "": feminine_plurals
            }
            data["inflections"] = data.get("inflections", []) + [item]

    if args.get("comp"):
        #check_all_missing(args.comp, "adjectives", tracking_categories)
        args["comp"]["label"] = "comparative"
        data["inflections"] = data.get("inflections", []) + [args.comp]

    if args.get("sup"):
        #check_all_missing(args.sup, "adjectives", tracking_categories)
        args["sup"]["label"] = "superlative"
        data["inflections"] = data.get("inflections", []) + [args.sup]

#    if args.irreg and is_superlative then
#        table.insert(data.categories, langname + " irregular superlative adjectives")


pos_functions["adjectives"] = {
    "params": {
        "inv": {"type": "boolean"}, #invariable
        "sp": {}, # special indicator: "first", "first-last", etc.
        "f": {"list": True}, #feminine form(s)
        "pl": {"list": True}, #plural override(s)
        "fpl": {"list": True}, #feminine plural override(s)
        "mpl": {"list": True}, #masculine plural override(s)
        "comp": {"list": True}, #comparative(s)
        "sup": {"list": True}, #comparative(s)
    },
    "func": lambda pagename, args, data, tracking_categories:
        do_adjective(pagename, args, data, tracking_categories, False)
}

pos_functions["comparative adjectives"] = {
    "params": {
        "inv": {"type": "boolean"}, #invariable
        "sp": {}, # special indicator: "first", "first-last", etc.
        "f": {"list": True}, #feminine form(s)
        "pl": {"list": True}, #plural override(s)
        "fpl": {"list": True}, #feminine plural override(s)
        "mpl": {"list": True}, #masculine plural override(s)
    },
    "func": lambda pagename, args, data, tracking_categories:
        do_adjective(pagename, args, data, tracking_categories, False)
}

pos_functions["superlative adjectives"] = {
   "params": {
        "inv": {"type": "boolean"}, #invariable
        "sp": {}, # special indicator: "first", "first-last", etc.
        "f": {"list": True}, #feminine form(s)
        "pl": {"list": True}, #plural override(s)
        "fpl": {"list": True}, #feminine plural override(s)
        "mpl": {"list": True}, #masculine plural override(s)
        "irreg": {"type": "boolean"},
    },
    "func": lambda pagename, args, data, tracking_categories:
        do_adjective(pagename, args, data, tracking_categories, True)
}


# Display information for a noun's gender
# This is separate so that it can also be used for proper nouns
def noun_gender(args, data):
    gender = args.get("1")
    if gender:
        data["genders"] = data.get("genders", []) + [gender]
    if len(data.get("genders", [])) == 0:
        data["genders"] = ["?"]

pos_functions["proper nouns"] = {
    "params": {
        1: {},
    },
    "func": lambda args, data:
        noun_gender(args, data)
}



def do_noun(pagename, args, data, tracking_categories=[]):
    allowed_genders = (
        "m",
        "f",
        "m-p",
        "f-p",
        "mf",
        "mf-p",
        "mfbysense",
        "mfbysense-p",
    )

    lemma = remove_links(data["heads"][0]) if len(data.get("heads",[])) else pagename

    if args.get("1") == "m-f":
        args["1"] = "mf"
    elif args.get("1") == "mfp" or args.get("1") == "m-f-p":
        args["1"] = "mf-p"

    if args.get("1"):
        if args["1"] not in allowed_genders:
            raise ValueError("Unrecognized gender: " + args["1"])
        data["genders"] = data.get("genders", []) + [ args["1"] ]

    if args.get("g2"):
        data["genders"] = data.get("genders", []) + [ args.get("g2") ]

#    if args["e"]:
#        #table.insert(data.categories, langname + " epicene nouns")
#        data["inflections"] = {"label": "epicene"}

    plurals = []
    plurals_label = "plural"

    if args.get("1","").endswith("-p"):
        data["inflections"] = {"label": "plural only"}
        if args.get("2"):
            raise ValueError("Can't specify plurals of a plurale tantum noun")
    else:
        # Gather plurals, handling requests for default plurals
        pl_args = args.get("pl", [])
        if args.get("2"):
            pl_args.insert(0, args.get("2"))

        for pl in pl_args:
            if pl == "+":
                plurals += make_plural(lemma)
            elif pl == "#":
                plurals.append(lemma)
            elif "+" in pl:
                pl = get_special_indicator(pl)
                plurals += make_plural(lemma, pl)
            else:
                plurals.append(pl)

        # Check for special plural signals
        mode = None

        if plurals and (plurals[0] in ["?", "!", "-", "~"]):
            mode = plurals[0]
            plurals.pop(0) # Remove the mode parameter

        if mode == "?":
            # Plural is unknown
            #table.insert(data.categories, langname + " nouns with unknown or uncertain plurals")
            pass
        elif mode == "!":
            # Plural is not attested
            plurals_label = "plural not attested"
            #table.insert(data.categories, langname + " nouns with unattested plurals")
            return
        elif mode == "-":
            # Uncountable noun; may occasionally have a plural
            #table.insert(data.categories, langname + " uncountable nouns")

            # If plural forms were given explicitly, then show "usually"
            if len(plurals):
                plurals_label = "plural not attested"
                #table.insert(data.categories, langname + " countable nouns")
            else:
                data["inflections"] = {"label": "uncountable"}
        else:
            # Countable or mixed countable/uncountable
            if len(plurals) == 0:
                plurals += make_plural(lemma)

            if mode == "~":
                # Mixed countable/uncountable noun, always has a plural
                plurals_label = "countable and uncountable"
                #table.insert(data.categories, langname + " uncountable nouns")
                #table.insert(data.categories, langname + " countable nouns")
            else:
                # Countable nouns
                #table.insert(data.categories, langname + " countable nouns")
                pass

    # Gather masculines/feminines. For each one, generate the corresponding plural(s).
    def handle_mf(mfs, inflect, default_plurals):
        retval = []
        for mf in mfs:
            if mf == "1" or mf == "+":
                # Generate default feminine.
                mf = inflect(lemma)
            elif mf == "#":
                mf = lemma
            special = get_special_indicator(mf)
            if special:
                mf = inflect(lemma, special)
            retval.append(mf)
            mfpls = make_plural(mf, special)
            if mfpls:
                for mfpl in mfpls:
                    # Add an accelerator for each masculine/feminine plural whose lemma
                    # is the corresponding singular, so that the accelerated entry
                    # that is generated has a definition that looks like
                    # # {{plural of|es|MFSING}}
                    default_plurals += [{"term": mfpl, "accel": {"form": "p", "lemma": mf}}]
        print("mf", [mfs, "plurals:", default_plurals, retval])
        return retval

    feminine_plurals = []
    fargs = args.get("f",[])
    if hasattr(fargs, 'casefold'):
        fargs = [fargs]
    feminines = handle_mf(fargs, make_feminine, feminine_plurals)
    print("xy", feminine_plurals)
    masculine_plurals = []
    margs = args.get("m",[])
    if hasattr(margs, 'casefold'):
        margs = [margs]
    masculines = handle_mf(margs, make_masculine, masculine_plurals)
    print("xx", masculine_plurals)

    def handle_mf_plural(mfpl, default_plurals, singulars):
        new_mfpls = {}
        for i, mfpl in enumerate(mfpl):
            accel = {}
            if len(mfpl) == len(singulars):
                # If same number of overriding masculine/feminine plurals as singulars,
                # assume each plural goes with the corresponding singular
                # and use each corresponding singular as the lemma in the accelerator.
                # The generated entry will have # {{plural of|es|SINGULAR}} as the
                # definition.
                accel = {"form": "p", "lemma": singulars[i]}
            else:
                accel = {}
            if mfpl == "+":
                for defpl in default_plurals:
                    # defpl is already a table
                    new_mfpls[""] = new_mfpl.get("", []) + [defpl]
            elif mfpl == "#":
                new_mfpls[""] = new_mfpl.get("", []) + [{"term": lemma, "accel": accel}]
            elif "+" in mfpl:
                mfpl = get_special_indicator(mfpl)
                for mf in singulars:
                    default_mfpls = make_plural(mf, mfpl)
                    for defp in default_mfpls:
                        new_mfpls[""] = new_mfpl.get("", []) + [{"term": defp, "accel": accel}]
            else:
                new_mfpls[""] = new_mfpl.get("", []) + [{"term": mfpl, "accel": accel}]
        print("mf_plural", [mfpl, default_plurals, singulars, new_mfpls])
        return new_mfpls

    if len(args.get("fpl", [])) > 0:
        # Override any existing feminine plurals.
        feminine_plurals = handle_mf_plural(args.fpl, feminine_plurals, feminines)

    if len(args.get("mpl", [])) > 0:
        # Override any existing masculine plurals.
        masculine_plurals = handle_mf_plural(args.mpl, masculine_plurals, masculines)

    #check_all_missing(plurals, "nouns", tracking_categories)
    #check_all_missing(feminines, "nouns", tracking_categories)
    #check_all_missing(feminine_plurals, "nouns", tracking_categories)
    #check_all_missing(masculines, "nouns", tracking_categories)
    #check_all_missing(masculine_plurals, "nouns", tracking_categories)

#    for mpl in masculine_plurals:
#        if mpl in plurals:
#            track("noun-redundant-mpl")

#    for _, fpl in ipairs(feminine_plurals) do
#        if redundant_plural(fpl) then
#            track("noun-redundant-fpl")


    print("XXXX", plurals)
    if len(plurals):
        item = {
            "label": "plural",
            "accel": {"form": "p"},
            "": plurals
        }
        data["inflections"] = data.get("inflections", []) + [item]
        print("XXXX", data)

    if len(feminines):
        item = {
            "label": "feminine",
            "accel": {"form": "f"},
            "": feminines
        }
        data["inflections"] = data.get("inflections", []) + [item]

    if len(feminine_plurals):
        item = {
                "label": "feminine plural",
                "": feminine_plurals
        }
        data["inflections"] = data.get("inflections", []) + [item]

    if len(masculines):
        item = {
            "label": "masculine",
            "": masculines
        }

    if len(masculine_plurals):
        item = {
            "label": "masculine plural",
            "": masculine_plurals
        }
        data["inflections"] = data.get("inflections", []) + [item]

# Display additional inflection information for a noun
pos_functions["nouns"] = {
    "params": {
        1: {"required": True, "default": "m"}, #gender
        "g2": {}, #second gender
        "e": {"type": "boolean"}, #epicene
        2: {"list": "pl"}, #plural override(s)
        "f": {"list": True}, #feminine form(s)
        "m": {"list": True}, #masculine form(s)
        "fpl": {"list": True}, #feminine plural override(s)
        "mpl": {"list": True}, #masculine plural override(s)
    },
    "func": lambda pagename, args, data, tracking_categories:
        do_noun(pagename, args, data)
}




'''

import re
import sys

from .paradigms import paradigms
from .combined import _data as combined

from ..get_template_params import get_template_params

def es_adj(t, title):
    results = get_adjective_forms(t, title)

    sources = {
        "f": ["f", "f2", "f3"],
        "pl": ["pl", "pl2", "pl3"],
        "mpl": ["mpl", "mpl2", "mpl2"],
        "fpl": ["fpl", "fpl2", "mpl3"]
    }

    overrides = {}
    for k,params in sources.items():
        for param in params:
            if t.has(param):
                overrides[k] = overrides.get(k, []) + [str(t.get(param).value)]

    for k,v in overrides.items():
        if k in results:
            results[k] = v

    return "; ".join([f"{k}={v}" for k,vs in sorted(results.items()) for v in vs])


def es_adj_sup(t, title):
    return es_adj(t, title)

def get_adjective_forms(template, title):
    if template is None:
        return {}

    if not title:
        return {}

    params = get_template_params(template)
    for k in [ "f", "pl", "mpl", "fpl" ]:
        if isinstance(params.get(k), str):
            params[k] = [params[k]]

    if "f" in params and "fpl" not in params:
        if "pl" in params:
            params["fpl"] = [ params["pl"][0] ]
        else:
            params["fpl"] = [ params["f"][0] + "s" ]

    if "m" not in params and "mpl" in params and "pl" not in params:
        params["pl"] = params.pop("mpl")

    if "pl" not in params:
        params["pl"] = [ title + "s" ]

    return {k:params[k] for k in ["f", "pl","fpl"] if k in params}

#'''
