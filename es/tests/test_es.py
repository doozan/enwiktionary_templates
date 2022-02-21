import re
import enwiktionary_templates
import mwparserfromhell

expand_template = enwiktionary_templates.expand_template
expand_templates = enwiktionary_templates.expand_templates

def _expand(text, pagename="test"):
    wikt = mwparserfromhell.parse(text)
    expand_templates(wikt, pagename)
    return str(wikt)

def test_es_compound_of():
    #assert _expand("{{es-compound of|adelgaz|ar|adelgazar|las|mood=inf}}") == 'compound form of "adelgazar"+"las"'
    assert _expand("{{es-compound of|adelgaz|ar|adelgazar|las|mood=inf}}") == 'infinitive_comb_las of "adelgazar"'
    assert _expand("{{es-compound of|adelgaz|ar|adelgazar|se|las|mood=ger}}") == 'gerund_comb_selas of "adelgazar"'

    assert _expand("{{es-compound of|adelgaz|ar|adelgazar|me|las|mood=imp|person=tu}}") == 'imp_2s_comb_melas of "adelgazar"'
    assert _expand("{{es-compound of|adelgaz|ar|adelgazar|me|mood=imp|person=usted}}") == 'imp_2sf_comb_me of "adelgazar"'
    assert _expand("{{es-compound of|adelgaz|ar|adelgazar|me|mood=imp|person=nosotros}}") == 'imp_1p_comb_me of "adelgazar"'
    assert _expand("{{es-compound of|adelgaz|ar|adelgazar|me|mood=imp|person=vosotros}}") == 'imp_2p_comb_me of "adelgazar"'
    assert _expand("{{es-compound of|adelgaz|ar|adelgazar|me|mood=imp|person=ustedes}}") == 'imp_2pf_comb_me of "adelgazar"'

    assert _expand("{{es-compound of|abraz|ar|abraza|los|mood=imperative|person=tú}}") == 'imp_2s_comb_los of "abrazar"'

    assert _expand("{{es-compound of|achaparr|ar|achaparrar|os|mood=inf}}") == 'infinitive_comb_os of "achaparrar"'
    assert _expand("{{es-compound of|achaparr|ar|achaparrar|os|mood=infinitive}}") == 'infinitive_comb_os of "achaparrar"'

    assert _expand("{{es-compound of|achaparr|ar|achaparrando|lo|mood=part}}") == 'gerund_comb_lo of "achaparrar"'
    assert _expand("{{es-compound of|achaparr|ar|achaparrando|lo|mood=gerund}}") == 'gerund_comb_lo of "achaparrar"'
    assert _expand("{{es-compound of|achic|ar|achicar|se|mood=infinitive}}") == 'infinitive_comb_se of "achicar"'


def test_es_conj():

    conj = {x.split("=")[0].strip():x.split("=")[1].strip() for x in _expand("{{es-conj}}", "decir").split(";")}
#    print(conj)
    assert [k for k,v in conj.items() if v=="dime"] == ["imp_2s_comb_me"]
    assert [k for k,v in conj.items() if v=="dímelo"] == ["imp_2s_comb_melo"]


    conj = {x.split("=")[0].strip():x.split("=")[1].strip() for x in _expand("{{es-conj}}", "tener").split(";")}
#    print(conj)
    expected = {'cond_1p': 'tendríamos', 'cond_1s': 'tendría', 'cond_2p': 'tendríais', 'cond_2pf': 'tendrían', 'cond_2s': 'tendrías', 'cond_2sf': 'tendría', 'cond_3p': 'tendrían', 'cond_3s': 'tendría', 'fut_1p': 'tendremos', 'fut_1s': 'tendré', 'fut_2p': 'tendréis', 'fut_2pf': 'tendrán', 'fut_2s': 'tendrás', 'fut_2sf': 'tendrá', 'fut_3p': 'tendrán', 'fut_3s': 'tendrá', 'fut_sub_1p': 'tuviéremos', 'fut_sub_1s': 'tuviere', 'fut_sub_2p': 'tuviereis', 'fut_sub_2pf': 'tuvieren', 'fut_sub_2s': 'tuvieres', 'fut_sub_2sf': 'tuviere', 'fut_sub_3p': 'tuvieren', 'fut_sub_3s': 'tuviere', 'gerund': 'teniendo', 'gerund_comb_la': 'teniéndola', 'gerund_comb_las': 'teniéndolas', 'gerund_comb_le': 'teniéndole', 'gerund_comb_les': 'teniéndoles', 'gerund_comb_lo': 'teniéndolo', 'gerund_comb_los': 'teniéndolos', 'gerund_comb_me': 'teniéndome', 'gerund_comb_mela': 'teniéndomela', 'gerund_comb_melas': 'teniéndomelas', 'gerund_comb_mele': 'teniéndomele', 'gerund_comb_meles': 'teniéndomeles', 'gerund_comb_melo': 'teniéndomelo', 'gerund_comb_melos': 'teniéndomelos', 'gerund_comb_nos': 'teniéndonos', 'gerund_comb_nosla': 'teniéndonosla', 'gerund_comb_noslas': 'teniéndonoslas', 'gerund_comb_nosle': 'teniéndonosle', 'gerund_comb_nosles': 'teniéndonosles', 'gerund_comb_noslo': 'teniéndonoslo', 'gerund_comb_noslos': 'teniéndonoslos', 'gerund_comb_os': 'teniéndoos', 'gerund_comb_osla': 'teniéndoosla', 'gerund_comb_oslas': 'teniéndooslas', 'gerund_comb_osle': 'teniéndoosle', 'gerund_comb_osles': 'teniéndoosles', 'gerund_comb_oslo': 'teniéndooslo', 'gerund_comb_oslos': 'teniéndooslos', 'gerund_comb_se': 'teniéndose', 'gerund_comb_sela': 'teniéndosela', 'gerund_comb_selas': 'teniéndoselas', 'gerund_comb_sele': 'teniéndosele', 'gerund_comb_seles': 'teniéndoseles', 'gerund_comb_selo': 'teniéndoselo', 'gerund_comb_selos': 'teniéndoselos', 'gerund_comb_te': 'teniéndote', 'gerund_comb_tela': 'teniéndotela', 'gerund_comb_telas': 'teniéndotelas', 'gerund_comb_tele': 'teniéndotele', 'gerund_comb_teles': 'teniéndoteles', 'gerund_comb_telo': 'teniéndotelo', 'gerund_comb_telos': 'teniéndotelos', 'imp_1p': 'tengamos', 'imp_1p_comb_la': 'tengámosla', 'imp_1p_comb_las': 'tengámoslas', 'imp_1p_comb_le': 'tengámosle', 'imp_1p_comb_les': 'tengámosles', 'imp_1p_comb_lo': 'tengámoslo', 'imp_1p_comb_los': 'tengámoslos', 'imp_1p_comb_nos': 'tengámonos', 'imp_1p_comb_nosla': 'tengámosnosla', 'imp_1p_comb_noslas': 'tengámosnoslas', 'imp_1p_comb_nosle': 'tengámosnosle', 'imp_1p_comb_nosles': 'tengámosnosles', 'imp_1p_comb_noslo': 'tengámosnoslo', 'imp_1p_comb_noslos': 'tengámosnoslos', 'imp_1p_comb_os': 'tengámoos', 'imp_1p_comb_osla': 'tengámososla', 'imp_1p_comb_oslas': 'tengámososlas', 'imp_1p_comb_osle': 'tengámososle', 'imp_1p_comb_osles': 'tengámososles', 'imp_1p_comb_oslo': 'tengámososlo', 'imp_1p_comb_oslos': 'tengámososlos', 'imp_1p_comb_te': 'tengámoste', 'imp_1p_comb_tela': 'tengámostela', 'imp_1p_comb_telas': 'tengámostelas', 'imp_1p_comb_tele': 'tengámostele', 'imp_1p_comb_teles': 'tengámosteles', 'imp_1p_comb_telo': 'tengámostelo', 'imp_1p_comb_telos': 'tengámostelos', 'imp_2p': 'tened', 'imp_2p_comb_la': 'tenedla', 'imp_2p_comb_las': 'tenedlas', 'imp_2p_comb_le': 'tenedle', 'imp_2p_comb_les': 'tenedles', 'imp_2p_comb_lo': 'tenedlo', 'imp_2p_comb_los': 'tenedlos', 'imp_2p_comb_me': 'tenedme', 'imp_2p_comb_mela': 'tenédmela', 'imp_2p_comb_melas': 'tenédmelas', 'imp_2p_comb_mele': 'tenédmele', 'imp_2p_comb_meles': 'tenédmeles', 'imp_2p_comb_melo': 'tenédmelo', 'imp_2p_comb_melos': 'tenédmelos', 'imp_2p_comb_nos': 'tenednos', 'imp_2p_comb_nosla': 'tenédnosla', 'imp_2p_comb_noslas': 'tenédnoslas', 'imp_2p_comb_nosle': 'tenédnosle', 'imp_2p_comb_nosles': 'tenédnosles', 'imp_2p_comb_noslo': 'tenédnoslo', 'imp_2p_comb_noslos': 'tenédnoslos', 'imp_2p_comb_os': 'teneos', 'imp_2p_comb_osla': 'tenédosla', 'imp_2p_comb_oslas': 'tenédoslas', 'imp_2p_comb_osle': 'tenédosle', 'imp_2p_comb_osles': 'tenédosles', 'imp_2p_comb_oslo': 'tenédoslo', 'imp_2p_comb_oslos': 'tenédoslos', 'imp_2pf': 'tengan', 'imp_2pf_comb_la': 'ténganla', 'imp_2pf_comb_las': 'ténganlas', 'imp_2pf_comb_le': 'ténganle', 'imp_2pf_comb_les': 'ténganles', 'imp_2pf_comb_lo': 'ténganlo', 'imp_2pf_comb_los': 'ténganlos', 'imp_2pf_comb_me': 'ténganme', 'imp_2pf_comb_mela': 'ténganmela', 'imp_2pf_comb_melas': 'ténganmelas', 'imp_2pf_comb_mele': 'ténganmele', 'imp_2pf_comb_meles': 'ténganmeles', 'imp_2pf_comb_melo': 'ténganmelo', 'imp_2pf_comb_melos': 'ténganmelos', 'imp_2pf_comb_nos': 'téngannos', 'imp_2pf_comb_nosla': 'téngannosla', 'imp_2pf_comb_noslas': 'téngannoslas', 'imp_2pf_comb_nosle': 'téngannosle', 'imp_2pf_comb_nosles': 'téngannosles', 'imp_2pf_comb_noslo': 'téngannoslo', 'imp_2pf_comb_noslos': 'téngannoslos', 'imp_2pf_comb_se': 'ténganse', 'imp_2pf_comb_sela': 'téngansela', 'imp_2pf_comb_selas': 'ténganselas', 'imp_2pf_comb_sele': 'téngansele', 'imp_2pf_comb_seles': 'ténganseles', 'imp_2pf_comb_selo': 'ténganselo', 'imp_2pf_comb_selos': 'ténganselos', 'imp_2s': 'ten', 'imp_2s_comb_la': 'tenla', 'imp_2s_comb_las': 'tenlas', 'imp_2s_comb_le': 'tenle', 'imp_2s_comb_les': 'tenles', 'imp_2s_comb_lo': 'tenlo', 'imp_2s_comb_los': 'tenlos', 'imp_2s_comb_me': 'tenme', 'imp_2s_comb_mela': 'ténmela', 'imp_2s_comb_melas': 'ténmelas', 'imp_2s_comb_mele': 'ténmele', 'imp_2s_comb_meles': 'ténmeles', 'imp_2s_comb_melo': 'ténmelo', 'imp_2s_comb_melos': 'ténmelos', 'imp_2s_comb_nos': 'tennos', 'imp_2s_comb_nosla': 'ténnosla', 'imp_2s_comb_noslas': 'ténnoslas', 'imp_2s_comb_nosle': 'ténnosle', 'imp_2s_comb_nosles': 'ténnosles', 'imp_2s_comb_noslo': 'ténnoslo', 'imp_2s_comb_noslos': 'ténnoslos', 'imp_2s_comb_te': 'tente', 'imp_2s_comb_tela': 'téntela', 'imp_2s_comb_telas': 'téntelas', 'imp_2s_comb_tele': 'téntele', 'imp_2s_comb_teles': 'ténteles', 'imp_2s_comb_telo': 'téntelo', 'imp_2s_comb_telos': 'téntelos', 'imp_2sf': 'tenga', 'imp_2sf_comb_la': 'téngala', 'imp_2sf_comb_las': 'téngalas', 'imp_2sf_comb_le': 'téngale', 'imp_2sf_comb_les': 'téngales', 'imp_2sf_comb_lo': 'téngalo', 'imp_2sf_comb_los': 'téngalos', 'imp_2sf_comb_me': 'téngame', 'imp_2sf_comb_mela': 'téngamela', 'imp_2sf_comb_melas': 'téngamelas', 'imp_2sf_comb_mele': 'téngamele', 'imp_2sf_comb_meles': 'téngameles', 'imp_2sf_comb_melo': 'téngamelo', 'imp_2sf_comb_melos': 'téngamelos', 'imp_2sf_comb_nos': 'ténganos', 'imp_2sf_comb_nosla': 'ténganosla', 'imp_2sf_comb_noslas': 'ténganoslas', 'imp_2sf_comb_nosle': 'ténganosle', 'imp_2sf_comb_nosles': 'ténganosles', 'imp_2sf_comb_noslo': 'ténganoslo', 'imp_2sf_comb_noslos': 'ténganoslos', 'imp_2sf_comb_se': 'téngase', 'imp_2sf_comb_sela': 'téngasela', 'imp_2sf_comb_selas': 'téngaselas', 'imp_2sf_comb_sele': 'téngasele', 'imp_2sf_comb_seles': 'téngaseles', 'imp_2sf_comb_selo': 'téngaselo', 'imp_2sf_comb_selos': 'téngaselos', 'imp_2sv': 'tené', 'impf_1p': 'teníamos', 'impf_1s': 'tenía', 'impf_2p': 'teníais', 'impf_2pf': 'tenían', 'impf_2s': 'tenías', 'impf_2sf': 'tenía', 'impf_3p': 'tenían', 'impf_3s': 'tenía', 'impf_sub_ra_1p': 'tuviéramos', 'impf_sub_ra_1s': 'tuviera', 'impf_sub_ra_2p': 'tuvierais', 'impf_sub_ra_2pf': 'tuvieran', 'impf_sub_ra_2s': 'tuvieras', 'impf_sub_ra_2sf': 'tuviera', 'impf_sub_ra_3p': 'tuvieran', 'impf_sub_ra_3s': 'tuviera', 'impf_sub_se_1p': 'tuviésemos', 'impf_sub_se_1s': 'tuviese', 'impf_sub_se_2p': 'tuvieseis', 'impf_sub_se_2pf': 'tuviesen', 'impf_sub_se_2s': 'tuvieses', 'impf_sub_se_2sf': 'tuviese', 'impf_sub_se_3p': 'tuviesen', 'impf_sub_se_3s': 'tuviese', 'infinitive': 'tener', 'infinitive_comb_la': 'tenerla', 'infinitive_comb_las': 'tenerlas', 'infinitive_comb_le': 'tenerle', 'infinitive_comb_les': 'tenerles', 'infinitive_comb_lo': 'tenerlo', 'infinitive_comb_los': 'tenerlos', 'infinitive_comb_me': 'tenerme', 'infinitive_comb_mela': 'tenérmela', 'infinitive_comb_melas': 'tenérmelas', 'infinitive_comb_mele': 'tenérmele', 'infinitive_comb_meles': 'tenérmeles', 'infinitive_comb_melo': 'tenérmelo', 'infinitive_comb_melos': 'tenérmelos', 'infinitive_comb_nos': 'tenernos', 'infinitive_comb_nosla': 'tenérnosla', 'infinitive_comb_noslas': 'tenérnoslas', 'infinitive_comb_nosle': 'tenérnosle', 'infinitive_comb_nosles': 'tenérnosles', 'infinitive_comb_noslo': 'tenérnoslo', 'infinitive_comb_noslos': 'tenérnoslos', 'infinitive_comb_os': 'teneros', 'infinitive_comb_osla': 'tenérosla', 'infinitive_comb_oslas': 'tenéroslas', 'infinitive_comb_osle': 'tenérosle', 'infinitive_comb_osles': 'tenérosles', 'infinitive_comb_oslo': 'tenéroslo', 'infinitive_comb_oslos': 'tenéroslos', 'infinitive_comb_se': 'tenerse', 'infinitive_comb_sela': 'tenérsela', 'infinitive_comb_selas': 'tenérselas', 'infinitive_comb_sele': 'tenérsele', 'infinitive_comb_seles': 'tenérseles', 'infinitive_comb_selo': 'tenérselo', 'infinitive_comb_selos': 'tenérselos', 'infinitive_comb_te': 'tenerte', 'infinitive_comb_tela': 'tenértela', 'infinitive_comb_telas': 'tenértelas', 'infinitive_comb_tele': 'tenértele', 'infinitive_comb_teles': 'tenérteles', 'infinitive_comb_telo': 'tenértelo', 'infinitive_comb_telos': 'tenértelos', 'infinitive_linked': 'tener', 'neg_imp_1p': 'no tengamos', 'neg_imp_2p': 'no tengáis', 'neg_imp_2pf': 'no tengan', 'neg_imp_2s': 'no tengas', 'neg_imp_2sf': 'no tenga', 'pp_fp': 'tenidas', 'pp_fs': 'tenida', 'pp_mp': 'tenidos', 'pp_ms': 'tenido', 'pres_1p': 'tenemos', 'pres_1s': 'tengo', 'pres_2p': 'tenéis', 'pres_2pf': 'tienen', 'pres_2s': 'tienes', 'pres_2sf': 'tiene', 'pres_2sv': 'tenés', 'pres_3p': 'tienen', 'pres_3s': 'tiene', 'pres_sub_1p': 'tengamos', 'pres_sub_1s': 'tenga', 'pres_sub_2p': 'tengáis', 'pres_sub_2pf': 'tengan', 'pres_sub_2s': 'tengas', 'pres_sub_2sf': 'tenga', 'pres_sub_2sv': 'tengás', 'pres_sub_3p': 'tengan', 'pres_sub_3s': 'tenga', 'pret_1p': 'tuvimos', 'pret_1s': 'tuve', 'pret_2p': 'tuvisteis', 'pret_2pf': 'tuvieron', 'pret_2s': 'tuviste', 'pret_2sf': 'tuvo', 'pret_3p': 'tuvieron', 'pret_3s': 'tuvo'}
    assert conj == expected

    assert len(conj) == 309

    template = next(mwparserfromhell.parse("{{es-conj}}").ifilter_templates())
    value = expand_template(template, "oír")
    assert len(value.split("; ")) == 309

    template = next(mwparserfromhell.parse("{{es-conj|<ue>}}").ifilter_templates())
    value = expand_template(template, "mostrar")

    template = next(mwparserfromhell.parse("{{es-conj}}").ifilter_templates())
    value = expand_template(template, "ir")
    assert "," not in value

    conj = {x.split("=")[0].strip():x.split("=")[1].strip() for x in _expand("{{es-conj}}", "decir").split(";")}
    assert [k for k,v in conj.items() if v=="dime"] == ["imp_2s_comb_me"]
#    assert [k for k,v in conj.items() if v=="dímelo"] == ["imp_2s_comb_melo"]

    conj = {x.split("=")[0].strip():x.split("=")[1].strip() for x in _expand("{{es-conj}}", "hacer").split(";")}
    assert [k for k,v in conj.items() if v=="házmelo"] == ["imp_2s_comb_melo"]

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

    template = next(mwparserfromhell.parse("{{es-noun|f|m=divo}}").ifilter_templates())
    assert expand_template(template, "diva") == 'pl=divas; m=divo; mpl=divos'

    template = next(mwparserfromhell.parse("{{es-noun|m}}").ifilter_templates())
    assert expand_template(template, "lapiz") == 'pl=lapices'

    template = next(mwparserfromhell.parse("{{es-noun|mf|webcamers|pl2=webcamer}}").ifilter_templates())
    assert expand_template(template, "webcamer") == 'pl=webcamers; pl=webcamer'

    template = next(mwparserfromhell.parse("{{es-noun|m|f=cordera|fpl=corderas}}").ifilter_templates())
    assert expand_template(template, "cordero") == 'pl=corderos; f=cordera; fpl=corderas'

    template = next(mwparserfromhell.parse("{{es-noun|m}}").ifilter_templates())
    assert expand_template(template, "agujero negro supermasivo") == 'pl=agujeros negro supermasivos'

    template = next(mwparserfromhell.parse("{{es-noun|m|+each}}").ifilter_templates())
    assert expand_template(template, "agujero negro supermasivo") == 'pl=agujeros negros supermasivos'





def test_es_adj():
    template = next(mwparserfromhell.parse("{{es-adj}}").ifilter_templates())
    assert expand_template(template, "testo") == 'f=testa; pl=testos; fpl=testas'

    template = next(mwparserfromhell.parse("{{es-adj|f=obturatriz|f2=obturadora}}").ifilter_templates())
    assert expand_template(template, "obturador") == 'f=obturatriz; f=obturadora; pl=obturadores; fpl=obturatrices; fpl=obturadoras'

    template = next(mwparserfromhell.parse("{{es-adj-comp|f=obturatriz|f2=obturadora}}").ifilter_templates())
    assert expand_template(template, "obturador") == 'f=obturatriz; f=obturadora; pl=obturadores; fpl=obturatrices; fpl=obturadoras'


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



def test_es_suffix():
    template = next(mwparserfromhell.parse("{{es-suffix|m|f=-ita}}").ifilter_templates())
    assert expand_template(template, "-ito") == 'f=-ita'



def test_es_verb_form_of():

    test = [ #{
('ten', 'imp_2s', '{{es-verb form of|mood=imp|num=s|pers=2|formal=n|sense=+|ending=er|tener}}'),
('tenemos', 'pres_1p', '{{es-verb form of|mood=ind|tense=pres|num=p|pers=1|ending=er|tener}}'),
('tené', 'imp_2sv', '{{es-verb form of|tener|ending=-er|mood=imperative|number=s|person=2|formal=n|sense=affirmative|voseo=y|region=Latin America}}'),
('tuvo', 'pret_3s', '{{es-verb form of|mood=ind|tense=pret|num=s|pers=3|ending=er|tener}}'),
('tengo', 'pres_1s', '{{es-verb form of|mood=ind|tense=pres|num=s|pers=1|ending=er|tener}}'),
('tenido', 'pp_ms', '{{es-verb form of|mood=par|gen=m|num=s|ending=er|tener}}'),
('tienes', 'pres_2s', '{{es-verb form of|mood=ind|tense=pres|num=s|pers=2|formal=n|ending=er|tener}}'),
('tiene', 'pres_2sf', '{{es-verb form of|mood=ind|tense=pres|num=s|pers=2|formal=y|ending=er|tener}}'),
('tiene', 'pres_3s', '{{es-verb form of|mood=ind|tense=pres|num=s|pers=3|ending=er|tener}}'),
('tienen', 'pres_2pf', '{{es-verb form of|mood=ind|tense=pres|num=p|pers=2|formal=y|ending=er|tener}}'),
('tienen', 'pres_3p', '{{es-verb form of|mood=ind|tense=pres|num=p|pers=3|ending=er|tener}}'),
('tenga', 'pres_sub_1s', '{{es-verb form of|mood=subj|tense=pres|num=s|pers=1|ending=er|tener}}'),
('tenga', 'pres_sub_2sf', '{{es-verb form of|mood=subj|tense=pres|num=s|pers=2|formal=y|ending=er|tener}}'),
('tenga', 'pres_sub_3s', '{{es-verb form of|mood=subj|tense=pres|num=s|pers=3|ending=er|tener}}'),
('tenga', 'imp_2sf', '{{es-verb form of|mood=imp|num=s|pers=2|formal=y|ending=er|tener}}'),
('tenía', 'impf_1s', '{{es-verb form of|mood=ind|tense=imp|num=s|pers=1|ending=er|tener}}'),
('tenía', 'impf_2sf', '{{es-verb form of|mood=ind|tense=imp|num=s|pers=2|formal=y|ending=er|tener}}'),
('tenía', 'impf_3s', '{{es-verb form of|mood=ind|tense=imp|num=s|pers=3|ending=er|tener}}'),
('tenéis', 'pres_2p', '{{es-verb form of|mood=ind|tense=pres|num=p|pers=2|formal=n|ending=er|tener}}'),
('tenías', 'impf_2s', '{{es-verb form of|mood=ind|tense=imp|num=s|pers=2|formal=n|ending=er|tener}}'),
('teníamos', 'impf_1p', '{{es-verb form of|mood=ind|tense=imp|num=p|pers=1|ending=er|tener}}'),
('teníais', 'impf_2p', '{{es-verb form of|mood=ind|tense=imp|num=p|pers=2|formal=n|ending=er|tener}}'),
('tenían', 'impf_2pf', '{{es-verb form of|mood=ind|tense=imp|num=p|pers=2|formal=y|ending=er|tener}}'),
('tenían', 'impf_3p', '{{es-verb form of|mood=ind|tense=imp|num=p|pers=3|ending=er|tener}}'),
('tuve', 'pret_1s', '{{es-verb form of|mood=ind|tense=pret|num=s|pers=1|ending=er|tener}}'),
('tuviste', 'pret_2s', '{{es-verb form of|mood=ind|tense=pret|num=s|pers=2|formal=n|ending=er|tener}}'),
('tuvimos', 'pret_1p', '{{es-verb form of|mood=ind|tense=pret|num=p|pers=1|ending=er|tener}}'),
('tuvisteis', 'pret_2p', '{{es-verb form of|mood=ind|tense=pret|num=p|pers=2|formal=n|ending=er|tener}}'),
('tuvieron', 'pret_2pf', '{{es-verb form of|mood=ind|tense=pret|num=p|pers=2|formal=y|ending=er|tener}}'),
('tuvieron', 'pret_3p', '{{es-verb form of|mood=ind|tense=pret|num=p|pers=3|ending=er|tener}}'),
('tendré', 'fut_1s', '{{es-verb form of|mood=ind|tense=fut|num=s|pers=1|ending=er|tener}}'),
('tendrás', 'fut_2s', '{{es-verb form of|mood=ind|tense=fut|num=s|pers=2|formal=n|ending=er|tener}}'),
('tendrá', 'fut_2sf', '{{es-verb form of|mood=ind|tense=fut|num=s|pers=2|formal=y|ending=er|tener}}'),
('tendrá', 'fut_3s', '{{es-verb form of|mood=ind|tense=fut|num=s|pers=3|ending=er|tener}}'),
('tendremos', 'fut_1p', '{{es-verb form of|mood=ind|tense=fut|num=p|pers=1|ending=er|tener}}'),
('tendréis', 'fut_2p', '{{es-verb form of|mood=ind|tense=fut|num=p|pers=2|formal=n|ending=er|tener}}'),
('tendrán', 'fut_2pf', '{{es-verb form of|mood=ind|tense=fut|num=p|pers=2|formal=y|ending=er|tener}}'),
('tendrán', 'fut_3p', '{{es-verb form of|mood=ind|tense=fut|num=p|pers=3|ending=er|tener}}'),
('tendría', 'cond_1s', '{{es-verb form of|mood=ind|tense=cond|num=s|pers=1|ending=er|tener}}'),
('tendría', 'cond_2sf', '{{es-verb form of|mood=ind|tense=cond|num=s|pers=2|formal=y|ending=er|tener}}'),
('tendría', 'cond_3s', '{{es-verb form of|mood=ind|tense=cond|num=s|pers=3|ending=er|tener}}'),
('tendrías', 'cond_2s', '{{es-verb form of|mood=ind|tense=cond|num=s|pers=2|formal=n|ending=er|tener}}'),
('tendríamos', 'cond_1p', '{{es-verb form of|mood=ind|tense=cond|num=p|pers=1|ending=er|tener}}'),
('tendríais', 'cond_2p', '{{es-verb form of|mood=ind|tense=cond|num=p|pers=2|formal=n|ending=er|tener}}'),
('tendrían', 'cond_2pf', '{{es-verb form of|mood=ind|tense=cond|num=p|pers=2|formal=y|ending=er|tener}}'),
('tendrían', 'cond_3p', '{{es-verb form of|mood=ind|tense=cond|num=p|pers=3|ending=er|tener}}'),
('tengas', 'pres_sub_2s', '{{es-verb form of|mood=subj|tense=pres|num=s|pers=2|formal=n|ending=er|tener}}'),
('tengas', 'neg_imp_2s', '{{es-verb form of|mood=imp|num=s|pers=2|formal=n|sense=-|ending=er|tener}}'),
('tengamos', 'pres_sub_1p', '{{es-verb form of|mood=subj|tense=pres|num=p|pers=1|ending=er|tener}}'),
('tengamos', 'imp_1p', '{{es-verb form of|mood=imp|num=p|pers=1|ending=er|tener}}'),
('tengáis', 'pres_sub_2p', '{{es-verb form of|mood=subj|tense=pres|num=p|pers=2|formal=n|ending=er|tener}}'),
('tengáis', 'neg_imp_2p', '{{es-verb form of|mood=imp|num=p|pers=2|formal=n|sense=-|ending=er|tener}}'),
('tengan', 'pres_sub_2pf', '{{es-verb form of|mood=subj|tense=pres|num=p|pers=2|formal=y|ending=er|tener}}'),
('tengan', 'pres_sub_3p', '{{es-verb form of|mood=subj|tense=pres|num=p|pers=3|ending=er|tener}}'),
('tengan', 'imp_2pf', '{{es-verb form of|mood=imp|num=p|pers=2|formal=y|ending=er|tener}}'),
('tuviera', 'impf_sub_ra_1s', '{{es-verb form of|mood=subj|tense=imp|sera=ra|num=s|pers=1|ending=er|tener}}'),
('tuviera', 'impf_sub_ra_2sf', '{{es-verb form of|mood=subj|tense=imp|sera=ra|num=s|pers=2|formal=y|ending=er|tener}}'),
('tuviera', 'impf_sub_ra_3s', '{{es-verb form of|mood=subj|tense=imp|sera=ra|num=s|pers=3|ending=er|tener}}'),
('tuvieras', 'impf_sub_ra_2s', '{{es-verb form of|mood=subj|tense=imp|sera=ra|num=s|pers=2|formal=n|ending=er|tener}}'),
('tuviéramos', 'impf_sub_ra_1p', '{{es-verb form of|mood=subj|tense=imp|sera=ra|num=p|pers=1|ending=er|tener}}'),
('tuvierais', 'impf_sub_ra_2p', '{{es-verb form of|mood=subj|tense=imp|sera=ra|num=p|pers=2|formal=n|ending=er|tener}}'),
('tuvieran', 'impf_sub_ra_2pf', '{{es-verb form of|mood=subj|tense=imp|sera=ra|num=p|pers=2|formal=y|ending=er|tener}}'),
('tuvieran', 'impf_sub_ra_3p', '{{es-verb form of|mood=subj|tense=imp|sera=ra|num=p|pers=3|ending=er|tener}}'),
('tuviese', 'impf_sub_se_1s', '{{es-verb form of|mood=subj|tense=imp|sera=se|num=s|pers=1|ending=er|tener}}'),
('tuviese', 'impf_sub_se_2sf', '{{es-verb form of|mood=subj|tense=imp|sera=se|num=s|pers=2|formal=y|ending=er|tener}}'),
('tuviese', 'impf_sub_se_3s', '{{es-verb form of|mood=subj|tense=imp|sera=se|num=s|pers=3|ending=er|tener}}'),
('tuvieses', 'impf_sub_se_2s', '{{es-verb form of|mood=subj|tense=imp|sera=se|num=s|pers=2|formal=n|ending=er|tener}}'),
('tuviésemos', 'impf_sub_se_1p', '{{es-verb form of|mood=subj|tense=imp|sera=se|num=p|pers=1|ending=er|tener}}'),
('tuvieseis', 'impf_sub_se_2p', '{{es-verb form of|mood=subj|tense=imp|sera=se|num=p|pers=2|formal=n|ending=er|tener}}'),
('tuviesen', 'impf_sub_se_2pf', '{{es-verb form of|mood=subj|tense=imp|sera=se|num=p|pers=2|formal=y|ending=er|tener}}'),
('tuviesen', 'impf_sub_se_3p', '{{es-verb form of|mood=subj|tense=imp|sera=se|num=p|pers=3|ending=er|tener}}'),
('tuviere', 'fut_sub_1s', '{{es-verb form of|mood=subj|tense=fut|num=s|pers=1|ending=er|tener}}'),
('tuviere', 'fut_sub_2sf', '{{es-verb form of|mood=subj|tense=fut|num=s|pers=2|formal=y|ending=er|tener}}'),
('tuviere', 'fut_sub_3s', '{{es-verb form of|mood=subj|tense=fut|num=s|pers=3|ending=er|tener}}'),
('tuvieres', 'fut_sub_2s', '{{es-verb form of|mood=subj|tense=fut|num=s|pers=2|formal=n|ending=er|tener}}'),
('tuviéremos', 'fut_sub_1p', '{{es-verb form of|mood=subj|tense=fut|num=p|pers=1|ending=er|tener}}'),
('tuviereis', 'fut_sub_2p', '{{es-verb form of|mood=subj|tense=fut|num=p|pers=2|formal=n|ending=er|tener}}'),
('tuvieren', 'fut_sub_2pf', '{{es-verb form of|mood=subj|tense=fut|num=p|pers=2|formal=y|ending=er|tener}}'),
('tuvieren', 'fut_sub_3p', '{{es-verb form of|mood=subj|tense=fut|num=p|pers=3|ending=er|tener}}'),
('tened', 'imp_2p', '{{es-verb form of|mood=imp|num=p|pers=2|formal=n|sense=+|ending=er|tener}}'),
('teniendo', 'gerund', '{{es-verb form of|mood=ger|ending=er|tener}}'),
('tenés', 'pres_2sv', '{{es-verb form of|formal=no|person=second-person|number=singular|tense=present|mood=indicative|ending=er|tener|voseo=yes|region=Latin America}}'),
('tenida', 'pp_fs', '{{es-verb form of|mood=par|gen=f|num=s|ending=er|tener}}'),
('tenidas', 'pp_fp', '{{es-verb form of|mood=par|gen=f|num=p|ending=er|tener}}'),
('tenidos', 'pp_mp', '{{es-verb form of|mood=par|gen=m|num=p|ending=er|tener}}'),
('tengás', 'pres_sub_2sv', '{{es-verb form of|mood=subj|tense=pres|num=s|pers=2|formal=n|voseo=yes|ending=er|tener}}'),
] #}

    conj = {x.split("=")[0].strip():x.split("=")[1].strip() for x in _expand("{{es-conj}}", "tener").split(";")}
    print("len", len(conj))
#    print(conj)

    for inflection, expected_slot, template in test:
        slot = re.match(r'(\S*) of "', _expand(template)).group(1)
        assert slot == expected_slot

        if "neg_"  in slot and not inflection.startswith("no "):
            inflection = "no " + inflection

#        if "f" in slot: # formal is really just 3rd person
#            slot = re.sub(r"2(.)f", r"3\1", slot)

        if conj[slot] != inflection:
            print(slot)
        assert conj[slot] == inflection

    #conj = {x.split("=")[0].strip():x.split("=")[1].strip() for x in _expand("{{es-conj}}", "comer").split(";")}
    #print({k:v for k,v in conj.items() if v=="cómelo"})
    #assert False
