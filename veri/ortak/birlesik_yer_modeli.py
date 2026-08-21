"""
Birlesik (esleme sonrasi tekillestirilmis) yer modeli.

veri/ortak/yer_modeli.py::Yer, HER KAYNAKTAN gelen HAM kaydi temsil eder --
ayni fiziksel yer (orn. "Amazon Koyu") OSM'de, Google Maps'te VE
TripAdvisor'da 3 AYRI Yer kaydi olarak var olabilir. veri/esleme/eslestirici.py
bu 3 kaydi tespit edip TEK bir BirlesikYer kaydina indirger.

Bu model kasitli olarak sunucu/veritabani/modeller.py::Yer + YerKaynak
tablolarinin alanlarina yakin tutulmustur -- ileride bu JSONL dosyalarini
PostgreSQL'e aktaracak bir yukleme (import) betigi yazildiginda alan alan
neredeyse birebir eslesecek.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from ortak.sabitler import ANA_KATEGORI_ALT_KATEGORILERI, Aktivite, AnaKategori, VeriKaynagi
from veri.ortak.yer_modeli import OzellikSeti


class KaynakReferansi(BaseModel):
    """Birlesik bir yerin, hangi ham kaynak kayitlarindan olusturuldugunu
    izlemek icin kullanilir (izlenebilirlik -- 'bu bilgi nereden geldi?')."""

    kaynak: VeriKaynagi
    kaynak_id: str
    kaynak_url: str | None = None
    kaynakta_puan_ortalamasi: float | None = None
    kaynakta_puan_sayisi: int | None = None


class BirlesikYer(BaseModel):
    """Esleme (dedup) sonrasi TEK bir fiziksel yeri temsil eden kayit.

    veritabanina aktarilacak nihai "Yer" satirinin JSONL karsiligidir.
    """

    isim: str
    ana_kategori: AnaKategori
    alt_kategori: str
    sehir: str
    ilce: str | None = None
    adres: str | None = None
    aciklama: str | None = None
    telefon: str | None = None
    web_sitesi: str | None = None

    enlem: float = Field(..., ge=-90, le=90)
    boylam: float = Field(..., ge=-180, le=180)

    ozellikler: OzellikSeti = Field(default_factory=OzellikSeti)
    aktiviteler: list[Aktivite] = Field(default_factory=list)
    fotograf_urlleri: list[str] = Field(default_factory=list)

    # Kaynaklarin puanlarindan agirlikli ortalama (bkz. eslestirici.py::_puanlari_birlestir)
    kaynakta_puan_ortalamasi: float | None = Field(default=None, ge=0, le=5)
    kaynakta_puan_sayisi: int | None = Field(default=None, ge=0)

    kaynaklar: list[KaynakReferansi] = Field(
        default_factory=list, description="Bu kaydi olusturan tum ham kaynak kayitlarinin listesi"
    )
    birlestirme_zamani: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("isim", "sehir")
    @classmethod
    def bos_olamaz(cls, deger: str) -> str:
        deger = deger.strip()
        if not deger:
            raise ValueError("bos olamaz")
        return deger

    @model_validator(mode="after")
    def alt_kategori_dogrula(self) -> "BirlesikYer":
        gecerli_alt_kategoriler = ANA_KATEGORI_ALT_KATEGORILERI[self.ana_kategori.value]
        gecerli_degerler = {uye.value for uye in gecerli_alt_kategoriler}
        if self.alt_kategori not in gecerli_degerler:
            raise ValueError(
                f"'{self.alt_kategori}' gecerli bir alt kategori degil. "
                f"'{self.ana_kategori.value}' icin gecerli degerler: {sorted(gecerli_degerler)}"
            )
        return self

    @property
    def kac_kaynaktan_dogrulandi(self) -> int:
        """Bu yerin kac FARKLI kaynak turunden (OSM/Google/TripAdvisor) geldigi.
        Birden fazlaysa, kalite kontrol acisindan daha 'guvenilir' sayilir."""
        return len({k.kaynak for k in self.kaynaklar})

    @property
    def yer_kimligi(self) -> str:
        """Bu BirlesikYer'in JSONL ciktisinda kalici bir veritabani id'si
        yoktur (esleme asamasi ile veritabanina aktarma asamasi ayri
        calisir). Bu yuzden isim+konumdan DETERMINISTIK bir kimlik turetilir:
        ayni yer sonraki calistirmalarda (isim/konum onemli olcude
        degismedigi surece) ayni kimligi alir.

        Bu kararlilik iki yerde sarttir: (1) veri/duygu_analizi/anlatim_uretici.py
        ayni yer icin HER ZAMAN ayni tanitim metnini uretebilsin diye,
        (2) sunucu/veritabani/aktarim/profil_aktar.py bu kimlikle
        YerProfili JSONL kaydini dogru Yer veritabani satirina baglayabilsin
        diye. Tek dogruluk kaynagi burasi -- baska hicbir yerde bu hash
        tekrar hesaplanmamali."""
        anahtar = f"{self.isim.strip().lower()}|{self.enlem:.5f}|{self.boylam:.5f}"
        return hashlib.md5(anahtar.encode("utf-8")).hexdigest()[:16]
