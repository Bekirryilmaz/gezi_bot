from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from sunucu.veritabani.admin_modelleri import IncelemeDosyasi
from sunucu.veritabani.bilgi_modelleri import Iddia
from sunucu.veritabani.kimlik_modelleri import Sube

DUSUK_RISK_AILELERI = frozenset(
    {
        "web_sitesi",
        "telefon",
        "adres",
        "yer_turu",
        "calisma_saatleri",
        "otopark",
        "acik_alan",
        "tekerlekli_sandalye_erisimi",
        "wifi",
        "rezervasyon",
    }
)
YUKSEK_RISK_AILELERI = frozenset({"amac_destegi"})
KAPSAM_ONCELIGI = {
    "calisma_saatleri": 110,
    "wifi": 100,
    "otopark": 90,
    "acik_alan": 80,
    "tekerlekli_sandalye_erisimi": 70,
    "rezervasyon": 60,
    "yer_turu": 25,
    "telefon": 20,
    "web_sitesi": 15,
    "adres": 10,
    "amac_destegi": 5,
}


@dataclass(frozen=True)
class KuyrukOnceligi:
    triyaj_sinifi: str
    oncelik_puani: int
    risk_sinifi: str


def kuyruk_onceligini_hesapla(
    *,
    aile: str,
    guclu_kanit: bool = False,
    dusuk_celiski: bool = True,
    dogrulanmis_sube: bool = False,
    pilot_mekan: bool = False,
    rota_kritik: bool = False,
) -> KuyrukOnceligi:
    if aile in DUSUK_RISK_AILELERI:
        triyaj = "dusuk_risk"
        risk = "dusuk"
    elif aile in YUKSEK_RISK_AILELERI:
        triyaj = "yuksek_risk"
        risk = "yuksek"
    else:
        triyaj = "orta_risk"
        risk = "normal"
    puan = KAPSAM_ONCELIGI.get(aile, 8)
    if guclu_kanit:
        puan += 12
    if dusuk_celiski:
        puan += 8
    if dogrulanmis_sube:
        puan += 10
    if rota_kritik or aile == "calisma_saatleri":
        puan += 25
    if pilot_mekan:
        puan += 40
    if triyaj == "yuksek_risk":
        puan -= 25
    return KuyrukOnceligi(triyaj_sinifi=triyaj, oncelik_puani=max(0, puan), risk_sinifi=risk)


def inceleme_kuyrugunu_triyaj_et(
    oturum: Session,
    *,
    dry_run: bool = False,
    pilot_sube_idleri: set[str] | None = None,
) -> dict[str, int]:
    from ortak.sabitler import ROTA_KAPSAM_AILELERI, RotaKapsamSinifi

    dosyalar = (
        oturum.query(IncelemeDosyasi)
        .filter(
            IncelemeDosyasi.durum != "tamamlandi", IncelemeDosyasi.dosya_turu == "claim_candidate"
        )
        .all()
    )
    sayac = {"dusuk_risk": 0, "yuksek_risk": 0, "orta_risk": 0, "guncellenen": 0}
    for dosya in dosyalar:
        iddia = oturum.get(Iddia, dosya.nesne_id)
        aile = iddia.aile if iddia is not None else ""
        sube = oturum.get(Sube, iddia.sube_id) if iddia is not None else None
        dogrulanmis = bool(
            sube is not None
            and getattr(sube, "kimlik_kalite_sinifi", "") in {"dogrulanmis", "guclu"}
        )
        oncelik = kuyruk_onceligini_hesapla(
            aile=aile,
            guclu_kanit=True,
            dusuk_celiski=True,
            dogrulanmis_sube=dogrulanmis,
            pilot_mekan=bool(
                pilot_sube_idleri is not None
                and iddia is not None
                and iddia.sube_id in pilot_sube_idleri
            ),
            rota_kritik=ROTA_KAPSAM_AILELERI.get(aile) == RotaKapsamSinifi.ROTA_KRITIK.value,
        )
        sayac[oncelik.triyaj_sinifi] += 1
        if dry_run:
            continue
        dosya.triyaj_sinifi = oncelik.triyaj_sinifi
        dosya.oncelik_puani = oncelik.oncelik_puani
        dosya.risk_sinifi = oncelik.risk_sinifi
        if oncelik.triyaj_sinifi == "dusuk_risk":
            dosya.onerilen_eylem = "grup_dusuk_risk_inceleme"
        sayac["guncellenen"] += 1
    if not dry_run:
        oturum.flush()
    return sayac


def _ana() -> None:
    import argparse
    import json

    from sunucu.veritabani.baglanti import OturumUretici

    ayristirici = argparse.ArgumentParser(description="OSM inceleme kuyrugu triyaji")
    ayristirici.add_argument("--yaz", action="store_true")
    args = ayristirici.parse_args()
    with OturumUretici() as oturum:
        ozet = inceleme_kuyrugunu_triyaj_et(oturum, dry_run=not args.yaz)
        if args.yaz:
            oturum.commit()
        print(json.dumps(ozet, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _ana()
