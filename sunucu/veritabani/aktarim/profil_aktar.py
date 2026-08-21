"""
YerProfili (JSONL) -> Yer.yer_profili / Yer.duygu_ozeti (PostgreSQL) aktarimi.

Baglanti, `YerProfili.yer_kimligi` (isim+enlem+boylam'dan turetilen
deterministik hash, bkz. `veri/ortak/birlesik_yer_modeli.py::BirlesikYer.yer_kimligi`)
uzerinden yapilir. Bu hash'i veritabani id'sine cevirmek icin, aktarimin
yer asamasinda (`yer_aktar.py`) kurulan `{yer_kimligi: yer_id}` haritasi
kullanilir -- bu yuzden profil aktarimi HER ZAMAN yer aktariminDAN SONRA
calistirilmalidir (bkz. `calistir.py` siralamasi).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from sunucu.veritabani.modeller import Yer
from veri.ortak.yer_profili_modeli import YerProfili


@dataclass
class ProfilAktarimSonucu:
    guncellenen: int = 0
    eslenemeyen: int = 0


def profilleri_aktar(
    oturum: Session,
    yer_kimligi_haritasi: dict[str, str],
    profiller: list[YerProfili],
) -> ProfilAktarimSonucu:
    sonuc = ProfilAktarimSonucu()

    for profil in profiller:
        yer_id = yer_kimligi_haritasi.get(profil.yer_kimligi)
        if yer_id is None:
            sonuc.eslenemeyen += 1
            continue

        yer = oturum.get(Yer, yer_id)
        if yer is None:
            sonuc.eslenemeyen += 1
            continue

        yer.yer_profili = profil.model_dump(mode="json", exclude={"yer_kimligi", "yer_ismi", "duygu_ozeti"})
        yer.duygu_ozeti = profil.duygu_ozeti
        yer.duygu_son_guncelleme = datetime.now(timezone.utc)
        sonuc.guncellenen += 1

    oturum.flush()
    return sonuc
