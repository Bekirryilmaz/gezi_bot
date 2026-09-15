"""Dahili NLP adaylarini aggregate projection'a ve sube auditine cevirir."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from statistics import quantiles
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from sunucu.bilgi.aggregation import (
    AGREGASYON_SURUMU,
    SignalObservation,
    aggregate,
    dahili_tercih_kapisi,
    guven_sinifini_uygula,
)
from sunucu.veritabani.bilgi_modelleri import DahiliGozlemAdayi, DahiliSinyalOzeti
from sunucu.veritabani.modeller import Yer, YerKaynak


def adaylardan_gozlemler(
    oturum: Session,
    *,
    sube_idleri: list[str] | None = None,
) -> list[SignalObservation]:
    sorgu = select(DahiliGozlemAdayi).where(DahiliGozlemAdayi.sube_id.is_not(None))
    if sube_idleri:
        sorgu = sorgu.where(DahiliGozlemAdayi.sube_id.in_(sube_idleri))
    gozlemler = []
    for aday in oturum.scalars(sorgu):
        gozlemler.append(
            SignalObservation(
                branch_id=str(aday.sube_id),
                family=aday.aile,
                evidence_id=aday.dahili_referans or aday.span_hash,
                source=aday.kaynak,
                direction=aday.yon,
                observed_at=aday.gozlem_zamani,
                valid_until=None,
                branch_confidence="verified"
                if aday.sube_guven_durumu == "eslesti"
                else "unknown",
                rights_status="allowed",
                verified=False,
                observation_id=str(aday.yorum_id),
                epistemic_type=aday.gozlem_turu,
                review_id=str(aday.yorum_id),
                kullanim_durumu=aday.kullanim_durumu,
            )
        )
    return gozlemler


def dagilimdan_esikler(unique_review_sayilari: list[int]) -> dict[str, int]:
    sayilar = sorted(int(deger) for deger in unique_review_sayilari if deger > 0)
    if not sayilar:
        return {"zayif_max_unique_review": 1, "orta_max_unique_review": 2}
    if len(sayilar) < 3:
        orta = max(sayilar[0], sayilar[-1])
        return {
            "zayif_max_unique_review": sayilar[0],
            "orta_max_unique_review": max(sayilar[0] + 1, orta),
        }
    kesitler = quantiles(sayilar, n=3, method="inclusive")
    zayif_max = max(1, int(kesitler[0]))
    orta_max = max(zayif_max + 1, int(kesitler[1]))
    return {
        "zayif_max_unique_review": zayif_max,
        "orta_max_unique_review": orta_max,
    }


def ozetleri_yaz(
    oturum: Session,
    gozlemler: list[SignalObservation],
    *,
    esikler: dict[str, int] | None = None,
) -> list[dict[str, Any]]:
    sinyaller = aggregate(gozlemler)
    if esikler is None:
        esikler = dagilimdan_esikler(
            [int(sinyal["unique_review_count"]) for sinyal in sinyaller]
        )
    yazilan = []
    for sinyal in sinyaller:
        kalibre = guven_sinifini_uygula(sinyal, esikler)
        tercih = dahili_tercih_kapisi(kalibre)
        ozet = {
            **kalibre,
            "preference_eligible": tercih["preference_eligible"],
            "hard_constraint_eligible": False,
        }
        degerler = {
            "sube_id": ozet["branch_id"],
            "aile": ozet["family"],
            "agregasyon_surumu": AGREGASYON_SURUMU,
            "guven_sinifi": ozet["guven_sinifi"],
            "durum": ozet["durum"],
            "ozet": ozet,
            "kirilim": ozet.get("kirilim") or {},
            "hesaplanma_zamani": datetime.now(UTC),
        }
        sorgu = insert(DahiliSinyalOzeti).values(**degerler)
        oturum.execute(
            sorgu.on_conflict_do_update(
                constraint="ux_dahili_sinyal_ozeti_sube_aile_surumu",
                set_={
                    "guven_sinifi": degerler["guven_sinifi"],
                    "durum": degerler["durum"],
                    "ozet": degerler["ozet"],
                    "kirilim": degerler["kirilim"],
                    "hesaplanma_zamani": degerler["hesaplanma_zamani"],
                },
            )
        )
        yazilan.append(ozet)
    oturum.flush()
    return yazilan


def sube_kaynak_audit(oturum: Session, *, sehir_id: str) -> dict[str, Any]:
    """Ayni subedeki birden cok Google kaynak kaydini mesafe ve isimle denetler."""
    satirlar = list(
        oturum.execute(
            select(
                YerKaynak.sube_id,
                YerKaynak.kaynak_id,
                YerKaynak.yer_id,
                Yer.isim,
                Yer.ana_kategori,
                Yer.alt_kategori,
            )
            .join(Yer, Yer.id == YerKaynak.yer_id)
            .where(
                Yer.sehir_id == sehir_id,
                YerKaynak.kaynak == "google_maps",
            )
        )
    )
    gruplar: dict[str, list[Any]] = {}
    for satir in satirlar:
        gruplar.setdefault(str(satir.sube_id), []).append(satir)
    coklu = {sube_id: kayitlar for sube_id, kayitlar in gruplar.items() if len(kayitlar) > 1}
    supheli = 0
    for kayitlar in coklu.values():
        isimler = {kayit.isim for kayit in kayitlar}
        kategoriler = {(kayit.ana_kategori, kayit.alt_kategori) for kayit in kayitlar}
        yer_idleri = {kayit.yer_id for kayit in kayitlar}
        farkli_konum = False
        if len(yer_idleri) > 1:
            ilk_id, son_id = list(yer_idleri)[0], list(yer_idleri)[-1]
            yer_a = Yer.__table__.alias("yer_a")
            yer_b = Yer.__table__.alias("yer_b")
            mesafe = oturum.scalar(
                select(func.ST_Distance(yer_a.c.konum, yer_b.c.konum)).where(
                    yer_a.c.id == ilk_id,
                    yer_b.c.id == son_id,
                )
            )
            farkli_konum = mesafe is not None and float(mesafe) > 30
        if len(isimler) > 1 or len(kategoriler) > 1 or farkli_konum:
            supheli += 1
    return {
        "google_kaynak_kaydi": len(satirlar),
        "google_sube": len(gruplar),
        "google_coklu_kaynak_sube": len(coklu),
        "fiziksel_sube_supheli": supheli,
    }


def sehir_ozetlerini_yenile(oturum: Session, *, sehir_id: str) -> dict[str, Any]:
    sube_idleri = list(
        oturum.scalars(
            select(YerKaynak.sube_id)
            .join(Yer, Yer.id == YerKaynak.yer_id)
            .where(Yer.sehir_id == sehir_id)
            .distinct()
        )
    )
    gozlemler = adaylardan_gozlemler(oturum, sube_idleri=[str(kimlik) for kimlik in sube_idleri])
    ham = aggregate(gozlemler)
    esikler = dagilimdan_esikler([int(sinyal["unique_review_count"]) for sinyal in ham])
    yazilan = ozetleri_yaz(oturum, gozlemler, esikler=esikler)
    siniflar = Counter(sinyal["guven_sinifi"] for sinyal in yazilan)
    tercih = sum(1 for sinyal in yazilan if sinyal.get("preference_eligible"))
    return {
        "aday_gozlem": len(gozlemler),
        "ozet": len(yazilan),
        "esikler": esikler,
        "guven_sinifi": dict(siniflar),
        "preference_eligible": tercih,
        "audit": sube_kaynak_audit(oturum, sehir_id=sehir_id),
    }


def sehir_id_bul(oturum: Session, sehir_anahtari: str) -> str:
    from sunucu.veritabani.modeller import Sehir
    from veri.ortak.sehir_ayarlari import sehir_getir

    isim = sehir_getir(sehir_anahtari).isim
    sehir = oturum.scalar(select(Sehir).where(Sehir.isim == isim))
    if sehir is None:
        raise ValueError(f"Sehir bulunamadi: {sehir_anahtari}")
    return sehir.id


def kalibrasyon_raporu(oturum: Session, *, sehir_id: str) -> dict[str, Any]:
    ozetler = list(
        oturum.scalars(
            select(DahiliSinyalOzeti).where(DahiliSinyalOzeti.agregasyon_surumu == AGREGASYON_SURUMU)
        )
    )
    unique_sayilari = [
        int((ozet.ozet or {}).get("unique_review_count") or 0) for ozet in ozetler
    ]
    esikler = dagilimdan_esikler(unique_sayilari)
    aileler = Counter(ozet.aile for ozet in ozetler)
    siniflar = Counter(ozet.guven_sinifi for ozet in ozetler)
    tercih = sum(1 for ozet in ozetler if (ozet.ozet or {}).get("preference_eligible"))
    return {
        "ozet": len(ozetler),
        "esikler": esikler,
        "aileler": dict(aileler),
        "guven_sinifi": dict(siniflar),
        "preference_eligible": tercih,
        "unique_review_p50": sorted(unique_sayilari)[len(unique_sayilari) // 2] if unique_sayilari else 0,
        "audit": sube_kaynak_audit(oturum, sehir_id=sehir_id),
    }


def pilot_yerleri_sec(oturum: Session, *, sehir_id: str, hedef: int = 50) -> dict[str, Any]:
    from sunucu.veritabani.kimlik_modelleri import Sube
    from sunucu.veritabani.modeller import Yer

    satirlar = oturum.execute(
        select(DahiliSinyalOzeti, Sube, Yer)
        .join(Sube, Sube.id == DahiliSinyalOzeti.sube_id)
        .join(Yer, Yer.id == Sube.legacy_yer_id)
        .where(
            Yer.sehir_id == sehir_id,
            DahiliSinyalOzeti.agregasyon_surumu == AGREGASYON_SURUMU,
            DahiliSinyalOzeti.durum != "karar_disi",
        )
    ).all()
    yerler: dict[str, dict[str, Any]] = {}
    for ozet, sube, yer in satirlar:
        govde = dict(ozet.ozet or {})
        kayit = yerler.setdefault(
            yer.id,
            {
                "yer_id": yer.id,
                "sube_id": sube.id,
                "isim": yer.isim,
                "alt_kategori": yer.alt_kategori,
                "aileler": [],
                "unique_review": 0,
                "preference_eligible": 0,
                "conflict": 0,
            },
        )
        kayit["aileler"].append(ozet.aile)
        kayit["unique_review"] = max(kayit["unique_review"], int(govde.get("unique_review_count") or 0))
        if govde.get("preference_eligible"):
            kayit["preference_eligible"] += 1
        if govde.get("conflict_level") in {"medium", "high"}:
            kayit["conflict"] += 1
    adaylar = sorted(
        (kayit for kayit in yerler.values() if kayit["preference_eligible"] > 0),
        key=lambda kayit: (kayit["preference_eligible"], kayit["unique_review"], -kayit["conflict"]),
        reverse=True,
    )
    secilen: list[dict[str, Any]] = []
    kategoriler: set[str] = set()
    for kayit in adaylar:
        if len(secilen) >= hedef:
            break
        if kayit["alt_kategori"] not in kategoriler or len(kategoriler) >= 8:
            secilen.append(kayit)
            kategoriler.add(kayit["alt_kategori"])
    return {
        "hedef": hedef,
        "aday": len(adaylar),
        "secilen": len(secilen),
        "kategoriler": sorted(kategoriler),
        "yerler": secilen,
    }
