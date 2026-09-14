from ortak.sabitler import DuyguEtiketi, VeriKaynagi
from veri.duygu_analizi.gozlem_adayi import yorumdan_aday_gozlemler
from veri.ortak.yorum_modeli import HamYorum


def test_nlp_yalniz_inceleme_bekleyen_gozlem_adayi_uretir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS, kaynak_yer_id="place-1", kaynak_yorum_id="review-1",
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
        kaynak=VeriKaynagi.EKSI_SOZLUK, kaynak_yer_id="yer-adayi",
        yorum_metni="Ortam sakin ve temizdi.",
    )
    aday = yorumdan_aday_gozlemler(yorum, DuyguEtiketi.OLUMLU, 0.5)[0]
    assert aday.kaynak is VeriKaynagi.EKSI_SOZLUK
    assert aday.yer_adayi == "yer-adayi"
    assert aday.span
    assert aday.model_surumu
    assert aday.cikarim_guven_sinifi.value == "orta"
