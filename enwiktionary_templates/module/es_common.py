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
Based on https://en.wiktionary.org/wiki/Module:es-common
 22:42, 11 April 2021
"""

import re

TEMPC1 = u'\uFFF1'
TEMPC2 = u'\uFFF2'
TEMPV1 = u'\uFFF3'

vowel = "aeiouáéíóúý" + TEMPV1
V = f"[{vowel}]"
AV = "[áéíóúý]" # accented vowel
W = "[iyuw]" # glide
C = f"[^{vowel}.]"

remove_accent = {
    "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ý": "y"
}
add_accent = {
    "a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "y": "ý"
}

def rfind(string, pattern):
    return re.search(pattern, string)

def rsub(string, pattern, replacement):
    return re.sub(pattern, replacement, string)

# apply rsub() repeatedly until no change
def rsub_repeatedly(term, foo, bar):
    while True:
        new_term = rsub(term, foo, bar)
        if new_term == term:
            return term
        term = new_term

def rsplit(string, pattern):
    return re.split(pattern, string)

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

    if count >1:
        return [None] * count
    return None

def ternery(cond, v1, v2):
    if cond:
        return v1
    return v2


def apply_vowel_alternation(stem, alternation):
    ret, err = None, None
    # Treat final -gu, -qu as a consonant, so the previous vowel can alternate (e.g. conseguir -> consigo).
    # This means a verb in -guar can't have a u-ú alternation but I don't think there are any verbs like that.
    stem = rsub(stem, "([gq])u$", r"\1" + TEMPC1)
    before_last_vowel, last_vowel, after_last_vowel = rmatch(stem, "^(.*)(" + V + ")(.*?)$", 3)

    if alternation == "ie":
        if last_vowel == "e" or last_vowel == "i":
            # allow i for adquirir -> adquiero, inquirir -> inquiero, etc.
            ret = before_last_vowel + "ie" + after_last_vowel
        else:
            err = "should have -e- or -i- as the last vowel"
    elif alternation == "ye":
        if last_vowel == "e":
            ret = before_last_vowel + "ye" + after_last_vowel
        else:
            err = "should have -e- as the last vowel"
    elif alternation == "ue":
        if last_vowel == "o" or last_vowel == "u":
            # allow u for jugar -> juego; correctly handle avergonzar -> avergüenzo
            if last_vowel == "o" and before_last_vowel.endswith("g"):
                ret = before_last_vowel + "üe" + after_last_vowel
            else:
                ret = before_last_vowel + "ue" + after_last_vowel
        else:
            err = "should have -o- or -u- as the last vowel"
    elif alternation == "hue":
        if last_vowel == "o":
            ret = before_last_vowel + "hue" + after_last_vowel
        else:
            err = "should have -o- as the last vowel"
    elif alternation == "i":
        if last_vowel == "e":
            ret = before_last_vowel + "i" + after_last_vowel
        else:
            err = "should have -i- as the last vowel"
    elif alternation == "í":
        if last_vowel == "e" or last_vowel == "i":
            # allow e for reír -> río, sonreír -> sonrío
            ret = before_last_vowel + "í" + after_last_vowel
        else:
            err = "should have -e- or -i- as the last vowel"
    elif alternation == "ú":
        if last_vowel == "u":
            ret = before_last_vowel + "ú" + after_last_vowel
        else:
            err = "should have -u- as the last vowel"
    else:
        error("Internal error: Unrecognized vowel alternation '" + alternation + "'")

    if ret:
        ret = ret.replace(TEMPC1, "u")
    return {"ret": ret, "err": err}


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
    word = rsub(word, r"([pbcktdg])\.([lr])", r".\1\2")
    word = rsub_repeatedly(word, "(" + C + r")\.s(" + C + ")", r"\1s.\2")
    # Any aeo, or stressed iu, should be syllabically divided from a following aeo or stressed iu.
    word = rsub_repeatedly(word, "([aeoáéíóúý])([aeoáéíóúý])", r"\1.\2")
    word = rsub_repeatedly(word, "([ií])([ií])", r"\1.\2")
    word = rsub_repeatedly(word, "([uú])([uú])", r"\1.\2")
    word = rsub(word, DIV, "")
    word = rsub(word, TEMPC1, "i")
    word = rsub(word, TEMPC2, "u")
    word = rsub(word, TEMPV1, "y")

    return rsplit(word, r"\.")

# Return the index of the (last) stressed syllable.
def stressed_syllable(syllables):
    # If a syllable is stressed, return it.
    for i in range(len(syllables)-1, -1, -1):
        if rfind(syllables[i], AV):
            return i

    # Monosyllabic words are stressed on that syllable.
    if len(syllables) == 1:
        return 0

    i = len(syllables)-1
    # Unaccented words ending in a vowel or a vowel + s/n are stressed on the preceding syllable.
    if rfind(syllables[i], V + "[sn]?$"):
        return i - 1

    # Remaining words are stressed on the last syllable.
    return i

def add_accent_to_syllable(syllable):
    # Don't do anything if syllable already stressed.
    if rfind(syllable, AV):
        return syllable

    # Prefer to accent an a/e/o in case of a diphthong or triphthong (the first one if for some reason
    # there are multiple, which should not occur with the standard syllabification algorithm);
    # otherwise, do the last i or u in case of a diphthong ui or iu.
    if rfind(syllable, "[aeo]"):
        return rsub(syllable, r"^(.*?)([aeo])", lambda m: m.group(1) + add_accent[m.group(2)])

    return rsub(syllable, r"^(.*)([iu])", lambda m: m.group(1) + add_accent[m.group(2)])

# Remove any accent from a syllable.
def remove_accent_from_syllable(syllable):
    return rsub(syllable, AV, lambda m: remove_accent.get(m.group(0), m.group(0)))

# Return true if an accent is needed on syllable number `sylno` if that syllable were to receive the stress,
# given the syllables of a word. The current accent may be on any syllable.
def accent_needed(syllables, sylno):
    # Diphthongs iu and ui are normally stressed on the second vowel, so if the accent is on the first vowel,
    # it's needed.
    if rfind(syllables[sylno], "íu") or rfind(syllables[sylno], "úi"):
        return True

    # If the default-stressed syllable is different from `sylno`, accent is needed.
    unaccented_syllables = []
    for syl in syllables:
        unaccented_syllables.append(remove_accent_from_syllable(syl))

    would_be_stressed_syl = stressed_syllable(unaccented_syllables)
    if would_be_stressed_syl != sylno:
        return True

    # At this point, we know that the stress would by default go on `sylno`, given the syllabification in
    # `syllables`. Now we have to check for situations where removing the accent mark would result in a
    # different syllabification. For example, países -> `pa.i.ses` but removing the accent mark would lead
    # to `pai.ses`. Similarly, río -> `ri.o` but removing the accent mark would lead to single-syllable `rio`.
    # We need to check whether (a) the stress falls on an i or u; (b) in the absence of an accent mark, the
    # i or u would form a diphthong with a preceding or following vowel and the stress would be on that vowel.
    # The conditions are slightly different when dealing with preceding or following vowels because ui and ui
    # diphthongs are by default stressed on the second vowel. We also have to ignore h between the vowels.
    accented_syllable = add_accent_to_syllable(unaccented_syllables[sylno])
    if sylno > 0 and rfind(unaccented_syllables[sylno - 1], "[aeo]$") and rfind(accented_syllable, "^h?[íú]"):
        return True

    if sylno < len(syllables)-1:
        if rfind(accented_syllable, "í$") and rfind(unaccented_syllables[sylno + 1], "^h?[aeou]") or \
            rfind(accented_syllable, "ú$") and rfind(unaccented_syllables[sylno + 1], "^h?[aeio]"):
            return True
    return False

def add_links(form, multiword_only=False):
    return form
    #raise ValueError("not implemented")

def strip_redundant_links(form):
    # Strip redundant brackets surrounding entire form.
    res = rmatch(form, r"^\[\[([^\[\]]*)\]\]$", 1)
    if res:
        return res
    return form
