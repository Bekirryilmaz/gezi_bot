from datetime import UTC, datetime, timedelta

from ortak.sabitler import (
    CalismaSaatiDurumu,
    RotaBilinmeyenDavranis,
    RotaHazirlikDurumu,
    TamamlikHucresi,
    ZiyaretSuresiKaynagi,
)
from sunucu.admin.kuyruk_triyaj import kuyruk_onceligini_hesapla
from sunucu.bilgi.calisma_saati import (
    AYRISTIRICI_SURUMU,
    calisma_saati_kaydini_kur,
    calisma_saatini_ayristir,
)
from sunucu.bilgi.rota_bilinmeyen import (
    akilli_rota_go_degerlendirmesi,
    rota_bilinmeyen_davranisi,
)
from sunucu.bilgi.rota_hazirlik import RotaHazirlikGirdisi, rota_hazirligini_hesapla
from sunucu.bilgi.rota_senaryo import senaryo_uygunlugunu_olc
from sunucu.bilgi.tarihi_neden import tarihi_mekan_nedenleri
from sunucu.bilgi.ziyaret_suresi import ziyaret_suresini_coz


def test_bilinen_basit_sozdizimi_known_olur():
    for ham in ("Mo-Fr 09:00-18:00", "Sa-Su 10:00-22:00", "24/7"):
        sonuc = calisma_saatini_ayristir(ham)
        assert sonuc.durum is CalismaSaatiDurumu.KNOWN, ham
        assert sonuc.sozdizimi_gecerli
        assert sonuc.parser_surumu == AYRISTIRICI_SURUMU


def test_bos_saat_unknown_acik_iddiasi_yok():
    sonuc = calisma_saatini_ayristir("")
    assert sonuc.durum is CalismaSaatiDurumu.UNKNOWN
    assert not sonuc.acik_iddiasi_kurulabilir
    kayit = calisma_saati_kaydini_kur(ham=None, kaynak="openstreetmap")
    assert kayit.durum is CalismaSaatiDurumu.UNKNOWN
    assert kayit.acik_iddiasi_kurulabilir is False


def test_karmasik_gece_ve_mevsim_invalid_tahmin_edilmez():
    for ham in (
        "Mo-Su 08:00-02:00",
        "Mo-Su",
        "Jan-Mar 09:00-17:00",
        'Mo-Fr 09:00-18:00 "by appointment"',
        "sunrise-sunset",
        "summer",
    ):
        sonuc = calisma_saatini_ayristir(ham)
        assert sonuc.durum is CalismaSaatiDurumu.INVALID, ham
        assert not sonuc.sozdizimi_gecerli
        assert not sonuc.acik_iddiasi_kurulabilir
        assert sonuc.haftalik == {}


def test_ph_kurali_parcali_known_hafta_ici_korunur():
    sonuc = calisma_saatini_ayristir("PH off; Mo-Fr 09:00-18:00")
    assert sonuc.durum is CalismaSaatiDurumu.PARTIALLY_KNOWN
    assert sonuc.sozdizimi_gecerli
    assert sonuc.haftalik["Mo"] == (("09:00", "18:00"),)
    assert sonuc.haftalik["Fr"] == (("09:00", "18:00"),)
    assert "ph" in sonuc.neden


def test_eski_saat_stale_olur_acik_sanilmaz():
    eski = datetime.now(UTC) - timedelta(days=200)
    kayit = calisma_saati_kaydini_kur(
        ham="Mo-Su 09:00-18:00",
        kaynak="openstreetmap",
        gozlemlenme_zamani=eski,
        cekilme_zamani=eski,
        ham_referans="https://www.openstreetmap.org/node/1",
    )
    assert kayit.durum is CalismaSaatiDurumu.STALE
    assert kayit.ayristirma.sozdizimi_gecerli
    assert kayit.acik_iddiasi_kurulabilir is False
    assert kayit.zaman_dilimi == "Europe/Istanbul"
    assert kayit.parser_surumu == AYRISTIRICI_SURUMU


def test_birinci_taraf_saat_kanit_alanlari_tasir():
    simdi = datetime.now(UTC)
    kayit = calisma_saati_kaydini_kur(
        ham="Mo-Su 08:30-17:30",
        kaynak="site_ici",
        gozlemlenme_zamani=simdi,
        cekilme_zamani=simdi,
        ham_referans="https://samsun.bel.tr/ornek-muze",
        zaman_dilimi="Europe/Istanbul",
    )
    assert kayit.durum is CalismaSaatiDurumu.KNOWN
    assert kayit.kaynak == "site_ici"
    assert kayit.ham_referans.endswith("ornek-muze")
    assert kayit.acik_iddiasi_kurulabilir is True


def test_planlama_tahmini_araliklidir_fact_degildir():
    tahmin = ziyaret_suresini_coz(alt_kategori="tarihi_kulturel")
    assert tahmin.kaynak is ZiyaretSuresiKaynagi.PLANLAMA_TAHMINI
    assert tahmin.fact_mi is False
    assert tahmin.minimum_dk == 45
    assert tahmin.tipik_dk == 60
    assert tahmin.maksimum_dk == 90
    assert "yaklasik" in tahmin.kullanici_ifadesi
    assert "45" in tahmin.kullanici_ifadesi and "90" in tahmin.kullanici_ifadesi
    dogrulanan = ziyaret_suresini_coz(dogrulanmis_dakika=80, alt_kategori="kafe")
    assert dogrulanan.kaynak is ZiyaretSuresiKaynagi.DOGRULANMIS_SURE
    assert dogrulanan.fact_mi is True
    assert dogrulanan.tipik_dk == 80
    kullanici = ziyaret_suresini_coz(kullanici_dakika=30, alt_kategori="kafe")
    assert kullanici.kaynak is ZiyaretSuresiKaynagi.KULLANICI_SECIMI
    assert kullanici.fact_mi is False


def test_bilinmeyen_saat_rota_sinirli_kalir_hazir_olmaz():
    sinirli = rota_hazirligini_hesapla(
        RotaHazirlikGirdisi(
            kimlik_sinifi="guclu",
            sube_durum="aktif",
            koordinat_gecerli=True,
            ilce_id="ilce-1",
            amaclar=("tarihi_kulturel_ziyaret",),
            yayin_uygun=True,
            calisma_saati=TamamlikHucresi.BILINMIYOR,
            calisma_saati_durumu=CalismaSaatiDurumu.UNKNOWN,
        )
    )
    assert sinirli.durum is RotaHazirlikDurumu.ROTA_SINIRLI
    parcali = rota_hazirligini_hesapla(
        RotaHazirlikGirdisi(
            kimlik_sinifi="guclu",
            sube_durum="aktif",
            koordinat_gecerli=True,
            ilce_id="ilce-1",
            amaclar=("kahve_icmek",),
            yayin_uygun=True,
            calisma_saati=TamamlikHucresi.BILINIYOR,
            calisma_saati_durumu=CalismaSaatiDurumu.PARTIALLY_KNOWN,
        )
    )
    assert parcali.durum is RotaHazirlikDurumu.ROTA_SINIRLI
    hazir = rota_hazirligini_hesapla(
        RotaHazirlikGirdisi(
            kimlik_sinifi="guclu",
            sube_durum="aktif",
            koordinat_gecerli=True,
            ilce_id="ilce-1",
            amaclar=("kahve_icmek",),
            yayin_uygun=True,
            calisma_saati=TamamlikHucresi.BILINIYOR,
            calisma_saati_durumu=CalismaSaatiDurumu.KNOWN,
        )
    )
    assert hazir.durum is RotaHazirlikDurumu.ROTA_HAZIR


def test_unknown_sozlesmesi_hard_block_ve_uyariyi_ayirir():
    assert (
        rota_bilinmeyen_davranisi("calisma_saati_bilinmiyor").davranis
        is RotaBilinmeyenDavranis.SINIRLI_UYARI
    )
    assert rota_bilinmeyen_davranisi("calisma_saati_bilinmiyor").acik_iddiasi is False
    assert (
        rota_bilinmeyen_davranisi("ziyaret_suresi_tahmini").davranis
        is RotaBilinmeyenDavranis.SINIRLI_UYARI
    )
    assert (
        rota_bilinmeyen_davranisi("gecis_bilinmiyor").davranis
        is RotaBilinmeyenDavranis.SINIRLI_UYARI
    )
    assert (
        rota_bilinmeyen_davranisi("rezervasyon_bilinmiyor").davranis
        is RotaBilinmeyenDavranis.SINIRLI_UYARI
    )
    assert (
        rota_bilinmeyen_davranisi("gecici_kapanis_bilinmiyor").davranis
        is RotaBilinmeyenDavranis.SINIRLI_UYARI
    )
    assert (
        rota_bilinmeyen_davranisi("kimlik_karantina").davranis
        is RotaBilinmeyenDavranis.HARD_BLOK
    )
    assert (
        rota_bilinmeyen_davranisi("koordinat_gecersiz").davranis
        is RotaBilinmeyenDavranis.HARD_BLOK
    )


def test_tarihi_mekan_reason_code_saat_eksikini_ayirir():
    satir = {
        "amaclar": ["tarihi_kulturel_ziyaret"],
        "kimlik_sinifi": "guclu",
        "matris": {
            "calisma_saatleri": TamamlikHucresi.BILINMIYOR.value,
            "koordinat": TamamlikHucresi.BILINIYOR.value,
            "ilce": TamamlikHucresi.BILINIYOR.value,
            "amac": TamamlikHucresi.BILINIYOR.value,
            "kimlik": TamamlikHucresi.BILINIYOR.value,
        },
        "rota_hazirlik": {"durum": "rota_sinirli", "neden_kodlari": ["calisma_saati_bilinmiyor"]},
        "ziyaret_suresi": {"kaynak": "planlama_tahmini", "fact_mi": False},
    }
    nedenler = tarihi_mekan_nedenleri(satir)
    assert "calisma_saati_eksik" in nedenler
    assert "ziyaret_suresi_fact_degil" in nedenler
    assert "kimlik_problemi" not in nedenler


def _aday(
    *,
    amac: str,
    ilce: str,
    durum: str,
    saat: str,
    sessiz: bool = False,
) -> dict:
    nlp = {}
    if sessiz:
        nlp["sessiz_ortam"] = {
            "guven_sinifi": "guclu",
            "preference_eligible": True,
        }
    return {
        "amaclar": [amac],
        "ilce_adi": ilce,
        "matris": {"calisma_saatleri": saat},
        "rota_hazirlik": {"durum": durum},
        "ziyaret_suresi": {
            "kaynak": "planlama_tahmini",
            "fact_mi": False,
            "minimum_dk": 30,
            "tipik_dk": 45,
            "maksimum_dk": 75,
        },
        "nlp": nlp,
    }


def test_senaryo_a_f_aday_sayilarini_ayirir():
    satirlar = [
        _aday(amac="kahve_icmek", ilce="Atakum", durum="rota_hazir", saat="biliniyor"),
        _aday(amac="kahve_icmek", ilce="Atakum", durum="rota_sinirli", saat="bilinmiyor"),
        _aday(
            amac="kahve_icmek",
            ilce="Atakum",
            durum="rota_sinirli",
            saat="bilinmiyor",
            sessiz=True,
        ),
        _aday(amac="yemek_yemek", ilce="Atakum", durum="rota_hazir", saat="biliniyor"),
        _aday(amac="yemek_yemek", ilce="İlkadım", durum="rota_sinirli", saat="bilinmiyor"),
        _aday(
            amac="tarihi_kulturel_ziyaret",
            ilce="İlkadım",
            durum="rota_sinirli",
            saat="bilinmiyor",
        ),
        _aday(
            amac="tarihi_kulturel_ziyaret",
            ilce="Atakum",
            durum="rota_kapali",
            saat="bilinmiyor",
        ),
    ]
    a = senaryo_uygunlugunu_olc(satirlar, "A")
    assert a["uygun_aday"] == 4
    assert a["rota_hazir"] == 2
    assert a["rota_sinirli"] == 2
    assert a["saat_bilinen"] == 2
    assert a["sure_tahmini_var"] == 4
    assert a["bloklanan"] == 0
    b = senaryo_uygunlugunu_olc(satirlar, "B")
    assert b["uygun_aday"] == 1
    c = senaryo_uygunlugunu_olc(satirlar, "C")
    assert c["uygun_aday"] == 2
    assert c["rota_hazir"] == 0
    d = senaryo_uygunlugunu_olc(satirlar, "D")
    assert d["uygun_aday"] == 6
    assert d["bloklanan"] == 1
    e = senaryo_uygunlugunu_olc(satirlar, "E")
    f = senaryo_uygunlugunu_olc(satirlar, "F")
    assert e["uygun_aday"] == d["uygun_aday"]
    assert f["uygun_aday"] == d["uygun_aday"]
    go = akilli_rota_go_degerlendirmesi(
        {
            "A": a,
            "B": b,
            "C": c,
            "D": d,
            "E": e,
            "F": f,
            "desteklenen_amaclar": ("kahve_icmek", "yemek_yemek", "tarihi_kulturel_ziyaret"),
            "desteklenmeyen_amaclar": ("kahvalti", "calisma"),
        }
    )
    assert go["kahvalti_zorunlu"] is False
    assert go["calisma_zorunlu"] is False
    assert "30_rota_hazir" not in go["kirilim"]


def test_kuyruk_pilot_ve_saat_onceligi():
    saat_pilot = kuyruk_onceligini_hesapla(
        aile="calisma_saatleri",
        guclu_kanit=True,
        dogrulanmis_sube=True,
        pilot_mekan=True,
        rota_kritik=True,
    )
    wifi = kuyruk_onceligini_hesapla(aile="wifi", guclu_kanit=True)
    adres = kuyruk_onceligini_hesapla(aile="adres")
    assert saat_pilot.oncelik_puani > wifi.oncelik_puani > adres.oncelik_puani
    assert saat_pilot.triyaj_sinifi == "dusuk_risk"


def test_resmi_saat_katalogu_known_ve_anit_eslesmez():
    from sunucu.bilgi.resmi_saat import (
        RESMI_CALISMA_SAATLERI,
        resmi_saat_atlama_nedeni,
        resmi_saati_esle,
    )

    for kayit in RESMI_CALISMA_SAATLERI:
        sonuc = calisma_saatini_ayristir(kayit["saat"])
        assert sonuc.durum is CalismaSaatiDurumu.KNOWN, kayit["saat"]
        assert sonuc.acik_iddiasi_kurulabilir
    gazi = resmi_saati_esle("Gazi Müzesi")
    assert gazi is not None and gazi.anahtar == "gazi_muzesi"
    amazon = resmi_saati_esle("Amazon Köyü")
    assert amazon is not None and amazon.anahtar == "amazon_koyu"
    assert resmi_saati_esle("Amazon Anıtı") is None
    assert resmi_saat_atlama_nedeni("Amazon Anıtı") == "acik_hava_anit_saat_yok"
    assert resmi_saat_atlama_nedeni("Arkeoloji Ve Etnografya Müzesi") == "ktb_tasinma_hizmet_disi"


def test_bilinmeyen_saat_acik_iddia_edilmez():
    assert calisma_saatini_ayristir("").acik_iddiasi_kurulabilir is False
    assert calisma_saatini_ayristir("Mo-Su 08:00-02:00").acik_iddiasi_kurulabilir is False
    kayit = calisma_saati_kaydini_kur(ham="Mo-Fr 09:00-18:00", kaynak="openstreetmap")
    assert kayit.acik_iddiasi_kurulabilir is True
    stale = calisma_saati_kaydini_kur(
        ham="Mo-Fr 09:00-18:00",
        kaynak="openstreetmap",
        gozlemlenme_zamani=datetime.now(UTC) - timedelta(days=200),
    )
    assert stale.acik_iddiasi_kurulabilir is False

