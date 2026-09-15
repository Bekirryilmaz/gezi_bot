from __future__ import annotations

from types import SimpleNamespace

from sunucu.api.semalar import YerDetay
from sunucu.api.uygulama import uygulama

YASAK_ALANLAR = {
    "yorum_metni",
    "yazar_takma_adi",
    "yazar",
    "author",
    "ornek_ifadeler",
    "ornek_yorumlar",
    "kaynakta_puan",
    "kaynakta_puan_ortalamasi",
    "kaynakta_puan_sayisi",
    "duygu_skoru",
    "duygu_skoru_ortalama",
    "duygu_etiketi",
    "genel_duygu_skoru",
    "genel_duygu_etiketi",
    "duygu_ozeti",
    "kullanilan_yorum_sayisi",
    "unique_review_count",
    "supporting_observation_count",
    "counter_observation_count",
    "kaynak_yorum_id",
    "review_id",
    "span",
    "preference_eligible",
    "guven_sinifi",
    "internal_confidence",
    "sentiment_percentage",
    "kimlik_kalite",
    "oncelik_puani",
    "triyaj_sinifi",
    "dahili_sinyal",
    "kimlik_kalite_sinifi",
    "kimlik_kalite_kirilim",
    "oncelik_puani",
    "yer_profili",
    "deneyim_puanlari",
    "skor_kirilimi",
}


def _anahtarlari_yur(value: object):
    if isinstance(value, dict):
        for anahtar, alt_deger in value.items():
            yield str(anahtar)
            yield from _anahtarlari_yur(alt_deger)
    elif isinstance(value, list):
        for oge in value:
            yield from _anahtarlari_yur(oge)


def test_public_openapi_recursive_yasak_alan_icermiyor():
    sema = uygulama.openapi()
    public_sema_anahtarlari = set(_anahtarlari_yur(sema))
    assert public_sema_anahtarlari.isdisjoint(YASAK_ALANLAR)


def test_public_mapper_ic_veriyi_projectiona_tasimiyor():
    yer = SimpleNamespace(
        id="yer-1",
        isim="Ornek",
        ana_kategori="gezilecek_yer",
        alt_kategori="tarihi_kulturel",
        ilce="Atakum",
        adres="Adres",
        aciklama="Aciklama",
        tanitim_metni="Tanitma",
        telefon=None,
        web_sitesi=None,
        ozellikler={"sponsorlu_mekan": True, "ornek_ifadeler": ["yasak"]},
        aktiviteler=["yuruyus"],
        fotograf_urlleri=[],
        kaynakta_puan_ortalamasi=4.9,
        duygu_skoru_ortalama=0.9,
        deneyim_puanlari={"ic": 99},
        yer_profili={"ornek_ifadeler": ["yasak"]},
        duygu_ozeti="Yorumdan turetilmis ozet",
    )
    payload = YerDetay.yerden_olustur(yer, 41.0, 36.0).model_dump()

    assert set(_anahtarlari_yur(payload)).isdisjoint(YASAK_ALANLAR)
    assert payload["ticari_bildirim"] == "sponsorlu"


def test_versioned_arama_public_contract_internal_skor_tasimiyor():
    sema = uygulama.openapi()
    assert "/v1/arama" in sema["paths"]
    arama_semalari = {
        ad: deger for ad, deger in sema["components"]["schemas"].items() if ad.startswith("Arama")
    }
    anahtarlar = set(_anahtarlari_yur(arama_semalari))
    assert anahtarlar.isdisjoint({"internal_score", "fuzzy_score", "benzerlik", "sponsor"})


def test_kesfet_ve_public_detail_versioned_contract_yasak_alan_tasimiyor():
    sema = uygulama.openapi()
    assert "/v1/kesfet/degerlendir" in sema["paths"]
    assert "/v1/yerler/{yer_id}" in sema["paths"]
    ilgili = {ad: deger for ad, deger in sema["components"]["schemas"].items() if ad.startswith(("Kesfet", "KamusalYer", "YayimlanmisBilgi"))}
    assert set(_anahtarlari_yur(ilgili)).isdisjoint(YASAK_ALANLAR | {"guven_sinifi", "sponsor"})
