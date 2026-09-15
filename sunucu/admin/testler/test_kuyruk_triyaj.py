from sunucu.admin.kuyruk_triyaj import kuyruk_onceligini_hesapla


def test_dusuk_risk_structured_fact_yuksek_risk_amac_cikarimindan_ayrilir():
    wifi = kuyruk_onceligini_hesapla(aile="wifi", guclu_kanit=True, dusuk_celiski=True, dogrulanmis_sube=True)
    amac = kuyruk_onceligini_hesapla(aile="amac_destegi", guclu_kanit=True, dusuk_celiski=True)
    assert wifi.triyaj_sinifi == "dusuk_risk"
    assert amac.triyaj_sinifi == "yuksek_risk"
    assert wifi.oncelik_puani > amac.oncelik_puani
    assert "sponsor" not in wifi.triyaj_sinifi


def test_calisma_saatleri_ve_rezervasyon_dusuk_risk_amactan_once_gelir():
    saat = kuyruk_onceligini_hesapla(aile="calisma_saatleri", guclu_kanit=True)
    rezervasyon = kuyruk_onceligini_hesapla(aile="rezervasyon", guclu_kanit=True)
    amac = kuyruk_onceligini_hesapla(aile="amac_destegi")
    assert saat.triyaj_sinifi == "dusuk_risk"
    assert rezervasyon.triyaj_sinifi == "dusuk_risk"
    assert saat.oncelik_puani > rezervasyon.oncelik_puani > amac.oncelik_puani
