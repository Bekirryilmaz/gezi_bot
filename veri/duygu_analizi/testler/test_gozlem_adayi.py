from ortak.sabitler import DuyguEtiketi, VeriKaynagi
from veri.duygu_analizi.gozlem_adayi import (
    yorumdan_aday_gozlemler,
    yorumdan_yapisal_sinyal_adaylari,
)
from veri.ortak.yorum_modeli import HamYorum


def test_nlp_yalniz_inceleme_bekleyen_gozlem_adayi_uretir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS,
        kaynak_yer_id="place-1",
        kaynak_yorum_id="review-1",
        yorum_metni="Manzarasi harikaydi ama fiyatlar biraz yuksekti.",
    )
    adaylar = yorumdan_aday_gozlemler(yorum, DuyguEtiketi.OLUMLU, 0.91)
    assert adaylar
    assert {aday.inceleme_durumu.value for aday in adaylar} == {"bekliyor"}
    assert all(not aday.otomatik_yayinlanabilir for aday in adaylar)
    payload = [aday.model_dump(mode="json") for aday in adaylar]
    metin = str(payload)
    for yasak in ("mekan_puani", "uygunluk", "claim", "duygu_yuzdesi", "duygu_skoru"):
        assert yasak not in metin
    assert {aday.konu for aday in adaylar} >= {"manzara", "fiyat"}


def test_nlp_adayi_kaynak_span_model_ve_guven_sinifi_tasir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="yer-adayi",
        yorum_metni="Ortam sakin ve temizdi.",
    )
    aday = yorumdan_aday_gozlemler(yorum, DuyguEtiketi.OLUMLU, 0.5)[0]
    assert aday.kaynak is VeriKaynagi.EKSI_SOZLUK
    assert aday.yer_adayi == "yer-adayi"
    assert aday.span
    assert aday.model_surumu
    assert aday.cikarim_guven_sinifi.value == "orta"


def test_negation_ve_karsi_sinyaller_olumlu_aday_uretmez():
    ornekler = {
        "çok sakin değil": ("sessiz_ortam", "karsi"),
        "otopark yok": ("otopark", "karsi"),
        "çocukla gidilmez": ("cocuk_uygunlugu", "karsi"),
        "wifi çekmiyor": ("wifi", "karsi"),
        "manzarası yok": ("manzara", "karsi"),
        "çok pahalı": ("uygun_fiyat", "karsi"),
    }
    for metin, beklenen in ornekler.items():
        yorum = HamYorum(
            kaynak=VeriKaynagi.GOOGLE_MAPS,
            kaynak_yer_id="place-1",
            yorum_metni=metin,
        )
        adaylar = yorumdan_yapisal_sinyal_adaylari(yorum, -0.8)
        assert (adaylar[0].konu, adaylar[0].tahmini_gozlem["yon"]) == beklenen


def test_yapisal_sinyal_genel_begeni_claimi_uretmez():
    yorum = HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS,
        kaynak_yer_id="place-1",
        yorum_metni="Harika, kaliteli ve en iyi mekan.",
    )
    assert yorumdan_yapisal_sinyal_adaylari(yorum, 0.9) == []


def test_yapisal_guven_duygu_skorundan_bagimsizdir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS,
        kaynak_yer_id="place-1",
        yorum_metni="Otopark var.",
    )
    for skor in (-0.99, 0.0, 0.99):
        aday = yorumdan_yapisal_sinyal_adaylari(yorum, skor)[0]
        assert aday.cikarim_guven_sinifi.value == "dusuk"


def test_genel_konu_yapisal_karsi_sinyali_bastirmaz(monkeypatch):
    from types import SimpleNamespace

    from veri.duygu_analizi import gozlem_adayi

    monkeypatch.setattr(
        gozlem_adayi,
        "konulari_tespit_et",
        lambda *args, **kwargs: [
            SimpleNamespace(
                konu="otopark", gecen_ifade="otopark", duygu_etiketi=DuyguEtiketi.OLUMLU
            )
        ],
    )
    yorum = HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS,
        kaynak_yer_id="place-1",
        yorum_metni="Otopark yok ama yemek harika.",
    )
    adaylar = yorumdan_aday_gozlemler(yorum, DuyguEtiketi.OLUMLU, 0.99)
    yapisal = [a for a in adaylar if a.tahmini_gozlem["bilgi_turu"] == "yapisal_sinyal_adayi"]
    assert len(yapisal) == 1
    assert yapisal[0].tahmini_gozlem["yon"] == "karsi"
