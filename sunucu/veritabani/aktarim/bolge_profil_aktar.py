"""
BolgeProfili (JSONL) -> bolge_profilleri (PostgreSQL) aktarimi.

`(sehir_id, bolge_adi)` unique kisitina gore upsert yapar -- yani bu betik
IDEMPOTENTTIR, defalarca calistirilabilir (ayni bolge tekrar tekrar
EKLENMEZ, sadece guncellenir). yer_aktar.py/yorum_aktar.py'nin idempotentlik
felsefesiyle AYNIDIR.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from sunucu.veritabani.modeller import BolgeProfili as BolgeProfiliTablosu
from veri.ortak.bolge_profili_modeli import BolgeProfili


@dataclass
class BolgeProfilAktarimSonucu:
    eklenen: int = 0
    guncellenen: int = 0


def _var_olan_bolgeyi_bul(oturum: Session, sehir_id: str, bolge_adi: str) -> BolgeProfiliTablosu | None:
    return (
        oturum.query(BolgeProfiliTablosu)
        .filter(BolgeProfiliTablosu.sehir_id == sehir_id, BolgeProfiliTablosu.bolge_adi == bolge_adi)
        .first()
    )


def bolge_profillerini_aktar(
    oturum: Session,
    sehir_id: str,
    profiller: list[BolgeProfili],
) -> BolgeProfilAktarimSonucu:
    sonuc = BolgeProfilAktarimSonucu()

    for profil in profiller:
        satir = _var_olan_bolgeyi_bul(oturum, sehir_id, profil.bolge_adi)
        konular_json = [konu.model_dump(mode="json") for konu in profil.on_plana_cikan_konular]

        if satir is None:
            satir = BolgeProfiliTablosu(
                sehir_id=sehir_id,
                bolge_adi=profil.bolge_adi,
                ilce_mi=profil.ilce_mi,
                genel_duygu_skoru=profil.genel_duygu_skoru,
                genel_duygu_etiketi=profil.genel_duygu_etiketi.value if profil.genel_duygu_etiketi else None,
                on_plana_cikan_konular=konular_json,
                kullanilan_yorum_sayisi=profil.kullanilan_yorum_sayisi,
                duygu_ozeti=profil.duygu_ozeti,
            )
            oturum.add(satir)
            sonuc.eklenen += 1
        else:
            satir.ilce_mi = profil.ilce_mi
            satir.genel_duygu_skoru = profil.genel_duygu_skoru
            satir.genel_duygu_etiketi = profil.genel_duygu_etiketi.value if profil.genel_duygu_etiketi else None
            satir.on_plana_cikan_konular = konular_json
            satir.kullanilan_yorum_sayisi = profil.kullanilan_yorum_sayisi
            satir.duygu_ozeti = profil.duygu_ozeti
            sonuc.guncellenen += 1

    oturum.flush()
    return sonuc
