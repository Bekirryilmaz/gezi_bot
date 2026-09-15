from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sunucu.kapsam.semalar import IlceDetayiSemasi, KamusalYerDetayiSemasi, SehirKapsamiSemasi
from sunucu.kapsam.servis import ilce_detayi_getir, sehir_kapsami_getir, yer_detayi_getir
from sunucu.karar_motoru.semalar import KararBaglamiSemasi
from sunucu.veritabani.baglanti import oturum_al


yonlendirici = APIRouter(prefix="/v1", tags=["kamusal-kapsam"])


@yonlendirici.get("/sehirler/{sehir_anahtari}/kapsam", response_model=SehirKapsamiSemasi)
def sehir_kapsami(sehir_anahtari: str, oturum: Session = Depends(oturum_al)) -> SehirKapsamiSemasi:
    try:
        return sehir_kapsami_getir(oturum, sehir_anahtari)
    except LookupError as hata:
        raise HTTPException(status_code=404, detail=str(hata)) from hata


@yonlendirici.get("/sehirler/{sehir_anahtari}/ilceler/{ilce_id}", response_model=IlceDetayiSemasi)
def ilce_detayi(sehir_anahtari: str, ilce_id: str, oturum: Session = Depends(oturum_al)) -> IlceDetayiSemasi:
    try:
        return ilce_detayi_getir(oturum, sehir_anahtari, ilce_id)
    except (LookupError, ValueError) as hata:
        raise HTTPException(status_code=404, detail=str(hata)) from hata


@yonlendirici.get("/yerler/{yer_id}", response_model=KamusalYerDetayiSemasi)
def yer_detayi(yer_id: str, oturum: Session = Depends(oturum_al)) -> KamusalYerDetayiSemasi:
    try:
        return yer_detayi_getir(oturum, yer_id)
    except LookupError as hata:
        raise HTTPException(status_code=404, detail=str(hata)) from hata


@yonlendirici.post("/yerler/{yer_id}/degerlendir", response_model=KamusalYerDetayiSemasi)
def yer_detayini_baglamla_degerlendir(
    yer_id: str,
    baglam: KararBaglamiSemasi,
    oturum: Session = Depends(oturum_al),
) -> KamusalYerDetayiSemasi:
    try:
        return yer_detayi_getir(oturum, yer_id, baglam_semasi=baglam)
    except LookupError as hata:
        raise HTTPException(status_code=404, detail=str(hata)) from hata
