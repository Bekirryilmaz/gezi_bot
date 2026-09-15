from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from sunucu.karar_motoru.domain import Karsilastirma, KosulDurumu, Tercih, ZorunluKosul


class AramaSonucuTuru(StrEnum):
    YER_KIMLIGI = "yer_kimligi"
    KATEGORI = "kategori"
    SEHIR = "sehir"
    ILCE = "ilce"
    BAGLAMSAL_ADAY = "baglamsal_aday"


class EslesmeNedeni(StrEnum):
    TAM_AD = "tam_ad"
    AD_BASLANGICI = "ad_baslangici"
    YAZIM_YAKINLIGI = "yazim_yakinligi"
    KATEGORI = "kategori"
    SEHIR = "sehir"
    ILCE = "ilce"
    BAGLAM = "baglam"


@dataclass(frozen=True)
class SomutKosulTanimi:
    kod: str
    etiket: str
    iddia_ailesi: str
    beklenen_deger: Any
    karsilastirma: Karsilastirma = Karsilastirma.ESITTIR

    def zorunlu_kosul(self) -> ZorunluKosul:
        return ZorunluKosul(
            kod=self.kod,
            iddia_ailesi=self.iddia_ailesi,
            beklenen_deger=self.beklenen_deger,
            karsilastirma=self.karsilastirma,
        )

    def tercih(self) -> Tercih:
        return Tercih(
            kod=self.kod,
            iddia_ailesi=self.iddia_ailesi,
            beklenen_deger=self.beklenen_deger,
            karsilastirma=self.karsilastirma,
        )


# Yalniz yapilandirilmis claim ailesi karsiligi olan MVP kosullari. API, bunlari
# da ancak aktif/yayinlanabilir bir claim gercekten varsa filtre katalogunda acar.
SOMUT_KOSULLAR: dict[str, SomutKosulTanimi] = {
    "tekerlekli_sandalye_erisimi": SomutKosulTanimi(
        "tekerlekli_sandalye_erisimi", "Tekerlekli sandalye erişimi", "tekerlekli_sandalye_erisimi", True
    ),
    "basamaksiz_giris": SomutKosulTanimi(
        "basamaksiz_giris", "Basamaksız giriş", "giris_basamak", False
    ),
    "engelli_tuvaleti": SomutKosulTanimi(
        "engelli_tuvaleti", "Erişilebilir tuvalet", "engelli_tuvaleti", True
    ),
    "otopark": SomutKosulTanimi("otopark", "Otopark", "otopark", True),
    "sessiz_ortam": SomutKosulTanimi("sessiz_ortam", "Sessiz ortam", "sessiz_ortam", True),
}


def claim_degerini_ac(deger: Any) -> Any:
    if isinstance(deger, dict):
        if "deger" in deger:
            return deger["deger"]
        if "var" in deger:
            return deger["var"]
    return deger


def kosul_durumu(tanim: SomutKosulTanimi, deger: Any, *, kullanilabilir: bool) -> KosulDurumu:
    if not kullanilabilir:
        return KosulDurumu.DEGERLENDIRILEMIYOR
    gercek = claim_degerini_ac(deger)
    if tanim.karsilastirma is Karsilastirma.ESITTIR:
        return KosulDurumu.UYGUN if gercek == tanim.beklenen_deger else KosulDurumu.UYGUN_DEGIL
    return KosulDurumu.DEGERLENDIRILEMIYOR
