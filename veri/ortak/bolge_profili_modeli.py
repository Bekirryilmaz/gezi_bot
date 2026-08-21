"""
Bolge Profili ("sehir/ilce tanitim duygu analizi") icin ortak model.

YerProfili (bkz. yer_profili_modeli.py) TEK bir isletmenin/mekanin profilini
cikarirken, BolgeProfili bir BUTUN BOLGENIN (sehir merkezi VEYA bir ilce)
GENEL izlenimini cikarir -- "Samsun'a gidersem nasil bir yer beni
karsilayacak?" sorusuna cevap vermek icin. Girdisi, Eksi Sozluk'ten
`kaynak_yer_id` alani "bolge:<sehir_anahtari>:<bolge_adi>" bicimindeki
IslenmisYorum kayitlaridir (bkz. eksi_sozluk_toplayici.py ve
bolge_profili_cikarici.py).

Sehir-bagimsiz tasarlanmistir: `sehir_anahtari` + `bolge_adi` ikilisi hangi
sehir/ilce oldugunu belirler, Samsun disinda bir sehir eklendiginde bu model
DEGISTIRILMEDEN kullanilabilir.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from ortak.sabitler import DuyguEtiketi


class BolgeKonuOzeti(BaseModel):
    """Bir bolge icin on plana cikan TEK bir konu + o konudaki baskin duygu.
    yer_profili_cikarici.py'deki `on_plana_cikan_konular` mantiginin bolge
    seviyesindeki karsiligidir (bkz. profil_pipeline_calistir.py)."""

    konu: str
    duygu_etiketi: DuyguEtiketi
    bahsedilme_sayisi: int = Field(..., ge=0)


class BolgeProfili(BaseModel):
    """Bir bolgenin (sehir merkezi veya bir ilce) TUM bolge-geneli
    yorumlarindan sentezlenen genel tanitim duygu profili.
    veri/duygu_analizi/bolge_profili_cikarici.py::bolge_profili_olustur
    tarafindan uretilir; sunucu/veritabani/modeller.py::BolgeProfili
    tablosuna aktarilir (bkz. sunucu/veritabani/aktarim/bolge_profil_aktar.py)."""

    sehir_anahtari: str = Field(..., description="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari, orn. 'samsun'")
    bolge_adi: str = Field(..., description="Sehir merkeziyse sehrin kendi adi, ilceyse ilce adi, orn. 'Atakum'")
    ilce_mi: bool = Field(..., description="False ise bu profil sehir MERKEZI/GENELI icindir")

    genel_duygu_skoru: float | None = Field(default=None, ge=-1, le=1, description="Bolgeye ait yorumlarin duygu_skoru ortalamasi")
    genel_duygu_etiketi: DuyguEtiketi | None = None

    on_plana_cikan_konular: list[BolgeKonuOzeti] = Field(default_factory=list)

    kullanilan_yorum_sayisi: int = Field(..., ge=0)
    duygu_ozeti: str | None = Field(
        default=None,
        description="veri/duygu_analizi/anlatim_uretici.py::bolge_tanitim_metni_uret tarafindan uretilen tanitim metni",
    )
    olusturulma_zamani: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def bolge_kimligi(self) -> str:
        """sunucu/veritabani/aktarim/bolge_profil_aktar.py'nin (sehir_id,
        bolge_adi) unique kisitiyla eslesen, JSONL icinde kullanilan
        deterministik anahtar."""
        return f"{self.sehir_anahtari}:{self.bolge_adi.strip().lower()}"
