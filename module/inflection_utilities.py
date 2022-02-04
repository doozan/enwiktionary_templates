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
Revision 62601729, 04:25, 25 May 2021
"""

import re

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


"""
In order to understand the following parsing code, you need to understand how inflected
text specs work. They are intended to work with inflected text where individual words to
be inflected may be followed by inflection specs in angle brackets. The format of the
text inside of the angle brackets is up to the individual language and part-of-speech
specific implementation. A real-world example is as follows:
"[[медичний|меди́чна]]<+> [[сестра́]]<*,*#.pr>". This is the inflection of a multiword
expression "меди́чна сестра́", which means "nurse" (literally "medical sister"), consisting
of two words: the adjective меди́чна ("medical" in the feminine singular) and the noun
сестра́ ("sister"). The specs in angle brackets follow each word to be inflected; for
example, <+> means that the preceding word should be declined as an adjective.

The code below works in terms of balanced expressions, which are bounded by delimiters
such as < > or [ ]. The intention is to allow separators such as spaces to be embedded
inside of delimiters; such embedded separators will not be parsed as separators.
For example, Ukrainian noun specs allow footnotes in brackets to be inserted inside of
angle brackets; something like "меди́чна<+> сестра́<pr.[this is a footnote]>" is legal,
as is "[[медичний|меди́чна]]<+> [[сестра́]]<pr.[this is an <i>italicized footnote</i>]>",
and the parsing code should not be confused by the embedded brackets, spaces or angle
brackets.

The parsing is done by two def s, which work in close concert::
parse_balanced_segment_run() and split_alternating_runs(). To illustrate, consider
the following:

parse_balanced_segment_run("foo<M.proper noun> bar<F>", "<", ">") =
  {"foo", "<M.proper noun>", " bar", "<F>", ""}

then

split_alternating_runs({"foo", "<M.proper noun>", " bar", "<F>", ""}, " ") =
  {{"foo", "<M.proper noun>", ""}, {"bar", "<F>", ""}}

Here, we start out with a typical inflected text spec "foo<M.proper noun> bar<F>",
call parse_balanced_segment_run() on it, and call split_alternating_runs() on the
result. The output of parse_balanced_segment_run() is a list where even-numbered
segments are bounded by the bracket-like characters passed into the def ,:
and odd-numbered segments consist of the surrounding text. split_alternating_runs()
is called on this, and splits *only* the odd-numbered segments, grouping all
segments between the specified character. Note that the inner lists output by
split_alternating_runs() are themselves in the same format as the output of
parse_balanced_segment_run(), with bracket-bounded text in the even-numbered segments.
Hence, such lists can be passed again to split_alternating_runs().
"""


# Parse a string containing matched instances of parens, brackets or the like.
# Return a list of strings, alternating between textual runs not containing the
# open/close characters and runs beginning and ending with the open/close
# characters. For example,
#
# parse_balanced_segment_run("foo(x(1)), bar(2)", "(", ")") = {"foo", "(x(1))", ", bar", "(2)", ""}.
def parse_balanced_segment_run(segment_run, _open, _close):
    break_on_open_close = m_string_utilities_capturing_split(segment_run, rf"([\{_open}\{_close}])")
    text_and_specs = []
    level = 0
    seg_group = []
    for i, seg in enumerate(break_on_open_close):
        if i % 2 == 1:
            if seg == _open:
                seg_group.append(seg)
                level = level + 1
            else:
                assert(seg == _close)
                seg_group.append(seg)
                level = level - 1
                if level < 0:
                    error("Unmatched " + _close + " sign: '" + segment_run + "'")
                elif level == 0:
                    text_and_specs.append("".join(seg_group))
                    seg_group = []

        elif level > 0:
            seg_group.append(seg)
        else:
            text_and_specs.append(seg)

    if level > 0:
        error("Unmatched " + _open + " sign: '" + segment_run + "'")

    return text_and_specs



# Like parse_balanced_segment_run() but accepts multiple sets of delimiters. For example,
#
# parse_multi_delimiter_balanced_segment_run("foo[bar(baz[bat])], quux<glorp>", {{"[", "]"}, {"(", ")"}, {"<", ">"}}) =
#        {"foo", "[bar(baz[bat])]", ", quux", "<glorp>", ""}.
def parse_multi_delimiter_balanced_segment_run(segment_run, delimiter_pairs):
    open_to_close_map = {}
    open_close_items = []
    for open_close in delimiter_pairs:
        _open, _close = open_close
        open_to_close_map[_open] = _close
        table.insert(open_close_items, rf"\{_open}")
        table.insert(open_close_items, rf"\{_close}")

    open_close_pattern = "([" + "".join(open_close_items) + "])"
    break_on_open_close = m_string_utilities_capturing_split(segment_run, open_close_pattern)
    text_and_specs = []
    level = 0
    seg_group = []
    open_at_level_zero = None
    for i, seg in enumerate(break_on_open_close):
        if i % 2 == 1:
            seg_group.append(seg)
            if level == 0:
                if not seg in open_to_close_map:
                    error("Unmatched " + seg + " sign: '" + segment_run + "'")

                assert(open_at_level_zero == None)
                open_at_level_zero = seg
                level = level + 1
            elif seg == open_at_level_zero:
                level = level + 1
            elif seg == open_to_close_map[open_at_level_zero]:
                level = level - 1
                assert(level >= 0)
                if level == 0:
                    text_and_specs.append("".join(seg_group))
                    seg_group = []
                    open_at_level_zero = None


        elif level > 0:
            seg_group.append(seg)
        else:
            text_and_specs.append(seg)


    if level > 0:
        error("Unmatched " + open_at_level_zero + " sign: '" + segment_run + "'")

    return text_and_specs



"""
Split a list of alternating textual runs of the format returned by
`parse_balanced_segment_run` on `splitchar`. This only splits the odd-numbered
textual runs (the portions between the balanced open/close characters).
The return value is a list of lists, where each list contains an odd number of
elements, where the even-numbered elements of the sublists are the original
balanced textual run portions. For example, if we:

parse_balanced_segment_run("foo<M.proper noun> bar<F>", "<", ">") =
  {"foo", "<M.proper noun>", " bar", "<F>", ""}

then

split_alternating_runs({"foo", "<M.proper noun>", " bar", "<F>", ""}, " ") =
  {{"foo", "<M.proper noun>", ""}, {"bar", "<F>", ""}}

Note that we did not touch the text "<M.proper noun>" even though it contains a space
in it, because it is an even-numbered element of the input list. This is intentional and
allows for embedded separators inside of brackets/parens/etc. Note also that the inner
lists in the return value are of the same form as the input list (i.e. they consist of
alternating textual runs where the even-numbered segments are balanced runs), and can in
turn be passed to split_alternating_runs().

If `preserve_splitchar` is passed in, the split character is included in the output,
as follows:

split_alternating_runs({"foo", "<M.proper noun>", " bar", "<F>", ""}, " ", True) =
  {{"foo", "<M.proper noun>", ""}, {" "}, {"bar", "<F>", ""}}

Consider what happens if the original string has multiple spaces between brackets,
and multiple sets of brackets without spaces between them.

parse_balanced_segment_run("foo[dated][low colloquial] baz-bat quux xyzzy[archaic]", "[", "]") =
  {"foo", "[dated]", "", "[low colloquial]", " baz-bat quux xyzzy", "[archaic]", ""}

then

split_alternating_runs({"foo", "[dated]", "", "[low colloquial]", " baz-bat quux xyzzy", "[archaic]", ""}, "[ %-]") =
  {{"foo", "[dated]", "", "[low colloquial]", ""}, {"baz"}, {"bat"}, {"quux"}, {"xyzzy", "[archaic]", ""}}

If `preserve_splitchar` is passed in, the split character is included in the output,
as follows:

split_alternating_runs({"foo", "[dated]", "", "[low colloquial]", " baz bat quux xyzzy", "[archaic]", ""}, "[ %-]", True) =
  {{"foo", "[dated]", "", "[low colloquial]", ""}, {" "}, {"baz"}, {"-"}, {"bat"}, {" "}, {"quux"}, {" "}, {"xyzzy", "[archaic]", ""}}

As can be seen, the even-numbered elements in the outer list are one-element lists consisting of the separator text.
"""
def split_alternating_runs(segment_runs, splitchar, preserve_splitchar=False):
    grouped_runs = []
    run = []
    for i, seg in enumerate(segment_runs):
        if i % 2 == 1:
            run.append(seg)
        else:
            parts = m_string_utilities_capturing_split(seg, "(" + splitchar + ")") if preserve_splitchar else rsplit(seg, splitchar)
            run.append(parts[0])
            for j in range(1,len(parts)):
                grouped_runs.append(run)
                run = [parts[j]]

    if run:
        grouped_runs.append(run)

    return grouped_runs



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

            new_vals.append(form.replace("|", "<!>"))

        return ",".join(new_vals)


# Insert a form (an object of the form {form=FORM, translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES})
# into a list of such forms. If the form is already present, the footnotes of the existing and
# new form might be combined (specifically, footnotes in the new form beginning with ! will be
# combined).
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
                # The behavior here has changed; track cases where the old behavior might
                # be needed by adding ! to the footnote.
                #require("Module:debug").track("inflection-utilities/combining-footnotes")
                any_footnotes_with_bang = False
                for footnote in form["footnotes"]:
                    if rfind(footnote, r"^\[!"):
                        any_footnotes_with_bang = True
                        break

                if any_footnotes_with_bang:
                    if not listform.get("footnotes"):
                        listform["footnotes"] = []

                    for footnote in form["footnotes"]:
                        already_seen = False
                        if rfind(footnote, r"^\[!"):
                            for existing_footnote in listform["footnotes"]:
                                if rsub(existing_footnote, r"^\[!", "") == rsub(footnote, r"^\[!", ""):
                                    already_seen = True
                                    break

                            if not already_seen:
                                listform["footnotes"].append(footnote)

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


# Map a def over the form values in FORMS (a list of objects of the form:
# {form=FORM, translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES}). The def is called with:
# two arguments, the original form and manual translit; if manual translit isn't relevant,
# it's fine to declare the def with only one argument. The return value is either a:
# single value (the new form) or two values (the new form and new manual translit).
# Use insert_form_into_list() to insert them into the returned list in case two different
# forms map to the same thing.
def map_forms(forms, fun):
    if not forms:
        return None

    retval = []
    for form in forms:
        newform, newtranslit = fun(form.get("form"), form.get("translit"))
        newform = {"form": newform, "translit": newtranslit, "footnotes": form.get("footnotes", [])}
        insert_form_into_list(retval, newform)

    return retval


# Map a list-returning def over the form values in FORMS (a list of objects of the form:
# {form=FORM, translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES}). The def is called witih:
# two arguments, the original form and manual translit; if manual translit isn't relevant,
# it's fine to declare the def with only one argument. The return value is either a:
# list of forms or a list of objects of the form {form=FORM, translit=MANUAL_TRANSLIT}.
# Use insert_form_into_list() to insert them into the returned list in case two different
# forms map to the same thing.
def flatmap_forms(forms, fun):
    if not forms:
        return None

    retval = []
    for form in forms:
        funret = fun(form.get("form"), form.get("translit"))
        for fr in funret:
            newform = None
            if type(fr) is dict:
                newform = {"form": fr.get("form"), "translit": fr.get("translit"), "footnotes": form.get("footnotes", [])}
            else:
                newform = {"form": fr, "footnotes": form.get("footnotes", [])}

            insert_form_into_list(retval, newform)

    return retval



# Map a def over the form values in FORMS (a single string, a single object of the form:
# {form=FORM, translit=MANUAL_TRANSLIT, footnotes=FOOTNOTES}, or a list of either of the
# previous two types). If FIRST_ONLY is given and FORMS is a list, only map over the first
# element. Return value is of the same form as FORMS. The def is called with two:
# arguments, the original form and manual translit; if manual translit isn't relevant,
# it's fine to declare the def with only one argument. The return value is either a:
# single value (the new form) or two values (the new form and new manual translit).
def map_form_or_forms(forms, fn, first_only):
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



# Expand a given footnote (as specified by the user, including the surrounding brackets)
# into the form to be inserted into the final generated table.
def expand_footnote(note):
    notetext = rmatch(note, r"^\[!?(.*)\]$")
    if not notetext:
        error("Internal error: Footnote should be surrounded by brackets: " + note)

    if footnote_abbrevs[notetext]:
        notetext = footnote_abbrevs[notetext]
    else:
        split_notes = m_string_utilities_capturing_split(notetext, "<(.*?)>")
        for i, split_note in enumerate(split_notes):
            if i % 2 == 0:
                split_notes[i] = footnote_abbrevs[split_note]
                if not split_notes[i]:
                    # Don't error for now, because HTML might be in the footnote.
                    # Instead we should switch the syntax here to e.g. <<a>> to avoid
                    # conflicting with HTML.
                    split_notes[i] = "<" + split_note + ">"
                    #error("Unrecognized footnote abbrev: <" + split_note + ">")

        notetext = "".join(split_notes)

    return notetext.capitalize() + "."



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




# Older entry point. FIXME: Obsolete me.
def generate_form(form, footnotes):
    return combine_form_and_footnotes(form, footnotes)



# Combine a single form (either a string or object {form = FORM, footnotes = FOOTNOTES, ...}) or a list of same
# along with footnotes and return a list of forms where each returned form is an object
# {form = FORM, footnotes = FOOTNOTES, ...}.
def convert_to_general_list_form(word_or_words, footnotes=[]):
    if isinstance(word_or_words, str):
        return [{"form": word_or_words, "footnotes": footnotes}]
    elif isinstance(word_or_words, dict):
        return [combine_form_and_footnotes(word_or_words, footnotes)]
    else:
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



def add_forms(forms, slot, stems, endings, combine_stem_ending, \
        lang=None, combine_stem_ending_tr=False, footnotes=[]):
    if stems == None or endings == None:
        return

    if isinstance(stems, str) and isinstance(endings, str):
        insert_form(forms, slot, {"form": combine_stem_ending(stems, endings), "footnotes": footnotes})
    elif isinstance(stems, str) and is_table_of_strings(endings):
        for ending in endings:
            insert_form(forms, slot, {"form": combine_stem_ending(stems, ending), "footnotes": rootnotes})

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

                new_form = combine_stem_ending(stem.get("form"), ending.get("form"))
                new_translit = None
                if stem.get("translit") or ending.get("translit"):
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

    # If the text begins with a hyphen, include the hyphen in the set of allowed characters
    # for an inflected segment. This way, e.g. conjugating "-ir" is treated as a regular
    # -ir verb rather than a hyphen + irregular [[ir]].
    is_suffix = rfind(text, r"^\-")
    # Call parse_balanced_segment_run() to keep multiword links together.
    bracketed_runs = parse_balanced_segment_run(text, "[", "]")
    # Split on space or hyphen. Use preserve_splitchar so we know whether the separator was
    # a space or hyphen.
    splitchar = " " if is_suffix else r"[ \-]"
    space_separated_groups = split_alternating_runs(bracketed_runs,
        splitchar, "preserve splitchar")

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
    segments = parse_balanced_segment_run(alternant_text, "<", ">")
    comma_separated_groups = split_alternating_runs(segments, r"\s*,\s*")
    alternant_spec = {"alternants": []}
    for _, comma_separated_group in ipairs(comma_separated_groups):
        table.insert(alternant_spec["alternants"], parse_multiword_spec(comma_separated_group, props))

    return alternant_spec


"""
Top-level parsing def . Parse text describing one or more inflected words.:
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
  parse_indicator_spec = def _TO_PARSE_AN_INDICATOR_SPEC (required; takes two arguments,:
                           a string surrounded by angle brackets and the lemma, and should
                           return a word_spec object containing properties describing the
                           indicators inside of the angle brackets),
  lang = LANG_OBJECT (only needed if manual translit or respelling may be present using //),
  transliterate_respelling = def _TO_TRANSLITERATE_RESPELLING (only needed of respelling:
                               is allowed in place of manual translit after //; takes one
                               argument, the respelling or translit, and should return the
                               transliteration of any resplling but return any translit
                               unchanged),
  allow_default_indicator = BOOLEAN_OR_NIL (True if the indicator in angle brackets can
                              be omitted and will be automatically added at the end of the
                              multiword text (if no alternants) or at the end of each
                              alternant (if alternants present),
  allow_blank_lemma = BOOLEAN_OR_NIL (True if a blank lemma is allowed; in such a case, the
                        calling def should substitute a default lemma, typically taken:
                        from the pagename)
}

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
            segments = parse_balanced_segment_run(alternant_segments[i], "<", ">")
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



# Older entry point. FIXME: Convert all uses of this to use parse_inflected_text instead. 
def parse_alternant_multiword_spec(text, parse_indicator_spec, allow_default_indicator, allow_blank_lemma):
    props = {
        "parse_indicator_spec": parse_indicator_spec,
        "allow_default_indicator": allow_default_indicator,
        "allow_blank_lemma": allow_blank_lemma,
    }
    return parse_inflected_text(text, props)



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


def append_forms(props, formtable, slot, forms, before_text, before_text_no_links,
        before_text_translit):
    if not forms:
        return

    def nop(k):
        return

    old_forms = formtable.get(slot, [{"form": ""}])
    ret_forms = []
    for _, old_form in ipairs(old_forms):
        for _, form in ipairs(forms):
            old_form_vars = props["get_variants"](old_form["form"]) if props.get("get_variants") else ""
            form_vars = props["get_variants"](form["form"]) if props.get("get_variants") else ""
            if old_form_vars != "" and form_vars != "" and old_form_vars != form_vars:
                # Reject combination due to non-matching variant codes.
                pass
            else:
                new_form = old_form["form"] + before_text + form["form"]
                new_translit = None
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
        if (not props.get("skip_slot") or not props.get("skip_slot")(slot)) and multiword_spec.get("forms", {}).get(slot):
            append_forms(props, multiword_spec.get("forms"), slot, pseudoform,
                (rfind(slot, "linked") or props.get("include_user_specified_links")) and
                multiword_spec.get("post_text") or multiword_spec.get("post_text_no_links"),
                multiword_spec.get("post_text_no_links"), multiword_spec.get("post_text_translit")
                )

    is_alternant_multiword = not not multiword_spec.get("alternant_or_word_specs")
    for _, word_spec in ipairs(ternery(is_alternant_multiword, multiword_spec.get("alternant_or_word_specs"), multiword_spec.get("word_specs"))):
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



def decline_multiword_or_alternant_multiword_spec(multiword_spec, props):
    return inflect_multiword_or_alternant_multiword_spec(multiword_spec, props)


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
    }

def get_footnote_text(form, footnote_obj):
    if not form.get("footnotes"):
        return ""

    link_indices = []
    for _, footnote in ipairs(form.footnotes):
        footnote = expand_footnote(footnote)
        this_noteindex = footnote_obj.seen_notes[footnote]
        if not this_noteindex:
            # Generate a footnote index.
            this_noteindex = footnote_obj.noteindex
            footnote_obj.noteindex = footnote_obj.noteindex + 1
            table.insert(footnote_obj.notes, '<sup style="color: red">' + this_noteindex + '</sup>' + footnote)
            footnote_obj.seen_notes[footnote] = this_noteindex

        m_table.insertIfNot(link_indices, this_noteindex)

    table.sort(link_indices)
    return '<sup style="color: red">' + ",".join(link_indices) + '</sup>'



"""
Convert the forms in `forms` (a list of form objects, each of which is a table of the form
{ form = FORM, translit = MANUAL_TRANSLIT_OR_NIL, footnotes = FOOTNOTE_LIST_OR_NIL, no_accel = True_TO_SUPPRESS_ACCELERATORS })
into strings. Each form list turns into a string consisting of a comma-separated list of linked forms, with accelerators
(unless `no_accel` is set in a given form). `props` is a table used in generating the strings, as follows:
{
  lang = LANG_OBJECT,
  lemmas = LEMMAS,
  slot_table = SLOT_TABLE,
  slot_list = SLOT_LIST,
  include_translit = BOOLEAN,
  create_footnote_obj = def _TO_CREATE_FOOTNOTE_OBJ,:
  canonicalize = def _TO_CANONICALIZE_EACH_FORM,:
  transform_link = def _TO_TRANSFORM_EACH_LINK,:
  join_spans = def _TO_JOIN_SPANS,:
  allow_footnote_symbols = BOOLEAN,
  footnotes = EXTRA_FOOTNOTES,
}
`lemmas` is the list of lemmas, used in the accelerators.
`slot_list` is a list of two-element lists of slots and associated accelerator inflections.
`slot_table` is a table mapping slots to associated accelerator inflections.
  (One of `slot_list` or `slot_table` must be given.)
If `include_translit` is given, transliteration is included in the generated strings.
`create_footnote_obj` is an optional def of no arguments to create the footnote object used to track footnotes;:
  see create_footnote_obj(). Customizing it is useful to prepopulate the footnote table using
  get_footnote_text().
`canonicalize` is an optional def of one argument (a form) to canonicalize each form before processing; it can return None:
  for no change.
`transform_link` is an optional def to transform a linked form prior to further processing; it is passed three arguments:
  (slot, link, link_tr) and should return the transformed link (or if translit is active, it should return the transformed link
  and corresponding translit). It can return None for no change.
`join_spans` is an optional def of three arguments (slot, orig_spans, tr_spans) where the spans in question are after:
  linking and footnote processing. It should return a string (the joined spans) or None for the default algorithm, which separately
  joins the orig_spans and tr_spans with commas and puts a newline between them.
If `allow_footnote_symbols` is given, footnote symbols attached to forms (e.g. numbers, asterisk) are separated off, placed outside
the links, and superscripted. In this case, `footnotes` should be a list of footnotes (preceded by footnote symbols, which are
superscripted). These footnotes are combined with any footnotes found in the forms and placed into `forms.footnotes`.
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
