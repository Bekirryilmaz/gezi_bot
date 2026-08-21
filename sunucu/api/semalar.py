"""
API istek/cevap semalari (Pydantic).

`sunucu/veritabani/modeller.py`'deki SQLAlchemy modellerinden BILEREK ayri
tutulur: veritabani semasi (nasil saklandigi) ile API semasi (disariya nasil
gosterildigi/hangi alanlarin istendigi) farkli kaygilardir -- birini
degistirmek digerini kirmasin diye ayrilir.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from ortak.sabitler import Aktivite, DeneyimEksen
from sunucu.veritabani.modeller import BolgeProfili, SabitRota, Sehir, Yer


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


class YerOzet(BaseModel):
    """Liste gorunumlerinde (yer listeleme, rota duraklari) kullanilan
    kisa yer bilgisi."""

    id: str
    isim: str
    ana_kategori: str
    alt_kategori: str
    ilce: str | None = None
    enlem: float
    boylam: float
    kaynakta_puan_ortalamasi: float | None = None
    duygu_skoru_ortalama: float | None = None
    kapak_fotografi_url: str | None = None

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
            kaynakta_puan_ortalamasi=yer.kaynakta_puan_ortalamasi,
            duygu_skoru_ortalama=yer.duygu_skoru_ortalama,
            kapak_fotografi_url=yer.fotograf_urlleri[0] if yer.fotograf_urlleri else None,
        )


class OrnekYorum(BaseModel):
    yazar_takma_adi: str | None = None
    yorum_metni: str
    kaynakta_puan: float | None = None
    duygu_etiketi: str | None = None


class YerDetay(YerOzet):
    """Yer detay sayfasinda gosterilen tam bilgi -- yer profili ve
    duygu ozeti dahil (bkz. dokumanlar/kategori_taksonomisi.md #6)."""

    adres: str | None = None
    aciklama: str | None = None
    tanitim_metni: str | None = None
    telefon: str | None = None
    web_sitesi: str | None = None
    ozellikler: dict = Field(default_factory=dict)
    aktiviteler: list[str] = Field(default_factory=list)
    fotograf_urlleri: list[str] = Field(default_factory=list)
    deneyim_puanlari: dict[str, int] = Field(default_factory=dict)
    yer_profili: dict = Field(default_factory=dict)
    duygu_ozeti: str | None = None
    ornek_yorumlar: list[OrnekYorum] = Field(default_factory=list)

    @classmethod
    def yerden_olustur(cls, yer: Yer, enlem: float, boylam: float, ornek_yorumlar: list[OrnekYorum]) -> "YerDetay":
        return cls(
            id=yer.id,
            isim=yer.isim,
            ana_kategori=yer.ana_kategori,
            alt_kategori=yer.alt_kategori,
            ilce=yer.ilce,
            enlem=enlem,
            boylam=boylam,
            kaynakta_puan_ortalamasi=yer.kaynakta_puan_ortalamasi,
            duygu_skoru_ortalama=yer.duygu_skoru_ortalama,
            kapak_fotografi_url=yer.fotograf_urlleri[0] if yer.fotograf_urlleri else None,
            adres=yer.adres,
            aciklama=yer.aciklama,
            tanitim_metni=getattr(yer, "tanitim_metni", None),
            telefon=yer.telefon,
            web_sitesi=yer.web_sitesi,
            ozellikler=yer.ozellikler,
            aktiviteler=yer.aktiviteler,
            fotograf_urlleri=yer.fotograf_urlleri,
            deneyim_puanlari=yer.deneyim_puanlari,
            yer_profili=yer.yer_profili,
            duygu_ozeti=yer.duygu_ozeti,
            ornek_yorumlar=ornek_yorumlar,
        )


class BolgeProfiliCevap(BaseModel):
    """Bir bolgenin (sehir merkezi veya bir ilce) tanitim duygu profili --
    veri/ortak/bolge_profili_modeli.py::BolgeProfili ile eslesir. Sehir
    secim/tanitim ekranlarinda 'Burasi nasil bir yer?' sorusuna cevap
    vermek icin kullanilir (bkz. dokumanlar/kategori_taksonomisi.md #6)."""

    bolge_adi: str
    ilce_mi: bool
    genel_duygu_skoru: float | None = None
    genel_duygu_etiketi: str | None = None
    on_plana_cikan_konular: list[dict] = Field(default_factory=list)
    kullanilan_yorum_sayisi: int
    duygu_ozeti: str | None = None
    tanitim_metni: str | None = None

    @classmethod
    def yerden_olustur(cls, bolge_profili: BolgeProfili) -> "BolgeProfiliCevap":
        return cls(
            bolge_adi=bolge_profili.bolge_adi,
            ilce_mi=bolge_profili.ilce_mi,
            genel_duygu_skoru=bolge_profili.genel_duygu_skoru,
            genel_duygu_etiketi=bolge_profili.genel_duygu_etiketi,
            on_plana_cikan_konular=bolge_profili.on_plana_cikan_konular,
            kullanilan_yorum_sayisi=bolge_profili.kullanilan_yorum_sayisi,
            duygu_ozeti=bolge_profili.duygu_ozeti,
            tanitim_metni=getattr(bolge_profili, "tanitim_metni", None),
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
    duraklar: list[dict] = Field(default_factory=list)
    kapak_fotografi_url: str | None = None

    @classmethod
    def yerden_olustur(cls, sabit_rota: SabitRota) -> "SabitRotaCevap":
        return cls(
            id=sabit_rota.id,
            isim=sabit_rota.isim,
            aciklama=sabit_rota.aciklama,
            bolge=sabit_rota.bolge,
            rota_tipi=sabit_rota.rota_tipi,
            duraklar=sabit_rota.duraklar,
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
    skor_kirilimi: dict[str, float] = Field(
        default_factory=dict, description="Bu duragin nicin secildigini aciklayan puan bilesenleri (seffaflik icin)"
    )


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
