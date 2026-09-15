from sunucu.admin.kuyruk_triyaj import kuyruk_onceligini_hesapla


def test_dusuk_risk_structured_fact_yuksek_risk_amac_cikarimindan_ayrilir():
    wifi = kuyruk_onceligini_hesapla(aile="wifi", guclu_kanit=True, dusuk_celiski=True, dogrulanmis_sube=True)
    amac = kuyruk_onceligini_hesapla(aile="amac_destegi", guclu_kanit=True, dusuk_celiski=True)
    assert wifi.triyaj_sinifi == "dusuk_risk"
    assert amac.triyaj_sinifi == "yuksek_risk"
    assert wifi.oncelik_puani > amac.oncelik_puani
    assert "sponsor" not in wifi.triyaj_sinifi
