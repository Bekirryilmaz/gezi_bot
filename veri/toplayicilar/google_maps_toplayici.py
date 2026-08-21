"""
Google Maps toplayicisi.

OSM'den farkli olarak Google Maps'in resmi/ucretsiz bir API'si (yorumlarla
birlikte) yok; bu yuzden bir internet tarayicisini otomatik yoneterek
(Playwright) sanki gercek bir kullanici geziniyormus gibi veri toplar:

- Istekler arasinda RASTGELE sureli beklemeler kullanilir (sabit araliklar
  bot izlenimi verir).
- Kullanici ajani (user-agent) her calistirmada degisir.
- Sayfa kaydirma (scroll) islemleri de anlik degil, adim adim ve aralarda
  bekemeli yapilir.

Onemli not (bakim): Google, sayfa yapisini ve CSS sinif isimlerini sik sik
degistirir. Bu yuzden secicilerin (selector) BUYUK COGUNLUGU bu dosyanin en
ustundeki `SECICILER` sozlugunde toplanmistir -- bir sey calismamaya
basladiginda once orayi kontrol et/guncelle. Ayrica mumkun oldugunca class
adi yerine daha kalici olan HTML ozniteliklerine (data-review-id, aria-label
vb.) ve "en yakin kaydirilabilir ata" gibi yapisal/genel yontemlere
guvenilmistir.

BILINEN KISIT (2026 itibariyle test edildi): Google, oturum acilmamis
(hesaba giris yapilmamis) ve otomasyon izlenimi veren tarayici oturumlarina
"sinirli gorunum" gosteriyor -- bu gorunumde yorum sayisi ve yorumlar
sekmesi/bolumu tamamen gizleniyor, sadece isim/adres/telefon/kategori/puan
gibi temel bilgiler kaliyor. Yani bu toplayici GUVENILIR SEKILDE yer bilgisi
(isim, kategori, adres, telefon, web sitesi, konum, puan) cekebiliyor ama
yorum METNI cekmek cogu zaman mumkun olmuyor (yorumlar bos liste donebilir,
bu bir hata degil, Google'in kisitlamasi). Bu yuzden proje tasarimda yorum
(duygu analizi) verisinin ana kaynagi Eksi Sozluk, TripAdvisor ve zamanla
kendi site-ici kullanici yorumlarimiz olacak (bkz. dokumanlar klasoru) --
Google Maps burada oncelikle bir "yer katalogu/dogrulama" kaynagi olarak
kullanilmali. Ileride hesaba giris yapilmis kalici bir oturum (persistent
context) denenebilir ama bu, hesabin askiya alinma riskini IP banindan daha
ciddi hale getirir; bu karari vermeden once tekrar degerlendir.

Calistirma (repo kokunden):
    python -m veri.toplayicilar.google_maps_toplayici --sehir samsun
"""

from __future__ import annotations

import argparse
import re
import threading
import time
from pathlib import Path
from urllib.parse import quote_plus

from playwright.sync_api import Page, sync_playwright
from pydantic import ValidationError

from ortak.sabitler import VeriKaynagi
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_tek_satir_ekle
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir, turkce_kucuk_harf
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.ortak.yer_modeli import OzellikSeti, Yer

from veri.ortak.yorum_modeli import HamYorum
from veri.toplayicilar.ortak_araclar import (
    engel_metni_var_mi,
    kullanici_ajani_sec,
    metinden_kategori_esle,
    mevcut_kaynak_idlerini_yukle,
    rastgele_bekle,
    uzun_ara_bekle,
)


class GoogleMapsEngellendiHatasi(Exception):
    """Google'in bot-korumasi (unusual traffic/captcha) sayfasi algilandiginda
    firlatilir; `calistir()` bunu yakalayip o ana kadarki veriyi diskte
    birakarak nazikce durur (bkz. tripadvisor_toplayici.py::_engellenmis_mi
    ile ayni felsefe)."""

# ---------------------------------------------------------------------------
# SECICILER: Google Maps sayfasindaki elemanlari bulmak icin kullanilan CSS
# secicileri / metinleri. Google bunlari degistirdiginde SADECE burasi
# guncellenmeli, asagidaki fonksiyonlara dokunmaya gerek kalmamali.
# ---------------------------------------------------------------------------
SECICILER = {
    "cerez_kabul_metinleri": ["Tümünü kabul et", "Kabul Et", "Accept all", "I agree"],
    "sonuc_karti_linki": "a.hfpxzc",
    "yer_ismi_basligi": "h1",
    "adres_dugmesi": 'button[data-item-id="address"]',
    "telefon_dugmesi": 'button[data-item-id^="phone"]',
    "website_linki": 'a[data-item-id="authority"]',
    # Onem sirasina gore denenir (bkz. _yer_detayini_cek); tek bir CSS
    # secicisinde birlestirmiyoruz cunku DOM'daki ilk eslesme her zaman en
    # guvenilir olan olmayabiliyor.
    "puan_alani_oncelikli": ["div.F7nice", 'span[aria-label*="yıldız"]', 'span[aria-label*="star"]'],
    "kategori_dugmesi": 'button[jsaction*="category"], .DkEaL',
    "hakkinda_dugmesi": 'button[aria-label*="Hakkında" i], button[aria-label*="About" i], button[data-item-id="about"]',
    "hakkinda_metin": 'div[aria-label*="Hakkında" i], div.PYvSYb, div.WeS02d',
    "yorumlar_sekmesi_metinleri": ["Yorumlar", "yorum", "Reviews"],
    "yorum_kutusu": "div[data-review-id]",
    "yorum_yazar_dugmesi": 'button[data-href*="/maps/contrib/"]',
    "daha_fazla_goster_dugmesi": 'button[aria-label*="Daha fazla" i], button[aria-label*="more" i]',
}

# Kategori esleme mantigi artik ortak_araclar.metinden_kategori_esle
# icinde -- TripAdvisor toplayicisi da (kendi kategori metniyle) ayni
# tabloyu kullaniyor, boylece iki kaynak arasinda taksonomi tutarliligi saglanir.

# Bir sehirde genis kapsam elde etmek icin taranacak varsayilan arama
# terimleri. dokumanlar/kategori_taksonomisi.md'deki ana basliklari kabaca
# temsil eder. Google Maps'te "<terim> <sehir>" seklinde aranir.
VARSAYILAN_ARAMA_TERIMLERI = [
    # --- Orijinal cekirdek terimler ---
    "gezilecek yerler",
    "tarihi yerler",
    "müzeler",
    "plajlar",
    "kamp alanları",
    "oteller",
    "pansiyonlar",
    "restoranlar",
    "kebapçılar",
    "deniz ürünleri restoranları",
    "kafeler",
    "tatlıcılar",
    "barlar",
    "gece kulüpleri",
    "parklar",
    "yürüyüş parkurları",
    # --- Faz 1 ile eklenen ek terimler: dini/tarihi, alisveris, yeme-icme
    # alt turleri, eglence ve doga -- amac dokumanlar/kategori_taksonomisi.md
    # taksonomisinin genel arama terimleriyle ONCEDEN kacirilan koselerini
    # kapatmak (bkz. plan Faz 1). ---
    "camiler",
    "kiliseler",
    "türbeler",
    "alışveriş merkezleri",
    "çarşılar",
    "pideciler",
    "lahmacuncular",
    "dönerciler",
    "mantıcılar",
    "kahvaltı mekanları",
    "pastaneler",
    "çikolatacılar",
    "hamamlar",
    "spa merkezleri",
    "sinemalar",
    "tiyatrolar",
    "şelaleler",
    "göletler",
    "yaylalar",
    "akvaryumlar",
    "hayvanat bahçeleri",
    "lunapark",
    "sanat galerileri",
    "kütüphaneler",
]


# Ilce-bazli aramada KULLANILACAK, en genel/kapsayici terimler -- 17 ilce ile
# CARPILDIGINDA arama sayisi hizla buyudugu icin (17 ilce x N terim), bilerek
# sadece en genel/yuksek getirili birkac terimle sinirlanir. Detay terimler
# (pideci, cami vb.) zaten sehir capinda VARSAYILAN_ARAMA_TERIMLERI ile araniyor.
_ILCE_BAZLI_ARAMA_TERIMLERI = ["gezilecek yerler", "restoranlar", "kafeler", "plajlar"]


def _ilce_bazli_arama_terimlerini_uret(sehir_anahtari: str) -> list[str]:
    """Sehrin ilceleriyle (varsa) `_ILCE_BAZLI_ARAMA_TERIMLERI`'ni carparak
    "<terim> <ilce> <sehir>" seklinde ek arama terimleri uretir -- sehir
    merkezi disindaki cografi kapsamayi artirmak icindir. Sehir icin ilce
    tanimli degilse bos liste doner (hata vermez)."""
    sehir = sehir_getir(sehir_anahtari)
    if not sehir.ilceler:
        return []
    return [f"{terim} {ilce}" for ilce in sehir.ilceler for terim in _ILCE_BAZLI_ARAMA_TERIMLERI]


def _en_yakin_kaydirilabilir_atayi_kaydir(sayfa: Page, ornek_eleman_secici: str, kac_kere: int = 8) -> None:
    """Verilen secici ile eslesen ilk elemanin en yakin kaydirilabilir
    (scrollable) atasini bulup asagi kaydirir.

    Google'in class isimlerine degil, DOM'daki gercek "scroll edilebilir mi"
    ozelligine bakar -- bu yuzden Google arayuzu degisse bile buyuk ihtimalle
    calismaya devam eder.
    """
    js_kodu = """
    (secici) => {
        const eleman = document.querySelector(secici);
        if (!eleman) return false;
        let ata = eleman.parentElement;
        while (ata) {
            if (ata.scrollHeight > ata.clientHeight + 50) {
                ata.scrollTop = ata.scrollHeight;
                return true;
            }
            ata = ata.parentElement;
        }
        return false;
    }
    """
    for _ in range(kac_kere):
        bulundu = sayfa.evaluate(js_kodu, ornek_eleman_secici)
        if not bulundu:
            break
        rastgele_bekle(1.2, 2.8)


def _engellenmis_mi(sayfa: Page) -> bool:
    """Google'in "unusual traffic" / captcha duvarina takilip takilmadigimizi
    kontrol eder. TripAdvisor'daki kadar agresif bir korumayla sik
    karsilasilmaz ama saatlerce suren buyuk taramalarda ihtimal sifir degil
    -- tespit edilirse `calistir()` o ana kadar toplanan veriyi diskte
    birakarak nazikce durur, sonraki calistirma `--devam-et` ile devam eder."""
    try:
        return engel_metni_var_mi(sayfa.content())
    except Exception:
        return False


def _cerezleri_kabul_et(sayfa: Page) -> None:
    for metin in SECICILER["cerez_kabul_metinleri"]:
        try:
            dugme = sayfa.get_by_role("button", name=metin)
            if dugme.count() > 0:
                dugme.first.click(timeout=3000)
                rastgele_bekle(1.0, 2.0)
                return
        except Exception:
            continue


def _arama_sonuc_linklerini_topla(sayfa: Page, maks_sonuc: int) -> list[str]:
    onceki_sayisi = 0
    for _ in range(15):
        linkler = sayfa.locator(SECICILER["sonuc_karti_linki"])
        sayi = linkler.count()
        if sayi >= maks_sonuc or sayi == onceki_sayisi:
            break
        onceki_sayisi = sayi
        _en_yakin_kaydirilabilir_atayi_kaydir(sayfa, SECICILER["sonuc_karti_linki"])

    linkler = sayfa.locator(SECICILER["sonuc_karti_linki"])
    sayi = min(linkler.count(), maks_sonuc)
    hrefler = []
    for i in range(sayi):
        href = linkler.nth(i).get_attribute("href")
        if href:
            hrefler.append(href)
    return hrefler


def _simge_mi(karakter: str) -> bool:
    """Google, ikonlarini (telefon, konum vb.) 'ozel kullanim alani' (private
    use area) unicode karakterleriyle bir font uzerinden gosterir. Bu
    karakterler metne karisir (orn. '\\ue0c8\\nAtaturk Blv. No:5'). Bu
    fonksiyon boyle bir karakteri tespit eder ki asagida temizleyebilelim."""
    return 0xE000 <= ord(karakter) <= 0xF8FF


def _dugme_metnini_temizle(ham_metin: str | None) -> str | None:
    """Bir dugmenin ic metninden ikon satirlarini cikarip gercek metni dondurur."""
    if not ham_metin:
        return None
    satirlar = [satir.strip() for satir in ham_metin.split("\n")]
    anlamli_satirlar = [satir for satir in satirlar if satir and not all(_simge_mi(k) for k in satir)]
    sonuc = " ".join(anlamli_satirlar).strip()
    return sonuc or None


# Yorum kutusunun ham metninde gecen, gercek yorum cumlelerine ait OLMAYAN
# bilinen "anahtar" satirlar (Google bunlari "Anahtar\nDeger" seklinde iki
# ayri satir olarak ya da "Anahtar: Deger" tek satir olarak gosterebiliyor).
_YORUM_METAVERI_ANAHTARLARI = {
    "kişi başı fiyat", "yiyecek", "hizmet", "atmosfer", "gürültü seviyesi",
    "grup büyüklüğü", "bekleme süresi", "park yeri", "park yeri seçenekleri",
    "rezervasyon", "vejetaryen seçenekler", "diyet kısıtlamaları",
    "çocuklara uygunluk", "özel etkinlikler", "öğün",
}


def _yorum_metnini_temizle(ham_blok: str) -> str:
    """Ham yorum kutusundan (yazar adi, 'Yerel Rehber - N yorum' bilgisi,
    tarih, 'Begen'/'Paylas' dugmeleri, isletme sahibi yaniti, alt puan
    kirilimlari gibi) gurultuyu ayiklayip geriye sadece yorumcunun kendi
    yazdigi metni birakmaya calisir.

    Google'in "sadece yorum metni" icin sabit/kalici bir HTML etiketi yok,
    bu yuzden bu temizlik metin desenlerine (heuristic) dayanir -- yuzde yuz
    mukemmel olmayabilir ama ham bloktan cok daha temiz bir sonuc verir.
    Kalan gurultu varsa veri/duygu_analizi asamasinda ek temizlik yapilabilir.
    """
    satirlar = [s.strip() for s in ham_blok.split("\n") if s.strip()]

    temiz_satirlar: list[str] = []
    baslik_satirlari_bitti = False
    for satir in satirlar:
        if satir in ("Beğen", "Paylaş"):
            continue
        if satir.startswith("İşletme sahibinin yanıtı"):
            break  # Bundan sonrasi isletme cevabi, yorumcunun kendi metni degil.

        if not baslik_satirlari_bitti:
            # Yazar adi / "Yerel Rehber - N yorum - M fotograf" / "X ay once" gibi
            # baslik satirlarini atla; bunlarin sonuncusu genelde bir tarih ifadesidir.
            if "yerel rehber" in turkce_kucuk_harf(satir) or re.search(r"\d+\s*(yorum|fotoğraf)", turkce_kucuk_harf(satir)):
                continue
            if re.search(r"(önce|YENİ|düzenlendi)$", satir):
                baslik_satirlari_bitti = True
                continue
            if not temiz_satirlar and len(satir) < 40 and ":" not in satir:
                continue  # Muhtemelen yazarin adi (baska hicbir isaretci olmadan).

        anahtar = turkce_kucuk_harf(satir.split(":")[0].strip())
        if turkce_kucuk_harf(satir) in _YORUM_METAVERI_ANAHTARLARI or anahtar in _YORUM_METAVERI_ANAHTARLARI:
            continue

        temiz_satirlar.append(satir)

    return " ".join(temiz_satirlar).strip()


def _sayidan_puan_cikar(metin: str | None) -> float | None:
    if not metin:
        return None
    eslesme = re.search(r"(\d+[.,]?\d*)", metin)
    if not eslesme:
        return None
    return float(eslesme.group(1).replace(",", "."))


def _yorumlar_sekmesine_gec(sayfa: Page) -> bool:
    for metin in SECICILER["yorumlar_sekmesi_metinleri"]:
        try:
            sekme = sayfa.get_by_role("tab", name=re.compile(metin, re.IGNORECASE))
            if sekme.count() > 0:
                sekme.first.click(timeout=3000)
                rastgele_bekle(1.5, 3.0)
                return True
        except Exception:
            continue
    return False


def _yorumlari_cek(sayfa: Page, kaynak_yer_id: str, maks_yorum: int) -> list[HamYorum]:
    if not _yorumlar_sekmesine_gec(sayfa):
        return []

    _en_yakin_kaydirilabilir_atayi_kaydir(sayfa, SECICILER["yorum_kutusu"], kac_kere=maks_yorum // 3 + 3)

    # "Daha fazla" butonlarina tiklayip kirpilmis yorum metinlerini genislet
    try:
        daha_fazla_dugmeleri = sayfa.locator(SECICILER["daha_fazla_goster_dugmesi"])
        for i in range(min(daha_fazla_dugmeleri.count(), maks_yorum)):
            try:
                daha_fazla_dugmeleri.nth(i).click(timeout=300)
            except Exception:
                pass
    except Exception:
        pass

    yorum_kutulari = sayfa.locator(SECICILER["yorum_kutusu"])
    toplam = min(yorum_kutulari.count(), maks_yorum * 2)  # Google bazen ayni yorumu DOM'da iki kez basabiliyor

    yorumlar: list[HamYorum] = []
    gorulen_yorum_idleri: set[str] = set()
    for i in range(toplam):
        if len(yorumlar) >= maks_yorum:
            break
        kutu = yorum_kutulari.nth(i)
        try:
            kaynak_yorum_id = kutu.get_attribute("data-review-id") or f"{kaynak_yer_id}-{i}"
            if kaynak_yorum_id in gorulen_yorum_idleri:
                continue  # Ayni yorum DOM'da tekrar etmis, atla.
            gorulen_yorum_idleri.add(kaynak_yorum_id)

            ham_metin = kutu.inner_text(timeout=500).strip()
            if not ham_metin:
                continue

            yazar_takma_adi = None
            try:
                yazar_dugmesi = kutu.locator(SECICILER["yorum_yazar_dugmesi"]).first
                if yazar_dugmesi.count() > 0:
                    yazar_takma_adi = yazar_dugmesi.inner_text(timeout=300).strip() or None
            except Exception:
                pass
            if not yazar_takma_adi:
                # Yedek yontem: yorum kutusunun ilk satiri hemen hemen her zaman
                # yazarin (goruntulenen) adidir.
                ilk_satir = ham_metin.split("\n", 1)[0].strip()
                yazar_takma_adi = ilk_satir or None

            puan = None
            try:
                puan_elemani = kutu.locator('[aria-label*="star"], [aria-label*="yıldız"]').first
                if puan_elemani.count() > 0:
                    puan = _sayidan_puan_cikar(puan_elemani.get_attribute("aria-label"))
            except Exception:
                pass

            metin = _yorum_metnini_temizle(ham_metin)
            if not metin:
                continue

            yorumlar.append(
                HamYorum(
                    kaynak=VeriKaynagi.GOOGLE_MAPS,
                    kaynak_yer_id=kaynak_yer_id,
                    kaynak_yorum_id=kaynak_yorum_id,
                    yazar_takma_adi=yazar_takma_adi,
                    yorum_metni=metin,
                    kaynakta_puan=puan,
                )
            )
        except Exception as hata:
            print(f"[UYARI] Bir yorum okunamadi, atlaniyor: {hata}")
            continue

    return yorumlar


def _sayfaya_git_yeniden_denemeli(sayfa: Page, url: str, deneme_sayisi: int = 3, timeout_ms: int = 30000) -> None:
    """`sayfa.goto` bazen (Faz 6'da gozlenen `net::ERR_NAME_NOT_RESOLVED` gibi)
    tamamen GECICI bir ag/DNS hatasiyla basarisiz olabilir -- bu tek seferlik
    bir engelleme DEGILDIR, sadece bir aglik hiccup'tir. Boyle bir hatada
    tum saatlik taramayi dusurmek yerine, kisa bir bekleme ile 1-2 kez daha
    denenir. Son denemede de basarisiz olursa hata YUKARI FIRLATILIR --
    caginan kod (calistir() icindeki arama-terimi dongusu) bunu yakalayip
    SADECE o terimi/yeri atlar, tarama COKMEZ."""
    son_hata: Exception | None = None
    for deneme in range(1, deneme_sayisi + 1):
        try:
            sayfa.goto(url, timeout=timeout_ms)
            return
        except Exception as hata:
            son_hata = hata
            if deneme < deneme_sayisi:
                print(f"[UYARI] Sayfaya gidilemedi (deneme {deneme}/{deneme_sayisi}), kisa bir bekleme sonrasi tekrar denenecek: {hata}")
                time.sleep(5.0 * deneme)
    assert son_hata is not None
    raise son_hata


class _ZamanAsimiBekcisi:
    """Bir tek yerin islenmesi (detay + yorumlar) belirli bir saniyeyi
    (varsayilan 100 sn) asarsa, sayfayi ZORLA kapatan bir 'bekci' (watchdog).

    Neden gerekli: Playwright'in kendi eylem timeout'lari (bkz.
    `baglam.set_default_timeout`) NORMAL sartlarda her cagriyi sinirlar, ama
    Faz 6'da COK saatlik gercek bir taramada gozlemlendigi uzere, tarayici
    surecinin kendisi (CDP baglantisi) beklenmedik bir sekilde YANIT VERMEZ
    hale gelebiliyor -- bu durumda Playwright'in kendi timeout mekanizmasi
    bile tetiklenmeyebilir ve tek bir yerin islenmesi SONSUZA KADAR surup tum
    saatlerce surecek taramayi tamamen kilitleyebilir. Bu bekci, `saniye`
    dolduğunda sayfayi disaridan zorla kapatarak ana thread'deki bloke olmus
    Playwright cagrisinin bir hata firlatmasini GARANTI EDER -- caginan
    kodun try/except'i devreye girip taramaya devam edebilir (bkz.
    `calistir()` icindeki `sayfa.is_closed()` kontrolu, kapali sayfa
    tespit edilince yeni bir sayfa acilir)."""

    def __init__(self, sayfa: Page, saniye: float = 100.0) -> None:
        self._sayfa = sayfa
        self._saniye = saniye
        self._zamanlayici = threading.Timer(saniye, self._zorla_kapat)

    def _zorla_kapat(self) -> None:
        print(f"[UYARI] Bir yerin islenmesi {self._saniye:.0f} saniyeyi asti (tarayici sureci yanit vermiyor olabilir), sayfa zorla kapatiliyor -- tarama bir sonraki yerle devam edecek.")
        try:
            self._sayfa.close()
        except Exception:
            pass

    def __enter__(self) -> "_ZamanAsimiBekcisi":
        self._zamanlayici.start()
        return self

    def __exit__(self, *_args: object) -> None:
        self._zamanlayici.cancel()


def _url_den_kaynak_id_cikar(url: str) -> str:
    """`_yer_detayini_cek` icindeki kaynak_id cikarma mantiginin URL-ONCESI
    (sayfayi hic acmadan) calisabilen hali -- arama sonuc listesindeki href'ler
    de detay sayfasiyla AYNI `!1s...` bicimini tasir. Bu, ana dongude ZATEN
    islenmis bir yeri, pahali (ve nadiren tikanan) tam sayfa ziyaretine hic
    girmeden ERKENDEN atlayabilmek icin kullanilir (bkz. `calistir()`)."""
    eslesme = re.search(r"!1s([^!]+)", url)
    return eslesme.group(1) if eslesme else url


def _yer_detayini_cek(sayfa: Page, url: str, sehir_adi: str, maks_yorum: int) -> tuple[Yer | None, list[HamYorum]]:
    _sayfaya_git_yeniden_denemeli(sayfa, url)
    rastgele_bekle(2.5, 5.0)

    try:
        isim = sayfa.locator(SECICILER["yer_ismi_basligi"]).first.inner_text(timeout=5000).strip()
    except Exception:
        print(f"[UYARI] Yer ismi okunamadi, atlaniyor: {url}")
        return None, []

    # Google Maps konumu URL'de iki farkli bicimde gorunebilir:
    #   1) .../@<enlem>,<boylam>,<zoom> (harita gorunumu URL'i)
    #   2) .../data=...!3d<enlem>!4d<boylam>... (yer detay URL'i -- daha sik rastlanan bicim)
    # Sayfa yuklendikten sonraki GUNCEL adres (sayfa.url) kullanilir, cunku
    # Google Maps sayfayi actiktan sonra adresi kendi ekliyor.
    guncel_url = sayfa.url
    enlem = boylam = None
    eslesme = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", guncel_url) or re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", url)
    if eslesme:
        enlem, boylam = float(eslesme.group(1)), float(eslesme.group(2))
    else:
        eslesme = re.search(r"!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)", guncel_url) or re.search(
            r"!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)", url
        )
        if eslesme:
            enlem, boylam = float(eslesme.group(1)), float(eslesme.group(2))
    if enlem is None or boylam is None:
        print(f"[UYARI] '{isim}' icin konum URL'den cikarilamadi, atlaniyor.")
        return None, []

    kategori_metni = None
    try:
        kategori_dugmesi = sayfa.locator(SECICILER["kategori_dugmesi"]).first
        if kategori_dugmesi.count() > 0:
            kategori_metni = kategori_dugmesi.inner_text(timeout=1000)
    except Exception:
        pass
    # Once Google'in kategori etiketini dene; yoksa/eslenemezse yer ISMINDEN
    # yedek esleme yap (orn. 'Anemon Grand Samsun Otel' -> otel). Bu, Google
    # bazi otel/plaj sayfalarinda kategori dugmesini gostermediginde veya
    # 'Heykel'/'Kumsal' gibi henuz sozlukte olmayan ama isimde ipucu tasiyan
    # durumlarda kaydi tamamen atlamak yerine kurtarir.
    # Isim eslemesi ONCE denenir: Google bazen "Konaklama Tesisi" gibi COK
    # genel bir etiket yazarken isimde "kamp"/"camping"/"otel" gibi daha
    # spesifik bir ipucu bulunur (bkz. Faz 6: 'Çadır Kent Camping' +
    # 'Konaklama Tesisi' -> kamp_karavan tercihi). Isimden hicbir sey
    # cikmazsa Google'in kategori etiketine dusulur.
    kategori_sonucu = metinden_kategori_esle(isim) or metinden_kategori_esle(kategori_metni)
    if kategori_sonucu is None:
        print(f"[UYARI] '{isim}' icin kategori eslenemedi ('{kategori_metni}'), atlaniyor.")
        return None, []
    ana_kategori, alt_kategori = kategori_sonucu

    adres = None
    try:
        adres_dugmesi = sayfa.locator(SECICILER["adres_dugmesi"]).first
        if adres_dugmesi.count() > 0:
            adres = _dugme_metnini_temizle(adres_dugmesi.inner_text(timeout=1000))
    except Exception:
        pass

    telefon = None
    try:
        telefon_dugmesi = sayfa.locator(SECICILER["telefon_dugmesi"]).first
        if telefon_dugmesi.count() > 0:
            telefon = _dugme_metnini_temizle(telefon_dugmesi.inner_text(timeout=1000))
    except Exception:
        pass

    web_sitesi = None
    try:
        website_linki = sayfa.locator(SECICILER["website_linki"]).first
        if website_linki.count() > 0:
            web_sitesi = website_linki.get_attribute("href")
    except Exception:
        pass

    puan_ortalamasi = puan_sayisi = None
    for secici in SECICILER["puan_alani_oncelikli"]:
        try:
            puan_alani = sayfa.locator(secici).first
            if puan_alani.count() == 0:
                continue
            puan_metni = puan_alani.inner_text(timeout=1000) or puan_alani.get_attribute("aria-label") or ""
            puan_ortalamasi = _sayidan_puan_cikar(puan_metni)
            if puan_ortalamasi is not None:
                break
        except Exception:
            continue
    # Not (bilinen kisit): Google, oturum acilmamis/otomasyon gorunumlu
    # oturumlara "sinirli gorunum" gosterip yorum sayisini ve yorumlar
    # sekmesini gizleyebiliyor -- bu durumda puan_sayisi ve asagidaki
    # yorumlar listesi bos donebilir. Bu beklenen bir davranistir, hata degildir.

    # Google Maps place id'sini URL'den cikarmaya calis (yoksa URL'in kendisini kullan)
    kaynak_id_eslesme = re.search(r"!1s([^!]+)", url)
    kaynak_id = kaynak_id_eslesme.group(1) if kaynak_id_eslesme else url

    hakkinda = None
    try:
        hakkinda_dugme = sayfa.locator(SECICILER["hakkinda_dugmesi"]).first
        if hakkinda_dugme.count() > 0:
            hakkinda_dugme.click(timeout=800)
            rastgele_bekle(0.4, 0.9)
        metin_alani = sayfa.locator(SECICILER["hakkinda_metin"]).first
        if metin_alani.count() > 0:
            ham = metin_alani.inner_text(timeout=800).strip()
            if ham and len(ham) > 40:
                hakkinda = ham[:1200]
    except Exception:
        pass

    try:
        yer = Yer(
            kaynak=VeriKaynagi.GOOGLE_MAPS,
            kaynak_id=kaynak_id,
            kaynak_url=url,
            isim=isim,
            ana_kategori=ana_kategori,
            alt_kategori=alt_kategori,
            sehir=sehir_adi,
            adres=adres,
            aciklama=hakkinda,
            telefon=telefon,
            web_sitesi=web_sitesi,
            enlem=enlem,
            boylam=boylam,
            kaynakta_puan_ortalamasi=puan_ortalamasi,
            kaynakta_puan_sayisi=puan_sayisi,
            ozellikler=OzellikSeti(hakkinda=hakkinda) if hakkinda else OzellikSeti(),
        )
    except ValidationError as hata:
        print(f"[UYARI] '{isim}' dogrulanamadi, atlaniyor: {hata}")
        return None, []

    yorumlar = _yorumlari_cek(sayfa, kaynak_id, maks_yorum)
    return yer, yorumlar


def calistir(
    sehir_anahtari: str,
    arama_terimleri: list[str] | None = None,
    maks_sonuc_terim_basi: int = 20,
    maks_yorum_yer_basi: int = 15,
    headless: bool = True,
    ilce_bazli_arama: bool = False,
    devam_et_dosyasi: str | Path | None = None,
) -> None:
    sehir = sehir_getir(sehir_anahtari)
    arama_terimleri = list(arama_terimleri or VARSAYILAN_ARAMA_TERIMLERI)
    if ilce_bazli_arama:
        arama_terimleri = arama_terimleri + _ilce_bazli_arama_terimlerini_uret(sehir_anahtari)

    kok = Path(__file__).resolve().parents[1] / "cikti" / "ham" / "google_maps"
    if devam_et_dosyasi is not None:
        # Onceki (muhtemelen kesintiye ugramis) bir calistirmaya devam
        # ediyoruz: aynen o dosyaya (yerler) ve esdegeri yorum dosyasina
        # EKLEME yapariz, sifirdan baslamayiz.
        yerler_dosyasi = Path(devam_et_dosyasi)
        yorumlar_dosyasi = Path(str(yerler_dosyasi).replace("_yerler_", "_yorumlar_"))
        print(f"[BILGI] Onceki calistirmaya devam ediliyor: {yerler_dosyasi}")
    else:
        tarih = bugunun_tarihi_dosya_adi()
        yerler_dosyasi = kok / f"{sehir.anahtar}_yerler_{tarih}.jsonl"
        yorumlar_dosyasi = kok / f"{sehir.anahtar}_yorumlar_{tarih}.jsonl"

    islenen_kaynak_idler: set[str] = mevcut_kaynak_idlerini_yukle(yerler_dosyasi)
    if islenen_kaynak_idler:
        print(f"[BILGI] {len(islenen_kaynak_idler)} yer daha once islenmis bulundu, bunlar atlanacak.")
    toplam_yer = toplam_yorum = 0

    with sync_playwright() as p:
        # Oracle sunucu gibi ekransiz (headless) ortamlarda headless=True sart.
        # Yerel bilgisayarinda tarayiciyi gozle izleyip hata ayiklamak
        # istersen --headed bayragini kullan.
        tarayici = p.chromium.launch(headless=headless)
        baglam = tarayici.new_context(
            user_agent=kullanici_ajani_sec(),
            locale="tr-TR",
            viewport={"width": 1366, "height": 900},
        )
        # Playwright'in varsayilan eylem timeout'u (30 sn) bazi durumlarda
        # (orn. tarayici surecinin gecici olarak yanit vermemesi) COK saatlik
        # bir tarama boyunca sessizce birikip beklenmedik uzun duruslara yol
        # acabiliyor -- burada BILINCLI olarak biraz daha SIKI bir tavan
        # koyuyoruz ki tek bir sikismis eylem, o terimin/yerin try/except'ine
        # daha CABUK dusup taramanin devam etmesini saglasin.
        baglam.set_default_timeout(20000)
        baglam.set_default_navigation_timeout(30000)
        sayfa = baglam.new_page()

        try:
            for terim_no, terim in enumerate(arama_terimleri, start=1):
                arama_sorgusu = f"{terim} {sehir.google_maps_arama_bolgesi}"
                print(f"[BILGI] ({terim_no}/{len(arama_terimleri)}) Aranıyor: '{arama_sorgusu}'")

                arama_url = f"https://www.google.com/maps/search/{quote_plus(arama_sorgusu)}?hl=tr"
                try:
                    _sayfaya_git_yeniden_denemeli(sayfa, arama_url)
                except Exception as hata:
                    # Bu, arama sayfasina ULASAMAMA hatasidir (orn. gecici bir
                    # DNS/ag sorunu, 3 denemeden sonra da cozulmedi) -- Google'in
                    # bot-korumasi DEGIL. Boyle bir durumda SADECE bu terimi
                    # atlayip devam ederiz; tum saatlik taramayi dusurmeyiz
                    # (bkz. Faz 6'da gozlenen ERR_NAME_NOT_RESOLVED olayi).
                    print(f"[UYARI] ({terim_no}/{len(arama_terimleri)}) '{arama_sorgusu}' icin arama sayfasina ulasilamadi, bu terim atlaniyor: {hata}")
                    continue
                rastgele_bekle(2.0, 4.0)

                if _engellenmis_mi(sayfa):
                    raise GoogleMapsEngellendiHatasi(
                        f"'{arama_sorgusu}' aranirken Google'in bot-korumasi duvarina takildik. "
                        "O ana kadar toplanan veri diskte kaldi; bir sure sonra "
                        f"'--devam-et {yerler_dosyasi}' ile devam edilebilir."
                    )

                _cerezleri_kabul_et(sayfa)

                try:
                    hrefler = _arama_sonuc_linklerini_topla(sayfa, maks_sonuc_terim_basi)
                except Exception as hata:
                    print(f"[UYARI] ({terim_no}/{len(arama_terimleri)}) '{arama_sorgusu}' icin sonuc listesi okunamadi, bu terim atlaniyor: {hata}")
                    continue
                print(f"[BILGI]   {len(hrefler)} sonuc bulundu.")

                for sira, href in enumerate(hrefler, start=1):
                    # Tam sayfa ziyaretinden ONCE, url'den kaynak_id'yi cikarip
                    # zaten islenmis mi diye bak -- boylece farkli arama
                    # terimlerinin ortusen sonuclarinda (cok yaygin) her
                    # tekrarda pahali (ve nadiren tikanan) bir sayfa
                    # ziyaretine hic girilmez (bkz. Faz 6 gozlemi: 189
                    # islenmis yerin bulundugu bir devam calistirmasinda,
                    # bu erken kontrol olmadan ayni sonuclar tekrar tekrar
                    # tam ziyaret ediliyordu).
                    if _url_den_kaynak_id_cikar(href) in islenen_kaynak_idler:
                        continue
                    rastgele_bekle()
                    try:
                        with _ZamanAsimiBekcisi(sayfa):
                            yer, yorumlar = _yer_detayini_cek(sayfa, href, sehir.isim, maks_yorum_yer_basi)
                    except Exception as hata:
                        print(f"[UYARI] ({sira}/{len(hrefler)}) '{href}' islenirken hata olustu, atlaniyor: {hata}")
                        continue
                    finally:
                        if sayfa.is_closed():
                            # Yukaridaki _ZamanAsimiBekcisi zorla kapatti (veya
                            # baska bir sebeple sayfa oldu) -- yeni bir sayfa
                            # acip taramaya devam ediyoruz, tekrar denemiyoruz
                            # (bu yer/terim bu turda atlanmis sayilir).
                            print("[BILGI] Sayfa kapanmisti, yeni bir sayfa acilip taramaya devam ediliyor.")
                            sayfa = baglam.new_page()
                    if yer is None:
                        continue
                    if yer.kaynak_id in islenen_kaynak_idler:
                        continue  # Farkli arama terimleri ayni yeri getirmis olabilir
                    islenen_kaynak_idler.add(yer.kaynak_id)

                    jsonl_tek_satir_ekle(yerler_dosyasi, yer)
                    toplam_yer += 1
                    for yorum in yorumlar:
                        jsonl_tek_satir_ekle(yorumlar_dosyasi, yorum)
                    toplam_yorum += len(yorumlar)

                    print(f"[BILGI]   ({sira}/{len(hrefler)}) '{yer.isim}' kaydedildi ({len(yorumlar)} yorumla).")

                    if sira % 10 == 0:
                        uzun_ara_bekle()
        except GoogleMapsEngellendiHatasi as hata:
            print(f"[UYARI] {hata}")
        finally:
            tarayici.close()

    print(f"[BILGI] Tamamlandi. Bu calistirmada {toplam_yer} yeni yer, {toplam_yorum} yorum kaydedildi.")
    print(f"[BILGI] Yerler: {yerler_dosyasi}")
    print(f"[BILGI] Yorumlar: {yorumlar_dosyasi}")


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(description="Google Maps'ten bir sehrin yer ve yorum verisini topla.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    ayristirici.add_argument("--maks-sonuc", type=int, default=25, help="Arama terimi basina maksimum sonuc sayisi")
    ayristirici.add_argument("--maks-yorum", type=int, default=35, help="Yer basina maksimum yorum sayisi")
    ayristirici.add_argument(
        "--headed", action="store_true", help="Tarayiciyi gorunur modda ac (yerel hata ayiklama icin)"
    )
    ayristirici.add_argument(
        "--ilce-bazli-arama",
        action="store_true",
        help="Sehrin ilceleriyle de ek aramalar yap (daha kapsamli ama daha uzun surer)",
    )
    ayristirici.add_argument(
        "--devam-et",
        default=None,
        help="Onceki (kesintiye ugramis) bir '<sehir>_yerler_<tarih>.jsonl' dosyasinin yolu -- verilirse "
        "o dosyadaki yerler atlanip ayni dosyaya EKLEME yapilarak devam edilir.",
    )
    argumanlar = ayristirici.parse_args()
    calistir(
        argumanlar.sehir,
        maks_sonuc_terim_basi=argumanlar.maks_sonuc,
        maks_yorum_yer_basi=argumanlar.maks_yorum,
        headless=not argumanlar.headed,
        ilce_bazli_arama=argumanlar.ilce_bazli_arama,
        devam_et_dosyasi=argumanlar.devam_et,
    )


if __name__ == "__main__":
    _ana()
