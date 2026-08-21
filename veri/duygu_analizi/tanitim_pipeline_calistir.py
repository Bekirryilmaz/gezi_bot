"""
Tum birlesik yerler + bolgeler icin tanitim_metni uretir.

Calistirma:
    python -m veri.duygu_analizi.tanitim_pipeline_calistir --sehir samsun
    python -m veri.duygu_analizi.tanitim_pipeline_calistir --sehir samsun --wiki
"""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import BaseModel, Field

from veri.duygu_analizi.tanitim_uretici import bolge_tanitim_metni_uret, yer_tanitim_metni_uret
from veri.ortak.birlesik_yer_modeli import BirlesikYer
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_oku, jsonl_yaz
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir
from veri.ortak.sehir_ayarlari import sehir_getir


class YerTanitimKaydi(BaseModel):
    yer_kimligi: str
    yer_ismi: str
    tanitim_metni: str


class BolgeTanitimKaydi(BaseModel):
    bolge_adi: str
    ilce_mi: bool = False
    tanitim_metni: str = Field(default="")


def _cikti_kok() -> Path:
    return Path(__file__).resolve().parents[1] / "cikti"


def _en_guncel(klasor: Path, desen: str) -> Path | None:
    if not klasor.exists():
        return None
    adaylar = sorted(klasor.glob(desen))
    return adaylar[-1] if adaylar else None


def calistir(sehir_anahtari: str, wiki: bool = False) -> None:
    sehir = sehir_getir(sehir_anahtari)
    birlesik_dosya = _en_guncel(_cikti_kok() / "islenmis" / "birlesik_yerler", f"{sehir_anahtari}_*.jsonl")
    if birlesik_dosya is None:
        print("[UYARI] Birlesik yer dosyasi yok.")
        return

    yer_kayitlari: list[YerTanitimKaydi] = []
    for kayit in jsonl_oku(birlesik_dosya):
        try:
            by = BirlesikYer(**kayit)
        except Exception:
            continue
        metin = yer_tanitim_metni_uret(by, wiki_denensin=wiki)
        yer_kayitlari.append(
            YerTanitimKaydi(yer_kimligi=by.yer_kimligi, yer_ismi=by.isim, tanitim_metni=metin)
        )

    tarih = bugunun_tarihi_dosya_adi()
    yer_cikti = _cikti_kok() / "islenmis" / "tanitimlar" / f"{sehir_anahtari}_yer_{tarih}.jsonl"
    jsonl_yaz(yer_cikti, yer_kayitlari)
    print(f"[BILGI] {len(yer_kayitlari)} yer tanitimi yazildi: {yer_cikti}")

    bolge_kayitlari: list[BolgeTanitimKaydi] = []
    for bolge_adi in sehir.tum_bolge_adlari():
        ilce_mi = bolge_adi != sehir.anahtar
        metin = bolge_tanitim_metni_uret(bolge_adi if ilce_mi else sehir.isim, sehir.isim, ilce_mi)
        bolge_kayitlari.append(
            BolgeTanitimKaydi(
                bolge_adi=bolge_adi if ilce_mi else sehir.anahtar,
                ilce_mi=ilce_mi,
                tanitim_metni=metin,
            )
        )

    bolge_cikti = _cikti_kok() / "islenmis" / "tanitimlar" / f"{sehir_anahtari}_bolge_{tarih}.jsonl"
    jsonl_yaz(bolge_cikti, bolge_kayitlari)
    print(f"[BILGI] {len(bolge_kayitlari)} bolge tanitimi yazildi: {bolge_cikti}")


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    p = argparse.ArgumentParser()
    p.add_argument("--sehir", default="samsun")
    p.add_argument("--wiki", action="store_true", help="Wikipedia ozetlerini de dene (daha yavas)")
    a = p.parse_args()
    calistir(a.sehir, wiki=a.wiki)


if __name__ == "__main__":
    _ana()
