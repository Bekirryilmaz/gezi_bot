"""
Bolge Profili pipeline'i -- ana calistirma betigi.

veri/duygu_analizi/pipeline_calistir.py'nin urettigi EN GUNCEL IslenmisYorum
JSONL'ini okur, "bolge:" onekli (Eksi Sozluk'un sehir/ilce-geneli, bkz.
eksi_sozluk_toplayici.py) kayitlari bulunan HER bolgeye gore gruplar (bkz.
bolge_profili_cikarici.py) ve her bolge icin:
  1. Genel duygu skoru/etiketi + on plana cikan konulari cikarir,
  2. anlatim_uretici.py ile samimi bir Turkce tanitim metni ("duygu_ozeti") uretir,
ve sonucu veri/cikti/islenmis/bolge_profilleri/<sehir>_<tarih>.jsonl dosyasina yazar.

Calistirma (repo kokunden, once asagidaki komutlarin calistirilmis olmasi gerekir):
    python -m veri.toplayicilar.eksi_sozluk_toplayici --sehir samsun
    python -m veri.duygu_analizi.pipeline_calistir --sehir samsun
    python -m veri.duygu_analizi.bolge_profili_pipeline_calistir --sehir samsun
"""

from __future__ import annotations

import argparse
from pathlib import Path

from veri.duygu_analizi.anlatim_uretici import bolge_tanitim_metni_uret
from veri.duygu_analizi.bolge_profili_cikarici import bolge_profili_olustur, yorumlari_bolgelere_bagla
from veri.ortak.bolge_profili_modeli import BolgeProfili
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_oku, jsonl_yaz
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.ortak.yorum_modeli import IslenmisYorum


def _cikti_kok() -> Path:
    # Bu dosya veri/duygu_analizi/ altinda, yani parents[1] = veri/
    return Path(__file__).resolve().parents[1] / "cikti"


def _en_guncel_dosyayi_bul(klasor: Path, desen: str) -> Path | None:
    if not klasor.exists():
        return None
    adaylar = sorted(klasor.glob(desen))  # dosya adlari tarih icerir, siralama = kronolojik
    return adaylar[-1] if adaylar else None


def _islenmis_yorumlari_yukle(sehir_anahtari: str) -> list[IslenmisYorum]:
    dosya = _en_guncel_dosyayi_bul(_cikti_kok() / "islenmis" / "yorumlar", f"{sehir_anahtari}_*.jsonl")
    if dosya is None:
        return []
    yorumlar: list[IslenmisYorum] = []
    for kayit in jsonl_oku(dosya):
        try:
            yorumlar.append(IslenmisYorum(**kayit))
        except Exception as hata:
            print(f"[UYARI] {dosya.name} icinde okunamayan IslenmisYorum kaydi atlandi: {hata}")
    return yorumlar


def _ozet_yazdir(profiller: list[BolgeProfili]) -> None:
    print("\n[BILGI] === Bolge Profili Ozeti ===")
    print(f"[BILGI] Toplam profil cikarilan bolge: {len(profiller)}")
    for profil in sorted(profiller, key=lambda p: p.kullanilan_yorum_sayisi, reverse=True):
        tur = "ilce" if profil.ilce_mi else "sehir merkezi"
        skor = f"{profil.genel_duygu_skoru:+.2f}" if profil.genel_duygu_skoru is not None else "bilgi_yetersiz"
        print(f"[BILGI]   {profil.bolge_adi} ({tur}): {profil.kullanilan_yorum_sayisi} yorum, duygu skoru {skor}")

    if profiller:
        ornek = max(profiller, key=lambda p: p.kullanilan_yorum_sayisi)
        print(f"\n[BILGI] Ornek tanitim metni -- '{ornek.bolge_adi}' ({ornek.kullanilan_yorum_sayisi} yorumdan uretildi):")
        print(f"[BILGI]   {ornek.duygu_ozeti}")


def calistir(sehir_anahtari: str) -> Path | None:
    sehir = sehir_getir(sehir_anahtari)

    islenmis_yorumlar = _islenmis_yorumlari_yukle(sehir_anahtari)
    if not islenmis_yorumlar:
        print(
            f"[UYARI] '{sehir.isim}' icin islenmis yorum bulunamadi. "
            f"Once 'python -m veri.duygu_analizi.pipeline_calistir --sehir {sehir_anahtari}' calistir."
        )
        return None

    bolgesel_yorumlar = yorumlari_bolgelere_bagla(islenmis_yorumlar)
    if not bolgesel_yorumlar:
        print(
            f"[UYARI] '{sehir.isim}' icin bolge-geneli ('bolge:' onekli) yorum bulunamadi. "
            f"Once 'python -m veri.toplayicilar.eksi_sozluk_toplayici --sehir {sehir_anahtari}' calistir."
        )
        return None

    print(f"[BILGI] {len(bolgesel_yorumlar)} bolge icin profil cikariliyor (toplam sehir+ilce sayisi: {len(sehir.tum_bolge_adlari())})...")

    profiller: list[BolgeProfili] = []
    for bolge_kaynak_yer_id, yorumlar in bolgesel_yorumlar.items():
        profil = bolge_profili_olustur(bolge_kaynak_yer_id, yorumlar)
        profil.duygu_ozeti = bolge_tanitim_metni_uret(profil)
        profiller.append(profil)

    cikti_dosyasi = _cikti_kok() / "islenmis" / "bolge_profilleri" / f"{sehir.anahtar}_{bugunun_tarihi_dosya_adi()}.jsonl"
    jsonl_yaz(cikti_dosyasi, profiller)
    print(f"[BILGI] {len(profiller)} bolge profili yazildi: {cikti_dosyasi}")

    _ozet_yazdir(profiller)

    return cikti_dosyasi


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(description="Eksi Sozluk'un bolge-geneli yorumlarindan Bolge Profili uretir.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    argumanlar = ayristirici.parse_args()
    calistir(argumanlar.sehir)


if __name__ == "__main__":
    _ana()
