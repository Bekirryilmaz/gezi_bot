"""
Sehir ve yer listeleme/detay uc noktalari.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ortak.sabitler import DeneyimEksen
from sunucu.api.semalar import (
    BolgeProfiliCevap,
    SehirCevap,
    SehirIstatistikleri,
    YerDetay,
    YerListeCevabi,
    YerOzet,
)
from sunucu.veritabani.baglanti import oturum_al
from sunucu.veritabani.modeller import BolgeProfili, Sehir
from sunucu.veritabani.sorgular import (
    sehir_yer_sayilari,
    sehir_yerlerini_sayfa_getir,
    yer_ve_koordinat_getir,
)
from veri.ortak.sehir_ayarlari import SEHIRLER, sehir_anahtarini_isme_gore_bul, sehir_getir

yonlendirici = APIRouter(tags=["yerler"])


def _sehri_veritabanindan_bul(oturum: Session, sehir_anahtari: str) -> Sehir:
    try:
        sehir_ayari = sehir_getir(sehir_anahtari)
    except KeyError as hata:
        raise HTTPException(status_code=404, detail=str(hata)) from hata

    sehir = oturum.query(Sehir).filter(Sehir.isim == sehir_ayari.isim).first()
    if sehir is None:
        raise HTTPException(
            status_code=404,
            detail=f"'{sehir_ayari.isim}' henuz veritabanina aktarilmamis. "
            f"Once 'python -m sunucu.veritabani.aktarim.calistir --sehir {sehir_anahtari}' calistir.",
        )
    return sehir


@yonlendirici.get("/sehirler", response_model=list[SehirCevap])
def sehirleri_listele(oturum: Session = Depends(oturum_al)) -> list[SehirCevap]:
    """Platformda aktif olan sehirleri listeler."""
    sehirler = oturum.query(Sehir).filter(Sehir.aktif_mi.is_(True)).order_by(Sehir.isim).all()
    sonuc = []
    for sehir in sehirler:
        anahtar = sehir_anahtarini_isme_gore_bul(sehir.isim) or sehir.isim.lower()
        sonuc.append(SehirCevap.yerden_olustur(sehir, anahtar))
    return sonuc


@yonlendirici.get("/sehirler/{sehir_anahtari}/yerler", response_model=YerListeCevabi)
def yerleri_listele(
    sehir_anahtari: str,
    ana_kategori: str | None = Query(default=None, description="Orn. 'gezilecek_yer', 'konaklama', 'yeme_icme'"),
    alt_kategori: str | None = Query(default=None, description="Orn. 'tarihi_kulturel', 'plaj_su'"),
    sadece_kesif: bool = Query(
        default=True,
        description="True: vitrin (konaklama gizlenir, yeme-icme yalniz etiketli/yuksek duygulu). "
        "False: rota motoru/test icin kisitlamasiz.",
    ),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    oturum: Session = Depends(oturum_al),
) -> YerListeCevabi:
    """Bir sehirdeki yerleri, opsiyonel kategori ve kesif filtresiyle sayfalar."""
    sehir = _sehri_veritabanindan_bul(oturum, sehir_anahtari)

    ana_kategoriler = [ana_kategori] if ana_kategori else None
    alt_kategoriler = [alt_kategori] if alt_kategori else None
    yerler_ve_koordinatlar, toplam_sayi = sehir_yerlerini_sayfa_getir(
        oturum,
        sehir.id,
        ana_kategoriler,
        alt_kategoriler,
        sadece_kesif=sadece_kesif,
        limit=limit,
        offset=offset,
    )
    return YerListeCevabi(
        yerler=[YerOzet.yerden_olustur(yer, enlem, boylam) for yer, enlem, boylam in yerler_ve_koordinatlar],
        toplam_sayi=toplam_sayi,
    )


@yonlendirici.get("/sehirler/{sehir_anahtari}/bolgeler", response_model=list[BolgeProfiliCevap])
def bolgeleri_listele(sehir_anahtari: str, oturum: Session = Depends(oturum_al)) -> list[BolgeProfiliCevap]:
    """Bir sehrin kendisi (sehir merkezi) VE tum ilceleri icin tanitim
    tanitimlarini dondurur. Sehir merkezi kaydi (varsa) her zaman ilk
    sirada gelir; ilceler yorum sayisina gore siralanmaz."""
    sehir = _sehri_veritabanindan_bul(oturum, sehir_anahtari)
    profiller = (
        oturum.query(BolgeProfili)
        .filter(BolgeProfili.sehir_id == sehir.id)
        .order_by(BolgeProfili.ilce_mi.asc(), BolgeProfili.bolge_adi.asc())
        .all()
    )
    return [
        BolgeProfiliCevap.yerden_olustur(profil, sehir_anahtari) for profil in profiller
    ]


@yonlendirici.get("/sehirler/{sehir_anahtari}/istatistikler", response_model=SehirIstatistikleri)
def sehir_istatistikleri(
    sehir_anahtari: str, oturum: Session = Depends(oturum_al)
) -> SehirIstatistikleri:
    """Ana sayfa kanit bandinin sayilari. Yorum sayisi bilerek yer almaz (K2)."""
    sehir = _sehri_veritabanindan_bul(oturum, sehir_anahtari)
    toplam, kesif, ilce = sehir_yer_sayilari(oturum, sehir.id)
    bolge_sayisi = (
        oturum.query(BolgeProfili).filter(BolgeProfili.sehir_id == sehir.id).count()
    )
    return SehirIstatistikleri(
        sehir_anahtari=sehir_anahtari,
        yer_sayisi=toplam,
        kesif_yer_sayisi=kesif,
        ilce_sayisi=ilce,
        bolge_profili_sayisi=bolge_sayisi,
        deneyim_ekseni_sayisi=len(DeneyimEksen),
    )


@yonlendirici.get("/yerler/{yer_id}", response_model=YerDetay)
def yer_detayi(yer_id: str, oturum: Session = Depends(oturum_al)) -> YerDetay:
    """Bir yerin kamusal allow-list detaylarini getirir."""
    sonuc = yer_ve_koordinat_getir(oturum, yer_id)
    if sonuc is None:
        raise HTTPException(status_code=404, detail=f"'{yer_id}' id'li yer bulunamadi.")

    yer, enlem, boylam = sonuc
    return YerDetay.yerden_olustur(yer, enlem, boylam)


@yonlendirici.get("/sehirler-tanimli", response_model=list[str], include_in_schema=False)
def tanimli_sehir_anahtarlari() -> list[str]:
    """Yardimci uc nokta: veri/ortak/sehir_ayarlari.py'de tanimli TUM
    sehir anahtarlarini listeler (henuz veritabanina aktarilmamis olsa bile)."""
    return sorted(SEHIRLER)
