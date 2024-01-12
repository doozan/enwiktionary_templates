import enwiktionary_templates.module.inflection_utilities as M

def test():

    segments = M.parse_balanced_segment_run("foo<M.proper noun> bar<F>", "<", ">")
    assert segments == ["foo", "<M.proper noun>", " bar", "<F>", ""]

    assert M.split_alternating_runs(segments, " ") == [["foo", "<M.proper noun>", ""], ["bar", "<F>", ""]]
    assert M.split_alternating_runs(segments, " ", True) == [["foo", "<M.proper noun>", ""], [" "], ["bar", "<F>", ""]]


    segments = M.parse_balanced_segment_run("foo[dated][low colloquial] baz-bat quux xyzzy[archaic]", "[", "]")
    assert segments == ["foo", "[dated]", "", "[low colloquial]", " baz-bat quux xyzzy", "[archaic]", ""]

    assert M.split_alternating_runs(segments, r"[ \-]") == \
        [["foo", "[dated]", "", "[low colloquial]", ""], ["baz"], ["bat"], ["quux"], ["xyzzy", "[archaic]", ""]]

    assert M.split_alternating_runs(segments, r"[ \-]", True) == \
        [["foo", "[dated]", "", "[low colloquial]", ""], [" "], ["baz"], ["-"], ["bat"], [" "], ["quux"], [" "], ["xyzzy", "[archaic]", ""]]


    assert M.parse_multi_delimiter_balanced_segment_run("foo[bar(baz[bat])], quux<glorp>", [["[", "]"], ["(", ")"], ["<", ">"]]) == ["foo", "[bar(baz[bat])]", ", quux", "<glorp>", ""]


    text = "[[медичний|меди́чна]]<+> [[сестра́]]<+>"
    segments = M.parse_balanced_segment_run(text, "<", ">")

    assert segments == ['[[медичний|меди́чна]]', '<+>', ' [[сестра́]]', '<+>', '']


def notest_parse_spec():

    parse_props = {
        "parse_indicator_spec": es_verb.parse_indicator_spec,
        "lang": None,
        "allow_default_indicator": True,
        "allow_blank_lemma": True,
    }

    #def parse_multiword_spec(segments, props, disable_allow_default_indicator):
    assert M.parse_multiword_spec(segments, parse_props, False) == {
        'post_text': '',
        'post_text_no_links': '',
        'post_text_translit': None,
        'word_specs': [{'angle_bracket_spec': '<+>',
                        'before_text': '',
                        'before_text_no_links': '',
                        'before_text_translit': None,
                        'lemma': '[[медичний|меди́чна]]',
                        'vowel_alt': [{'footnotes': [], 'form': '+'}]},
                       {'angle_bracket_spec': '<+>',
                        'before_text': ' ',
                        'before_text_no_links': ' ',
                        'before_text_translit': None,
                        'lemma': '[[сестра́]]',
                        'vowel_alt': [{'footnotes': [], 'form': '+'}]}]}


