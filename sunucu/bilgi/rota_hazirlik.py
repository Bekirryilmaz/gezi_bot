"""Rota hazirlik durumu: skor degil, aciklanabilir ic state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ortak.sabitler import (
    ONERIYE_UYGUN_KIMLIK_SINIFLARI,
    CalismaSaatiDurumu,
    KimlikKaliteSinifi,
    RotaHazirlikDurumu,
    RotaHazirlikNedeni,
    TamamlikHucresi,
)


@dataclass(frozen=True)
class RotaHazirlikGirdisi:
    kimlik_sinifi: str
    sube_durum: str
    koordinat_gecerli: bool
    ilce_id: str | None
    amaclar: tuple[str, ...]
    yayin_uygun: bool
    calisma_saati: TamamlikHucresi
    calisma_saati_durumu: CalismaSaatiDurumu | None = None


@dataclass(frozen=True)
class RotaHazirlikOzeti:
    durum: RotaHazirlikDurumu
    neden_kodlari: tuple[str, ...]
    kirilim: dict[str, Any]

    def sozluk(self) -> dict[str, Any]:
        return {
            "durum": self.durum.value,
            "neden_kodlari": list(self.neden_kodlari),
            "kirilim": dict(self.kirilim),
        }


def rota_hazirligini_hesapla(girdi: RotaHazirlikGirdisi) -> RotaHazirlikOzeti:
    nedenler: list[str] = []
    kimlik = girdi.kimlik_sinifi
    if girdi.sube_durum != "aktif":
        nedenler.append(RotaHazirlikNedeni.SUBE_AKTIF_DEGIL.value)
        return _kapali(nedenler, girdi)
    if kimlik == KimlikKaliteSinifi.KARANTINA.value or not girdi.koordinat_gecerli:
        if kimlik == KimlikKaliteSinifi.KARANTINA.value:
            nedenler.append(RotaHazirlikNedeni.KIMLIK_KARANTINA.value)
        if not girdi.koordinat_gecerli:
            nedenler.append(RotaHazirlikNedeni.KOORDINAT_GECERSIZ.value)
        return _kapali(nedenler, girdi)

    if kimlik == KimlikKaliteSinifi.SUPHELI.value:
        nedenler.append(RotaHazirlikNedeni.KIMLIK_SUPHELI.value)
    elif kimlik in ONERIYE_UYGUN_KIMLIK_SINIFLARI:
        nedenler.append(RotaHazirlikNedeni.KIMLIK_UYGUN.value)
    else:
        nedenler.append(RotaHazirlikNedeni.KIMLIK_SUPHELI.value)

    if girdi.koordinat_gecerli:
        nedenler.append(RotaHazirlikNedeni.KOORDINAT_UYGUN.value)
    if girdi.ilce_id:
        nedenler.append(RotaHazirlikNedeni.ILCE_UYGUN.value)
    else:
        nedenler.append(RotaHazirlikNedeni.ILCE_EKSIK.value)
    if girdi.amaclar:
        nedenler.append(RotaHazirlikNedeni.AMAC_BILINIYOR.value)
    else:
        nedenler.append(RotaHazirlikNedeni.AMAC_BILINMIYOR.value)
    if girdi.yayin_uygun:
        nedenler.append(RotaHazirlikNedeni.YAYIN_UYGUN.value)
    else:
        nedenler.append(RotaHazirlikNedeni.YAYIN_UYGUN_DEGIL.value)

    saat_durumu = girdi.calisma_saati_durumu
    if saat_durumu is CalismaSaatiDurumu.PARTIALLY_KNOWN:
        nedenler.append(RotaHazirlikNedeni.CALISMA_SAATI_PARCALI.value)
    elif saat_durumu is CalismaSaatiDurumu.STALE:
        nedenler.append(RotaHazirlikNedeni.CALISMA_SAATI_ESKIMIS.value)
    elif saat_durumu is CalismaSaatiDurumu.INVALID:
        nedenler.append(RotaHazirlikNedeni.CALISMA_SAATI_GECERSIZ.value)
    elif girdi.calisma_saati is TamamlikHucresi.BILINIYOR:
        nedenler.append(RotaHazirlikNedeni.CALISMA_SAATI_BILINIYOR.value)
    elif girdi.calisma_saati is TamamlikHucresi.YALNIZ_DAHILI:
        nedenler.append(RotaHazirlikNedeni.CALISMA_SAATI_YALNIZ_DAHILI.value)
    elif girdi.calisma_saati is TamamlikHucresi.CELISKILI:
        nedenler.append(RotaHazirlikNedeni.CALISMA_SAATI_GECERSIZ.value)
    else:
        nedenler.append(RotaHazirlikNedeni.CALISMA_SAATI_BILINMIYOR.value)

    temel_eksik = (
        kimlik not in ONERIYE_UYGUN_KIMLIK_SINIFLARI
        or not girdi.ilce_id
        or not girdi.amaclar
        or not girdi.yayin_uygun
    )
    if temel_eksik:
        if RotaHazirlikNedeni.ROTA_KRITIK_EKSIK.value not in nedenler:
            nedenler.append(RotaHazirlikNedeni.ROTA_KRITIK_EKSIK.value)
        return RotaHazirlikOzeti(
            durum=RotaHazirlikDurumu.KESIF_ADAYI,
            neden_kodlari=tuple(nedenler),
            kirilim=_kirilim(girdi, RotaHazirlikDurumu.KESIF_ADAYI),
        )

    saat_hazir = girdi.calisma_saati is TamamlikHucresi.BILINIYOR and saat_durumu in {
        None,
        CalismaSaatiDurumu.KNOWN,
    }
    if saat_hazir:
        return RotaHazirlikOzeti(
            durum=RotaHazirlikDurumu.ROTA_HAZIR,
            neden_kodlari=tuple(nedenler),
            kirilim=_kirilim(girdi, RotaHazirlikDurumu.ROTA_HAZIR),
        )
    return RotaHazirlikOzeti(
        durum=RotaHazirlikDurumu.ROTA_SINIRLI,
        neden_kodlari=tuple(nedenler),
        kirilim=_kirilim(girdi, RotaHazirlikDurumu.ROTA_SINIRLI),
    )


def _kapali(nedenler: list[str], girdi: RotaHazirlikGirdisi) -> RotaHazirlikOzeti:
    return RotaHazirlikOzeti(
        durum=RotaHazirlikDurumu.ROTA_KAPALI,
        neden_kodlari=tuple(nedenler),
        kirilim=_kirilim(girdi, RotaHazirlikDurumu.ROTA_KAPALI),
    )


def _kirilim(girdi: RotaHazirlikGirdisi, durum: RotaHazirlikDurumu) -> dict[str, Any]:
    return {
        "durum": durum.value,
        "kimlik_sinifi": girdi.kimlik_sinifi,
        "sube_durum": girdi.sube_durum,
        "koordinat_gecerli": girdi.koordinat_gecerli,
        "ilce_var": bool(girdi.ilce_id),
        "amaclar": list(girdi.amaclar),
        "yayin_uygun": girdi.yayin_uygun,
        "calisma_saati": girdi.calisma_saati.value,
        "calisma_saati_durumu": (
            girdi.calisma_saati_durumu.value if girdi.calisma_saati_durumu else None
        ),
        "kamusal_skor": False,
    }
