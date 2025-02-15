import re
import sys

placetype_aliases = {
    "c": "country",
    "cc": "constituent country",
    "p": "province",
    "ap": "autonomous province",
    "r": "region",
    "ar": "autonomous region",
    "adr": "administrative region",
    "sar": "special administrative region",
    "s": "state",
    "arch": "archipelago",
    "bor": "borough",
    "can": "canton",
    "carea": "council area",
    "cdblock": "community development block",
    "cdep": "Crown dependency",
    "cdp": "census-designated place",
    "CDP": "census-designated place",
    "co": "county",
    "cobor": "county borough",
    "colcity": "county-level city",
    "coll": "collectivity",
    "comm": "community",
    "acomm": "autonomous community",
    "cont": "continent",
    "cpar": "civil parish",
    "dep": "dependency",
    "dept": "department",
    "dist": "district",
    "distmun": "district municipality",
    "div": "division",
    "fpref": "French prefecture",
    "gov": "governorate",
    "govnat": "governorate",
    "ires": "Indian reservation",
    "isl": "island",
    "lbor": "London borough",
    "lgarea": "local government area",
    "lgdist": "local government district",
    "metbor": "metropolitan borough",
    "metcity": "metropolitan city",
    "mtn": "mountain",
    "mun": "municipality",
    "mundist": "municipal district",
    "obl": "oblast",
    "aobl": "autonomous oblast",
    "okr": "okrug",
    "aokr": "autonomous okrug",
    "par": "parish",
    "parmun": "parish municipality",
    "pen": "peninsula",
    "pref": "prefecture",
    "preflcity": "prefecture-level city",
    "apref": "autonomous prefecture",
    "rep": "republic",
    "arep": "autonomous republic",
    "riv": "river",
    "rcomun": "regional county municipality",
    "rdist": "regional district",
    "rmun": "regional municipality",
    "robor": "royal borough",
    "runit": "regional unit",
    "rurmun": "rural municipality",
    "terrauth": "territorial authority",
    "terr": "territory",
    "aterr": "autonomous territory",
    "uterr": "union territory",
    "tjarea": "tribal jurisdictional area",
    "twp": "township",
    "twpmun": "township municipality",
    "utwpmun": "united township municipality",
    "val": "valley",
    "voi": "voivodeship",
    "wcomm": "Welsh community",
    "range": "mountain range",
    "departmental capital": "department capital",
    "home-rule city": "home rule city",
    "home-rule municipality": "home rule municipality",
    "sub-provincial city": "subprovincial city",
    "sub-prefecture-level city": "sub-prefectural city",
    "nonmetropolitan county": "non-metropolitan county",
    "inner-city area": "inner city area",
}
placetype_equivs = {
    "administrative capital": "capital city",
    "administrative center": "administrative centre",
    "administrative headquarters": "administrative centre",
    "administrative seat": "administrative centre",
    "ancient city": "ancient settlement",
    "ancient hamlet": "ancient settlement",
    "ancient town": "ancient settlement",
    "ancient village": "ancient settlement",
    "archipelago": "island",
    "associated province": "province",
    "autonomous territory": "dependent territory",
    "bailiwick": "polity",
    "barangay": "neighborhood", # not completely correct, barangays are formal administrative divisions of a city
    "barrio": "neighborhood", # not completely correct, in some countries barrios are formal administrative divisions of a city
    "bishopric": "polity",
    "built-up area": "area",
    "burgh": "borough",
    "cape": "peninsula",
    "capital": "capital city",
    "caplc": "capital city",
    "caravan city": "city", # should be 'former city' if we distinguish that
    "cathedral city": "city",
    "central business district": "neighborhood",
    "ceremonial county": "county",
    "chain of islands": "island",
    "charter community": "village",
    "commandery": "historical political subdivision",
    "community": "village",
    "comune": "municipality",
    "contregion": "region",
    "county-controlled city": "county-administered city",
    "county-level city": "prefecture-level city",
    "crown dependency": "dependency",
    "Crown dependency": "dependency",
    "department capital": "capital city",
    "deserted mediaeval village": "ancient settlement",
    "deserted medieval village": "ancient settlement",
    "direct-administered municipality": "municipality",
    "direct-controlled municipality": "municipality",
    "distributary": "river",
    "district capital": "capital city",
    "district headquarters": "administrative centre",
    "dormant volcano": "volcano",
    "duchy": "polity",
    "empire": "polity",
    "external territory": "dependent territory",
    "federal territory": "territory",
    "First Nations reserve": "Indian reserve",
    "frazione": "village", # should be "hamlet" but hamlet in turn redirects to village
    "geographical region": "region",
    "glen": "valley",
    "group of islands": "island",
    "hamlet": "village",
    "harbor city": "city",
    "harbour city": "city",
    "harbor town": "town",
    "harbour town": "town",
    "headquarters": "administrative centre",
    "heath": "moor",
    "hill station": "town",
    "hill town": "town",
    # We try to list all top-level polities and political subdivisions here and classify them
    # accordingly. (Note that the following entries also apply to anything preceded by "former",
    # "ancient", "historic", "medieval", etc., according to qualifier_equivs.) Anything we don't
    # list will be categorized as if the qualifier were absent, e.g. "ancient city" will be
    # categorized as a city and "former sea" as a sea.
    "historical autonomous republic": "historical political subdivision",
    "historical autonomous territory": "historical political subdivision",
    "historical borough": "historical political subdivision",
    "historical canton": "historical political subdivision",
    "historical bailiwick": "historical polity",
    "historical barangay": "historical political subdivision",
    "historical bishopric": "historical polity",
    "historical city": "historical settlement",
    "historical civilisation": "historical polity",
    "historical civilization": "historical polity",
    "historical civil parish": "historical political subdivision",
    "historical colony": "historical polity",
    "historical commandery": "historical political subdivision",
    "historical commonwealth": "historical polity",
    "historical commune": "historical political subdivision",
    "historical council area": "historical political subdivision",
    "historical county": "historical political subdivision",
    "historical county borough": "historical political subdivision",
    "historical country": "historical polity",
    "historical crown dependency": "historical polity",
    "historical department": "historical political subdivision",
    "historical dependency": "historical polity",
    "historical district": "historical political subdivision",
    "historical division": "historical political subdivision",
    "historical duchy": "historical polity",
    "historical empire": "historical polity",
    "historical governorate": "historical political subdivision",
    "historical hamlet": "historical settlement",
    "historical kingdom": "historical polity",
    "historical krai": "historical political subdivision",
    "historical maritime republic": "historical polity",
    "historical metropolitan borough": "historical political subdivision",
    "historical municipality": "historical political subdivision",
    "historical oblast": "historical political subdivision",
    "historical okrug": "historical political subdivision",
    "historical parish": "historical political subdivision",
    "historical periphery": "historical political subdivision",
    "historical prefecture": "historical political subdivision",
    "historical province": "historical political subdivision",
    "historical regency": "historical political subdivision",
    "historical regional unit": "historical political subdivision",
    "historical republic": "historical polity",
    "historical satrapy": "historical polity",
    "historical separatist state": "historical polity",
    # The following could refer either to a state of a country (a subdivision)
    # or a state = sovereign entity. The latter appears more common (e.g. in
    # various "ancient states" of East Asia).
    "historical state": "historical polity",
    "historical subdistrict": "historical political subdivision",
    "historical subdivision": "historical political subdivision",
    "historical subprefecture": "historical political subdivision",
    "historical town": "historical settlement",
    "historical village": "historical settlement",
    "historical voivodeship": "historical political subdivision",
    "home rule city": "city",
    "home rule municipality": "municipality",
    "inactive volcano": "volcano",
    "independent city": "city",
    "independent town": "town",
    "inner city area": "neighborhood",
    "island country": "country",
    "island municipality": "municipality",
    "judicial capital": "capital city",
    "kingdom": "polity",
    "legislative capital": "capital city",
    "local authority district": "local government district",
    "local government district with borough status": "local government district",
    "local urban district": "unincorporated community",
    "locality": "village", # not necessarily true, but usually is the case
    "macroregion": "region",
    "market city": "city",
    "market town": "town",
    "mediaeval capital": "ancient capital",
    "medieval capital": "ancient capital",
    "mediaeval city": "ancient settlement",
    "medieval city": "ancient settlement",
    "mediaeval hamlet": "ancient settlement",
    "medieval hamlet": "ancient settlement",
    "mediaeval town": "ancient settlement",
    "medieval town": "ancient settlement",
    "mediaeval village": "ancient settlement",
    "medieval village": "ancient settlement",
    "megacity": "city",
    "metropolitan county": "county",
    "microdistrict": "neighborhood",
    "microstate": "country",
    "minster town": "town",
    "moorland": "moor",
    "mountain indigenous district": "district",
    "mountain indigenous township": "township",
    "mountain range": "mountain",
    "mountainous region": "region",
    "municipality with city status": "municipality",
    "national capital": "capital city",
    "national park": "park",
    "neighbourhood": "neighborhood",
    "new town": "town",
    "non-metropolitan county": "county",
    "non-metropolitan district": "local government district",
    "overseas collectivity": "collectivity",
    "overseas department": "department",
    "overseas territory": "territory",
    "pass": "mountain pass",
    "populated place": "village", # not necessarily true, but usually is the case
    "port city": "city",
    "port town": "town",
    "provincial capital": "capital city",
    "regional capital": "capital city",
    "regional municipality": "municipality",
    "resort city": "city",
    "royal burgh": "borough",
    "royal capital": "capital city",
    "settlement": "village", # not necessarily true, but usually is the case
    "sheading": "district",
    "shire": "county",
    "shire county": "county",
    "shire town": "county seat",
    "spa city": "city",
    "spit": "peninsula",
    "state capital": "capital city",
    "state park": "park",
    "statutory city": "city",
    "statutory town": "town",
    "stream": "river",
    "submerged ghost town": "ghost town",
    "sub-prefectural city": "subprovincial city",
    "suburban area": "suburb",
    "subway station": "metro station",
    "supercontinent": "continent",
    "traditional county": "county",
    "treaty port": "city", # should be 'former city' if we distinguish that
    "territorial authority": "district",
    "underground station": "metro station",
    "unincorporated territory": "territory",
    "unrecognised country": "unrecognized country",
    "urban area": "neighborhood",
    "urban township": "township",
    "urban-type settlement": "town",
    "town with bystatus": "town",
    "tributary": "river",
    "ward": "neighborhood", # not completely correct, wards are formal administrative divisions of a city
}
cat_data = {
    "administrative village": {
        "preposition": "of",
    },

    "administrative centre": {
        "article": "the",
        "preposition": "of",
    },

    "airport": {
    },

    "ancient capital": {
        "article": "the",
        "preposition": "of",
    },

    "ancient settlement": {
    },

    "area": {
    },

    "atoll": {
    },

    "autonomous community": {
        "preposition": "of",

    },

    "autonomous oblast": {
        "preposition": "of",
        "affix_type": "Suf",
        "no_affix_strings": "oblast",
    },

    "autonomous okrug": {
        "preposition": "of",
        "affix_type": "Suf",
        "no_affix_strings": "okrug",
    },

    "autonomous region": {
        "preposition": "of",
    },

    "autonomous republic": {
        "preposition": "of",
    },

    "bay": {
        "preposition": "of",
    },

    "beach": {
    },

    "borough": {
        "preposition": "of",
    },

    "borough seat": {
        "article": "the",
        "preposition": "of",
    },

    "canton": {
        "preposition": "of",
        "affix_type": "suf",
    },

    "capital city": {
        "article": "the",
        "preposition": "of",
    },

    "census area": {
        "affix_type": "Suf",
    },

    "census-designated place": {
    },

    "city": {
        "preposition": "in"
    },

    "city-state": {
    },

    "civil parish": {
        "preposition": "of",
        "affix_type": "suf",
    },

    "collectivity": {
        "preposition": "of",
    },

    "colony": {
        "preposition": "of",

    },

    "commonwealth": {
        "preposition": "of",
    },

    "community development block": {
        "affix_type": "suf",
        "no_affix_strings": "block",
    },

    "constituent country": {
        "preposition": "of",
        "fallback": "country",
    },

    "continent": {
    },

    "council area": {
        "preposition": "of",
        "affix_type": "suf",
    },

    "country": {
    },

    "county": {
        "preposition": "of",
    },

    "county-administered city": {
    },

    "county borough": {
        "preposition": "of",
        "affix_type": "suf",
        "fallback": "borough",
    },

    "county seat": {
        "article": "the",
        "preposition": "of",
    },

    "county town": {
        "article": "the",
        "preposition": "of",
    },

    "department": {
        "preposition": "of",
        "affix_type": "suf",

    },

    "dependency": {
        "preposition": "of",

    },

    "dependent territory": {
        "preposition": "of",

    },

    "desert": {
    },

    "district": {
        "preposition": "of",
        "affix_type": "suf",
    },

    "district municipality": {
        "preposition": "of",
        "affix_type": "suf",
        "no_affix_strings": ["district", "municipality"],
        "fallback": "municipality",
    },

    "division": {
        "preposition": "of",

    },

    "enclave": {
        "preposition": "of",
    },

    "exclave": {
        "preposition": "of",
    },

    "federal city": {
        "preposition": "of",

    },

    "federal subject": {
        "preposition": "of",

    },

    "fictional location": {
    },

    "forest": {
    },

    "French prefecture": {
        "article": "the",
        "preposition": "of",

    },

    "ghost town": {

    },

    "governorate": {
        "preposition": "of",
        "affix_type": "suf",
    },

    "gulf": {
        "preposition": "of",
        "holonym_article": "the",

    },

    "headland": {
    },

    "hill": {
    },

    "historical capital": {
        "article": "the",
        "preposition": "of",
    },

    "historical county": {
        "preposition": "of",
    },

    "historical polity": {
    },

    "historical political subdivision": {
        "preposition": "of",
    },

    "historical region": {
    },

    "historical settlement": {
    },

    "island": {
    },

    "kibbutz": {
        "plural" "kibbutzim",
    },

    "krai": {
        "preposition": "of",
        "affix_type": "Suf",
    },

    "lake": {
    },

    "largest city": {
        "article": "the",
        "fallback": "city",
    },

    "local government district": {
        "preposition": "of",
        "affix_type": "suf",
        "affix": "district",
    },

    "London borough": {
        "preposition": "of",
        "affix_type": "suf",
        "affix": "borough",
        "fallback": "local government district",
    },

    "marginal sea": {
        "preposition": "of",

    },

    "metropolitan borough": {
        "preposition": "of",
        "affix_type": "Pref",
        "no_affix_strings": ["borough", "city"],
        "fallback": "local government district",
    },

    "metropolitan city": {
        "preposition": "of",
        "affix_type": "Pref",
        "no_affix_strings": ["metropolitan", "city"],
        "fallback": "city",
    },

    "moor": {
    },

    "mountain": {
    },

    "mountain pass": {
    },

    "municipal district": {
        "preposition": "of",
        "affix_type": "Pref",
        "no_affix_strings": "district",
        "fallback": "municipality",
    },

    "municipality": {
        "preposition": "of",
    },

    "mythological location": {
    },

    "neighborhood": {
        "preposition": "of",
    },

    "non-city capital": {
        "article": "the",
        "preposition": "of",
    },

    "oblast": {
        "preposition": "of",
        "affix_type": "Suf",
    },

    "ocean": {
        "holonym_article": "the",
    },

    "okrug": {
        "preposition": "of",
        "affix_type": "Suf",
    },

    "parish": {
        "preposition": "of",
        "affix_type": "suf",
    },

    "parish municipality": {
        "preposition": "of",
        "fallback": "municipality",
    },

    "parish seat": {
        "article": "the",
        "preposition": "of",
    },

    "park": {
    },

    "peninsula": {
    },

    "periphery": {
        "preposition": "of",
    },

    "planned community": {
        # Include this empty so we don't categorize 'planned community' into
        # villages, as 'community' does.
    },

    "polity": {
    },

    "prefecture": {
        "preposition": "of",
    },

    "prefecture-level city": {
    },

    "province": {
        "preposition": "of",
    },

    "raion": {
        "preposition": "of",
        "affix_type": "Suf",
    },

    "regency": {
        "preposition": "of",
    },

    "region": {
        "preposition": "of",
    },

    "regional district": {
        "preposition": "of",
        "affix_type": "Pref",
        "no_affix_strings": "district",
        "fallback": "district",

    },

    "regional county municipality": {
        "preposition": "of",
        "affix_type": "Suf",
        "no_affix_strings": ["municipality", "county"],
        "fallback": "municipality",
    },

    "regional municipality": {
        "preposition": "of",
        "affix_type": "Pref",
        "no_affix_strings": "municipality",
        "fallback": "municipality",
    },

    "regional unit": {
        "preposition": "of",
    },

    "republic": {
        "preposition": "of",

    },

    "river": {
        "holonym_article": "the",

    },

    "royal borough": {
        "preposition": "of",
        "affix_type": "Pref",
        "no_affix_strings": ["royal", "borough"],
        "fallback": "local government district",
    },

    "rural municipality": {
        "preposition": "of",
        "affix_type": "Pref",
        "no_affix_strings": "municipality",
        "fallback": "municipality",
    },

    "satrapy": {
        "preposition": "of",
    },

    "sea": {
        "holonym_article": "the",
    },

    "special administrative region": {
        "preposition": "of",
    },

    "star": {
    },

    "state": {
        "preposition": "of",
    },

    "strait": {
    },

    "subdistrict": {
        "preposition": "of",
    },

    "subdivision": {
        "preposition": "of",
        "affix_type": "suf",
    },

    "subprefecture": {
        "preposition": "of",
    },

    "subprovince": {
        "preposition": "of",
    },

    "subprovincial city": {
        # CHINA
    },

    "subregion": {
        "preposition": "of",
    },

    "suburb": {
        "preposition": "of",
    },

    "tehsil": {
        "affix_type": "suf",
        "no_affix_strings": {"tehsil", "tahsil"},
    },

    "territory": {
        "preposition": "of",

    },

    "town": {
    },

    "township": {
    },

    "township municipality": {
        "preposition": "of",
        "fallback": "municipality",
    },

    "traditional region": {
    },

    "tributary": {
        "preposition": "of",
    },

    "unincorporated community": {
    },

    "union territory": {
        "preposition": "of",
        "article": "a",
    },

    "unitary authority": {
        "article": "a",
        "fallback": "local government district",
    },

    "unitary district": {
        "article": "a",
        "fallback": "local government district",
    },

    "united township municipality": {
        "article": "a",
        "fallback": "township municipality",
    },

    "unrecognized country": {
    },

    "valley": {
    },

    "village": {
    },

    "village municipality": {
        "preposition": "of",
    },

    "voivodeship": {
        "preposition": "of",
        "holonym_article": "the",
    },

    "volcano": {
        "plural": "volcanoes",
    },

    "Welsh community": {
        "preposition": "of",
        "affix_type": "suf",
        "affix": "community",
    },
}
placename_uses_the = {
    "archipelago": [
        "Cyclades",
        "Dodecanese",
    ],
    "borough": [
        "Bronx"
    ],
    "country": [
        "Bahamas", 
        "Central African Republic", 
        "Comoros", 
        "Czech Republic", 
        "Democratic Republic of Congo", 
        "Dominican Republic", 
        "Federated States of Micronesia", 
        "Gambia", 
        "Holy Roman Empire",
        "Maldives", 
        "Marshall Islands", 
        "Netherlands", 
        "Philippines", 
        "Republic of Congo", 
        "Solomon Islands", 
        "United Arab Emirates", 
        "United Kingdom", 
#        "United States", 
    ],
    "island": [
        "North Island",
        "South Island",
    ],
    "region": [
        "Balkans",
        "Russian Far East",
        "Caribbean",
        "Caucasus",
        "Middle East",
        "North Caucasus",
        "South Caucasus",
        "West Bank",
    ],
    "valley": [
        "San Fernando Valley"
    ]
}


def res_ends_with(res, endswith):
    """
    res_ends_with(["abc", "def"], "cdef") == True
    res_ends_with(["ab", "cd", "ef"], "bcdef") == True
    res_ends_with(["abc", "def"], "Xdef") == False
    """
    remaining = len(endswith)
    matched = 0
    idx = 1
    while remaining > 0 and idx <= len(res):
        max_match = len(res[-idx]) if len(res[-idx]) < remaining else remaining
        if not res[-idx][-max_match:] == endswith[-max_match:]:
            return False
        else:
            remaining -= max_match
            endswith = endswith[0:-max_match]
        idx += 1

    return remaining == 0

def add_article(res, article, word):
    if not article or not word:
        return

    if res_ends_with(res, f"{article} "):
        return

    if article in "Aa" and word[0] in "aeiouAEIOU":
        # change a to an if it's preceeding a vowel
        article += "n"
    res.append(f"{article} ")

def add_placename(res, placename, placetype, affix_type, article, prep, alt_format, is_text):

    if placename == "and":
        res.append(" and")
        return

    if not alt_format:
        if is_text and not res_ends_with(res, " and"):
            res.append(f", {placename}")
            return

        if prep and not placename.startswith(prep.strip()):
            res.append(prep)
        elif not article:
            res.append(" ")

    prep = None

    cat = cat_data.get(placetype)
    if cat is not None:
        if not affix_type:
            affix_type = cat.get("affix_type")

        if placetype in ["state", "province", "autonomous community"]:
            prep = ", "
        else:
            prep = cat.get("preposition", "in")
            prep = f" {prep} "

    if affix_type == "pref":
        article = add_article(res, article, placetype)
        res.append(placetype)
        res.append(" of ")

    elif affix_type == "Pref":
        article = add_article(res, article, placetype)
        res.append(placetype.capitalize())
        res.append(" of ")

    if placetype in placename_uses_the and placename in placename_uses_the[placetype]:
        article = "the"
    elif cat and "holonym_article" in cat:
        article = cat.get("holonym_article")

    article = add_article(res, article, placename)
    res.append(placename)

    if placename != placetype:
        if affix_type == "suf":
            res.append(" ")
            res.append(placetype)
        elif affix_type == "Suf":
            res.append(" ")
            res.append(placetype.capitalize())
        elif affix_type not in [None, "", "pref", "Pref"]:
            res.append(" ")
            res.append(placetype)
            print("Unhandled affix", affix_type, [res, placename, placetype, affix_type, article, prep, alt_format, is_text], file=sys.stderr)

    return prep

def place(t, title):

    if 2 in t:
        params = []
        val = t[2]
        alt_format = "<<" in val

        if alt_format:
            params = re.split("<<(.*?)>>", t[2])
        else:
            params = [val]
            x = 3
            while x in t:
                params.append(t[x])
                x += 1

        res = []
        t_vals = []
        x = 1
        if "t" in t:
            t_vals.append(t["t"])
            x = 2

        while f"t{x}" in t:
            t_vals.append(t[f"t{x}"])
            x += 1

        if t_vals:
            res.append(", ".join(t_vals))
            res.append(" (")

        article = None
        if not alt_format:
            if "a" in t:
                article = str(t["a"])
            else:
                article = "a" if t_vals else "A"

        prep = None
        for i, param in enumerate(params):

            affix_type = None
            cat = None

            match = re.match("((?P<holonym>[^:/]+)[:]?(?P<affix_type>[^/]*)/)?(?P<value>.*)", param)

            hol = match.group("holonym")
            if hol:
                placetype = hol
                affix_type = match.group("affix_type")
            else:
                placetype = param

            placetype = placetype_aliases.get(placetype, placetype)
            placetype = placetype_equivs.get(placetype, placetype)

            placename = match.group("value")

            if "/" in placename:
                for placename in param.split("/"):

                    if placename.startswith(";"):
                        placename = placename[1:].lstrip()
                        article = "a"
                        prep = None
                        if placename:
                            res.append(placename)
                        continue

                    prep = add_placename(res, placename, placetype, affix_type, article, prep, alt_format, is_text=False)
                    article = None
            else:
                if placename.startswith(";"):
                    placename = placename[1:].lstrip()
                    article = "a"
                    prep = None
                    if placename:
                        res.append(placename)
                else:
                    is_text = hol is None and i > 1
                    prep = add_placename(res, placename, placetype, affix_type, article, prep, alt_format, is_text)

            article = None

        if t_vals:
            res.append(")")

        return "".join(res)

    else:
        return title + " (place)"

