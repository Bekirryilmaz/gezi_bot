"""
Serbest metin (ozellikle Eksi Sozluk'un bolge-geneli entry'leri) icinde
BILINEN yer isimlerinin gecip gecmedigini tespit eden basit, aciklanabilir
bir eslestirici.

Neden gerekli: Eksi Sozluk'ta bir baslik (orn. "samsun") sehir/ilce GENELINDE
konusulur, ama entry'lerin bir kismi ACIKCA belirli bir yerden bahseder
(orn. "amazon koyu'na gittik, manzarasi guzeldi"). Bu modul, boyle bir
entry'yi -- bolge profiline katkisi disinda -- FIRSATCI olarak o yerin
(BirlesikYer) profiline de baglamak icin kullanilir (bkz.
yer_profili_cikarici.py::yorumlari_yerlere_bagla).

Tasarim/kabul edilen sinirlamalar (dokumanlar/veri_sozlugu.md ile ayni ruhta,
"aciklanabilir, tahmine yer birakmayan" bir yaklasim):
- Sadece 2+ kelimelik VE yeterince uzun isimler aranir (tek kelimelik "kale"
  gibi genel isimler kasitli olarak DISLANIR -- cok fazla yanlis-pozitif
  uretirler).
- Eslesme, kelime siniri (word boundary) farkindaligiyla yapilir (regex),
  boylece "kale" ismi "kalede" gibi baska bir kelimenin PARCASI olarak degil,
  sadece BAGIMSIZ bir kelime/ifade olarak eslesir.
- Bircok yer isim eslesmesi bulunursa (nadir ama olasi -- uzun bir entry
  birden fazla yerden bahsedebilir), en fazla `maks_sonuc` tanesi dondurulur.
"""

from __future__ import annotations

import re

from veri.ortak.birlesik_yer_modeli import BirlesikYer
from veri.ortak.metin_araclari import turkce_kucuk_harf

# Bu esigin altindaki isimler (orn. "kale", "park", "cami") tek basina
# aranmaz -- cok genel oldugu icin metinde gecmesi o yerden bahsedildigi
# anlamina gelmez, sadece yanlis-pozitif uretir.
_MINIMUM_KARAKTER_UZUNLUGU = 6
# Tek kelimelik isimler de (yeterince uzun olsalar bile) varsayilan olarak
# ARANMAZ -- cunku genelde ozel isim + genel tur kelimesinden olusan (orn.
# "Amazon Koyu", "Liman Camii") COK KELIMELI isimler, tek kelimelik genel
# isimlerden (orn. "Liman") cok daha ayirt edicidir.
_MINIMUM_KELIME_SAYISI = 2

YerIndeksi = list[tuple[str, re.Pattern[str], str]]


def _normallestir(metin: str) -> str:
    return " ".join(turkce_kucuk_harf(metin.strip()).split())


def yer_isimlerini_indeksle(birlesik_yerler: list[BirlesikYer]) -> YerIndeksi:
    """Her BirlesikYer icin, eger ismi yeterince ayirt ediciyse (2+ kelime,
    minimum uzunluk), (normal_isim, kelime_siniri_deseni, yer_kimligi) demeti
    uretir. Cok kisa/genel isimler (bkz. modul dokstring'i) atlanir.

    Sonuc, isim UZUNLUGUNA GORE AZALAN sirada dondurulur -- boylece
    `metinde_gecen_yerleri_bul` daha ozel/uzun isimleri once dener (orn.
    "Amazon Doga Parki" ismi varken sadece "Amazon Koyu" ile karistirilmaz)."""
    indeks: YerIndeksi = []
    gorulen_isimler: set[str] = set()
    for yer in birlesik_yerler:
        isim_normal = _normallestir(yer.isim)
        if len(isim_normal) < _MINIMUM_KARAKTER_UZUNLUGU:
            continue
        if len(isim_normal.split()) < _MINIMUM_KELIME_SAYISI:
            continue
        if isim_normal in gorulen_isimler:
            continue  # Ayni isimde birden fazla yer varsa (nadir), ilkini kullan -- belirsizlik kabul edilir.
        gorulen_isimler.add(isim_normal)
        desen = re.compile(r"(?<!\w)" + re.escape(isim_normal) + r"(?!\w)", re.IGNORECASE)
        indeks.append((isim_normal, desen, yer.yer_kimligi))

    indeks.sort(key=lambda ogr: len(ogr[0]), reverse=True)
    return indeks


def metinde_gecen_yerleri_bul(metin: str, yer_indeksi: YerIndeksi, maks_sonuc: int = 3) -> list[str]:
    """Verilen metinde `yer_indeksi`'ndeki yer isimlerinden gecenleri
    bulup `yer_kimligi` listesi olarak dondurur (bulunamazsa bos liste)."""
    if not metin or not yer_indeksi:
        return []
    metin_normal = _normallestir(metin)
    bulunan_kimlikler: list[str] = []
    for _isim, desen, yer_kimligi in yer_indeksi:
        if desen.search(metin_normal):
            bulunan_kimlikler.append(yer_kimligi)
            if len(bulunan_kimlikler) >= maks_sonuc:
                break
    return bulunan_kimlikler
