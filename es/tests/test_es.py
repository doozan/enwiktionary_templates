import enwiktionary_templates
import mwparserfromhell

expand_template = enwiktionary_templates.expand_template

def test_es_compound_of():
    template = next(mwparserfromhell.parse("# {{es-compound of|adelgaz|ar|adelgazar|las|mood=inf}}").ifilter_templates())
    assert expand_template(template, "test") == 'compound form of "adelgazar"+"las"'

def test_es_conj():
    template = next(mwparserfromhell.parse("{{es-conj-er||p=tener}}").ifilter_templates())
    value = expand_template(template, "test")
    assert value == "1=tener; 10=tiene; 11=tenemos; 12=tenéis; 13=tienen; 14=tenía; 15=tenías; 16=tenía; 17=teníamos; 18=teníais; 19=tenían; 2=teniendo; 20=tuve; 21=tuviste; 22=tuvo; 23=tuvimos; 24=tuvisteis; 25=tuvieron; 26=tendré; 27=tendrás; 28=tendrá; 29=tendremos; 3=tenido; 30=tendréis; 31=tendrán; 32=tendría; 33=tendrías; 34=tendría; 35=tendríamos; 36=tendríais; 37=tendrían; 38=tenga; 39=tengas; 4=tenida; 41=tenga; 42=tengamos; 43=tengáis; 44=tengan; 45=tuviera; 46=tuvieras; 47=tuviera; 48=tuviéramos; 49=tuvierais; 5=tenidos; 50=tuvieran; 51=tuviese; 52=tuvieses; 53=tuviese; 54=tuviésemos; 55=tuvieseis; 56=tuviesen; 57=tuviere; 58=tuvieres; 59=tuviere; 6=tenidas; 60=tuviéremos; 61=tuviereis; 62=tuvieren; 63=ten; 64=tené; 65=tenga; 66=tengamos; 67=tened; 68=tengan; 69=tengas; 7=tengo; 70=tenga; 71=tengamos; 72=tengáis; 73=tengan; 8=tienes; 9=tenés; ger_acc-dat_1=teniéndómela; ger_acc-dat_1=teniéndómelas; ger_acc-dat_1=teniéndómelo; ger_acc-dat_1=teniéndómelos; ger_acc-dat_2=teniéndótela; ger_acc-dat_2=teniéndótelas; ger_acc-dat_2=teniéndótelo; ger_acc-dat_2=teniéndótelos; ger_acc-dat_3=teniéndósela; ger_acc-dat_3=teniéndóselas; ger_acc-dat_3=teniéndóselo; ger_acc-dat_3=teniéndóselos; ger_acc-dat_4=teniéndónosla; ger_acc-dat_4=teniéndónoslas; ger_acc-dat_4=teniéndónoslo; ger_acc-dat_4=teniéndónoslos; ger_acc-dat_5=teniéndóosla; ger_acc-dat_5=teniéndóoslas; ger_acc-dat_5=teniéndóoslo; ger_acc-dat_5=teniéndóoslos; ger_acc-dat_6=teniéndósela; ger_acc-dat_6=teniéndóselas; ger_acc-dat_6=teniéndóselo; ger_acc-dat_6=teniéndóselos; ger_acc-dat_7=teniéndósela; ger_acc-dat_7=teniéndóselas; ger_acc-dat_7=teniéndóselo; ger_acc-dat_7=teniéndóselos; ger_acc_1=teniéndome; ger_acc_2=teniéndote; ger_acc_3=teniéndola; ger_acc_3=teniéndolo; ger_acc_3=teniéndose; ger_acc_4=teniéndonos; ger_acc_5=teniéndoos; ger_acc_6=teniéndolas; ger_acc_6=teniéndolos; ger_acc_6=teniéndose; ger_acc_7=teniéndose; ger_dat_1=teniéndome; ger_dat_2=teniéndote; ger_dat_3=teniéndole; ger_dat_3=teniéndose; ger_dat_4=teniéndonos; ger_dat_5=teniéndoos; ger_dat_6=teniéndoles; ger_dat_6=teniéndose; imp_1p_acc-dat_2=tengámóstela; imp_1p_acc-dat_2=tengámóstelas; imp_1p_acc-dat_2=tengámóstelo; imp_1p_acc-dat_2=tengámóstelos; imp_1p_acc-dat_4=tengámónosla; imp_1p_acc-dat_4=tengámónoslas; imp_1p_acc-dat_4=tengámónoslo; imp_1p_acc-dat_4=tengámónoslos; imp_1p_acc-dat_5=tengámóosla; imp_1p_acc-dat_5=tengámóoslas; imp_1p_acc-dat_5=tengámóoslo; imp_1p_acc-dat_5=tengámóoslos; imp_1p_acc_2=tengámoste; imp_1p_acc_3=tengámosla; imp_1p_acc_3=tengámoslo; imp_1p_acc_4=tengámonos; imp_1p_acc_5=tengámoos; imp_1p_acc_6=tengámoslas; imp_1p_acc_6=tengámoslos; imp_1p_dat_2=tengámoste; imp_1p_dat_3=tengámosle; imp_1p_dat_4=tengámonos; imp_1p_dat_5=tengámoos; imp_1p_dat_6=tengámosles; imp_f2p_acc-dat_1=téngánmela; imp_f2p_acc-dat_1=téngánmelas; imp_f2p_acc-dat_1=téngánmelo; imp_f2p_acc-dat_1=téngánmelos; imp_f2p_acc-dat_4=téngánnosla; imp_f2p_acc-dat_4=téngánnoslas; imp_f2p_acc-dat_4=téngánnoslo; imp_f2p_acc-dat_4=téngánnoslos; imp_f2p_acc-dat_6=téngánsela; imp_f2p_acc-dat_6=téngánselas; imp_f2p_acc-dat_6=téngánselo; imp_f2p_acc-dat_6=téngánselos; imp_f2p_acc-dat_7=téngánsela; imp_f2p_acc-dat_7=téngánselas; imp_f2p_acc-dat_7=téngánselo; imp_f2p_acc-dat_7=téngánselos; imp_f2p_acc_1=ténganme; imp_f2p_acc_3=ténganla; imp_f2p_acc_3=ténganlo; imp_f2p_acc_4=téngannos; imp_f2p_acc_6=ténganlas; imp_f2p_acc_6=ténganlos; imp_f2p_acc_6=ténganse; imp_f2p_acc_7=ténganse; imp_f2p_dat_1=ténganme; imp_f2p_dat_3=ténganle; imp_f2p_dat_4=téngannos; imp_f2p_dat_6=ténganles; imp_f2p_dat_6=ténganse; imp_f2s_acc-dat_1=téngámela; imp_f2s_acc-dat_1=téngámelas; imp_f2s_acc-dat_1=téngámelo; imp_f2s_acc-dat_1=téngámelos; imp_f2s_acc-dat_3=téngásela; imp_f2s_acc-dat_3=téngáselas; imp_f2s_acc-dat_3=téngáselo; imp_f2s_acc-dat_3=téngáselos; imp_f2s_acc-dat_4=téngánosla; imp_f2s_acc-dat_4=téngánoslas; imp_f2s_acc-dat_4=téngánoslo; imp_f2s_acc-dat_4=téngánoslos; imp_f2s_acc-dat_7=téngásela; imp_f2s_acc-dat_7=téngáselas; imp_f2s_acc-dat_7=téngáselo; imp_f2s_acc-dat_7=téngáselos; imp_f2s_acc_1=téngame; imp_f2s_acc_3=téngala; imp_f2s_acc_3=téngalo; imp_f2s_acc_3=téngase; imp_f2s_acc_4=ténganos; imp_f2s_acc_6=téngalas; imp_f2s_acc_6=téngalos; imp_f2s_acc_7=téngase; imp_f2s_dat_1=téngame; imp_f2s_dat_3=téngale; imp_f2s_dat_3=téngase; imp_f2s_dat_4=ténganos; imp_f2s_dat_6=téngales; imp_i2p_acc-dat_1=tenédmela; imp_i2p_acc-dat_1=tenédmelas; imp_i2p_acc-dat_1=tenédmelo; imp_i2p_acc-dat_1=tenédmelos; imp_i2p_acc-dat_4=tenédnosla; imp_i2p_acc-dat_4=tenédnoslas; imp_i2p_acc-dat_4=tenédnoslo; imp_i2p_acc-dat_4=tenédnoslos; imp_i2p_acc-dat_5=tenéosla; imp_i2p_acc-dat_5=tenéoslas; imp_i2p_acc-dat_5=tenéoslo; imp_i2p_acc-dat_5=tenéoslos; imp_i2p_acc-dat_7=tenédosla; imp_i2p_acc-dat_7=tenédoslas; imp_i2p_acc-dat_7=tenédoslo; imp_i2p_acc-dat_7=tenédoslos; imp_i2p_acc_1=tenedme; imp_i2p_acc_3=tenedla; imp_i2p_acc_3=tenedlo; imp_i2p_acc_4=tenednos; imp_i2p_acc_5=teneos; imp_i2p_acc_6=tenedlas; imp_i2p_acc_6=tenedlos; imp_i2p_acc_7=tenedos; imp_i2p_dat_1=tenedme; imp_i2p_dat_3=tenedle; imp_i2p_dat_4=tenednos; imp_i2p_dat_5=teneos; imp_i2p_dat_6=tenedles; imp_i2s_acc-dat_1=ténmela; imp_i2s_acc-dat_1=ténmelas; imp_i2s_acc-dat_1=ténmelo; imp_i2s_acc-dat_1=ténmelos; imp_i2s_acc-dat_2=téntela; imp_i2s_acc-dat_2=téntelas; imp_i2s_acc-dat_2=téntelo; imp_i2s_acc-dat_2=téntelos; imp_i2s_acc-dat_4=ténnosla; imp_i2s_acc-dat_4=ténnoslas; imp_i2s_acc-dat_4=ténnoslo; imp_i2s_acc-dat_4=ténnoslos; imp_i2s_acc_1=tenme; imp_i2s_acc_2=tente; imp_i2s_acc_3=tenla; imp_i2s_acc_3=tenlo; imp_i2s_acc_4=tennos; imp_i2s_acc_6=tenlas; imp_i2s_acc_6=tenlos; imp_i2s_dat_1=tenme; imp_i2s_dat_2=tente; imp_i2s_dat_3=tenle; imp_i2s_dat_4=tennos; imp_i2s_dat_6=tenles; inf_acc-dat_1=tenérmela; inf_acc-dat_1=tenérmelas; inf_acc-dat_1=tenérmelo; inf_acc-dat_1=tenérmelos; inf_acc-dat_2=tenértela; inf_acc-dat_2=tenértelas; inf_acc-dat_2=tenértelo; inf_acc-dat_2=tenértelos; inf_acc-dat_3=tenérsela; inf_acc-dat_3=tenérselas; inf_acc-dat_3=tenérselo; inf_acc-dat_3=tenérselos; inf_acc-dat_4=tenérnosla; inf_acc-dat_4=tenérnoslas; inf_acc-dat_4=tenérnoslo; inf_acc-dat_4=tenérnoslos; inf_acc-dat_5=tenérosla; inf_acc-dat_5=tenéroslas; inf_acc-dat_5=tenéroslo; inf_acc-dat_5=tenéroslos; inf_acc-dat_6=tenérsela; inf_acc-dat_6=tenérselas; inf_acc-dat_6=tenérselo; inf_acc-dat_6=tenérselos; inf_acc-dat_7=tenérsela; inf_acc-dat_7=tenérselas; inf_acc-dat_7=tenérselo; inf_acc-dat_7=tenérselos; inf_acc_1=tenerme; inf_acc_2=tenerte; inf_acc_3=tenerla; inf_acc_3=tenerlo; inf_acc_3=tenerse; inf_acc_4=tenernos; inf_acc_5=teneros; inf_acc_6=tenerlas; inf_acc_6=tenerlos; inf_acc_6=tenerse; inf_acc_7=tenerse; inf_dat_1=tenerme; inf_dat_2=tenerte; inf_dat_3=tenerle; inf_dat_3=tenerse; inf_dat_4=tenernos; inf_dat_5=teneros; inf_dat_6=tenerles; inf_dat_6=tenerse"
    assert len(value.split("; ")) == 301

    template = next(mwparserfromhell.parse("{{es-conj-er||p=tener|combined=1}}").ifilter_templates())
    value = expand_template(template, "test")
    assert value == "1=tener; 10=tiene; 11=tenemos; 12=tenéis; 13=tienen; 14=tenía; 15=tenías; 16=tenía; 17=teníamos; 18=teníais; 19=tenían; 2=teniendo; 20=tuve; 21=tuviste; 22=tuvo; 23=tuvimos; 24=tuvisteis; 25=tuvieron; 26=tendré; 27=tendrás; 28=tendrá; 29=tendremos; 3=tenido; 30=tendréis; 31=tendrán; 32=tendría; 33=tendrías; 34=tendría; 35=tendríamos; 36=tendríais; 37=tendrían; 38=tenga; 39=tengas; 4=tenida; 41=tenga; 42=tengamos; 43=tengáis; 44=tengan; 45=tuviera; 46=tuvieras; 47=tuviera; 48=tuviéramos; 49=tuvierais; 5=tenidos; 50=tuvieran; 51=tuviese; 52=tuvieses; 53=tuviese; 54=tuviésemos; 55=tuvieseis; 56=tuviesen; 57=tuviere; 58=tuvieres; 59=tuviere; 6=tenidas; 60=tuviéremos; 61=tuviereis; 62=tuvieren; 63=ten; 64=tené; 65=tenga; 66=tengamos; 67=tened; 68=tengan; 69=tengas; 7=tengo; 70=tenga; 71=tengamos; 72=tengáis; 73=tengan; 8=tienes; 9=tenés; ger_acc-dat_1=teniéndómela; ger_acc-dat_1=teniéndómelas; ger_acc-dat_1=teniéndómelo; ger_acc-dat_1=teniéndómelos; ger_acc-dat_2=teniéndótela; ger_acc-dat_2=teniéndótelas; ger_acc-dat_2=teniéndótelo; ger_acc-dat_2=teniéndótelos; ger_acc-dat_3=teniéndósela; ger_acc-dat_3=teniéndóselas; ger_acc-dat_3=teniéndóselo; ger_acc-dat_3=teniéndóselos; ger_acc-dat_4=teniéndónosla; ger_acc-dat_4=teniéndónoslas; ger_acc-dat_4=teniéndónoslo; ger_acc-dat_4=teniéndónoslos; ger_acc-dat_5=teniéndóosla; ger_acc-dat_5=teniéndóoslas; ger_acc-dat_5=teniéndóoslo; ger_acc-dat_5=teniéndóoslos; ger_acc-dat_6=teniéndósela; ger_acc-dat_6=teniéndóselas; ger_acc-dat_6=teniéndóselo; ger_acc-dat_6=teniéndóselos; ger_acc-dat_7=teniéndósela; ger_acc-dat_7=teniéndóselas; ger_acc-dat_7=teniéndóselo; ger_acc-dat_7=teniéndóselos; ger_acc_1=teniéndome; ger_acc_2=teniéndote; ger_acc_3=teniéndola; ger_acc_3=teniéndolo; ger_acc_3=teniéndose; ger_acc_4=teniéndonos; ger_acc_5=teniéndoos; ger_acc_6=teniéndolas; ger_acc_6=teniéndolos; ger_acc_6=teniéndose; ger_acc_7=teniéndose; ger_dat_1=teniéndome; ger_dat_2=teniéndote; ger_dat_3=teniéndole; ger_dat_3=teniéndose; ger_dat_4=teniéndonos; ger_dat_5=teniéndoos; ger_dat_6=teniéndoles; ger_dat_6=teniéndose; imp_1p_acc-dat_2=tengámóstela; imp_1p_acc-dat_2=tengámóstelas; imp_1p_acc-dat_2=tengámóstelo; imp_1p_acc-dat_2=tengámóstelos; imp_1p_acc-dat_4=tengámónosla; imp_1p_acc-dat_4=tengámónoslas; imp_1p_acc-dat_4=tengámónoslo; imp_1p_acc-dat_4=tengámónoslos; imp_1p_acc-dat_5=tengámóosla; imp_1p_acc-dat_5=tengámóoslas; imp_1p_acc-dat_5=tengámóoslo; imp_1p_acc-dat_5=tengámóoslos; imp_1p_acc_2=tengámoste; imp_1p_acc_3=tengámosla; imp_1p_acc_3=tengámoslo; imp_1p_acc_4=tengámonos; imp_1p_acc_5=tengámoos; imp_1p_acc_6=tengámoslas; imp_1p_acc_6=tengámoslos; imp_1p_dat_2=tengámoste; imp_1p_dat_3=tengámosle; imp_1p_dat_4=tengámonos; imp_1p_dat_5=tengámoos; imp_1p_dat_6=tengámosles; imp_f2p_acc-dat_1=téngánmela; imp_f2p_acc-dat_1=téngánmelas; imp_f2p_acc-dat_1=téngánmelo; imp_f2p_acc-dat_1=téngánmelos; imp_f2p_acc-dat_4=téngánnosla; imp_f2p_acc-dat_4=téngánnoslas; imp_f2p_acc-dat_4=téngánnoslo; imp_f2p_acc-dat_4=téngánnoslos; imp_f2p_acc-dat_6=téngánsela; imp_f2p_acc-dat_6=téngánselas; imp_f2p_acc-dat_6=téngánselo; imp_f2p_acc-dat_6=téngánselos; imp_f2p_acc-dat_7=téngánsela; imp_f2p_acc-dat_7=téngánselas; imp_f2p_acc-dat_7=téngánselo; imp_f2p_acc-dat_7=téngánselos; imp_f2p_acc_1=ténganme; imp_f2p_acc_3=ténganla; imp_f2p_acc_3=ténganlo; imp_f2p_acc_4=téngannos; imp_f2p_acc_6=ténganlas; imp_f2p_acc_6=ténganlos; imp_f2p_acc_6=ténganse; imp_f2p_acc_7=ténganse; imp_f2p_dat_1=ténganme; imp_f2p_dat_3=ténganle; imp_f2p_dat_4=téngannos; imp_f2p_dat_6=ténganles; imp_f2p_dat_6=ténganse; imp_f2s_acc-dat_1=téngámela; imp_f2s_acc-dat_1=téngámelas; imp_f2s_acc-dat_1=téngámelo; imp_f2s_acc-dat_1=téngámelos; imp_f2s_acc-dat_3=téngásela; imp_f2s_acc-dat_3=téngáselas; imp_f2s_acc-dat_3=téngáselo; imp_f2s_acc-dat_3=téngáselos; imp_f2s_acc-dat_4=téngánosla; imp_f2s_acc-dat_4=téngánoslas; imp_f2s_acc-dat_4=téngánoslo; imp_f2s_acc-dat_4=téngánoslos; imp_f2s_acc-dat_7=téngásela; imp_f2s_acc-dat_7=téngáselas; imp_f2s_acc-dat_7=téngáselo; imp_f2s_acc-dat_7=téngáselos; imp_f2s_acc_1=téngame; imp_f2s_acc_3=téngala; imp_f2s_acc_3=téngalo; imp_f2s_acc_3=téngase; imp_f2s_acc_4=ténganos; imp_f2s_acc_6=téngalas; imp_f2s_acc_6=téngalos; imp_f2s_acc_7=téngase; imp_f2s_dat_1=téngame; imp_f2s_dat_3=téngale; imp_f2s_dat_3=téngase; imp_f2s_dat_4=ténganos; imp_f2s_dat_6=téngales; imp_i2p_acc-dat_1=tenédmela; imp_i2p_acc-dat_1=tenédmelas; imp_i2p_acc-dat_1=tenédmelo; imp_i2p_acc-dat_1=tenédmelos; imp_i2p_acc-dat_4=tenédnosla; imp_i2p_acc-dat_4=tenédnoslas; imp_i2p_acc-dat_4=tenédnoslo; imp_i2p_acc-dat_4=tenédnoslos; imp_i2p_acc-dat_5=tenéosla; imp_i2p_acc-dat_5=tenéoslas; imp_i2p_acc-dat_5=tenéoslo; imp_i2p_acc-dat_5=tenéoslos; imp_i2p_acc-dat_7=tenédosla; imp_i2p_acc-dat_7=tenédoslas; imp_i2p_acc-dat_7=tenédoslo; imp_i2p_acc-dat_7=tenédoslos; imp_i2p_acc_1=tenedme; imp_i2p_acc_3=tenedla; imp_i2p_acc_3=tenedlo; imp_i2p_acc_4=tenednos; imp_i2p_acc_5=teneos; imp_i2p_acc_6=tenedlas; imp_i2p_acc_6=tenedlos; imp_i2p_acc_7=tenedos; imp_i2p_dat_1=tenedme; imp_i2p_dat_3=tenedle; imp_i2p_dat_4=tenednos; imp_i2p_dat_5=teneos; imp_i2p_dat_6=tenedles; imp_i2s_acc-dat_1=ténmela; imp_i2s_acc-dat_1=ténmelas; imp_i2s_acc-dat_1=ténmelo; imp_i2s_acc-dat_1=ténmelos; imp_i2s_acc-dat_2=téntela; imp_i2s_acc-dat_2=téntelas; imp_i2s_acc-dat_2=téntelo; imp_i2s_acc-dat_2=téntelos; imp_i2s_acc-dat_4=ténnosla; imp_i2s_acc-dat_4=ténnoslas; imp_i2s_acc-dat_4=ténnoslo; imp_i2s_acc-dat_4=ténnoslos; imp_i2s_acc_1=tenme; imp_i2s_acc_2=tente; imp_i2s_acc_3=tenla; imp_i2s_acc_3=tenlo; imp_i2s_acc_4=tennos; imp_i2s_acc_6=tenlas; imp_i2s_acc_6=tenlos; imp_i2s_dat_1=tenme; imp_i2s_dat_2=tente; imp_i2s_dat_3=tenle; imp_i2s_dat_4=tennos; imp_i2s_dat_6=tenles; inf_acc-dat_1=tenérmela; inf_acc-dat_1=tenérmelas; inf_acc-dat_1=tenérmelo; inf_acc-dat_1=tenérmelos; inf_acc-dat_2=tenértela; inf_acc-dat_2=tenértelas; inf_acc-dat_2=tenértelo; inf_acc-dat_2=tenértelos; inf_acc-dat_3=tenérsela; inf_acc-dat_3=tenérselas; inf_acc-dat_3=tenérselo; inf_acc-dat_3=tenérselos; inf_acc-dat_4=tenérnosla; inf_acc-dat_4=tenérnoslas; inf_acc-dat_4=tenérnoslo; inf_acc-dat_4=tenérnoslos; inf_acc-dat_5=tenérosla; inf_acc-dat_5=tenéroslas; inf_acc-dat_5=tenéroslo; inf_acc-dat_5=tenéroslos; inf_acc-dat_6=tenérsela; inf_acc-dat_6=tenérselas; inf_acc-dat_6=tenérselo; inf_acc-dat_6=tenérselos; inf_acc-dat_7=tenérsela; inf_acc-dat_7=tenérselas; inf_acc-dat_7=tenérselo; inf_acc-dat_7=tenérselos; inf_acc_1=tenerme; inf_acc_2=tenerte; inf_acc_3=tenerla; inf_acc_3=tenerlo; inf_acc_3=tenerse; inf_acc_4=tenernos; inf_acc_5=teneros; inf_acc_6=tenerlas; inf_acc_6=tenerlos; inf_acc_6=tenerse; inf_acc_7=tenerse; inf_dat_1=tenerme; inf_dat_2=tenerte; inf_dat_3=tenerle; inf_dat_3=tenerse; inf_dat_4=tenernos; inf_dat_5=teneros; inf_dat_6=tenerles; inf_dat_6=tenerse"
    assert len(value.split("; ")) == 301

    template = next(mwparserfromhell.parse("{{es-conj-ír|p=oír|o|combined=1}}").ifilter_templates())
    value = expand_template(template, "test")
    assert len(value.split("; ")) == 301


def test_es_noun():
    template = next(mwparserfromhell.parse("{{es-noun|m}}").ifilter_templates())
    assert expand_template(template, "testo") == 'pl=testos'

    template = next(mwparserfromhell.parse("{{es-proper noun|m}}").ifilter_templates())
    assert expand_template(template, "testo") == 'pl=testos'

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


