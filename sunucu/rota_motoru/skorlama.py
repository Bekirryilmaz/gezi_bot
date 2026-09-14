"""
Yer uygunluk puanlamasi.

Bir yerin kullanicinin tercihleriyle NE KADAR uyumlu oldugunu bir puanla
ifade eder. Puan, ayri bilesenlerin toplamidir ve HER ZAMAN bir kirilim
(breakdown) ile doner -- "bu puan neden bu cikti" sorusu her zaman
izlenebilir olsun diye (projenin genel seffaflik ilkesiyle tutarli, bkz.
veri/duygu_analizi/yer_profili_cikarici.py'deki `ornek_ifadeler` mantigi).

Baslangic agirliklari (asagidaki sabitler) ilk tahminlerdir, gercek
kullanici geri bildirimiyle zamanla ayarlanmasi beklenir (projedeki diger
esikler gibi, bkz. yer_profili_cikarici.py ust notu).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ortak.sabitler import OzelEtiket
from sunucu.rota_motoru.veri_tipleri import AdayYer, RotaTercihleri
from sunucu.rota_motoru.zaman_butcesi import ziyaret_suresi_tahmini_dk

_AKTIVITE_ESLESME_BONUSU = 15.0
_ZORUNLU_DURAK_PUANI = 1_000.0  # skor siralamasinda her zaman en uste cikmasi icin
_FIYAT_TERCIH_BONUSU = 10.0
_FIYAT_TERCIH_CEZASI = -10.0
_SAKINLIK_CEZA_CARPANI = 15.0  # kalabalik zaman dilimi basina, ayrica asagida guvenle carpilir
_KAYNAK_PUANI_AGIRLIGI = 2.0  # 0-5 arasi kaynak puanini kucuk bir katki olarak dahil eder (esit skorlarda ayirt edici)
_SEHRIN_KLASIGI_BONUSU = 15.0
_YOL_YORGUNLUGU_ESIGI = 1.5
_YOL_YORGUNLUGU_CARPANI = 0.5


@dataclass
class SkorSonucu:
    toplam_puan: float
    kirilim: dict[str, float] = field(default_factory=dict)
    zorunlu_mu: bool = False


def yer_uygunluk_puani(
    yer: AdayYer,
    tercihler: RotaTercihleri,
    yol_suresi_dk: float | None = None,
) -> SkorSonucu:
    if yer.id in tercihler.zorunlu_duraklar:
        return SkorSonucu(
            toplam_puan=_ZORUNLU_DURAK_PUANI,
            kirilim={"zorunlu_durak": _ZORUNLU_DURAK_PUANI},
            zorunlu_mu=True,
        )

    kirilim: dict[str, float] = {}

    deneyim_puani = _deneyim_ekseni_puani_hesapla(yer, tercihler, kirilim)
    aktivite_bonusu = _aktivite_bonusu_hesapla(yer, tercihler, kirilim)
    fiyat_katkisi = _fiyat_tercihi_katkisi_hesapla(yer, tercihler, kirilim)
    sakinlik_katkisi = _sakinlik_tercihi_katkisi_hesapla(yer, tercihler, kirilim)
    kalite_katkisi = _kaynak_kalitesi_katkisi_hesapla(yer, kirilim)
    kuratorluk_katkisi = _kuratorluk_bonusu_hesapla(yer, kirilim)

    toplam = deneyim_puani + aktivite_bonusu + fiyat_katkisi + sakinlik_katkisi + kalite_katkisi + kuratorluk_katkisi
    toplam = _yol_yorgunlugu_uygula(yer, yol_suresi_dk, toplam, kirilim)
    return SkorSonucu(toplam_puan=round(toplam, 2), kirilim=kirilim)


def _kuratorluk_bonusu_hesapla(yer: AdayYer, kirilim: dict[str, float]) -> float:
    """Yalniz organik kuratorluk sinyalleri; ticari metadata karara girmez."""
    katki = 0.0
    if yer.ozellik_isaretli(OzelEtiket.SEHRIN_KLASIGI.value):
        kirilim["sehrin_klasigi_bonusu"] = _SEHRIN_KLASIGI_BONUSU
        katki += _SEHRIN_KLASIGI_BONUSU
    return katki


def _yol_yorgunlugu_uygula(
    yer: AdayYer,
    yol_suresi_dk: float | None,
    toplam: float,
    kirilim: dict[str, float],
) -> float:
    """ROI: yolda gecen sure ziyaret suresinin 1.5 katini asarsa skoru yarila."""
    if yol_suresi_dk is None:
        return toplam
    ziyaret = ziyaret_suresi_tahmini_dk(yer) or 0
    if ziyaret <= 0:
        return toplam
    if (yol_suresi_dk / ziyaret) <= _YOL_YORGUNLUGU_ESIGI:
        return toplam
    onceki = toplam
    toplam = toplam * _YOL_YORGUNLUGU_CARPANI
    kirilim["yol_yorgunlugu_cezasi"] = round(toplam - onceki, 2)
    return toplam


def _deneyim_ekseni_puani_hesapla(yer: AdayYer, tercihler: RotaTercihleri, kirilim: dict[str, float]) -> float:
    """dokumanlar/kategori_taksonomisi.md #4 -- kullanicinin 'ne kadar
    tarihi, ne kadar eglence' gibi ilgi agirliklarini yerin deneyim
    puanlariyla carpip agirlikli ortalamasini alir."""
    if not tercihler.ilgi_agirliklari:
        return 0.0

    toplam_agirlik = sum(tercihler.ilgi_agirliklari.values()) or 1.0
    toplam_katki = 0.0
    for eksen, agirlik in tercihler.ilgi_agirliklari.items():
        eksen_puani = yer.deneyim_puanlari.get(eksen, 0)
        katki = (agirlik / toplam_agirlik) * eksen_puani
        if katki:
            kirilim[f"deneyim:{eksen}"] = round(katki, 2)
        toplam_katki += katki
    return toplam_katki


def _aktivite_bonusu_hesapla(yer: AdayYer, tercihler: RotaTercihleri, kirilim: dict[str, float]) -> float:
    if not tercihler.aktiviteler:
        return 0.0
    ortak = set(yer.aktiviteler) & set(tercihler.aktiviteler)
    if not ortak:
        return 0.0
    kirilim["aktivite_eslesmesi"] = _AKTIVITE_ESLESME_BONUSU
    return _AKTIVITE_ESLESME_BONUSU


def _fiyat_tercihi_katkisi_hesapla(yer: AdayYer, tercihler: RotaTercihleri, kirilim: dict[str, float]) -> float:
    """dokumanlar/kategori_taksonomisi.md #6 -- ziyaretci ALGISINA gore
    fiyat (yer_profili.fiyat_algisi), objektif fiyat_seviyesi'nden farkli.
    `guven` dusukse (az yorumdan turemisse) katki da kucuk kalir."""
    if not tercihler.ucuz_tercih_et:
        return 0.0

    fiyat_algisi = yer.yer_profili.get("fiyat_algisi") or {}
    deger = fiyat_algisi.get("deger")
    guven = fiyat_algisi.get("guven", 0.0)

    katki = 0.0
    if deger == "ucuz":
        katki = _FIYAT_TERCIH_BONUSU * guven
    elif deger == "pahali":
        katki = _FIYAT_TERCIH_CEZASI * guven

    if katki:
        kirilim["fiyat_tercihi"] = round(katki, 2)
    return katki


def _sakinlik_tercihi_katkisi_hesapla(yer: AdayYer, tercihler: RotaTercihleri, kirilim: dict[str, float]) -> float:
    """dokumanlar/kategori_taksonomisi.md #6 -- yer_profili.kalabalik_zamanlar'da
    'kalabalik' olarak isaretlenen zaman dilimi sayisi kadar kucuk bir ceza
    uygular (hangi zaman dilimi oldugu rota algoritmasinda henuz ayirt
    edilmiyor -- kullanicinin hangi gun/saatte gezecegi bilinmiyor, bu
    yuzden genel bir 'kalabalik olma egilimi' cezasi olarak ele alinir)."""
    if not tercihler.sakin_tercih_et:
        return 0.0

    kalabalik_zamanlar = yer.yer_profili.get("kalabalik_zamanlar") or {}
    kalabalik_sayisi = sum(1 for deger in kalabalik_zamanlar.values() if deger == "kalabalik")
    if not kalabalik_sayisi:
        return 0.0

    katki = -_SAKINLIK_CEZA_CARPANI * kalabalik_sayisi
    kirilim["sakinlik_tercihi"] = round(katki, 2)
    return katki


def _kaynak_kalitesi_katkisi_hesapla(yer: AdayYer, kirilim: dict[str, float]) -> float:
    """Esit/yakin skorlu yerler arasinda ayirt edici olmasi icin kaynak
    puanindan (Google/OSM/TripAdvisor ortalamasi) kucuk bir katki eklenir."""
    if not yer.kaynakta_puan_ortalamasi:
        return 0.0
    katki = yer.kaynakta_puan_ortalamasi * _KAYNAK_PUANI_AGIRLIGI
    kirilim["kaynak_kalitesi"] = round(katki, 2)
    return katki
