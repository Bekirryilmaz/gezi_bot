from ortak.sabitler import (
    ROTA_KAPSAM_AILELERI,
    RotaHazirlikDurumu,
    RotaKapsamSinifi,
    TamamlikHucresi,
    ZiyaretSuresiKaynagi,
)
from sunucu.bilgi.calisma_saati import calisma_saatini_ayristir
from sunucu.bilgi.rota_hazirlik import RotaHazirlikGirdisi, rota_hazirligini_hesapla
from sunucu.bilgi.ziyaret_suresi import ziyaret_suresini_coz


def test_calisma_saati_gecerli_normalize_ve_24_7():
    basit = calisma_saatini_ayristir("Mo-Su 08:00-22:00")
    assert basit.sozdizimi_gecerli
    assert basit.normalize == "Mo-Su 08:00-22:00"
    assert basit.haftalik["Mo"] == (("08:00", "22:00"),)
    assert basit.haftalik["Su"] == (("08:00", "22:00"),)
    acik = calisma_saatini_ayristir("24/7")
    assert acik.her_zaman_acik and acik.sozdizimi_gecerli


def test_calisma_saati_karmasik_ve_gecersiz_tahmin_edilmez():
    for ham in (
        "Mo-Su 08:00-02:00",
        "PH off; Mo-Fr 09:00-18:00",
        "Mo-Su",
        "Jan-Mar 09:00-17:00",
        'Mo-Fr 09:00-18:00 "by appointment"',
        "sunrise-sunset",
        "",
    ):
        sonuc = calisma_saatini_ayristir(ham)
        assert not sonuc.sozdizimi_gecerli, ham
        assert sonuc.haftalik == {}


def test_calisma_saati_parcali_ve_off():
    sonuc = calisma_saatini_ayristir("Mo-Fr 09:00-12:00,13:00-18:00; Sa 10:00-14:00; Su off")
    assert sonuc.sozdizimi_gecerli
    assert sonuc.haftalik["Mo"] == (("09:00", "12:00"), ("13:00", "18:00"))
    assert sonuc.haftalik["Sa"] == (("10:00", "14:00"),)
    assert sonuc.haftalik["Su"] == ()


def test_ziyaret_suresi_sezgisel_fact_degildir():
    sezgisel = ziyaret_suresini_coz(alt_kategori="kafe")
    assert sezgisel.kaynak is ZiyaretSuresiKaynagi.KATEGORI_SEZGISEL
    assert sezgisel.fact_mi is False
    assert sezgisel.dakika == 45
    dogrulanan = ziyaret_suresini_coz(dogrulanmis_dakika=80, alt_kategori="kafe")
    assert dogrulanan.fact_mi is True
    assert dogrulanan.kaynak is ZiyaretSuresiKaynagi.BILINEN_DOGRULANMIS
    kullanici = ziyaret_suresini_coz(
        kullanici_dakika=30, dogrulanmis_dakika=80, alt_kategori="muze"
    )
    assert kullanici.kaynak is ZiyaretSuresiKaynagi.KULLANICI_SECIMI
    assert kullanici.fact_mi is False
    bilinmeyen = ziyaret_suresini_coz(alt_kategori="internet_kafe")
    assert bilinmeyen.kaynak is ZiyaretSuresiKaynagi.BILINMIYOR
    assert bilinmeyen.dakika is None


def test_rota_hazirlik_saat_yoksa_sinirli_karantina_kapali():
    hazir = rota_hazirligini_hesapla(
        RotaHazirlikGirdisi(
            kimlik_sinifi="guclu",
            sube_durum="aktif",
            koordinat_gecerli=True,
            ilce_id="ilce-1",
            amaclar=("kahve_icmek",),
            yayin_uygun=True,
            calisma_saati=TamamlikHucresi.BILINIYOR,
        )
    )
    assert hazir.durum is RotaHazirlikDurumu.ROTA_HAZIR
    assert "calisma_saati_biliniyor" in hazir.neden_kodlari
    sinirli = rota_hazirligini_hesapla(
        RotaHazirlikGirdisi(
            kimlik_sinifi="kullanilabilir",
            sube_durum="aktif",
            koordinat_gecerli=True,
            ilce_id="ilce-1",
            amaclar=("yemek_yemek",),
            yayin_uygun=True,
            calisma_saati=TamamlikHucresi.BILINMIYOR,
        )
    )
    assert sinirli.durum is RotaHazirlikDurumu.ROTA_SINIRLI
    kesif = rota_hazirligini_hesapla(
        RotaHazirlikGirdisi(
            kimlik_sinifi="kullanilabilir",
            sube_durum="aktif",
            koordinat_gecerli=True,
            ilce_id=None,
            amaclar=(),
            yayin_uygun=True,
            calisma_saati=TamamlikHucresi.BILINMIYOR,
        )
    )
    assert kesif.durum is RotaHazirlikDurumu.KESIF_ADAYI
    kapali = rota_hazirligini_hesapla(
        RotaHazirlikGirdisi(
            kimlik_sinifi="karantina",
            sube_durum="aktif",
            koordinat_gecerli=False,
            ilce_id="ilce-1",
            amaclar=("kahve_icmek",),
            yayin_uygun=True,
            calisma_saati=TamamlikHucresi.BILINIYOR,
        )
    )
    assert kapali.durum is RotaHazirlikDurumu.ROTA_KAPALI
    assert hazir.kirilim["kamusal_skor"] is False


def test_rota_kapsam_aileleri_taksonomiyle_hizali():
    assert ROTA_KAPSAM_AILELERI["calisma_saatleri"] == RotaKapsamSinifi.ROTA_KRITIK.value
    assert ROTA_KAPSAM_AILELERI["wifi"] == RotaKapsamSinifi.KARAR_ONEMLI.value
    assert ROTA_KAPSAM_AILELERI["web_sitesi"] == RotaKapsamSinifi.ISTEGE_BAGLI.value
    assert ROTA_KAPSAM_AILELERI["ziyaret_suresi"] == RotaKapsamSinifi.KARAR_ONEMLI.value
