"""
Cok boyutlu yer profili icin ortak modeller.

Bu model, veri/duygu_analizi/pipeline_calistir.py'nin urettigi IslenmisYorum
kayitlarinin YER BAZINDA (bir yerin TUM yorumlari birlikte) sentezlenmesinin
sonucudur. veri/ortak/yorum_modeli.py::IslenmisYorum "bir yorum ne diyor"
sorusuna, YerProfili ise "bu yerin TUMU nasil bir yer" sorusuna cevap verir.

dokumanlar/kategori_taksonomisi.md #6'ya bakiniz.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class BoyutTespiti(BaseModel):
    """Tek bir profil boyutu (fiyat algisi, ulasim kolayligi vb.) icin
    tespit edilen deger + izlenebilirlik bilgisi.

    `guven` alani, bu tespitin KAC yorum/bahsedilmeye dayandigini yansitan
    0-1 arasi bir degerdir -- 0'a yakinsa "bilgi_yetersiz" durumunu, 1'e
    yakinsa cok sayida yorumdan turedigi icin guclu bir egilimi ifade eder.
    `ornek_ifadeler`, bu siniflandirmayi tetikleyen GERCEK yorum ifadelerinin
    bir kismidir -- "neden bu sonuc cikti" sorusunu HER ZAMAN geriye izlenebilir
    tutmak icin (konu_analizi.py'deki `gecen_ifade` alaniyla ayni amac)."""

    deger: str = Field(..., description="Orn. 'ucuz', 'kolay', 'bilgi_yetersiz'")
    guven: float = Field(..., ge=0, le=1, description="Kac yorum/bahsedilmeye dayandigina gore 0-1 arasi guven duzeyi")
    ornek_ifadeler: list[str] = Field(default_factory=list, description="Izlenebilirlik icin kaynak ifade ornekleri")


class YerProfili(BaseModel):
    """Bir yerin TUM (ona baglanabilen) yorumlarindan sentezlenen cok boyutlu
    profili. veri/duygu_analizi/yer_profili_cikarici.py::yer_profili_olustur
    tarafindan uretilir; sunucu/veritabani/modeller.py::Yer.yer_profili
    alanina bu modelin JSON karsiligi yazilir."""

    yer_kimligi: str = Field(..., description="Ilgili BirlesikYer kaydini isaret eden turetilmis kimlik")
    yer_ismi: str = Field(..., description="Insan tarafindan okunabilirlik icin -- JSONL dosyasini gozle kontrol ederken kimlik yerine isme bakabilesin")

    fiyat_algisi: BoyutTespiti
    ulasim_kolayligi: BoyutTespiti

    kalabalik_zamanlar: dict[str, str] = Field(
        default_factory=dict,
        description="Orn. {'hafta_sonu_aksam': 'kalabalik', 'hafta_ici_genel': 'sakin'} -- sadece yeterli veri olan zaman dilimleri listelenir",
    )
    ziyaretci_profili: dict[str, float] = Field(
        default_factory=dict,
        description="Ziyaretci tipi -> bahsedilme orani (0-1). Orn. {'aile': 0.42, 'cift': 0.31}",
    )

    kullanilan_yorum_sayisi: int = Field(..., ge=0, description="Bu profilin turetildigi toplam yorum sayisi")
    duygu_ozeti: str | None = Field(
        default=None, description="veri/duygu_analizi/anlatim_uretici.py tarafindan uretilen, kullaniciya gosterilecek tanitim metni"
    )
    olusturulma_zamani: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
