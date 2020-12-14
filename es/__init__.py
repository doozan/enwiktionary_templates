from .es_conj import es_conj_ar, es_conj_er, es_conj_ir, es_conj_ír
from .es_noun import es_noun
from .es_adj import es_adj, es_adj_sup

@staticmethod
def es_compound_of(t,title):
    if t.has(5):
        return f'compound form of "{t.get(1)}{t.get(2)}"+"{t.get(4)}"+"{t.get(5)}"'
    if t.has(4):
        return f'compound form of "{t.get(1)}{t.get(2)}"+"{t.get(4)}"'

    if t.has(2):
        return f'compound form of "{t.get(1)}{t.get(2)}"'

    return ""
