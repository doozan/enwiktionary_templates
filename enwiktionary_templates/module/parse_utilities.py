import re

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

"""
In order to understand the following parsing code, you need to understand how inflected text specs work. They are
intended to work with inflected text where individual words to be inflected may be followed by inflection specs in
angle brackets. The format of the text inside of the angle brackets is up to the individual language and part-of-speech
specific implementation. A real-world example is as follows: "[[медичний|меди́чна]]<+> [[сестра́]]<*,*#.pr>". This is the inflection of a multiword expression "меди́чна сестра́", which means "nurse" in Ukrainian (literally "medical sister"),
consisting of two words: the adjective меди́чна ("medical" in the feminine singular) and the noun сестра́ ("sister"). The
specs in angle brackets follow each word to be inflected; for example, <+> means that the preceding word should be
declined as an adjective.

The code below works in terms of balanced expressions, which are bounded by delimiters such as < > or [ ]. The
intention is to allow separators such as spaces to be embedded inside of delimiters; such embedded separators will not
be parsed as separators. For example, Ukrainian noun specs allow footnotes in brackets to be inserted inside of angle
brackets; something like "меди́чна<+> сестра́<pr.[this is a footnote]>" is legal, as is
"[[медичний|меди́чна]]<+> [[сестра́]]<pr.[this is an <i>italicized footnote</i>]>", and the parsing code should not be
confused by the embedded brackets, spaces or angle brackets.

The parsing is done by two functions, which work in close concert: parse_balanced_segment_run() and
split_alternating_runs(). To illustrate, consider the following:

parse_balanced_segment_run("foo<M.proper noun> bar<F>", "<", ">") =
  {"foo", "<M.proper noun>", " bar", "<F>", ""}

then

split_alternating_runs({"foo", "<M.proper noun>", " bar", "<F>", ""}, " ") =
  {{"foo", "<M.proper noun>", ""}, {"bar", "<F>", ""}}

Here, we start out with a typical inflected text spec "foo<M.proper noun> bar<F>", call parse_balanced_segment_run() on
it, and call split_alternating_runs() on the result. The output of parse_balanced_segment_run() is a list where
even-numbered segments are bounded by the bracket-like characters passed into the function, and odd-numbered segments
consist of the surrounding text. split_alternating_runs() is called on this, and splits *only* the odd-numbered
segments, grouping all segments between the specified character. Note that the inner lists output by
split_alternating_runs() are themselves in the same format as the output of parse_balanced_segment_run(), with
bracket-bounded text in the even-numbered segments. Hence, such lists can be passed again to split_alternating_runs().
"""

# Parse a string containing matched instances of parens, brackets or the like. Return a list of strings, alternating
# between textual runs not containing the open/close characters and runs beginning and ending with the open/close
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
Split a list of alternating textual runs of the format returned by `parse_balanced_segment_run` on `splitchar`. This
only splits the odd-numbered textual runs (the portions between the balanced open/close characters).  The return value
is a list of lists, where each list contains an odd number of elements, where the even-numbered elements of the sublists
are the original balanced textual run portions. For example, if we do

parse_balanced_segment_run("foo<M.proper noun> bar<F>", "<", ">") =
  {"foo", "<M.proper noun>", " bar", "<F>", ""}

then

split_alternating_runs({"foo", "<M.proper noun>", " bar", "<F>", ""}, " ") =
  {{"foo", "<M.proper noun>", ""}, {"bar", "<F>", ""}}

Note that we did not touch the text "<M.proper noun>" even though it contains a space in it, because it is an
even-numbered element of the input list. This is intentional and allows for embedded separators inside of
brackets/parens/etc. Note also that the inner lists in the return value are of the same form as the input list (i.e.
they consist of alternating textual runs where the even-numbered segments are balanced runs), and can in turn be passed
to split_alternating_runs().

If `preserve_splitchar` is passed in, the split character is included in the output, as follows:

split_alternating_runs({"foo", "<M.proper noun>", " bar", "<F>", ""}, " ", true) =
  {{"foo", "<M.proper noun>", ""}, {" "}, {"bar", "<F>", ""}}

Consider what happens if the original string has multiple spaces between brackets, and multiple sets of brackets
without spaces between them.

parse_balanced_segment_run("foo[dated][low colloquial] baz-bat quux xyzzy[archaic]", "[", "]") =
  {"foo", "[dated]", "", "[low colloquial]", " baz-bat quux xyzzy", "[archaic]", ""}

then

split_alternating_runs({"foo", "[dated]", "", "[low colloquial]", " baz-bat quux xyzzy", "[archaic]", ""}, "[ %-]") =
  {{"foo", "[dated]", "", "[low colloquial]", ""}, {"baz"}, {"bat"}, {"quux"}, {"xyzzy", "[archaic]", ""}}

If `preserve_splitchar` is passed in, the split character is included in the output,
as follows:

split_alternating_runs({"foo", "[dated]", "", "[low colloquial]", " baz bat quux xyzzy", "[archaic]", ""}, "[ %-]", true) =
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

def strip_spaces(text):
    return rsub(text, r"^\s*(.-)\s*$", r"\1")

# Apply an arbitrary function `frob` to the "raw-text" segments in a split run set (the output of
# split_alternating_runs()). We leave alone stuff within balanced delimiters (footnotes, inflection specs and the
# like), as well as splitchars themselves if present. `preserve_splitchar` indicates whether splitchars are present
# in the split run set. `frob` is a function of one argument (the string to frob) and should return one argument (the
# frobbed string). We operate by only frobbing odd-numbered segments, and only in odd-numbered runs if
# preserve_splitchar is given.

def frob_raw_text_alternating_runs(split_run_set, frob, preserve_splitchar):
    for i, run in ipairs(split_run_set):
        if not preserve_splitchar or i % 2 == 1:
            for j, segment in ipairs(run):
                if j % 2 == 1:
                    run[j] = frob(segment)

# Like split_alternating_runs() but applies an arbitrary function `frob` to "raw-text" segments in the result (i.e.
# not stuff within balanced delimiters such as footnotes and inflection specs, and not splitchars if present). `frob`
# is a function of one argument (the string to frob) and should return one argument (the frobbed string).

def split_alternating_runs_and_frob_raw_text(run, splitchar, frob, preserve_splitchar):
    split_runs = export.split_alternating_runs(run, splitchar, preserve_splitchar)
    frob_raw_text_alternating_runs(split_runs, frob, preserve_splitchar)
    return split_runs
