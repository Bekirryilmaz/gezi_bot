from __future__ import annotations

from sqlalchemy import and_
from sqlalchemy.orm import Session

from sunucu.bilgi.pilot_claimleri import FRESHNESS_POLITIKALARI
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu
from sunucu.veritabani.kimlik_modelleri import Sube
from sunucu.veritabani.yayin_modelleri import YayinKaydi
from sunucu.yayin.domain import KullanimTuru
from sunucu.yayin.servis import yayin_kaydi_kamusal_mi


UNKNOWN_GOSTERILEN_AILELER = ("wifi", "tekerlekli_sandalye_erisimi", "ucretsiz")


def yer_pratik_bilgileri(oturum: Session, yer_id: str) -> list[dict]:
    satirlar = (
        oturum.query(Iddia, IddiaSurumu, YayinKaydi)
        .join(Sube, Sube.id == Iddia.sube_id)
        .join(
            IddiaSurumu,
            and_(IddiaSurumu.iddia_id == Iddia.id, IddiaSurumu.surum_no == Iddia.aktif_surum_no),
        )
        .join(
            YayinKaydi,
            and_(YayinKaydi.nesne_turu == "claim", YayinKaydi.nesne_id == Iddia.id),
        )
        .filter(Sube.legacy_yer_id == yer_id, YayinKaydi.aktif_mi.is_(True))
        .all()
    )
    if not satirlar:
        return []
    sonuc: list[dict] = []
    gorulen: set[str] = set()
    for iddia, surum, yayin in satirlar:
        gorulen.add(iddia.aile)
        kamusal = yayin_kaydi_kamusal_mi(yayin, KullanimTuru.DETAY)
        durum_gosterilebilir = surum.bilgi_durumu in {"eskimis", "celiskili"}
        if not kamusal and not durum_gosterilebilir:
            continue
        sonuc.append({
            "aile": iddia.aile,
            "deger": surum.deger.get("deger") if kamusal and isinstance(surum.deger, dict) else None,
            "bilgi_durumu": surum.bilgi_durumu,
            "kapsam": iddia.kapsam,
            "gecerlilik_baslangici": surum.gecerlilik_baslangici,
            "gecerlilik_bitisi": surum.gecerlilik_bitisi,
            "dogrulanma_zamani": surum.dogrulanma_zamani,
            "yeniden_dogrulama": FRESHNESS_POLITIKALARI.get(iddia.aile, {}).get("yeniden_dogrulama"),
        })
    if sonuc:
        for aile in UNKNOWN_GOSTERILEN_AILELER:
            if aile not in gorulen:
                sonuc.append({
                    "aile": aile,
                    "deger": None,
                    "bilgi_durumu": "bilinmiyor",
                    "kapsam": {"sube_kapsami": "tam_sube"},
                    "gecerlilik_baslangici": None,
                    "gecerlilik_bitisi": None,
                    "dogrulanma_zamani": None,
                    "yeniden_dogrulama": FRESHNESS_POLITIKALARI[aile]["yeniden_dogrulama"],
                })
    return sorted(sonuc, key=lambda x: x["aile"])
