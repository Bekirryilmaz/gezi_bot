from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from sunucu.api.altyapi import hata_cevabi
from sunucu.kesfet.semalar import KesfetDegerlendirmeCevabi, KesfetDegerlendirmeTalebi
from sunucu.kesfet.servis import kesfet_degerlendir
from sunucu.veritabani.baglanti import oturum_al


yonlendirici = APIRouter(prefix="/v1/kesfet", tags=["kesfet"])


@yonlendirici.post("/degerlendir", response_model=KesfetDegerlendirmeCevabi)
def degerlendir(
    talep: KesfetDegerlendirmeTalebi,
    request: Request,
    oturum: Session = Depends(oturum_al),
) -> KesfetDegerlendirmeCevabi | JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid4()))
    try:
        return kesfet_degerlendir(oturum, talep, request_id=request_id)
    except ValueError as hata:
        raise HTTPException(status_code=422, detail=str(hata)) from hata
    except SQLAlchemyError:
        oturum.rollback()
        return hata_cevabi(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            kod="kesfet_servisi_kullanilamiyor",
            mesaj="Keşfet değerlendirmesi şu anda tamamlanamıyor. Bağlamını koruyup yeniden deneyebilirsin.",
            request_id=request_id,
        )

