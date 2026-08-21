"""
Booking.com toplayicisi (konaklama/otel yorumlari).

BILINEN, KRITIK ENGEL (2026-08-03'te "Veri Derinlestirme" plani Faz 5
sirasinda tespit edildi -- BOT KORUMASI DEGIL, YASAL/DUZENLEYICI BIR ENGEL):

Booking.com, 2017'de Istanbul 5. Asliye Ticaret Mahkemesi'nin TURSAB'in
haksiz rekabet davasinda verdigi ihtiyati tedbir karari geregince, TURKIYE
IP'SINDEN erisen kullanicilara TURKIYE'DEKI tesisler icin ARAMA SONUCU
GOSTERMIYOR ve dogrudan otel sayfalarina gidildiginde bile bu sayfalari ana
sayfaya YONLENDIRIYOR (redirect). Bu, TripAdvisor'daki DataDome bot
korumasindan TAMAMEN FARKLI bir engel turudur -- rastgele gecikme, user-agent
rotasyonu, "insan taklidi" davranis gibi hicbir bot-korumasi-atlatma teknigi
bunu COZEMEZ, cunku Booking.com bu kisitlamaya KENDI ISTEGIYLE (mahkeme
karari geregi) uyuyor. Test sirasinda:
  1. Arama sonuc sayfasi (searchresults.tr.html?ss=Samsun...) SIFIR otel
     karti dondurdu, sadece "Simdilik Turkiye'de bulunan musterilerimize
     maalesef sadece yurt disi tesisler icin rezervasyon yapabiliyoruz..."
     uyarisi gosterildi.
  2. Google'da bulunan DOGRUDAN bir Samsun oteli URL'si
     (booking.com/hotel/tr/anemon-samsun.html) ACILDIGINDA DA otelin kendi
     sayfasina degil, Booking.com ANA SAYFASINA yonlendirildi.
Yani bu engel arama VE dogrudan sayfa erisiminin HER IKISINI de kapsiyor.

EK BULGU (proje icin onemli): Ayni oteller, TURKIYE DISINDAN erisildiginde
(bu ortamdaki web-arama araciyla dogrulandi) normal sekilde aciliyor, ama
gorunen yorumlarin BUYUK COGUNLUGU YABANCI dilde (Ingilizce, Rusca, Arapca)
-- cunku Turkiyeli gezginler bu platformu yerli otel rezervasyonu icin
KULLANAMIYOR. Bu, projenin Turkce-agirlikli duygu analizi hattiyla (BERT
Turkce model + konu_analizi.py'nin Turkce anahtar kelime sozlugu) kismen
CELISIYOR -- yani engel bir sekilde asilsa bile getiri, Google Maps/Eksi
Sozluk kadar Turkce-yogun OLMAYACAKTIR.

SONUC/KARAR: `tum_kaynaklari_calistir.py` bu kaynagi VARSAYILAN OLARAK
ATLAR (bkz. o dosyadaki `--booking-dene` bayragi) -- TripAdvisor'la ayni
muamele. Bu modul SILINMEDI: (1) haber kaynaklarina gore Booking.com'un
Turkiye'ye donusu icin yasal duzenleme TBMM gundeminde (bkz. commit
tarihi itibariyla guncel haberler), yasallasirsa bu kisitlama kalkabilir;
(2) Oracle Cloud sunucusu TURKIYE DISINDA bir bolgede (orn. Frankfurt,
Amsterdam) saglanirsa engel gecerli olmayabilir. Asagidaki seciciler bu
yuzden CANLI DOGRULANAMADAN (TripAdvisor'daki durumla ayni sekilde)
yazilmistir -- once JSON-LD (schema.org) tabanli, DOM'a en az bagimli
yontem denenir; kullanmadan once --headed ile TEK bir sayfa acip gozle
dogrulaman siddetle onerilir.

Calistirma (repo kokunden, engel kalkarsa/farkli bir agdan):
    python -m veri.toplayicilar.booking_toplayici --sehir samsun --headed --maks-sonuc 3
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright
from pydantic import ValidationError

from ortak.sabitler import VeriKaynagi
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_tek_satir_ekle
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir, turkce_kucuk_harf
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.ortak.yer_modeli import Yer
from veri.ortak.yorum_modeli import HamYorum
from veri.toplayicilar.ortak_araclar import (
    engel_metni_var_mi,
    kullanici_ajani_sec,
    metinden_kategori_esle,
    mevcut_kaynak_idlerini_yukle,
    rastgele_bekle,
    uzun_ara_bekle,
)

TABAN_ADRES = "https://www.booking.com"

# Bu proje kapsaminda TESPIT EDILEN Turkiye-ozel engelin isaretleri (bkz.
# modul dokstring'i). `ortak_araclar.ORTAK_ENGEL_IFADELERI`'ne ek olarak
# buraya EKLENIR (bkz. _engellenmis_mi).
_TURKIYE_ENGELI_IFADELERI: tuple[str, ...] = (
    "sadece yurt dışı tesisler için rezervasyon",
    "sadece yurt disi tesisler icin rezervasyon",
    "only book properties abroad",
)

# DOM tabanli yedek yontem icin seciciler -- CANLI DOGRULANAMADI (bkz. modul
# dokstring'i), TripAdvisor modulundeki durumun ayni. Booking.com'un
# `data-testid` kullanimi yaygin oldugu icin oncelik bunlara verilir.
SECICILER = {
    "cerez_kabul_metinleri": ["Kabul Et", "Accept", "I agree"],
    "sonuc_karti": '[data-testid="property-card"]',
    "sonuc_karti_linki": '[data-testid="title-link"]',
    "yer_ismi_basligi": "h2",
    "adres_alani": '[data-testid="address"]',
    "puan_alani": '[data-testid="review-score"]',
}


def _engellenmis_mi(sayfa: Page, beklenen_url_oneki: str | None = None) -> bool:
    """Turkiye-ozel yonlendirme engelini (bkz. modul dokstring'i) VE genel
    bot-korumasi isaretlerini (ortak_araclar.engel_metni_var_mi) kontrol eder.
    `beklenen_url_oneki` verilirse, sayfanin GUNCEL url'i bu onekle
    baslamiyorsa (yani anasayfaya yonlendirildiysek) da engellenmis sayilir."""
    try:
        if beklenen_url_oneki and not sayfa.url.startswith(beklenen_url_oneki):
            return True
    except Exception:
        pass
    try:
        html = sayfa.content()
    except Exception:
        return False
    return engel_metni_var_mi(html, _TURKIYE_ENGELI_IFADELERI)


class BookingEngellendiHatasi(Exception):
    """Booking.com'un Turkiye-ozel erisim kisitlamasi (veya bot korumasi)
    tespit edildiginde firlatilir. bkz. modul dokstring'i -- bu YASAL bir
    kisitlama olabilir, bu durumda tekrar denemek FAYDASIZDIR."""

    def __init__(self, url: str) -> None:
        super().__init__(
            f"Booking.com bu oturumdan/bolgeden erisimi kisitliyor (URL: {url}). "
            "bkz. veri/toplayicilar/booking_toplayici.py modul dokstring'i -- bu bir "
            "IP/bot korumasi degil, TURKIYE'YE OZEL YASAL bir kisitlama olabilir "
            "(mahkeme karari), bu durumda ayni agdan tekrar denemek sonucu degistirmez."
        )
        self.url = url


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


def _json_ld_bloklarini_cikar(html: str) -> list[dict[str, Any]]:
    corba = BeautifulSoup(html, "lxml")
    sonuc: list[dict[str, Any]] = []
    for etiket in corba.find_all("script", type="application/ld+json"):
        if not etiket.string:
            continue
        try:
            veri = json.loads(etiket.string)
        except json.JSONDecodeError:
            continue
        adaylar = veri if isinstance(veri, list) else [veri]
        for aday in adaylar:
            if isinstance(aday, dict):
                sonuc.append(aday)
    return sonuc


def _sayidan_puan_cikar(metin: str | None) -> float | None:
    if not metin:
        return None
    eslesme = re.search(r"(\d+[.,]?\d*)", str(metin))
    if not eslesme:
        return None
    return float(eslesme.group(1).replace(",", "."))


# Booking.com'un "mulk tipi" (property type) metinlerini bizim taksonomimize
# esler -- METIN_TABANLI_KATEGORI_ESLEMESI zaten otel/pansiyon/hostel/apart
# icin genel eslemeler icerdigi icin burada sadece Booking'e ozel ek
# ifadeler (orn. "apart daire", "tatil evi") tanimlanir.
_MULK_TIPI_EK_ESLEME: dict[str, str] = {
    "apart daire": "ev_kiralama",
    "tatil evi": "ev_kiralama",
    "villa": "ev_kiralama",
    "butik otel": "otel",
    "konukevi": "pansiyon_apart",
}


def _mulk_tipini_esle(metin: str | None, isim: str) -> tuple[str, str] | None:
    if metin:
        for anahtar, alt_kategori in _MULK_TIPI_EK_ESLEME.items():
            if anahtar in turkce_kucuk_harf(metin):
                from ortak.sabitler import AnaKategori

                return AnaKategori.KONAKLAMA, alt_kategori
    return metinden_kategori_esle(metin) or metinden_kategori_esle(isim)


def _yer_detayini_cek(sayfa: Page, url: str, sehir_adi: str, maks_yorum: int) -> tuple[Yer | None, list[HamYorum]]:
    try:
        sayfa.goto(url, timeout=30000)
    except Exception as hata:
        print(f"[UYARI] Sayfa yuklenemedi, atlaniyor: {url} ({hata})")
        return None, []
    rastgele_bekle(2.5, 5.0)

    if _engellenmis_mi(sayfa, beklenen_url_oneki=None):
        raise BookingEngellendiHatasi(url)

    html = sayfa.content()
    json_ld_bloklari = _json_ld_bloklarini_cikar(html)
    json_ld_yer = next(
        (b for b in json_ld_bloklari if str(b.get("@type", "")) in {"Hotel", "LodgingBusiness"}), None
    )

    isim = adres = None
    enlem = boylam = puan_ortalamasi = None
    puan_sayisi = None
    mulk_tipi_metni = None

    if json_ld_yer is not None:
        isim = json_ld_yer.get("name")
        adres_nesnesi = json_ld_yer.get("address")
        if isinstance(adres_nesnesi, dict):
            parcalar = [adres_nesnesi.get("streetAddress"), adres_nesnesi.get("addressLocality")]
            adres = ", ".join(p for p in parcalar if p) or None
        geo = json_ld_yer.get("geo")
        if isinstance(geo, dict):
            try:
                enlem = float(geo["latitude"])
                boylam = float(geo["longitude"])
            except (KeyError, TypeError, ValueError):
                pass
        puan_nesnesi = json_ld_yer.get("aggregateRating")
        if isinstance(puan_nesnesi, dict):
            puan_ortalamasi = _sayidan_puan_cikar(puan_nesnesi.get("ratingValue"))
            try:
                puan_sayisi = int(puan_nesnesi.get("reviewCount") or 0) or None
            except (TypeError, ValueError):
                puan_sayisi = None

    if not isim:
        try:
            isim = sayfa.locator(SECICILER["yer_ismi_basligi"]).first.inner_text(timeout=5000).strip()
        except Exception:
            print(f"[UYARI] '{url}' icin ne JSON-LD ne de DOM'dan isim okunabildi, atlaniyor.")
            return None, []

    if not adres:
        try:
            adres_alani = sayfa.locator(SECICILER["adres_alani"]).first
            if adres_alani.count() > 0:
                adres = adres_alani.inner_text(timeout=1000).strip() or None
        except Exception:
            pass

    if enlem is None or boylam is None:
        print(f"[UYARI] '{isim}' icin konum (enlem/boylam) bulunamadi, atlaniyor.")
        return None, []

    kategori_sonucu = _mulk_tipini_esle(mulk_tipi_metni, isim)
    if kategori_sonucu is None:
        print(f"[UYARI] '{isim}' icin kategori eslenemedi, atlaniyor.")
        return None, []
    ana_kategori, alt_kategori = kategori_sonucu

    kaynak_id_eslesme = re.search(r"/hotel/[a-z]{2}/([a-z0-9-]+)\.html", url)
    kaynak_id = kaynak_id_eslesme.group(1) if kaynak_id_eslesme else url

    try:
        yer = Yer(
            kaynak=VeriKaynagi.BOOKING_COM,
            kaynak_id=kaynak_id,
            kaynak_url=url,
            isim=isim,
            ana_kategori=ana_kategori,
            alt_kategori=alt_kategori,
            sehir=sehir_adi,
            adres=adres,
            enlem=enlem,
            boylam=boylam,
            kaynakta_puan_ortalamasi=puan_ortalamasi,
            kaynakta_puan_sayisi=puan_sayisi,
        )
    except ValidationError as hata:
        print(f"[UYARI] '{isim}' dogrulanamadi, atlaniyor: {hata}")
        return None, []

    yorumlar = _yorumlari_cek_best_effort(sayfa, kaynak_id, maks_yorum)
    return yer, yorumlar


def _yorumlari_cek_best_effort(sayfa: Page, kaynak_yer_id: str, maks_yorum: int) -> list[HamYorum]:
    """Booking.com'un yorum kutulari CANLI DOGRULANAMADI (bkz. modul
    dokstring'i) -- bu fonksiyon "yorum metni + varsa puan" iceren genel bir
    kart deseni arar, hicbir sey bulamazsa (hata degil) sessizce bos liste
    doner. Booking'in tipik yorum karti isaretcisi `data-testid="review"`
    (kamuya acik dokumantasyon/topluluk kaynaklarina gore) denenir."""
    yorumlar: list[HamYorum] = []
    try:
        kutular = sayfa.locator('[data-testid="review"]')
        toplam = min(kutular.count(), maks_yorum)
    except Exception:
        return yorumlar

    for i in range(toplam):
        try:
            kutu = kutular.nth(i)
            metin = kutu.inner_text(timeout=1000).strip()
            if not metin or len(metin) < 15:
                continue
            yorumlar.append(
                HamYorum(
                    kaynak=VeriKaynagi.BOOKING_COM,
                    kaynak_yer_id=kaynak_yer_id,
                    kaynak_yorum_id=f"{kaynak_yer_id}-{i}",
                    yorum_metni=metin,
                )
            )
        except Exception:
            continue
    return yorumlar


def _arama_sonuc_linklerini_topla(sayfa: Page, maks_sonuc: int) -> list[str]:
    onceki_sayisi = 0
    for _ in range(10):
        linkler = sayfa.locator(SECICILER["sonuc_karti_linki"])
        sayi = linkler.count()
        if sayi >= maks_sonuc or sayi == onceki_sayisi:
            break
        onceki_sayisi = sayi
        sayfa.mouse.wheel(0, 2000)
        rastgele_bekle(1.0, 2.5)

    linkler = sayfa.locator(SECICILER["sonuc_karti_linki"])
    sayi = min(linkler.count(), maks_sonuc)
    hrefler: list[str] = []
    for i in range(sayi):
        href = linkler.nth(i).get_attribute("href")
        if href:
            hrefler.append(href if href.startswith("http") else f"{TABAN_ADRES}{href}")
    return hrefler


def calistir(
    sehir_anahtari: str,
    maks_sonuc: int = 40,
    maks_yorum_yer_basi: int = 40,
    headless: bool = True,
    devam_et_dosyasi: str | Path | None = None,
) -> None:
    sehir = sehir_getir(sehir_anahtari)

    kok = Path(__file__).resolve().parents[1] / "cikti" / "ham" / "booking_com"
    if devam_et_dosyasi is not None:
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
        tarayici = p.chromium.launch(headless=headless)
        baglam = tarayici.new_context(
            user_agent=kullanici_ajani_sec(),
            locale="tr-TR",
            viewport={"width": 1366, "height": 900},
        )
        sayfa = baglam.new_page()

        try:
            arama_sorgusu = f"{sehir.isim}, Türkiye"
            arama_url = f"{TABAN_ADRES}/searchresults.tr.html?ss={quote_plus(arama_sorgusu)}&lang=tr"
            sayfa.goto(arama_url, timeout=30000)
            rastgele_bekle(2.5, 5.0)
            _cerezleri_kabul_et(sayfa)

            if _engellenmis_mi(sayfa):
                raise BookingEngellendiHatasi(arama_url)

            hrefler = _arama_sonuc_linklerini_topla(sayfa, maks_sonuc)
            print(f"[BILGI] {len(hrefler)} sonuc bulundu.")

            for sira, href in enumerate(hrefler, start=1):
                rastgele_bekle()
                try:
                    yer, yorumlar = _yer_detayini_cek(sayfa, href, sehir.isim, maks_yorum_yer_basi)
                except BookingEngellendiHatasi:
                    raise
                except Exception as hata:
                    print(f"[UYARI] ({sira}/{len(hrefler)}) '{href}' islenirken hata olustu, atlaniyor: {hata}")
                    continue
                if yer is None:
                    continue
                if yer.kaynak_id in islenen_kaynak_idler:
                    continue
                islenen_kaynak_idler.add(yer.kaynak_id)

                jsonl_tek_satir_ekle(yerler_dosyasi, yer)
                toplam_yer += 1
                for yorum in yorumlar:
                    jsonl_tek_satir_ekle(yorumlar_dosyasi, yorum)
                toplam_yorum += len(yorumlar)

                print(f"[BILGI]   ({sira}/{len(hrefler)}) '{yer.isim}' kaydedildi ({len(yorumlar)} yorumla).")

                if sira % 10 == 0:
                    uzun_ara_bekle()
        except BookingEngellendiHatasi as hata:
            print(f"[HATA] {hata}")
            print(
                f"[BILGI] Engellenmeden once {toplam_yer} yer, {toplam_yorum} yorum kaydedilmisti "
                "(bu veriler dosyada guvende, kayip yok)."
            )
        finally:
            tarayici.close()

    print(f"[BILGI] Tamamlandi. Bu calistirmada {toplam_yer} yeni yer, {toplam_yorum} yorum kaydedildi.")
    print(f"[BILGI] Yerler: {yerler_dosyasi}")
    print(f"[BILGI] Yorumlar: {yorumlar_dosyasi}")


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(description="Booking.com'dan bir sehrin konaklama yer ve yorum verisini topla.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    ayristirici.add_argument("--maks-sonuc", type=int, default=40, help="Maksimum otel/konaklama sonuc sayisi")
    ayristirici.add_argument("--maks-yorum", type=int, default=40, help="Yer basina maksimum yorum sayisi")
    ayristirici.add_argument(
        "--headed", action="store_true", help="Tarayiciyi gorunur modda ac (yerel hata ayiklama icin)"
    )
    ayristirici.add_argument(
        "--devam-et",
        default=None,
        help="Onceki (kesintiye ugramis) bir '<sehir>_yerler_<tarih>.jsonl' dosyasinin yolu",
    )
    argumanlar = ayristirici.parse_args()
    calistir(
        argumanlar.sehir,
        maks_sonuc=argumanlar.maks_sonuc,
        maks_yorum_yer_basi=argumanlar.maks_yorum,
        headless=not argumanlar.headed,
        devam_et_dosyasi=argumanlar.devam_et,
    )


if __name__ == "__main__":
    _ana()
