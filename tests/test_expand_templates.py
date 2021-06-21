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

import pytest
import enwiktionary_templates
import mwparserfromhell

expand_template = enwiktionary_templates.expand_template
expand_templates = enwiktionary_templates.expand_templates

def _expand(text, pagename):
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, pagename)
    return str(wikt)

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
    assert expand_template(template, "test") == "ellipsis of ''Antigua Guatemala''"

    template = next(mwparserfromhell.parse("# {{es-compound of|adelgaz|ar|adelgazar|las|mood=inf}}").ifilter_templates())
    assert expand_template(template, "test") == 'compound form of "adelgazar"+"las"'

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

    template = next(mwparserfromhell.parse("{{suffix|en|do|ing}}").ifilter_templates())
    assert expand_template(template, "test") == "do + -ing"

def test_af():
    template = next(mwparserfromhell.parse("{{af|en|volley|ball}}").ifilter_templates())
    assert expand_template(template, "test") == "volley + ball"

    template = next(mwparserfromhell.parse("{{affix|en|pest|-i-|-cide}}").ifilter_templates())
    assert expand_template(template, "test") == "pest + -i- + -cide"

def test_doublet():
    template = next(mwparserfromhell.parse("{{doublet|en|test}}").ifilter_templates())
    assert expand_template(template, "test") == "Doublet of test"

    template = next(mwparserfromhell.parse("{{doublet|en|test|notext=1}}").ifilter_templates())
    assert expand_template(template, "test") == "test"

    template = next(mwparserfromhell.parse("{{doublet|en|test|nocap=1}}").ifilter_templates())
    assert expand_template(template, "test") == "doublet of test"

    template = next(mwparserfromhell.parse("{{doublet|en|test|test2}}").ifilter_templates())
    assert expand_template(template, "test") == "Doublet of test, test2"

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


def test_derived():

    text = "From {{der|es|la|grātīs}}."
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == "From Latin ''grātīs''."

    text = "From {{der|es|LL.|abōminābilis}}."
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == "From Late Latin ''abōminābilis''."

    text = "From {{der|es|la|argentum||silver}}"
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == "From Latin ''argentum'' (“silver”)"


def test_inherited():
    text = "From {{inh|es|la|tenēre||to hold, to have}}"
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, "title")
    assert str(wikt) == "From Latin ''tenēre'' (“to hold, to have”)"


def test_u_es_false_friend():
    assert _expand("{{U:es:false friend}}", "test") == "Test is a false friend and does not mean the same as the English word for test."
    assert _expand("{{U:es:false friend|foo}}", "test") == "Test is a false friend and does not mean the same as the English word for test. \nThe Spanish word for test is ''foo''."
    assert _expand("{{U:es:false friend|foo|en=bar}}", "test") == "Test is a false friend and does not mean bar. \nThe Spanish word for bar is ''foo''."
    assert _expand("{{U:es:false friend|foo|en=bar|gloss=glossy}}", "test") == "Test is a false friend and does not mean bar in the sense of ''glossy''. \nThe Spanish word for bar in that sense is ''foo''."

def test_univerbation():
    assert _expand("{{univerbation|es|one|two}}", "test") == "Univerbation of one + two"
    assert _expand("{{univerbation|es|one|two|three}}", "test") == "Univerbation of one + two + three"

def test_deverbal():
    assert _expand("{{deverbal|es|escombrar}}", "test") == "Deverbal of ''escombrar''"
    assert _expand("{{deverbal|es|escombrar||to clear out}}", "test") == "Deverbal of ''escombrar'' (“to clear out”)"
    assert _expand("{{deverbal|es|limpiar|t=to clean}}", "test") == "Deverbal of ''limpiar'' (“to clean”)"

def test_calique():
    assert _expand("{{calque|es|nci|necuātl}}", "aguamiel") == "Calque of Classical Nahuatl ''necuātl''"

def test_bor():
    assert _expand("From the {{bor|es|ar|-}} suffix {{m|ar|ـِيّ}}.", "xxx") == "From the Arabic suffix ''ـِيّ''."


