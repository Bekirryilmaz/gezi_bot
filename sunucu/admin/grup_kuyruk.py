"""Grup inceleme icin aile bazinda bekleyen dosya listesi."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from ortak.sabitler import GRUP_INCELEME_DUSUK_RISK_AILELERI, GRUP_INCELEME_KRITIK_AILELER
from sqlalchemy import String, cast
from sqlalchemy.orm import Session

from sunucu.admin.grup_inceleme import grup_inceleme_guvenli_mi
from sunucu.admin.kuyruk_triyaj import DUSUK_RISK_AILELERI
from sunucu.bilgi.calisma_saati import calisma_saati_degerini_al, calisma_saatini_ayristir
from sunucu.veritabani.admin_modelleri import IncelemeDosyasi
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu
from sunucu.veritabani.kimlik_modelleri import Sube
from sunucu.veritabani.modeller import Yer


def _surum(oturum: Session, iddia: Iddia) -> IddiaSurumu | None:
    if not iddia.aktif_surum_no:
        return None
    return (
        oturum.query(IddiaSurumu)
        .filter_by(iddia_id=iddia.id, surum_no=iddia.aktif_surum_no)
        .first()
    )


def grup_adaylarini_listele(
    oturum: Session,
    *,
    aile: str | None = None,
    sube_idleri: set[str] | None = None,
    yalniz_dusuk_risk: bool = True,
    azami: int = 400,
) -> list[dict[str, Any]]:
    sorgu = (
        oturum.query(IncelemeDosyasi, Iddia, Sube, Yer)
        .join(Iddia, cast(Iddia.id, String) == IncelemeDosyasi.nesne_id)
        .join(Sube, Sube.id == Iddia.sube_id)
        .join(Yer, Yer.id == Sube.legacy_yer_id)
        .filter(
            IncelemeDosyasi.durum != "tamamlandi",
            IncelemeDosyasi.dosya_turu == "claim_candidate",
            IncelemeDosyasi.nesne_turu == "claim",
        )
    )
    if aile:
        sorgu = sorgu.filter(Iddia.aile == aile)
    if sube_idleri:
        sorgu = sorgu.filter(Iddia.sube_id.in_(list(sube_idleri)))
    kayitlar: list[dict[str, Any]] = []
    for dosya, iddia, sube, yer in sorgu.order_by(
        IncelemeDosyasi.oncelik_puani.desc(), Sube.guncel_isim, Iddia.aile
    ).limit(azami):
        if yalniz_dusuk_risk and (
            iddia.aile in GRUP_INCELEME_KRITIK_AILELER
            or (
                iddia.aile not in GRUP_INCELEME_DUSUK_RISK_AILELERI
                and iddia.aile not in DUSUK_RISK_AILELERI
            )
        ):
            continue
        uygun, neden = grup_inceleme_guvenli_mi(dosya, iddia)
        surum = _surum(oturum, iddia)
        deger = surum.deger if surum else None
        saat_gecerli = None
        if iddia.aile == "calisma_saatleri":
            ayristirma = calisma_saatini_ayristir(calisma_saati_degerini_al(deger))
            saat_gecerli = ayristirma.sozdizimi_gecerli
            if not saat_gecerli:
                uygun = False
                neden = f"saat_sozdizimi_{ayristirma.neden}"
        kayitlar.append(
            {
                "dosya_id": dosya.id,
                "iddia_id": iddia.id,
                "sube_id": iddia.sube_id,
                "mekan_adi": sube.guncel_isim or yer.isim,
                "aile": iddia.aile,
                "durum": dosya.durum,
                "triyaj_sinifi": dosya.triyaj_sinifi,
                "oncelik_puani": dosya.oncelik_puani,
                "candidate_deger": deger.get("deger") if isinstance(deger, dict) else deger,
                "grup_uygun": uygun,
                "grup_neden": neden,
                "saat_sozdizimi_gecerli": saat_gecerli,
            }
        )
    return kayitlar


def grup_ozetini_kur(kayitlar: list[dict[str, Any]]) -> dict[str, Any]:
    aileler: dict[str, dict[str, int]] = defaultdict(
        lambda: {"toplam": 0, "uygun": 0, "atlanan": 0}
    )
    for kayit in kayitlar:
        kova = aileler[kayit["aile"]]
        kova["toplam"] += 1
        if kayit["grup_uygun"]:
            kova["uygun"] += 1
        else:
            kova["atlanan"] += 1
    return {
        "kayitlar": kayitlar,
        "aile_ozeti": dict(aileler),
        "toplam": len(kayitlar),
        "uygun": sum(1 for k in kayitlar if k["grup_uygun"]),
        "otomatik_yayin": False,
    }
