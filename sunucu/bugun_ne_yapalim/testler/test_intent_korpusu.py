import json
from pathlib import Path

from sunucu.bugun_ne_yapalim.intent import metni_coz
from sunucu.bugun_ne_yapalim.korpus_raporu import _uyuyor_mu

KORPUS = Path(__file__).with_name("intent_korpusu.json")


def test_en_az_100_gercekci_turkce_ifade_regresyonu():
    ornekler = json.loads(KORPUS.read_text(encoding="utf-8"))
    assert len(ornekler) >= 100
    hatalar = []
    for ornek in ornekler:
        cozum = metni_coz(ornek["input"])
        if not _uyuyor_mu(cozum, ornek["beklenen"]):
            hatalar.append((ornek["input"], ornek["beklenen"], cozum))
    assert not hatalar


def test_negation_olumlu_olanak_uydurmaz():
    for metin in ("otopark yok", "wifi çekmiyor", "manzarası yok"):
        cozum = metni_coz(metin)
        assert "wifi" not in cozum["zorunlu_kosullar"]
        assert "otopark" not in cozum["zorunlu_kosullar"]


def test_partner_sohbetten_romantik_veya_sakinlik_turetilmez():
    cozum = metni_coz("sevgilimle kahve içip sohbet edeceğiz")
    assert cozum["kisi_baglami"] == "partner"
    assert cozum["ana_amac"] == "kahve_icmek"
    assert "sohbet" in cozum["aktiviteler"]
    assert "sessiz_ortam" not in cozum["tercihler"]
