"""Ortak metin araçları.

Yer URL slug üretimi. `veri/ortak/metin_araclari.py` ile karıştırılmaz:
oradaki `bolge_slug` Türkçe karakterli + alt çizgilidir ve yer URL'i değildir.
Bu modül `veri/` paketine bağımlı değildir.
"""

from __future__ import annotations

import re
import unicodedata

# Türkçe'ye özgü dönüşümler (NFKD'den önce uygulanır).
_TR_HARITA = str.maketrans(
    {
        "ş": "s",
        "Ş": "S",
        "ı": "i",
        "I": "I",
        "İ": "i",  # İ → i (combining dot üretmemek için NFKD'den önce)
        "ğ": "g",
        "Ğ": "G",
        "ü": "u",
        "Ü": "U",
        "ö": "o",
        "Ö": "O",
        "ç": "c",
        "Ç": "C",
    }
)

_GECERSIZ_RE = re.compile(r"[^a-z0-9]+")
_TIRE_RE = re.compile(r"-{2,}")

MAKS_UZUNLUK = 60
BOS_SLUG = "yer"


def slug_uret(ad: str) -> str:
    """Yer adından URL slug üretir.

    Kurallar: İ→i sonra lower; ş/ı/ğ/ü/ö/ç ASCII'ye; yalnız [a-z0-9-];
    boşluk ve diğerleri `-`; tekrar `-` tekle; kenar kırp; en çok 60
    karakter; boş kalırsa ``yer``.

    Çakışma eki (-2, -3) bu fonksiyonda YOKTUR; benzersizlik aktarım
    katmanında sağlanır.
    """
    if not ad:
        return BOS_SLUG
    metin = ad.translate(_TR_HARITA)
    metin = unicodedata.normalize("NFKD", metin)
    metin = "".join(c for c in metin if not unicodedata.combining(c))
    metin = metin.lower()
    metin = _GECERSIZ_RE.sub("-", metin)
    metin = _TIRE_RE.sub("-", metin).strip("-")
    metin = metin[:MAKS_UZUNLUK].rstrip("-")
    return metin or BOS_SLUG
