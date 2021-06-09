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

# generate all indirect + direct pronoun combinations
GENERATE_ALL_COMBINATIONS=True

"""
Data and utilities for processing Spanish sections of enwiktionary

Based on https://en.wiktionary.org/wiki/Module%3Aes%2Dverb
Revision 62366447, 01:28, 13 April 2021

forms values
  string
  list
     string (simple form)
     dict
         form: string
         footnotes: list of strings

"""


"""

Authorship: Ben Wing <benwing2>

TERMINOLOGY:

-- "slot" = A particular combination of tense/mood/person/number/etc.
     Example slot names for verbs are "pres_1s" (present indicative first-person singular), "pres_sub_2sv" (present
     subjunctive second-person singular voseo form) "impf_sub_ra_3p" (imperfect subjunctive -ra form third-person
     plural), "imp_1p_comb_lo" (imperative first-person plural combined with clitic [[lo]]).
     Each slot is filled with zero or more forms.

-- "form" = The conjugated Spanish form representing the value of a given slot.

-- "lemma" = The dictionary form of a given Spanish term. For Spanish, always the infinitive.

"""

import re
import sys
import enwiktionary_templates.module.inflection_utilities as iut
import enwiktionary_templates.module.es_common as com

lang = {} #require("Module:languages").getByCode("es")

def rfind(string, pattern):
    return re.search(pattern, string)

def rmatch(string, pattern, count):
    if not string:
        raise ValueError("no string")
    if string:
        res = re.match(pattern, string)
        if res:
            if len(res.groups()) == 1:
                return res.group(1)
            else:
                return res.groups()

    if count == 1:
        return None
    return [None] * count

def rsub(string, pattern, replacement):
    return re.sub(pattern, replacement, string)

def rsplit(string, pattern):
    return re.split(pattern, string)

def link_term(term, face):
    return term

def m_links_remove_links(string):
    return string

def ternery(cond, v1, v2):
    if cond:
        return v1
    return v2

def lua_or(v1, v2):
    for v in [v1, v2]:
        if v:
            return v

V = com.V # vowel regex class
AV = com.AV # accented vowel regex class
C = com.C # consonant regex class

# replace .- with .*? in rexeg
# replace % with \ in regex
# replace " .. " with " + " in string concat
# replace nil with None, true with True, false with False
# replace "--" with "#"
# in every rsub, add final param with number of expected elements

fut_sub_note = "[mostly obsolete form, now mainly used in legal jargon]"
pres_sub_voseo_note = "[Argentine and Uruguayan " + link_term("voseo", "term") + " prefers the " + \
    link_term("tú", "term") + " form for the present subjunctive]"

vowel_alternants = ("ie", "ie-i", "ye", "ye-i", "ue", "ue-u", "hue", "i", "í", "ú", "+")
vowel_alternant_to_desc = {
    "ie": "e-ie",
    "ie-i": "e-ie-i",
    "ye": "e-ye",
    "ye-i": "e-ye-i",
    "ue": "o-ue",
    "ue-u": "o-ue-u",
    "hue": "o-hue",
    "i": "e-i",
    "í": "i-í",
    "ú": "u-ú",
}

raise_vowel = {"e": "i", "o": "u"}

all_persons_numbers = {
    "1s": "1|s",
    "2s": "2|s",
    "2sv": "2|s|voseo",
    "3s": "3|s",
    "1p": "1|p",
    "2p": "2|p",
    "3p": "3|p",
    "me": "me",
    "te": "te",
    "se": "se",
    "nos": "nos",
    "os": "os",
    "lo": "lo",
    "la": "la",
    "le": "le",
    "los": "los",
    "las": "las",
    "les": "les",
}

for p1 in ["me", "te", "se", "nos", "os"]:
    for p2 in ["lo", "la", "le", "los", "las", "les"]:
        all_persons_numbers[p1+p2] = p1+p2

person_number_list_basic = [ "1s", "2s", "3s", "1p", "2p", "3p" ]
person_number_list_voseo = [ "1s", "2s", "2sv", "3s", "1p", "2p", "3p" ]
# local persnum_to_index = {}
# for k, v in pairs(person_number_list) do
#     persnum_to_index[v: k
# end
imp_person_number_list = [ "2s", "2p" ]

person_number_to_reflexive_pronoun = {
    "1s": "me",
    "2s": "te",
    "2sv": "te",
    "3s": "se",
    "1p": "nos",
    "2p": "os",
    "3p": "se",
}

verb_slots_basic = {
    "infinitive": "inf",
    "infinitive_linked": "inf",
    "gerund": "ger",
    "pp_ms": "m|s|past|part",
    "pp_fs": "f|s|past|part",
    "pp_mp": "m|p|past|part",
    "pp_fp": "f|p|past|part",
}

verb_slots_combined = {}

verb_slot_combined_rows = {}

# Add entries for a slot with person/number variants.
# `verb_slots` is the table to add to.
# `slot_prefix` is the prefix of the slot, typically specifying the tense/aspect.
# `tag_suffix` is the set of inflection tags to add after the person/number tags,
# or "-" to use "-" as the inflection tags (which indicates that no accelerator entry
# should be generated).
def add_slot_personal(verb_slots, slot_prefix, tag_suffix, person_number_list):
    for persnum in person_number_list:
        persnum_tag = all_persons_numbers[persnum]
        slot = slot_prefix + "_" + persnum
        if tag_suffix == "-":
            verb_slots[slot] = "-"
        else:
            verb_slots[slot] = persnum_tag + "|" + tag_suffix

add_slot_personal(verb_slots_basic, "pres", "pres|ind", person_number_list_voseo)
add_slot_personal(verb_slots_basic, "impf", "impf|ind", person_number_list_basic)
add_slot_personal(verb_slots_basic, "pret", "pret|ind", person_number_list_basic)
add_slot_personal(verb_slots_basic, "fut", "fut|ind", person_number_list_basic)
add_slot_personal(verb_slots_basic, "cond", "cond", person_number_list_basic)
add_slot_personal(verb_slots_basic, "pres_sub", "pres|sub", person_number_list_voseo)
add_slot_personal(verb_slots_basic, "impf_sub_ra", "impf|sub", person_number_list_basic)
add_slot_personal(verb_slots_basic, "impf_sub_se", "impf|sub", person_number_list_basic)
add_slot_personal(verb_slots_basic, "fut_sub", "fut|sub", person_number_list_basic)
add_slot_personal(verb_slots_basic, "imp", "imp", {"2s", "2sv", "3s", "1p", "2p", "3p"})
add_slot_personal(verb_slots_basic, "neg_imp", "-", {"2s", "3s", "1p", "2p", "3p"})

def add_combined_slot(basic_slot, slot_prefix, pronouns1, pronouns2):
    pronouns = pronouns1 + pronouns2
    if GENERATE_ALL_COMBINATIONS:
        for p1 in pronouns1:
            for p2 in pronouns2:
                pronouns.append(p1 + p2)

    add_slot_personal(verb_slots_combined, basic_slot + "_comb", slot_prefix + "|combined", pronouns)
    verb_slot_combined_rows[basic_slot] = pronouns

add_combined_slot("infinitive", "inf", ["me", "te", "se", "nos", "os"], ["lo", "la", "le", "los", "las", "les"])
add_combined_slot("gerund", "gerund", ["me", "te", "se", "nos", "os"], ["lo", "la", "le", "los", "las", "les"])
add_combined_slot("imp_2s", "imp|2s", ["me", "te", "nos"], ["lo", "la", "le", "los", "las", "les"])
add_combined_slot("imp_3s", "imp|3s", ["me", "se", "nos"], ["lo", "la", "le", "los", "las", "les"])
add_combined_slot("imp_1p", "imp|1p", ["te", "nos", "os"], ["lo", "la", "le", "los", "las", "les"])
add_combined_slot("imp_2p", "imp|2p", ["me", "nos", "os"], ["lo", "la", "le", "los", "las", "les"])
add_combined_slot("imp_3p", "imp|3p", ["me", "se", "nos"], ["lo", "la", "le", "los", "las", "les"])

all_verb_slots = { **verb_slots_basic, **verb_slots_combined}

verb_slots_basic_map = verb_slots_basic

verb_slots_combined_map = verb_slots_combined


def match_against_verbs(ref_verb, prefixes):
    def f(verb):
        for prefix in prefixes:
            if verb == prefix + ref_verb:
                return prefix, ref_verb
    return f


def _irreg_match_brir(verb):
    prefix, base_verb = rmatch(verb, "^(.*)(brir)$", 2)
    # Only match abrir, cubrir and compounds, and don't match desabrir/jabrir
    if not prefix:
        return
    elif not prefix.endswith("a") or prefix.endswith("cu"):
        return
    elif prefix == "desa" or prefix == "ja":
        return
    else:
        return prefix, base_verb

def _irreg_match_romper(verb):
    prefix, base_verb = rmatch(verb, "^(.*)(romper)$", 2)
    # Don't match corromper
    if prefix != "cor":
        return prefix, base_verb

irreg_conjugations = [
    {
        # andar, desandar
        # we don't want to match e.g. mandar.
        "match": match_against_verbs("andar", ["", "des"]),
        "forms": {"pret": "anduv", "pret_conj": "irreg"}
    },
    {
        # asir, desasir
        "match": "asir",
        # use 'asgu' because we're in a front environment; if we use 'asg', we'll get '#asjo'
        "forms": {"pres1_and_sub": "asgu"}
    },
    {
        # abrir, cubrir and compounds
        "match": _irreg_match_brir,
        "forms": {"pp": "biert"}
    },
    {
        "match": "caber",
        "forms": {"pres1_and_sub": "quep", "pret": "cup", "pret_conj": "irreg", "fut": "cabr"}
    },
    {
        # caer, decaer, descaer, recaer
        "match": "caer",
        # use 'caigu' because we're in a front environment; if we use 'caig', we'll get '#caijo'
        "forms": {"pres1_and_sub": "caigu"}
    },
    {
        # cocer, escocer, precocer, etc.
        "match": "cocer",
        # override cons_alt, otherwise the verb would be categorized as a c-zc alternating verb
        "forms": {"vowel_alt": "ue", "pres1": "cuez", "pres_sub_unstressed": "coz", "cons_alt": "c-z"}, # not cozco, as would normally be generated
    },
    {
        # dar, desdar
        "match": match_against_verbs("dar", ["", "des"]),
        "forms": {
            # we need to override various present indicative forms and add an accent for the compounds;
            # not needed for the simplex and in fact the accents will be removed in that case
            "pres_1s": "doy",
            "pres_2s": "dás",
            "pres_3s": "dá",
            "pres_2p": "dáis",
            "pres_3p": "dán",
            "pret": "d", "pret_conj": "er",
            "pres_sub_1s": "dé*",  # * signals that the monosyllabic accent must remain
            "pres_sub_2s": "dés",
            "pres_sub_3s": "dé*",
            "pres_sub_2p": "déis",
            "pres_sub_3p": "dén",
            "imp_2s": "dá",
        }
    },
    {
        # decir, redecir, entredecir
        "match": match_against_verbs("decir", ["", "re", "entre"]),
        "forms": {
            # for this and variant verbs in -decir, we set cons_alt to False because we don't want the
            # verb categorized as a c-zc alternating verb, which would happen by default
            # use 'digu' because we're in a front environment; if we use 'dig', we'll get '#dijo'
            "pres1_and_sub": "digu", "vowel_alt": "i", "cons_alt": False, "pret": "dij", "pret_conj": "irreg",
            "pp": "dich", "fut": "dir",
            "imp_2s": "dí" # need the accent for the compounds; it will be removed in the simplex
        }
    },
    {
        # antedecir, interdecir
        "match": match_against_verbs("decir", ["ante", "inter"]),
        "forms": {
            "pres1_and_sub": "digu", "vowel_alt": "i", "cons_alt": False, "pret": "dij", "pret_conj": "irreg",
            "pp": "dich", "fut": "dir" # imp_2s regular
        }
    },
    {
        # bendecir, maldecir
        "match": match_against_verbs("decir", ["ben", "mal"]),
        "forms": {
            "pres1_and_sub": "digu", "vowel_alt": "i", "cons_alt": False, "pret": "dij", "pret_conj": "irreg",
            "pp": ["decid", "dit"] # imp_2s regular, fut regular
        }
    },
    {
        # condecir, contradecir, desdecir, predecir, others?
        "match": "decir",
        "forms": {
            "pres1_and_sub": "digu", "vowel_alt": "i", "cons_alt": False, "pret": "dij", "pret_conj": "irreg",
            "pp": "dich", "fut": ["decir", "dir"] # imp_2s regular
        }
    },
    {
        # conducir, producir, reducir, traducir, etc.
        "match": "ducir",
        "forms": {"pret": "duj", "pret_conj": "irreg"}
    },
    {
        # elegir, reelegir; not preelegir, per RAE
        "match": match_against_verbs("elegir", ["", "re"]),
        "forms": {"vowel_alt": "i", "pp": ["elegid", "elect"]}
    },
    {
        "match": "^estar",
        "forms": {
            "pres_1s": "estoy",
            "pres_2s": "estás",
            "pres_2sv": "estás",
            "pres_3s": "está",
            "pres_3p": "están",
            "pret": "estuv",
            "pret_conj": "irreg",
            "pres_sub_1s": "esté",
            "pres_sub_2s": "estés",
            "pres_sub_2sv": "estés",
            "pres_sub_3s": "esté",
            "pres_sub_3p": "estén",
            "imp_2s": "está",
            "imp_2sv": "está",
        }
    },
    {
        # freír, refreír
        "match": "freír",
        "forms": {"vowel_alt": "í", "pp": ["freíd", "frit"]}
    },
    {
        "match": "garantir",
        "forms": {
            "pres_stressed": [{"form": "garant", "footnotes": ["[only used in Argentina and Uruguay]"]}],
            "pres1_and_sub": [{"form": "garant", "footnotes": ["[only used in Argentina and Uruguay]"]}],
        }
    },
    {
        "match": "^haber",
        "forms": {
            "pres_1s": "he",
            "pres_2s": "has",
            "pres_2sv": "has",
            "pres_3s": ["ha", {"form": "hay", "footnotes": ["[used impersonally]"]}],
            "pres_1p": "hemos",
            "pres_3p": "han",
            "pres1_and_sub": "hay", # only for subjunctive as we override pres_1s
            "pret": "hub",
            "pret_conj": "irreg",
            "imp_2s": ["habe", "he"],
            "imp_2sv": ["habe", "he"],
            "fut": "habr",
        }
    },
    {
        "match": "satisfacer",
        "forms": {
            # see below for cons_alt setting and pres1_and_sub setting
            "pres1_and_sub": "satisfagu", "cons_alt": False, "pret": "satisfic", "pret_conj": "irreg",
            "pp": "satisfech", "fut": "satisfar", "imp_2s": ["satisface", "satisfaz"]
        }
    },
    {
        "match": match_against_verbs("hacer", ["contra", "re"]),
        # contrahacer/rehacer require an extra accent in the preterite (rehíce, rehízo).
        "forms": {
            # see below for cons_alt setting and pres1_and_sub setting
            "pres1_and_sub": "hagu", "cons_alt": False,
            "pret": "hic", "pret_1s": "híce", "pret_3s": "hízo", "pret_conj": "irreg",
            "pp": "hech", "fut": "har", "imp_2s": "haz"
        }
    },
    {
        # hacer, deshacer, contrahacer, rehacer, facer, desfacer, jacer
        "match": lambda verb: rmatch(verb, "^(.*[hjf])(acer)$", 2),
        "forms": {
            # for these verbs, we set cons_alt to False because we don't want the verb categorized as a
            # c-zc alternating verb, which would happen by default
            # use 'agu' because we're in a front environment; if we use 'ag', we'll get '#hajo'
            "pres1_and_sub": "agu", "cons_alt": False, "pret": "ic", "pret_conj": "irreg", "pp": "ech",
            "fut": "ar", "imp_2s": "az"
        }
    },
    {
        # imprimir, reimprimir
        "match": "imprimir",
        "forms": {"pp": ["imprimid", "impres"]}
    },
    {
        # infecir
        "match": "infecir",
        # override cons_alt, otherwise the verb would be categorized as a c-zc alternating verb
        "forms": {"vowel_alt": "i", "pres1": "infiz", "pres_sub_unstressed": "infez", "cons_alt": "c-z"}, # not infizco, as would normally be generated
    },
    {
        "match": "infecir",
        # override cons_alt, otherwise the verb would be categorized as a c-zc alternating verb
        "forms": {"pres1_and_sub": "infez", "cons_alt": "c-z"}, # not mezco, as would normally be generated
    },
    {
        "match": "^ir",
        "forms": {
            "pres_1s": "voy",
            "pres_2s": "vas",
            "pres_2sv": "vas",
            "pres_3s": "va",
            "pres_1p": "vamos",
            "pres_2p": "vais",
            "pres_3p": "van",
            "pres1_and_sub": "vay", # only for subjunctive as we override pres_1s
            "full_impf": "ib",
            "impf_1p": "íbamos",
            "pret": "fu",
            "pret_conj": "irreg", # this signals that fu + -ieron -> fueron not fuyeron
            "pret_1s": "fui",
            "pret_3s": "fue",
            "imp_2s": "ve",
            "imp_2sv": "andá",
            "imp_1p": ["vamos", "vayamos"],
            "refl_imp_2p": ["idos", "iros"],
            "imp_2p_comb_os": ["idos", "iros"],
        }
    },
    {
        # mecer, remecer
        # we don't want to match e.g. adormecer, estremecer
        "match": match_against_verbs("mecer", ["re", ""]),
        # override cons_alt, otherwise the verb would be categorized as a c-zc alternating verb
        "forms": {"pres1_and_sub": "mez", "cons_alt": "c-z"}, # not mezco, as would normally be generated
    },
    {
        # morir, desmorir, premorir
        "match": "morir",
        "forms": {"vowel_alt": "ue-u", "pp": "muert"},
    },
    {
        # oír, desoír, entreoír, trasoír
        "match": "oír",
        # use 'oigu' because we're in a front environment; if we use 'oig', we'll get '#oijo'
        "forms": {"pres1_and_sub": "oigu"}
    },
    {
        "match": "olver", # solver, volver, bolver and derivatives
        "forms": {"vowel_alt": "ue", "pp": "uelt"}
    },
    {
        # placer, desplacer
        "match": "placer",
        "forms": {
            "pret_3s": ["plació", {"form": "plugo", "footnotes": ["[archaic]"]}],
            "pret_3p": ["placieron", {"form": "pluguieron", "footnotes": ["[archaic]"]}],
            "pres_sub_3s": ["plazca", {"form": "plega", "footnotes": ["[archaic]"]}, {"form": "plegue", "footnotes": ["[archaic]"]}],
            "impf_sub_ra_3s": ["placiera", {"form": "pluguiera", "footnotes": ["[archaic]"]}],
            "impf_sub_ra_3p": ["placieran", {"form": "pluguieran", "footnotes": ["[archaic]"]}],
            "impf_sub_se_3s": ["placiese", {"form": "pluguiese", "footnotes": ["[archaic]"]}],
            "impf_sub_se_3p": ["placiesen", {"form": "pluguiesen", "footnotes": ["[archaic]"]}],
            "fut_sub_3s": ["placiere", {"form": "pluguiere", "footnotes": ["[archaic]"]}],
            "fut_sub_3p": ["placieren", {"form": "pluguieren", "footnotes": ["[archaic]"]}],
        }
    },
    {
        "match": "poder",
        "forms": {"vowel_alt": "ue", "pret": "pud", "pret_conj": "irreg", "fut": "podr", "gerund": "pudiendo"}
    },
    {
        # poner, componer, deponer, imponer, oponer, suponer, many others
        "match": "poner",
        "forms": {
            # use 'pongu' because we're in a front environment; if we use 'pong', we'll get '#ponjo'
            "pres1_and_sub": "pongu", "pret": "pus", "pret_conj": "irreg", "fut": "pondr", "pp": "puest",
            "imp_2s": "pón" # need the accent for the compounds; it will be removed in the simplex
        }
    },
    {
        # proveer, desproveer
        "match": "proveer",
        "forms": {"pp": ["proveíd", "provist"]},
    },
    {
        "match": "pudrir",
        "forms": {"pp": "podrid"}
    },
    {
        # querer, desquerer, malquerer
        "match": "querer",
        "forms": {"vowel_alt": "ie", "pret": "quis", "pret_conj": "irreg", "fut": "querr"}
    },
    {
        "match": "^raer",
        # use 'raigu' because we're in a front environment; if we use 'raig', we'll get '#raijo'
        "forms": {"pres1_and_sub": ["raigu", "ray"]}
    },
    {
        # roer, corroer
        "match": "roer",
        # use 'roigu' because we're in a front environment; if we use 'roig', we'll get '#roijo'
        "forms": {"pres1_and_sub": ["ro", "roigu", "roy"]}
    },
    {
        # romper, entrerromper, arromper, derromper; not corromper; FIXME: not sure about interromper (obsolete)
        "match": _irreg_match_romper,
        "forms": {"pp": "rot"}
    },
    {
        # saber, resaber
        "match": "saber",
        "forms": {
            "pres_1s": "sé*", # * signals that the monosyllabic accent must remain
            "pres1_and_sub": "sep", # only for subjunctive as we override pres_1s
            "pret": "sup",
            "pret_conj": "irreg",
            "fut": "sabr",
        }
    },
    {
        "match": "salir",
        "forms": {
            # use 'salgu' because we're in a front environment; if we use 'salg', we'll get '#saljo'
            "pres1_and_sub": "salgu", "fut": "saldr", "imp_2s": "sal",
            # These don't exist per the RAE.
            "imp_2s_comb_lo": [], "imp_2s_comb_los": [], "imp_2s_comb_la": [], "imp_2s_comb_las": [],
            "imp_2s_comb_le": [], "imp_2s_comb_les": [],
        },
    },
    {
        "match": "scribir", # escribir, describir, proscribir, etc.
        "forms": {"pp": ["scrit", {"form": "script", "footnotes": ["[Argentina and Uruguay]"]}]}
    },
    {
        "match": "^ser",
        "forms": {
            "pres_1s": "soy",
            "pres_2s": "eres",
            "pres_2sv": "sos",
            "pres_3s": "es",
            "pres_1p": "somos",
            "pres_2p": "sois",
            "pres_3p": "son",
            "pres1_and_sub": "se", # only for subjunctive as we override pres_1s
            "full_impf": "er",
            "impf_1p": "éramos",
            "pret": "fu",
            "pret_conj": "irreg", # this signals that fu + -ieron -> fueron not fuyeron
            "pret_1s": "fui",
            "pret_3s": "fue",
            "fut": "ser",
            "imp_2s": "sé*", # * signals that the monosyllabic accent must remain
            "imp_2sv": "sé*",
        }
    },
    {
        "match": "^soler",
        "forms": {
            "vowel_alt": "ue",
            "fut": [{"form": "soler", "footnotes": ["[rare but acceptable]"]}],
            "fut_sub": [{"form": "sol", "footnotes": ["[rare but acceptable]"]}],
            "pp": [{"form": "solid", "footnotes": ["[rare but acceptable]"]}],
        }
    },
    {
        # tener, abstener, contener, detener, obtener, sostener, and many others
        "match": "tener",
        "forms": {
            # use 'tengu' because we're in a front environment; if we use 'teng', we'll get '#tenjo'
            "pres1_and_sub": "tengu", "vowel_alt": "ie", "pret": "tuv", "pret_conj": "irreg", "fut": "tendr",
            "imp_2s": "tén" # need the accent for the compounds; it will be removed in the simplex
        }
    },
    {
        # traer, atraer, detraer, distraer, extraer, sustraer, and many others
        "match": "traer",
        # use 'traigu' because we're in a front environment; if we use 'traig', we'll get '#traijo'
        "forms": {"pres1_and_sub": "traigu", "pret": "traj", "pret_conj": "irreg"}
    },
    {
        # valer, equivaler, prevaler
        "match": "valer",
        # use 'valgu' because we're in a front environment; if we use 'valg', we'll get '#valjo'
        "forms": {"pres1_and_sub": "valgu", "fut": "valdr"}
    },
    {
        "match": "venir",
        "forms": {
            # use 'vengu' because we're in a front environment; if we use 'veng', we'll get '#venjo'
            "pres1_and_sub": "vengu", "vowel_alt": "ie-i", "pret": "vin", "pret_conj": "irreg",
            # uniquely for this verb, pres sub 1p/2p do not raise the vowel even though we are an
            # e-ie-i verb (contrast sentir -> sintamos/sintáis)
            "pres_sub_1p": "vengamos", "pres_sub_2p": "vengáis",
            "fut": "vendr", "imp_2s": "vén" # need the accent for the compounds; it will be removed in the simplex
        }
    },
    {
        # We want to match antever etc. but not atrever etc. No way to avoid listing each verb.
        "match": match_against_verbs("ver", ["ante", "entre", "pre", "re", ""]),
        "forms": {
            # we need to override various present indicative forms and add an accent for the compounds;
            # not needed for the simplex and in fact the accents will be removed in that case
            "pres_2s": "vés",
            "pres_2sv": "vés",
            "pres_3s": "vé",
            "pres_2p": "véis",
            "pres_3p": "vén",
            "pres1_and_sub": "ve",
            "impf": "ve", "pp": "vist",
            "imp_2s": "vé" # need the accent for the compounds; it will be removed in the simplex
        }
    },
    {
        # yacer, adyacer, subyacer
        "match": "yacer",
        # use 'yazqu/yazgu/yagu' because we're in a front environment; see 'decir' above
        "forms": {"pres1_and_sub": ["yazqu", "yazgu", "yagu"], "imp_2s": ["yace", "yaz"]}
    },
]


reflexive_masc_forms = {
    "su": ["mi", "tu", "su", "nuestro", "vuestro", "su"],
    "sus": ["mis", "tus", "sus", "nuestros", "vuestros", "sus"],
    "sí": ["mí", "ti", "sí", "nosotros", "vosotros", "sí"],
    "consigo": ["conmigo", "contigo", "consigo", "con nosotros", "con vosotros", "consigo"],
}

reflexive_fem_forms = {
    "su": ["mi", "tu", "su", "nuestra", "vuestra", "su"],
    "sus": ["mis", "tus", "sus", "nuestras", "vuestras", "sus"],
    "sí": ["mí", "ti", "sí", "nosotras", "vosotras", "sí"],
    "consigo": ["conmigo", "contigo", "consigo", "con nosotras", "con vosotras", "consigo"],
}

reflexive_forms = {
    "se": ["me", "te", "se", "nos", "os", "se"],
    "suyo": ["mío", "tuyo", "suyo", "nuestro", "vuestro", "suyo"],
    "suya": ["mía", "tuya", "suya", "nuestra", "vuestra", "suya"],
    "suyos": ["míos", "tuyos", "suyos", "nuestros", "vuestros", "suyos"],
    "suyas": ["mías", "tuyas", "suyas", "nuestras", "vuestras", "suyas"],
}

def skip_slot(base, slot, allow_overrides=False):
    if not allow_overrides and (
        (base.get("basic_overrides") and base["basic_overrides"].get(slot)) or \
        (base.get("combined_overrides") and base["combined_overrides"].get(slot)) or \
        base.get("refl") and \
        (base.get("reflexive_only_overrides") and base["reflexive_only_overrides"].get(slot))
        ):
    # Skip any slots for which there are overrides.
              return True

    if base.get("only3s") and (slot.startswith("pp_f") or slot.startswith("pp_mp")):
        # diluviar, atardecer, neviscar; impersonal verbs have only masc sing pp
        return True

    if not ("1" in slot or "2" in slot or "3" in slot):
        # Don't skip non-personal slots.
        return False

    if base.get("nofinite"):
        return True

    if base.get("only3s") and (not "3s" in slot or slot.startswith("imp_") or slot.startswith("neg_imp_")):
        # diluviar, atardecer, neviscar
        return True

    if base.get("only3sp") and (not ("3s" in slot or "3p" in slot) or slot.startswith("imp_") or slot.startswith("^neg_imp_")):
        # atañer, concernir
        return True

    return False

def escape_reflexive_indicators(arg1):
    if not "pron>" in arg1:
        return arg1

    # TODO: iut 
    segments = iut.parse_balanced_segment_run(arg1, "<", ">")
    # Loop over every other segment. The even-numbered segments are angle-bracket specs while
    # the odd-numbered segments are the text between them.
    # TODO: test this
    for i in range(1, len(segments), 2):
        if segments[i] == "<mpron>":
            segments[i] = "⦃⦃mpron⦄⦄"
        elif segments[i] == "<fpron>":
            segments[i] = "⦃⦃fpron⦄⦄"
        elif segments[i] == "<pron>":
            segments[i] = "⦃⦃pron⦄⦄"

    return segments



def undo_escape_form(form):
    return form.replace("⦃⦃", "<").replace("⦄⦄", ">")


def remove_reflexive_indicators(form):
    # TODO: Is this a regex?
    return form.replace("⦃⦃.*?⦄⦄", "")


def replace_reflexive_indicators(slot, form):
    if not "⦃" in form:
        return form
    raise ValueError("Internal error: replace_reflexive_indicators not implemented yet")

# Add the `stem` to the `ending` for the given `slot` and apply any phonetic modifications.
# `is_combining_ending` is true if `ending` is actually the ending (this function is also
# called to combine prefix + stem). WARNING: This function is written very carefully; changes
# to it can easily have unintended consequences.
def combine_stem_ending(base, slot, stem, ending, is_combining_ending):
    if not is_combining_ending:
        return stem + ending

    if base["stems"].get("raising_conj") and (rfind(ending, "^i" + V) or \
        slot == "pres_sub_1p" or slot == "pres_sub_2p" or slot == "pres_sub_2sv"):
            # need to raise e -> i, o -> u: dormir -> durmió, durmiera, durmiendo, durmamos
            stem = rsub(stem, "([eo])(" + C + "*)$", lambda m: raise_vowel[m.group(1)] + m.group(2))
            # also with stem ending in -gu or -qu (e.g. erguir -> irguió, irguiera, irguiendo, irgamos)
            stem = rsub(stem, "([eo])(" + C + "*[gq]u)$", lambda m: raise_vowel[m.group(1)] + m.group(2))

    # Lots of sound changes involving endings beginning with i + vowel
    if rfind(ending, "^i" + V):
        # (1) final -i of stem absorbed: sonreír -> sonrió, sonriera, sonriendo; note that this rule may be fed
        # by the preceding one (stem sonre- raised to sonri-, then final i absorbed)
        stem = rsub(stem, "i$", "")

        # (2) In the preterite of irregular verbs (likewise for other tenses derived from the preterite stem, i.e.
        #     imperfect and future subjunctive), initial i absorbed after j (dijeron not #dijieron, likewise for
        #     condujeron, trajeron) and u (fueron not #fuyeron). Does not apply in regular verb tejer (tejieron not
        #     #tejeron) and concluir (concluyeron not #conclueron).
        if base["stems"].get("pret_conj") == "irreg" and rfind(stem, "[ju]$"):
            ending = rsub(ending, "^i", "")

        # (3) initial i -> y after vowel and word-initially: poseer -> poseyó, poseyera, poseyendo;
        # concluir -> concluyó, concluyera, concluyendo; ir -> yendo; but not conseguir/delinquir
        if stem == "" or (rfind(stem, V + "$") and not rfind(stem, "[gq]u$")):
            ending = rsub(ending, "^i", "y")

        # (4) -gü + ie- -> -guye-: argüir -> arguyó, arguyera, arguyendo
        if stem.endswith("gü"):
            # transfer the y to the stem to avoid gü -> gu below in front/back conversions
            stem = rsub(stem, "ü$", "uy")
            ending = rsub(stem, "^i", "")

        # (5) initial i absorbed after ñ, ll, y: tañer -> tañó, tañera, tañendo; bullir -> bulló, bullera, bullendo
        if rfind(stem, "[ñy]$") or rfind(stem, "ll$"):
            ending = rsub(ending, "^i", "")

    # If ending begins with i, it must get an accent after a/e/i/o to prevent the two merging into a diphthong:
    # caer -> caíste, caímos; reír -> reíste, reímos (pres and pret). This does not apply after u, e.g.
    # concluir -> concluiste, concluimos.
    if ending.startswith("i") and rfind(stem, "[aeio]$"):
        ending = rsub(ending, "^i", "í")

    # If -oír/-uir (i.e. -ir with stem ending in -o/u, e.g. oír, concluir), a y must be added before endings
    # beginning with a/e/o. Check for base["stems"].pret_conj == "irreg" to exclude stem fu- of [[ir]].
    if base["conj"] == "ir" and rfind(ending, "^[aeoáéó]") and base["stems"].get("pret_conj") != "irreg":
        if rfind(stem, "[oú]$"): # oír -> oye, rehuir -> rehúyo/rehúye (with indicator 'ú')
            stem = stem + "y"
        elif rfind(stem, "[^gq]u$"): # concluir, but not conseguir or delinquir
            stem = stem + "y"
        elif stem.endswith("ü"): # argüir -> arguyendo
            stem = rsub(stem, "ü$", "uy")

    # Spelling changes in the stem; it depends on whether the stem given is the pre-front-vowel or
    # pre-back-vowel variant, as indicated by `frontback`. We want these front-back spelling changes to happen
    # between stem and ending, not between prefix and stem; the prefix may not have the same "front/backness"
    # as the stem.
    is_front = rfind(ending, "^[eiéí]")
    if base.get("frontback") == "front" and not is_front:
        # parecer -> parezco, conducir -> conduzco; use zqu to avoid triggering the following gsub();
        # the third line will replace zqu -> zc
        if slot != "pret_3s": # exclude hice -> hizo (not #hizco)
            stem = rsub(stem, "(" + V + ")c$", r"\1zqu")
        stem = rsub(stem, "sc$", "squ") # evanescer -> evanesco, fosforescer -> fosforesco
        stem = rsub(stem, "c$", "z") # ejercer -> ejerzo, uncir -> unzo
        stem = rsub(stem, "qu$", "c") # delinquir -> delinco, parecer -> parezqu- -> parezco
        stem = rsub(stem, "g$", "j") # coger -> cojo, afligir -> aflijo
        stem = rsub(stem, "gu$", "g") # distinguir -> distingo
        stem = rsub(stem, "gü$", "gu") # may not occur; argüir -> arguyo handled above
    elif base.get("frontback") == "back" and is_front:
        stem = rsub(stem, "gu$", "gü") # averiguar -> averigüé
        stem = rsub(stem, "g$", "gu") # cargar -> cargué
        stem = rsub(stem, "c$", "qu") # marcar -> marqué
        stem = rsub(stem, "[çz]$", "c") # aderezar/adereçar -> aderecé

    return stem + ending


def add(base, slot, stems, endings, is_combining_ending, allow_overrides):
    if skip_slot(base, slot, allow_overrides):
        return

    def do_combine_stem_ending(stem, ending):
        return combine_stem_ending(base, slot, stem, ending, is_combining_ending)
    iut.add_forms(base["forms"], slot, stems, endings, do_combine_stem_ending, None, None, base.get("all_footnotes"))


def add3(base, slot, prefix, stems, endings, allow_overrides=False):
    if not prefix:
        return add(base, slot, stems, endings, "is combining ending", allow_overrides)

    if skip_slot(base, slot, allow_overrides):
        return

    is_combining_ending = False

    def do_combine_stem_ending(stem, ending):
        return combine_stem_ending(base, slot, stem, ending, is_combining_ending)

    # Have to reimplement add_multiple_forms() ourselves due to the is_combining_ending
    # flag, which needs to be different when adding prefix to stems vs. stems to ending.
    # Otherwise we get e.g. #reímpreso instead of reimpreso.
    tempdest = {}
    iut.add_forms(tempdest, slot, prefix, stems, do_combine_stem_ending)
    is_combining_ending = True
    iut.add_forms(base["forms"], slot, tempdest.get(slot), endings, do_combine_stem_ending)


def insert_form(base, slot, form):
    if not skip_slot(base, slot):
        iut.insert_form(base["forms"], slot, form)

def insert_forms(base, slot, forms):
    if not skip_slot(base, slot):
        iut.insert_forms(base["forms"], slot, forms)


def add_single_stem_tense(base, slot_pref, stems, s1, s2, s3, p1, p2, p3):
    def addit(slot, ending):
        add3(base, slot_pref + "_" + slot, base["prefix"], stems, ending)
    addit("1s", s1)
    addit("2s", s2)
    addit("3s", s3)
    addit("1p", p1)
    addit("2p", p2)
    addit("3p", p3)

def add_present_indic(base):
    def addit(slot, stems, ending):
        add3(base, "pres_" + slot, base["prefix"], stems, ending)

    if base["conj"] == "ar":
        s2, s2v, s3, p1, p2, p3 = "as", "ás", "a", "amos", "áis", "an"
    elif base["conj"] == "er":
        s2, s2v, s3, p1, p2, p3 = "es", "és", "e", "emos", "éis", "en"
    elif base["conj"] == "ir":
        s2, s2v, s3, p1, p2, p3 = "es", "ís", "e", "imos", "ís", "en"
    else:
        raise ValueError("Internal error: Unrecognized conjugation " + base["conj"])

    addit("1s", base["stems"].get("pres1"), "o")
    addit("2s", base["stems"].get("pres_stressed"), s2)
    addit("2sv", base["stems"].get("pres_unstressed"), s2v)
    addit("3s", base["stems"].get("pres_stressed"), s3)
    addit("1p", base["stems"].get("pres_unstressed"), p1)
    addit("2p", base["stems"].get("pres_unstressed"), p2)
    addit("3p", base["stems"].get("pres_stressed"), p3)

def add_present_subj(base):
    def addit(slot, stems, ending):
        add3(base, "pres_sub_" + slot, base["prefix"], stems, ending)

    if base.get("conj") == "ar":
        s1, s2, s2v, s3, p1, p2, p3 = "e", "es", "és", "e", "emos", "éis", "en"
    else:
        s1, s2, s2v, s3, p1, p2, p3 = "a", "as", "ás", "a", "amos", "áis", "an"

    addit("1s", base["stems"].get("pres_sub_stressed"), s1)
    addit("2s", base["stems"].get("pres_sub_stressed"), s2)
    addit("2sv", base["stems"].get("pres_sub_unstressed"), s2v)
    addit("3s", base["stems"].get("pres_sub_stressed"), s3)
    addit("1p", base["stems"].get("pres_sub_unstressed"), p1)
    addit("2p", base["stems"].get("pres_sub_unstressed"), p2)
    addit("3p", base["stems"].get("pres_sub_stressed"), p3)


def add_imper(base):
    def addit(slot, stems, ending):
        add3(base, "imp_" + slot, base["prefix"], stems, ending)

    if base.get("conj") == "ar":
        addit("2s", base["stems"].get("pres_stressed"), "a")
        addit("2sv", base["stems"].get("pres_unstressed"), "á")
        addit("2p", base["stems"].get("pres_unstressed"), "ad")
    elif base.get("conj") == "er":
        addit("2s", base["stems"].get("pres_stressed"), "e")
        addit("2sv", base["stems"].get("pres_unstressed"), "é")
        addit("2p", base["stems"].get("pres_unstressed"), "ed")
    elif base.get("conj") == "ir":
        addit("2s", base["stems"].get("pres_stressed"), "e")
        addit("2sv", base["stems"].get("pres_unstressed"), "í")
        addit("2p", base["stems"].get("pres_unstressed"), "id")
    else:
        error("Internal error: Unrecognized conjugation " + base["conj"])

def add_non_present(base):
    def add_tense(slot, stem, s1, s2, s3, p1, p2, p3):
        add_single_stem_tense(base, slot, stem, s1, s2, s3, p1, p2, p3)

    stems = base["stems"]

    if stems.get("full_impf"):
        # An override needs to be supplied for the impf_1p due to the accent on the stem.
        add_tense("impf", stems.get("full_impf"), "a", "as", "a", {}, "ais", "an")
    elif base["conj"] == "ar":
        add_tense("impf", stems.get("impf"), "aba", "abas", "aba", "ábamos", "abais", "aban")
    else:
        add_tense("impf", stems.get("impf"), "ía", "ías", "ía", "íamos", "íais", "ían")

    if stems.get("pret_conj") == "irreg":
        add_tense("pret", stems.get("pret"), "e", "iste", "o", "imos", "isteis", "ieron")
    elif stems.get("pret_conj") == "ar":
        add_tense("pret", stems.get("pret"), "é", "aste", "ó", "amos", "asteis", "aron")
    else:
        add_tense("pret", stems.get("pret"), "í", "iste", "ió", "imos", "isteis", "ieron")

    if stems.get("pret_conj") == "ar":
        add_tense("impf_sub_ra", stems.get("impf_sub_ra"), "ara", "aras", "ara", "áramos", "arais", "aran")
        add_tense("impf_sub_se", stems.get("impf_sub_se"), "ase", "ases", "ase", "ásemos", "aseis", "asen")
        add_tense("fut_sub", stems.get("fut_sub"), "are", "ares", "are", "áremos", "areis", "aren")
    else:
        add_tense("impf_sub_ra", stems.get("impf_sub_ra"), "iera", "ieras", "iera", "iéramos", "ierais", "ieran")
        add_tense("impf_sub_se", stems.get("impf_sub_se"), "iese", "ieses", "iese", "iésemos", "ieseis", "iesen")
        add_tense("fut_sub", stems.get("fut_sub"), "iere", "ieres", "iere", "iéremos", "iereis", "ieren")

    add_tense("fut", stems.get("fut"), "é", "ás", "á", "emos", "éis", "án")
    add_tense("cond", stems.get("cond"), "ía", "ías", "ía", "íamos", "íais", "ían")

    # Do the participles.
    def addit(slot, stems, ending):
        add3(base, slot, base["prefix"], stems, ending)
    insert_form(base, "infinitive", {"form": base["verb"]})
    # TODO: wtf is this lua syntax
    addit("gerund", stems.get("pres_unstressed"), base["conj"] == "ar" and "ando" or "iendo")
    addit("pp_ms", stems.get("pp"), "o")
    addit("pp_fs", stems.get("pp"), "a")
    addit("pp_mp", stems.get("pp"), "os")
    addit("pp_fp", stems.get("pp"), "as")


# Remove monosyllabic accents (e.g. the 3sg preterite of fiar is fio not #fió). Note that there are a
# few monosyllabic verb forms that intentionally have an accent, to distinguish them from other words
# with the same pronunciation. These are as follows:
# (1) [[sé]] 1sg present indicative of [[saber]];
# (2) [[sé]] 2sg imperative of [[ser]];
# (3) [[dé]] 1sg and 3sg present subjunctive of [[dar]].
# For these, a * is added, which indicates that the accent needs to remain. If we see such a *, we remove
# it but otherwise leave the form alone.
def remove_monosyllabic_accents(base):
    for slot, accel in verb_slots_basic.items():
        for form in base["forms"].get(slot, []):
            if "*" in form["form"]: # * means leave alone any accented vowel
                form["form"] = form["form"].replace("*", "")
            elif not rfind(form["form"], r"^\-") and rfind(form["form"], AV) and not rfind(form["form"], V + C + V):
                # Has an accented vowel and no VCV sequence and not a suffix; may be monosyllabic, in which
                # case we need to remove the accent. Check # of syllables and remove accent if only 1. Note
                # that the checks for accented vowel and VCV sequence are not strictly needed, but are
                # optimizations to avoid running the whole syllabification algorithm on every verb form.
                syllables = com.syllabify(form["form"])
                if len(syllables) == 1:
                    form["form"] = com.remove_accent_from_syllable(syllables[0])



# Add the clitic pronouns in `pronouns` to the forms in `base_slot`. If `do_combined_slots` is given,
# store the results into the appropriate combined slots, e.g. `imp_2s_comb_lo` for second singular imperative + lo.
# Otherwise, directly modify `base_slot`. The latter case is used for handling reflexive verbs, and in that case
# `pronouns` should contain only a single pronoun.
def add_forms_with_clitic(base, base_slot, pronouns, do_combined_slots=False):
    if not base["forms"].get(base_slot):
        # This can happen, e.g. in only3s/only3sp verbs.
        return
    for form in base["forms"][base_slot]:
        # Figure out that correct accenting of the verb when a clitic pronoun is attached to it. We may need to
        # add or remove an accent mark:
        # (1) No accent mark currently, none needed: infinitive sentar because of sentarlo; imperative singular
        #     ten because of tenlo;
        # (2) Accent mark currently, still needed: infinitive oír because of oírlo;
        # (3) No accent mark currently, accent needed: imperative singular siente -> siénte because of siéntelo;
        # (4) Accent mark currently, not needed: imperative singular está -> estálo, sé -> selo.
        syllables = com.syllabify(form["form"])
        sylno = com.stressed_syllable(syllables)
        syllables.append("lo")
        needs_accent = com.accent_needed(syllables, sylno)
        if needs_accent:
            syllables[sylno] = com.add_accent_to_syllable(syllables[sylno])
        else:
            syllables[sylno] = com.remove_accent_from_syllable(syllables[sylno])
        syllables.pop() # remove added clitic pronoun
        reaccented_verb = "".join(syllables)
        for pronoun in pronouns:
            cliticized_verb = None
            # Some further special cases.
            if base_slot == "imp_1p" and (pronoun == "nos" or pronoun == "os"):
                # Final -s disappears: sintamos + nos -> sintámonos, sintamos + os -> sintámoos
                cliticized_verb = rsub(reaccented_verb, "s$", "") + pronoun
            elif base_slot == "imp_2p" and pronoun == "os":
                # Final -d disappears, which may cause an accent to be required:
                # haced + os -> haceos, sentid + os -> sentíos
                if reaccented_verb.endswith("id"):
                    cliticized_verb = rsub(reaccented_verb, "id$", "íos")
                else:
                    cliticized_verb = rsub(reaccented_verb, "d$", "os")
            else:
                cliticized_verb = reaccented_verb + pronoun
            if do_combined_slots:
                insert_form(base, base_slot + "_comb_" + pronoun,
                        {"form": cliticized_verb, "footnotes": form.get("footnotes", [])})
            else:
                form["form"] = cliticized_verb


# Generate the combinations of verb form (infinitive, gerund or various imperatives) + clitic pronoun.
def add_combined_forms(base):
    for base_slot, pronouns in verb_slot_combined_rows.items():
        # Skip non-infinitive/gerund combinations for reflexive verbs. We will copy the appropriate imperative
        # combinations later.
        if not base.get("refl") or base_slot == "infinitive" or base_slot == "gerund":
            add_forms_with_clitic(base, base_slot, pronouns, "do combined slots")

def process_slot_overrides(base, do_basic, reflexive_only=False):
    overrides = {}
    if reflexive_only:
        overrides = base["basic_reflexive_only_overrides"]
    elif do_basic:
        overrides = base["basic_overrides"]
    else:
        overrides = base["combined_overrides"]

    #local overrides = reflexive_only and base.basic_reflexive_only_overrides or
    #    do_basic and base.basic_overrides or base.combined_overrides
    for slot, forms in overrides.items():
        add(base, slot, base.get("prefix"), forms, False, "allow overrides")


# Add a reflexive pronoun or fixed clitic, e.g. [[lo]], as appropriate to the base form that were generated.
# `do_joined` means to do only the forms where the pronoun is joined to the end of the form; otherwise, do only the
# forms where it is not joined and precedes the form.
def add_reflexive_or_fixed_clitic_to_forms(base, do_reflexive, do_joined):
    for slot, accel in verb_slots_basic.items():
        clitic = None
        if not do_reflexive:
            clitic = base["clitic"]
        elif ("1" in slot or "2" in slot or "3" in slot):
            persnum = re.match("^.*_(.*?)$", slot).group(1)
            clitic = person_number_to_reflexive_pronoun[persnum]
        else:
            clitic = "se"

        if base["forms"].get(slot):
            if slot == "infinitive" or slot == "gerund" or slot.startswith("imp_"):
                if do_joined:
                    add_forms_with_clitic(base, slot, [clitic])
            elif do_reflexive and slot.startswith("pp_") or slot == "infinitive_linked":
                # do nothing with reflexive past participles or with infinitive linked (handled at the end)
                pass
            elif slot.startswith("neg_imp_"):
                raise ValueError("Internal error: Should not have forms set for negative imperative at this stage")
            elif not do_joined:
                # Add clitic as separate word before all other forms. Check whether form already has brackets
                # (as will be the case if the form has a fixed clitic).
                for form in base["forms"][slot]:
                    if base["args"].get("noautolinkverb"):
                        form["form"] = clitic + " " + form["form"]
                    else:
                        clitic_pref = "[[" + clitic + "]] "
                        if "[[" in form["form"]:
                            form["form"] = clitic_pref + form["form"]
                        else:
                            form["form"] = clitic_pref + "[[" + form["form"] + "]]"



def copy_subjunctives_to_imperatives(base):
    # Copy subjunctives to imperatives, unless there's an override for the given slot (as with the imp_1p of [[ir]]).
    for persnum in ["3s", "1p", "3p"]:
        _from = "pres_sub_" + persnum
        _to = "imp_" + persnum
        insert_forms(base, _to, iut.map_forms(base["forms"].get(_from), lambda form, translit: [form, translit]))


def handle_infinitive_linked(base):

    def f(form, translit):
        if form == base["lemma"] and rfind(base["linked_lemma"], r"\[\["):
            return base["linked_lemma"], None
        return form, None

    # Compute linked versions of potential lemma slots, for use in {{es-verb}}.
    # We substitute the original lemma (before removing links) for forms that
    # are the same as the lemma, if the original lemma has links.
    for slot in ["infinitive"]:
        insert_forms(base, slot + "_linked", iut.map_forms(base["forms"][slot], f))



def generate_negative_imperatives(base):
    def f(form, translit=None):
        if base["args"].get("noautolinkverb"):
            return "no " + form
        elif "[[" in form:
            # already linked, e.g. when reflexive
            return "[[no]] " + form, None
        else:
            return "[[no]] [[" + form + "]]", None

    # Copy subjunctives to negative imperatives, preceded by "no".
    for persnum in ["2s", "3s", "1p", "2p", "3p"]:
        _from = "pres_sub_" + persnum
        _to = "neg_imp_" + persnum
        insert_forms(base, _to, iut.map_forms(base["forms"].get(_from), f))


def copy_imperatives_to_reflexive_combined_forms(base):
    copy_table = {
        "imp_2s": "imp_2s_comb_te",
        "imp_3s": "imp_3s_comb_se",
        "imp_1p": "imp_1p_comb_nos",
        "imp_2p": "imp_2p_comb_os",
        "imp_3p": "imp_3p_comb_se",
    }

    def f(form, translit):
        return form, translit

    # Copy imperatives (with the clitic reflexive pronoun already added) to the appropriate "combined" reflexive
    # forms.
    for _from, _to in copy_table.items():
        # Need to call map_forms() to clone the form objects because insert_forms() doesn't clone them, and may
        # side-effect them when inserting footnotes.
        if _from in base["forms"]:
            insert_forms(base, _to, iut.map_forms(base["forms"][_from], f))

def add_missing_links_to_forms(base):
    # Any forms without links should get them now. Redundant ones will be stripped later.
    for slot, forms in base["forms"].items():
        for form in forms:
            if not "[[" in form["form"]:
                form["form"] = "[[" + form["form"] + "]]"


def conjugate_verb(base):
    add_present_indic(base)
    add_present_subj(base)
    add_imper(base)
    add_non_present(base)
    # This should happen before add_combined_forms() so overrides of basic forms end up part of the combined forms.
    process_slot_overrides(base, "do basic") # do basic slot overrides
    # This should happen after process_slot_overrides() in case a derived slot is based on an override (as with the
    # imp_3s of [[dar]], [[estar]]).
    copy_subjunctives_to_imperatives(base)
    # This should happen after process_slot_overrides() because overrides may have accents in them that need to be
    # removed. (This happens e.g. for most present indicative forms of [[ver]], which have accents in them for the
    # prefixed derived verbs, but the accents shouldn't be present in the base verb.)
    remove_monosyllabic_accents(base)
    if not base.get("nocomb"):
        # This should happen before add_reflexive_pronouns() because the combined forms of reflexive verbs don't have
        # the reflexive attached.
        add_combined_forms(base)

    # We need to add joined reflexives, then joined and non-joined clitics, then non-joined reflexives, so we get
    # [[házmelo]] but [[no]] [[me]] [[lo]] [[haga]].
    if base.get("refl"):
        # This should happen after remove_monosyllabic_accents() so the * marking the preservation of monosyllabic
        # accents doesn't end up in the middle of a word.
        add_reflexive_or_fixed_clitic_to_forms(base, "do reflexive", "do joined")
        process_slot_overrides(base, "do basic", "do reflexive") # do reflexive-only basic slot overrides

    if base.get("clitic"):
        # This should happen after reflexives are added.
        add_reflexive_or_fixed_clitic_to_forms(base, False, "do joined")
        add_reflexive_or_fixed_clitic_to_forms(base, False, False)

    if base.get("refl"):
        add_reflexive_or_fixed_clitic_to_forms(base, "do reflexive", False)

    # This should happen after add_reflexive_or_fixed_clitic_to_forms() so negative imperatives get the reflexive pronoun
    # and clitic in them.
    generate_negative_imperatives(base)
    if not base.get("nocomb"):
        if base.get("refl"):
            # This should happen after process_slot_overrides() for reflexive-only basic slots so the overridden
            # forms (e.g. [[idos]]/[[iros]] for [[ir]]) get appropriately copied.
            copy_imperatives_to_reflexive_combined_forms(base)
        process_slot_overrides(base, False) # do combined slot overrides

    # This should happen before add_missing_links_to_forms() so that the comparison `form == base.lemma`
    # in handle_infinitive_linked() works correctly and compares unlinked forms to unlinked forms.
    handle_infinitive_linked(base)
    if not base["args"].get("noautolinkverb"):
        add_missing_links_to_forms(base)

def parse_indicator_spec(angle_bracket_spec, lemma):
    base = {}
    def parse_err(msg):
        raise ValueError(msg + ": " + angle_bracket_spec)

    def fetch_footnotes(separated_group):
        footnotes = []
        for j in range(1, len(separated_group), 2):
            if separated_group[j+1] != "":
                parse_err("Extraneous text after bracketed footnotes: '" + separated_group + "'")
            footnotes.append(separated_group[j])
        return footnotes

    inside = rmatch(angle_bracket_spec, "^<(.*)>$", 1)
    if not inside:
        return base

    segments = iut.parse_balanced_segment_run(inside, "[", "]")
    dot_separated_groups = iut.split_alternating_runs(segments, r"\.")
    for dot_separated_group in dot_separated_groups:
        comma_separated_groups = iut.split_alternating_runs(dot_separated_group, r"\s*,\s*")
        first_element = comma_separated_groups[0][0]
        if first_element in vowel_alternants:
            for j in range(0, len(comma_separated_groups)):
                alt = comma_separated_groups[j][0]
                if not alt in vowel_alternants:
                    parse_err("Unrecognized vowel alternant '" + alt + "'")
                if base.get("vowel_alt"):
                    for existing_alt in base["vowel_alt"]:
                        if existing_alt["form"] == alt:
                            parse_err("Vowel alternant '" + alt + "' specified twice")
                else:
                    base["vowel_alt"] = []

                base["vowel_alt"] = [{"form": alt, "footnotes": fetch_footnotes(comma_separated_groups[j])}]

        elif (first_element == "no_pres_stressed" or first_element == "no_pres1_and_sub" or \
                first_element == "only3s" or first_element == "only3sp"):
            if len(comma_separated_groups[0]) > 1:
                parse_err("No footnotes allowed with '" + first_element + "' spec")
            if base.get(first_element):
                parse_err("Spec '" + first_element + "' specified twice")
            base[first_element] = True
        else:
            parse_err("Unrecognized spec '" + comma_separated_groups[0][0] + "'")

    return base


# Normalize all lemmas, substituting the pagename for blank lemmas and adding links to multiword lemmas.
def normalize_all_lemmas(alternant_multiword_spec):

    # (1) Add links to all before and after text.
    if not alternant_multiword_spec["args"].get("noautolinktext"):
        alternant_multiword_spec["post_text"] = com.add_links(alternant_multiword_spec["post_text"], False)
        for alternant_or_word_spec in alternant_multiword_spec["alternant_or_word_specs"]:
            alternant_or_word_spec["before_text"] = com.add_links(alternant_or_word_spec["before_text"], False)
            if alternant_or_word_spec.get("alternants"):
                for multiword_spec in alternant_or_word_spec["alternants"]:
                    multiword_spec["post_text"] = com.add_links(multiword_spec["post_text"])
                    for word_spec in multiword_spec["word_specs"]:
                        word_spec["before_text"] = com.add_links(word_spec["before_text"])

    def f(base):
        if base.get("lemma", "") == "":
            base["lemma"] = lua_or(alternant_multiword_spec["args"]["pagename"], alternant_multiword_spec["args"].get("head",[None])[0])
            if not base["lemma"]:
                #PAGENAME = mw.title.getCurrentTitle().text
                base["lemma"] = PAGENAME

        base["user_specified_lemma"] = base["lemma"]

        base["lemma"] = m_links_remove_links(base["lemma"])
        refl_verb, clitic = rmatch(base["lemma"], "^(.*?)(l[aeo]s?)$", 2)
        if not refl_verb:
            refl_verb, clitic = base["lemma"], None
        verb, refl = rmatch(refl_verb, "^(.*?)(se)$", 2)
        if not verb:
            verb, refl = refl_verb, None
        base["user_specified_verb"] = verb
        base["refl"] = refl
        base["clitic"] = clitic

        if base["refl"] and base["clitic"]:
            # We have to parse the verb suffix to see how to construct the base verb; e.g.
            # abrírsela -> abrir but oírsela -> oír. We parse the verb suffix again in all cases
            # in detect_indicator_spec(), after splitting off the prefix of irrregular verbs.
            actual_verb = None
            inf_stem, suffix = rmatch(base["user_specified_verb"], "^(.*)([aáeéií]r)$", 2)
            if not inf_stem:
                raise ValueError("Unrecognized infinitive: " + base["user_specified_verb"])
            if suffix == "ír" and inf_stem[-1] in "aoe":
                # accent on suffix should remain
                base["verb"] = base["user_specified_verb"]
            else:
                base["verb"] = inf_stem + com.remove_accent_from_syllable(suffix)
        else:
            base["verb"] = base["user_specified_verb"]

        linked_lemma = None
        if alternant_multiword_spec["args"].get("noautolinkverb") or (base.get("user_specified_lemma") and "[[" in base["user_specified_lemma"]):
            linked_lemma = base["user_specified_lemma"]
        elif base["refl"] or base["clitic"]:
            # Reconstruct the linked lemma with separate links around base verb, reflexive pronoun and clitic.
            # TODO : wtf lua
            linked_lemma = "x"
            #base.get("user_specified_verb") == base["verb"] and "[[" + base.user_specified_verb + "]]" or
            #    "[[" + base.verb + "|" + base["user_specified_verb"] + "]]"
            linked_lemma = linked_lemma + (refl and "[[" + refl + "]]" or "") + \
                (clitic and "[[" + clitic + "]]" or "")
        else:
            # Add links to the lemma so the user doesn't specifically need to, since we preserve
            # links in multiword lemmas and include links in non-lemma forms rather than allowing
            # the entire form to be a link.
            linked_lemma = com.add_links(base["user_specified_lemma"])
        base["linked_lemma"] = linked_lemma

    # (2) Remove any links from the lemma, but remember the original form
    #     so we can use it below in the 'lemma_linked' form.
    iut.map_word_specs(alternant_multiword_spec, f)

def construct_stems(base):

    stems = base["stems"]
    stems["pres_unstressed"] = stems.get("pres_unstressed", base.get("inf_stem"))

    if stems.get("pres_stressed"):
        pass
    # If no_pres_stressed given, pres_stressed stem should be empty so no forms are generated.
    elif base.get("no_pres_stressed"):
        pass
    else:
        stems["pres_stressed"] = \
        base.get("vowel_alt",
        base.get("inf_stem"))

    if stems.get("pres1_and_sub"):
        pass
    # If no_pres_stressed given, the entire subjunctive is missing.
    elif base.get("no_pres_stressed"):
        pass
   # If no_pres1_and_sub given, pres1 and entire subjunctive are missing.
    elif base.get("no_pres_stressed"):
        pass
    else:
        pass
        #stems["pres1_and_sub"] = None

    stems["pres1"] = stems.get("pres1", stems.get("pres1_and_sub", stems.get("pres_stressed")))
    stems["impf"] = stems.get("impf", base.get("inf_stem"))
    stems["pret"] = stems.get("pret", base.get("inf_stem"))
    stems["pret_conj"] = stems.get("pret_conj", base.get("conj"))
    stems["fut"] = stems.get("fut", base.get("inf_stem") + base.get("conj"))
    stems["cond"] = stems.get("cond", stems.get("fut"))
    stems["pres_sub_stressed"] = stems.get("pres_sub_stressed", stems.get("pres1"))
    stems["pres_sub_unstressed"] = stems.get("pres_sub_unstressed", stems.get("pres1_and_sub", stems.get("pres_unstressed")))
    stems["impf_sub_ra"] = stems.get("impf_sub_ra", stems.get("pret"))
    stems["impf_sub_se"] = stems.get("impf_sub_se", stems.get("pret"))
    stems["fut_sub"] = stems.get("fut_sub", stems.get("pret"))
    stems["pp"] = stems.get("pp", 
        combine_stem_ending(base, "pp_ms", base.get("inf_stem"), "ad", "is combining ending")
        if base.get("conj") == "ar" else
    #    # use combine_stem_ending esp. so we get reído, caído, etc.
        combine_stem_ending(base, "pp_ms", base.get("inf_stem"), "id", "is combining ending"))


def detect_indicator_spec(base):
    base["forms"] = {}
    base["stems"] = {}

    if base.get("only3s") and base.get("only3sp"):
        raise ValueError("'only3s' and 'only3sp' cannot both be specified")

    base["basic_overrides"] = {}
    base["basic_reflexive_only_overrides"] = {}
    base["combined_overrides"] = {}
    for irreg_conj in irreg_conjugations:
        if callable(irreg_conj.get("match")):
            res = irreg_conj["match"](base["verb"])
            if not res:
                res = [None, None]
            base["prefix"], base["non_prefixed_verb"] = res
        elif irreg_conj["match"].startswith("^") and irreg_conj["match"][1:] == base["verb"]:
            # begins with ^, for exact match, and matches
            base["prefix"], base["non_prefixed_verb"] = "", base["verb"]
        else:
            base["prefix"], base["non_prefixed_verb"] = rmatch(base["verb"], "^(.*)(" + irreg_conj["match"] + ")$", 2)
        if base["prefix"] is not None:
            # we found an irregular verb
            base["irreg_verb"] = True
            for stem, forms in irreg_conj["forms"].items():
                if stem.startswith("refl_"):
                    stem = rsub(stem, "^refl_", "")
                    if not verb_slots_basic_map[stem]:
                        raise ValueError("Internal error: setting for 'refl_" + stem + "' does not refer to a basic verb slot")
                    base["basic_reflexive_only_overrides"][stem] = forms
                elif verb_slots_basic_map.get(stem):
                    # an individual form override of a basic form
                    base["basic_overrides"][stem] = forms
                elif verb_slots_combined_map.get(stem):
                    # an individual form override of a combined form
                    base["combined_overrides"][stem] = forms
                else:
                    base["stems"][stem] = forms
            break

    base["prefix"] = base.get("prefix", "")
    if not base["non_prefixed_verb"]:
        base["non_prefixed_verb"] = base["verb"]
    inf_stem, suffix = rmatch(base["non_prefixed_verb"], "^(.*)([aeií]r)$", 2)
    if not suffix:
        raise ValueError("Unrecognized infinitive: " + base["verb"])

    base["inf_stem"] = inf_stem
    suffix = suffix == "ír" and "ir" or suffix
    base["conj"] = suffix
    base["frontback"] = ternery(suffix == "ar", "back", "front")

    if base["stems"].get("vowel_alt"): # irregular verb with specified vowel alternation
        if base.get("vowel_alt"):
            raise ValueError(base["verb"] + " is a recognized irregular verb, and should not have vowel alternations specified with it")
        base["vowel_alt"] = iut.convert_to_general_list_form(base["stems"].get("vowel_alt"))

    # Convert vowel alternation indicators into stems.
    if base.get("vowel_alt"):
        for altform in base["vowel_alt"]:
            altform["alt"] = altform["form"] # save original indicator
            alt = altform["alt"]
            if base.get("conj") == "ir":
                raising = (
                    alt == "ie-i" or alt == "ye-i" or alt == "ue-u" or alt == "i" or alt == "í" or alt == "ú"
                )
                if base["stems"].get("raising_conj") is None:
                    base["stems"]["raising_conj"] = raising
                elif base["stems"]["raising_conj"] != raising:
                    raise ValueError("Can't currently support a mixture of raising (e.g. 'ie-i') and non-raising (e.g. 'ie') vowel alternations in -ir verbs")
            if alt == "+":
                altform["form"] = base["inf_stem"]
            else:
                normalized_alt = alt
                if alt == "ie-i" or alt == "ye-i" or alt == "ue-u":
                    if base["conj"] != "ir":
                        raise ValueError("Vowel alternation '" + alt + "' only supported with -ir verbs")
                    # ie-i is like i except for the vowel raising before i+V, similarly for ye-i, ue-u,
                    # so convert appropriately.
                    normalized_alt = alt == "ie-i" and "ie" or alt == "ye-i" and "ye" or "ue"
                ret = com.apply_vowel_alternation(base["inf_stem"], normalized_alt)
                if ret.get("err"):
                    raise ValueError("To use '" + alt + "', present stem '" + base["inf_stem"] + "' " + ret["err"])
                altform["form"] = ret["ret"]


def detect_all_indicator_specs(alternant_multiword_spec, from_headword):
    # Propagate some settings up or down.
    def f1(base):
        if base.get("refl"):
            alternant_multiword_spec["refl"] = True
        if base.get("clitic"):
            alternant_multiword_spec["clitic"] = True
        base["from_headword"] = from_headword
        base["args"] = alternant_multiword_spec["args"]
        # If fixed clitic, don't include combined forms.
        base["nocomb"] = alternant_multiword_spec["args"].get("nocomb", base["clitic"])
    iut.map_word_specs(alternant_multiword_spec, f1)


    def validate_refl(base):
        if not base.get("refl"):
            raise ValueError("If some alternants are reflexive, all must be")

    if not from_headword and not alternant_multiword_spec.get("args.nocomb"):
        # If we have a combined table, we run into issues if we have multiple
        # verbs and some are reflexive and some aren't, because we use a
        # different table for reflexive verbs. So throw an error.
        if alternant_multiword_spec.get("refl"):
            iut.map_word_specs(alternant_multiword_spec, validate_refl)

    def f2(base):
        detect_indicator_spec(base)
        construct_stems(base)

    iut.map_word_specs(alternant_multiword_spec, f2)

def compute_categories_and_annotation(alternant_multiword_spec, from_headword):
    # not implemented
    return

# Externally callable function to parse and conjugate a verb given user-specified arguments.
# Return value is WORD_SPEC, an object where the conjugated forms are in `WORD_SPEC.forms`
# for each slot. If there are no values for a slot, the slot key will be missing. The value
# for a given slot is a list of objects {form=FORM, footnotes=FOOTNOTES}.
def do_generate_forms(args, from_headword, d, PAGENAME):
    params = {
        1: {},
        "nocomb": {"type": "boolean"},
        "noautolinktext": {"type": "boolean"},
        "noautolinkverb": {"type": "boolean"},
    }

    if from_headword:
        params["head"] = {"list": True}
        params["pres"] = {"list": True} # present
        params["pres_qual"] = {"list": "pres=_qual", "allow_holes": True}
        params["pret"] = {"list": True} # preterite
        params["pret_qual"] = {"list": "pret=_qual", "allow_holes": True}
        params["part"] = {"list": True} # participle
        params["part_qual"] = {"list": "part=_qual", "allow_holes": True}
        params["pagename"] = {} # for testing
        params["attn"] = {"type": "boolean"}
        params["id"] = {}
        params["json"] = {}
        params["pagename"] = {}
        params["new"] = {} # temporary hack; will remove

    #args = require("Module:parameters").process(parent_args, params)

    arg1 = args[1]
    if not arg1 and from_headword:
        arg1 = args.pagename or args.head[1]

    if not arg1:
        if PAGENAME == "es-conj" or PAGENAME == "es-verb":
            arg1 = d or "licuar<+,ú>"
        else:
            arg1 = PAGENAME

    if " " in arg1 and not "<" in arg1:
        # If multiword lemma without <> already, try to add it after the first word.

        need_explicit_angle_brackets = False
        if "((" in arg1:
            need_explicit_angle_brackets = True
        else:
            refl_clitic_verb, orig_refl_clitic_verb, post = None, None, None

            # Try to preserve the brackets in the part after the verb, but don't do it
            # if there aren't the same number of left and right brackets in the verb
            # (which means the verb was linked as part of a larger expression).
            refl_clitic_verb, post = rmatch(arg1, "^(.*?)( .*)$", 2)
            left_brackets = rsub(refl_clitic_verb, r"[^\[]", "")
            right_brackets = rsub(refl_clitic_verb, r"[^\]]", "")
            if len(left_brackets) == len(right_brackets):
                arg1 = refl_clitic_verb + "<>" + post
            else:
                need_explicit_angle_brackets = True

        if need_explicit_angle_brackets:
            raise ValueError("Multiword argument without <> and with alternants, a multiword linked verb or unbalanced brackets; please include <> explicitly: " + arg1)

    parse_props = {
        "parse_indicator_spec": parse_indicator_spec,
        "lang": lang,
        "allow_default_indicator": True,
        "allow_blank_lemma": True,
    }

    escaped_arg1 = escape_reflexive_indicators(arg1)
    alternant_multiword_spec = iut.parse_inflected_text(escaped_arg1, parse_props)
    pos = None
    alternant_multiword_spec["pos"] = lua_or(pos, "verbs")
    alternant_multiword_spec["args"] = args

    normalize_all_lemmas(alternant_multiword_spec)

    detect_all_indicator_specs(alternant_multiword_spec, from_headword)
    inflect_props = {
        "slot_list": all_verb_slots,
        "lang": lang,
        "inflect_word_spec": conjugate_verb,
        # We add links around the generated verbal forms rather than allow the entire multiword
        # expression to be a link, so ensure that user-specified links get included as well.
        "include_user_specified_links": True,
    }

    iut.inflect_multiword_or_alternant_multiword_spec(alternant_multiword_spec, inflect_props)

    # Remove redundant brackets around entire forms.
    for slot, forms in alternant_multiword_spec["forms"].items():
        for form in forms:
            form["form"] = com.strip_redundant_links(form["form"])

    #compute_categories_and_annotation(alternant_multiword_spec, from_headword)
    return alternant_multiword_spec

# Concatenate all forms of all slots into a single string of the form
# "SLOT=FORM,FORM,...|SLOT=FORM,FORM,...|...". Embedded pipe symbols (as might occur
# in embedded links) are converted to <!>. If INCLUDE_PROPS is given, also include
# additional properties (currently, none). This is for use by bots.
def concat_forms(alternant_multiword_spec, include_props):
    ins_text = []
    for slot in all_verb_slots:
        formtext = iut.concat_forms_in_slot(alternant_multiword_spec["forms"].get(slot))
        if formtext:
            ins_text.append(slot + "=" + formtext)
    return "|".join(ins_text)


# Template-callable function to parse and conjugate a verb given user-specified arguments and return
# the forms as a string "SLOT=FORM,FORM,...|SLOT=FORM,FORM,...|...". Embedded pipe symbols (as might
# occur in embedded links) are converted to <!>. If |include_props=1 is given, also include
# additional properties (currently, none). This is for use by bots.
def generate_forms(args, include_props):
    alternant_multiword_spec = do_generate_forms(args)
    return concat_forms(alternant_multiword_spec, include_props)



