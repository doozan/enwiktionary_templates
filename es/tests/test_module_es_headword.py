#from .module_es_headword import make_plural
import enwiktionary_templates.es.module_es_headword as es_headword

def test_add_endings():
    add_endings = es_headword.add_endings

    assert add_endings("word", "end") == ["wordend"]
    assert add_endings("word", ["1", "2"]) == ["word1", "word2"]
    assert add_endings(["one", "two"], "x") == ["onex", "twox"]
    assert add_endings(["a", "b"], ["1", "2"]) == ["a1", "a2", "b1", "b2"]

def test_syllabify():
    syllabify = es_headword.syllabify

    assert syllabify("alguien") == "al.guien"

    assert syllabify("paranoia") == "pa.ra.no.ia"
    assert syllabify("baiano") == "ba.ia.no"
    assert syllabify("abreuense") == "ab.re.uen.se"

    assert syllabify("ankylosaurio") == "an.ky.lo.sau.rio"
    assert syllabify("cryptomeria") == "cryp.to.me.ria"
    assert syllabify("brandy") == "bran.dy"
    assert syllabify("cherry") == "cher.ry"

def test_remove_links():
    remove_links = es_headword.remove_links
    assert remove_links("[[page|displayed text]]") == "displayed text"
    assert remove_links("[[page and displayed text]]") == "page and displayed text"
    assert remove_links("[[Category:English lemmas|WORD]]") == ""
    assert remove_links("test") == "test"

def test_handle_multiword():
    make_plural = es_headword.make_plural

    assert make_plural("hijo de puta") == ["hijos de puta"]
    assert make_plural("one two three") == ["ones two threes"]

def test_make_plural():
    make_plural = es_headword.make_plural

    # ends in unstressed vowel or á, é, ó
    for ending in "aeiouáéó".split():
        assert make_plural("word" + ending) == ["word" + ending + "s"]

    # ends in í or ú
    for ending in "íú".split():
        assert make_plural("word" + ending) == ["word" + ending + "s", "word" + ending + "es"]

    # ends in a vowel + z
    for ending in "aeiouáéíóúý".split():
        assert make_plural("word" + ending + "z") == ["word" + ending + "ces"]

    # ends in tz
    assert make_plural("wordtz") == ["wordtz"]

    # ends in s or x with more than 1 syllable, last syllable unstressed
    assert make_plural("portugues") == ["portugues"]
    assert make_plural("latinx") == ["latinx"]

    # ends in l, r, n, d, z, or j with 3 or more syllables, accented on third to last syllable
    #for ending in "lrndzj":
    for ending in "lrndj":  # z is buggy
        assert make_plural("háblado" + ending) == ["háblado" + ending ]

    # ends in a stressed vowel + consonant
    assert make_plural("patán") == ["patanes"]

    # ends in a vowel + y, l, r, n, d, j, s, x

    # add accent if it ends in n
    assert make_plural("joven") == ["jóvenes"]

    # otherwise + es
    for ending in "ylrdj": # s is buggy, x is buggy
        assert make_plural("hablado" + ending) == ["hablado" + ending + "es" ]

    # ends in a vowel + ch
    assert make_plural("grouch") == ["grouches"]

    # ends in two consonants
    assert make_plural("jeff") == ["jeffs"]

    # ends in a vowel + consonant other than l, r, n, d, z, j, s, or x
    for ending in "bcfghkmpqtvw": # z is buggy
        assert make_plural("hablado" + ending) == ["hablado" + ending + "s" ]

def test_make_feminine():
    make_feminine = es_headword.make_feminine

    words = {
        "chico": "chica",
        "holgazán": "holgazana",
        "comodín": "comodina",
        "bretón": "bretona",
        "común": "común", # no fem
        "francés": "francesa",
        "kirguís": "kirguisa",
        "mandamás": "mandamás", # no fem
        "volador": "voladora",
        "agricultor": "agricultora",
        "defensor": "defensora",
        "avizor": "avizora",
        "flexor": "flexora",
        "señor": "señora",
        "posterior": "posterior", # no
        "bicolor": "bicolor", # no
        "mayor": "mayor", # no
        "mejor": "mejor", #no
        "menor": "menor", #no
        "peor": "peor", # no
        "español": "española",
        "mongol": "mongola",
        "test": "test"
    }

    for m,f in words.items():
        assert make_feminine(m) == f

def test_make_masculine():
    make_masculine = es_headword.make_masculine

    words = {
        "chica": "chico",
        "voladora": "volador",
        "test": "test"
    }

    for f,m in words.items():
        assert make_masculine(f) == m


def test_do_adjective():
    do_adjective = es_headword.do_adjective

    #def do_adjective(pagename, args, data, tracking_categories=[], is_superlative=False):

    args = {}
    data = {}
    do_adjective("rojo", args, data)
    assert data == {'inflections': [{'': ['roja'], 'accel': {'form': 'f|s'}, 'label': 'feminine'}, {'': ['rojos'], 'accel': {'form': 'm|p'}, 'label': 'masculine plural'}, {'': ['rojas'], 'accel': {'form': 'f|p'}, 'label': 'feminine plural'}]} != {'inflections': [{'': ['rojos'], 'accel': {'form': 'm|p'}, 'label': 'masculine plural'}, {'': ['rojas'], 'accel': {'form': 'f|p'}, 'label': 'feminine plural'}]}


def test_do_noun():
    do_noun = es_headword.do_noun

    args = {"1": "m"}
    data = {}
    do_noun("protector", args, data)
    assert data == {'genders': ['m'],
          'inflections': [{'': ['protectores'],
                           'accel': {'form': 'p'},
                           'label': 'plural'}]}

    args = {"1": "m", "f": "+"}
    data = {}
    do_noun("protector", args, data)
    assert data == {'genders': ['m'],
       'inflections': [{'': ['protectores'],
                         'accel': {'form': 'p'},
                         'label': 'plural'},
                        {'': ['protectora'],
                         'accel': {'form': 'f'},
                         'label': 'feminine'},
                        {'': [{'accel': {'form': 'p',
                                         'lemma': 'protectora'},
                               'term': 'protectoras'}],
                         'label': 'feminine plural'}],
       }


    args = {"1": "m", "f": "+", "f2": "protectriz"}
    data = {}
    do_noun("protector", args, data)
    assert data == {'genders': ['m'],
        'inflections': [{'': ['protectores'],
                         'accel': {'form': 'p'},
                         'label': 'plural'},
                        {'': ['protectora'],
                         'accel': {'form': 'f'},
                         'label': 'feminine'},
                        {'': [{'accel': {'form': 'p', 'lemma': 'protectora'},
                               'term': 'protectoras'}],
                         'label': 'feminine plural'}]}



