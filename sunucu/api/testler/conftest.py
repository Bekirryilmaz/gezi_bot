from __future__ import annotations

import pytest

from sunucu.api.altyapi import ApiGuvenlikMiddleware
from sunucu.api.uygulama import uygulama


def _yazma_sayacini_sifirla() -> None:
    katman = uygulama.middleware_stack
    while katman is not None:
        if isinstance(katman, ApiGuvenlikMiddleware):
            katman.yazma_sayacini_sifirla()
            return
        katman = getattr(katman, "app", None)


@pytest.fixture(autouse=True)
def _api_yazma_limiti_sifirla():
    _yazma_sayacini_sifirla()
    yield
    _yazma_sayacini_sifirla()
