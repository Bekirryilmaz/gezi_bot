"""OSM opening_hours sozdizimini muhafazakar ayristirir; tahmin etmez."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

GUN_SIRASI = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")
_GUN_INDEKS = {gun: indeks for indeks, gun in enumerate(GUN_SIRASI)}
_GUN = r"(?:Mo|Tu|We|Th|Fr|Sa|Su)"
_SAAT = r"(?:[01]\d|2[0-3]|24):[0-5]\d"
_KARMASIK = re.compile(
    r"\b(?:PH|SH|sunrise|sunset|dawn|dusk|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
    re.IGNORECASE,
)
_YORUM = re.compile(r'["“”]|open until|by appointment|on appointment', re.IGNORECASE)


@dataclass(frozen=True)
class CalismaSaatiAyristirma:
    ham: str
    sozdizimi_gecerli: bool
    normalize: str | None
    her_zaman_acik: bool
    haftalik: dict[str, tuple[tuple[str, str], ...]]
    neden: str

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
        }


def _bos(neden: str, ham: str) -> CalismaSaatiAyristirma:
    return CalismaSaatiAyristirma(ham, False, None, False, {}, neden)


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


def calisma_saatini_ayristir(ham: str | None) -> CalismaSaatiAyristirma:
    metin = re.sub(r"[\u2013\u2014]", "-", (ham or "").strip())
    metin = re.sub(r"\s+", " ", metin)
    if not metin:
        return _bos("bos", "")
    if _YORUM.search(metin) or _KARMASIK.search(metin) or "(" in metin or "[" in metin:
        return _bos("karmasik_sozdizimi", metin)
    if metin == "24/7":
        aralik = (("00:00", "24:00"),)
        return CalismaSaatiAyristirma(
            ham=metin,
            sozdizimi_gecerli=True,
            normalize="24/7",
            her_zaman_acik=True,
            haftalik={gun: aralik for gun in GUN_SIRASI},
            neden="gecerli",
        )
    if metin == "off":
        return CalismaSaatiAyristirma(
            metin, True, "off", False, {gun: () for gun in GUN_SIRASI}, "gecerli"
        )

    haftalik: dict[str, list[tuple[str, str]]] = {gun: [] for gun in GUN_SIRASI}
    kurallar: list[str] = []
    for kural in metin.split(";"):
        kural = kural.strip()
        if not kural:
            return _bos("bos_kural", metin)
        if kural == "off":
            return _bos("belirsiz_off", metin)
        parcalar = kural.split(" ", 1)
        if len(parcalar) != 2:
            return _bos("gun_veya_saat_eksik", metin)
        gun_ifade, saat_ifade = parcalar
        gunler = _gunleri_coz(gun_ifade)
        if gunler is None:
            return _bos("gecersiz_gun", metin)
        if saat_ifade == "off":
            for indeks in gunler:
                haftalik[GUN_SIRASI[indeks]] = []
            kurallar.append(f"{gun_ifade} off")
            continue
        araliklar = _saat_araliklari(saat_ifade)
        if araliklar is None:
            return _bos("gecersiz_saat_araligi", metin)
        for indeks in gunler:
            haftalik[GUN_SIRASI[indeks]] = list(araliklar)
        kurallar.append(f"{gun_ifade} {saat_ifade}")
    return CalismaSaatiAyristirma(
        ham=metin,
        sozdizimi_gecerli=True,
        normalize="; ".join(kurallar),
        her_zaman_acik=False,
        haftalik={gun: tuple(araliklar) for gun, araliklar in haftalik.items()},
        neden="gecerli",
    )


def calisma_saati_degerini_al(deger: Any) -> str | None:
    if deger is None:
        return None
    if isinstance(deger, str):
        return deger
    if isinstance(deger, dict):
        ham = deger.get("deger") or deger.get("ham") or deger.get("opening_hours")
        return str(ham) if ham else None
    return str(deger)
