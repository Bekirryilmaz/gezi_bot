from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class HakDurumu(StrEnum):
    BILINMIYOR = "bilinmiyor"
    IZINLI = "izinli"
    YASAK = "yasak"


class KullanimAmaci(StrEnum):
    KAMUSAL_GOSTERIM = "kamusal_gosterim"
    TUREV_IDDIA = "turev_iddia"
    AI_ISLEME = "ai_isleme"
    UZUN_SURELI_SAKLAMA = "uzun_sureli_saklama"


class BilgiDurumu(StrEnum):
    BILINIYOR = "biliniyor"
    BILINMIYOR = "bilinmiyor"
    CELISKILI = "celiskili"
    ESKIMIS = "eskimis"
    GERI_CEKILMIS = "geri_cekilmis"


class GuvenSinifi(StrEnum):
    BELIRSIZ = "belirsiz"
    SINIRLI = "sinirli"
    DESTEKLI = "destekli"
    GUCLU = "guclu"


class IddiaAilesi(StrEnum):
    GIRIS_BASAMAK = "giris_basamak"
    ACIK_ALAN = "acik_alan"
    CALISMA_SAATI = "calisma_saati"
    FIYAT = "fiyat"
    OTOPARK = "otopark"
    ZIYARET_KOSULU = "ziyaret_kosulu"


@dataclass(frozen=True)
class KaynakHaklari:
    kamusal_gosterim: HakDurumu = HakDurumu.BILINMIYOR
    turev_iddia: HakDurumu = HakDurumu.BILINMIYOR
    ai_isleme: HakDurumu = HakDurumu.BILINMIYOR
    uzun_sureli_saklama: HakDurumu = HakDurumu.BILINMIYOR

    def izinli_mi(self, amac: KullanimAmaci | str) -> bool:
        """Yalniz istenen kullanim amacinin hakkini kontrol eder."""
        kullanim_amaci = KullanimAmaci(amac)
        return HakDurumu(getattr(self, kullanim_amaci.value)) is HakDurumu.IZINLI

    def amaclar_izinli_mi(self, *amaclar: KullanimAmaci | str) -> bool:
        """Bir akis icin acikca gereken amaclarin tamamini kontrol eder."""
        return all(self.izinli_mi(amac) for amac in amaclar)


@dataclass(frozen=True)
class ZamanKapsami:
    olay_zamani: datetime | None
    kaynakta_gozlemlenme_zamani: datetime | None
    cekilme_zamani: datetime
    dogrulanma_zamani: datetime | None
    sisteme_alinma_zamani: datetime
    gecerlilik_baslangici: datetime | None
    gecerlilik_bitisi: datetime | None

    def dogrula(self) -> None:
        if self.gecerlilik_baslangici and self.gecerlilik_bitisi:
            if self.gecerlilik_bitisi <= self.gecerlilik_baslangici:
                raise ValueError("gecerlilik_bitisi baslangictan sonra olmalidir")


def yayin_adayi_mi(
    *,
    bilgi_durumu: BilgiDurumu,
    kaynak_haklari: KaynakHaklari,
    destekleyen_kanit_sayisi: int,
    ai_tarafindan_uretildi: bool,
) -> bool:
    """IP-04 yayini yapmaz; yalniz temel bilgi kapisini hesaplar."""
    return bool(
        bilgi_durumu is BilgiDurumu.BILINIYOR
        and destekleyen_kanit_sayisi > 0
        and kaynak_haklari.izinli_mi(KullanimAmaci.TUREV_IDDIA)
        and not ai_tarafindan_uretildi
    )

