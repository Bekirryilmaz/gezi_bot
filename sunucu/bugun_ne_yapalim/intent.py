"""Turkce serbest metni aciklanabilir karar niyetine ayirir.

Bu modul mekan secmez, claim uretmez ve Karar Motorunu gecmez. Yalniz
kullanicinin soyledigi katmanlari cikartir; soylenmeyen sifatlari turetmez.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from sunucu.arama.normalizasyon import turkce_arama_normalize

AMAC_ETIKETLERI = {
    "kahve_icmek": "kahve içmek",
    "yemek_yemek": "yemek yemek",
    "tatli_yemek": "tatlı yemek",
    "kahvalti_yapmak": "kahvaltı yapmak",
    "eglence": "eğlenmek",
    "gezme": "gezmek",
    "tarihi_kulturel_ziyaret": "tarih-kültür gezisi",
    "acik_hava": "açık havada vakit geçirmek",
    "calisma": "çalışmak",
    "birlikte_vakit": "birlikte vakit geçirmek",
    "aileyle_vakit": "ailece vakit geçirmek",
    "cocukla_aktivite": "çocuklarla bir şey yapmak",
}

AMAC_SORGULARI = {
    "kahve_icmek": "kafe",
    "yemek_yemek": "yeme içme",
    "tatli_yemek": "tatlı pastane",
    "kahvalti_yapmak": "kahvaltı",
    "eglence": "eğlence aktivite",
    "gezme": "gezilecek yer",
    "tarihi_kulturel_ziyaret": "tarih ve kültür",
    "acik_hava": "doğa manzara",
    "calisma": "kafe",
    "birlikte_vakit": "kafe",
    "aileyle_vakit": "gezilecek yer",
    "cocukla_aktivite": "eğlence aktivite",
}

# Bugunku yayimli amac_destegi sozlesmesinde gercekten bulunan degerler.
KARARDA_DESTEKLENEN_AMACLAR = {
    "kahve_icmek",
    "yemek_yemek",
    "tarihi_kulturel_ziyaret",
}


@dataclass(frozen=True)
class DesenGrubu:
    kod: str
    desenler: tuple[str, ...]


KISI_DESENLERI = (
    DesenGrubu(
        "partner",
        (
            r"\bsevgili(?:m)?le\b",
            r"\bsevgiliyle\b",
            r"\besimle\b",
            r"\bes ile\b",
            r"\bpartner(?:im)?le\b",
        ),
    ),
    DesenGrubu("aile", (r"\bailemle\b", r"\bailemi\b", r"\bailecek\b", r"\baileyle\b")),
    DesenGrubu(
        "arkadaslar", (r"\barkadas(?:lar)?la\b", r"\barkadaslarla\b", r"\barkadas grubuyla\b")
    ),
    DesenGrubu(
        "cocuklar",
        (r"\bcocuk(?:lar)?la\b", r"\bcocuklarla\b", r"\bcocugumla\b", r"\bcocuklarala\b"),
    ),
    DesenGrubu("yalniz", (r"\btek basima\b", r"\byalniz\b", r"\bkendi basima\b")),
)

AMAC_DESENLERI = (
    DesenGrubu("kahvalti_yapmak", (r"\bkahvalti", r"\bbrunch\b")),
    DesenGrubu("tatli_yemek", (r"\btatli(?:ci)?", r"\bpasta(?:ne)?", r"\bdondurma")),
    DesenGrubu("kahve_icmek", (r"\bkahve(?:ci)?", r"\bkafe\b", r"\bcafe\b")),
    DesenGrubu(
        "yemek_yemek",
        (
            r"\byemek",
            r"\byemege\b",
            r"\byemegi\b",
            r"\brestoran",
            r"\blokanta",
            r"\bkarn(?:im|imiz)? ac",
            r"\baciktik\b",
        ),
    ),
    DesenGrubu(
        "tarihi_kulturel_ziyaret",
        (r"\bmuze", r"\bmusee\b", r"\btarihi", r"\bkulturel", r"\banit\b"),
    ),
    DesenGrubu(
        "calisma",
        (
            r"\blaptop",
            r"\bders calis",
            r"\bcalismalik",
            r"\bcalisacag",
            r"\bcalisicam",
            r"\bcalisaca",
        ),
    ),
    DesenGrubu(
        "cocukla_aktivite", (r"\bcocu(?:k|g).*?(?:gide|cik|oyna|park|aktivite)", r"\boyun alani")
    ),
    DesenGrubu("acik_hava", (r"\bacik hava", r"\bparkta\b", r"\bsahil(?:de|e)\b", r"\bpiknik")),
    DesenGrubu("eglence", (r"\beglen", r"\baktivite", r"\bcanli muzi", r"\boyun oyn")),
    DesenGrubu("gezme", (r"\bgez", r"\bdolas", r"\btur at", r"\byuruyus")),
    DesenGrubu(
        "birlikte_vakit", (r"\btakil", r"\botur(?:mak|alim|acag|ucaz|malik)", r"\bvakit gecir")
    ),
)

AKTIVITE_DESENLERI = (
    DesenGrubu("sohbet", (r"\bsohbet", r"\bmuhabbet")),
    DesenGrubu("oturmak", (r"\botur(?:mak|alim|acag|ucaz|malik)",)),
    DesenGrubu("dolasmak", (r"\bdolas", r"\bgez")),
    DesenGrubu("canli_muzik", (r"\bcanli muzi",)),
)

TERCIH_DESENLERI = (
    DesenGrubu(
        "sessiz_ortam", (r"\bsakin", r"\bsessiz", r"\bgurultu olmasin", r"\bkalabalik olmasin")
    ),
    DesenGrubu("manzara", (r"\bmanzara", r"\bdeniz gor", r"\bseyir")),
    DesenGrubu(
        "uygun_fiyat",
        (r"\bucuz", r"\buygun fiyat", r"\bpahali (?:olmasin|.*istemiyorum)", r"\bbutce dostu"),
    ),
    DesenGrubu("yakinda", (r"\byakin", r"\buzak olmasin", r"\byurumelik")),
    DesenGrubu("aile_uygunlugu", (r"\bailece .*yer", r"\baile(?:m|miz)? icin uygun")),
    DesenGrubu("cocuk_uygunlugu", (r"\bcocuk.*uygun", r"\bcocuklarla gide", r"\bcocukla gidil")),
    DesenGrubu("calisma_uygunlugu", (r"\bcalismalik", r"\blaptop", r"\bders calis")),
    DesenGrubu("acik_hava", (r"\bacik hava", r"\bbahce", r"\bteras")),
    DesenGrubu("canli_muzik", (r"\bcanli muzi",)),
    DesenGrubu("rezervasyon", (r"\brezervasyon",)),
)

ZORUNLULUK = re.compile(r"\b(kesin|sart|zorunlu|mutlaka|olmazsa olmaz)\b")


def _bul(metin: str, gruplar: Iterable[DesenGrubu]) -> list[str]:
    return [g.kod for g in gruplar if any(re.search(d, metin) for d in g.desenler)]


def _negatif_baglamda(metin: str, anahtar: str) -> bool:
    """Bir olanagin yoklugunu olumlu tercih/constraint olarak isaretleme."""
    return bool(
        re.search(rf"\b{anahtar}\b.{{0,18}}\b(yok|olmasin|cekmi(?:yor|yo)|bulunmuyor)\b", metin)
    )


def amaclari_onceliklendir(
    bulunan: list[str], kisi: str | None
) -> tuple[str | None, tuple[str, ...]]:
    if not bulunan:
        if kisi == "cocuklar":
            return "cocukla_aktivite", ()
        return None, ()
    # Somut tuketim/ziyaret fiili, genel vakit gecirme fiilinden once gelir.
    oncelik = [
        "kahvalti_yapmak",
        "tatli_yemek",
        "calisma",
        "cocukla_aktivite",
        "kahve_icmek",
        "yemek_yemek",
        "tarihi_kulturel_ziyaret",
        "acik_hava",
        "eglence",
        "gezme",
        "birlikte_vakit",
    ]
    sirali = [kod for kod in oncelik if kod in bulunan]
    return sirali[0], tuple(sirali[1:])


def metni_coz(metin: str) -> dict[str, object]:
    normal = turkce_arama_normalize(metin)
    kisiler = _bul(normal, KISI_DESENLERI)
    kisi = kisiler[0] if len(kisiler) == 1 else None
    ana_amac, alt_amaclar = amaclari_onceliklendir(_bul(normal, AMAC_DESENLERI), kisi)
    aktiviteler = tuple(_bul(normal, AKTIVITE_DESENLERI))
    tercihler = _bul(normal, TERCIH_DESENLERI)
    zorunlu: list[str] = []
    desteklenmeyen: list[str] = []
    for kod, anahtarlar in (
        ("wifi", ("wifi", "wi fi", "internet")),
        ("otopark", ("otopark", "park yeri")),
    ):
        gecen = next((a for a in anahtarlar if a in normal), None)
        if not gecen or _negatif_baglamda(normal, re.escape(gecen)):
            continue
        pencere = normal[max(0, normal.find(gecen) - 24) : normal.find(gecen) + len(gecen) + 24]
        (zorunlu if ZORUNLULUK.search(pencere) else tercihler).append(kod)
    for kod in tuple(tercihler):
        if kod not in {"wifi", "otopark", "sessiz_ortam"}:
            desteklenmeyen.append(kod)
    if ana_amac and ana_amac not in KARARDA_DESTEKLENEN_AMACLAR:
        desteklenmeyen.append(ana_amac)
    if "sohbet" in aktiviteler:
        desteklenmeyen.append("sohbet_uygunlugu")
    if kisi == "cocuklar":
        desteklenmeyen.append("cocuk_uygunlugu")
    if kisi == "aile":
        desteklenmeyen.append("aile_uygunlugu")
    # Museum is a literal requested subtype, not interchangeable with all history venues.
    if re.search(r"\b(?:muze|musee)", normal):
        desteklenmeyen.append("muze_turu")
        if ana_amac == "tarihi_kulturel_ziyaret":
            zorunlu.append("muze_turu")
    return {
        "ham_input": metin,
        "normalize_edilmis_input": normal,
        "kisi_baglami": kisi,
        "ana_amac": ana_amac,
        "alt_amaclar": alt_amaclar,
        "aktiviteler": aktiviteler,
        "ziyaret_baglamlari": (
            ("birlikte_vakit",) if kisi in {"partner", "arkadaslar", "aile"} else ()
        ),
        "tercihler": tuple(dict.fromkeys(tercihler)),
        "zorunlu_kosullar": tuple(dict.fromkeys(zorunlu)),
        "desteklenmeyen_istekler": tuple(dict.fromkeys(desteklenmeyen)),
        "celisen_niyet": len(kisiler) > 1,
    }
