from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ortak.sabitler import KimlikKaliteSinifi, ONERIYE_UYGUN_KIMLIK_SINIFLARI
from veri.ortak.sehir_ayarlari import sehir_anahtarini_isme_gore_bul, sehir_getir


class DuplicateKarari(StrEnum):
    OTOMATIK_BIRLESTIR = "otomatik_birlestir"
    INSAN_INCELEMESI = "insan_incelemesi"
    AYRI_TUT = "ayri_tut"


@dataclass(frozen=True)
class KimlikKaliteOzeti:
    sinif: KimlikKaliteSinifi
    kirilim: dict[str, object]


def isim_gecerli_mi(isim: str | None) -> bool:
    temiz = (isim or "").strip()
    if len(temiz) < 2:
        return False
    if not any(karakter.isalpha() for karakter in temiz):
        return False
    return True


def oneriye_uygun_mu(sinif: KimlikKaliteSinifi | str | None) -> bool:
    deger = sinif.value if isinstance(sinif, KimlikKaliteSinifi) else (sinif or KimlikKaliteSinifi.KULLANILABILIR.value)
    return deger in ONERIYE_UYGUN_KIMLIK_SINIFLARI


def _sehir_disi_mi(enlem: float | None, boylam: float | None, sehir_anahtari: str | None) -> bool:
    if enlem is None or boylam is None:
        return True
    if sehir_anahtari is None:
        return False
    try:
        ayar = sehir_getir(sehir_anahtari)
    except KeyError:
        isim_anahtar = sehir_anahtarini_isme_gore_bul(sehir_anahtari)
        if not isim_anahtar:
            return False
        ayar = sehir_getir(isim_anahtar)
    bbox = ayar.cografi_bbox()
    if bbox is None:
        return False
    min_enlem, max_enlem, min_boylam, max_boylam = bbox
    return not (min_enlem <= enlem <= max_enlem and min_boylam <= boylam <= max_boylam)


def kimlik_kalitesini_hesapla(
    *,
    isim: str,
    enlem: float | None,
    boylam: float | None,
    sehir_anahtari: str | None,
    alt_kategori: str | None,
    kaynak_sayisi: int = 1,
    ayni_isim_yakin_cift: int = 0,
    ilce_id: str | None = None,
    kategori_kaynak_uyumu: bool = True,
    sube_durum: str = "aktif",
) -> KimlikKaliteOzeti:
    bayraklar: list[str] = []
    if not isim_gecerli_mi(isim):
        bayraklar.append("isim_gecersiz")
    if enlem is None or boylam is None:
        bayraklar.append("koordinat_gecersiz")
    elif _sehir_disi_mi(enlem, boylam, sehir_anahtari):
        bayraklar.append("sehir_disi_koordinat")
    if ayni_isim_yakin_cift > 0:
        bayraklar.append("duplicate_suphesi")
    if not kategori_kaynak_uyumu:
        bayraklar.append("kategori_uyusmazligi")
    if sube_durum not in {"aktif"}:
        bayraklar.append("sube_aktif_degil")
    if not alt_kategori:
        bayraklar.append("kategori_eksik")

    if "isim_gecersiz" in bayraklar or "koordinat_gecersiz" in bayraklar or "sehir_disi_koordinat" in bayraklar:
        sinif = KimlikKaliteSinifi.KARANTINA
    elif "duplicate_suphesi" in bayraklar or "kategori_uyusmazligi" in bayraklar:
        sinif = KimlikKaliteSinifi.SUPHELI
    elif kaynak_sayisi >= 2 and ilce_id and not bayraklar:
        sinif = KimlikKaliteSinifi.GUCLU
    elif not bayraklar:
        sinif = KimlikKaliteSinifi.KULLANILABILIR
    else:
        sinif = KimlikKaliteSinifi.SUPHELI

    return KimlikKaliteOzeti(
        sinif=sinif,
        kirilim={
            "bayraklar": bayraklar,
            "kaynak_sayisi": kaynak_sayisi,
            "ilce_var": bool(ilce_id),
            "alt_kategori": alt_kategori,
        },
    )


def duplicate_kararini_ver(
    *,
    ayni_kaynak_id: bool,
    isim_ayni: bool,
    mesafe_metre: float,
    ayni_telefon: bool,
    ayni_website: bool,
    ayni_kategori: bool,
    ayni_koordinat: bool,
    zincir_marka: bool = False,
) -> DuplicateKarari:
    if zincir_marka and mesafe_metre > 150:
        return DuplicateKarari.AYRI_TUT
    if ayni_website and mesafe_metre > 150 and not ayni_kaynak_id:
        return DuplicateKarari.AYRI_TUT
    if (
        ayni_kaynak_id
        and isim_ayni
        and (ayni_koordinat or mesafe_metre <= 15)
        and (ayni_telefon or ayni_website)
    ):
        return DuplicateKarari.OTOMATIK_BIRLESTIR
    if isim_ayni and ayni_kategori and mesafe_metre <= 30 and (ayni_telefon or ayni_website):
        return DuplicateKarari.OTOMATIK_BIRLESTIR
    if isim_ayni and ayni_kategori and mesafe_metre <= 150:
        return DuplicateKarari.INSAN_INCELEMESI
    if (ayni_telefon or (ayni_website and mesafe_metre <= 150)) and not ayni_kaynak_id:
        return DuplicateKarari.INSAN_INCELEMESI
    return DuplicateKarari.AYRI_TUT
