"""Disposable PostgreSQL testleri icin parola sizdirmayan admin URL secimi."""

from __future__ import annotations

import os

from sqlalchemy.engine import URL, make_url
from sunucu.veritabani.baglanti import VARSAYILAN_VERITABANI_URL


def admin_url_adaylari() -> list[URL]:
    """Explicit test adminini, sonra CI turetimini ve yerel fallback'i dondurur."""
    explicit = os.environ.get("TEST_ADMIN_VERITABANI_URL")
    if explicit:
        return [make_url(explicit)]

    uygulama_url = make_url(os.environ.get("VERITABANI_URL", VARSAYILAN_VERITABANI_URL))
    turetilen = uygulama_url.set(database="postgres")
    yerel_fallback = URL.create(
        drivername=uygulama_url.drivername,
        username="postgres",
        host=uygulama_url.host or "localhost",
        port=uygulama_url.port or 5432,
        database="postgres",
    )
    return [turetilen] if turetilen == yerel_fallback else [turetilen, yerel_fallback]
