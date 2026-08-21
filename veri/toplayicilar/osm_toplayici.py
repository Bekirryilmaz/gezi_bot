"""
OpenStreetMap (Overpass API) toplayicisi.

Bu, veri katmaninin "iskelet" (seed) verisini saglayan ilk ve en ucuz
kaynaktir: resmi, ucretsiz, ticari kullanima uygun (ODbL lisansli) bir
API'dir, bu yuzden insan-taklidi gecikmeye ihtiyaci yoktur.

Ne yapar:
1. Secilen sehrin il sinirini (OSM ISO3166-2 koduyla) bulur.
2. O sinir icinde, dokumanlar/kategori_taksonomisi.md'deki kategorilere
   karsilik gelen OSM etiketlerine sahip tum yerleri tek bir sorguda ceker.
3. Her OSM etiketini (tourism=museum, amenity=cafe, natural=beach, vb.)
   kendi ana_kategori/alt_kategori sistemimize esler.
4. Sonuclari ortak `Yer` modeline donusturup JSONL olarak diske yazar.

Calistirma (repo kokunden):
    python -m veri.toplayicilar.osm_toplayici --sehir samsun
"""

from __future__ import annotations

import argparse
from pathlib import Path

import requests

from ortak.sabitler import (
    Aktivite,
    AnaKategori,
    GezilecekYerAltKategori,
    KonaklamaAltKategori,
    VeriKaynagi,
    YemeIcmeAltKategori,
)
from pydantic import ValidationError

from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_yaz
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir, turkce_kucuk_harf
from veri.ortak.sehir_ayarlari import SehirAyari, sehir_getir
from veri.ortak.yer_modeli import OzellikSeti, Yer

OVERPASS_ADRESI = "https://overpass-api.de/api/interpreter"
ISTEK_ZAMAN_ASIMI_SANIYE = 200

# Overpass API, taniyamadigi/bos User-Agent gonderen isteklere 406 Not
# Acceptable ile donebiliyor. Kim oldugumuzu belirten bir User-Agent gondermek
# hem bu sorunu cozer hem de iyi bir API kullanim pratigidir.
_ISTEK_BASLIKLARI = {"User-Agent": "SamsunGeziBotu/0.1 (veri toplama asamasi, ticari olmayan gelistirme)"}

# ---------------------------------------------------------------------------
# OSM etiketi -> bizim kategori sistemimiz eslemesi.
#
# Liste sirali: bir eleman birden fazla kurala uyuyorsa ILK eslesen kural
# kullanilir. Bu yuzden daha spesifik kurallar (orn. "historic") daha genel
# olanlardan once gelir.
#
# Her satir: (osm_anahtari, osm_degeri veya None (anahtarin herhangi bir
# degeri de eslesir), ana_kategori, alt_kategori, varsayilan aktiviteler)
# ---------------------------------------------------------------------------
_ETIKET_KURALLARI: list[tuple[str, str | None, AnaKategori, str, list[Aktivite]]] = [
    ("historic", None, AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.TARIHI_KULTUREL.value, []),
    ("tourism", "museum", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.TARIHI_KULTUREL.value, []),
    ("tourism", "gallery", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.TARIHI_KULTUREL.value, []),
    ("tourism", "artwork", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.FOTOGRAF_NOKTASI.value, [Aktivite.FOTOGRAFCILIK]),
    ("tourism", "viewpoint", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.FOTOGRAF_NOKTASI.value, [Aktivite.FOTOGRAFCILIK]),
    ("tourism", "theme_park", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.EGLENCE_AKTIVITE.value, []),
    ("tourism", "zoo", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.EGLENCE_AKTIVITE.value, []),
    ("tourism", "aquarium", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.EGLENCE_AKTIVITE.value, []),
    ("tourism", "camp_site", AnaKategori.KONAKLAMA, KonaklamaAltKategori.KAMP_KARAVAN.value, [Aktivite.KAMP]),
    ("tourism", "caravan_site", AnaKategori.KONAKLAMA, KonaklamaAltKategori.KAMP_KARAVAN.value, [Aktivite.KAMP]),
    ("tourism", "hotel", AnaKategori.KONAKLAMA, KonaklamaAltKategori.OTEL.value, []),
    ("tourism", "motel", AnaKategori.KONAKLAMA, KonaklamaAltKategori.OTEL.value, []),
    ("tourism", "hostel", AnaKategori.KONAKLAMA, KonaklamaAltKategori.HOSTEL.value, []),
    ("tourism", "guest_house", AnaKategori.KONAKLAMA, KonaklamaAltKategori.PANSIYON_APART.value, []),
    ("tourism", "apartment", AnaKategori.KONAKLAMA, KonaklamaAltKategori.EV_KIRALAMA.value, []),
    ("tourism", "attraction", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.FOTOGRAF_NOKTASI.value, []),
    ("natural", "beach", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.PLAJ_SU.value, [Aktivite.YUZME]),
    ("leisure", "beach_resort", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.PLAJ_SU.value, [Aktivite.YUZME]),
    ("natural", "waterfall", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.DOGA_MANZARA.value, [Aktivite.FOTOGRAFCILIK]),
    ("natural", "peak", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.DOGA_MANZARA.value, [Aktivite.YURUYUS_TREKKING, Aktivite.FOTOGRAFCILIK]),
    ("natural", "cave_entrance", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.DOGA_MANZARA.value, []),
    ("leisure", "park", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.DOGA_MANZARA.value, [Aktivite.YURUYUS_TREKKING]),
    ("leisure", "garden", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.DOGA_MANZARA.value, []),
    ("leisure", "nature_reserve", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.DOGA_MANZARA.value, [Aktivite.YURUYUS_TREKKING, Aktivite.KUS_GOZLEMCILIGI]),
    ("leisure", "water_park", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.EGLENCE_AKTIVITE.value, [Aktivite.YUZME]),
    ("leisure", "amusement_arcade", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.EGLENCE_AKTIVITE.value, []),
    ("leisure", "miniature_golf", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.EGLENCE_AKTIVITE.value, []),
    ("leisure", "bowling_alley", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.EGLENCE_AKTIVITE.value, []),
    ("sport", "climbing", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.SPOR_DOGA_YURUYUS.value, [Aktivite.YURUYUS_TREKKING]),
    ("sport", "equestrian", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.EGLENCE_AKTIVITE.value, [Aktivite.AT_BINME]),
    ("amenity", "nightclub", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.GECE_HAYATI.value, []),
    ("amenity", "casino", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.EGLENCE_AKTIVITE.value, []),
    ("amenity", "place_of_worship", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.DINI_MANEVI.value, []),
    ("amenity", "marketplace", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.ALISVERIS.value, []),
    ("shop", "mall", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.ALISVERIS.value, []),
    ("shop", "gift", AnaKategori.GEZILECEK_YER, GezilecekYerAltKategori.ALISVERIS.value, []),
    ("amenity", "cafe", AnaKategori.YEME_ICME, YemeIcmeAltKategori.KAFE.value, []),
    ("amenity", "ice_cream", AnaKategori.YEME_ICME, YemeIcmeAltKategori.TATLI_PASTANE.value, []),
    ("shop", "pastry", AnaKategori.YEME_ICME, YemeIcmeAltKategori.TATLI_PASTANE.value, []),
    ("shop", "confectionery", AnaKategori.YEME_ICME, YemeIcmeAltKategori.TATLI_PASTANE.value, []),
    ("amenity", "fast_food", AnaKategori.YEME_ICME, YemeIcmeAltKategori.SOKAK_LEZZETI.value, []),
    ("amenity", "pub", AnaKategori.YEME_ICME, YemeIcmeAltKategori.MEYHANE_BAR.value, []),
    ("amenity", "bar", AnaKategori.YEME_ICME, YemeIcmeAltKategori.MEYHANE_BAR.value, []),
    ("amenity", "biergarten", AnaKategori.YEME_ICME, YemeIcmeAltKategori.MEYHANE_BAR.value, []),
    ("amenity", "restaurant", AnaKategori.YEME_ICME, YemeIcmeAltKategori.RESTORAN_LOKANTA.value, []),
]

# Restoran/lokantalarda "cuisine" etiketine gore daha ozel bir alt kategoriye
# tasima. Anahtar: cuisine degerinde gecen alt metin, deger: yeni alt kategori.
_MUTFAK_TABANLI_INCELIK: dict[str, str] = {
    "fish": YemeIcmeAltKategori.DENIZ_MAHSULLERI.value,
    "seafood": YemeIcmeAltKategori.DENIZ_MAHSULLERI.value,
    "kebab": YemeIcmeAltKategori.KEBAP_IZGARA.value,
    "turkish": YemeIcmeAltKategori.KEBAP_IZGARA.value,
    "steak_house": YemeIcmeAltKategori.KEBAP_IZGARA.value,
    "regional": YemeIcmeAltKategori.EV_YEMEKLERI_ESNAF.value,
    "home_cooking": YemeIcmeAltKategori.EV_YEMEKLERI_ESNAF.value,
}

# Mekanlarda alkol servisi oldugunu varsayimsal olarak isaretledigimiz alt kategoriler.
_ALKOLLU_VARSAYILAN_ALT_KATEGORILER = {
    YemeIcmeAltKategori.MEYHANE_BAR.value,
    GezilecekYerAltKategori.GECE_HAYATI.value,
}


def _overpass_sorgusu_olustur(iso_kod: str) -> str:
    satirlar = []
    for anahtar, deger, *_geri_kalan in _ETIKET_KURALLARI:
        if deger is None:
            satirlar.append(f'  nwr["{anahtar}"](area.calisma_alani);')
        else:
            satirlar.append(f'  nwr["{anahtar}"="{deger}"](area.calisma_alani);')
    govde = "\n".join(satirlar)
    return (
        f'[out:json][timeout:{ISTEK_ZAMAN_ASIMI_SANIYE - 20}];\n'
        f'area["ISO3166-2"="{iso_kod}"]->.calisma_alani;\n'
        f"(\n{govde}\n);\n"
        f"out center tags;"
    )


def _elementten_kategori_bul(etiketler: dict) -> tuple[AnaKategori, str, list[Aktivite]] | None:
    for anahtar, deger, ana_kategori, alt_kategori, aktiviteler in _ETIKET_KURALLARI:
        if anahtar not in etiketler:
            continue
        if deger is not None and etiketler[anahtar] != deger:
            continue
        return ana_kategori, alt_kategori, list(aktiviteler)
    return None


def _restoran_incelt(alt_kategori: str, etiketler: dict) -> str:
    if alt_kategori != YemeIcmeAltKategori.RESTORAN_LOKANTA.value:
        return alt_kategori
    mutfak = turkce_kucuk_harf(etiketler.get("cuisine", ""))
    for anahtar_metin, yeni_alt_kategori in _MUTFAK_TABANLI_INCELIK.items():
        if anahtar_metin in mutfak:
            return yeni_alt_kategori
    return alt_kategori


def _evet_hayir_donustur(deger: str | None) -> bool | None:
    if deger == "yes":
        return True
    if deger == "no":
        return False
    return None


def _ozellikleri_cikar(etiketler: dict, alt_kategori: str) -> OzellikSeti:
    # OSM'de fee=yes -> ucret var (bizim icin ucretsiz=False), fee=no -> ucretsiz=True
    fee_degeri = etiketler.get("fee")
    ucretsiz = {"yes": False, "no": True}.get(fee_degeri)

    wifi = None
    erisim = etiketler.get("internet_access")
    if erisim in ("wlan", "yes"):
        wifi = True
    elif erisim == "no":
        wifi = False

    alkol_servisi = True if alt_kategori in _ALKOLLU_VARSAYILAN_ALT_KATEGORILER else None

    return OzellikSeti(
        ucretsiz=ucretsiz,
        wifi=wifi,
        engelli_erisimi=_evet_hayir_donustur(etiketler.get("wheelchair")),
        alkol_servisi=alkol_servisi,
        aile_cocuk_dostu=_evet_hayir_donustur(etiketler.get("kids_area") or etiketler.get("family_friendly")),
    )


def _adresi_olustur(etiketler: dict) -> str | None:
    parcalar = []
    if etiketler.get("addr:street"):
        sokak = etiketler["addr:street"]
        if etiketler.get("addr:housenumber"):
            sokak += f" {etiketler['addr:housenumber']}"
        parcalar.append(sokak)
    if etiketler.get("addr:suburb"):
        parcalar.append(etiketler["addr:suburb"])
    return ", ".join(parcalar) if parcalar else None


def _elementi_yere_donustur(element: dict, sehir_adi: str) -> Yer | None:
    etiketler = element.get("tags", {})
    isim = etiketler.get("name")
    if not isim:
        return None  # Ismi olmayan yerleri sitede gosteremeyiz, atlanir.

    kategori_sonucu = _elementten_kategori_bul(etiketler)
    if kategori_sonucu is None:
        return None
    ana_kategori, alt_kategori, aktiviteler = kategori_sonucu
    alt_kategori = _restoran_incelt(alt_kategori, etiketler)

    if element["type"] == "node":
        enlem, boylam = element.get("lat"), element.get("lon")
    else:
        merkez = element.get("center", {})
        enlem, boylam = merkez.get("lat"), merkez.get("lon")
    if enlem is None or boylam is None:
        return None

    try:
        return Yer(
            kaynak=VeriKaynagi.OPENSTREETMAP,
            kaynak_id=f"{element['type']}/{element['id']}",
            kaynak_url=f"https://www.openstreetmap.org/{element['type']}/{element['id']}",
            isim=isim,
            ana_kategori=ana_kategori,
            alt_kategori=alt_kategori,
            sehir=sehir_adi,
            ilce=etiketler.get("addr:district") or etiketler.get("addr:suburb"),
            adres=_adresi_olustur(etiketler),
            aciklama=etiketler.get("description"),
            telefon=etiketler.get("phone") or etiketler.get("contact:phone"),
            web_sitesi=etiketler.get("website") or etiketler.get("contact:website"),
            enlem=float(enlem),
            boylam=float(boylam),
            ozellikler=_ozellikleri_cikar(etiketler, alt_kategori),
            aktiviteler=aktiviteler,
        )
    except ValidationError as hata:
        print(f"[UYARI] '{isim}' dogrulanamadi, atlaniyor: {hata}")
        return None


def calistir(sehir_anahtari: str, cikti_dosyasi: Path | None = None) -> list[Yer]:
    sehir: SehirAyari = sehir_getir(sehir_anahtari)
    print(f"[BILGI] {sehir.isim} icin Overpass API sorgusu hazirlaniyor...")
    sorgu = _overpass_sorgusu_olustur(sehir.osm_iso_kodu)

    yanit = requests.post(
        OVERPASS_ADRESI, data={"data": sorgu}, headers=_ISTEK_BASLIKLARI, timeout=ISTEK_ZAMAN_ASIMI_SANIYE
    )
    yanit.raise_for_status()
    veri = yanit.json()
    elementler = veri.get("elements", [])
    print(f"[BILGI] Overpass API {len(elementler)} ham eleman dondurdu, isleniyor...")

    yerler: list[Yer] = []
    atlanan_sayisi = 0
    for element in elementler:
        yer = _elementi_yere_donustur(element, sehir.isim)
        if yer is None:
            atlanan_sayisi += 1
            continue
        yerler.append(yer)

    print(f"[BILGI] {len(yerler)} yer basariyla donusturuldu, {atlanan_sayisi} eleman atlandi (isim/kategori/konum eksik).")

    kategori_sayaci: dict[str, int] = {}
    for yer in yerler:
        kategori_sayaci[yer.alt_kategori] = kategori_sayaci.get(yer.alt_kategori, 0) + 1
    print("[BILGI] Alt kategori dagilimi:")
    for alt_kategori, adet in sorted(kategori_sayaci.items(), key=lambda x: -x[1]):
        print(f"         {alt_kategori}: {adet}")

    if cikti_dosyasi is None:
        cikti_dosyasi = (
            Path(__file__).resolve().parents[1]
            / "cikti" / "ham" / "osm" / f"{sehir.anahtar}_{bugunun_tarihi_dosya_adi()}.jsonl"
        )
    jsonl_yaz(cikti_dosyasi, yerler)
    print(f"[BILGI] Sonuclar yazildi: {cikti_dosyasi}")
    return yerler


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(description="OpenStreetMap Overpass API ile bir sehrin yer verisini cek.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    argumanlar = ayristirici.parse_args()
    calistir(argumanlar.sehir)


if __name__ == "__main__":
    _ana()
