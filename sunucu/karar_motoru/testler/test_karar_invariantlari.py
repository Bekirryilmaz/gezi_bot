from dataclasses import replace

import pytest

from sunucu.bilgi.domain import BilgiDurumu
from sunucu.karar_motoru.domain import (
    BilgiReferansi, CografiBaglam, KararAdayi, KararBaglami, KararMotoru,
    KararSonucuTuru, KosulDurumu, Tercih, ZorunluKosul,
)
from sunucu.karar_motoru.semalar import KararSonucuSemasi
from sunucu.yayin.domain import YayinUygunlukDurumu


def bilgi(aile: str, deger, *, durum=BilgiDurumu.BILINIYOR, yayinlanabilir=True, kimlik="claim"):
    return BilgiReferansi(kimlik, aile, 1, deger, durum, yayinlanabilir, 1)


def baglam(**degisiklikler):
    veri = dict(
        amac="uzun_sohbet", cografi_baglam=CografiBaglam("samsun"),
        zorunlu_kosullar=(ZorunluKosul("basamaksiz", "giris_basamak", False),),
        tercihler=(Tercih("manzara", "manzara", True, oncelik=5),),
        bilgi_surumu="bilgi-1", politika_surumu="politika-1",
    )
    veri.update(degisiklikler)
    return KararBaglami(**veri)


def aday(*bilgiler, sponsorlu=False):
    return KararAdayi(
        yer_id="yer-1", canonical_id="canonical-1", sube_id="sube-1", isim="Yer",
        sehir="Samsun", ilce="Atakum", yayin_durumu=YayinUygunlukDurumu.YAYINLANABILIR,
        yayin_surumu=3, bilgiler=tuple(bilgiler), sponsorlu=sponsorlu,
    )


def test_hard_constraint_fail_guclu_preference_ile_telafi_edilemez():
    sonuc = KararMotoru().degerlendir(baglam(), aday(
        bilgi("giris_basamak", True), bilgi("manzara", True), bilgi("amac_destegi", ["uzun_sohbet"])
    ))
    assert sonuc.uygunluk is KosulDurumu.UYGUN_DEGIL
    assert sonuc.karar_turu is KararSonucuTuru.IHTIYACLA_UYUSMUYOR
    assert not any(g.kod.value == "tercih_destekleniyor" for g in sonuc.gerekceler)


def test_hard_constraint_unknown_uygun_degil_degildir():
    sonuc = KararMotoru().degerlendir(baglam(), aday(bilgi("amac_destegi", ["uzun_sohbet"])))
    assert sonuc.uygunluk is KosulDurumu.DEGERLENDIRILEMIYOR
    assert sonuc.karar_turu is KararSonucuTuru.KRITIK_BILGI_BILINMIYOR


def test_sponsor_karari_degistirmez():
    bilgiler = (bilgi("giris_basamak", False), bilgi("manzara", True), bilgi("amac_destegi", ["uzun_sohbet"]))
    motor = KararMotoru()
    assert replace(motor.degerlendir(baglam(), aday(*bilgiler)), trace_reference=None) == replace(motor.degerlendir(baglam(), aday(*bilgiler, sponsorlu=True)), trace_reference=None)


def test_ayni_context_ve_surum_ayni_karar():
    a = aday(bilgi("giris_basamak", False), bilgi("amac_destegi", ["uzun_sohbet"]))
    motor = KararMotoru()
    assert motor.degerlendir(baglam(giris_kanali="kesfet"), a) == motor.degerlendir(baglam(giris_kanali="akilli_rota"), a)


@pytest.mark.parametrize(
    ("durum", "kod"),
    [
        (BilgiDurumu.GERI_CEKILMIS, "kritik_kosul_geri_cekilmis"),
        (BilgiDurumu.ESKIMIS, "kritik_kosul_eskimis"),
        (BilgiDurumu.CELISKILI, "kritik_kosul_celiskili"),
    ],
)
def test_gecersiz_kritik_claim_dogrulanmis_uygunluk_uretmez(durum, kod):
    sonuc = KararMotoru().degerlendir(baglam(), aday(
        bilgi("giris_basamak", False, durum=durum, yayinlanabilir=False),
        bilgi("amac_destegi", ["uzun_sohbet"]),
    ))
    assert sonuc.uygunluk is KosulDurumu.DEGERLENDIRILEMIYOR
    assert [x.kod.value for x in sonuc.bilinmeyenler] == [kod]
    assert sonuc.kullanilan_iddia_surumleri == ()


def test_public_dto_internal_score_ve_yasak_alanlari_tasimaz():
    sonuc = KararMotoru().degerlendir(baglam(), aday(
        bilgi("giris_basamak", False), bilgi("amac_destegi", ["uzun_sohbet"])
    ))
    payload = KararSonucuSemasi.domainden(sonuc).model_dump()
    metin = str(payload)
    for yasak in ("internal_score", "duygu_skoru", "model_confidence", "sponsor"):
        assert yasak not in metin


def test_reddedilen_yer_ayni_baglamda_tekrar_onerilmez():
    sonuc = KararMotoru().degerlendir(
        baglam(reddedilen_yerler=frozenset({"yer-1"})),
        aday(bilgi("giris_basamak", False), bilgi("amac_destegi", ["uzun_sohbet"])),
    )
    assert sonuc.karar_turu is KararSonucuTuru.IHTIYACLA_UYUSMUYOR
    assert sonuc.kritik_engeller[0].kod.value == "kullanici_tarafindan_reddedildi"


def test_anlasilmayan_kritik_girdi_netlestirme_ister():
    sonuc = KararMotoru().degerlendir(
        baglam(anlasilmayan_kritik_girdiler=("sakinlik",)),
        aday(bilgi("giris_basamak", False), bilgi("amac_destegi", ["uzun_sohbet"])),
    )
    assert sonuc.karar_turu is KararSonucuTuru.NETLESTIRME_GEREKLI


def test_cografi_kapsam_sessizce_genisletilmez():
    sonuc = KararMotoru().degerlendir(
        baglam(cografi_baglam=CografiBaglam("ordu")),
        aday(bilgi("giris_basamak", False), bilgi("amac_destegi", ["uzun_sohbet"])),
    )
    assert sonuc.karar_turu is KararSonucuTuru.KAPSAM_DISI
    assert sonuc.kritik_engeller[-1].kod.value == "cografi_kapsam_disi"
