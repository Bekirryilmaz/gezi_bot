from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from ortak.sabitler import (
    DAHILI_SINYAL_DEGER_SOZLUGU,
    AdaySozlesmeSurumu,
    CikarimYontemi,
    DahiliSinyalAilesi,
    GozlemTuru,
    SinyalYonu,
    VeriKaynagi,
    ZamansalDurum,
)
from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

_LEGACY_ZORUNLU_ALANLARI = frozenset(
    {
        "kaynak",
        "yer_adayi",
        "span",
        "konu",
        "tahmini_gozlem",
        "model_surumu",
        "cikarim_guven_sinifi",
    }
)
_LEGACY_ALANLARI = _LEGACY_ZORUNLU_ALANLARI | {
    "kaynak_kayit_id",
    "sube_adayi",
    "zaman_kapsami",
    "inceleme_durumu",
    "olusturulma_zamani",
}
_CANONICAL_IZ_ALANLARI = frozenset(
    {
        "aile",
        "yon",
        "deger",
        "gozlem_turu",
        "yorum_parmak_izi",
        "zamansal_durum",
        "cikarim_yontemi",
        "kural_surumu",
        "guven_kirilimi",
        "span_hash",
        "dahili_referans",
    }
)


class CikarimGuvenSinifi(StrEnum):
    DUSUK = "dusuk"
    ORTA = "orta"
    YUKSEK = "yuksek"


class IncelemeDurumu(StrEnum):
    BEKLIYOR = "bekliyor"
    INCELEMEDE = "incelemede"
    KABUL = "kabul"
    RED = "red"


class AdayGozlem(BaseModel):
    """NLP'nin tek ciktisi; kanit, claim, yayin veya uygunluk degildir."""
    model_config = ConfigDict(extra="forbid")

    kaynak: VeriKaynagi
    sozlesme_surumu: AdaySozlesmeSurumu = AdaySozlesmeSurumu.CANONICAL_V1
    kaynak_kayit_id: str | None = None
    yorum_parmak_izi: str | None = None
    yer_adayi: str = Field(description="Kaynak yer kimligi veya eslesme adayi")
    sube_adayi: str | None = None
    span: str = Field(description="Cikarimin baglandigi sinirli kaynak parcasi")
    konu: str
    aile: DahiliSinyalAilesi | str | None = None
    yon: SinyalYonu | None = None
    deger: Any = None
    gozlem_turu: GozlemTuru | None = None
    tahmini_gozlem: dict[str, Any]
    zaman_kapsami: dict[str, Any] = Field(default_factory=dict)
    zamansal_durum: ZamansalDurum = ZamansalDurum.UNKNOWN
    cikarim_yontemi: CikarimYontemi = CikarimYontemi.GERIYE_UYUMLU
    model_surumu: str
    kural_surumu: str | None = None
    cikarim_guven_sinifi: CikarimGuvenSinifi
    guven_kirilimi: dict[str, Any] = Field(default_factory=dict)
    span_hash: str | None = None
    dahili_referans: str | None = None
    inceleme_durumu: IncelemeDurumu = IncelemeDurumu.BEKLIYOR
    olusturulma_zamani: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="before")
    @classmethod
    def exact_tarihi_shapei_tani(cls, veri: Any) -> Any:
        """Yalniz exact tarihi alan kumesini legacy parse yoluna alir."""
        if not isinstance(veri, Mapping):
            return veri
        alanlar = set(veri)
        serialize_legacy_alanlari = set(cls.model_fields) | {
            "otomatik_yayinlanabilir"
        }
        serialize_legacy = (
            veri.get("sozlesme_surumu")
            in {AdaySozlesmeSurumu.LEGACY, AdaySozlesmeSurumu.LEGACY.value}
            and alanlar == serialize_legacy_alanlari
            and veri.get("otomatik_yayinlanabilir") is False
            and veri.get("cikarim_yontemi")
            in {CikarimYontemi.GERIYE_UYUMLU, CikarimYontemi.GERIYE_UYUMLU.value}
        )
        if serialize_legacy:
            temiz_veri = dict(veri)
            temiz_veri.pop("otomatik_yayinlanabilir")
            return temiz_veri
        canonical_iz_var = bool(alanlar & _CANONICAL_IZ_ALANLARI)
        if canonical_iz_var:
            if veri.get("sozlesme_surumu") in {
                AdaySozlesmeSurumu.LEGACY,
                AdaySozlesmeSurumu.LEGACY.value,
            }:
                return {
                    **veri,
                    "sozlesme_surumu": AdaySozlesmeSurumu.CANONICAL_V1,
                }
            return veri
        if "sozlesme_surumu" in veri:
            return veri
        exact_legacy_shape = (
            _LEGACY_ZORUNLU_ALANLARI <= alanlar <= _LEGACY_ALANLARI
        )
        if exact_legacy_shape:
            return {**veri, "sozlesme_surumu": AdaySozlesmeSurumu.LEGACY}
        return veri

    @model_validator(mode="after")
    def acik_sozlesmeyi_tamamla(self) -> AdayGozlem:
        """Eski payloadlari kaybetmeden yeni acik alanlari doldurur."""
        if self.sozlesme_surumu is AdaySozlesmeSurumu.LEGACY:
            self._legacy_sozlesmeyi_tamamla()
        else:
            gerekli_alanlar = {
                "aile",
                "yon",
                "deger",
                "gozlem_turu",
                "cikarim_yontemi",
                "kural_surumu",
                "guven_kirilimi",
            }
            eksik_alanlar = gerekli_alanlar - self.model_fields_set
            if eksik_alanlar:
                eksikler = ", ".join(sorted(eksik_alanlar))
                raise ValueError(f"canonical aday alanlari explicit olmalidir: {eksikler}")
            if not self.kaynak_kayit_id and not self.yorum_parmak_izi:
                raise ValueError(
                    "canonical aday kaynak_kayit_id veya yorum_parmak_izi tasimalidir"
                )
            if self.yorum_parmak_izi:
                try:
                    parmak_izi_gecerli = (
                        len(self.yorum_parmak_izi) == 64
                        and int(self.yorum_parmak_izi, 16) >= 0
                    )
                except ValueError:
                    parmak_izi_gecerli = False
                if not parmak_izi_gecerli:
                    raise ValueError("yorum_parmak_izi sha256 olmali")
            self._canonical_sozlesmeyi_dogrula()
        if self.kural_surumu is None:
            self.kural_surumu = self.model_surumu
        if not self.guven_kirilimi:
            self.guven_kirilimi = {
                "sinif": self.cikarim_guven_sinifi.value,
                "genel_bert_kullanildi": self.cikarim_yontemi
                is CikarimYontemi.DUYGU_MODELI,
            }
        self.span_hash = hashlib.sha256(self.span.encode("utf-8")).hexdigest()
        if self.kaynak_kayit_id:
            yorum_kimligi = f"kayit:{self.kaynak_kayit_id}"
        elif self.yorum_parmak_izi:
            yorum_kimligi = f"parmak-izi:{self.yorum_parmak_izi}"
        else:
            yorum_kimligi = f"legacy:{self.yer_adayi}:{self.span_hash}"
        referans_bilesenleri = {
            "kaynak": self.kaynak.value,
            "yorum_kimligi": yorum_kimligi,
            "kaynak_yer": self.yer_adayi,
            "sube": self.sube_adayi,
            "aile": str(self.aile),
            "gozlem_turu": self.gozlem_turu.value,
            "yon": self.yon.value if self.yon else None,
            "span_hash": self.span_hash,
            "model_surumu": self.model_surumu,
            "kural_surumu": self.kural_surumu,
        }
        referans_ham = json.dumps(
            referans_bilesenleri,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        referans_hash = hashlib.sha256(referans_ham.encode("utf-8")).hexdigest()
        self.dahili_referans = f"aday:{referans_hash}"
        return self

    def _legacy_sozlesmeyi_tamamla(self) -> None:
        if self.aile is None:
            self.aile = self.konu
        tahmini_yon = self.tahmini_gozlem.get("yon")
        if self.yon is None and tahmini_yon:
            self.yon = {
                "destek": SinyalYonu.SUPPORT,
                "karsi": SinyalYonu.COUNTER,
                "support": SinyalYonu.SUPPORT,
                "counter": SinyalYonu.COUNTER,
            }.get(str(tahmini_yon))
        if self.deger is None and "deger" in self.tahmini_gozlem:
            self.deger = self.tahmini_gozlem["deger"]
        if self.gozlem_turu is None:
            bilgi_turu = self.tahmini_gozlem.get("bilgi_turu")
            self.gozlem_turu = (
                GozlemTuru.FACT_SIGNAL
                if bilgi_turu == "yapisal_sinyal_adayi" or self.yon is not None
                else GozlemTuru.SENTIMENT_SIGNAL
            )

    def _canonical_sozlesmeyi_dogrula(self) -> None:
        self.aile = DahiliSinyalAilesi(self.aile)
        if self.konu != self.aile.value:
            raise ValueError("konu canonical aile ile ayni olmalidir")
        if self.yon is None or self.gozlem_turu is None or self.deger is None:
            raise ValueError("canonical aday yon, gozlem_turu ve deger tasimalidir")
        tahmini_yon = self.tahmini_gozlem.get("yon")
        if tahmini_yon is not None:
            beklenen_yon = "destek" if self.yon is SinyalYonu.SUPPORT else "karsi"
            if tahmini_yon not in {self.yon.value, beklenen_yon}:
                raise ValueError("tahmini_gozlem yonu canonical yon ile celisiyor")
        if "deger" in self.tahmini_gozlem and self.tahmini_gozlem["deger"] != self.deger:
            raise ValueError("tahmini_gozlem degeri canonical deger ile celisiyor")
        if not isinstance(self.deger, (bool, str)):
            raise ValueError("canonical deger boolean veya sinirli string olmalidir")
        anahtar = (self.aile.value, self.gozlem_turu.value, self.yon.value)
        izinli_degerler = DAHILI_SINYAL_DEGER_SOZLUGU.get(anahtar, ())
        if self.deger not in izinli_degerler:
            raise ValueError("aile, gozlem_turu, yon ve deger kombinasyonu gecersiz")

    def kalici_payload(self, *, ham_icerik_saklanabilir: bool) -> dict[str, Any]:
        """Kaynak saklama hakkina gore kalici JSONL payloadi uretir."""
        payload = self.model_dump(mode="json")
        if not ham_icerik_saklanabilir:
            payload.pop("span", None)
        payload.pop("yazar_takma_adi", None)
        return payload

    @computed_field(return_type=bool)
    @property
    def otomatik_yayinlanabilir(self) -> bool:
        return False
