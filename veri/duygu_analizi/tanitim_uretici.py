"""
Mekan/bolge icin TANITIM metni uretir (duygu ozetinden AYRI).

Oncelik sirasi (yer):
  1) Google Maps 'hakkinda' (ozellikler veya aciklama icinde saklanmissa)
  2) Wikipedia ozeti (MediaWiki API, ucretsiz)
  3) OSM description (aciklama alani)
  4) Kategori/alt kategori sablonu

LLM kullanilmaz.
"""

from __future__ import annotations

import re
from functools import lru_cache

import requests

from ortak.sabitler import AnaKategori
from veri.ortak.birlesik_yer_modeli import BirlesikYer
from veri.ortak.metin_araclari import turkce_kucuk_harf

_WIKI_API = "https://tr.wikipedia.org/w/api.php"
_WIKI_TIMEOUT = 8

_ALT_KATEGORI_TANITIM: dict[str, str] = {
    "tarihi_kulturel": "tarihi ve kültürel bir nokta",
    "doga_manzara": "doğa ve manzara odaklı bir yer",
    "plaj_su": "plaj veya su kenarı bir mekan",
    "eglence_aktivite": "eğlence ve aktivite sunan bir yer",
    "gece_hayati": "gece hayatı mekanı",
    "alisveris": "alışveriş noktası",
    "spor_doga_yuruyus": "spor ve yürüyüş için uygun bir alan",
    "dini_manevi": "dini veya manevi bir mekân",
    "fotograf_noktasi": "fotoğraf çekmek için tercih edilen bir nokta",
    "otel": "konaklama tesisi (otel)",
    "pansiyon_apart": "pansiyon veya apart tipi konaklama",
    "kamp_karavan": "kamp veya karavan alanı",
    "hostel": "hostel tipi konaklama",
    "ev_kiralama": "kiralık konaklama seçeneği",
    "restoran_lokanta": "yemek yenilebilecek bir restoran",
    "deniz_mahsulleri": "deniz mahsulleri ağırlıklı bir restoran",
    "kebap_izgara": "kebap ve ızgara odaklı bir mekan",
    "ev_yemekleri_esnaf": "ev yemekleri / esnaf lokantası",
    "fine_dining_romantik": "daha özel / romantik bir yemek deneyimi sunan mekan",
    "sokak_lezzeti": "sokak lezzeti noktası",
    "kafe": "kafe",
    "tatli_pastane": "tatlı / pastane",
    "kahve_uzmanlik": "kahve odaklı bir mekan",
    "meyhane_bar": "meyhane veya bar",
    "cay_bahcesi": "çay bahçesi",
}


def _temizle(metin: str | None, maks: int = 900) -> str | None:
    if not metin:
        return None
    temiz = re.sub(r"\s+", " ", metin).strip()
    if len(temiz) < 40:
        return None
    if len(temiz) > maks:
        kesik = temiz[: maks - 1].rsplit(" ", 1)[0]
        return kesik + "…"
    return temiz


@lru_cache(maxsize=256)
def wikipedia_ozeti(baslik: str) -> str | None:
    """Turkce Wikipedia'dan kisa ozet (extract) ceker. Bulunamazsa None."""
    try:
        yanit = requests.get(
            _WIKI_API,
            params={
                "action": "query",
                "format": "json",
                "prop": "extracts",
                "exintro": 1,
                "explaintext": 1,
                "redirects": 1,
                "titles": baslik,
            },
            timeout=_WIKI_TIMEOUT,
            headers={"User-Agent": "SamandiraGeziBot/0.1 (egitim; tanitim metni)"},
        )
        yanit.raise_for_status()
        sayfalar = yanit.json().get("query", {}).get("pages", {})
        for sayfa in sayfalar.values():
            if sayfa.get("missing") is not None:
                continue
            return _temizle(sayfa.get("extract"))
    except Exception:
        return None
    return None


def _google_hakkinda(birlesik: BirlesikYer) -> str | None:
    oz = birlesik.ozellikler
    if getattr(oz, "hakkinda", None):
        return _temizle(oz.hakkinda)
    ekstra = getattr(oz, "model_extra", None) or {}
    if isinstance(ekstra, dict):
        aday = ekstra.get("hakkinda") or ekstra.get("google_hakkinda")
        if aday:
            return _temizle(str(aday))
    return None


def _sablon_tanitim(birlesik: BirlesikYer) -> str:
    tur = _ALT_KATEGORI_TANITIM.get(birlesik.alt_kategori, "gezilebilecek bir yer")
    sehir = birlesik.sehir
    ilce = f" {birlesik.ilce} bölgesinde" if birlesik.ilce else f" {sehir}’da"
    ana = {
        AnaKategori.GEZILECEK_YER.value: f"{birlesik.isim},{ilce} {tur}. Ziyaretten önce güncel saat ve koşulları kontrol etmeni öneririz.",
        AnaKategori.YEME_ICME.value: f"{birlesik.isim},{ilce} {tur}. Menü ve yoğunluk güne göre değişebilir; mümkünse rezervasyon veya yoğun saatleri göz önünde bulundur.",
        AnaKategori.KONAKLAMA.value: f"{birlesik.isim},{ilce} {tur}. Konum ve olanaklar seyahat planına göre değerlendirilmeli; güncel fiyat ve müsaitlik için doğrudan tesisle iletişime geçmek en sağlıklısı.",
    }
    return ana.get(birlesik.ana_kategori.value, f"{birlesik.isim},{ilce} {tur}.")


def yer_tanitim_metni_uret(birlesik: BirlesikYer, wiki_denensin: bool = True) -> str:
    """Oncelik sirasina gore bir tanitim paragrafi dondurur (asla bos olmaz)."""
    google = _google_hakkinda(birlesik)
    if google:
        return google

    if wiki_denensin:
        for aday_baslik in (birlesik.isim, f"{birlesik.isim} ({birlesik.sehir})", f"{birlesik.isim}, {birlesik.sehir}"):
            ozet = wikipedia_ozeti(aday_baslik)
            if ozet and turkce_kucuk_harf(birlesik.sehir)[:4] in turkce_kucuk_harf(ozet):
                return ozet
            # Sehir gecmiyorsa yine de kisa ve isimle basliyorsa kabul et
            if ozet and turkce_kucuk_harf(ozet).startswith(turkce_kucuk_harf(birlesik.isim)[:8]):
                return ozet

    osm = _temizle(birlesik.aciklama)
    if osm:
        return osm

    return _sablon_tanitim(birlesik)


def bolge_tanitim_metni_uret(bolge_adi: str, sehir_isim: str, ilce_mi: bool) -> str:
    if wiki_baslik := (bolge_adi if ilce_mi else sehir_isim):
        # Sehir geneli icin sehir adi, ilce icin "Ilce, Sehir"
        arama = f"{bolge_adi}, {sehir_isim}" if ilce_mi and bolge_adi.lower() != sehir_isim.lower() else sehir_isim
        if ilce_mi:
            for baslik in (f"{bolge_adi}, {sehir_isim}", bolge_adi, f"{bolge_adi} ({sehir_isim})"):
                ozet = wikipedia_ozeti(baslik)
                if ozet:
                    return ozet
        else:
            ozet = wikipedia_ozeti(sehir_isim) or wikipedia_ozeti(arama)
            if ozet:
                return ozet

    if ilce_mi:
        return (
            f"{bolge_adi}, {sehir_isim} iline bağlı bir ilçedir. "
            f"Bölgeyi tanımak için sahil, merkez ve çevre yerleşimleri birlikte düşünmek faydalıdır; "
            f"konaklama ve gezi planını buradaki yoğunluğa göre şekillendirebilirsin."
        )
    return (
        f"{sehir_isim}, Karadeniz kıyısında gezilecek yerleri, yeme-içme seçenekleri ve "
        f"konaklama alternatifleriyle öne çıkan bir şehirdir. İlçeleri ve sahil bandı "
        f"farklı ritimler sunar; rotanı buna göre kurmak deneyimi zenginleştirir."
    )
