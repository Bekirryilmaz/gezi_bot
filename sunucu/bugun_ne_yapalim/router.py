from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from sunucu.api.altyapi import hata_cevabi
from sunucu.bugun_ne_yapalim.semalar import BugunNeYapalimCevabi, BugunNeYapalimTalebi
from sunucu.bugun_ne_yapalim.servis import bugun_ne_yapalim
from sunucu.veritabani.baglanti import oturum_al

yonlendirici = APIRouter(tags=["bugun-ne-yapalim"])


@yonlendirici.post("/v1/bugun-ne-yapalim", response_model=BugunNeYapalimCevabi)
def degerlendir(
    talep: BugunNeYapalimTalebi,
    request: Request,
    oturum: Session = Depends(oturum_al),
) -> BugunNeYapalimCevabi | JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid4()))
    try:
        return bugun_ne_yapalim(oturum, talep, request_id=request_id)
    except ValueError as hata:
        raise HTTPException(status_code=422, detail=str(hata)) from hata
    except SQLAlchemyError:
        oturum.rollback()
        return hata_cevabi(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            kod="bugun_ne_yapalim_kullanilamiyor",
            mesaj=(
                "Bugün Ne Yapalım değerlendirmesi şu anda tamamlanamıyor. "
                "Girdin korunarak yeniden deneyebilirsin."
            ),
            request_id=request_id,
        )
