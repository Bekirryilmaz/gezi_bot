from __future__ import annotations

import argparse
import json
import uuid
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any

from geoalchemy2 import Geometry
from ortak.cografya_araclari import haversine_metre
from ortak.sabitler import AnaKategori, KimlikKaliteSinifi
from sqlalchemy import cast, func, select
from sqlalchemy.orm import Session
from veri.ortak.sehir_ayarlari import sehir_anahtarini_isme_gore_bul
from veri.toplayicilar.ortak_araclar import metinden_kategori_esle

from sunucu.arama.normalizasyon import turkce_arama_normalize
from sunucu.kimlik.kalite import (
    DuplicateKarari,
    duplicate_kararini_ver,
    kimlik_kalitesini_hesapla,
    oneriye_uygun_mu,
)
from sunucu.veritabani.admin_modelleri import IncelemeDosyasi
from sunucu.veritabani.baglanti import OturumUretici
from sunucu.veritabani.kimlik_modelleri import EslemeAdayi, Sube, YerKimligi
from sunucu.veritabani.modeller import Sehir, Yer, YerKaynak

_KIMLIK_INCELEME = "kimlik_inceleme"
_KARANTINA = "karantina"
_KAYNAK_ETIKETI_KATEGORI_DUZELTMESI = frozenset({"internet_kafe", "tatli_pastane"})


def kaynak_etiketinden_kategori_duzelt(isim: str, alt_kategori: str | None) -> str | None:
    """Isimdeki kaynak etiketi, kahve/restoran kimligini daha ozel taksonomiye ceker."""
    eslesen = metinden_kategori_esle(isim)
    if eslesen is None:
        return None
    hedef = eslesen[1]
    if hedef == alt_kategori:
        return None
    if hedef in _KAYNAK_ETIKETI_KATEGORI_DUZELTMESI:
        return hedef
    return None


def _uuid5(anahtar: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"samandira:kimlik:{anahtar}"))


def _kategori_kaynak_uyumu(alt_kategori: str, isim: str, ozellikler: dict | None) -> bool:
    if kaynak_etiketinden_kategori_duzelt(isim, alt_kategori):
        return False
    mutfak = str((ozellikler or {}).get("cuisine") or "").casefold()
    if alt_kategori in {"kafe", "kahve_uzmanlik"} and any(
        parca in mutfak for parca in ("kebab", "steak", "seafood", "fish")
    ):
        return False
    return True


def kimlik_auditini_calistir(oturum: Session, *, sehir_id: str, dry_run: bool = False) -> dict[str, Any]:
    sehir = oturum.get(Sehir, sehir_id)
    if sehir is None:
        raise ValueError("sehir bulunamadi")
    sehir_anahtari = sehir_anahtarini_isme_gore_bul(sehir.isim) or sehir.arama_isim
    enlem = func.ST_Y(cast(Yer.konum, Geometry))
    boylam = func.ST_X(cast(Yer.konum, Geometry))
    satirlar = list(
        oturum.execute(
            select(Yer, Sube, YerKimligi, enlem.label("enlem"), boylam.label("boylam"))
            .join(Sube, Sube.legacy_yer_id == Yer.id)
            .join(YerKimligi, YerKimligi.id == Sube.yer_kimligi_id)
            .where(Yer.sehir_id == sehir_id)
        )
    )
    kaynak_sayilari: dict[str, int] = defaultdict(int)
    kaynak_id_sube: dict[tuple[str, str], list[str]] = defaultdict(list)
    for kaynak in oturum.scalars(select(YerKaynak).join(Yer, Yer.id == YerKaynak.yer_id).where(Yer.sehir_id == sehir_id)):
        kaynak_sayilari[str(kaynak.sube_id)] += 1
        kaynak_id_sube[(kaynak.kaynak, kaynak.kaynak_id)].append(str(kaynak.sube_id))

    isim_gruplari: dict[str, list[Any]] = defaultdict(list)
    for satir in satirlar:
        isim_gruplari[turkce_arama_normalize(satir.Yer.isim)].append(satir)

    yakin_cift: dict[str, int] = defaultdict(int)
    duplicate_ozet: dict[str, int] = defaultdict(int)
    inceleme_ciftleri: list[tuple[str, str, DuplicateKarari]] = []
    for _norm, grup in isim_gruplari.items():
        if len(grup) < 2:
            continue
        for i, sol in enumerate(grup):
            for sag in grup[i + 1 :]:
                if sol.enlem is None or sag.enlem is None:
                    continue
                mesafe = haversine_metre(float(sol.enlem), float(sol.boylam), float(sag.enlem), float(sag.boylam))
                ayni_telefon = bool(sol.Yer.telefon and sol.Yer.telefon == sag.Yer.telefon)
                ayni_site = bool(sol.Yer.web_sitesi and sol.Yer.web_sitesi == sag.Yer.web_sitesi)
                karar = duplicate_kararini_ver(
                    ayni_kaynak_id=False,
                    isim_ayni=True,
                    mesafe_metre=mesafe,
                    ayni_telefon=ayni_telefon,
                    ayni_website=ayni_site,
                    ayni_kategori=sol.Yer.alt_kategori == sag.Yer.alt_kategori,
                    ayni_koordinat=mesafe <= 15,
                    zincir_marka=ayni_site,
                )
                duplicate_ozet[karar.value] += 1
                if mesafe <= 150:
                    yakin_cift[str(sol.Sube.id)] += 1
                    yakin_cift[str(sag.Sube.id)] += 1
                if karar is DuplicateKarari.INSAN_INCELEMESI:
                    inceleme_ciftleri.append((str(sol.Sube.id), str(sag.Sube.id), karar))

    sinif_sayaci: dict[str, int] = defaultdict(int)
    karantina = 0
    kategori_duzeltme = 0
    for satir in satirlar:
        yer, sube = satir.Yer, satir.Sube
        hedef_kategori = kaynak_etiketinden_kategori_duzelt(yer.isim, yer.alt_kategori)
        if hedef_kategori is not None:
            kategori_duzeltme += 1
            if not dry_run:
                yer.ana_kategori = AnaKategori.YEME_ICME.value
                yer.alt_kategori = hedef_kategori
        ozet = kimlik_kalitesini_hesapla(
            isim=yer.isim,
            enlem=None if satir.enlem is None else float(satir.enlem),
            boylam=None if satir.boylam is None else float(satir.boylam),
            sehir_anahtari=sehir_anahtari,
            alt_kategori=yer.alt_kategori,
            kaynak_sayisi=kaynak_sayilari.get(str(sube.id), 1),
            ayni_isim_yakin_cift=yakin_cift.get(str(sube.id), 0),
            ilce_id=yer.ilce_id,
            kategori_kaynak_uyumu=_kategori_kaynak_uyumu(yer.alt_kategori, yer.isim, yer.ozellikler),
            sube_durum=sube.durum,
        )
        sinif_sayaci[ozet.sinif.value] += 1
        if not oneriye_uygun_mu(ozet.sinif):
            karantina += 1
        if dry_run:
            continue
        sube.kimlik_kalite_sinifi = ozet.sinif.value
        sube.kimlik_kalite_kirilim = dict(ozet.kirilim)
        if ozet.sinif is KimlikKaliteSinifi.KARANTINA:
            sube.durum = _KARANTINA
            satir.YerKimligi.durum = _KARANTINA
            _inceleme_yaz(oturum, sube_id=str(sube.id), eylem="kimlik_karantina", kirilim=ozet.kirilim)
        elif ozet.sinif is KimlikKaliteSinifi.SUPHELI:
            sube.durum = _KIMLIK_INCELEME
            _inceleme_yaz(oturum, sube_id=str(sube.id), eylem="kimlik_inceleme", kirilim=ozet.kirilim)
        elif sube.durum in {_KARANTINA, _KIMLIK_INCELEME} and ozet.sinif in {
            KimlikKaliteSinifi.KULLANILABILIR,
            KimlikKaliteSinifi.GUCLU,
            KimlikKaliteSinifi.DOGRULANMIS,
        }:
            sube.durum = "aktif"
            satir.YerKimligi.durum = "aktif"

    if not dry_run:
        for sol_id, sag_id, _karar in inceleme_ciftleri:
            _esleme_adayi_yaz(oturum, sol_id, sag_id)
        oturum.flush()

    return {
        "yer_sayisi": len(satirlar),
        "siniflar": dict(sinif_sayaci),
        "oneri_disi": karantina,
        "kategori_kaynak_etiketi_duzeltme": kategori_duzeltme,
        "duplicate": dict(duplicate_ozet),
        "insan_incelemesi_cift": len(inceleme_ciftleri),
        "ayni_kaynak_id_coklu_canonical": sum(1 for subeler in kaynak_id_sube.values() if len(set(subeler)) > 1),
        "dry_run": dry_run,
        "zaman": datetime.now(UTC).isoformat(),
    }


def _inceleme_yaz(oturum: Session, *, sube_id: str, eylem: str, kirilim: dict) -> None:
    dosya_id = _uuid5(f"inceleme:{eylem}:{sube_id}")
    if oturum.get(IncelemeDosyasi, dosya_id):
        return
    oturum.add(
        IncelemeDosyasi(
            id=dosya_id,
            dosya_turu="kimlik",
            nesne_turu="sube",
            nesne_id=sube_id,
            durum="bekliyor",
            risk_sinifi="yuksek" if eylem == "kimlik_karantina" else "normal",
            onerilen_eylem=eylem,
            komut_payload={"kirilim": kirilim},
            acan_aktor_id=None,
            karar_gerekcesi="Kimlik kalitesi tarayicisi; otomatik yayin yok.",
        )
    )


def _esleme_adayi_yaz(oturum: Session, sol_id: str, sag_id: str) -> None:
    if sol_id > sag_id:
        sol_id, sag_id = sag_id, sol_id
    mevcut = (
        oturum.query(EslemeAdayi)
        .filter_by(sol_sube_id=sol_id, sag_sube_id=sag_id)
        .first()
    )
    if mevcut:
        return
    oturum.add(
        EslemeAdayi(
            sol_sube_id=sol_id,
            sag_sube_id=sag_id,
            confidence=0.4,
            belirsizlik={"kaynak": "kimlik_kalitesi_v1"},
            durum="bekliyor",
        )
    )


def _ana() -> None:
    ayristirici = argparse.ArgumentParser(description="Kimlik kalitesi tarayicisi")
    ayristirici.add_argument("--sehir", required=True)
    ayristirici.add_argument("--yaz", action="store_true")
    args = ayristirici.parse_args()
    with OturumUretici() as oturum:
        sehir = oturum.query(Sehir).filter(Sehir.arama_isim == args.sehir).one()
        ozet = kimlik_auditini_calistir(oturum, sehir_id=str(sehir.id), dry_run=not args.yaz)
        if args.yaz:
            oturum.commit()
        print(json.dumps(ozet, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _ana()
