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

Based on https://en.wiktionary.org/wiki/Module:inflection_utilities
Revision 69941302, 03:14, 27 November 2022
"""

import re
import enwiktionary_templates.module.parse_utilities as put

#export = {}

#m_links = require("Module:links")
#m_string_utilities = require("Module:string utilities")
#m_table = require("Module:table")

#rsplit = mw.text.split
#rfind = mw.ustring.find
#rmatch = mw.ustring.match
#rsubn = mw.ustring.gsub

def rfind(string, pattern):
    return re.search(pattern, string)

def rmatch(string, pattern):
    return re.match(pattern, string)

def rsplit(string, pattern):
    return re.split(pattern, string)

# version of rsubn() that discards all but the first return value
def rsub(string, pattern, replacement):
    return re.sub(pattern, replacement, string)

def ipairs(item):
    if not item:
        return []
    return enumerate(item)

def pairs(table):
    return values(table)

def ternery(cond, v1, v2):
    if cond:
        return v1
    return v2

def lua_or(v1, v2):
    for v in [v1, v2]:
        if v:
            return v

class table():
    @staticmethod
    def insert(target, value):
        target.append(value)

def m_string_utilities_capturing_split(string, pattern):
    return re.split(pattern, string)

def m_links_remove_links(string):
    return string

footnote_abbrevs = {
    "a": "archaic",
    "c": "colloquial",
    "d": "dialectal",
    "fp": "folk-poetic",
    "l": "literary",
    "lc": "low colloquial",
    "p": "poetic",
    "pej": "pejorative",
    "r": "rare",
}


def remove_redundant_links(text):
    # remove redundant link surrounding entire form
    return rsub(text, r"^\[\[([^\[\]|]*)\]\]$", r"\1")

def error(err):
    raise ValueError(err)


#------------------------------------------------------------------------------------------------------------
#--                                             PARSING CODE                                               --
#------------------------------------------------------------------------------------------------------------

parse_balanced_segment_run = put.parse_balanced_segment_run
parse_multi_delimiter_balanced_segment_run = put.parse_multi_delimiter_balanced_segment_run
split_alternating_runs = put.split_alternating_runs

# Like split_alternating_runs() but strips spaces from both ends of the odd-numbered elements (only in
# odd-numbered runs if preserve_splitchar is given). Effectively we leave alone the footnotes and splitchars
# themselves, but otherwise strip extraneous spaces. Spaces in the middle of an element are also left alone.
def split_alternating_runs_and_strip_spaces(segment_runs, splitchar, preserve_splitchar):
    return put.split_alternating_runs_and_frob_raw_text(segment_runs, splitchar, put.strip_spaces, preserve_splitchar)

#------------------------------------------------------------------------------------------------------------
#--                                             INFLECTION CODE                                            --
#------------------------------------------------------------------------------------------------------------

"""
The following code is used in building up the inflection of terms in inflected languages, where a term can potentially
consist of several inflected words, each surrounded by fixed text, and a given slot (e.g. accusative singular) of a
given word can potentially consist of multiple possible inflected forms. In addition, each form may be associated with
a manual translation and/or a list of footnotes (or qualifiers, in the case of headword lines). The following
terminology is helpful to understand:

* An `inflection dimension` is a particular dimension over which a term may be inflected, such as case, number, gender,
  person, tense, mood, voice, aspect, etc.
* A `term` is a word or multiword expression that can be inflected. A multiword term may in turn consist of several
  single-word inflected terms with surrounding fixed text. A term belongs to a particular `part of speech` (e.g. noun,
  verb, adjective, etc.).
* A `slot` is a particular combination of inflection dimensions. An example might be "accusative plural" for a noun,
  or "first-person singular present indicative" for a verb. Slots are named in a language-specific fashion. For
  example, the slot "accusative plural" might have a name "accpl", while "first-person singular present indicative"
  might be variously named "pres1s", "pres_ind_1_sg", etc. Each slot is filled with zero or more `forms`.
* A `form` is a particular inflection of a slot for a particular term. Forms are described using `form objects`, which
  are Lua objects taking the form {form="FORM", translit="MANUAL_TRANSLIT", footnotes={"FOOTNOTE", "FOOTNOTE", ...}}.
  FORM is a `form string` specifying the value of the form itself. MANUAL_TRANSLIT specifies optional manual
  transliteration for the form, in case (a) the form string is in a different script; and (b) either the form's
  automatic transliteration is incorrect and needs to be overridden, or the language of the term has no automatic
  transliteration (e.g. in the case of Persian and Hebrew). FOOTNOTE is a footnote to be attached to the form in
  question, and should be e.g. "[archaic]" or "[only in the meaning 'to succeed (an officeholder)']", i.e. the string
  must be surrounded by brackets and should begin with a lowercase letter and not end in a period/full stop. When such
  footnotes are converted to actual footnotes in a table of inflected forms, the brackets will be removed, the first
  letter will be capitalized and a period/full stop will be added to the end. (However, when such footnotes are used
  as qualifiers in headword lines, only the brackets will be removed, with no capitalization or final period.) Note
  that only FORM is mandatory. 
* The `lemma` is the particular form of a term under which the term is entered into a dictionary. For example, for
  verbs, it is most commonly the infinitive, but this differs for some languages: e.g. Latin, Greek and Bulgarian use
  the first-person singular present indicative (active voice in the case of Latin and Greek); Sanskrit and Macedonian
  use the third-person singular present indicative (active voice in the case of Sanskrit); Hebrew and Arabic use the
  third-person singular masculine past (aka "perfect"); etc. For nouns, the lemma form is most commonly the nominative
  singular, but e.g. for Old French it is the objective singular and for Sanskrit it is the root.
"""

def extract_footnote_modifiers(footnote):
    footnote_mods, footnote_without_mods = rmatch(footnote, r"^\[([!*+]?)(.*)\]$")
    if not footnote_mods:
        raise ValueError(f"Saw footnote '{footnote }' not surrounded by brackets")
    return footnote_mods, footnote_without_mods


# Insert a form (an object of the form {form=FORM, translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES}) into a list of such
# forms. If the form is already present, the footnotes of the existing and new form might be combined (specifically,
# footnotes in the new form beginning with ! will be combined).
def insert_form_into_list(_list, form):
    # Don't do anything if the form object or the form inside it is None. This simplifies
    # form insertion in the presence of inflection generating def s that may return None,:
    # such as generate_noun_vocative() and generate_noun_count_form().
    if not form or not form.get("form"):
        return

    for listform in _list:
        if listform["form"] == form["form"] and listform.get("translit") == form.get("translit"):
            # Form already present; maybe combine footnotes.
            if form.get("footnotes"):
                # Unimplemented
                pass
            return

    # Form not found.
    _list.append(form)


# Insert a form (an object of the form {form=FORM, translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES})
# into the given slot in the given form table.
def insert_form(formtable, slot, form):
    # Don't do anything if the form object or the form inside it is None. This simplifies
    # form insertion in the presence of inflection generating def s that may return None,:
    # such as generate_noun_vocative() and generate_noun_count_form().
    if not form or not form.get("form"):
        return

    if not formtable.get(slot):
        formtable[slot] = []

    insert_form_into_list(formtable[slot], form)



# Insert a list of forms (each of which is an object of the form
# {form=FORM, translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES}) into the given slot in the given
# form table. FORMS can be None.
def insert_forms(formtable, slot, forms):
    if not forms:
        return

    for form in forms:
        insert_form(formtable, slot, form)

def identity(form, translit):
    return form, translit

def call_map_function_str(s, fun):
    if s == "?":
        return "?"

    newform, newtranslit = fun(s)
    if newtranslit:
        return {"form": newform, "translit": newtranslit}
    else:
        return newform

def call_map_function_obj(form, fun):
    if form.get("form") == "?":
        return {"form": "?", "footnotes": form["footnotes"]}
    newform, newtranslit = fun(form["form"], form.get("translit"))
    return {"form":newform, "translit":newtranslit, "footnotes": form.get("footnotes")}


# Map a function over the form values in FORMS (a list of objects of the form
# {form=FORM, translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES}). The function is called with two arguments, the original
# form and manual translit; if manual translit isn't relevant, it's fine to declare the function with only one
# argument. The return value is either a single value (the new form) or two values (the new form and new manual
# translit). Use insert_form_into_list() to insert them into the returned list in case two different forms map to the
# same thing.

def map_forms(forms, fun):
    if not forms:
        return None

    retval = []
    for form in forms:
        insert_form_into_list(retval, call_map_function_obj(form, fun))

    return retval


# Map a list-returning function over the form values in FORMS (a list of form objects of the form {form=FORM,
# translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES}). If the input form is "?", it is preserved on output and the
# function is not called. The function is called with two arguments, the original form and manual translit; if manual
# translit isn't relevant, it's fine to declare the function with only one argument. The return value is either a list
# of forms or a list of form objects of the form {form=FORM, translit=MANUAL_TRANSLIT}. The footnotes (if any) from
# the input form objects are preserved on output. Uses insert_form_into_list() to insert the resulting form objects
# into the returned list in case two different forms map to the same thing.

def flatmap_forms(forms, fun):
    if not forms:
        return None

    retval = []
    for form in forms:
        funret = ["?"] if fun["form"] == "?" else fun(form["form"], form.get("translit"))
        for fr in funret:
            newform = None
            if type(fr) is dict:
                newform = {"form": fr.get("form"), "translit": fr.get("translit"), "footnotes": form.get("footnotes", [])}
            else:
                newform = {"form": fr, "footnotes": form.get("footnotes", [])}

            insert_form_into_list(retval, newform)

    return retval


# Map a function over the form values in FORMS (a single string, a form object of the form {form=FORM,
# translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES}, or a list of either of the previous two types). If the input form is
# "?", it is preserved on output and the function is not called. If FIRST_ONLY is given and FORMS is a list, only map
# over the first element. Return value is of the same form as FORMS, unless FORMS is a string and the function return
# both form and manual translit (in which case the return value is a form object). The function is called with two
# arguments, the original form and manual translit; if manual translit isn't relevant, it's fine to declare the
# function with only one argument. The return value is either a single value (the new form) or two values (the new
# form and new manual translit). The footnotes (if any) from the input form objects are preserved on output.
#
# FIXME: This function is used only in [[Module:bg-verb]] and should be moved into that module.

def map_form_or_forms(forms, fn, first_only):
    raise ValueError("not updated, to  02:41, 29 June 2022 revision or beyond")
    if forms == None:
        return None
    elif isinstance(forms, str):
        return forms == "?" and "?" or fn(forms)
    elif forms.get("form"):
        if forms["form"] == "?":
            return {"form": "?", "footnotes": forms.get("footnotes", [])}

        newform, newtranslit = fn(forms["form"], forms["translit"])
        return {"form": newform, "translit": newtranslit, "footnotes": forms.get("footnotes", [])}
    else:
        retval = []
        for form in forms:
            if first_only:
                return map_form_or_forms(form, fn)

            retval.append(map_form_or_forms(form, fn))

        return retval


# Combine two sets of footnotes. If either is None, just return the other, and if both are None,
# return None.
def combine_footnotes(notes1, notes2):
    if not notes1 and not notes2:
        return None

    if not notes1:
        return notes2

    if not notes2:
        return notes1

    combined = { **notes1, **notes2 }

    return combined


# Expand a given footnote (as specified by the user, including the surrounding brackets) into the form to be inserted
# into the final generated table. If `no_parse_refs` is not given and the footnote is a reference (of the form
# '[ref:...]'), parse and return the specified reference(s). Two values are returned, `footnote_string` (the expanded
# footnote, or nil if the second value is present) and `references` (a list of objects of the form
# {text = TEXT, name = NAME, group = GROUP} if the footnote is a reference and `no_parse_refs` is not given, otherwise
# nil). Unless `return_raw` is given, the returned footnote string is capitalized and has a final period added.

def expand_footnote_or_references(note, return_raw, no_parse_refs):
    notetext = rmatch(note, r"^\[!?(.*)\]$")
    if not notetext:
        error("Internal error: Footnote should be surrounded by brackets: " + note)

    # Unimplemented

    return notetext.capitalize() + "."

# Older entry point. Equivalent to expand_footnote_or_references(note, true).
# FIXME: Convert all uses to use expand_footnote_or_references() instead.
def expand_footnote(note):
    return expand_footnote_or_references(note, False, "no parse refs")


def fetch_headword_qualifiers_and_references(footnotes):
    # Unimplemented
    return None

# Combine a form (either a string or a table {form = FORM, footnotes = FOOTNOTES, ...}) with footnotes.
# Do the minimal amount of work; e.g. if FOOTNOTES is None, just return FORM.
def combine_form_and_footnotes(form, footnotes):
    if isinstance(footnotes, str):
        footnotes = [footnotes]

    if footnotes:
        if type(form) is dict:
            #form = m_table.shallowcopy(form)
            form["footnotes"] = combine_footnotes(form.get("footnotes"), footnotes)
            return form
        else:
            return {"form": form, "footnotes": footnotes}

    else:
        return form

# Combine a single form (either a string or object {form = FORM, footnotes = FOOTNOTES, ...}) or a list of same
# along with footnotes and return a list of forms where each returned form is an object
# {form = FORM, footnotes = FOOTNOTES, ...}.
def convert_to_general_list_form(word_or_words, footnotes=[]):

    if isinstance(footnotes, str):
        footnotes = [footnotes]
    if isinstance(word_or_words, str):
        return [{"form": word_or_words, "footnotes": footnotes}]
    elif isinstance(word_or_words, dict) and "form" in word_or_words:
        return [combine_form_and_footnotes(word_or_words, footnotes)]
    elif not footnotes:
        must_convert = False

        for form in word_or_words:
            if isinstance(form, str):
                must_convert = True

        if not must_convert:
            return word_or_words

        retval = []
        for form in word_or_words:
            if isinstance(form, str):
                retval.append({"form": form, "footnotes": footnotes})
            else:
                retval.append(combine_form_and_footnotes(form, footnotes))

        return retval


def is_table_of_strings(forms):
    for form in forms:
        if not isinstance(form, int) or not isinstance(form, str):
            return False

    return True


# Combine `stems` and `endings` and store into slot `slot` of form table `forms`. Either of `stems` and `endings` can
# be nil, a single string, a list of strings, a form object or a list of form objects. The combination of a given stem
# and ending happens using `combine_stem_ending`, which takes two parameters (stem and ending, each a string) and
# returns one value (a string). If manual transliteration is present in either `stems` or `endings`, `lang` (a
# language object) along with `combine_stem_ending_tr` (a function like `combine_stem_ending` for combining manual
# transliteration) must be given. `footnotes`, if specified, is a list of additional footnotes to attach to the
# resulting inflections (stem+ending combinations). The resulting inflections are inserted into the form table using
# export.insert_form(), in case of duplication.

def add_forms(forms, slot, stems, endings, combine_stem_ending, \
        lang=None, combine_stem_ending_tr=False, footnotes=[]):
    if stems == None or endings == None:
        return

    def combine(stem, ending):
        if stem == "?" or ending == "?":
            return "?"
        return combine_stem_ending(stem, ending)

    if isinstance(stems, str) and isinstance(endings, str):
        insert_form(forms, slot, {"form": combine(stems, endings), "footnotes": footnotes})
    elif isinstance(stems, str) and is_table_of_strings(endings):
        for ending in endings:
            insert_form(forms, slot, {"form": combine(stems, ending), "footnotes": footnotes})

    else:
        stems = convert_to_general_list_form(stems)
        endings = convert_to_general_list_form(endings, footnotes)
        for _, stem in ipairs(stems):
            for _, ending in ipairs(endings):
                footnotes = None
                if stem.get("footnotes") and ending.get("footnotes"):
                    #footnotes = m_table.shallowcopy(stem.footnotes)
                    footnotes = stem["footnotes"]
                    for _, footnote in ipairs(ending["footnotes"]):
                        if footnote not in footnotes:
                            footnotes.append(footnote)

                elif stem.get("footnotes"):
                    footnotes = stem["footnotes"]
                elif ending.get("footnotes"):
                    footnotes = ending["footnotes"]

                new_form = combine(stem.get("form"), ending.get("form"))
                new_translit = None
                if new_form != "?" and (stem.get("translit") or ending.get("translit")):
                    if not lang or not combine_stem_ending_tr:
                        error("Internal error: With manual translit, 'lang' and 'combine_stem_ending_tr' must be passed to 'add_forms'")

                    stem_tr = stem.translit if stem.get("translit") else lang.transliterate(m_links_remove_links(stem.form))
                    ending_tr = ending.translit if ending.get("translit") else lang.transliterate(m_links_remove_links(ending.form))
                    new_translit = combine_stem_ending_tr(stem_tr, ending_tr)

                insert_form(forms, slot, {"form": new_form, "translit": new_translit, "footnotes": footnotes})


def add_multiple_forms(forms, slot, sets_of_forms, combine_stem_ending, \
        lang, combine_stem_ending_tr, footnotes):
    if len(sets_of_forms) == 0:
        return
    elif len(sets_of_forms) == 1:
        formset = convert_to_general_list_form(sets_of_forms[0], footnotes)
        insert_forms(forms, slot, formset)
    elif len(sets_of_forms) == 2:
        stems = sets_of_forms[0]
        endings = sets_of_forms[1]
        add_forms(forms, slot, stems, endings, combine_stem_ending,
            lang, combine_stem_ending_tr, footnotes)
    else:
        prev = sets_of_forms[0]
        for i in range(1,len(sets_of_forms)):
            tempdest = []
            add_forms(tempdest, slot, prev, sets_of_forms[i], combine_stem_ending,
                lang, combine_stem_ending_tr, i == len(sets_of_forms) and footnotes or None)
            prev = tempdest[slot]

        insert_forms(forms, slot, prev)


def iterate_slot_list_or_table(props, do_slot):
    if props.get("slot_list"):
#        for _, slot_and_accel_form in ipairs(props["slot_list"]):
#            slot, accel_form = slot_and_accel_form
       for slot, accel_form in props["slot_list"].items():
            do_slot(slot, accel_form)

    else:
        for slot, accel_form in props.get("slot_table",{}).items():
            do_slot(slot, accel_form)


def parse_before_or_post_text(props, text, segments, lemma_is_last):

    # Call parse_balanced_segment_run() to keep multiword links together.
    bracketed_runs = put.parse_balanced_segment_run(text, "[", "]")
    # Split normally on space or hyphen (but customizable). Use preserve_splitchar so we know whether the separator was
    # a space or hyphen.

    space_separated_groups = []
    if props.get("split_bracketed_runs_into_words"):
        space_separated_groups = props["split_bracketed_runs_into_words"](bracketed_runs)

    if not space_separated_groups:
        # If the text begins with a hyphen, include the hyphen in the set of allowed characters
        # for an inflected segment. This way, e.g. conjugating "-ir" is treated as a regular
        # -ir verb rather than a hyphen + irregular [[ir]].
        is_suffix = rfind(text, "^\-")
        split_pattern = is_suffix and " " or "[ \-]"
        space_separated_groups = put.split_alternating_runs(bracketed_runs, split_pattern, "preserve splitchar")

    parsed_components = []
    parsed_components_translit = []
    saw_manual_translit = False
    lemma = None
    for j, space_separated_group in ipairs(space_separated_groups):
        component = "".join(space_separated_group)
        if lemma_is_last and j == len(space_separated_groups)-1:
            lemma = component
            if lemma == "" and not props.get("allow_blank_lemma"):
                error("Word is blank: '" + "".join(segments) + "'")

        elif rfind(component, "//"):
            # Manual translit or respelling specified.
            if not props.get("lang"):
                error("Manual translit not allowed for this language; if this is incorrect, 'props.lang' must be set internally")

            saw_manual_translit = True
            split = rsplit(component, "//")
            if len(split) != 2:
                error("Term with translit or respelling should have only one // in it: " + component)

            translit = None
            component, translit = split
            if props.get("transliterate_respelling"):
                translit = props["transliterate_respelling"](translit)

            parsed_components.append(component)
            parsed_components_translit.append(translit)
        else:
            parsed_components.append(component)
            parsed_components_translit.append(False) # signal that it may need later transliteration

    if saw_manual_translit:
        for j, parsed_component in ipairs(parsed_components):
            if not parsed_components_translit[j]:
                parsed_components_translit[j] = props["lang"].transliterate(m_links_remove_links(parsed_component))

    text = "".join(parsed_components)
    translit = None
    if saw_manual_translit:
        translit = "".join(parsed_components_translit)


    return text, translit, lemma



"""
Parse a segmented multiword spec such as "[[медичний|меди́чна]]<+> [[сестра́]]<*,*#.pr>" (in Ukrainian).
"Segmented" here means it is broken up on <...> segments using parse_balanced_segment_run(text, "<", ">"),
e.g. the above text would be passed in as {"[[медичний|меди́чна]]", "<+>", " [[сестра́]]", "<*,*#.pr>", ""}.

The return value is a table of the form
{
  word_specs = {WORD_SPEC, WORD_SPEC, ...},
  post_text = "TEXT-AT-END",
  post_text_no_links = "TEXT-AT-END-NO-LINKS",
  post_text_translit = "MANUAL-TRANSLIT-OF-TEXT-AT-END" or None (if no manual translit or respelling was specified in the post-text)
}

where WORD_SPEC describes an individual inflected word and "TEXT-AT-END" is any raw text that may occur
after all inflected words. Individual words or linked text (including multiword text) may be given manual
transliteration or respelling in languages that support this using TEXT//TRANSLIT or TEXT//RESPELLING.
Each WORD_SPEC is of the form returned by parse_indicator_spec():

{
  lemma = "LEMMA",
  before_text = "TEXT-BEFORE-WORD",
  before_text_no_links = "TEXT-BEFORE-WORD-NO-LINKS",
  before_text_translit = "MANUAL-TRANSLIT-OF-TEXT-BEFORE-WORD" or None (if no manual translit or respelling was specified in the before-text)
  # Fields as described in parse_indicator_spec()
  ...
}

For example, the return value for "[[медичний|меди́чна]]<+> [[сестра́]]<*,*#.pr>" is
{
  word_specs = {
    {
      lemma = "[[медичний|меди́чна]]",
      overrides = {},
      adj = True,
      before_text = "",
      before_text_no_links = "",
      forms = {},
    },
    {
      lemma = "[[сестра́]]",
      overrides = {},
      stresses = {
        {
          reducible = True,
          genpl_reversed = False,
        },
        {
          reducible = True,
          genpl_reversed = True,
        },
      },
      animacy = "pr",
      before_text = " ",
      before_text_no_links = " ",
      forms = {},
    },
  },
  post_text = "",
  post_text_no_links = "",
}
"""
def parse_multiword_spec(segments, props, disable_allow_default_indicator):
    multiword_spec = {
        "word_specs": []
    }
    if not disable_allow_default_indicator and props.get("allow_default_indicator") and len(segments) == 1:
        segments.append("<>")
        segments.append("")

    # Loop over every other segment. The even-numbered segments are angle-bracket specs while
    # the odd-numbered segments are the text between them.
    for i in range(1, len(segments), 2):
        before_text, before_text_translit, lemma = \
            parse_before_or_post_text(props, segments[i - 1], segments, "lemma is last")
        base = props["parse_indicator_spec"](segments[i], lemma)
        base["before_text"] = before_text
        base["before_text_no_links"] = m_links_remove_links(base["before_text"])
        base["before_text_translit"] = before_text_translit
        base["lemma"] = base.get("lemma", lemma)
        multiword_spec["word_specs"].append(base)

    multiword_spec["post_text"], multiword_spec["post_text_translit"], lemma = \
        parse_before_or_post_text(props, segments[len(segments)-1], segments, False)
    multiword_spec["post_text_no_links"] = m_links_remove_links(multiword_spec["post_text"])
    return multiword_spec



"""
Parse an alternant, e.g. "((родо́вий,родови́й))" or "((ру́син<pr>,руси́н<b.pr>))" (both in Ukrainian).
The return value is a table of the form
{
  alternants = {MULTIWORD_SPEC, MULTIWORD_SPEC, ...}
}

where MULTIWORD_SPEC describes a given alternant and is as returned by parse_multiword_spec().
"""
def parse_alternant(alternant, props):
    parsed_alternants = []
    alternant_text = rmatch(alternant, r"^\(\((.*)\)\)$")
    segments = put.parse_balanced_segment_run(alternant_text, "<", ">")
    comma_separated_groups = put.split_alternating_runs(segments, r"\s*,\s*")
    alternant_spec = {"alternants": []}
    for _, comma_separated_group in ipairs(comma_separated_groups):
        table.insert(alternant_spec["alternants"], parse_multiword_spec(comma_separated_group, props))

    return alternant_spec


"""
Top-level parsing function. Parse text describing one or more inflected words.
`text` is the inflected text to parse, which generally has <...> specs following words to
be inflected, and may have alternants indicated using double parens. Examples:

"[[медичний|меди́чна]]<+> [[сестра́]]<*,*#.pr>" (Ukrainian, for [[медична сестра]] "nurse (lit. medical sister)")
"((ру́син<pr>,руси́н<b.pr>))" (Ukrainian, for [[русин]] "Rusyn")
"पंचायती//पंचाय*ती राज<M>" (Hindi, for [[पंचायती राज]] "village council", with phonetic respelling in the before-text component)
"((<M>,<M.plstem:फ़तूह.dirpl:फ़तूह>))" (Hindi, for [[फ़तह]] "win, victory", on that page, where the lemma is omitted and taken from the pagename)
"" (for any number of Hindi adjectives, where the lemma is omitted and taken from the pagename, and the angle bracket spec <> is assumed)
"काला<+>धन<M>" (Hindi, for [[कालाधन]] "black money")

`props` is an object specifying properties used during parsing, as follows:
{
  parse_indicator_spec = FUNCTION_TO_PARSE_AN_INDICATOR_SPEC (required),
  lang = LANG_OBJECT,
  transliterate_respelling = FUNCTION_TO_TRANSLITERATE_RESPELLING,
  split_bracketed_runs_into_words = nil or FUNCTION_TO_SPLIT_BRACKETED_RUNS_INTO_WORDS,
  allow_default_indicator = BOOLEAN_OR_NIL,
  allow_blank_lemma = BOOLEAN_OR_NIL,
}
						
`parse_indicator_spec` is a required function that takes two arguments, a string surrounded by angle brackets and the
lemma, and should return a word_spec object containing properties describing the indicators inside of the angle
brackets).

`lang` is the language object for the language in question; only needed if manual translit or respelling may be present
using //.

`transliterate_respelling` is a function that is only needed if respelling is allowed in place of manual translit after
//. It takes one argument, the respelling or translit, and should return the transliteration of any respelling but
return any translit unchanged.

`split_bracketed_runs_into_words` is an optional function to split the passed-in text into words. It is used, for
example, to determine what text constitutes a word when followed by an angle-bracket spec, i.e. what the lemma to be
inflected is vs. surrounding fixed text. It takes one argument, the result of splitting the original text on brackets,
and should return alternating runs of words and split characters, or nil to apply the default algorithm. Specifically,
the value passed in is the result of calling `parse_balanced_segment_run(text, "[", "]")` from
[[Module:parse utilities]] on the original text, and the default version of this function calls
`split_alternating_runs(bracketed_runs, pattern, "preserve splitchar")`, where `bracketed_runs` is the value passed in
and `pattern` splits on either spaces or hyphens (unless the text begins with a hyphen, in which case splitting is only
on spaces, so that suffixes can be inflected).

`allow_default_indicator` should be true if the indicator in angle brackets can be omitted and should be automatically
added at the end of the multiword text (if no alternants) or at the end of each alternant (if alternants present).

`allow_blank_lemma` should be true of if a blank lemma is allowed; in such a case, the calling function should
substitute a default lemma, typically taken from the pagename.

The return value is a table of the form
{
  alternant_or_word_specs = {ALTERNANT_OR_WORD_SPEC, ALTERNANT_OR_WORD_SPEC, ...}
  post_text = "TEXT-AT-END",
  post_text_no_links = "TEXT-AT-END-NO-LINKS",
  post_text_translit = "TRANSLIT-OF-TEXT-AT-END" (or None),
}

where ALTERNANT_OR_WORD_SPEC is either an alternant spec as returned by parse_alternant()
or a multiword spec as described in the comment above parse_multiword_spec(). An alternant spec
looks as follows:
{
  alternants = {MULTIWORD_SPEC, MULTIWORD_SPEC, ...},
  before_text = "TEXT-BEFORE-ALTERNANT",
  before_text_no_links = "TEXT-BEFORE-ALTERNANT",
  before_text_translit = "TRANSLIT-OF-TEXT-BEFORE-ALTERNANT" (or None),
}
i.e. it is like what is returned by parse_alternant() but has extra `before_text`
and `before_text_no_links` fields.
"""
def parse_inflected_text(text, props):
    alternant_multiword_spec = {"alternant_or_word_specs": []}
    alternant_segments = m_string_utilities_capturing_split(text, r"(\(\(.*?\)\))")
    last_post_text, last_post_text_no_links, last_post_text_translit = None, None, None
    for i in range(len(alternant_segments)):
        if i % 2 == 0:
            segments = put.parse_balanced_segment_run(alternant_segments[i], "<", ">")
            # Disable allow_default_indicator if alternants are present and we're processing
            # the non-alternant text. Otherwise we will try to treat the non-alternant text
            # surrounding the alternants as an inflected word rather than as raw text.
            multiword_spec = parse_multiword_spec(segments, props, len(alternant_segments) != 1)
            for _, word_spec in ipairs(multiword_spec["word_specs"]):
                table.insert(alternant_multiword_spec["alternant_or_word_specs"], word_spec)

            last_post_text = multiword_spec["post_text"]
            last_post_text_no_links = multiword_spec["post_text_no_links"]
            last_post_text_translit = multiword_spec["post_text_translit"]
        else:
            alternant_spec = parse_alternant(alternant_segments[i], props)
            alternant_spec["before_text"] = last_post_text
            alternant_spec["before_text_no_links"] = last_post_text_no_links
            alternant_spec["before_text_translit"] = last_post_text_translit
            table.insert(alternant_multiword_spec["alternant_or_word_specs"], alternant_spec)


    alternant_multiword_spec["post_text"] = last_post_text
    alternant_multiword_spec["post_text_no_links"] = last_post_text_no_links
    alternant_multiword_spec["post_text_translit"] = last_post_text_translit
    return alternant_multiword_spec


# Inflect alternants in ALTERNANT_SPEC (an object as returned by parse_alternant()).
# This sets the form values in `ALTERNANT_SPEC.forms` for all slots.
# (If a given slot has no values, it will not be present in `ALTERNANT_SPEC.forms`).
def inflect_alternants(alternant_spec, props):
    def f(slot):
        if not props.get("skip_slot") or not props["skip_slot"](slot):
            insert_forms(alternant_spec["forms"], slot, multiword_spec.forms[slot])

    alternant_spec["forms"] = []
    for _, multiword_spec in ipairs(alternant_spec["alternants"]):
        inflect_multiword_or_alternant_multiword_spec(multiword_spec, props)
        iterate_slot_list_or_table(props, f)


"""
Subfunction of export.inflect_multiword_or_alternant_multiword_spec(). This is used in building up the inflections of
multiword expressions. The basic purpose of this function is to append a set of forms representing the inflections of
a given inflected term in a given slot onto the existing forms for that slot. Given a multiword expression potentially
consisting of several inflected terms along with fixed text in between, we work iteratively from left to right, adding
the new forms onto the existing ones. Normally, all combinations of new and existing forms are created, meaning if
there are M existing forms and N new ones, we will end up with M*N forms. However, some of these combinations can be
rejected using the variant mechanism (see the description of get_variants below).

Specifically, `formtable` is a table of per-slot forms, where the key is a slot and the value is a list of form objects
(objects of the form {form=FORM, translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES}). `slot` is the slot in question.
`forms` specifies the forms to be appended onto the existing forms, and is likewise a list of form objects. `props`
is the same as in export.inflect_multiword_or_alternant_multiword_spec(). `before_text` is the fixed text that goes
before the forms to be added. `before_text_no_links` is the same as `before_text` but with any links (i.e. hyperlinks
of the form [[TERM]] or [[TERM|DISPLAY]]) converted into raw terms using remove_links() in [[Module:links]], and
`before_text_translit` is optional manual translit of `before_text_no_links`.

Note that the value "?" in a form is "infectious" in that if either the existing or new form has the value "?", the
resulting combination will also be "?". This allows "?" to be used to mean "unknown".
"""

def append_forms(props, formtable, slot, forms, before_text, before_text_no_links,
        before_text_translit):

    if not forms:
        return

    def nop(k):
        return

    old_forms = formtable.get(slot, [{"form": ""}])
    ret_forms = []
    for old_form in old_forms:
        for form in forms:
            old_form_vars = props["get_variants"](old_form["form"]) if props.get("get_variants") else ""
            form_vars = props["get_variants"](form["form"]) if props.get("get_variants") else ""
            if old_form_vars != "" and form_vars != "" and old_form_vars != form_vars:
                # Reject combination due to non-matching variant codes.
                pass
            else:
                new_form = None
                new_translit = None
                if old_form.get("form") == "?" or form["form"] == "?":
                    new_form = "?"
                else:
                    new_form = old_form["form"] + before_text + form["form"]
                    if old_form.get("translit") or before_text_translit or form.get("translit"):
                        if not props.get("lang"):
                            error("Internal error: If manual translit is given, 'props.lang' must be set")

                        if not before_text_translit:
                            before_text_translit = lua_or(props["lang"].get("transliterate", nop)(before_text_no_links), "")

                        old_translit = lua_or(old_form.get("translit"), props.get("lang").get("transliterate", nop)(m_links_remove_links(old_form.form)), "")
                        translit = lua_or(form.get("translit"), props.get("lang").get("transliterate", nop)(m_links_remove_links(form.form)), "")
                        new_translit = old_translit + before_text_translit + translit

                new_footnotes = combine_footnotes(old_form.get("footnotes", []), form.get("footnotes", []))
                table.insert(ret_forms, {"form": new_form, "translit": new_translit,
                    "footnotes": new_footnotes})

    formtable[slot] = ret_forms

"""
Top-level inflection function. Create the inflections of a noun, verb, adjective or similar. `multiword_spec` is as
returned by `parse_inflected_text` and describes the properties of the term to be inflected, including all the
user-provided inflection specifications (e.g. the number, gender, conjugation/declension/etc. of each word) and the
surrounding text. `props` indicates how to do the actual inflection (see below). The resulting inflected forms are
stored into the `.forms` property of `multiword_spec`. This property holds a table whose keys are slots (i.e. ID's
of individual inflected forms, such as "pres_1sg" for the first-person singular present indicative tense of a verb)
and whose values are lists of the form { form = FORM, translit = MANUAL_TRANSLIT_OR_NIL, footnotes = FOOTNOTE_LIST_OR_NIL},
where FORM is a string specifying the value of the form (e.g. "ouço" for the first-person singular present indicative
of the Portuguese verb [[ouvir]]); MANUAL_TRANSLIT_OR_NIL is the corresponding manual transliteration if needed (i.e.
if the form is in a non-Latin script and the automatic transliteration is incorrect or unavailable), otherwise nil;
and FOOTNOTE_LIST_OR_NIL is a list of footnotes to be attached to the form, or nil for no footnotes. Note that
currently footnotes must be surrounded by brackets, e.g "[archaic]", and should not begin with a capital letter or end
with a period. (Conversion from "[archaic]" to "Archaic." happens automatically.) 

This function has no return value, but modifies `multiword_spec` in-place, adding the `forms` table as described above.
After calling this function, call show_forms() on the `forms` table to convert the forms and footnotes given in this
table to strings suitable for display.

`props` is an object specifying properties used during inflection, as follows:
{
  slot_list = {{"SLOT", "ACCEL"}, {"SLOT", "ACCEL"}, ...},
  slot_table = {SLOT = "ACCEL", SLOT = "ACCEL", ...},
  skip_slot = FUNCTION_TO_SKIP_A_SLOT or nil,
  lang = LANG_OBJECT or nil,
  inflect_word_spec = FUNCTION_TO_INFLECT_AN_INDIVIDUAL_WORD,
  get_variants = FUNCTION_TO_RETURN_A_VARIANT_CODE or nil,
  include_user_specified_links = BOOLEAN,
}

`slot_list` is a list of two-element lists of slots and associated accelerator inflections. SLOT is arbitrary but
should correspond with slot names as generated by `inflect_word_spec`. ACCEL is the corresponding accelerator form;
e.g. if SLOT is "pres_1sg", ACCEL might be "1|s|pres|ind". ACCEL is actually unused during inflection, but is used
during show_forms(), which takes the same `slot_list` as a property upon input.

`slot_table` is a table mapping slots to associated accelerator inflections and serves the same function as
`slot_list`. Only one of `slot_list` or `slot_table` must be given. For new code it is preferable to use `slot_list`
because this allows you to control the order of processing slots, which may occasionally be important.

`skip_slot` is a function of one argument, a slot name, and should return a boolean indicating whether to skip the
given slot during inflection. It can be used, for example, to skip singular slots if the overall term being inflected
is plural-only, and vice-versa.

`lang` is a language object. This is only used to generate manual transliteration. If the language is written in the
Latin script or manual transliteration cannot be specified in the input to parse_inflected_text(), this can be omitted.
(Manual transliteration is allowed if the `lang` object is set in the `props` passed to parse_inflected_text().)

`inflect_word_spec` is the function to do the actual inflection. Note that for compatibility purposes the same function
can be set as the `decline_word_spec` property; don't use this in new code. It is passed a single argument, which is
a WORD_SPEC object describing the word to be inflected and the user-provided inflection specifications. It is exactly
the same as was returned by the `parse_indicator_spec` function provided in the `props` sent on input to
`parse_inflected_text`, but has additional fields describing the word to be inflected and the surrounding text, as
follows:
{
  lemma = "LEMMA",
  before_text = "TEXT-BEFORE-WORD",
  before_text_no_links = "TEXT-BEFORE-WORD-NO-LINKS",
  before_text_translit = "MANUAL-TRANSLIT-OF-TEXT-BEFORE-WORD" or nil (if no manual translit or respelling was specified in the before-text)
  -- Fields as described in parse_indicator_spec()
  ...
}

Here LEMMA is the word to be inflected as specified by the user (including any links if so given), and the
`before_text*` fields describe the raw text preceding the word to be inflected. Any other fields in this object are as
set by `parse_inflected_text`, and describe things like the gender, number, conjugation/declension, etc. as specified
by the user in the <...> spec following the word to be inflected.

`inflect_word_spec` should initialize the `.forms` property of the passed-in WORD_SPEC object to the inflected forms of
the word in question. The value of this property is a table of the same format as the `.forms` property that is
ultimately generated by inflect_multiword_or_alternant_multiword_spec() and described above near the top of this
documentation: i.e. a table whose keys are slots and whose values are lists of the form
  { form = FORM, translit = MANUAL_TRANSLIT_OR_NIL, footnotes = FOOTNOTE_LIST_OR_NIL}.

`get_variants` is either nil or a function of one argument (a string, the value of an individual form). The purpose of
this function is to ensure that in a multiword term where a given slot has more than one possible variant, the final
output has only parallel variants in it. For example, feminine nouns and adjectives in Russian have two possible
endings, one typically in -ой (-oj) and the other in -ою (-oju). If we have a feminine adjective-noun combination (or
a hyphenated feminine noun-noun combination, or similar), and we don't specify `get_variants`, we'll end up with four
values for the instrumental singular: one where both adjective and noun end in -ой, one where both end in -ою, and
two where one of the words ends in -ой and the other in -ою. In general if we have N words each with K variants, we'll
end up with an explosion of N^K possibilities. `get_variants` avoids this by returning a variant code (an arbitary
string) for each variant. If two words each have a non-empty variant code, and the variant codes disagree, the
combination will be rejected. If `get_variants` is not provided, or either variant code is an empty string, or the
variant codes agree, the combination is allowed.

The recommended way to use `get_variants` is as follows:
1. During inflection in `inflect_word_spec`, add a special character or string to each of the variants generated for a
   given slot when there is more than one. (As an optimization, do this only when there is more than one word being
   inflected.) Special Unicode characters can be used for this purpose, e.g. U+FFF0, U+FFF1, ..., U+FFFD, which have
   no meaning in Unicode.
2. Specify `get_variants` as a function that pulls out and returns the special character(s) or string included in the
   variant forms.
3. When calling show_forms(), specify a `canonicalize` function that removes the variant code character(s) or string
   from each form before converting to the display form.

See [[Module:hi-verb]] and [[Module:hi-common]] for an example of doing this in a generalized fashion. (Look for
add_variant_codes(), get_variants() and remove_variant_codes().)

`include_user_specified_links`, if given, ensures that user-specified links in the raw text surrounding a given word
are preserved in the output. If omitted or set to false, such links will be removed and the whole multiword expression
will be linked.
"""

def inflect_multiword_or_alternant_multiword_spec(multiword_spec, props):
    multiword_spec["forms"] = {}
    def f(slot, accel):
        if not props.get("skip_slot") or not props["skip_slot"](slot):
            append_forms(props, multiword_spec["forms"], slot, word_spec["forms"].get(slot),
                (rfind(slot, "linked") or props.get("include_user_specified_links")) and
                word_spec.get("before_text") or word_spec.get("before_text_no_links"),
                word_spec.get("before_text_no_links"), word_spec.get("before_text_translit")
                )

    def f2(slot, accel):
        # If slot is empty or should be skipped, don't try to append post-text.
        if (not props.get("skip_slot") or not props["skip_slot"](slot)) and multiword_spec.get("forms", {}).get(slot):
            append_forms(props, multiword_spec.get("forms"), slot, pseudoform,
                (rfind(slot, "linked") or props.get("include_user_specified_links")) and
                multiword_spec.get("post_text") or multiword_spec.get("post_text_no_links"),
                multiword_spec.get("post_text_no_links"), multiword_spec.get("post_text_translit")
                )

    is_alternant_multiword = bool(multiword_spec.get("alternant_or_word_specs"))
    word_specs = multiword_spec["alternant_or_word_specs"] if is_alternant_multiword else multiword_spec["word_specs"]
    for word_spec in word_specs:
        if word_spec.get("alternants"):
            inflect_alternants(word_spec, props)
        elif props.get("decline_word_spec"):
            props["decline_word_spec"](word_spec)
        else:
            props["inflect_word_spec"](word_spec)

        iterate_slot_list_or_table(props, f)

    if multiword_spec["post_text"]:
        pseudoform = [{"form": ""}]
        iterate_slot_list_or_table(props, f2)



def map_word_specs(alternant_multiword_spec, fun):
    for _, alternant_or_word_spec in ipairs(alternant_multiword_spec["alternant_or_word_specs"]):
        if alternant_or_word_spec.get("alternants"):
            for _, multiword_spec in ipairs(alternant_or_word_spec["alternants"]):
                for _, word_spec in ipairs(multiword_spec["word_specs"]):
                    fun(word_spec)
        else:
            fun(alternant_or_word_spec)

def create_footnote_obj():
    return {
        "notes": [],
        "seen_notes": [],
        "noteindex": 1,
        "seen_refs": [],
    }

def get_footnote_text(form, footnote_obj):
    return ""
    # Unimplemented


"""
Convert the forms in `forms` (a list of form objects, each of which is a table of the form
{ form = FORM, translit = MANUAL_TRANSLIT_OR_NIL, footnotes = FOOTNOTE_LIST_OR_NIL, no_accel = TRUE_TO_SUPPRESS_ACCELERATORS })
into strings. Each form list turns into a string consisting of a comma-separated list of linked forms, with accelerators
(unless `no_accel` is set in a given form). `props` is a table used in generating the strings, as follows:
{
  lang = LANG_OBJECT,
  lemmas = {"LEMMA", "LEMMA", ...},
  slot_list = {{"SLOT", "ACCEL"}, {"SLOT", "ACCEL"}, ...},
  slot_table = {SLOT = "ACCEL", SLOT = "ACCEL", ...},
  include_translit = BOOLEAN,
  create_footnote_obj = nil or FUNCTION_TO_CREATE_FOOTNOTE_OBJ,
  canonicalize = nil or FUNCTION_TO_CANONICALIZE_EACH_FORM,
  transform_link = nil or FUNCTION_TO_TRANSFORM_EACH_LINK,
  transform_accel_obj = nil or FUNCTION_TO_TRANSFORM_EACH_ACCEL_OBJ,
  join_spans = nil or FUNCTION_TO_JOIN_SPANS,
  allow_footnote_symbols = BOOLEAN,
  footnotes = nil or {"EXTRA_FOOTNOTE", "EXTRA_FOOTNOTE", ...},
}

`lemmas` is the list of lemmas, used in the accelerators.

`slot_list` is a list of two-element lists of slots and associated accelerator inflections. SLOT should correspond to
slots generated during inflect_multiword_or_alternant_multiword_spec(). ACCEL is the corresponding accelerator form;
e.g. if SLOT is "pres_1sg", ACCEL might be "1|s|pres|ind". ACCEL is used in generating entries for accelerator support
(see [[WT:ACCEL]]).

`slot_table` is a table mapping slots to associated accelerator inflections and serves the same function as
`slot_list`. Only one of `slot_list` or `slot_table` must be given. For new code it is preferable to use `slot_list`
because this allows you to control the order of processing slots, which may occasionally be important.

`include_translit`, if given, causes transliteration to be included in the generated strings.

`create_footnote_obj` is an optional function of no arguments to create the footnote object used to track footnotes;
see export.create_footnote_obj(). Customizing it is useful to prepopulate the footnote table using
export.get_footnote_text().

`canonicalize` is an optional function of one argument (a form) to canonicalize each form before processing; it can
return nil for no change. The most common purpose of this function is to remove variant codes from the form. See the
documentation for inflect_multiword_or_alternant_multiword_spec() for a description of variant codes and their purpose.

`generate_link` is an optional function to generate the link text for a given form. It is passed four arguments (slot,
for, origentry, accel_obj) where `slot` is the slot being processed, `form` is the specific form object to generate a
link for, `origentry` is the actual text to convert into a link, and `accel_obj` is the accelerator object to include
in the link. If nil is returned, the default algorithm will apply, which is to call
`full_link{lang = lang, term = origentry, tr = "-", accel = accel_obj}` from [[Module:links]]. This can be used e.g. to
customize the appearance of the link. Note that the link should not include any transliteration because it is handled
specially (all transliterations are grouped together).

`transform_link` is an optional function to transform a linked form prior to further processing. It is passed three
arguments (slot, link, link_tr) and should return the transformed link (or if translit is active, it should return two
values, the transformed link and corresponding translit). It can return nil for no change. `transform_link` is used,
for example, in [[Module:de-verb]], where it adds the appropriate pronoun ([[ich]], [[du]], etc.) to finite verb forms,
and adds [[dass]] before special subordinate-clause variants of finte verb forms.

`transform_accel_obj` is an optional function of three arguments (slot, formobj, accel_obj) to transform the default
constructed accelerator object in `accel_obj` into an object that should be passed to full_link() in [[Module:links]].
It should return the new accelerator object, or nil for no acceleration. It can destructively modify the accelerator
object passed in. NOTE: This is called even when the passed-in `accel_obj` is nil (either because the accelerator in
`slot_table` or `slot_list` is "-", or because the form contains links, or because for some reason there is no lemma
available).

`join_spans` is an optional function of three arguments (slot, orig_spans, tr_spans) where the spans in question are
after linking and footnote processing. It should return a string (the joined spans) or nil for the default algorithm,
which separately joins the orig_spans and tr_spans with commas and puts a newline between them.

`allow_footnote_symbols`, if given, causes any footnote symbols attached to forms (e.g. numbers, asterisk) to be
separated off, placed outside the links, and superscripted. In this case, `footnotes` should be a list of footnotes
(preceded by footnote symbols, which are superscripted). These footnotes are combined with any footnotes found in the
forms and placed into `forms.footnotes`. This mechanism of specifying footnotes is provided for backward compatibility
with certain existing inflection modules and should not be used for new modules. Instead, use the regular footnote
mechanism specified using the `footnotes` property attached to each form object.
"""
def show_forms(forms, props):
    footnote_obj = props.create_footnote_obj and props.create_footnote_obj() or create_footnote_obj()
    accel_lemma = props.lemmas[1]
    accel_lemma_translit
    if type(accel_lemma) is dict:
        accel_lemma_translit = accel_lemma.translit
        accel_lemma = accel_lemma.form

    accel_lemma = accel_lemma and m_links_remove_links(accel_lemma) or None
    lemma_forms = {}
    for lemma in props.get("lemmas", []):
        if type(lemma) is dict:
            m_table.insertIfNot(lemma_forms, lemma.form)
        else:
            m_table.insertIfNot(lemma_forms, lemma)


    forms.lemma = ", ".join(lemma_forms) if lemma_forms else mw.title.getCurrentTitle().text

    m_table_tools = require("Module:table tools")
    m_script_utilities = require("Module:script utilities")
    def do_slot(slot, accel_form):
        formvals = forms[slot]
        if formvals:
            orig_spans = {}
            tr_spans = {}
            orignotes, trnotes = "", ""
            if not isinstance(formvals, list):
                raise ValueError(f"Internal error: For slot '{slot}', expected list but got ", formvals)
            for i, form in enumerate(formvals):
                orig_text = props.canonicalize and props.canonicalize(form.form) or form.form
                link
                if form.form == "—" or form.form == "?":
                    link = orig_text
                else:
                    origentry
                    if props.allow_footnote_symbols:
                        origentry, orignotes = m_table_tools.get_notes(orig_text)
                    else:
                        origentry = orig_text

                    # remove redundant link surrounding entire form
                    origentry = remove_redundant_links(origentry)
                    accel_obj
                    # check if form still has links; if so, don't add accelerators
                    # because the resulting entries will be wrong
                    if accel_lemma and not form.no_accel and accel_form != "-" and \
                        not rfind(origentry, r"\[\["):
                        accel_obj = {
                            "form": accel_form,
                            "translit": ternery(props.get("include_translit"), form.get("translit"), None),
                            "lemma": accel_lemma,
                            "lemma_translit": ternery(props.get("include_translit"), accel_lemma_translit, None),
                        }
                    if props.get("transform_accel_obj"):
                        accel_obj = props["transform_accel_obj"](slot, form, accel_obj)
                    if props.get("generate_link"):
                        link = props["generate_link"](slot, form, origentry, accel_obj)

                    if not link:
                        link = m_links_full_link({"lang": props["lang"], "term": origentry, "tr": "-", "accel": accel_obj})

                tr = ternery(props.get("include_translit"), lua_or(form.get("translit"), props["lang"].transliterate(m_links_remove_links(orig_text))), None)
                trentry = None
                if props.get("allow_footnote_symbols") and tr:
                    trentry, trnotes = m_table_tools.get_notes(tr)
                else:
                    trentry = tr

                if props.get("transform_link"):
                    newlink, newtr = props["transform_link"](slot, link, tr)
                    if newlink:
                        link, tr = newlink, newtr


                link = link + orignotes
                tr = ternery(tr, m_script_utilities.tag_translit(trentry, props.lang, "default", " style=\"color: #888;\"") + trnotes, None)
                if form.get("footnotes"):
                    footnote_text = get_footnote_text(form, footnote_obj)
                    link = link + footnote_text
                    tr = ternery(tr, tr + footnote_text, None)

                table.insert(orig_spans, link)
                if tr:
                    table.insert(tr_spans, tr)


            joined_spans = None
            if props.get("join_spans"):
                joined_spans = props["join_spans"](slot, orig_spans, tr_spans)

            if not joined_spans:
                orig_span = ", ".join(orig_spans)
                tr_span
                if len(tr_spans) > 0:
                    tr_span = ", ".join(tr_spans)

                if tr_span:
                    joined_spans = orig_span + "<br />" + tr_span
                else:
                    joined_spans = orig_span


            forms[slot] = joined_spans
        else:
            forms[slot] = "—"

    iterate_slot_list_or_table(props, do_slot)

    all_notes = footnote_obj.notes
    if props.footnotes:
        for _, note in enumerate(props.get("footnotes", [])):
            symbol, entry = m_table_tools.get_initial_notes(note)
            table.insert(all_notes, symbol + entry)

    forms.footnote = "<br />".join(all_notes)

# Given a list of forms (each of which is a table of the form
# {form=FORM, translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES}), concatenate into a
# SLOT=FORM//TRANSLIT,FORM//TRANSLIT,... string (or SLOT=FORM,FORM,... if no translit),
# replacing embedded | signs with <!>.
def concat_forms_in_slot(forms):
    if forms:
        new_vals = []
        for v in forms:
            form = v["form"]
            if v.get("translit"):
                form = form + "//" + v["translit"]
            new_vals.append(rsub(form, "[|]", "<!>"))

        return ",".join(new_vals)
