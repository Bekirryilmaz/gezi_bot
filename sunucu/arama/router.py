from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from sunucu.arama.semalar import AramaCevabi, AramaFiltreleriCevabi
from sunucu.arama.servis import ara, filtre_katalogunu_getir
from sunucu.veritabani.baglanti import oturum_al

yonlendirici = APIRouter(prefix="/v1/arama", tags=["arama"])


@yonlendirici.get("", response_model=AramaCevabi)
def arama_yap(
    q: str = Query(min_length=1, max_length=120),
    sehir: str | None = Query(default=None, max_length=100),
    ilce: str | None = Query(default=None, description="Canonical ilce UUID'si; serbest metin kabul edilmez."),
    tur: str | None = Query(default=None, max_length=50),
    zorunlu_kosul: list[str] = Query(default=[]),
    tercih: list[str] = Query(default=[]),
    limit: int = Query(default=20, ge=1, le=50),
    cursor: str | None = Query(default=None, max_length=500),
    oturum: Session = Depends(oturum_al),
) -> AramaCevabi:
    try:
        return ara(
            oturum, q=q, sehir_degeri=sehir, ilce_id=ilce, tur=tur,
            zorunlu_kosullar=zorunlu_kosul, tercihler=tercih, limit=limit, cursor=cursor,
        )
    except ValueError as hata:
        raise HTTPException(status_code=422, detail=str(hata)) from hata


@yonlendirici.get("/filtreler", response_model=AramaFiltreleriCevabi)
def arama_filtreleri(
    sehir: str | None = Query(default=None, max_length=100),
    oturum: Session = Depends(oturum_al),
) -> AramaFiltreleriCevabi:
    try:
        return filtre_katalogunu_getir(oturum, sehir)
    except ValueError as hata:
        raise HTTPException(status_code=422, detail=str(hata)) from hata
