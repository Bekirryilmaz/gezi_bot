"""
Eksi Sozluk toplayicisi.

Google Maps'in aksine Eksi Sozluk sunucu tarafinda tamamen hazir HTML
dondurdugu icin (JavaScript calistirmaya gerek yok) burada agir bir tarayici
otomasyonuna (Playwright) degil, hafif bir HTTP istemcisine (requests) ve
HTML ayristirmaya (BeautifulSoup) ihtiyacimiz var.

Onemli fark: Google Maps'teki yorumlar dogrudan BIR isletmeyle iliskiliyken,
Eksi Sozluk'taki "entry"ler bir BASLIK (konu) altinda toplanir ve genelde
BELIRLI BIR BOLGE (sehir merkezi veya bir ilce) hakkindadir, tek bir
isletmeyle degil. Bu toplayici, `veri/ortak/sehir_ayarlari.py`'deki
`SehirAyari.tum_bolge_adlari()` (sehir + tum ilceler) uzerinde doner ve her
biri icin `bolge_basliklarini_getir()` ile o bolgenin Eksi Sozluk basligi
(veya basliklari) belirlenir. Uretilen HamYorum kayitlarinda `kaynak_yer_id`
alani ozel bir bicimde doldurulur:

    kaynak_yer_id = "bolge:<sehir_anahtari>:<bolge_adi>"

Bu kayitlar iki sekilde kullanilir:
  1) veri/duygu_analizi/bolge_profili_cikarici.py -- bolgenin (sehir/ilce)
     GENEL bir tanitim duygu profilini cikarmak icin (bkz. Bolge Profili).
  2) veri/duygu_analizi/yer_ismi_tespiti.py -- entry metninde bilinen bir
     yerin adi geciyorsa, entry'yi FIRSATCI olarak o yere de baglamak icin
     (bkz. yer_profili_cikarici.py::yorumlari_yerlere_bagla).

Calistirma (repo kokunden):
    python -m veri.toplayicilar.eksi_sozluk_toplayici --sehir samsun --maks-sayfa 10
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from ortak.sabitler import VeriKaynagi
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_tek_satir_ekle
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir, turkce_kucuk_harf
from veri.ortak.sehir_ayarlari import bolge_slug, sehir_getir
from veri.ortak.yorum_modeli import HamYorum
from veri.toplayicilar.ortak_araclar import kullanici_ajani_sec, rastgele_bekle

TABAN_ADRES = "https://eksisozluk.com"


def _sayfa_getir(baslik_slug: str, sayfa_no: int) -> BeautifulSoup | None:
    url = f"{TABAN_ADRES}/{baslik_slug}"
    parametreler = {"p": sayfa_no} if sayfa_no > 1 else {}
    basliklar = {"User-Agent": kullanici_ajani_sec(), "Accept-Language": "tr-TR,tr;q=0.9"}
    try:
        yanit = requests.get(url, params=parametreler, headers=basliklar, timeout=20)
    except requests.RequestException as hata:
        print(f"[UYARI] '{baslik_slug}' sayfa {sayfa_no} istegi basarisiz: {hata}")
        return None
    if yanit.status_code == 404:
        print(f"[UYARI] '{baslik_slug}' basligi bulunamadi (404). Slug'i kontrol et.")
        return None
    if yanit.status_code != 200:
        print(f"[UYARI] '{baslik_slug}' sayfa {sayfa_no} beklenmeyen durum kodu: {yanit.status_code}")
        return None
    return BeautifulSoup(yanit.text, "lxml")


def _toplam_sayfa_sayisini_bul(corba: BeautifulSoup) -> int:
    pager = corba.find("div", class_="pager")
    if pager is None or not pager.get("data-pagecount"):
        return 1
    try:
        return int(pager["data-pagecount"])
    except (ValueError, TypeError):
        return 1


def _tarihi_ayristir(ham_tarih: str | None) -> datetime | None:
    """Eksi Sozluk tarih bicimi: '16.06.1999 ~ 02.01.2001 11:16' (olusturma ~ duzenleme)
    veya sadece '16.06.1999 18:17'. Her zaman ILK (olusturma) tarihini aliriz."""
    if not ham_tarih:
        return None
    ilk_kisim = ham_tarih.split("~")[0].strip()
    for bicim in ("%d.%m.%Y %H:%M", "%d.%m.%Y"):
        try:
            return datetime.strptime(ilk_kisim, bicim)
        except ValueError:
            continue
    return None


def _entryleri_ayikla(corba: BeautifulSoup, kaynak_yer_id: str) -> list[HamYorum]:
    entryler: list[HamYorum] = []
    for li in corba.select("li[data-id]"):
        icerik_div = li.find("div", class_="content")
        if icerik_div is None:
            continue
        metin = icerik_div.get_text(separator="\n").strip()
        # Cok kisa/bos entry'leri (orn. sadece "(bkz: ...)" iceren) atlamiyoruz,
        # cunku bunlar da duygu tasiyabilir; sadece gercekten bos olanlari eliyoruz.
        if not metin:
            continue

        entry_id = li.get("data-id")
        yazar = li.get("data-author")
        if not yazar:
            yazar_etiketi = li.find("a", class_="entry-author")
            yazar = yazar_etiketi.get_text(strip=True) if yazar_etiketi else None

        tarih_etiketi = li.find("a", class_="entry-date")
        yorum_tarihi = _tarihi_ayristir(tarih_etiketi.get_text(strip=True) if tarih_etiketi else None)

        try:
            entryler.append(
                HamYorum(
                    kaynak=VeriKaynagi.EKSI_SOZLUK,
                    kaynak_yer_id=kaynak_yer_id,
                    kaynak_yorum_id=entry_id,
                    yazar_takma_adi=yazar,
                    yorum_metni=metin,
                    yorum_tarihi=yorum_tarihi,
                )
            )
        except Exception as hata:
            print(f"[UYARI] Entry {entry_id} donusturulemedi: {hata}")
            continue

    return entryler


def calistir(sehir_anahtari: str, maks_sayfa_baslik_basi: int = 10) -> None:
    sehir = sehir_getir(sehir_anahtari)
    bolgeler = sehir.tum_bolge_adlari()
    if not bolgeler:
        print(f"[UYARI] '{sehir.isim}' icin veri/ortak/sehir_ayarlari.py'de tanimli bolge/baslik yok.")
        return

    cikti_dosyasi = (
        Path(__file__).resolve().parents[1]
        / "cikti" / "ham" / "eksi_sozluk" / f"{sehir.anahtar}_{bugunun_tarihi_dosya_adi()}.jsonl"
    )

    toplam_entry = 0
    for bolge_no, bolge_adi in enumerate(bolgeler, start=1):
        basliklar = sehir.bolge_basliklarini_getir(bolge_adi)
        kaynak_yer_id = f"bolge:{sehir.anahtar}:{bolge_slug(bolge_adi)}"
        print(f"[BILGI] ({bolge_no}/{len(bolgeler)}) Bolge: '{bolge_adi}' -- basliklar: {basliklar}")

        for baslik in basliklar:
            baslik_slug = _sluglastir(baslik)
            print(f"[BILGI]   Baslik taraniyor: '{baslik}' (slug: {baslik_slug})")

            ilk_sayfa = _sayfa_getir(baslik_slug, 1)
            if ilk_sayfa is None:
                continue
            toplam_sayfa = min(_toplam_sayfa_sayisini_bul(ilk_sayfa), maks_sayfa_baslik_basi)
            print(f"[BILGI]     Toplam {toplam_sayfa} sayfa islenecek (basliktaki gercek sayfa sayisi daha fazla olabilir).")

            for sayfa_no in range(1, toplam_sayfa + 1):
                try:
                    corba = ilk_sayfa if sayfa_no == 1 else _sayfa_getir(baslik_slug, sayfa_no)
                    if corba is None:
                        continue
                    entryler = _entryleri_ayikla(corba, kaynak_yer_id)
                except Exception as hata:
                    print(f"[UYARI] '{baslik_slug}' sayfa {sayfa_no} islenirken hata olustu, atlaniyor: {hata}")
                    continue
                for entry in entryler:
                    jsonl_tek_satir_ekle(cikti_dosyasi, entry)
                toplam_entry += len(entryler)
                print(f"[BILGI]     Sayfa {sayfa_no}/{toplam_sayfa}: {len(entryler)} entry kaydedildi.")

                if sayfa_no < toplam_sayfa:
                    rastgele_bekle(2.0, 5.0)

    print(f"[BILGI] Tamamlandi. Toplam {toplam_entry} entry kaydedildi.")
    print(f"[BILGI] Sonuclar: {cikti_dosyasi}")


def _sluglastir(baslik: str) -> str:
    """Eksi Sozluk URL'lerinde baslik, kucuk harfe cevrilip bosluklarin
    tire ile degistirildigi bir 'slug' halinde kullanilir. Turkce karakterler
    Eksi Sozluk'ta OLDUGU GIBI (sozluk--nokta gibi) korunur, bu yuzden
    yalnizca bosluk/tekil tirnak donusumu yapiyoruz, ASCII'ye indirmiyoruz.
    (`turkce_kucuk_harf` kullanilir -- normal `.lower()`, 'İ' harfini
    Windows konsolunda cakmaya sebep olan bir birlesik karaktere cevirir,
    bkz. veri/ortak/metin_araclari.py modul dokstring'i.)"""
    return turkce_kucuk_harf(baslik.strip()).replace(" ", "-").replace("'", "")


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(description="Eksi Sozluk'tan bir sehrin basliklarindaki entry'leri topla.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    ayristirici.add_argument("--maks-sayfa", type=int, default=10, help="Baslik basina taranacak maksimum sayfa sayisi")
    argumanlar = ayristirici.parse_args()
    calistir(argumanlar.sehir, maks_sayfa_baslik_basi=argumanlar.maks_sayfa)


if __name__ == "__main__":
    _ana()
