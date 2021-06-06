import enwiktionary_templates
import mwparserfromhell

expand_template = enwiktionary_templates.expand_template

def test_es_compound_of():
    template = next(mwparserfromhell.parse("# {{es-compound of|adelgaz|ar|adelgazar|las|mood=inf}}").ifilter_templates())
    assert expand_template(template, "test") == 'compound form of "adelgazar"+"las"'

def test_es_conj():
    template = next(mwparserfromhell.parse("{{es-conj}}").ifilter_templates())
    value = expand_template(template, "tener")
    assert value == "cond_1p=tendríamos; cond_1s=tendría; cond_2p=tendríais; cond_2s=tendrías; cond_3p=tendrían; cond_3s=tendría; fut_1p=tendremos; fut_1s=tendré; fut_2p=tendréis; fut_2s=tendrás; fut_3p=tendrán; fut_3s=tendrá; fut_sub_1p=tuviéremos; fut_sub_1s=tuviere; fut_sub_2p=tuviereis; fut_sub_2s=tuvieres; fut_sub_3p=tuvieren; fut_sub_3s=tuviere; gerund=teniendo; gerund_comb_la=teniéndola; gerund_comb_las=teniéndolas; gerund_comb_le=teniéndole; gerund_comb_les=teniéndoles; gerund_comb_lo=teniéndolo; gerund_comb_los=teniéndolos; gerund_comb_me=teniéndome; gerund_comb_mela=teniéndomela; gerund_comb_melas=teniéndomelas; gerund_comb_mele=teniéndomele; gerund_comb_meles=teniéndomeles; gerund_comb_melo=teniéndomelo; gerund_comb_melos=teniéndomelos; gerund_comb_nos=teniéndonos; gerund_comb_nosla=teniéndonosla; gerund_comb_noslas=teniéndonoslas; gerund_comb_nosle=teniéndonosle; gerund_comb_nosles=teniéndonosles; gerund_comb_noslo=teniéndonoslo; gerund_comb_noslos=teniéndonoslos; gerund_comb_os=teniéndoos; gerund_comb_osla=teniéndoosla; gerund_comb_oslas=teniéndooslas; gerund_comb_osle=teniéndoosle; gerund_comb_osles=teniéndoosles; gerund_comb_oslo=teniéndooslo; gerund_comb_oslos=teniéndooslos; gerund_comb_se=teniéndose; gerund_comb_sela=teniéndosela; gerund_comb_selas=teniéndoselas; gerund_comb_sele=teniéndosele; gerund_comb_seles=teniéndoseles; gerund_comb_selo=teniéndoselo; gerund_comb_selos=teniéndoselos; gerund_comb_te=teniéndote; gerund_comb_tela=teniéndotela; gerund_comb_telas=teniéndotelas; gerund_comb_tele=teniéndotele; gerund_comb_teles=teniéndoteles; gerund_comb_telo=teniéndotelo; gerund_comb_telos=teniéndotelos; imp_1p=tengamos; imp_1p_comb_la=tengámosla; imp_1p_comb_las=tengámoslas; imp_1p_comb_le=tengámosle; imp_1p_comb_les=tengámosles; imp_1p_comb_lo=tengámoslo; imp_1p_comb_los=tengámoslos; imp_1p_comb_nos=tengámonos; imp_1p_comb_nosla=tengámosnosla; imp_1p_comb_noslas=tengámosnoslas; imp_1p_comb_nosle=tengámosnosle; imp_1p_comb_nosles=tengámosnosles; imp_1p_comb_noslo=tengámosnoslo; imp_1p_comb_noslos=tengámosnoslos; imp_1p_comb_os=tengámoos; imp_1p_comb_osla=tengámososla; imp_1p_comb_oslas=tengámososlas; imp_1p_comb_osle=tengámososle; imp_1p_comb_osles=tengámososles; imp_1p_comb_oslo=tengámososlo; imp_1p_comb_oslos=tengámososlos; imp_1p_comb_te=tengámoste; imp_1p_comb_tela=tengámostela; imp_1p_comb_telas=tengámostelas; imp_1p_comb_tele=tengámostele; imp_1p_comb_teles=tengámosteles; imp_1p_comb_telo=tengámostelo; imp_1p_comb_telos=tengámostelos; imp_2p=tened; imp_2p_comb_la=tenedla; imp_2p_comb_las=tenedlas; imp_2p_comb_le=tenedle; imp_2p_comb_les=tenedles; imp_2p_comb_lo=tenedlo; imp_2p_comb_los=tenedlos; imp_2p_comb_me=tenedme; imp_2p_comb_mela=tenedmela; imp_2p_comb_melas=tenedmelas; imp_2p_comb_mele=tenedmele; imp_2p_comb_meles=tenedmeles; imp_2p_comb_melo=tenedmelo; imp_2p_comb_melos=tenedmelos; imp_2p_comb_nos=tenednos; imp_2p_comb_nosla=tenednosla; imp_2p_comb_noslas=tenednoslas; imp_2p_comb_nosle=tenednosle; imp_2p_comb_nosles=tenednosles; imp_2p_comb_noslo=tenednoslo; imp_2p_comb_noslos=tenednoslos; imp_2p_comb_os=teneos; imp_2p_comb_osla=tenedosla; imp_2p_comb_oslas=tenedoslas; imp_2p_comb_osle=tenedosle; imp_2p_comb_osles=tenedosles; imp_2p_comb_oslo=tenedoslo; imp_2p_comb_oslos=tenedoslos; imp_2s=ten; imp_2s_comb_la=tenla; imp_2s_comb_las=tenlas; imp_2s_comb_le=tenle; imp_2s_comb_les=tenles; imp_2s_comb_lo=tenlo; imp_2s_comb_los=tenlos; imp_2s_comb_me=tenme; imp_2s_comb_mela=tenmela; imp_2s_comb_melas=tenmelas; imp_2s_comb_mele=tenmele; imp_2s_comb_meles=tenmeles; imp_2s_comb_melo=tenmelo; imp_2s_comb_melos=tenmelos; imp_2s_comb_nos=tennos; imp_2s_comb_nosla=tennosla; imp_2s_comb_noslas=tennoslas; imp_2s_comb_nosle=tennosle; imp_2s_comb_nosles=tennosles; imp_2s_comb_noslo=tennoslo; imp_2s_comb_noslos=tennoslos; imp_2s_comb_te=tente; imp_2s_comb_tela=tentela; imp_2s_comb_telas=tentelas; imp_2s_comb_tele=tentele; imp_2s_comb_teles=tenteles; imp_2s_comb_telo=tentelo; imp_2s_comb_telos=tentelos; imp_2sv=tené; imp_3p=tengan; imp_3p_comb_la=ténganla; imp_3p_comb_las=ténganlas; imp_3p_comb_le=ténganle; imp_3p_comb_les=ténganles; imp_3p_comb_lo=ténganlo; imp_3p_comb_los=ténganlos; imp_3p_comb_me=ténganme; imp_3p_comb_mela=ténganmela; imp_3p_comb_melas=ténganmelas; imp_3p_comb_mele=ténganmele; imp_3p_comb_meles=ténganmeles; imp_3p_comb_melo=ténganmelo; imp_3p_comb_melos=ténganmelos; imp_3p_comb_nos=téngannos; imp_3p_comb_nosla=téngannosla; imp_3p_comb_noslas=téngannoslas; imp_3p_comb_nosle=téngannosle; imp_3p_comb_nosles=téngannosles; imp_3p_comb_noslo=téngannoslo; imp_3p_comb_noslos=téngannoslos; imp_3p_comb_se=ténganse; imp_3p_comb_sela=téngansela; imp_3p_comb_selas=ténganselas; imp_3p_comb_sele=téngansele; imp_3p_comb_seles=ténganseles; imp_3p_comb_selo=ténganselo; imp_3p_comb_selos=ténganselos; imp_3s=tenga; imp_3s_comb_la=téngala; imp_3s_comb_las=téngalas; imp_3s_comb_le=téngale; imp_3s_comb_les=téngales; imp_3s_comb_lo=téngalo; imp_3s_comb_los=téngalos; imp_3s_comb_me=téngame; imp_3s_comb_mela=téngamela; imp_3s_comb_melas=téngamelas; imp_3s_comb_mele=téngamele; imp_3s_comb_meles=téngameles; imp_3s_comb_melo=téngamelo; imp_3s_comb_melos=téngamelos; imp_3s_comb_nos=ténganos; imp_3s_comb_nosla=ténganosla; imp_3s_comb_noslas=ténganoslas; imp_3s_comb_nosle=ténganosle; imp_3s_comb_nosles=ténganosles; imp_3s_comb_noslo=ténganoslo; imp_3s_comb_noslos=ténganoslos; imp_3s_comb_se=téngase; imp_3s_comb_sela=téngasela; imp_3s_comb_selas=téngaselas; imp_3s_comb_sele=téngasele; imp_3s_comb_seles=téngaseles; imp_3s_comb_selo=téngaselo; imp_3s_comb_selos=téngaselos; impf_1p=teníamos; impf_1s=tenía; impf_2p=teníais; impf_2s=tenías; impf_3p=tenían; impf_3s=tenía; impf_sub_ra_1p=tuviéramos; impf_sub_ra_1s=tuviera; impf_sub_ra_2p=tuvierais; impf_sub_ra_2s=tuvieras; impf_sub_ra_3p=tuvieran; impf_sub_ra_3s=tuviera; impf_sub_se_1p=tuviésemos; impf_sub_se_1s=tuviese; impf_sub_se_2p=tuvieseis; impf_sub_se_2s=tuvieses; impf_sub_se_3p=tuviesen; impf_sub_se_3s=tuviese; infinitive=tener; infinitive_comb_la=tenerla; infinitive_comb_las=tenerlas; infinitive_comb_le=tenerle; infinitive_comb_les=tenerles; infinitive_comb_lo=tenerlo; infinitive_comb_los=tenerlos; infinitive_comb_me=tenerme; infinitive_comb_mela=tenermela; infinitive_comb_melas=tenermelas; infinitive_comb_mele=tenermele; infinitive_comb_meles=tenermeles; infinitive_comb_melo=tenermelo; infinitive_comb_melos=tenermelos; infinitive_comb_nos=tenernos; infinitive_comb_nosla=tenernosla; infinitive_comb_noslas=tenernoslas; infinitive_comb_nosle=tenernosle; infinitive_comb_nosles=tenernosles; infinitive_comb_noslo=tenernoslo; infinitive_comb_noslos=tenernoslos; infinitive_comb_os=teneros; infinitive_comb_osla=tenerosla; infinitive_comb_oslas=teneroslas; infinitive_comb_osle=tenerosle; infinitive_comb_osles=tenerosles; infinitive_comb_oslo=teneroslo; infinitive_comb_oslos=teneroslos; infinitive_comb_se=tenerse; infinitive_comb_sela=tenersela; infinitive_comb_selas=tenerselas; infinitive_comb_sele=tenersele; infinitive_comb_seles=tenerseles; infinitive_comb_selo=tenerselo; infinitive_comb_selos=tenerselos; infinitive_comb_te=tenerte; infinitive_comb_tela=tenertela; infinitive_comb_telas=tenertelas; infinitive_comb_tele=tenertele; infinitive_comb_teles=tenerteles; infinitive_comb_telo=tenertelo; infinitive_comb_telos=tenertelos; infinitive_linked=tener; neg_imp_1p=no tengamos; neg_imp_2p=no tengáis; neg_imp_2s=no tengas; neg_imp_3p=no tengan; neg_imp_3s=no tenga; pp_fp=tenidas; pp_fs=tenida; pp_mp=tenidos; pp_ms=tenido; pres_1p=tenemos; pres_1s=tengo; pres_2p=tenéis; pres_2s=tienes; pres_2sv=tenés; pres_3p=tienen; pres_3s=tiene; pres_sub_1p=tengamos; pres_sub_1s=tenga; pres_sub_2p=tengáis; pres_sub_2s=tengas; pres_sub_2sv=tengás; pres_sub_3p=tengan; pres_sub_3s=tenga; pret_1p=tuvimos; pret_1s=tuve; pret_2p=tuvisteis; pret_2s=tuviste; pret_3p=tuvieron; pret_3s=tuvo"
    assert len(value.split("; ")) == 291

    template = next(mwparserfromhell.parse("{{es-conj}}").ifilter_templates())
    value = expand_template(template, "oír")
    assert len(value.split("; ")) == 291

    template = next(mwparserfromhell.parse("{{es-conj|<ue>}}").ifilter_templates())
    value = expand_template(template, "mostrar")
    #assert len(value.split("; ")) == 291
    print(value)
    assert False


def test_es_noun():
    template = next(mwparserfromhell.parse("{{es-noun|m}}").ifilter_templates())
    assert expand_template(template, "testo") == 'pl=testos'

    template = next(mwparserfromhell.parse("{{es-proper noun|m}}").ifilter_templates())
    assert expand_template(template, "testo") == ''

    template = next(mwparserfromhell.parse("{{es-noun|m|testoz}}").ifilter_templates())
    assert expand_template(template, "testo") == 'pl=testoz'

    template = next(mwparserfromhell.parse("{{es-noun|m|testoz|pl2=+}}").ifilter_templates())
    assert expand_template(template, "testo") == 'pl=testoz; pl=testos'

    template = next(mwparserfromhell.parse("{{es-noun|m|testoz}}").ifilter_templates())
    assert expand_template(template, "testo") == 'pl=testoz'

    template = next(mwparserfromhell.parse("{{es-noun|m|f=testa}}").ifilter_templates())
    assert expand_template(template, "testo") == 'pl=testos; f=testa; fpl=testas'

    template = next(mwparserfromhell.parse("{{es-noun|m|f=1}}").ifilter_templates())
    assert expand_template(template, "testo") == 'pl=testos; f=testa; fpl=testas'

    template = next(mwparserfromhell.parse("{{es-noun|m}}").ifilter_templates())
    assert expand_template(template, "lapiz") == 'pl=lapices'

    template = next(mwparserfromhell.parse("{{es-noun|mf|webcamers|pl2=webcamer}}").ifilter_templates())
    assert expand_template(template, "webcamer") == 'pl=webcamers; pl=webcamer'


def test_es_adj():
    template = next(mwparserfromhell.parse("{{es-adj}}").ifilter_templates())
    assert expand_template(template, "testo") == 'f=testa; pl=testos; fpl=testas'

#    template = next(mwparserfromhell.parse("{{es-adj|f=testa}}").ifilter_templates())
#    assert expand_template(template, "testo") == 'f=testa; fpl=testas; pl=testos'

#    template = next(mwparserfromhell.parse("{{es-adj|f=afecta}}").ifilter_templates())
#    assert expand_template(template, "afecto") == 'f=afecta; fpl=afectas; pl=afectos'




def notest_get_adj_forms():
    # Explicit plural
    word = make_word("testo", "{{es-adj|pl=testoz}}")
    assert Data.get_forms(word) == {"pl":["testoz"]}

    # whitespace
    word = make_word("testo", "{{es-adj|pl= testoz }}")
    assert Data.get_forms(word) == {"pl":["testoz"]}
    word = make_word("testo", "{{es-adj| pl=testoz }}")
    assert Data.get_forms(word) == {"pl":["testoz"]}

    # generate plurals
    word = make_word("testo", "{{es-adj|f=testa}}")
    assert Data.get_forms(word) == {"pl":["testos"], "f":["testa"], "fpl":["testas"]}

    # use specified feminine plural
    word = make_word("testo", "{{es-adj|f=testa|fpl=testaz}}")
    assert Data.get_forms(word) == {"pl":["testos"], "f":["testa"], "fpl":["testaz"]}

    # pl used for pl and fpl
    word = make_word("testo", "{{es-adj|f=testa|pl=testoz}}")
    assert Data.get_forms(word) == {"pl":["testoz"], "f":["testa"], "fpl":["testoz"]}

    # mpl specifies masculine plural
    word = make_word("torpón", "{{es-adj|f=torpona|mpl=torpones}}")
    assert Data.get_forms(word) == {"pl":["torpones"], "f":["torpona"], "fpl":["torponas"]}

    # es-adj-sup works, too
    word = make_word("testo", "{{es-adj-sup|f=testa}}")
    assert Data.get_forms(word) == {"pl":["testos"], "f":["testa"], "fpl":["testas"]}


def notest_get_noun_forms():
    # Explicit plural
    word = make_word("testo", "{{es-noun|m|testoz}}")
    assert Data.get_forms(word) == {"pl":["testoz"]}

    # whitespace
    word = make_word("testo", "{{es-noun|m| testoz }}")
    assert Data.get_forms(word) == {"pl":["testoz"]}

    # Generated plural
    word = make_word("testo", "{{es-noun|m}}")
    assert Data.get_forms(word) == {"pl":["testos"]}

    # Generated plural
    word = make_word("robot", "{{es-noun|m}}")
    assert Data.get_forms(word) == {"pl":["robots"]}

    # No plural
    word = make_word("testo", "{{es-noun|m|-}}")
    assert Data.get_forms(word) == {}

    word = make_word("testa", "{{es-noun|f|testaz}}")
    assert Data.get_forms(word) == {"pl":["testaz"]}

    word = make_word("testa", "{{es-noun|f}}")
    assert Data.get_forms(word) == {"pl":["testas"]}

    word = make_word("testo", "{{es-noun|m|f=testa}}")
    assert Data.get_forms(word) == {"pl":["testos"], "f":["testa"], "fpl":["testas"]}

    word = make_word("testo", "{{es-noun|m|f=1}}")
    assert Data.get_forms(word) == {"pl":["testos"], "f":["testa"], "fpl":["testas"]}

    word = make_word("testo", "{{es-noun|m|f=testa|f2=test2a|f3=test3a}}")
    assert Data.get_forms(word) == {"pl":["testos"], "f":["testa", "test2a", "test3a"], "fpl":["testas", "test2as", "test3as"]}

    word = make_word("testo", "{{es-noun|m|f=testa|f2=test2a|f3=test3a|fpl=testaz}}")
    assert Data.get_forms(word) == {"pl":["testos"], "f":["testa", "test2a", "test3a"], "fpl":["testaz"]}

    word = make_word("testo", "{{es-noun|m|f=testa|f2=test2a|f3=test3a|fpl=testaz|fpl2=test2az}}")
    assert Data.get_forms(word) == {"pl":["testos"], "f":["testa", "test2a", "test3a"], "fpl":["testaz", "test2az"]}

    word = make_word("argentine", "{{es-noun|m|g2=f|m=argentino|f=argentina}}")
    assert Data.get_forms(word) == {"pl":["argentines"], "m":["argentino"], "mpl":["argentinos"], "f":["argentina"], "fpl":["argentinas"]}

def notest_get_verb_forms1():

    data = """\
==Spanish==

===Verb===
{{es-verb|ten|er|pres=tengo|pret=tuve}}

# {{lb|es|transitive}} to [[have]], [[possess]] {{gloss|literally}}

====Conjugation====
{{es-conj-er||p=tener|combined=1}}
"""

    wikt = parse_page(data, "tener", None)
    word = next(wikt.ifilter_words())
    forms = Data.get_forms(word)
    assert forms['1'] == {'tener'}
    assert forms['2'] == {'teniendo'}
    assert forms['inf_acc_1'] == {'tenerme'}
    assert sorted(forms['inf_acc-dat_1']) == sorted(['tenérmelos', 'tenérmela', 'tenérmelas', 'tenérmelo'])

def notest_get_verb_forms_dar():

    data = """\
==Spanish==

===Etymology 1===
From {{der|es|la|attentō}}.

===Verb===
{{es-verb|d|ar|pres=doy|pret=di}}

# {{lb|es|transitive}} to [[give]], to [[give out]]

====Conjugation====
{{es-conj-ar|p=dar|d|combined=1}}
{{es-conj-ar|p=dar|d|combined=1|ref=yes}}
"""

    wikt = parse_page(data, "dar", None)
    word = next(wikt.ifilter_words())
    template = next(word.ifilter_templates(matches=lambda x: "es-verb" in x.name.strip()))
    forms = Data.get_forms(word)
    assert len(forms) == 177

    assert forms["imp_f2s_acc_3"] == {'dela', 'delo', 'dese'}
    assert forms["imp_f2s_acc-dat_3"] == {'déselas', 'désela', 'déselo', 'déselos'}

def notest_get_verb_forms2():

    data = """\
==Spanish==

===Etymology 1===
From {{der|es|la|attentō}}.

====Verb====
{{es-verb|atent|ar|pres=atiento}}

# {{lb|es|intransitive}} to commit a violent or criminal [[attack]], to [[strike]]

===Etymology 2===
{{rfe|es}}

====Verb====
{{es-verb|atent|ar}}

# {{lb|es|transitive|obsolete}} to [[touch]]

===Conjugation===
{{es-conj-ar|at|nt|p=e-ie|combined=1}}
"""

    wikt = parse_page(data, "atentar", None)
    word = next(wikt.ifilter_words())
    template = next(word.ifilter_templates(matches=lambda x: "es-verb" in x.name.strip()))
    forms = Data.get_forms(word)
    assert len(forms) == 180

def notest_get_verb_rogar():

    data = """\
==Spanish==

===Verb===
{{es-verb|rog|ar|pres=ruego|pret=rogué}}

# to [[beg]], [[entreat]], [[implore]], [[pray]]

====Conjugation====
{{es-conj-ar|p=-gar o-ue|r|combined=1}}
"""

    wikt = parse_page(data, "rogar", None)
    word = next(wikt.ifilter_words())
    template = next(word.ifilter_templates(matches=lambda x: "es-verb" in x.name.strip()))
    forms = Data.get_forms(word)

    assert forms["1"] == {"rogar"}


def notest_get_verb_forms_noconjugation():

    data = """\
==Spanish==

===Verb===
{{es-verb|atent|ar|pres=atiento}}

# {{lb|es|intransitive}} to commit a violent or criminal [[attack]], to [[strike]]
"""

    wikt = parse_page(data, "atentar", None)
    word = next(wikt.ifilter_words())
    template = next(word.ifilter_templates(matches=lambda x: "es-verb" in x.name.strip()))
    forms = Data.get_forms(word)
    assert forms == {}


def notest_inflect():
    assert len(Data.inflect(["habl"], "-ar", "", False)) == 73
    assert Data.inflect(["habl"], "-ar", "", False)[1] == ["hablar"]
    assert Data.inflect(["habl"], "-ar", "", True)[1] == ["hablarse"]

def notest_inflect_combined():
    forms = Data.inflect(["habl"], "-ar", "", False)
    combined = Data.inflect_combined(forms, "-ar", "", False)
    assert  combined == {'inf_acc_1': ['hablarme'], 'inf_acc_2': ['hablarte'], 'inf_acc_3': ['hablarlo', 'hablarla', 'hablarse'], 'inf_acc_4': ['hablarnos'], 'inf_acc_5': ['hablaros'], 'inf_acc_6': ['hablarlos', 'hablarlas', 'hablarse'], 'inf_acc_7': ['hablarse'], 'inf_dat_1': ['hablarme'], 'inf_dat_2': ['hablarte'], 'inf_dat_3': ['hablarle', 'hablarse'], 'inf_dat_4': ['hablarnos'], 'inf_dat_5': ['hablaros'], 'inf_dat_6': ['hablarles', 'hablarse'], 'ger_acc_1': ['hablándome'], 'ger_acc_2': ['hablándote'], 'ger_acc_3': ['hablándolo', 'hablándola', 'hablándose'], 'ger_acc_4': ['hablándonos'], 'ger_acc_5': ['hablándoos'], 'ger_acc_6': ['hablándolos', 'hablándolas', 'hablándose'], 'ger_acc_7': ['hablándose'], 'ger_dat_1': ['hablándome'], 'ger_dat_2': ['hablándote'], 'ger_dat_3': ['hablándole', 'hablándose'], 'ger_dat_4': ['hablándonos'], 'ger_dat_5': ['hablándoos'], 'ger_dat_6': ['hablándoles', 'hablándose'], 'imp_i2s_acc_1': ['háblame'], 'imp_i2s_acc_2': ['háblate'], 'imp_i2s_acc_3': ['háblalo', 'háblala'], 'imp_i2s_acc_4': ['háblanos'], 'imp_i2s_acc_6': ['háblalos', 'háblalas'], 'imp_i2s_dat_1': ['háblame'], 'imp_i2s_dat_2': ['háblate'], 'imp_i2s_dat_3': ['háblale'], 'imp_i2s_dat_4': ['háblanos'], 'imp_i2s_dat_6': ['háblales'], 'imp_f2s_acc_1': ['hábleme'], 'imp_f2s_acc_3': ['háblelo', 'háblela', 'háblese'], 'imp_f2s_acc_4': ['háblenos'], 'imp_f2s_acc_6': ['háblelos', 'háblelas'], 'imp_f2s_acc_7': ['háblese'], 'imp_f2s_dat_1': ['hábleme'], 'imp_f2s_dat_3': ['háblele', 'háblese'], 'imp_f2s_dat_4': ['háblenos'], 'imp_f2s_dat_6': ['hábleles'], 'imp_1p_acc_2': ['hablémoste'], 'imp_1p_acc_3': ['hablémoslo', 'hablémosla'], 'imp_1p_acc_4': ['hablémonos'], 'imp_1p_acc_5': ['hablémoos'], 'imp_1p_acc_6': ['hablémoslos', 'hablémoslas'], 'imp_1p_dat_2': ['hablémoste'], 'imp_1p_dat_3': ['hablémosle'], 'imp_1p_dat_4': ['hablémonos'], 'imp_1p_dat_5': ['hablémoos'], 'imp_1p_dat_6': ['hablémosles'], 'imp_i2p_acc_1': ['habladme'], 'imp_i2p_acc_3': ['habladlo', 'habladla'], 'imp_i2p_acc_4': ['habladnos'], 'imp_i2p_acc_5': ['hablaos'], 'imp_i2p_acc_6': ['habladlos', 'habladlas'], 'imp_i2p_acc_7': ['hablados'], 'imp_i2p_dat_1': ['habladme'], 'imp_i2p_dat_3': ['habladle'], 'imp_i2p_dat_4': ['habladnos'], 'imp_i2p_dat_5': ['hablaos'], 'imp_i2p_dat_6': ['habladles'], 'imp_f2p_acc_1': ['háblenme'], 'imp_f2p_acc_3': ['háblenlo', 'háblenla'], 'imp_f2p_acc_4': ['háblennos'], 'imp_f2p_acc_6': ['háblenlos', 'háblenlas', 'háblense'], 'imp_f2p_acc_7': ['háblense'], 'imp_f2p_dat_1': ['háblenme'], 'imp_f2p_dat_3': ['háblenle'], 'imp_f2p_dat_4': ['háblennos'], 'imp_f2p_dat_6': ['háblenles', 'háblense']}

    forms = Data.inflect([], "-ir", "venir", False)
    combined = Data.inflect_combined(forms, "-ir", "venir", False)
    assert combined['imp_i2s_acc_4'] == ['venos']
    assert combined['imp_i2s_dat_4'] == ['venos']
    assert combined['imp_i2p_acc_5'] == ['veníos']
    assert combined['imp_i2p_dat_5'] == ['veníos']

    forms = Data.inflect([], "-ir", "ir", False)
    combined = Data.inflect_combined(forms, "-ir", "ir", False)
    assert combined['imp_i2p_dat_5'] ==  ['idos', 'iros']


def notest_create_accented_form():
    assert Data.create_accented_form("hablame") == "háblame"

    # 'ue' or 'ua' count as 1 vowel, accent goes on e or a
    assert Data.create_accented_form("aburguesele") == "aburguésele"
    assert Data.create_accented_form("malualo") == "málualo"
    # unless ua_disyllabic is set
    assert Data.create_accented_form("malualo",True) == "malúalo"

    # 'ai' or 'oi' counts as 1 vowel, accent goes on a or o
    assert Data.create_accented_form("bailame") == "báilame"
    assert Data.create_accented_form("boilame") == "bóilame"
    assert Data.create_accented_form("beilame") == "beílame"


