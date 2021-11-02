from .es_conj import es_conj
from .es_noun import es_noun
from .es_adj import es_adj, es_adj_sup, es_adj_comp

@staticmethod
def es_compound_of(t,title):
    if t.has(5):
        return f'compound form of "{t.get(1)}{t.get(2)}"+"{t.get(4)}"+"{t.get(5)}"'
    if t.has(4):
        return f'compound form of "{t.get(1)}{t.get(2)}"+"{t.get(4)}"'

    if t.has(2):
        return f'compound form of "{t.get(1)}{t.get(2)}"'

    return ""

@staticmethod
def es_note_noun_common_gender_a(t,title):
    return ""

@staticmethod
def es_note_noun_mf(t,title):
    return ""

@staticmethod
def es_note_noun_f_starting_with_stressed_a(t,title):
    return ""

@staticmethod
def es_proper_noun(t,title):
    return ""

@staticmethod
def es_suffix(t,title):

    forms = []
    for p in ["f", "pl", "fpl"]:
        if t.has(p):
            forms.append(f"{p}={t.get(p).value}")

    if not forms:
        return ""

    return "; ".join(forms)
