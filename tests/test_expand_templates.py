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
import pytest
import enwiktionary_templates
import mwparserfromhell

expand_template = enwiktionary_templates.expand_template
expand_templates = enwiktionary_templates.expand_templates

def _expand(text, pagename="test"):
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, pagename)
    return str(wikt)

def test_get_params():
    template = next(mwparserfromhell.parse("{{test|XX|one<f:foo><b:bar>|two<f:foo>|three<b:bar>}}}").ifilter_templates())
    assert enwiktionary_templates.get_params(template) == {1: 'XX', 2: 'one', 'f1': 'foo', 'b1': 'bar', 3: 'two', 'f2': 'foo', 4: 'three', 'b3': 'bar'}

def test_expand_template():

    template = next(mwparserfromhell.parse("{{XXX_unknown_XXX|test}}}").ifilter_templates())
    assert expand_template(template, "test") == "{{XXX_unknown_XXX|test}}"

    template = next(mwparserfromhell.parse("{{gloss|test}}}").ifilter_templates())
    assert expand_template(template, "test") == "(test)"

    template = next(mwparserfromhell.parse("{{gl|test}}}").ifilter_templates())
    assert expand_template(template, "test") == "(test)"

    template = next(mwparserfromhell.parse("{{g|test}}}").ifilter_templates())
    assert expand_template(template, "test") == "{test}"

    template = next(mwparserfromhell.parse("{{lb|en|test1|test2|test3}}}").ifilter_templates())
    assert expand_template(template, "test") == "(test1, test2, test3)"

    template = next(mwparserfromhell.parse("{{ellipsis of |es|Antigua Guatemala|nocap=1}}").ifilter_templates())
    assert expand_template(template, "test") == 'ellipsis of "Antigua Guatemala"'

#def test_indtr():
#    template = next(mwparserfromhell.parse("{{indtr|es|en|.also|.figurative}}").ifilter_templates())
#    assert expand_template(template, "test") == "xx"

def test_expand_templates():

    text = "{{lb|en|test}} blah {{gloss|test}}"
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == "(test) blah (test)"

    #text = "{{lb|es|reflexive|_|+ {{m|es|por}}}}"
    text = "{{q|+ {{m|es|test}}}}"
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == "(+ ''test'')"

    text = "{{m|la|argentum||silver}}"
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == "''argentum'' (“silver”)"

    text = "{{etyl|la|en}}"
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == "Latin"

    assert _expand("{{suffix|en|do|ing}}") == "do + -ing"
    assert _expand("{{suffix|en|do|-ing}}") == "do + -ing"

    assert _expand("{{back-form|en}}") == "Back formation"

    assert _expand("From {{inh|es|la|-andus}}. Compare {{cog|it|-}} and {{cog|pt|-ando}}, {{cog|ro|-ând}}, {{cog|fr|-ant}}.") == 'From Latin "-andus". Compare Italian and Portuguese "-ando", Romanian "-ând", French "-ant".'

def test_acronym_of():
    assert _expand("{{acronym of|es||Universidad Católica Andrés Bello}}") == 'acronym of "Universidad Católica Andrés Bello"'

def test_af():
    assert _expand("{{af|en|volley|ball}}") == "volley + ball"
    assert _expand("{{affix|en|pest|-i-|-cide}}") == "pest + -i- + -cide"

    assert _expand("{{af|es|lang1=mxi|Galib|t1=victorious|-ez|lit=son of the victorious}}") == 'Mozarabic Galib ("victorious") + -ez'
    assert _expand("{{af|es|a-|bancal|gloss2=terrace, plot of land|-ar}}") == 'a- + bancal ("terrace, plot of land") + -ar'

    assert _expand("{{blend|he|תַּשְׁבֵּץ|tr1=tashbéts|t1=crossword puzzle|חֵץ|t2=arrow|tr2=chets}}") == 'Blend of תַּשְׁבֵּץ (tashbéts, "crossword puzzle") + חֵץ (chets, "arrow")'

    assert _expand("{{af|es|en-|كَرَامَة<lang:ar>|-ar}}") == 'en- + Arabic كَرَامَة + -ar'
    assert _expand("{{af|es|en-|ar:كَرَامَة|-ar}}") == 'en- + Arabic كَرَامَة + -ar'

def test_doublet():
    assert _expand("{{doublet|en|test}}") == "Doublet of test"

    assert _expand("{{doublet|en|test|notext=1}}") == "test"

    assert _expand("{{doublet|en|test|nocap=1}}") == "doublet of test"

    assert _expand("{{doublet|en|test|test2}}") == "Doublet of test, test2"

def test_newlabels():
    template = next(mwparserfromhell.parse("{{lb|en|test}}").ifilter_templates())
    assert expand_template(template, "test") == "(test)"

    template = next(mwparserfromhell.parse("{{lb|en|test|test}}").ifilter_templates())
    assert expand_template(template, "test") == "(test, test)"

    template = next(mwparserfromhell.parse("{{lb|en|test|and|test}}").ifilter_templates())
    assert expand_template(template, "test") == "(test and test)"

    # Alias
    template = next(mwparserfromhell.parse("{{lb|en|test|&|test}}").ifilter_templates())
    assert expand_template(template, "test") == "(test and test)"

    # Topical
    template = next(mwparserfromhell.parse("{{lb|en|alchemy}}").ifilter_templates())
    assert expand_template(template, "test") == "([[alchemy]])"

    # Regional
    template = next(mwparserfromhell.parse("{{lb|en|Peru}}").ifilter_templates())
    assert expand_template(template, "test") == "([[w:Peru|Peru]])"

    # Make sure language specific subvarieties work
    template = next(mwparserfromhell.parse("{{lb|es|Latin American Spanish}}").ifilter_templates())
    assert expand_template(template, "test") == "(Latin America)"

    # Spacing
    template = next(mwparserfromhell.parse("{{lb|es|Argentina| & |Uruguay|Rio de la Plata|lunfardo}}").ifilter_templates())
    assert expand_template(template, "test") == "([[w:Argentina|Argentina]] and [[w:Uruguay|Uruguay]], Rio de la Plata, lunfardo)"


def test_indtr():

    text = "{{indtr|pt|de}}"
    template = mwparserfromhell.parse(text).filter_templates()[0]
    assert expand_template(template, "test") == "([[Appendix:Glossary#transitive|transitive]] with '''[[de]]''')"

    text = "{{indtr|pt|de|sobre}}"
    template = mwparserfromhell.parse(text).filter_templates()[0]
    assert expand_template(template, "test") == "([[Appendix:Glossary#transitive|transitive]] with '''[[de]]''' or '''[[sobre]]''')"

    tests = {
        "{{indtr|pt|de|sobre|qual2=informal}}":
            "([[Appendix:Glossary#transitive|transitive]] with '''[[de]]''' or '''[[sobre]]'''(informal))",
        "{{indtr|pt|de|sobre|direct=1}}":
            "([[Appendix:Glossary#transitive|transitive]] with '''[[de]]''' or '''[[sobre]]''' or with no preposition)",
        "{{indtr|pt|de|sobre|direct=1|qualdirect=rare}}":
            "([[Appendix:Glossary#transitive|transitive]] with '''[[de]]''' or '''[[sobre]]''' or with no preposition (rare))",
        "{{indtr|pt|de|sobre|intr=1}}":
            "([[Appendix:Glossary#intransitive|intransitive]], or [[Appendix:Glossary#transitive|transitive]] with '''[[de]]''' or '''[[sobre]]''')",
        "{{indtr|pt|de|sobre|.informal|.geography}}":
            "(informal, [[geography]], [[Appendix:Glossary#transitive|transitive]] with '''[[de]]''' or '''[[sobre]]''')",
        "{{indtr|pt|para|ditr=1}}":
            "([[Appendix:Glossary#ditransitive|ditransitive]] with the indirect object taking '''[[para]]''')",
        "{{indtr|pt|com|aux=gerund}}":
            "([[Appendix:Glossary#auxiliary|auxiliary]] with '''[[com]]''' and a verb in the gerund)",
        "{{indtr|fr|à|;|de|qual1=+ person being informed|qual2=usually|qual3=+ information}}":
            "([[Appendix:Glossary#transitive|transitive]] with '''[[à]]'''(+ person being informed) and usually with '''[[de]]'''(+ information))"
    }

    for k,v in tests.items():
        template = mwparserfromhell.parse(k).filter_templates()[0]
        assert expand_template(template, "test") == v

def test_cognate():
    assert _expand("{{cog|qfa-sub-ibe}}") == "a pre-Roman substrate of Iberia"
    assert _expand("{{cog|it|guida}}") == 'Italian "guida"'

def test_derived():

    text = "From {{der|es|la|grātīs}}."
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == 'From Latin "grātīs".'

    text = "From {{der|es|LL.|abōminābilis}}."
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == 'From Late Latin "abōminābilis".'

    text = "From {{der|es|la|argentum||silver}}"
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == 'From Latin "argentum" (“silver”)'

    assert _expand("{{der|es|la|-esco|-ēscere}}") == 'Latin "-ēscere"'

    assert enwiktionary_templates.Template._get_lang("gem") == "Germanic"
    assert _expand("{{der|es|gem}}") == "Germanic"


def test_inherited():
    text = "From {{inh|es|la|tenēre||to hold, to have}}"
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == 'From Latin "tenēre" (“to hold, to have”)'

    assert _expand("{{inh+|es|la|vāgīna|t=sheath}}") == 'Inherited from Latin "vāgīna" (“sheath”)'


def test_u_es_false_friend():
    assert _expand("{{U:es:false friend}}") == "Test is a false friend and does not mean the same as the English word for test."
    assert _expand("{{U:es:false friend|foo}}") == "Test is a false friend and does not mean the same as the English word for test.\nThe Spanish word for test is ''foo''."
    assert _expand("{{U:es:false friend|foo|en=bar}}") == "Test is a false friend and does not mean bar.\nThe Spanish word for bar is ''foo''."
    assert _expand("{{U:es:false friend|foo|en=bar|gloss=glossy}}") == "Test is a false friend and does not mean bar in the sense of ''glossy''.\nThe Spanish word for bar in that sense is ''foo''."

    assert _expand("{{U:es:false friend|foo|es2=foo2|en=bar}}") == "Test is a false friend and does not mean bar.\nThe Spanish word for bar is ''foo'' or ''foo2''."
    assert _expand("{{U:es:false friend|foo|es2=foo2|gl2=glossy2|en=bar}}") == "Test is a false friend and does not mean bar.\nThe Spanish word for bar is ''foo'' or ''foo2''."

def test_univerbation():
    assert _expand("{{univerbation|es|one|two}}") == "Univerbation of one + two"
    assert _expand("{{univerbation|es|one|two|three}}") == "Univerbation of one + two + three"

def test_deverbal():
    assert _expand("{{deverbal|es|escombrar}}") == 'Deverbal of "escombrar"'
    assert _expand("{{deverbal|es|escombrar||to clear out}}") == 'Deverbal of "escombrar" (“to clear out”)'
    assert _expand("{{deverbal|es|limpiar|t=to clean}}") == 'Deverbal of "limpiar" (“to clean”)'

def test_calique():
    assert _expand("{{calque|es|nci|necuātl}}") == 'Calque of Classical Nahuatl "necuātl"'

def test_bor():
    assert _expand("From the {{bor|es|ar|-}} suffix {{m|ar|ـِيّ}}.") == "From the Arabic suffix ''ـِيّ''."

def test_pagename_expansion():
    assert _expand("{{es-note-noun-mf}}") == "The noun test is like most Spanish nouns with a human referent.  The masculine forms are used when the referent is known to be male, a group of males, a group of mixed or unknown gender, or an individual of unknown or unspecified gender.  The feminine forms are used if the referent is known to be female or a group of females."

def test_named_after():
    assert _expand("{{named-after|en|nationality=French|occupation=navigator|Louis Antoine de Bougainville|wplink=Louis_Antoine_de_Bougainville|nocat=1}}.") == "Named after French navigator Louis Antoine de Bougainville."
    assert _expand("Possibly {{named-after|en|nocap=1|nationality=Greco-Egyptian|occupation=pharaoh|Κλαύδιος Πτολεμαῖος|wplink=Ptolemy|tr=Klaudios Ptolemaios|sc=polytonic|nocat=1}}.") == "Possibly named after Greco-Egyptian pharaoh Κλαύδιος Πτολεμαῖος (Klaudios Ptolemaios)."

def test_coinage():
    assert _expand("{{coinage|en|Josiah Willard Gibbs}}") == "Coined by Josiah Willard Gibbs"
    assert _expand("{{coinage|en|Josiah Willard Gibbs|in=1881|nat=American|occ=scientist}}") == "Coined by American scientist Josiah Willard Gibbs in 1881"

def test_and_lit():
    assert _expand("{{&lit|es|to [[serve]] (on an [[dish]], [[plate]])}}") == "Used other than figuratively or idiomatically: to [[serve]] (on an [[dish]], [[plate]])."

def test_fem():
    assert _expand("{{female equivalent of|es|sirviente|t=[[maid]], [[servant]]}}") == 'female equivalent of "sirviente" (“[[maid]], [[servant]]”)'

def test_place():
    assert _expand("{{place|en|country|cont/Europe}}.") == "A country in Europe."
    assert _expand("{{place|en|city|p/Ontario|c/Canada}}.") == "A city in Ontario, Canada."
    assert _expand("{{place|en|city|c/Netherlands}}.") == "A city in the Netherlands."
    assert _expand("{{place|en|city|s/Pennsylvania|c/United States}}.") == "A city in Pennsylvania, United States."
    assert _expand("{{place|fr|country|cont/Europe|t1=Germany}}") == "Germany (a country in Europe)"
    assert _expand("{{place|en|county|s/Virginia|c/United States}}.") == "A county of Virginia, United States."
    assert _expand("{{place|en|country|in central|cont/Europe}}.") == "A country in central Europe."
    assert _expand("{{place|en|A <<neighborhood>> midway up the <<inlet/Golden Horn>> within <<dist/Fatih>> in <<city/Istanbul>>, <<c/Turkey>>.}}") == "A neighborhood midway up the Golden Horn within Fatih district in Istanbul, Turkey."
    assert _expand("{{place|en|A <<former>> French <<colony>> on the <<isl:pref/Hispaniola>> from 1659 to 1809, roughly equivalent to modern-day <<c/Haiti>>}}.") == "A former French colony on the island of Hispaniola from 1659 to 1809, roughly equivalent to modern-day Haiti."


    assert _expand("{{place|es|The name of a number of <<cities>> and <<town>>s in <<c/Spain>>.}}") == "The name of a number of cities and towns in Spain."
    assert _expand("{{place|es|<<ancient>> [[Greek]] <<city>> on the <<riv:Suf/Orontes>>, in modern <<c/Turkey>>|t1=Antioch|t2=Antioch on the Orontes}}") == "Antioch, Antioch on the Orontes (ancient [[Greek]] city on the Orontes River, in modern Turkey)"
    assert _expand("{{place|es|country|cont/Europe|and|cont/Asia|t=Armenia}}") == "Armenia (a country in Europe and Asia)"
    assert _expand("{{place|es|town|province/Ciego de Ávila|c/Cuba}}") == "A town in Ciego de Ávila, Cuba"
    assert _expand("{{place|es|autonomous territory|c/Netherlands|in the|sea/Caribbean|t1=Aruba}}") == "Aruba (an autonomous territory of the Netherlands, in the Caribbean)"
    #assert _expand("{{place|es|autonomous territory|c/Netherlands|in the|sea/Caribbean|t1=Aruba}}") == "Aruba (an autonomous territory of the Netherlands in the Caribbean)"
    assert _expand("{{place|es|archipelago/and/country|r/Caribbean|t=Bahamas}}") == "Bahamas (an archipelago and country in the Caribbean)"

    assert _expand("{{place|es|island|ocean/Atlantic Ocean|;, and|overseas territory|c/United Kingdom|t=Saint Helena}}") == "Saint Helena (an island in the Atlantic Ocean, and overseas territory of the United Kingdom)"
    assert _expand("{{place|es|mountain range|acomm/Catalonia|c/Spain|near [[Barcelona]], the site of a [[monastery]]|t=Montserrat}}") == "Montserrat (a mountain range in Catalonia, Spain, near [[Barcelona]], the site of a [[monastery]])"
#    assert _expand("{{place|es|mountain|es:state/Puebla}}") == "A mountain in Puebla"

    assert _expand("{{place|es|department|c/El Salvador}}") == "A department of El Salvador"
#    assert _expand("{{place|es|province|r/Ancash|c/Peru}}") == "A province of Ancash, Peru"
    assert _expand("{{place|es|state|c/USA|t=Alaska}}") == "Alaska (a state of the United States)"
    assert _expand("{{place|es|province|autonomous community/en:Castile-La Mancha|country/Spain|capital/en:Albacete|t1=Albacete}}") == "Albacete (a province of Castile-La Mancha, Spain, Albacete)"
    assert _expand("{{place|es|capital|s/New York|t1=Albany}}") == "Albany (the capital of New York)"
    assert _expand("{{place|es|ancient region|c/Georgia|t1=Iberia}}") == "Iberia (an ancient region in Georgia)"
    assert _expand("{{place|es|river|c/Peru}}") == "A river in Peru"
    #assert _expand("") == ""

    from enwiktionary_templates.place import res_ends_with

    assert res_ends_with(["abc", "def"], "cdef") == True
    assert res_ends_with(["abc", "def"], "Xabcdef") == False
    assert res_ends_with(["ab", "cd", "ef"], "bcdef") == True
    assert res_ends_with(["abc", "def"], "Xdef") == False

    # Isla Príncipe Eduardo
    # an island in the subantarctic Indian Ocean, part of the [https://en.wikipedia.org/wiki/Prince_Edward_Islands Prince Edward Islands]


def test_inflections():
    # {{adj form of|es|rojo||m|p}}
    # {{inflection of|es|rojo||p}}
    #
    assert _expand("{{inflection of|es|brillar||1|s|impf|ind}}") == 'inflection of "brillar"'

    assert _expand("{{adj form of|es|rojo||m|p}}") == 'masculine plural of "rojo"'
    assert _expand("{{noun form of|es|rojo||m|p}}") == 'masculine plural of "rojo"'


    assert _expand("{{form of|es||-torio}}") == 'form of "-torio"'
    assert _expand("{{form of|es|plural|-torio}}") == 'plural of "-torio"'

    assert _expand("{{inflection of|es|éste|gloss=this||n|s}}") == 'neuter singular of "éste"'


def test_forms():
    from enwiktionary_parser.utils import nest_aware_iterator

    assert _expand("{{forms|a|b}}") == 'form=a; form=b'


def test_etydate():

    assert _expand("{{etydate|1900}}") == 'First attested in 1900'
    assert _expand("{{etydate|1900|1910}}") == 'First attested in 1900, but in common usage only as of 1910'
    assert _expand("{{etydate|1900|first half of the 19th century}}") == 'First attested in 1900, but in common usage only as of first half of the 19th century'
    assert _expand("{{etydate|r|1900|1910}}") == 'First attested in 1900-1910'

    assert _expand("{{etydate|c|1900}}") == 'First attested in c. 1900'
    assert _expand("{{etydate|c|1900|1990}}") == 'First attested in c. 1900, but in common usage only as of 1990'
    assert _expand("{{etydate|c|r|1900|1910|1990}}") == 'First attested in c. 1900-1910, but in common usage only as of 1990'


def test_transclude_sense():
    lines = """\
acidaemia:medicine::{{lb|en|medicine}} a medical condition marked by an abnormally high concentration of [[hydrogen]] ions in a person's [[blood]]
acidimeter:Q110083401::{{lb|en|chemistry}} An [[instrument]] for ascertaining the strength of acids.
acidimetric:relational::{{lb|en|chemistry}} Describing a [[titration]] in which the [[titrant]] is an [[acid]].
acidimetrically:chemistry::{{lb|en|chemistry}} By means of, or in terms of, [[acidimetry]].\
""".splitlines()

    transclude_senses = {}
    for l in lines:
        word, senseid, _, sense = l.split(":", 3)
        transclude_senses[(word,senseid)] = sense.strip()

    wikt = mwparserfromhell.parse("{{transclude sense|es|acidimeter|id=Q110083401}}")
    expand_templates(wikt, "test", transclude_senses)
    print(str(wikt))

    assert str(wikt) == "([[chemistry]]) acidimeter (An [[instrument]] for ascertaining the strength of acids.)"
