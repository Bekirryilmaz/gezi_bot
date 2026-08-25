"""
Bir gunun kac durak kaldirabilecegini hesaplayan zaman butcesi mantigi.

Varsayimlar (baslangic degerleri -- README'de de belirtildigi gibi, gercek
kullanici geri bildirimiyle zamanla ayarlanmasi beklenir):
- Bir gunde gezi icin ayrilan toplam sure: `GUNLUK_GEZI_DAKIKASI`
- Sehir ici ortalama ulasim hizi (yuruyus+arac karisik, kisa mesafeler
  icin kaba bir varsayim): `ORTALAMA_SEHIR_ICI_HIZ_KMH`
- Bir yerin `ozellikler.ortalama_ziyaret_suresi_dk`'si bilinmiyorsa, alt
  kategoriye gore bir varsayilan sure kullanilir.
"""

from __future__ import annotations

from ortak.cografya_araclari import haversine_metre
from ortak.sabitler import bekleme_payi_dk
from sunucu.rota_motoru.veri_tipleri import AdayYer

GUNLUK_GEZI_DAKIKASI = 8 * 60  # 09:00 - 17:00 gibi bir gezi gunu varsayimi
ORTALAMA_SEHIR_ICI_HIZ_KMH = 30.0

# Alt kategoriye gore varsayilan ziyaret suresi (dakika). Yer'in kendi
# `ozellikler.ortalama_ziyaret_suresi_dk`'si varsa ona oncelik verilir.
_VARSAYILAN_ZIYARET_SURESI_DK: dict[str, int] = {
    "tarihi_kulturel": 60,
    "doga_manzara": 45,
    "plaj_su": 90,
    "eglence_aktivite": 90,
    "gece_hayati": 90,
    "alisveris": 45,
    "spor_doga_yuruyus": 90,
    "dini_manevi": 30,
    "fotograf_noktasi": 20,
    "restoran_lokanta": 60,
    "deniz_mahsulleri": 60,
    "kebap_izgara": 60,
    "ev_yemekleri_esnaf": 60,
    "fine_dining_romantik": 90,
    "sokak_lezzeti": 20,
    "kafe": 45,
    "tatli_pastane": 30,
    "kahve_uzmanlik": 45,
    "meyhane_bar": 90,
    "cay_bahcesi": 45,
}
_VARSAYILAN_ZIYARET_SURESI_GENEL_DK = 45


def ziyaret_suresi_tahmini_dk(yer: AdayYer) -> int:
    if yer.ortalama_ziyaret_suresi_dk:
        return yer.ortalama_ziyaret_suresi_dk
    return _VARSAYILAN_ZIYARET_SURESI_DK.get(yer.alt_kategori, _VARSAYILAN_ZIYARET_SURESI_GENEL_DK)


def ulasim_suresi_tahmini_dk(baslangic: tuple[float, float], bitis: tuple[float, float]) -> int:
    mesafe_km = haversine_metre(baslangic[0], baslangic[1], bitis[0], bitis[1]) / 1000
    saat = mesafe_km / ORTALAMA_SEHIR_ICI_HIZ_KMH
    return round(saat * 60)


def gun_butcesine_sigar_mi(
    mevcut_dakika: int,
    eklenecek_yer: AdayYer,
    onceki_nokta: tuple[float, float],
) -> tuple[bool, int]:
    """`onceki_nokta`dan `eklenecek_yer`e gidip orada vakit gecirmenin
    toplam dakikasini hesaplar, gunluk butceye sigip sigmadigini dondurur.

    NOT: bu, kaba bir on-elemedir (skor sirasina gore eklenirken kullanilir);
    nihai, cografi olarak optimize edilmis sira `siralama.py` tarafindan
    belirlenir -- o yuzden buradaki tahmin gercek rota mesafesinden biraz
    farkli olabilir, bu kabul edilebilir bir yaklastirma."""
    ulasim = ulasim_suresi_tahmini_dk(onceki_nokta, (eklenecek_yer.enlem, eklenecek_yer.boylam))
    ziyaret = ziyaret_suresi_tahmini_dk(eklenecek_yer)
    tampon = bekleme_payi_dk(eklenecek_yer.ana_kategori)
    yeni_toplam = mevcut_dakika + ulasim + ziyaret + tampon
    return yeni_toplam <= GUNLUK_GEZI_DAKIKASI, yeni_toplam
