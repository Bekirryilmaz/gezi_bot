"""Dusuk risk yapisal OSM adaylari icin grup inceleme; kor otomatik yayin yoktur."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from fastapi import HTTPException, status
from ortak.sabitler import GRUP_INCELEME_DUSUK_RISK_AILELERI, GRUP_INCELEME_KRITIK_AILELER
from sqlalchemy.orm import Session

from sunucu.admin.audit import audit_yaz
from sunucu.admin.kuyruk_triyaj import DUSUK_RISK_AILELERI
from sunucu.admin.workflow import _komutu_uygula, nesne_yetkisini_dogrula
from sunucu.auth.rbac import Yetki
from sunucu.auth.servis import AdminBaglami
from sunucu.bilgi.calisma_saati import calisma_saati_degerini_al, calisma_saatini_ayristir
from sunucu.veritabani.admin_modelleri import IncelemeDosyasi
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu

GRUP_AZAMI = 80
_ONAY_EYLEMLERI = frozenset({"claim_approve", "grup_dusuk_risk_inceleme"})


@dataclass
class GrupIncelemeSonucu:
    onaylanan: list[str] = field(default_factory=list)
    atlanan: list[dict[str, str]] = field(default_factory=list)
    hatalar: list[dict[str, str]] = field(default_factory=list)
    otomatik_yayin: bool = False

    def sozluk(self) -> dict[str, Any]:
        return {
            "onaylanan": list(self.onaylanan),
            "atlanan": list(self.atlanan),
            "hatalar": list(self.hatalar),
            "otomatik_yayin": False,
        }


def _iddia_surumu(oturum: Session, iddia: Iddia) -> IddiaSurumu | None:
    if not iddia.aktif_surum_no:
        return None
    return (
        oturum.query(IddiaSurumu)
        .filter_by(iddia_id=iddia.id, surum_no=iddia.aktif_surum_no)
        .first()
    )


def grup_inceleme_guvenli_mi(dosya: IncelemeDosyasi, iddia: Iddia | None) -> tuple[bool, str]:
    if dosya.durum == "tamamlandi":
        return False, "dosya_tamamlandi"
    if dosya.dosya_turu != "claim_candidate":
        return False, "dosya_turu_uygunsuz"
    if iddia is None:
        return False, "iddia_yok"
    if iddia.aile in GRUP_INCELEME_KRITIK_AILELER:
        return False, "kritik_aile_grup_yayini_yasak"
    if (
        iddia.aile not in GRUP_INCELEME_DUSUK_RISK_AILELERI
        and iddia.aile not in DUSUK_RISK_AILELERI
    ):
        return False, "aile_dusuk_risk_degil"
    if dosya.triyaj_sinifi and dosya.triyaj_sinifi not in {"dusuk_risk", None}:
        if dosya.triyaj_sinifi == "yuksek_risk":
            return False, "yuksek_risk_grup_yayini_yasak"
    return True, "uygun"


def grup_incelemeyi_uygula(
    oturum: Session,
    *,
    baglam: AdminBaglami,
    dosya_idleri: list[str],
    gerekce: str,
    istek_id: str,
    eylem: str = "claim_approve",
) -> GrupIncelemeSonucu:
    if Yetki.YAYINLA not in baglam.yetkiler:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Grup inceleme icin yayin yetkisi gerekir.",
        )
    if not gerekce or len(gerekce.strip()) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Grup inceleme gerekcesi en az 8 karakter olmalidir.",
        )
    if eylem not in _ONAY_EYLEMLERI:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Grup inceleme yalniz claim_approve destekler.",
        )
    if not dosya_idleri:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Dosya listesi bos olamaz."
        )
    if len(dosya_idleri) > GRUP_AZAMI:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Grup en fazla {GRUP_AZAMI} dosya alabilir.",
        )
    if len(set(dosya_idleri)) != len(dosya_idleri):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tekrarlayan dosya kimligi var.",
        )

    dosyalar = (
        oturum.query(IncelemeDosyasi)
        .filter(IncelemeDosyasi.id.in_(dosya_idleri))
        .with_for_update()
        .all()
    )
    by_id = {str(d.id): d for d in dosyalar}
    if len(by_id) != len(dosya_idleri):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bazi inceleme dosyalari bulunamadi."
        )

    aileler: set[str] = set()
    for dosya in dosyalar:
        iddia = oturum.get(Iddia, dosya.nesne_id)
        aileler.add(iddia.aile if iddia is not None else "")
    if len(aileler) != 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Grup inceleme tek aile olmalidir.",
        )

    sonuc = GrupIncelemeSonucu()
    for dosya_id in dosya_idleri:
        dosya = by_id[dosya_id]
        nesne_yetkisini_dogrula(oturum, baglam, dosya.nesne_turu, dosya.nesne_id)
        iddia = oturum.get(Iddia, dosya.nesne_id)
        uygun, neden = grup_inceleme_guvenli_mi(dosya, iddia)
        if not uygun:
            sonuc.atlanan.append({"dosya_id": dosya_id, "neden": neden})
            continue
        assert iddia is not None
        if iddia.aile == "calisma_saatleri":
            surum = _iddia_surumu(oturum, iddia)
            ham = calisma_saati_degerini_al(surum.deger if surum else None)
            ayristirma = calisma_saatini_ayristir(ham)
            if not ayristirma.sozdizimi_gecerli:
                sonuc.atlanan.append(
                    {"dosya_id": dosya_id, "neden": f"saat_sozdizimi_{ayristirma.neden}"}
                )
                continue
            if surum is not None:
                govde = dict(surum.deger or {})
                govde["normalize"] = ayristirma.normalize
                govde["sozdizimi_gecerli"] = True
                govde["zaman_kapsami"] = "haftalik"
                govde["her_zaman_acik"] = ayristirma.her_zaman_acik
                surum.deger = govde
        dosya.onerilen_eylem = "claim_approve"
        try:
            _komutu_uygula(oturum, dosya, baglam.kullanici.id, gerekce.strip(), istek_id)
        except HTTPException as hata:
            detay = hata.detail
            mesaj = detay if isinstance(detay, str) else str(detay)
            sonuc.hatalar.append({"dosya_id": dosya_id, "neden": mesaj})
            continue
        sonuc.onaylanan.append(dosya_id)
    audit_yaz(
        oturum,
        aktor_id=baglam.kullanici.id,
        eylem="grup_inceleme",
        nesne_turu="inceleme_grubu",
        nesne_id=istek_id,
        onceki=None,
        yeni={
            "onaylanan": len(sonuc.onaylanan),
            "atlanan": len(sonuc.atlanan),
            "otomatik_yayin": False,
        },
        gerekce=gerekce.strip(),
        istek_id=istek_id,
    )
    return sonuc
