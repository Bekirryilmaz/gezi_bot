"""
TripAdvisor toplayicisi.

BILINEN ONEMLI KISIT (2026 itibariyle test edildi): TripAdvisor, Google Maps
ve Eksi Sozluk'ten cok daha agresif bir bot koruma sistemi (DataDome)
kullaniyor. En gelismis "insan taklidi" ayarlarla (webdriver bayragini
gizleme, rastgele user-agent, once ana sayfaya ugrayip sonra hedefe gitme,
rastgele gecikmeler) denendiginde bile, paylasimli/veri-merkezi
IP'lerinden (bulut sunucular dahil) gelen istekler DAHA ILK YUKLEMEDE
"Erisim gecici olarak kisitlanmistir" duvarina takilabiliyor. Bu, kodun bir
hatasi degil, TripAdvisor'in IP itibarina bakan bir korumasi. Bu engelleme
sayfasinin metni sayfanin govdesinde DEGIL, captcha-delivery.com'dan
yuklenen bir <iframe> icinde oldugu icin, tespit (_engellenmis_mi) gorunur
metne degil ham HTML'e (iframe kaynagi dahil) bakar.

Bu yuzden bu toplayici iki katmanli calisir:
1. Her sayfa yuklemesinden sonra bir engellenme sayfasi olup olmadigini
   kontrol eder (_engellenmis_mi). Engellenme tespit edilirse calisma
   HEMEN durdurulur (bos yere denemeye devam edip zaman harcanmaz) ve
   acik, eylem onerili bir Turkce uyari basilir.
2. Sayfa engellenmemisse, veriyi ONCELIKLE sayfanin kendi SEO amacli
   "yapisal veri" (schema.org JSON-LD, <script type="application/ld+json">)
   bloklarindan okur. Bu, CSS sinif adlarindan (orn. "biGQs _P pZUbB") COK
   daha guvenilir bir yontemdir cunku bu bloklar arama motorlari icin
   yazilir ve TripAdvisor tasarimini degistirse bile nadiren kaldirilir.
   JSON-LD'de bulunmayan alanlar (orn. tam yorum listesi) icin en son care
   olarak DOM tabanli (best-effort) bir yedek yontem kullanilir.

Pratik oneri: TripAdvisor surekli engelliyorsa, projenin veri stratejisinde
zaten belirtildigi gibi ana yorum kaynaklari Google Maps (yer bilgisi) ve
Eksi Sozluk (Turkce serbest metin) olarak kalsin; TripAdvisor'i sadece
IP'nin "temiz" oldugu donemlerde (orn. taze acilmis bulut sunucu, dusuk
istek hacmi, gunde birkac sayfa) ek/dogrulama kaynagi olarak kullan. DOM
tabanli secicileri (bkz. SECICILER) canli ortama almadan once --headed
bayragiyla TEK bir sayfa acip gozle dogrulaman siddetle onerilir, cunku bu
dosya TripAdvisor'in engeli yuzunden canli DOM uzerinde tam test edilerek
yazilamamistir.

KANARYA TESTI SONUCU (2026-08-03, "Veri Derinlestirme" plani Faz 4):
Bu toplayici, kullanicinin KENDI EV/REZIDANSIYEL IP'sinden (bulut/veri
merkezi IP'si DEGIL) `--maks-sonuc 3 --maks-yorum 5` ile test edildi.
Sonuc: ILK istekte (Attractions listeleme sayfasi) yine `_engellenmis_mi`
tarafindan DataDome engeli tespit edildi, 0 yer/yorum kaydedilmeden nazikce
durduruldu (veri kaybi yok). Yani engelleme sadece bulut/veri-merkezi
IP'lerine ozgu degil -- bu proje icin TripAdvisor'i GUVENILIR bir kaynak
olarak SAYMA, veri stratejisinde birincil kaynaklar Google Maps + Eksi
Sozluk (+ Booking.com) olarak kalsin. Bu toplayici koddan SILINMEDI (ileride
farkli bir IP/vekil ile tekrar denenebilir, ya da TripAdvisor korumasini
gevsetirse diye), ama `tum_kaynaklari_calistir.py` varsayilan olarak bu
kaynagi ATLAR (bkz. o dosyadaki `--tripadvisor-dene` bayragi).

Calistirma (repo kokunden):
    python -m veri.toplayicilar.tripadvisor_toplayici --sehir samsun
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright
from pydantic import ValidationError

from ortak.sabitler import VeriKaynagi
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_tek_satir_ekle
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir, turkce_kucuk_harf
from veri.ortak.sehir_ayarlari import SehirAyari, sehir_getir
from veri.ortak.yer_modeli import Yer
from veri.ortak.yorum_modeli import HamYorum
from veri.toplayicilar.ortak_araclar import (
    kullanici_ajani_sec,
    metinden_kategori_esle,
    mevcut_kaynak_idlerini_yukle,
    rastgele_bekle,
    uzun_ara_bekle,
)

TABAN_ADRES = "https://www.tripadvisor.com.tr"

# TripAdvisor'da her "kategori" (gezilecek yer / restoran / otel) kendi
# listeleme URL bicimine ve detay sayfasi URL onekine sahiptir. Sehir yolu
# (orn. "g298035-Samsun_Turkish_Black_Sea_Coast") "g<lokasyon_id>-<slug>"
# seklindedir; asagida ikiye ayrilir.
KATEGORILER: dict[str, dict[str, str]] = {
    "gezilecek_yer": {
        "liste_sablonu": "/Attractions-{lokasyon_id}-Activities-{slug}.html",
        "detay_oneki": "/Attraction_Review-",
    },
    "restoran": {
        "liste_sablonu": "/Restaurants-{lokasyon_id}-{slug}.html",
        "detay_oneki": "/Restaurant_Review-",
    },
    "otel": {
        "liste_sablonu": "/Hotels-{lokasyon_id}-{slug}.html",
        "detay_oneki": "/Hotel_Review-",
    },
}

# DOM tabanli yedek yontem icin seciciler. bkz. modul docstring'indeki uyari:
# bunlar TripAdvisor'in engeli yuzunden canli test edilemedi, kullanmadan
# once dogrula.
SECICILER = {
    "cerez_kabul_metinleri": ["Tümünü kabul et", "Kabul Et", "Accept all", "I agree"],
    "yer_ismi_basligi": "h1",
    # Yorum kalici baglantilari genelde "-r<sayi>-" deseniyle URL icerir;
    # bu, sik degisen class isimlerinden cok daha kararli bir isaretcidir.
    "yorum_kalici_baglanti_deseni": re.compile(r"-r\d+-"),
}


def _engellenmis_mi(sayfa: Page) -> bool:
    """TripAdvisor'in bot-korumasi devreye girdiginde gosterdigi engelleme
    sayfasini tespit eder. Test sirasinda bunun DataDome (captcha-delivery.com)
    tabanli oldugu, "Erisim gecici olarak kisitlanmistir" metninin ise ana
    sayfada DEGIL, capctha-delivery.com'dan gelen bir <iframe> icinde
    oldugu goruldu -- yani sayfa govdesinin (body) gorunur metni BOS gelir,
    normal bir "metin ara" kontrolu bu yuzden yanilir. Bu nedenle asil
    kontrolu HAM HTML uzerinden (iframe kaynagini da gorebilecek sekilde)
    yapiyoruz, DOM'un gorsel olarak isledigi metin uzerinden degil.
    """
    try:
        baslik = turkce_kucuk_harf((sayfa.title() or "").strip())
    except Exception:
        baslik = ""
    try:
        html = turkce_kucuk_harf(sayfa.content())
    except Exception:
        html = ""

    # Kesin isaretci: DataDome'un CAPTCHA/engelleme iframe'inin kaynagi.
    if "captcha-delivery.com" in html:
        return True

    # Genel guvenlik agi: baslik sadece cip"lak" alan adindan ibaretse (orn.
    # "tripadvisor.com" veya "tripadvisor.com.tr") VE sayfa icerigi gercek
    # bir TripAdvisor sayfasi icin beklenenden COK kisa ise (gercek sayfalar
    # onbinlerce karakterdir), bu da baska bir engelleme/interstitial turunu
    # (ileride DataDome disi bir sistem devreye girerse) yakalar.
    if re.fullmatch(r"tripadvisor\.com(\.tr)?", baslik) and len(html) < 5000:
        return True

    engelleme_ifadeleri = [
        "erişim geçici olarak kısıtlanmıştır",
        "access to this page has been denied",
        "access to this page has been blocked",
    ]
    return any(ifade in html for ifade in engelleme_ifadeleri)


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


def _lokasyon_id_ve_slug(sehir: SehirAyari) -> tuple[str, str]:
    if not sehir.tripadvisor_sehir_yolu:
        raise ValueError(
            f"'{sehir.isim}' icin veri/ortak/sehir_ayarlari.py'de tripadvisor_sehir_yolu tanimli degil."
        )
    lokasyon_id, _, slug = sehir.tripadvisor_sehir_yolu.partition("-")
    if not lokasyon_id or not slug:
        raise ValueError(f"tripadvisor_sehir_yolu bicimi hatali: '{sehir.tripadvisor_sehir_yolu}' (beklenen: 'g123-Slug_Adi')")
    return lokasyon_id, slug


def _json_ld_bloklarini_cikar(html: str) -> list[dict[str, Any]]:
    """Sayfadaki tum <script type="application/ld+json"> bloklarini ayristirip
    duz bir sozluk listesine cevirir (bazi bloklar tek nesne, bazilari liste,
    bazilari "@graph" icinde ic ice liste olabilir -- hepsini duzlestirir)."""
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
            if not isinstance(aday, dict):
                continue
            if "@graph" in aday and isinstance(aday["@graph"], list):
                sonuc.extend(eleman for eleman in aday["@graph"] if isinstance(eleman, dict))
            else:
                sonuc.append(aday)
    return sonuc


def _tip_eslesiyor_mu(nesne: dict[str, Any], aranan_tipler: set[str]) -> bool:
    tip = nesne.get("@type")
    tipler = tip if isinstance(tip, list) else [tip]
    return any(str(t) in aranan_tipler for t in tipler if t)


def _json_ld_icinde_yer_bul(bloklar: list[dict[str, Any]]) -> dict[str, Any] | None:
    """LocalBusiness/TouristAttraction/Restaurant/LodgingBusiness gibi
    "yer" tanimlayan schema.org tiplerinden ilkini bulur."""
    aranan_tipler = {
        "LocalBusiness", "TouristAttraction", "Restaurant", "CafeOrCoffeeShop",
        "BarOrPub", "LodgingBusiness", "Hotel", "Museum", "Park",
    }
    for blok in bloklar:
        if _tip_eslesiyor_mu(blok, aranan_tipler):
            return blok
    return None


def _sayidan_puan_cikar(metin: str | None) -> float | None:
    if not metin:
        return None
    eslesme = re.search(r"(\d+[.,]?\d*)", str(metin))
    if not eslesme:
        return None
    return float(eslesme.group(1).replace(",", "."))


def _json_ld_yer_verisini_ayikla(
    json_ld_yer: dict[str, Any], varsayilan_kategori_ipucu: str
) -> tuple[str | None, str | None, str | None, float | None, float | None, str | None, float | None, int | None]:
    """JSON-LD nesnesinden (isim, adres, telefon, enlem, boylam, kategori_metni,
    puan_ortalamasi, puan_sayisi) demeti cikarir. Alan yoksa None doner."""
    isim = json_ld_yer.get("name")

    adres_nesnesi = json_ld_yer.get("address")
    adres = None
    if isinstance(adres_nesnesi, dict):
        parcalar = [adres_nesnesi.get("streetAddress"), adres_nesnesi.get("addressLocality")]
        adres = ", ".join(p for p in parcalar if p) or None
    elif isinstance(adres_nesnesi, str):
        adres = adres_nesnesi

    telefon = json_ld_yer.get("telephone")

    enlem = boylam = None
    geo = json_ld_yer.get("geo")
    if isinstance(geo, dict):
        try:
            enlem = float(geo["latitude"])
            boylam = float(geo["longitude"])
        except (KeyError, TypeError, ValueError):
            pass

    # Kategori ipucu icin schema.org tipini, varsa "servesCuisine" alanini ve
    # bizim listeleme sayfasindan gelen ipucunu birlestiriyoruz -- boylece
    # metinden_kategori_esle en genis anahtar kelime havuzuyla calisir.
    tip = json_ld_yer.get("@type")
    tip_metni = " ".join(tip) if isinstance(tip, list) else str(tip or "")
    mutfak = json_ld_yer.get("servesCuisine")
    mutfak_metni = " ".join(mutfak) if isinstance(mutfak, list) else str(mutfak or "")
    kategori_metni = f"{varsayilan_kategori_ipucu} {tip_metni} {mutfak_metni}".strip()

    puan_ortalamasi = puan_sayisi = None
    puan_nesnesi = json_ld_yer.get("aggregateRating")
    if isinstance(puan_nesnesi, dict):
        puan_ortalamasi = _sayidan_puan_cikar(puan_nesnesi.get("ratingValue"))
        try:
            puan_sayisi = int(puan_nesnesi.get("reviewCount") or puan_nesnesi.get("ratingCount") or 0) or None
        except (TypeError, ValueError):
            puan_sayisi = None

    return isim, adres, telefon, enlem, boylam, kategori_metni, puan_ortalamasi, puan_sayisi


def _json_ld_ornek_yorumlarini_cikar(json_ld_yer: dict[str, Any], kaynak_yer_id: str) -> list[HamYorum]:
    """Bazi TripAdvisor sayfalari SEO icin JSON-LD icine birkac ORNEK yorum
    gomer ("review" alani). Bu, TAM yorum listesi degildir (genelde 3-5
    adet) ama DOM scraping'e hic gerek kalmadan, %100 guvenilir sekilde
    gelen bonus bir veridir."""
    yorumlar: list[HamYorum] = []
    ham_yorumlar = json_ld_yer.get("review")
    if not ham_yorumlar:
        return yorumlar
    if isinstance(ham_yorumlar, dict):
        ham_yorumlar = [ham_yorumlar]
    for i, ham in enumerate(ham_yorumlar):
        if not isinstance(ham, dict):
            continue
        metin = ham.get("reviewBody") or ham.get("description")
        if not metin:
            continue
        yazar = ham.get("author")
        if isinstance(yazar, dict):
            yazar = yazar.get("name")
        puan = None
        puan_nesnesi = ham.get("reviewRating")
        if isinstance(puan_nesnesi, dict):
            puan = _sayidan_puan_cikar(puan_nesnesi.get("ratingValue"))
        try:
            yorumlar.append(
                HamYorum(
                    kaynak=VeriKaynagi.TRIPADVISOR,
                    kaynak_yer_id=kaynak_yer_id,
                    kaynak_yorum_id=f"{kaynak_yer_id}-jsonld-{i}",
                    yazar_takma_adi=str(yazar) if yazar else None,
                    yorum_metni=str(metin).strip(),
                    kaynakta_puan=puan,
                    yorum_tarihi=None,
                )
            )
        except Exception:
            continue
    return yorumlar


def _dom_yorumlarini_cek_best_effort(sayfa: Page, kaynak_yer_id: str, maks_yorum: int) -> list[HamYorum]:
    """DOM tabanli YEDEK yorum cekme yontemi (JSON-LD'de yorum yoksa/az ise
    devreye girer). CSS sinif adlarina degil, yorum kalici baglantisinin URL
    deseninine ("-r<sayi>-") dayanir -- bu, TripAdvisor tasarim degisikligine
    Google Maps'teki class-tabanli secicilerden daha dayaniklidir, ama YINE DE
    canli olarak dogrulanmamistir (bkz. modul docstring'i). Herhangi bir
    adimda beklenmedik bir yapiyla karsilasirsa sessizce bos liste doner --
    boylece bu yedek yontemin basarisiz olmasi programin geri kalanini
    (JSON-LD'den gelen guvenilir yer verisini) etkilemez.
    """
    yorumlar: list[HamYorum] = []
    try:
        yorum_baglantilari = sayfa.locator('a[href*="Review-g"]')
        toplam = min(yorum_baglantilari.count(), maks_yorum)
    except Exception:
        return yorumlar

    gorulen: set[str] = set()
    for i in range(toplam):
        try:
            baglanti = yorum_baglantilari.nth(i)
            href = baglanti.get_attribute("href") or ""
            if not SECICILER["yorum_kalici_baglanti_deseni"].search(href):
                continue
            if href in gorulen:
                continue
            gorulen.add(href)

            # Yorum metninin kendisi genelde bu baglantinin ait oldugu karta
            # (birkac ust seviye) yakin bir yerdedir. En yakin, yeterince
            # uzun metin iceren atayi ariyoruz.
            kart_metni = baglanti.evaluate(
                """
                (el) => {
                    let ata = el;
                    for (let i = 0; i < 6 && ata; i++) {
                        if (ata.innerText && ata.innerText.trim().length > 80) {
                            return ata.innerText.trim();
                        }
                        ata = ata.parentElement;
                    }
                    return null;
                }
                """
            )
            if not kart_metni:
                continue

            yorumlar.append(
                HamYorum(
                    kaynak=VeriKaynagi.TRIPADVISOR,
                    kaynak_yer_id=kaynak_yer_id,
                    kaynak_yorum_id=href,
                    yazar_takma_adi=None,
                    yorum_metni=kart_metni,
                )
            )
        except Exception:
            continue

    return yorumlar


def _yer_detayini_cek(
    sayfa: Page, url: str, sehir_adi: str, kategori_ipucu: str, maks_yorum: int
) -> tuple[Yer | None, list[HamYorum]]:
    try:
        sayfa.goto(url, timeout=30000)
    except Exception as hata:
        print(f"[UYARI] Sayfa yuklenemedi, atlaniyor: {url} ({hata})")
        return None, []
    rastgele_bekle(2.5, 5.0)

    if _engellenmis_mi(sayfa):
        raise TripAdvisorEngellendiHatasi(url)

    html = sayfa.content()
    json_ld_bloklari = _json_ld_bloklarini_cikar(html)
    json_ld_yer = _json_ld_icinde_yer_bul(json_ld_bloklari)

    if json_ld_yer is None:
        # Yapisal veri yoksa (nadir ama olasi), DOM'dan en azindan ismi almayi dene.
        try:
            isim = sayfa.locator(SECICILER["yer_ismi_basligi"]).first.inner_text(timeout=5000).strip()
        except Exception:
            print(f"[UYARI] '{url}' icin ne JSON-LD ne de DOM'dan isim okunabildi, atlaniyor.")
            return None, []
        print(f"[UYARI] '{isim}' icin schema.org yapisal verisi bulunamadi; adres/konum/puan eksik olabilir.")
        adres = telefon = kategori_metni = None
        enlem = boylam = puan_ortalamasi = None
        puan_sayisi = None
    else:
        isim, adres, telefon, enlem, boylam, kategori_metni, puan_ortalamasi, puan_sayisi = _json_ld_yer_verisini_ayikla(
            json_ld_yer, kategori_ipucu
        )

    if not isim:
        print(f"[UYARI] '{url}' icin isim bulunamadi, atlaniyor.")
        return None, []

    if enlem is None or boylam is None:
        print(f"[UYARI] '{isim}' icin konum (enlem/boylam) bulunamadi, atlaniyor.")
        return None, []

    kategori_sonucu = metinden_kategori_esle(kategori_metni or kategori_ipucu)
    if kategori_sonucu is None:
        print(f"[UYARI] '{isim}' icin kategori eslenemedi ('{kategori_metni}'), atlaniyor.")
        return None, []
    ana_kategori, alt_kategori = kategori_sonucu

    kaynak_id_eslesme = re.search(r"-(d\d+)-", url)
    kaynak_id = kaynak_id_eslesme.group(1) if kaynak_id_eslesme else url

    try:
        yer = Yer(
            kaynak=VeriKaynagi.TRIPADVISOR,
            kaynak_id=kaynak_id,
            kaynak_url=url,
            isim=isim,
            ana_kategori=ana_kategori,
            alt_kategori=alt_kategori,
            sehir=sehir_adi,
            adres=adres,
            telefon=telefon,
            enlem=enlem,
            boylam=boylam,
            kaynakta_puan_ortalamasi=puan_ortalamasi,
            kaynakta_puan_sayisi=puan_sayisi,
        )
    except ValidationError as hata:
        print(f"[UYARI] '{isim}' dogrulanamadi, atlaniyor: {hata}")
        return None, []

    yorumlar = _json_ld_ornek_yorumlarini_cikar(json_ld_yer, kaynak_id) if json_ld_yer else []
    if len(yorumlar) < maks_yorum:
        yorumlar.extend(_dom_yorumlarini_cek_best_effort(sayfa, kaynak_id, maks_yorum - len(yorumlar)))

    return yer, yorumlar


class TripAdvisorEngellendiHatasi(Exception):
    """TripAdvisor'in bot-korumasi devreye girdiginde firlatilir. Bu
    yakalandiginda calisma NAZIKCE durdurulur -- ayni oturumda tekrar tekrar
    denemek IP itibarini daha da kotulestirebilir ve zaman kaybettirir."""

    def __init__(self, url: str) -> None:
        super().__init__(
            f"TripAdvisor bu oturumdan gelen istekleri engelliyor (URL: {url}). "
            "Bu, IP itibariyla ilgili bir korumadir, kodun hatasi degildir. "
            "Oneri: daha az sikli/daha az hacimli tekrar dene, farkli bir agdan "
            "(orn. Oracle sunucunun kendi IP'si) dene, ya da bu calistirmayi atlayip "
            "Google Maps + Eksi Sozluk kaynaklarina guven."
        )
        self.url = url


def _liste_sayfasindan_detay_linklerini_topla(
    sayfa: Page, liste_url: str, detay_oneki: str, maks_sonuc: int
) -> list[str]:
    try:
        sayfa.goto(liste_url, timeout=30000)
    except Exception as hata:
        print(f"[UYARI] Listeleme sayfasi yuklenemedi: {liste_url} ({hata})")
        return []
    rastgele_bekle(2.5, 5.0)
    _cerezleri_kabul_et(sayfa)

    if _engellenmis_mi(sayfa):
        raise TripAdvisorEngellendiHatasi(liste_url)

    # Href'i detay_oneki ile baslayan (orn. "/Attraction_Review-") TUM linkleri
    # topluyoruz -- bu, TripAdvisor'in kart konteynerlerine verdigi (sik
    # degisen) class isimlerine bagli olmayan, yapisal olarak kararli bir yontem.
    baglanti_secici = f'a[href^="{detay_oneki}"]'
    onceki_sayisi = 0
    for _ in range(10):
        sayi = sayfa.locator(baglanti_secici).count()
        if sayi >= maks_sonuc or sayi == onceki_sayisi:
            break
        onceki_sayisi = sayi
        sayfa.mouse.wheel(0, 2000)
        rastgele_bekle(1.0, 2.5)

    hrefler: list[str] = []
    gorulen: set[str] = set()
    baglantilar = sayfa.locator(baglanti_secici)
    for i in range(baglantilar.count()):
        href = baglantilar.nth(i).get_attribute("href")
        if not href:
            continue
        tam_url = href if href.startswith("http") else f"{TABAN_ADRES}{href}"
        if tam_url in gorulen:
            continue
        gorulen.add(tam_url)
        hrefler.append(tam_url)
        if len(hrefler) >= maks_sonuc:
            break

    return hrefler


def calistir(
    sehir_anahtari: str,
    kategoriler: list[str] | None = None,
    maks_sonuc_kategori_basi: int = 20,
    maks_yorum_yer_basi: int = 10,
    headless: bool = True,
    devam_et_dosyasi: str | Path | None = None,
) -> None:
    sehir = sehir_getir(sehir_anahtari)
    lokasyon_id, slug = _lokasyon_id_ve_slug(sehir)
    kategoriler = kategoriler or list(KATEGORILER.keys())

    kok = Path(__file__).resolve().parents[1] / "cikti" / "ham" / "tripadvisor"
    if devam_et_dosyasi is not None:
        yerler_dosyasi = Path(devam_et_dosyasi)
        yorumlar_dosyasi = Path(str(yerler_dosyasi).replace("_yerler_", "_yorumlar_"))
        print(f"[BILGI] Onceki calistirmaya devam ediliyor: {yerler_dosyasi}")
    else:
        tarih = bugunun_tarihi_dosya_adi()
        yerler_dosyasi = kok / f"{sehir.anahtar}_yerler_{tarih}.jsonl"
        yorumlar_dosyasi = kok / f"{sehir.anahtar}_yorumlar_{tarih}.jsonl"

    toplam_yer = toplam_yorum = 0
    islenen_kaynak_idler: set[str] = mevcut_kaynak_idlerini_yukle(yerler_dosyasi)
    if islenen_kaynak_idler:
        print(f"[BILGI] {len(islenen_kaynak_idler)} yer daha once islenmis bulundu, bunlar atlanacak.")

    with sync_playwright() as p:
        tarayici = p.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        baglam = tarayici.new_context(
            user_agent=kullanici_ajani_sec(),
            locale="tr-TR",
            viewport={"width": 1366, "height": 900},
        )
        # navigator.webdriver bayragi otomasyon tespitinde kullanilan en temel
        # isaretlerden biri; gizlemek engellenme ihtimalini biraz azaltabilir
        # (ama TripAdvisor'in korumasi bundan ibaret degil, bkz. modul docstring'i).
        baglam.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        sayfa = baglam.new_page()

        try:
            for kategori_anahtari in kategoriler:
                if kategori_anahtari not in KATEGORILER:
                    print(f"[UYARI] Bilinmeyen kategori '{kategori_anahtari}', atlaniyor.")
                    continue
                kategori_ayari = KATEGORILER[kategori_anahtari]
                liste_url = TABAN_ADRES + kategori_ayari["liste_sablonu"].format(lokasyon_id=lokasyon_id, slug=slug)
                print(f"[BILGI] '{kategori_anahtari}' listeleniyor: {liste_url}")

                hrefler = _liste_sayfasindan_detay_linklerini_topla(
                    sayfa, liste_url, kategori_ayari["detay_oneki"], maks_sonuc_kategori_basi
                )
                print(f"[BILGI]   {len(hrefler)} sonuc bulundu.")

                for sira, href in enumerate(hrefler, start=1):
                    rastgele_bekle()
                    try:
                        yer, yorumlar = _yer_detayini_cek(
                            sayfa, href, sehir.isim, kategori_anahtari.replace("_", " "), maks_yorum_yer_basi
                        )
                    except TripAdvisorEngellendiHatasi:
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
        except TripAdvisorEngellendiHatasi as hata:
            print(f"[HATA] {hata}")
            print(
                f"[BILGI] Engellenmeden once {toplam_yer} yer, {toplam_yorum} yorum kaydedilmisti "
                "(bu veriler dosyada guvende, kayip yok)."
            )
        finally:
            tarayici.close()

    print(f"[BILGI] Tamamlandi. Toplam {toplam_yer} yer, {toplam_yorum} yorum kaydedildi.")
    print(f"[BILGI] Yerler: {yerler_dosyasi}")
    print(f"[BILGI] Yorumlar: {yorumlar_dosyasi}")


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(description="TripAdvisor'dan bir sehrin yer ve yorum verisini topla.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    ayristirici.add_argument(
        "--kategoriler",
        nargs="+",
        choices=list(KATEGORILER.keys()),
        default=None,
        help="Taranacak kategoriler (varsayilan: hepsi)",
    )
    ayristirici.add_argument("--maks-sonuc", type=int, default=20, help="Kategori basina maksimum sonuc sayisi")
    ayristirici.add_argument("--maks-yorum", type=int, default=10, help="Yer basina maksimum yorum sayisi")
    ayristirici.add_argument(
        "--headed", action="store_true", help="Tarayiciyi gorunur modda ac (yerel hata ayiklama icin)"
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
        kategoriler=argumanlar.kategoriler,
        maks_sonuc_kategori_basi=argumanlar.maks_sonuc,
        maks_yorum_yer_basi=argumanlar.maks_yorum,
        headless=not argumanlar.headed,
        devam_et_dosyasi=argumanlar.devam_et,
    )


if __name__ == "__main__":
    _ana()
