"""
Veritabani semasi (SQLAlchemy modelleri).

Tasarim kararlari:

- Her yer bir `sehir_id` tasir -> proje sehir-bagimsiz calisir, yeni sehir
  eklemek yeni bir Sehir satiri + o sehir icin toplayici calistirmaktan ibarettir.
- `Yer` tablosu hem gezilecek yerleri hem konaklamayi hem yeme-icme mekanlarini
  tutar (ana_kategori ile ayrilir). Boylece rota algoritmasi tek bir tablo
  uzerinden cografi sorgu (PostGIS) yapabilir; ayri tablolara bolmek gereksiz
  JOIN karmasikligi yaratirdi.
- `ozellikler`, `aktiviteler`, `deneyim_puanlari` JSONB olarak tutulur (ayri
  tablo/kolon acmak yerine). Sebep: dokumanlar/kategori_taksonomisi.md
  zamanla genisleyecek (yeni ozellik/aktivite eklenecek), JSONB ile bu yeni
  alanlar icin veritabani migration'i gerekmez.
- Kaynak izlenebilirligi `YerKaynak` ile ayri tutulur: ayni fiziksel yer birden
  fazla kaynaktan (OSM + Google + TripAdvisor) gelebilir, esleme (veri/esleme)
  bunlari tek bir `Yer` satirina baglar ama hangi kaynaktan geldigini kaybetmeyiz.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ortak.sabitler import AnaKategori
from sunucu.veritabani.temel import Taban


def _uuid_uret() -> str:
    return str(uuid.uuid4())


class Sehir(Taban):
    """Platformun kapsadigi her sehir. Samsun ilk kayittir, digerleri
    bolgesel buyume stratejisine gore zamanla eklenir."""

    __tablename__ = "sehirler"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid_uret)
    isim: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    plaka_kodu: Mapped[str | None] = mapped_column(String(2))
    bolge: Mapped[str | None] = mapped_column(String(50), comment="Orn. 'Karadeniz' -- bolgesel rota gruplamasi icin")
    merkez_enlem: Mapped[float | None] = mapped_column(Float)
    merkez_boylam: Mapped[float | None] = mapped_column(Float)
    aktif_mi: Mapped[bool] = mapped_column(default=True, comment="Site uzerinde yayinda mi")
    olusturulma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    yerler: Mapped[list["Yer"]] = relationship(back_populates="sehir")

    def __repr__(self) -> str:
        return f"<Sehir {self.isim}>"


class Yer(Taban):
    """Bir gezilecek yer, konaklama veya yeme-icme mekani.

    veri/ortak/yer_modeli.py::Yer pydantic modeliyle kavramsal olarak
    eslesir; buradaki tablo, esleme (dedup) sonrasi TEKIL/birlestirilmis
    yer kaydini tutar (ham kaynak verisi degil)."""

    __tablename__ = "yerler"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid_uret)
    sehir_id: Mapped[str] = mapped_column(ForeignKey("sehirler.id", ondelete="CASCADE"), nullable=False)

    isim: Mapped[str] = mapped_column(String(255), nullable=False)
    ana_kategori: Mapped[str] = mapped_column(String(30), nullable=False)
    alt_kategori: Mapped[str] = mapped_column(String(50), nullable=False)

    ilce: Mapped[str | None] = mapped_column(String(100))
    adres: Mapped[str | None] = mapped_column(Text)
    aciklama: Mapped[str | None] = mapped_column(Text)
    tanitim_metni: Mapped[str | None] = mapped_column(
        Text, comment="Wikipedia/OSM/Google/sablon birlesiminden turetilen tanitim"
    )
    telefon: Mapped[str | None] = mapped_column(String(30))
    web_sitesi: Mapped[str | None] = mapped_column(String(500))

    # PostGIS cografi nokta -- rota algoritmasindaki "en yakin N yer" ve
    # "X km yaricap icindeki yerler" sorgulari icin (ST_DWithin, ST_Distance).
    konum: Mapped[str] = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=False)

    ozellikler: Mapped[dict] = mapped_column(JSONB, default=dict, comment="dokumanlar/kategori_taksonomisi.md #2")
    aktiviteler: Mapped[list] = mapped_column(JSONB, default=list, comment="dokumanlar/kategori_taksonomisi.md #3")
    fotograf_urlleri: Mapped[list] = mapped_column(JSONB, default=list)

    # Kaynaklardaki ham puanlarin agirlikli ortalamasi (esleme asamasinda hesaplanir)
    kaynakta_puan_ortalamasi: Mapped[float | None] = mapped_column(Float)
    kaynakta_puan_sayisi: Mapped[int | None] = mapped_column(Integer)

    # Duygu analizinden uretilen, rota algoritmasinin dogrudan kullandigi alanlar
    duygu_skoru_ortalama: Mapped[float | None] = mapped_column(Float, comment="-1..+1 arasi, yorumlar.duygu_skoru ortalamasi")
    deneyim_puanlari: Mapped[dict] = mapped_column(
        JSONB, default=dict, comment="dokumanlar/kategori_taksonomisi.md #4 -- 6 eksende 0-100 puan"
    )
    yer_profili: Mapped[dict] = mapped_column(
        JSONB, default=dict, comment="dokumanlar/kategori_taksonomisi.md #6 -- YerProfili (fiyat algisi, ulasim, kalabalik zamanlar, ziyaretci profili)"
    )
    duygu_ozeti: Mapped[str | None] = mapped_column(
        Text, comment="yer_profili'nden sentezlenen, kullaniciya gosterilecek samimi tanitim metni"
    )
    duygu_son_guncelleme: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    olusturulma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    guncellenme_zamani: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    sehir: Mapped["Sehir"] = relationship(back_populates="yerler")
    kaynaklar: Mapped[list["YerKaynak"]] = relationship(back_populates="yer", cascade="all, delete-orphan")
    yorumlar: Mapped[list["Yorum"]] = relationship(back_populates="yer", cascade="all, delete-orphan")
    konaklama_detayi: Mapped["KonaklamaDetay | None"] = relationship(
        back_populates="yer", cascade="all, delete-orphan", uselist=False
    )

    __table_args__ = (
        Index("ix_yerler_konum", "konum", postgresql_using="gist"),
        Index("ix_yerler_sehir_kategori", "sehir_id", "ana_kategori", "alt_kategori"),
    )

    def __repr__(self) -> str:
        return f"<Yer {self.isim} ({self.alt_kategori})>"


class BolgeProfili(Taban):
    """Bir bolgenin (sehir merkezi veya bir ilce) GENEL tanitim duygu
    profili -- veri/ortak/bolge_profili_modeli.py::BolgeProfili ile eslesir.

    `Yer` tablosundan AYRI tutulur cunku bir bolge belirli bir isletmeyi
    degil, BUTUN bir cografi alani (orn. 'Atakum ilcesi') temsil eder;
    Eksi Sozluk'un bolge-geneli yorumlarindan (bkz. eksi_sozluk_toplayici.py,
    bolge_profili_cikarici.py) turetilir ve kullanicilara sehir/ilce
    TANITIMI icin gosterilir (orn. sehir secim ekraninda 'Atakum nasil bir
    yer?' bilgisi)."""

    __tablename__ = "bolge_profilleri"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid_uret)
    sehir_id: Mapped[str] = mapped_column(ForeignKey("sehirler.id", ondelete="CASCADE"), nullable=False)

    bolge_adi: Mapped[str] = mapped_column(String(100), nullable=False, comment="Sehir merkeziyse sehrin adi, ilceyse ilce adi")
    ilce_mi: Mapped[bool] = mapped_column(default=False, comment="False ise bu profil sehir MERKEZI/GENELI icindir")

    genel_duygu_skoru: Mapped[float | None] = mapped_column(Float, comment="-1..+1, bolgeye ait yorumlarin ortalamasi")
    genel_duygu_etiketi: Mapped[str | None] = mapped_column(String(20))
    on_plana_cikan_konular: Mapped[list] = mapped_column(JSONB, default=list, comment="[{konu, duygu_etiketi, bahsedilme_sayisi}]")
    kullanilan_yorum_sayisi: Mapped[int] = mapped_column(Integer, default=0)
    duygu_ozeti: Mapped[str | None] = mapped_column(Text, comment="anlatim_uretici.py::bolge_tanitim_metni_uret ciktisi")
    tanitim_metni: Mapped[str | None] = mapped_column(Text, comment="Wikipedia/sablon bolge tanitimi")

    olusturulma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    guncellenme_zamani: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    sehir: Mapped["Sehir"] = relationship()

    __table_args__ = (UniqueConstraint("sehir_id", "bolge_adi", name="ux_bolge_profilleri_sehir_bolge"),)

    def __repr__(self) -> str:
        return f"<BolgeProfili {self.bolge_adi}>"


class YerKaynak(Taban):
    """Bir Yer'in hangi ham veri kaynaklarindan geldigini izler.

    Esleme (veri/esleme) asamasi, ayni fiziksel yeri farkli kaynaklarda
    (OSM + Google + TripAdvisor) tespit edip tek bir Yer'e bagladiginda,
    her kaynagi burada ayri bir satir olarak tutar. Boylece 'bu bilgi
    nereden geldi' sorusu her zaman cevaplanabilir."""

    __tablename__ = "yer_kaynaklari"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid_uret)
    yer_id: Mapped[str] = mapped_column(ForeignKey("yerler.id", ondelete="CASCADE"), nullable=False)

    kaynak: Mapped[str] = mapped_column(String(30), nullable=False)
    kaynak_id: Mapped[str] = mapped_column(String(255), nullable=False)
    kaynak_url: Mapped[str | None] = mapped_column(String(500))
    cekilme_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    kaynakta_gozlemlenme_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sisteme_alinma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    veri_batch_id: Mapped[str | None] = mapped_column(ForeignKey("veri_batchleri.id", ondelete="SET NULL"))
    sube_id: Mapped[str | None] = mapped_column(ForeignKey("subeler.id", ondelete="RESTRICT"))

    yer: Mapped["Yer"] = relationship(back_populates="kaynaklar")

    __table_args__ = (UniqueConstraint("kaynak", "kaynak_id", name="ux_yer_kaynaklari_kaynak_kimlik"),)


class KonaklamaDetay(Taban):
    """`Yer.ana_kategori == KONAKLAMA` olan kayitlar icin ek, konaklamaya
    ozel alanlar. Ayri tabloda tutulur cunku bu alanlar diger yer tiplerinde
    (restoran, tarihi yer vb.) anlamsizdir -- Yer tablosunu gereksiz bos
    kolonlarla sismekten kurtarir."""

    __tablename__ = "konaklama_detaylari"

    yer_id: Mapped[str] = mapped_column(ForeignKey("yerler.id", ondelete="CASCADE"), primary_key=True)
    gecelik_fiyat_araligi_min: Mapped[float | None] = mapped_column(Float)
    gecelik_fiyat_araligi_max: Mapped[float | None] = mapped_column(Float)
    rezervasyon_linkleri: Mapped[dict] = mapped_column(JSONB, default=dict, comment="orn. {'booking': '...', 'etstur': '...'}")
    oda_sayisi: Mapped[int | None] = mapped_column(Integer)

    yer: Mapped["Yer"] = relationship(back_populates="konaklama_detayi")


class Yorum(Taban):
    """veri/ortak/yorum_modeli.py::IslenmisYorum ile eslesir. Duygu analizi
    pipeline'inin cikisi burada saklanir."""

    __tablename__ = "yorumlar"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid_uret)
    yer_id: Mapped[str] = mapped_column(ForeignKey("yerler.id", ondelete="CASCADE"), nullable=False)

    kaynak: Mapped[str] = mapped_column(String(30), nullable=False)
    kaynak_yorum_id: Mapped[str | None] = mapped_column(String(255))
    yazar_takma_adi: Mapped[str | None] = mapped_column(String(100))

    yorum_metni: Mapped[str] = mapped_column(Text, nullable=False)
    kaynakta_puan: Mapped[float | None] = mapped_column(Float)
    yorum_tarihi: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    dil: Mapped[str] = mapped_column(String(5), default="tr")

    duygu_skoru: Mapped[float | None] = mapped_column(Float, comment="-1..+1")
    duygu_etiketi: Mapped[str | None] = mapped_column(String(20))
    konu_duygulari: Mapped[list] = mapped_column(JSONB, default=list, comment="[{konu, duygu_etiketi, gecen_ifade}]")
    analiz_model_adi: Mapped[str | None] = mapped_column(String(200))
    analiz_zamani: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    cekilme_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    yer: Mapped["Yer"] = relationship(back_populates="yorumlar")

    __table_args__ = (
        UniqueConstraint("kaynak", "kaynak_yorum_id", name="ux_yorumlar_kaynak_kimlik"),
        Index("ix_yorumlar_yer", "yer_id"),
    )


class SabitRota(Taban):
    """Bizim elle kuratorlugunu yaptigimiz, bilinen/hazir rotalar
    (orn. Karya/Likya Yolu, Antep-Urfa gastronomi rotasi). Algoritma
    tarafindan degil, elle olusturulur ve guncellenir."""

    __tablename__ = "sabit_rotalar"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid_uret)
    isim: Mapped[str] = mapped_column(String(255), nullable=False)
    aciklama: Mapped[str | None] = mapped_column(Text)
    bolge: Mapped[str | None] = mapped_column(String(50), comment="Orn. 'Karadeniz', tek sehri asan rotalar icin")
    rota_tipi: Mapped[str | None] = mapped_column(String(50), comment="Orn. 'gastronomi', 'tarihi', 'doga'")
    duraklar: Mapped[list] = mapped_column(JSONB, default=list, comment="[{gun, yer_id veya serbest_metin_konum, aciklama}]")
    kapak_fotografi_url: Mapped[str | None] = mapped_column(String(500))
    olusturulma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class KullaniciRotasi(Taban):
    """Algoritmanin kullanici tercihlerine gore urettigi kisisel rota
    (Faz 2). Semasi simdiden tanimlanir ki veri katmani hangi alanlarin
    doldurulmasi gerektigini bilerek ilerlesin."""

    __tablename__ = "kullanici_rotalari"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=_uuid_uret)
    sehir_id: Mapped[str] = mapped_column(ForeignKey("sehirler.id", ondelete="CASCADE"), nullable=False)

    tercihler: Mapped[dict] = mapped_column(
        JSONB, nullable=False, comment="gun_sayisi, ilgi_agirliklari, aktiviteler, zorunlu_duraklar, konaklama_yer_id vb."
    )
    gunler: Mapped[list] = mapped_column(JSONB, default=list, comment="[{gun_no, duraklar: [yer_id, ...]}]")
    konaklama_onerisi_yer_id: Mapped[str | None] = mapped_column(
        ForeignKey("yerler.id"), comment="Senaryo 2: konaklama bolgesi belli degilse onerilen yer"
    )

    olusturulma_zamani: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# Ayrik domain dosyalari metadata'ya kaydedilir; public API bunlari import etmez.
from sunucu.veritabani.bilgi_modelleri import (  # noqa: E402,F401
    Gozlem, Iddia, IddiaSurumu, KanitBaglantisi, KaynakPolitikasi, VeriBatch,
)
from sunucu.veritabani.kimlik_modelleri import (  # noqa: E402,F401
    EslemeAdayi, EslemeKarari, Sube, YerAlias, YerBirlestirmesi, YerKimligi,
)
from sunucu.veritabani.yayin_modelleri import (  # noqa: E402,F401
    EtkiBaglantisi, GecersizlestirmeOlayi, GeriCekmeKaydi, PublicProjection, YayinKaydi,
)
from sunucu.veritabani.admin_modelleri import (  # noqa: E402,F401
    AdminAuditOlayi, AdminKullanici, AdminKullaniciRolu, AdminOturum, AdminRol, IncelemeDosyasi,
)
