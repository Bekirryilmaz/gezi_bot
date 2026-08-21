"""
Tum toplayicilarin (osm, google_maps, eksi_sozluk, tripadvisor) uretmesi gereken
ortak "Yer" veri modeli.

Amac: hangi kaynaktan gelirse gelsin, bir "yer" (gezilecek yer / konaklama /
restoran / kafe) her zaman ayni alanlara, ayni tiplere sahip olsun. Boylece
esleme (veri/esleme), kalite kontrol (veri/kalite_kontrol) ve veritabanina
aktarma islemleri tek bir formatla ugrasir.

Her toplayici, kendi ham verisini cektikten sonra bu modele donusturup
JSONL olarak veri/cikti/ham/<kaynak>/ altina yazar.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from ortak.sabitler import (
    ANA_KATEGORI_ALT_KATEGORILERI,
    Aktivite,
    AnaKategori,
    VeriKaynagi,
)


class OzellikSeti(BaseModel):
    """dokumanlar/kategori_taksonomisi.md #2'deki ozellik etiketleri.

    Hepsi opsiyoneldir cunku bir kaynaktan her ozellik cikarilamayabilir.
    None = bilinmiyor/tespit edilemedi (yanlislikla False sanilmasin diye
    ayri bir deger olarak tutulur).
    """

    model_config = {"extra": "allow"}

    alkol_servisi: bool | None = None
    ogrenci_dostu: bool | None = None
    aile_cocuk_dostu: bool | None = None
    evcil_hayvan_dostu: bool | None = None
    ucretsiz: bool | None = None
    rezervasyon_gerekli: bool | None = None
    engelli_erisimi: bool | None = None
    manzarali: bool | None = None
    romantik: bool | None = None
    sakin_calisma_ortami: bool | None = None
    canli_muzik: bool | None = None
    wifi: bool | None = None
    otopark: bool | None = None
    fiyat_seviyesi: int | None = Field(default=None, ge=1, le=4)
    en_iyi_ziyaret_mevsimi: str | None = None
    ortalama_ziyaret_suresi_dk: int | None = Field(default=None, ge=0)
    # Google Maps "Hakkinda" metni (tanitim_uretici tarafindan okunur)
    hakkinda: str | None = None


class Yer(BaseModel):
    """Bir gezilecek yer, konaklama veya yeme-icme mekanini temsil eden
    standart, kaynak-bagimsiz veri modeli."""

    # Kaynak izlenebilirligi -- her kayit hangi kaynaktan, ne zaman, hangi
    # orijinal kimlikle geldigini bilmeli. Esleme (dedup) asamasinda kritik.
    kaynak: VeriKaynagi
    kaynak_id: str = Field(..., description="Kaynaktaki orijinal kimlik (orn. OSM node id, Google place_id)")
    kaynak_url: str | None = None
    cekilme_zamani: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Temel bilgiler
    isim: str
    ana_kategori: AnaKategori
    alt_kategori: str
    sehir: str
    ilce: str | None = None
    adres: str | None = None
    aciklama: str | None = None
    telefon: str | None = None
    web_sitesi: str | None = None

    # Konum
    enlem: float = Field(..., ge=-90, le=90)
    boylam: float = Field(..., ge=-180, le=180)

    # Zenginlestirme
    ozellikler: OzellikSeti = Field(default_factory=OzellikSeti)
    aktiviteler: list[Aktivite] = Field(default_factory=list)
    fotograf_urlleri: list[str] = Field(default_factory=list)

    # Kaynaktaki ham puan (varsa) -- duygu analizi skorundan farkli, o ayri
    # hesaplanir. Bu sadece kaynagin kendi puanidir (orn. Google 4.5/5).
    kaynakta_puan_ortalamasi: float | None = Field(default=None, ge=0, le=5)
    kaynakta_puan_sayisi: int | None = Field(default=None, ge=0)

    @field_validator("isim", "sehir")
    @classmethod
    def bos_olamaz(cls, deger: str) -> str:
        deger = deger.strip()
        if not deger:
            raise ValueError("bos olamaz")
        return deger

    @model_validator(mode="after")
    def alt_kategori_dogrula(self) -> "Yer":
        gecerli_alt_kategoriler = ANA_KATEGORI_ALT_KATEGORILERI[self.ana_kategori.value]
        gecerli_degerler = {uye.value for uye in gecerli_alt_kategoriler}
        if self.alt_kategori not in gecerli_degerler:
            raise ValueError(
                f"'{self.alt_kategori}' gecerli bir alt kategori degil. "
                f"'{self.ana_kategori.value}' icin gecerli degerler: {sorted(gecerli_degerler)}"
            )
        return self

    def benzersiz_anahtar(self) -> str:
        """Ayni kaynak icinde tekillik kontrolu icin kullanilan anahtar."""
        return f"{self.kaynak.value}:{self.kaynak_id}"
