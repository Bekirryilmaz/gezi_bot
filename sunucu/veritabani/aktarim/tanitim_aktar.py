"""tanitim_metni JSONL -> yerler / bolge_profilleri aktarimi."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from sunucu.veritabani.modeller import BolgeProfili, Yer


@dataclass
class TanitimAktarimSonucu:
    yer_guncellenen: int = 0
    bolge_guncellenen: int = 0
    yer_eslenemeyen: int = 0


def yer_tanitimlarini_aktar(
    oturum: Session,
    yer_kimligi_haritasi: dict[str, str],
    kayitlar: list[dict],
) -> TanitimAktarimSonucu:
    sonuc = TanitimAktarimSonucu()
    for kayit in kayitlar:
        yer_id = yer_kimligi_haritasi.get(kayit.get("yer_kimligi", ""))
        if not yer_id:
            sonuc.yer_eslenemeyen += 1
            continue
        yer = oturum.get(Yer, yer_id)
        if yer is None:
            sonuc.yer_eslenemeyen += 1
            continue
        yer.tanitim_metni = kayit.get("tanitim_metni")
        # Yorumsuz yerlerde duygu_ozeti bos ise yapisal metni deneyim alanina yazma
        # burada yapilmaz -- profil_pipeline/fallback ayri
        sonuc.yer_guncellenen += 1
    oturum.flush()
    return sonuc


def bolge_tanitimlarini_aktar(oturum: Session, sehir_id: str, kayitlar: list[dict]) -> int:
    guncellenen = 0
    for kayit in kayitlar:
        profil = (
            oturum.query(BolgeProfili)
            .filter(BolgeProfili.sehir_id == sehir_id, BolgeProfili.bolge_adi == kayit["bolge_adi"])
            .first()
        )
        if profil is None:
            continue
        profil.tanitim_metni = kayit.get("tanitim_metni")
        guncellenen += 1
    oturum.flush()
    return guncellenen
