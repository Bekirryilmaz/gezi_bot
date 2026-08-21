"""
Rota motorunun kullandigi, SQLAlchemy/veritabanindan BAGIMSIZ saf veri tipleri.

Boylece `skorlama.py`, `zaman_butcesi.py`, `kumeleme.py`, `siralama.py`
gercek bir veritabani baglantisi olmadan, sentetik `AdayYer` listeleriyle
test edilebilir (bkz. `sunucu/rota_motoru/testler/`). Veritabani <-> bu
tipler arasindaki donusum SADECE `rota_olusturucu.py`'de yapilir.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AdayYer:
    """Rota motorunun bir 'yer'i degerlendirmek icin ihtiyac duydugu
    minimal bilgi kumesi -- `sunucu/veritabani/modeller.py::Yer`'in
    sadelestirilmis izdusumu."""

    id: str
    isim: str
    ana_kategori: str
    alt_kategori: str
    enlem: float
    boylam: float
    deneyim_puanlari: dict[str, int] = field(default_factory=dict)
    yer_profili: dict = field(default_factory=dict)
    aktiviteler: list[str] = field(default_factory=list)
    ortalama_ziyaret_suresi_dk: int | None = None
    kaynakta_puan_ortalamasi: float | None = None
    duygu_skoru_ortalama: float | None = None
    kapak_fotografi_url: str | None = None
    ilce: str | None = None


@dataclass
class RotaTercihleri:
    """`sunucu/api/semalar.py::RotaTercihleri`'nin rota motoru icindeki
    karsiligi -- API katmanindan (Pydantic/Enum) bagimsiz, saf Python
    tipleriyle (str/float/bool) calisir."""

    ilgi_agirliklari: dict[str, float] = field(default_factory=dict)
    aktiviteler: list[str] = field(default_factory=list)
    zorunlu_duraklar: list[str] = field(default_factory=list)
    ucuz_tercih_et: bool = False
    sakin_tercih_et: bool = False


@dataclass
class RotaDuragiSonucu:
    yer: AdayYer
    sira: int
    onceki_duraktan_mesafe_metre: float
    tahmini_ziyaret_suresi_dk: int
    skor_kirilimi: dict[str, float] = field(default_factory=dict)


@dataclass
class GunSonucu:
    gun_no: int
    duraklar: list[RotaDuragiSonucu]
    toplam_mesafe_metre: float
    toplam_sure_dakikasi: int


@dataclass
class RotaSonucu:
    gunler: list[GunSonucu]
    konaklama_onerisi: AdayYer | None = None
    id: str | None = None  # rota_olusturucu.py::_rotayi_kaydet tarafindan doldurulur
    rota_tavsiyesi: str | None = None
    konaklama_bolgesi_adi: str | None = None
    konaklama_bolgesi_gerekce: str | None = None
    konaklama_bolgesi_enlem: float | None = None
    konaklama_bolgesi_boylam: float | None = None
    ornek_konaklamalar: list[AdayYer] = field(default_factory=list)
    alternatif_etiketi: str | None = None  # orn. "Tarih & kültür ağırlıklı"
