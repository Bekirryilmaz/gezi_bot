"""
Tum toplayicilarin (osm, google_maps, eksi_sozluk, tripadvisor) ortak kullandigi
kucuk yardimci fonksiyonlar: rastgele bekleme (insan-taklidi gecikme),
kullanici ajani (user-agent) rotasyonu ve serbest metinden taksonomi
kategorisi cikarma.

Not: OpenStreetMap Overpass API resmi/ucretsiz bir API'dir, insan-taklidi
gecikmeye ihtiyaci yoktur -- bu araclar ozellikle google_maps_toplayici.py ve
tripadvisor_toplayici.py gibi tarayici otomasyonu kullanan modullerde
kullanilir.
"""

from __future__ import annotations

import random
import time
from pathlib import Path

from ortak.sabitler import AnaKategori
from veri.ortak.dosya_araclari import jsonl_oku
from veri.ortak.metin_araclari import turkce_kucuk_harf

# Google Maps ve TripAdvisor'in kendi (Turkce) kategori/etiket metinlerini
# bizim taksonomimize (dokumanlar/kategori_taksonomisi.md) esleyen ORTAK
# tablo. Iki farkli kaynak, kendi kategori sozcuklerini kullansa da hedef
# taksonomi ayni oldugu icin bu esleme tek bir yerde tutulur -- boylece iki
# toplayici arasinda ayni kelimenin farkli kategoriye esitlenmesi riski
# ortadan kalkar. Anahtar kucuk harfe cevrilip metin icinde aranir (esnek
# eslesme icin), bu yuzden hem "Kebapçı" hem "En iyi kebap" gibi varyasyonlar
# tek bir "kebap" anahtariyla yakalanir.
METIN_TABANLI_KATEGORI_ESLEMESI: dict[str, tuple[AnaKategori, str]] = {
    "internet cafe": (AnaKategori.YEME_ICME, "internet_kafe"),
    "internet kafe": (AnaKategori.YEME_ICME, "internet_kafe"),
    "internet_cafe": (AnaKategori.YEME_ICME, "internet_kafe"),
    "internetcafe": (AnaKategori.YEME_ICME, "internet_kafe"),
    "kafe": (AnaKategori.YEME_ICME, "kafe"),
    "kahve": (AnaKategori.YEME_ICME, "kahve_uzmanlik"),
    "pastane": (AnaKategori.YEME_ICME, "tatli_pastane"),
    "tatlı": (AnaKategori.YEME_ICME, "tatli_pastane"),
    "dondurma": (AnaKategori.YEME_ICME, "tatli_pastane"),
    "fast food": (AnaKategori.YEME_ICME, "sokak_lezzeti"),
    "büfe": (AnaKategori.YEME_ICME, "sokak_lezzeti"),
    "sokak lezzet": (AnaKategori.YEME_ICME, "sokak_lezzeti"),
    "deniz ürünleri": (AnaKategori.YEME_ICME, "deniz_mahsulleri"),
    "balık": (AnaKategori.YEME_ICME, "deniz_mahsulleri"),
    "kebap": (AnaKategori.YEME_ICME, "kebap_izgara"),
    "ızgara": (AnaKategori.YEME_ICME, "kebap_izgara"),
    "pide": (AnaKategori.YEME_ICME, "sokak_lezzeti"),
    "pideci": (AnaKategori.YEME_ICME, "sokak_lezzeti"),
    "lahmacun": (AnaKategori.YEME_ICME, "sokak_lezzeti"),
    "steakhouse": (AnaKategori.YEME_ICME, "kebap_izgara"),
    "steak": (AnaKategori.YEME_ICME, "kebap_izgara"),
    "ev yemek": (AnaKategori.YEME_ICME, "ev_yemekleri_esnaf"),
    "lokanta": (AnaKategori.YEME_ICME, "ev_yemekleri_esnaf"),
    "esnaf": (AnaKategori.YEME_ICME, "ev_yemekleri_esnaf"),
    "restoran": (AnaKategori.YEME_ICME, "restoran_lokanta"),
    "bar": (AnaKategori.YEME_ICME, "meyhane_bar"),
    "meyhane": (AnaKategori.YEME_ICME, "meyhane_bar"),
    "pub": (AnaKategori.YEME_ICME, "meyhane_bar"),
    "gece kulüb": (AnaKategori.GEZILECEK_YER, "gece_hayati"),
    "otel": (AnaKategori.KONAKLAMA, "otel"),
    "hotel": (AnaKategori.KONAKLAMA, "otel"),
    "motel": (AnaKategori.KONAKLAMA, "otel"),
    "pansiyon": (AnaKategori.KONAKLAMA, "pansiyon_apart"),
    "apart": (AnaKategori.KONAKLAMA, "pansiyon_apart"),
    "hostel": (AnaKategori.KONAKLAMA, "hostel"),
    "kamp": (AnaKategori.KONAKLAMA, "kamp_karavan"),
    "karavan": (AnaKategori.KONAKLAMA, "kamp_karavan"),
    "müze": (AnaKategori.GEZILECEK_YER, "tarihi_kulturel"),
    "ören yeri": (AnaKategori.GEZILECEK_YER, "tarihi_kulturel"),
    "tarihi": (AnaKategori.GEZILECEK_YER, "tarihi_kulturel"),
    "kale": (AnaKategori.GEZILECEK_YER, "tarihi_kulturel"),
    "anıt": (AnaKategori.GEZILECEK_YER, "tarihi_kulturel"),
    "heykel": (AnaKategori.GEZILECEK_YER, "tarihi_kulturel"),
    "saat kule": (AnaKategori.GEZILECEK_YER, "tarihi_kulturel"),
    "cami": (AnaKategori.GEZILECEK_YER, "dini_manevi"),
    "kilise": (AnaKategori.GEZILECEK_YER, "dini_manevi"),
    "sinagog": (AnaKategori.GEZILECEK_YER, "dini_manevi"),
    "plaj": (AnaKategori.GEZILECEK_YER, "plaj_su"),
    "sahil": (AnaKategori.GEZILECEK_YER, "plaj_su"),
    "kumsal": (AnaKategori.GEZILECEK_YER, "plaj_su"),
    "yüzme": (AnaKategori.GEZILECEK_YER, "plaj_su"),
    "yuzme": (AnaKategori.GEZILECEK_YER, "plaj_su"),
    "night club": (AnaKategori.GEZILECEK_YER, "gece_hayati"),
    "eğlence": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "lunapark": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "oyun merkez": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "park": (AnaKategori.GEZILECEK_YER, "doga_manzara"),
    "koru": (AnaKategori.GEZILECEK_YER, "doga_manzara"),
    "orman": (AnaKategori.GEZILECEK_YER, "doga_manzara"),
    "doğa": (AnaKategori.GEZILECEK_YER, "doga_manzara"),
    "yürüyüş": (AnaKategori.GEZILECEK_YER, "spor_doga_yuruyus"),
    "tur": (AnaKategori.GEZILECEK_YER, "spor_doga_yuruyus"),
    "alışveriş": (AnaKategori.GEZILECEK_YER, "alisveris"),
    "çarşı": (AnaKategori.GEZILECEK_YER, "alisveris"),
    "pazar": (AnaKategori.GEZILECEK_YER, "alisveris"),
    "avm": (AnaKategori.GEZILECEK_YER, "alisveris"),
    "alışveriş merkezi": (AnaKategori.GEZILECEK_YER, "alisveris"),
    # --- Veri derinlestirme (Faz 1) ile eklenen ek eslemeler ---
    # Yeme-icme: onceden kacirilan yaygin Google/TripAdvisor kategori metinleri.
    "çikolata": (AnaKategori.YEME_ICME, "tatli_pastane"),
    "dönerci": (AnaKategori.YEME_ICME, "kebap_izgara"),
    "döner": (AnaKategori.YEME_ICME, "kebap_izgara"),
    "pizza": (AnaKategori.YEME_ICME, "restoran_lokanta"),
    "sushi": (AnaKategori.YEME_ICME, "restoran_lokanta"),
    "hamburger": (AnaKategori.YEME_ICME, "restoran_lokanta"),
    "burger": (AnaKategori.YEME_ICME, "restoran_lokanta"),
    "waffle": (AnaKategori.YEME_ICME, "tatli_pastane"),
    "çay bahçesi": (AnaKategori.YEME_ICME, "cay_bahcesi"),
    "mantı": (AnaKategori.YEME_ICME, "ev_yemekleri_esnaf"),
    "kahvaltı": (AnaKategori.YEME_ICME, "restoran_lokanta"),
    "künefe": (AnaKategori.YEME_ICME, "tatli_pastane"),
    "baklava": (AnaKategori.YEME_ICME, "tatli_pastane"),
    "waffle evi": (AnaKategori.YEME_ICME, "tatli_pastane"),
    # Gezilecek yer: dini/tarihi/eglence/doga alt turleri.
    "türbe": (AnaKategori.GEZILECEK_YER, "dini_manevi"),
    "manastır": (AnaKategori.GEZILECEK_YER, "dini_manevi"),
    "sinema": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "tiyatro": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "hamam": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "spa": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "kaplıca": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "akvaryum": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "hayvanat bahçesi": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "bowling": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
    "şelale": (AnaKategori.GEZILECEK_YER, "doga_manzara"),
    "gölet": (AnaKategori.GEZILECEK_YER, "doga_manzara"),
    "göl": (AnaKategori.GEZILECEK_YER, "doga_manzara"),
    "yayla": (AnaKategori.GEZILECEK_YER, "doga_manzara"),
    "mağara": (AnaKategori.GEZILECEK_YER, "doga_manzara"),
    "sanat galerisi": (AnaKategori.GEZILECEK_YER, "tarihi_kulturel"),
    "galeri": (AnaKategori.GEZILECEK_YER, "tarihi_kulturel"),
    "kütüphane": (AnaKategori.GEZILECEK_YER, "tarihi_kulturel"),
    # Konaklama: Google/Booking.com'da farkli adlandirilan mulk tipleri.
    "villa": (AnaKategori.KONAKLAMA, "ev_kiralama"),
    "tatil köyü": (AnaKategori.KONAKLAMA, "otel"),
    "resort": (AnaKategori.KONAKLAMA, "otel"),
    "misafirhane": (AnaKategori.KONAKLAMA, "pansiyon_apart"),
    "guesthouse": (AnaKategori.KONAKLAMA, "pansiyon_apart"),
    # Google Maps bazi otel/kamp sayfalarinda kategori olarak genel
    # "Konaklama Tesisi" yazar (ozel tip yerine) -- yine de konaklama olarak
    # kabul edilir. "camping" Ingilizce etiketi de kamp alt kategorisine
    # dusurulur (bkz. Faz 6 kanarya: 'Çadır Kent Camping' atlaniyordu).
    "konaklama": (AnaKategori.KONAKLAMA, "otel"),
    "camping": (AnaKategori.KONAKLAMA, "kamp_karavan"),
    "bungalov": (AnaKategori.KONAKLAMA, "ev_kiralama"),
    "bungalow": (AnaKategori.KONAKLAMA, "ev_kiralama"),
    "kiralık daire": (AnaKategori.KONAKLAMA, "ev_kiralama"),
    "kiralik daire": (AnaKategori.KONAKLAMA, "ev_kiralama"),
    "günlük kiralık": (AnaKategori.KONAKLAMA, "ev_kiralama"),
    "gunluk kiralik": (AnaKategori.KONAKLAMA, "ev_kiralama"),
    # Ulasim/eglence: Google Maps "Dağ Teleferiği" etiketi.
    "teleferik": (AnaKategori.GEZILECEK_YER, "eglence_aktivite"),
}


def metinden_kategori_esle(metin: str | None) -> tuple[AnaKategori, str] | None:
    """Herhangi bir kaynagin (Google Maps kategori etiketi, TripAdvisor
    ust-kategori/breadcrumb metni vb.) serbest metnini bizim (ana_kategori,
    alt_kategori) taksonomimize esler. Eslesme bulunamazsa None doner --
    cagiran kod bu durumda kaydi atlamayi (kalitesiz veri uretmemek icin)
    tercih etmelidir."""
    if not metin:
        return None
    kucuk_metin = turkce_kucuk_harf(metin)
    for anahtar_metin, sonuc in sorted(
        METIN_TABANLI_KATEGORI_ESLEMESI.items(),
        key=lambda parca: len(parca[0]),
        reverse=True,
    ):
        if anahtar_metin in kucuk_metin:
            return sonuc
    return None

# Gercek tarayicilarin gonderdigi, yaygin kullanici ajani (user-agent) degerleri.
# Her istek/oturumda rastgele biri secilerek "hep ayni bot" izlenimi azaltilir.
KULLANICI_AJANLARI: list[str] = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
]


def kullanici_ajani_sec() -> str:
    return random.choice(KULLANICI_AJANLARI)


def rastgele_bekle(min_saniye: float = 2.5, maks_saniye: float = 6.0) -> None:
    """Istekler arasinda insan davranisina benzeyen, degisken sureli bekleme.

    Sabit bir gecikme (orn. hep 3 saniye) yerine rastgele bir aralik
    kullanmak, "her istek arasinda tam X saniye var" gibi belirgin bir bot
    imzasi birakmamak icindir.
    """
    time.sleep(random.uniform(min_saniye, maks_saniye))


def uzun_ara_bekle(min_saniye: float = 20.0, maks_saniye: float = 45.0) -> None:
    """Her N kayittan sonra (orn. her 20-30 yer/yorumdan sonra) yapilan,
    normal bekleme araligindan daha uzun bir 'mola'. Gercek bir kullanicinin
    ara sira durup sayfaya bakmasini/dinlenmesini taklit eder."""
    time.sleep(random.uniform(min_saniye, maks_saniye))


def mevcut_kaynak_idlerini_yukle(dosya: Path, alan_adi: str = "kaynak_id") -> set[str]:
    """Bir toplayici cikti dosyasi (orn. `<sehir>_yerler_<tarih>.jsonl`) daha
    once kismen doldurulmussa (orn. cok saatlik bir tarama yarida kesintiye
    ugradiysa), bu fonksiyon o dosyadaki kayitlarin `alan_adi` degerlerini
    okuyup bir kume olarak dondurur -- caginan toplayici bu kimlikleri
    "zaten islenmis" sayip atlayabilir, boylece SIFIRDAN baslamak zorunda
    kalinmaz (bkz. veri/toplayicilar/tum_kaynaklari_calistir.py ve
    her toplayicinin `--devam-et` bayragi).

    Dosya yoksa veya okunamazsa bos kume doner (hata firlatmaz) -- devam
    etme bir "best effort" ozelligidir, olmamasi taramayi durdurmamali."""
    if not dosya.exists():
        return set()
    idler: set[str] = set()
    try:
        for kayit in jsonl_oku(dosya):
            deger = kayit.get(alan_adi)
            if deger:
                idler.add(str(deger))
    except Exception as hata:
        print(f"[UYARI] '{dosya}' devam-et icin okunamadi, sifirdan baslanacak: {hata}")
        return set()
    return idler


# Farkli bot korumasi sistemlerinin (DataDome, Akamai, reCAPTCHA/hCaptcha
# duvarlari, Google'in "unusual traffic" sayfasi vb.) HTML govdesinde veya
# gorunur metinde biraktigi, dile/siteye ozel olmayan ORTAK isaretler. Her
# toplayici kendi ozel ifadelerini bu listeye EKLEYEREK cagirir (bkz.
# tripadvisor_toplayici.py::_engellenmis_mi, google_maps_toplayici.py'deki
# esdegeri) -- boylece "engellendi mi?" mantigi tek bir yerde bakim gorur.
ORTAK_ENGEL_IFADELERI: tuple[str, ...] = (
    "captcha-delivery.com",
    "erişim geçici olarak kısıtlanmıştır",
    "access to this page has been denied",
    "access to this page has been blocked",
    "unusual traffic",
    "olağan dışı trafik",
    "g-recaptcha",
    "hcaptcha",
    "checking your browser",
    "just a moment",
    "recaptcha",
)


def engel_metni_var_mi(ham_html: str, ek_ifadeler: tuple[str, ...] = ()) -> bool:
    """Bir sayfanin ham HTML'inde (gorunur metin degil -- bazi engelleme
    duvarlari captcha-delivery.com gibi bir iframe icinde gelir ve gorunur
    metne YANSIMAZ) bilinen bot-korumasi isaretlerinden biri geciyor mu diye
    bakar. `ek_ifadeler` ile kaynaga ozel ekstra ifadeler eklenebilir."""
    kucuk_html = turkce_kucuk_harf(ham_html)
    tum_ifadeler = ORTAK_ENGEL_IFADELERI + ek_ifadeler
    return any(ifade in kucuk_html for ifade in tum_ifadeler)
