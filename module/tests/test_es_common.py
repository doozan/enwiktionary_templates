import enwiktionary_templates.module.es_common as M

def test_syllabify():
    syllabify = M.syllabify

    assert syllabify("alguien") == ["al", "guien"]

    assert syllabify("paranoia") == ["pa", "ra", "no", "ia"]
    assert syllabify("baiano") == ["ba", "ia", "no"]
    assert syllabify("abreuense") == ["a", "bre", "uen", "se"]

    assert syllabify("ankylosaurio") == ["an", "ky", "lo", "sau", "rio"]
    assert syllabify("cryptomeria") == ["cryp", "to", "me", "ria"]
    assert syllabify("brandy") == ["bran", "dy"]
    assert syllabify("cherry") == ["cher", "ry"]

def test_remove_accent_from_syllable():
    assert M.remove_accent_from_syllable("tán") == "tan"
    assert M.remove_accent_from_syllable("tén") == "ten"
    assert M.remove_accent_from_syllable("tín") == "tin"
    assert M.remove_accent_from_syllable("tón") == "ton"
    assert M.remove_accent_from_syllable("tún") == "tun"

    assert M.remove_accent_from_syllable("tan") == "tan"
