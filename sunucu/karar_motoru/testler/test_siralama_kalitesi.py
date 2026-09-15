
from ortak.sabitler import AmacEslemeSeviyesi, amac_esleme_seviyesi
from sunucu.bilgi.domain import BilgiDurumu
from sunucu.karar_motoru.domain import (
    BilgiReferansi,
    CografiBaglam,
    DahiliSinyalReferansi,
    KararAdayi,
    KararBaglami,
    KararMotoru,
    KararSonucuTuru,
    KosulDurumu,
    NedenKodu,
    Tercih,
)
from sunucu.karar_motoru.siralama import oneri_listesini_sec, sirala_adaylar, siralama_anahtari
from sunucu.yayin.domain import YayinUygunlukDurumu


def _baglam(**degisiklikler):
    veri = dict(
        amac="kahve_icmek",
        cografi_baglam=CografiBaglam("samsun"),
        tercihler=(Tercih("sohbet", "sohbet_uygunlugu", True, oncelik=4),),
        bilgi_surumu="b",
        politika_surumu="p",
    )
    veri.update(degisiklikler)
    return KararBaglami(**veri)


def _aday(isim, *, alt="kafe", bilgiler=(), sinyaller=(), kalite="kullanilabilir", ilce="Atakum", canonical="c"):
    return KararAdayi(
        yer_id=isim,
        canonical_id=canonical or isim,
        sube_id=isim,
        isim=isim,
        sehir="Samsun",
        ilce=ilce,
        yayin_durumu=YayinUygunlukDurumu.YAYINLANABILIR,
        yayin_surumu=1,
        bilgiler=tuple(bilgiler),
        alt_kategori=alt,
        dahili_sinyaller=tuple(sinyaller),
        kimlik_kalite_sinifi=kalite,
    )


def test_internet_kafe_kahve_amaci_uretmez():
    assert amac_esleme_seviyesi("internet_kafe", "kahve_icmek") is AmacEslemeSeviyesi.NO_PURPOSE_INFERENCE
    assert amac_esleme_seviyesi("kafe", "kahve_icmek") is AmacEslemeSeviyesi.DIRECT_PURPOSE_FACT
    assert amac_esleme_seviyesi("kahve_uzmanlik", "kahve_icmek") is AmacEslemeSeviyesi.DIRECT_PURPOSE_FACT
    assert amac_esleme_seviyesi("restoran_lokanta", "kahve_icmek") is AmacEslemeSeviyesi.NO_PURPOSE_INFERENCE
    assert (
        amac_esleme_seviyesi("tatli_pastane", "kahve_icmek")
        is AmacEslemeSeviyesi.NO_PURPOSE_INFERENCE
    )
    assert amac_esleme_seviyesi("sokak_lezzeti", "yemek_yemek") is AmacEslemeSeviyesi.DIRECT_PURPOSE_FACT
    sonuc = KararMotoru().degerlendir(
        _baglam(),
        _aday("Net Cafe", alt="internet_kafe"),
    )
    assert sonuc.uygunluk is KosulDurumu.DEGERLENDIRILEMIYOR
    assert any(g.kod is NedenKodu.AMAC_BILINMIYOR for g in sonuc.bilinmeyenler)


def test_karantina_ve_supheli_kimlik_oneri_havuzuna_girmez():
    motor = KararMotoru()
    for sinif in ("karantina", "supheli"):
        sonuc = motor.degerlendir(_baglam(), _aday("Kirli", kalite=sinif))
        assert sonuc.karar_turu is KararSonucuTuru.KAPSAM_DISI
        assert sonuc.kritik_engeller[0].kod is NedenKodu.KIMLIK_ONERIYE_UYGUN_DEGIL


def test_quality_fact_deneyim_alfabetikten_once_gelir():
    claim = BilgiReferansi("c1", "wifi", 1, True, BilgiDurumu.BILINIYOR, True, 1)
    deneyim = DahiliSinyalReferansi(
        "s", "sohbet_uygunlugu", "v1", "guclu", "aktif", True, True
    )
    zayif = _aday("Adalet Cafe")
    guclu = _aday(
        "Günevi",
        bilgiler=(claim,),
        sinyaller=(deneyim,),
        kalite="guclu",
        canonical="gunevi",
    )
    sakin = _aday("Anka", sinyaller=(deneyim,), canonical="anka")
    sirali = sirala_adaylar(_baglam(), [zayif, guclu, sakin])
    assert [a.isim for a in sirali] == ["Günevi", "Anka", "Adalet Cafe"]


def test_ayni_normalize_isim_top_listede_tekrarlanmaz():
    a = _aday("153 Restoran", alt="restoran_lokanta", canonical="a", ilce="Atakum")
    b = _aday("153 Restoran", alt="restoran_lokanta", canonical="b", ilce="İlkadım")
    secilen = oneri_listesini_sec(_baglam(amac="yemek_yemek", tercihler=()), [a, b], hedef=5)
    assert len(secilen) == 1


def test_weak_experience_siralamaya_girmez_unknown_burden_ayirir():
    zayif = DahiliSinyalReferansi("s", "sohbet_uygunlugu", "v1", "zayif", "karar_disi", False, False)
    orta = DahiliSinyalReferansi("s", "sohbet_uygunlugu", "v1", "orta", "aktif", True, True)
    a = _aday("A Kafe", sinyaller=(zayif,), canonical="a")
    b = _aday("B Kafe", sinyaller=(orta,), canonical="b")
    sirali = sirala_adaylar(_baglam(), [a, b])
    assert [x.isim for x in sirali] == ["B Kafe", "A Kafe"]
    anahtar_a = siralama_anahtari(_baglam(), a)
    anahtar_b = siralama_anahtari(_baglam(), b)
    assert anahtar_b.deneyim_destek > anahtar_a.deneyim_destek
    assert anahtar_a.bilinmeyen_yuku > anahtar_b.bilinmeyen_yuku


def test_ilce_baglaminda_dis_ilce_sirada_geriye_dusar():
    atakum = _aday("Atakum Kafe", ilce="Atakum", canonical="a")
    kavak = _aday("Kavak Kafe", ilce="Kavak", canonical="k")
    baglam = _baglam(cografi_baglam=CografiBaglam("samsun", ilce="Atakum"))
    sirali = sirala_adaylar(baglam, [kavak, atakum])
    assert [a.isim for a in sirali][0] == "Atakum Kafe"
