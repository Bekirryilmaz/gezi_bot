from __future__ import annotations

import re
import unicodedata

_TURKCE_CEVIRI = str.maketrans(
    {"Ç": "C", "Ğ": "G", "İ": "I", "I": "I", "Ö": "O", "Ş": "S", "Ü": "U",
     "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u"}
)
_AYIRICI = re.compile(r"[^a-z0-9]+")


def turkce_arama_normalize(metin: str | None) -> str:
    """SQL'deki samandira_arama_normalize ile ayni, aciklanabilir donusum."""
    if not metin:
        return ""
    ascii_yakin = unicodedata.normalize("NFKD", metin.translate(_TURKCE_CEVIRI))
    ascii_yakin = "".join(harf for harf in ascii_yakin if not unicodedata.combining(harf))
    return _AYIRICI.sub(" ", ascii_yakin.lower()).strip()


def baglam_tokenini_cikar(sorgu: str, token: str) -> str:
    """Yalniz tam kelime/ifade sinirindaki sehir-ilce tokenini kaldirir."""
    if not token:
        return sorgu
    parcalar = sorgu.split()
    token_parcalari = token.split()
    uzunluk = len(token_parcalari)
    for baslangic in range(len(parcalar) - uzunluk + 1):
        if parcalar[baslangic : baslangic + uzunluk] == token_parcalari:
            return " ".join(parcalar[:baslangic] + parcalar[baslangic + uzunluk :]).strip()
    return sorgu
