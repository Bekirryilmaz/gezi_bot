"""OSM opening_hours sozdizimini muhafazakar ayristirir; tahmin etmez."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from ortak.sabitler import CalismaSaatiDurumu

AYRISTIRICI_SURUMU = "v2"
VARSAYILAN_ZAMAN_DILIMI = "Europe/Istanbul"
TAZE_GUN_SINIRI = 180
GUN_SIRASI = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")
_GUN_INDEKS = {gun: indeks for indeks, gun in enumerate(GUN_SIRASI)}
_GUN = r"(?:Mo|Tu|We|Th|Fr|Sa|Su)"
_SAAT = r"(?:[01]\d|2[0-3]|24):[0-5]\d"
_KARMASIK = re.compile(
    r"\b(?:PH|SH|sunrise|sunset|dawn|dusk|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
    re.IGNORECASE,
)
_YORUM = re.compile(r'["“”]|open until|by appointment|on appointment|summer', re.IGNORECASE)


@dataclass(frozen=True)
class CalismaSaatiAyristirma:
    ham: str
    sozdizimi_gecerli: bool
    normalize: str | None
    her_zaman_acik: bool
    haftalik: dict[str, tuple[tuple[str, str], ...]]
    neden: str
    durum: CalismaSaatiDurumu
    parser_surumu: str = AYRISTIRICI_SURUMU

    @property
    def acik_iddiasi_kurulabilir(self) -> bool:
        return self.durum is CalismaSaatiDurumu.KNOWN

    def sozluk(self) -> dict[str, Any]:
        return {
            "ham": self.ham,
            "sozdizimi_gecerli": self.sozdizimi_gecerli,
            "normalize": self.normalize,
            "her_zaman_acik": self.her_zaman_acik,
            "haftalik": {
                gun: [list(aralik) for aralik in araliklar]
                for gun, araliklar in self.haftalik.items()
            },
            "neden": self.neden,
            "durum": self.durum.value,
            "parser_surumu": self.parser_surumu,
            "acik_iddiasi_kurulabilir": self.acik_iddiasi_kurulabilir,
        }


@dataclass(frozen=True)
class CalismaSaatiKaydi:
    ayristirma: CalismaSaatiAyristirma
    durum: CalismaSaatiDurumu
    kaynak: str
    gozlemlenme_zamani: datetime | None
    cekilme_zamani: datetime | None
    parser_surumu: str
    ham_referans: str | None
    zaman_dilimi: str
    gecerlilik_bitisi: datetime | None

    @property
    def acik_iddiasi_kurulabilir(self) -> bool:
        return self.durum is CalismaSaatiDurumu.KNOWN

    def sozluk(self) -> dict[str, Any]:
        govde = self.ayristirma.sozluk()
        govde.update(
            {
                "durum": self.durum.value,
                "kaynak": self.kaynak,
                "gozlemlenme_zamani": (
                    self.gozlemlenme_zamani.isoformat() if self.gozlemlenme_zamani else None
                ),
                "cekilme_zamani": self.cekilme_zamani.isoformat() if self.cekilme_zamani else None,
                "parser_surumu": self.parser_surumu,
                "ham_referans": self.ham_referans,
                "zaman_dilimi": self.zaman_dilimi,
                "gecerlilik_bitisi": (
                    self.gecerlilik_bitisi.isoformat() if self.gecerlilik_bitisi else None
                ),
                "acik_iddiasi_kurulabilir": self.acik_iddiasi_kurulabilir,
            }
        )
        return govde


def _sonuc(
    *,
    ham: str,
    sozdizimi_gecerli: bool,
    normalize: str | None,
    her_zaman_acik: bool,
    haftalik: dict[str, tuple[tuple[str, str], ...]],
    neden: str,
    durum: CalismaSaatiDurumu,
) -> CalismaSaatiAyristirma:
    return CalismaSaatiAyristirma(
        ham=ham,
        sozdizimi_gecerli=sozdizimi_gecerli,
        normalize=normalize,
        her_zaman_acik=her_zaman_acik,
        haftalik=haftalik,
        neden=neden,
        durum=durum,
        parser_surumu=AYRISTIRICI_SURUMU,
    )


def _bos(neden: str, ham: str, durum: CalismaSaatiDurumu) -> CalismaSaatiAyristirma:
    return _sonuc(
        ham=ham,
        sozdizimi_gecerli=False,
        normalize=None,
        her_zaman_acik=False,
        haftalik={},
        neden=neden,
        durum=durum,
    )


def _dakika(saat: str) -> int:
    saat_parca, dakika_parca = saat.split(":")
    return int(saat_parca) * 60 + int(dakika_parca)


def _gun_araligi(bas: str, bit: str) -> tuple[int, ...] | None:
    bas_i = _GUN_INDEKS[bas]
    bit_i = _GUN_INDEKS[bit]
    if bas_i <= bit_i:
        return tuple(range(bas_i, bit_i + 1))
    return None


def _gunleri_coz(ifade: str) -> tuple[int, ...] | None:
    gunler: list[int] = []
    for parca in ifade.split(","):
        parca = parca.strip()
        if not parca:
            return None
        if "-" in parca:
            bas, bit = (p.strip() for p in parca.split("-", 1))
            if bas not in _GUN_INDEKS or bit not in _GUN_INDEKS:
                return None
            aralik = _gun_araligi(bas, bit)
            if aralik is None:
                return None
            gunler.extend(aralik)
        else:
            if parca not in _GUN_INDEKS:
                return None
            gunler.append(_GUN_INDEKS[parca])
    if not gunler:
        return None
    return tuple(dict.fromkeys(gunler))


def _saat_araliklari(ifade: str) -> tuple[tuple[str, str], ...] | None:
    araliklar: list[tuple[str, str]] = []
    for parca in ifade.split(","):
        parca = parca.strip()
        eslesme = re.fullmatch(rf"({_SAAT})-({_SAAT})", parca)
        if eslesme is None:
            return None
        bas, bit = eslesme.group(1), eslesme.group(2)
        if bit != "24:00" and _dakika(bit) <= _dakika(bas):
            return None
        if bas == "24:00":
            return None
        araliklar.append((bas, bit))
    return tuple(araliklar)


def _kural_karmasik_mi(kural: str) -> bool:
    return bool(_YORUM.search(kural) or _KARMASIK.search(kural) or "(" in kural or "[" in kural)


def _kurali_uygula(
    kural: str, haftalik: dict[str, list[tuple[str, str]]]
) -> str | None:
    if kural == "off":
        return "belirsiz_off"
    parcalar = kural.split(" ", 1)
    if len(parcalar) != 2:
        return "gun_veya_saat_eksik"
    gun_ifade, saat_ifade = parcalar
    gunler = _gunleri_coz(gun_ifade)
    if gunler is None:
        return "gecersiz_gun"
    if saat_ifade == "off":
        for indeks in gunler:
            haftalik[GUN_SIRASI[indeks]] = []
        return None
    araliklar = _saat_araliklari(saat_ifade)
    if araliklar is None:
        return "gecersiz_saat_araligi"
    for indeks in gunler:
        haftalik[GUN_SIRASI[indeks]] = list(araliklar)
    return None


def calisma_saatini_ayristir(ham: str | None) -> CalismaSaatiAyristirma:
    metin = re.sub(r"[\u2013\u2014]", "-", (ham or "").strip())
    metin = re.sub(r"\s+", " ", metin)
    if not metin:
        return _bos("bos", "", CalismaSaatiDurumu.UNKNOWN)
    if metin == "24/7":
        aralik = (("00:00", "24:00"),)
        return _sonuc(
            ham=metin,
            sozdizimi_gecerli=True,
            normalize="24/7",
            her_zaman_acik=True,
            haftalik={gun: aralik for gun in GUN_SIRASI},
            neden="gecerli",
            durum=CalismaSaatiDurumu.KNOWN,
        )
    if metin in {"off", "closed"}:
        return _sonuc(
            ham=metin,
            sozdizimi_gecerli=True,
            normalize=metin,
            her_zaman_acik=False,
            haftalik={gun: () for gun in GUN_SIRASI},
            neden="surekli_kapali",
            durum=CalismaSaatiDurumu.KNOWN,
        )

    haftalik: dict[str, list[tuple[str, str]]] = {gun: [] for gun in GUN_SIRASI}
    kurallar: list[str] = []
    atlanan: list[str] = []
    hatali: list[str] = []
    for kural in metin.split(";"):
        kural = kural.strip()
        if not kural:
            return _bos("bos_kural", metin, CalismaSaatiDurumu.INVALID)
        if _kural_karmasik_mi(kural):
            atlanan.append(kural)
            continue
        hata = _kurali_uygula(kural, haftalik)
        if hata:
            hatali.append(hata)
            continue
        kurallar.append(kural)

    if kurallar and not hatali and not atlanan:
        return _sonuc(
            ham=metin,
            sozdizimi_gecerli=True,
            normalize="; ".join(kurallar),
            her_zaman_acik=False,
            haftalik={gun: tuple(araliklar) for gun, araliklar in haftalik.items()},
            neden="gecerli",
            durum=CalismaSaatiDurumu.KNOWN,
        )
    if kurallar and atlanan and not hatali:
        ph_var = any("ph" in parca.lower() for parca in atlanan)
        neden = "kismi_ph_atlandi" if ph_var else "kismi_kural_atlandi"
        return _sonuc(
            ham=metin,
            sozdizimi_gecerli=True,
            normalize="; ".join(kurallar),
            her_zaman_acik=False,
            haftalik={gun: tuple(araliklar) for gun, araliklar in haftalik.items()},
            neden=neden,
            durum=CalismaSaatiDurumu.PARTIALLY_KNOWN,
        )
    if hatali:
        return _bos(hatali[0], metin, CalismaSaatiDurumu.INVALID)
    if atlanan:
        return _bos("karmasik_sozdizimi", metin, CalismaSaatiDurumu.INVALID)
    return _bos("gecersiz", metin, CalismaSaatiDurumu.INVALID)


def calisma_saati_degerini_al(deger: Any) -> str | None:
    if deger is None:
        return None
    if isinstance(deger, str):
        return deger
    if isinstance(deger, dict):
        ham = deger.get("deger") or deger.get("ham") or deger.get("opening_hours")
        return str(ham) if ham else None
    return str(deger)


def calisma_saati_kaydini_kur(
    *,
    ham: str | None,
    kaynak: str,
    gozlemlenme_zamani: datetime | None = None,
    cekilme_zamani: datetime | None = None,
    ham_referans: str | None = None,
    zaman_dilimi: str | None = None,
    simdi: datetime | None = None,
) -> CalismaSaatiKaydi:
    ayristirma = calisma_saatini_ayristir(ham)
    durum = ayristirma.durum
    an = simdi or datetime.now(UTC)
    gozlem = gozlemlenme_zamani or cekilme_zamani
    gecerlilik = None
    if gozlem is not None:
        gecerlilik = gozlem + timedelta(days=TAZE_GUN_SINIRI)
        if durum in {CalismaSaatiDurumu.KNOWN, CalismaSaatiDurumu.PARTIALLY_KNOWN}:
            if an - gozlem > timedelta(days=TAZE_GUN_SINIRI):
                durum = CalismaSaatiDurumu.STALE
    return CalismaSaatiKaydi(
        ayristirma=ayristirma,
        durum=durum,
        kaynak=kaynak,
        gozlemlenme_zamani=gozlemlenme_zamani,
        cekilme_zamani=cekilme_zamani,
        parser_surumu=AYRISTIRICI_SURUMU,
        ham_referans=ham_referans,
        zaman_dilimi=zaman_dilimi or VARSAYILAN_ZAMAN_DILIMI,
        gecerlilik_bitisi=gecerlilik,
    )
