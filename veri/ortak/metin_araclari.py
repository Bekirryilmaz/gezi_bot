"""
Turkce metin isleme icin kucuk, bagimsiz yardimci fonksiyonlar.

Bu modul neden var: Python'un standart `str.lower()` metodu, Turkce'ye ozel
noktali buyuk 'I' harfini (Ilkadim, Istanbul gibi kelimelerdeki 'İ', U+0130)
kucuk harfe cevirirken "i" + BIRLESIK NOKTA (U+0307, combining dot above)
ikilisine cevirir -- goze normal 'i' gibi gorunse de bu iki farkli unicode
kod noktasidir. Bu durum iki ayri soruna yol acar:

1. Bu birlesik karakter, Windows konsolunun varsayilan kod sayfalarinda
   (cp1254, cp1252 vb.) tanimli olmadigi icin bir `print()` cagrisi
   `UnicodeEncodeError` ile CALISMAYI TAMAMEN DURDURABILIR (bu, cok saatlik
   bir tarama sirasinda felakete yol acar).
2. Anahtar-kelime eslesmesi yapan kodlarda (duygu analizi konu tespiti,
   kategori esleme, yer-ismi tespiti) beklenmeyen sessiz basarisizliklara
   yol acabilir, cunku aranan anahtar kelime duz 'i' icerirken metindeki
   karsiligi 'i' + birlesik nokta olur ve tam string eslesmesi kacabilir.

`turkce_kucuk_harf` bu ikisini de onlemek icin 'İ' harfini once duz 'i'ye
cevirip SONRA standart `.lower()` uygular."""

from __future__ import annotations

import sys


def konsolu_guvenli_hale_getir() -> None:
    """Windows konsolunun varsayilan kod sayfasi (cp1254, cp1252 vb.) HER
    unicode karakteri temsil edemez -- ozellikle scraping sirasinda internetten
    gelen serbest metinlerde (yer adlari, yorumlar, emoji vb.) beklenmedik bir
    karakterle karsilasmak `print()`'i `UnicodeEncodeError` ile COKERTIP
    saatlerce suren bir taramayi bosa cikarabilir (bkz. bu modulun ust
    dokstring'i).

    Bu fonksiyon stdout/stderr'i UTF-8'e, kodlanamayan karakterleri SESSIZCE
    '?' ile degistirecek (`errors="replace"`) sekilde ayarlar -- calisma asla
    bir yazdirma hatasi yuzunden durmaz. Her toplayici/pipeline'in CLI giris
    noktasinda (`if __name__ == "__main__":` bloklarinda) cagirilmalidir.
    Reconfigure desteklemeyen ortamlarda (orn. bazi test/IDE konsollari)
    sessizce atlanir."""
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def turkce_kucuk_harf(metin: str) -> str:
    """Turkce metinleri, 'İ' (U+0130) harfinin `str.lower()` ile birlesik
    nokta karakterine (U+0307) donusmesini ONLEYECEK sekilde kucuk harfe
    cevirir. Diger tum karakterler icin normal `.lower()` davranisiyla
    aynidir."""
    return metin.replace("İ", "i").lower()
