from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from sunucu.api.altyapi import hata_cevabi
from sunucu.karar_motoru.semalar import KararDegerlendirmeCevabi, KararDegerlendirmeTalebi, KararSonucuSemasi
from sunucu.karar_motoru.servis import kararlari_degerlendir
from sunucu.veritabani.baglanti import oturum_al

yonlendirici = APIRouter(prefix="/v1/kararlar", tags=["kararlar"])


@yonlendirici.post("/degerlendir", response_model=KararDegerlendirmeCevabi)
def karar_degerlendir(talep: KararDegerlendirmeTalebi, request: Request, oturum: Session = Depends(oturum_al)) -> KararDegerlendirmeCevabi | JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid4()))
    baglam = talep.baglam.domaine(talep.giris_kanali)
    try:
        sonuclar, trace, _adaylar = kararlari_degerlendir(oturum, baglam, talep.aday_yer_idleri, request_id=request_id)
    except SQLAlchemyError:
        oturum.rollback()
        return hata_cevabi(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            kod="karar_servisi_kullanilamiyor",
            mesaj="Karar icin gereken bilgi servisi gecici olarak kullanilamiyor.",
            request_id=request_id,
        )
    return KararDegerlendirmeCevabi(
        sonuclar=[KararSonucuSemasi.domainden(sonuc) for sonuc in sonuclar],
        trace_reference=trace,
    )
