"""
API istek/cevap semalari (Pydantic).

`sunucu/veritabani/modeller.py`'deki SQLAlchemy modellerinden BILEREK ayri
tutulur: veritabani semasi (nasil saklandigi) ile API semasi (disariya nasil
gosterildigi/hangi alanlarin istendigi) farkli kaygilardir -- birini
degistirmek digerini kirmasin diye ayrilir.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ortak.sabitler import Aktivite, DeneyimEksen, OzelEtiket
from sunucu.veritabani.modeller import BolgeProfili, SabitRota, Sehir, Yer


class ApiHataDetayi(BaseModel):
    kod: str
    mesaj: str
    durum: Literal["empty", "insufficient", "unavailable", "error"]
    request_id: str
    ayrintilar: list[dict[str, str]] | None = None


class ApiHataCevabi(BaseModel):
    hata: ApiHataDetayi


class SehirCevap(BaseModel):
    id: str
    anahtar: str
    isim: str
    plaka_kodu: str | None = None
    bolge: str | None = None
    merkez_enlem: float | None = None
    merkez_boylam: float | None = None

    @classmethod
    def yerden_olustur(cls, sehir: Sehir, anahtar: str) -> "SehirCevap":
        return cls(
            id=sehir.id,
            anahtar=anahtar,
            isim=sehir.isim,
            plaka_kodu=sehir.plaka_kodu,
            bolge=sehir.bolge,
            merkez_enlem=sehir.merkez_enlem,
            merkez_boylam=sehir.merkez_boylam,
        )


class SehirIstatistikleri(BaseModel):
    """Ana sayfa kanit bandi: sayilar elle yazilmaz, buradan gelir
    (bkz. plan/tasarim/yon.md 3.8). Yorum sayisi BILEREK yoktur (K2)."""

    sehir_anahtari: str
    yer_sayisi: int
    kesif_yer_sayisi: int
    ilce_sayisi: int
    bolge_profili_sayisi: int
    deneyim_ekseni_sayisi: int


class YerOzet(BaseModel):
    """Kamusal yer ozeti.

    Bu allow-list ham puan, duygu ve ic karar alanlarini bilerek tasimaz.
    SQLAlchemy modeli veya ic analiz DTO'su response_model olarak
    kullanilmamalidir.
    """

    id: str
    isim: str
    ana_kategori: str
    alt_kategori: str
    ilce: str | None = None
    enlem: float
    boylam: float
    kapak_fotografi_url: str | None = None
    ticari_bildirim: str | None = None

    @classmethod
    def yerden_olustur(cls, yer: Yer, enlem: float, boylam: float) -> "YerOzet":
        return cls(
            id=yer.id,
            isim=yer.isim,
            ana_kategori=yer.ana_kategori,
            alt_kategori=yer.alt_kategori,
            ilce=yer.ilce,
            enlem=enlem,
            boylam=boylam,
            kapak_fotografi_url=yer.fotograf_urlleri[0] if yer.fotograf_urlleri else None,
            ticari_bildirim=(
                "sponsorlu"
                if yer.ozellikler.get(OzelEtiket.SPONSORLU_MEKAN.value) in (True, "true", "evet", "1", 1)
                else None
            ),
        )


class YerListeCevabi(BaseModel):
    """Keşif listesi: sayfa + filtre sonrasi toplam adet."""

    yerler: list[YerOzet]
    toplam_sayi: int


class PratikBilgi(BaseModel):
    """Yayina uygun claim projection'i; ham evidence veya ic puan tasimaz."""

    aile: str
    deger: Any | None = None
    bilgi_durumu: Literal["biliniyor", "bilinmiyor", "eskimis", "celiskili"]
    kapsam: dict[str, Any] = Field(default_factory=dict)
    gecerlilik_baslangici: datetime | None = None
    gecerlilik_bitisi: datetime | None = None
    dogrulanma_zamani: datetime | None = None
    yeniden_dogrulama: str | None = None


class IcOrnekYorum(BaseModel):
    """Yalniz ic/admin kullanim icin ham yorum DTO'su; public router'a baglanmaz."""

    yazar_takma_adi: str | None = None
    yorum_metni: str
    kaynakta_puan: float | None = None
    duygu_etiketi: str | None = None


class IcYerAnalizi(BaseModel):
    """Veritabaninda korunan, kamusal sozlesmeye girmeyen analiz alanlari."""

    kaynakta_puan_ortalamasi: float | None = None
    duygu_skoru_ortalama: float | None = None
    deneyim_puanlari: dict[str, int] = Field(default_factory=dict)
    yer_profili: dict = Field(default_factory=dict)
    duygu_ozeti: str | None = None
    ornek_yorumlar: list[IcOrnekYorum] = Field(default_factory=list)


class YerDetay(YerOzet):
    """Kamusal yer detayi; yalniz acikca izin verilen olgusal alanlar."""

    adres: str | None = None
    aciklama: str | None = None
    tanitim_metni: str | None = None
    telefon: str | None = None
    web_sitesi: str | None = None
    aktiviteler: list[str] = Field(default_factory=list)
    fotograf_urlleri: list[str] = Field(default_factory=list)
    pratik_bilgiler: list[PratikBilgi] = Field(default_factory=list)

    @classmethod
    def yerden_olustur(cls, yer: Yer, enlem: float, boylam: float) -> "YerDetay":
        return cls(
            id=yer.id,
            isim=yer.isim,
            ana_kategori=yer.ana_kategori,
            alt_kategori=yer.alt_kategori,
            ilce=yer.ilce,
            enlem=enlem,
            boylam=boylam,
            kapak_fotografi_url=yer.fotograf_urlleri[0] if yer.fotograf_urlleri else None,
            ticari_bildirim=(
                "sponsorlu"
                if yer.ozellikler.get(OzelEtiket.SPONSORLU_MEKAN.value) in (True, "true", "evet", "1", 1)
                else None
            ),
            adres=yer.adres,
            aciklama=yer.aciklama,
            tanitim_metni=getattr(yer, "tanitim_metni", None),
            telefon=yer.telefon,
            web_sitesi=yer.web_sitesi,
            aktiviteler=yer.aktiviteler,
            fotograf_urlleri=yer.fotograf_urlleri,
        )


class BolgeProfiliCevap(BaseModel):
    """Kamusal bolge tanitimi; yorum ve duygu turevlerini tasimaz."""

    bolge_adi: str
    ilce_mi: bool
    tanitim_metni: str | None = None
    # sehir_ayarlari.ilce_merkezleri — kolon yok, K6 veri katmani (poligon sonra).
    enlem: float | None = None
    boylam: float | None = None

    @classmethod
    def yerden_olustur(
        cls, bolge_profili: BolgeProfili, sehir_anahtari: str | None = None
    ) -> "BolgeProfiliCevap":
        from veri.ortak.sehir_ayarlari import bolge_merkezini_bul

        merkez = (
            bolge_merkezini_bul(sehir_anahtari, bolge_profili.bolge_adi)
            if sehir_anahtari
            else None
        )
        return cls(
            bolge_adi=bolge_profili.bolge_adi,
            ilce_mi=bolge_profili.ilce_mi,
            tanitim_metni=getattr(bolge_profili, "tanitim_metni", None),
            enlem=merkez[0] if merkez else None,
            boylam=merkez[1] if merkez else None,
        )


class SabitRotaCevap(BaseModel):
    """Elle kuratorlugu yapilan hazir rotalar (orn. Karya/Likya Yolu) --
    algoritma tarafindan degil, `sunucu/veritabani/modeller.py::SabitRota`
    tablosuna elle girilerek olusturulur."""

    id: str
    isim: str
    aciklama: str | None = None
    bolge: str | None = None
    rota_tipi: str | None = None
    durak_sayisi: int = 0
    kapak_fotografi_url: str | None = None

    @classmethod
    def yerden_olustur(cls, sabit_rota: SabitRota) -> "SabitRotaCevap":
        return cls(
            id=sabit_rota.id,
            isim=sabit_rota.isim,
            aciklama=sabit_rota.aciklama,
            bolge=sabit_rota.bolge,
            rota_tipi=sabit_rota.rota_tipi,
            durak_sayisi=len(sabit_rota.duraklar or []),
            kapak_fotografi_url=sabit_rota.kapak_fotografi_url,
        )


class RotaTercihleri(BaseModel):
    """dokumanlar/kategori_taksonomisi.md #4 (deneyim eksenleri) ve #6
    (yer profili) ile eslesen kullanici tercihleri."""

    ilgi_agirliklari: dict[DeneyimEksen, float] = Field(
        default_factory=dict,
        description="Deneyim ekseni -> 0-1 agirlik. Orn. {'tarihi_kulturel_puani': 0.8, 'eglence_puani': 0.2}",
    )
    aktiviteler: list[Aktivite] = Field(default_factory=list, description="Kullanicinin yapmak istedigi aktiviteler")
    zorunlu_duraklar: list[str] = Field(default_factory=list, description="Mutlaka rotaya dahil edilecek yer id'leri")
    ucuz_tercih_et: bool = Field(default=False, description="yer_profili.fiyat_algisi=ucuz olan yerler oncelenir")
    sakin_tercih_et: bool = Field(default=False, description="yer_profili.kalabalik_zamanlar'i kalabalik olan yerler geri planda kalir")


class RotaTalebi(BaseModel):
    """Yalniz kapali legacy endpoint'lerin istek sekli."""

    sehir_anahtari: str = Field(..., description="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari, orn. 'samsun'")
    gun_sayisi: int = Field(..., ge=1, le=14)
    konaklama_yer_id: str | None = Field(
        default=None, description="Senaryo 1: konaklama_yer_id VEYA konaklama_enlem/boylam verilirse konaklama bolgesi belli sayilir"
    )
    konaklama_enlem: float | None = Field(default=None, ge=-90, le=90)
    konaklama_boylam: float | None = Field(default=None, ge=-180, le=180)
    konaklama_bolge_adi: str | None = Field(
        default=None,
        description="Senaryo 1: ilce/bolge adi (orn. 'Atakum') -- merkez koordinata cozulur",
    )
    tercihler: RotaTercihleri = Field(default_factory=RotaTercihleri)
    alternatif_sayisi: int = Field(default=3, ge=2, le=3, description="Senaryo 2 alternatif endpoint'i icin")


class RotaDuragi(BaseModel):
    yer: YerOzet
    sira: int = Field(..., description="Gun icindeki durak sirasi, 1'den baslar")
    onceki_duraktan_mesafe_metre: float
    tahmini_ziyaret_suresi_dk: int


class GunPlani(BaseModel):
    gun_no: int
    duraklar: list[RotaDuragi]
    toplam_mesafe_metre: float
    toplam_sure_dakikasi: int


class KonaklamaBolgesiOnerisi(BaseModel):
    bolge_adi: str
    gerekce: str | None = None
    enlem: float | None = None
    boylam: float | None = None
    ornek_konaklamalar: list[YerOzet] = Field(default_factory=list)


class RotaCevap(BaseModel):
    id: str
    sehir_anahtari: str
    gun_sayisi: int
    gunler: list[GunPlani]
    konaklama_onerisi: YerOzet | None = Field(
        default=None, description="Eski Senaryo 2 otel onerisi (geriye uyumluluk); tercih bolge onerisi"
    )
    rota_tavsiyesi: str | None = None
    konaklama_bolgesi_onerisi: KonaklamaBolgesiOnerisi | None = None
    alternatif_etiketi: str | None = None


class AlternatifRotalarCevap(BaseModel):
    alternatifler: list[RotaCevap]


class GunlukPlanTalebi(BaseModel):
    """MVP'nin kamusal tek gunluk plan istegi; cok gun ve konaklama alani yoktur."""

    model_config = ConfigDict(extra="forbid")

    sehir_anahtari: str = Field(..., description="Tanimli sehir anahtari, orn. 'samsun'")
    tercihler: RotaTercihleri = Field(default_factory=RotaTercihleri)


class GunlukPlanCevap(BaseModel):
    """Tek bir gunluk plan aggregate'inin kamusal projection'i."""

    id: str
    sehir_anahtari: str
    duraklar: list[RotaDuragi]
    toplam_mesafe_metre: float
    toplam_sure_dakikasi: int
    rota_tavsiyesi: str | None = None
