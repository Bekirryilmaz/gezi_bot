"""
BirlesikYer (JSONL) -> Yer/YerKaynak (PostgreSQL) aktarimi.

Bu dosya BILEREK sadece `veri/ortak/` (paylasilan Pydantic modelleri) ve
`ortak/` (paylasilan sabitler) ice aktarir; `veri/esleme` veya
`veri/duygu_analizi` gibi pipeline'a ozgu modullere BAGIMLI DEGILDIR --
sunucu katmani, veri katmaninin ic mantigindan bagimsiz kalmali, sadece
onun JSONL "sozlesmesini" (contract) okumali.

Idempotentlik: ayni BirlesikYer kaydi birden fazla kez aktarilirsa (orn.
toplayicilar yeniden calistirildiginda) yeni bir Yer satiri DUPLICATE
OLUSTURULMAZ -- eslesme, `YerKaynak(kaynak, kaynak_id)` unique ciftine gore
yapilir: BirlesikYer.kaynaklar listesindeki HERHANGI BIR referans daha once
aktarilmis bir Yer'e isaret ediyorsa, o Yer guncellenir.
"""

from __future__ import annotations

from geoalchemy2.elements import WKTElement
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ortak.sabitler import VARSAYILAN_DENEYIM_PUANLARI
from sunucu.veritabani.modeller import KonaklamaDetay, KullaniciRotasi, Yer, YerKaynak, Yorum
from veri.ortak.birlesik_yer_modeli import BirlesikYer, KaynakReferansi
from sunucu.kimlik.servis import aday_kaydet, legacy_yer_icin_kimlik_sagla
from sunucu.arama.normalizasyon import turkce_arama_normalize
from sunucu.veritabani.arama_modelleri import Ilce


def _konum_noktasi_uret(enlem: float, boylam: float) -> WKTElement:
    return WKTElement(f"POINT({boylam} {enlem})", srid=4326)


def _essiz_kaynak_referanslari(birlesik_yer: BirlesikYer) -> list[KaynakReferansi]:
    """Ham kaynak verisinde (orn. Google Maps'in ayni yeri iki kez
    dondurmesi) BirlesikYer.kaynaklar icinde ayni (kaynak, kaynak_id) cifti
    birden fazla kez gecebilir -- bu, `YerKaynak` tablosundaki unique
    kisiti ihlal eder. Burada (kaynak, kaynak_id) bazinda tekillestirilir,
    ilk gorulen kayit tutulur."""
    gorulen: set[tuple[str, str]] = set()
    essizler: list[KaynakReferansi] = []
    for kaynak_ref in birlesik_yer.kaynaklar:
        anahtar = (kaynak_ref.kaynak.value, kaynak_ref.kaynak_id)
        if anahtar in gorulen:
            continue
        gorulen.add(anahtar)
        essizler.append(kaynak_ref)
    return essizler


def _mevcut_yerleri_bul(oturum: Session, birlesik_yer: BirlesikYer) -> list[Yer]:
    """BirlesikYer.kaynaklar listesindeki (kaynak, kaynak_id) ciftlerinden
    HERHANGI birine isaret eden TUM Yer satirlarini dondurur.

    Esleme katmani bazen (nadiren) farkli OSM geometrilerini tek
    BirlesikYer'de birlestirir; onceki aktarimda bunlar ayri Yer
    satirlari olarak kalmis olabilir. Bu durumda tek `.first()` yetmez --
    tum eslesen Yer'leri bulup birlestirmek gerekir (bkz. `_yerleri_birlestir`).
    """
    if not birlesik_yer.kaynaklar:
        return []

    ciftler = [(kaynak_ref.kaynak.value, kaynak_ref.kaynak_id) for kaynak_ref in _essiz_kaynak_referanslari(birlesik_yer)]
    eslesen_kaynaklar = (
        oturum.query(YerKaynak)
        .filter(tuple_(YerKaynak.kaynak, YerKaynak.kaynak_id).in_(ciftler))
        .all()
    )
    gorulen_yer_idler: set[str] = set()
    yerler: list[Yer] = []
    for kaynak in eslesen_kaynaklar:
        if kaynak.yer_id in gorulen_yer_idler:
            continue
        gorulen_yer_idler.add(kaynak.yer_id)
        yerler.append(kaynak.yer)
    return yerler


def _birincil_yeri_sec(yerler: list[Yer]) -> Yer:
    """Birden fazla Yer ayni BirlesikYer'e isaret ediyorsa hangisinin
    'kanonik' kalacagina karar verir. Oncelik: Google Maps kaynagi olan >
    daha cok kaynak referansi olan > listedeki ilk."""

    def _anahtar(yer: Yer) -> tuple[int, int]:
        google_var = any(k.kaynak == "google_maps" for k in yer.kaynaklar)
        return (1 if google_var else 0, len(yer.kaynaklar))

    return max(yerler, key=_anahtar)


def _yerleri_birlestir(oturum: Session, birincil: Yer, ikinciller: list[Yer]) -> None:
    """`ikinciller` listesindeki Yer satirlarinin kaynak/yorum/konaklama
    baglarini `birincil`'e tasir, sonra ikincil satirlari siler.

    Bu, esleme katmaninin once ayri aktarilmis iki kaydi sonradan tek
    BirlesikYer'de birlestirmesi durumunda UniqueViolation'i onler."""
    for ikincil in ikinciller:
        if ikincil.id == birincil.id:
            continue

        for kaynak in list(ikincil.kaynaklar):
            kaynak.yer_id = birincil.id

        oturum.query(Yorum).filter(Yorum.yer_id == ikincil.id).update(
            {Yorum.yer_id: birincil.id}, synchronize_session=False
        )

        oturum.query(KullaniciRotasi).filter(
            KullaniciRotasi.konaklama_onerisi_yer_id == ikincil.id
        ).update(
            {KullaniciRotasi.konaklama_onerisi_yer_id: birincil.id},
            synchronize_session=False,
        )

        ikincil_konaklama = oturum.get(KonaklamaDetay, ikincil.id)
        if ikincil_konaklama is not None:
            birincil_konaklama = oturum.get(KonaklamaDetay, birincil.id)
            if birincil_konaklama is None:
                ikincil_konaklama.yer_id = birincil.id
            else:
                oturum.delete(ikincil_konaklama)

        oturum.flush()
        oturum.delete(ikincil)
        oturum.flush()
        print(
            f"[BILGI] Yer birlestirildi: '{ikincil.isim}' -> '{birincil.isim}' "
            f"(esleme katmani bunlari tek yer olarak isaretlemisti)."
        )


def _eksik_kaynaklari_ekle(oturum: Session, yer: Yer, birlesik_yer: BirlesikYer, veri_batch_id: str | None = None) -> None:
    """`yer`de henuz kaydi olmayan yeni YerKaynak referanslarini ekler
    (orn. bu yer ilk aktarimda sadece OSM'den geldi, bu aktarimda Google
    Maps de eslesmis olabilir).

    Global unique kisiti nedeniyle, (kaynak, kaynak_id) baska bir Yer'de
    zaten varsa (birlestirme adimi atlanmissa) sessizce atlaniyor -- aksi
    halde UniqueViolation firlatilir."""
    mevcut_ciftler = {(kaynak.kaynak, kaynak.kaynak_id) for kaynak in yer.kaynaklar}
    for kaynak_ref in _essiz_kaynak_referanslari(birlesik_yer):
        cift = (kaynak_ref.kaynak.value, kaynak_ref.kaynak_id)
        if cift in mevcut_ciftler:
            continue
        baska_yerde = (
            oturum.query(YerKaynak)
            .filter(YerKaynak.kaynak == cift[0], YerKaynak.kaynak_id == cift[1])
            .first()
        )
        if baska_yerde is not None:
            continue
        mevcut_ciftler.add(cift)
        oturum.add(
            YerKaynak(
                yer_id=yer.id,
                kaynak=kaynak_ref.kaynak.value,
                kaynak_id=kaynak_ref.kaynak_id,
                kaynak_url=_kisalt(kaynak_ref.kaynak_url, 500),
                cekilme_zamani=kaynak_ref.cekilme_zamani,
                kaynakta_gozlemlenme_zamani=kaynak_ref.kaynakta_gozlemlenme_zamani,
                veri_batch_id=veri_batch_id,
            )
        )


def _kisalt(deger: str | None, maks: int) -> str | None:
    """DB String(n) sutunlarina sigmayan degerleri nazikce kirpar.
    Google Maps bazen 'web sitesi' alanina 500+ karakterlik bir Google
    arama URL'si koyabiliyor (bkz. 2026-08-04 aktarim hatasi:
    StringDataRightTruncation on web_sitesi)."""
    if deger is None:
        return None
    if len(deger) <= maks:
        return deger
    return deger[:maks]


def _temel_alanlari_guncelle(yer: Yer, birlesik_yer: BirlesikYer) -> None:
    """Aciklayici/degisken alanlari (isim, adres, ozellikler vb.) en guncel
    BirlesikYer kaydiyla senkronize eder. `deneyim_puanlari` BILEREK burada
    YOK -- kuratorluk mudahalesi olabilecegi icin ayri ele alinir (bkz.
    `_varsayilan_deneyim_puanlarini_uygula`)."""
    yer.isim = _kisalt(birlesik_yer.isim, 255) or birlesik_yer.isim
    yer.ana_kategori = birlesik_yer.ana_kategori.value
    yer.alt_kategori = birlesik_yer.alt_kategori
    yer.ilce = _kisalt(birlesik_yer.ilce, 100)
    yer.adres = birlesik_yer.adres  # Text sutunu, uzunluk siniri yok
    yer.aciklama = birlesik_yer.aciklama
    yer.telefon = _kisalt(birlesik_yer.telefon, 30)
    yer.web_sitesi = _kisalt(birlesik_yer.web_sitesi, 500)
    yer.konum = _konum_noktasi_uret(birlesik_yer.enlem, birlesik_yer.boylam)
    yer.ozellikler = birlesik_yer.ozellikler.model_dump(mode="json")
    yer.aktiviteler = [aktivite.value for aktivite in birlesik_yer.aktiviteler]
    yer.fotograf_urlleri = list(birlesik_yer.fotograf_urlleri)
    yer.kaynakta_puan_ortalamasi = birlesik_yer.kaynakta_puan_ortalamasi
    yer.kaynakta_puan_sayisi = birlesik_yer.kaynakta_puan_sayisi


def _canonical_ilceyi_bagla(oturum: Session, yer: Yer) -> None:
    """Serbest metni yalniz ayni sehirde tam normalize eslesme varsa baglar."""
    normalize_ilce = turkce_arama_normalize(yer.ilce)
    if not normalize_ilce:
        # Eksik yeni kaynak metni, mevcut canonical bagi silmez.
        return
    ilce = (
        oturum.query(Ilce)
        .filter(Ilce.sehir_id == yer.sehir_id, Ilce.arama_isim == normalize_ilce, Ilce.aktif_mi.is_(True))
        .one_or_none()
    )
    if ilce is not None:
        yer.ilce_id = ilce.id


def _varsayilan_deneyim_puanlarini_uygula(yer: Yer) -> None:
    """`deneyim_puanlari` alani hala bossa (ilk aktarim), alt kategoriye
    gore varsayilan puanlari uygular. Zaten doluysa (daha once kuratorluk
    veya bu aktarim tarafindan doldurulmussa) DOKUNULMAZ -- boylece elle
    yapilan iyilestirmeler bir sonraki aktarimda ezilmez."""
    if yer.deneyim_puanlari:
        return
    yer.deneyim_puanlari = dict(VARSAYILAN_DENEYIM_PUANLARI.get(yer.alt_kategori, {}))


def yer_yukle_veya_olustur(oturum: Session, sehir_id: str, birlesik_yer: BirlesikYer, veri_batch_id: str | None = None) -> Yer:
    """Bir BirlesikYer kaydini veritabanina aktarir. Var olan bir Yer'e
    eslesirse gunceller, eslesmezse yeni Yer + YerKaynak satirlari olusturur.
    Donen Yer, `oturum.flush()` sonrasi kesin bir `id`'ye sahiptir.

    Birden fazla mevcut Yer ayni BirlesikYer'in kaynaklarina isaret
    ediyorsa (esleme yanlis-pozitif birlestirmesi), once bunlari tek
    satira indirger, sonra gunceller."""
    mevcut_yerler = _mevcut_yerleri_bul(oturum, birlesik_yer)

    if not mevcut_yerler:
        yer = Yer(
            sehir_id=sehir_id,
            isim=birlesik_yer.isim,
            ana_kategori=birlesik_yer.ana_kategori.value,
            alt_kategori=birlesik_yer.alt_kategori,
            konum=_konum_noktasi_uret(birlesik_yer.enlem, birlesik_yer.boylam),
        )
        oturum.add(yer)
        oturum.flush()  # yer.id'yi hemen almak icin (YerKaynak FK'si icin gerekli)
        for kaynak_ref in _essiz_kaynak_referanslari(birlesik_yer):
            oturum.add(
                YerKaynak(
                    yer_id=yer.id,
                    kaynak=kaynak_ref.kaynak.value,
                    kaynak_id=kaynak_ref.kaynak_id,
                    kaynak_url=kaynak_ref.kaynak_url,
                    cekilme_zamani=kaynak_ref.cekilme_zamani,
                    kaynakta_gozlemlenme_zamani=kaynak_ref.kaynakta_gozlemlenme_zamani,
                    veri_batch_id=veri_batch_id,
                )
            )
    else:
        yer = _birincil_yeri_sec(mevcut_yerler)
        ikinciller = [aday for aday in mevcut_yerler if aday.id != yer.id]
        if ikinciller:
            ana_sube = legacy_yer_icin_kimlik_sagla(oturum, yer)
            for ikincil in ikinciller:
                diger_sube = legacy_yer_icin_kimlik_sagla(oturum, ikincil)
                aday_kaydet(oturum, ana_sube.id, diger_sube.id, 0.9, {"neden": "importta_coklu_legacy_eslesme"})
            oturum.flush()
            return yer
        _eksik_kaynaklari_ekle(oturum, yer, birlesik_yer, veri_batch_id)

    _temel_alanlari_guncelle(yer, birlesik_yer)
    _canonical_ilceyi_bagla(oturum, yer)
    _varsayilan_deneyim_puanlarini_uygula(yer)

    sube = legacy_yer_icin_kimlik_sagla(oturum, yer)
    referanslar = {(r.kaynak.value, r.kaynak_id): r for r in _essiz_kaynak_referanslari(birlesik_yer)}
    for kaynak in yer.kaynaklar:
        kaynak.sube_id = sube.id
        ref = referanslar.get((kaynak.kaynak, kaynak.kaynak_id))
        if ref is not None:
            kaynak.veri_batch_id = veri_batch_id
            kaynak.cekilme_zamani = ref.cekilme_zamani
            kaynak.kaynakta_gozlemlenme_zamani = ref.kaynakta_gozlemlenme_zamani

    oturum.flush()
    return yer
