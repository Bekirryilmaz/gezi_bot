"""Alembic autogenerate icin dar kapsamli sistem nesnesi filtreleri."""

from __future__ import annotations

from typing import Any

POSTGIS_SISTEM_TABLOLARI = frozenset({"spatial_ref_sys"})


def nesneyi_karsilastir(
    nesne: Any,
    ad: str | None,
    tur: str,
    reflected: bool,
    compare_to: Any,
) -> bool:
    """Yalniz PostGIS'in yonettigi bilinen tablolarini autogenerate disinda tutar."""
    del nesne, compare_to
    return not (reflected and tur == "table" and ad in POSTGIS_SISTEM_TABLOLARI)
