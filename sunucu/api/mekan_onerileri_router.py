"""Kullanici mekan onerisi gonderme + yonetici onay/red."""

from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile
from geoalchemy2.elements import WKTElement
from sqlalchemy.orm import Session

from ortak.sabitler import (
    AnaKategori,
    GezilecekYerAltKategori,
    KonaklamaAltKategori,
    MekanOneriDurumu,
    MekanOneriKategori,
    OzelEtiket,
    VeriKaynagi,
    YemeIcmeAltKategori,
)
from sunucu.api.guvenlik import (
    eposta_gecerli_mi,
    hiz_siniri_kontrol,
    istemci_ip,
    turnstile_dogrula,
    yonetici_gerekli,
)
from sunucu.api.semalar import MekanOneriCevap, MekanOneriGonderimCevabi, MekanOneriOnayCevabi
from sunucu.veritabani.baglanti import oturum_al
from sunucu.veritabani.modeller import MekanOneri, Sehir, Yer, YerKaynak
from veri.ortak.metin_araclari import turkce_kucuk_harf

yonlendirici = APIRouter(tags=["mekan-onerileri"])

YUKLEME_KOKU = Path(__file__).resolve().parents[1] / "yuklemeler" / "mekan-onerileri"
MAKS_FOTOGRAF = 3
MAKS_BOYUT = 5 * 1024 * 1024
IZINLI_SIHIR: dict[bytes, str] = {
    b"\xff\xd8\xff": ".jpg",
    b"\x89PNG\r\n\x1a\n": ".png",
}

KATEGORI_ESLEME: dict[str, tuple[str, str]] = {
    MekanOneriKategori.GIZLI_KOY.value: (
        AnaKategori.GEZILECEK_YER.value,
        GezilecekYerAltKategori.PLAJ_SU.value,
    ),
    MekanOneriKategori.SELALE_DOGA.value: (
        AnaKategori.GEZILECEK_YER.value,
        GezilecekYerAltKategori.DOGA_MANZARA.value,
    ),
    MekanOneriKategori.BUTIK_KAFE.value: (
        AnaKategori.YEME_ICME.value,
        YemeIcmeAltKategori.KAFE.value,
    ),
    MekanOneriKategori.MANZARA_TEPE.value: (
        AnaKategori.GEZILECEK_YER.value,
        GezilecekYerAltKategori.FOTOGRAF_NOKTASI.value,
    ),
    MekanOneriKategori.TARIHI_KALINTI.value: (
        AnaKategori.GEZILECEK_YER.value,
        GezilecekYerAltKategori.TARIHI_KULTUREL.value,
    ),
    MekanOneriKategori.KAMP_KARAVAN.value: (
        AnaKategori.KONAKLAMA.value,
        KonaklamaAltKategori.KAMP_KARAVAN.value,
    ),
    MekanOneriKategori.DIGER.value: (
        AnaKategori.GEZILECEK_YER.value,
        GezilecekYerAltKategori.DOGA_MANZARA.value,
    ),
}


def _uzanti_bul(icerik: bytes) -> str:
    for sihir, uzanti in IZINLI_SIHIR.items():
        if icerik.startswith(sihir):
            return uzanti
    if len(icerik) >= 12 and icerik[:4] == b"RIFF" and icerik[8:12] == b"WEBP":
        return ".webp"
    raise HTTPException(
        status_code=400,
        detail="Sadece JPEG, PNG veya WebP gorselleri kabul edilir.",
    )


def _fotograflari_kaydet(dosyalar: list[UploadFile]) -> list[str]:
    if not dosyalar:
        raise HTTPException(status_code=400, detail="En az bir fotograf yukle.")
    if len(dosyalar) > MAKS_FOTOGRAF:
        raise HTTPException(status_code=400, detail=f"En fazla {MAKS_FOTOGRAF} fotograf yukle.")

    YUKLEME_KOKU.mkdir(parents=True, exist_ok=True)
    urller: list[str] = []
    for dosya in dosyalar:
        icerik = dosya.file.read()
        if not icerik:
            raise HTTPException(status_code=400, detail="Bos fotograf dosyasi gonderildi.")
        if len(icerik) > MAKS_BOYUT:
            raise HTTPException(status_code=400, detail="Her fotograf en fazla 5 MB olabilir.")
        uzanti = _uzanti_bul(icerik)
        ad = f"{uuid.uuid4().hex}{uzanti}"
        (YUKLEME_KOKU / ad).write_bytes(icerik)
        urller.append(f"/yuklemeler/mekan-onerileri/{ad}")
    return urller


def _sehir_bul_veya_olustur(oturum: Session, isim: str, enlem: float, boylam: float) -> Sehir:
    hedef = turkce_kucuk_harf(isim.strip())
    for sehir in oturum.query(Sehir).all():
        if turkce_kucuk_harf(sehir.isim) == hedef:
            return sehir
    sehir = Sehir(
        isim=isim.strip()[:100],
        merkez_enlem=enlem,
        merkez_boylam=boylam,
        aktif_mi=True,
    )
    oturum.add(sehir)
    oturum.flush()
    return sehir


def _oneri_yer_aktar(oturum: Session, oneri: MekanOneri) -> Yer:
    esleme = KATEGORI_ESLEME.get(oneri.kategori)
    if esleme is None:
        raise HTTPException(status_code=400, detail="Bilinmeyen oneri kategorisi.")
    ana_kategori, alt_kategori = esleme
    sehir = _sehir_bul_veya_olustur(oturum, oneri.sehir, oneri.enlem, oneri.boylam)

    aciklama_parcalari = [oneri.aciklama]
    if oneri.ziyaretci_tuyosu:
        aciklama_parcalari.append(f"Ziyaretci tuyosu: {oneri.ziyaretci_tuyosu}")

    yer = Yer(
        sehir_id=sehir.id,
        isim=oneri.baslik,
        ana_kategori=ana_kategori,
        alt_kategori=alt_kategori,
        ilce=oneri.ilce,
        aciklama="\n\n".join(aciklama_parcalari),
        tanitim_metni=oneri.aciklama,
        konum=WKTElement(f"POINT({oneri.boylam} {oneri.enlem})", srid=4326),
        ozellikler={OzelEtiket.TOPLULUK_KESFI.value: True},
        aktiviteler=[],
        fotograf_urlleri=list(oneri.fotograf_urlleri or []),
        deneyim_puanlari={},
        yer_profili={},
    )
    oturum.add(yer)
    oturum.flush()
    oturum.add(
        YerKaynak(
            yer_id=yer.id,
            kaynak=VeriKaynagi.SITE_ICI.value,
            kaynak_id=oneri.id,
        )
    )
    return yer


@yonlendirici.post("/mekan-onerileri", response_model=MekanOneriGonderimCevabi)
async def mekan_onerisi_olustur(
    istek: Request,
    baslik: str = Form(...),
    kategori: str = Form(...),
    sehir: str = Form(...),
    ilce: str = Form(...),
    aciklama: str = Form(...),
    gonderen_eposta: str = Form(...),
    enlem: float = Form(...),
    boylam: float = Form(...),
    gonderen_adi: str | None = Form(default=None),
    ziyaretci_tuyosu: str | None = Form(default=None),
    turnstile_jetonu: str | None = Form(default=None),
    sirket_sitesi: str | None = Form(default=None),
    fotograflar: list[UploadFile] = File(...),
    oturum: Session = Depends(oturum_al),
) -> MekanOneriGonderimCevabi:
    """Yeni oneri: her zaman beklemede kaydedilir, haritaya dusmez."""
    if sirket_sitesi:
        return MekanOneriGonderimCevabi(
            id="yoksayildi",
            status=MekanOneriDurumu.BEKLEMEDE.value,
            mesaj="Öneriniz incelenmek üzere ekibimize ulaştı!",
        )

    baslik = baslik.strip()
    sehir = sehir.strip()
    ilce = ilce.strip()
    aciklama = aciklama.strip()
    eposta = gonderen_eposta.strip()
    adi = gonderen_adi.strip() if gonderen_adi else None
    tuyo = ziyaretci_tuyosu.strip() if ziyaretci_tuyosu else None

    if len(baslik) < 3 or len(baslik) > 200:
        raise HTTPException(status_code=400, detail="Mekan adi 3-200 karakter olmali.")
    if kategori not in {k.value for k in MekanOneriKategori}:
        raise HTTPException(status_code=400, detail="Gecersiz kategori.")
    if len(sehir) < 2 or len(ilce) < 2:
        raise HTTPException(status_code=400, detail="Sehir ve ilce zorunludur.")
    if len(aciklama) < 20 or len(aciklama) > 2500:
        raise HTTPException(status_code=400, detail="Aciklama 20-2500 karakter olmali.")
    if not eposta_gecerli_mi(eposta):
        raise HTTPException(status_code=400, detail="Gecerli bir e-posta gir.")
    if not (-90 <= enlem <= 90 and -180 <= boylam <= 180):
        raise HTTPException(status_code=400, detail="Gecerli bir konum sec (enlem/boylam).")
    if tuyo and len(tuyo) > 500:
        raise HTTPException(status_code=400, detail="Ziyaretci tuyosu en fazla 500 karakter.")

    ip = istemci_ip(istek)
    turnstile_dogrula(turnstile_jetonu, ip)
    hiz_siniri_kontrol(ip, eposta)

    urller = _fotograflari_kaydet([f for f in fotograflar if f.filename])
    oneri = MekanOneri(
        baslik=baslik,
        kategori=kategori,
        sehir=sehir,
        ilce=ilce,
        aciklama=aciklama,
        ziyaretci_tuyosu=tuyo,
        enlem=enlem,
        boylam=boylam,
        fotograf_urlleri=urller,
        gonderen_adi=adi or None,
        gonderen_eposta=eposta,
        durum=MekanOneriDurumu.BEKLEMEDE.value,
        ip_adresi=ip[:64],
    )
    oturum.add(oneri)
    try:
        oturum.commit()
        oturum.refresh(oneri)
    except Exception:
        oturum.rollback()
        raise
    return MekanOneriGonderimCevabi(
        id=oneri.id,
        status=oneri.durum,
        mesaj="Öneriniz incelenmek üzere ekibimize ulaştı!",
    )


@yonlendirici.get("/mekan-onerileri", response_model=list[MekanOneriCevap])
def mekan_onerilerini_listele(
    durum: str | None = Query(default="beklemede"),
    oturum: Session = Depends(oturum_al),
    _: None = Depends(yonetici_gerekli),
) -> list[MekanOneriCevap]:
    sorgu = oturum.query(MekanOneri).order_by(MekanOneri.olusturulma_zamani.desc())
    if durum:
        sorgu = sorgu.filter(MekanOneri.durum == durum)
    return [MekanOneriCevap.kayittan(kayit) for kayit in sorgu.limit(200).all()]


@yonlendirici.get("/mekan-onerileri/{oneri_id}", response_model=MekanOneriCevap)
def mekan_onerisi_detay(
    oneri_id: str,
    oturum: Session = Depends(oturum_al),
    _: None = Depends(yonetici_gerekli),
) -> MekanOneriCevap:
    oneri = oturum.query(MekanOneri).filter(MekanOneri.id == oneri_id).first()
    if oneri is None:
        raise HTTPException(status_code=404, detail="Oneri bulunamadi.")
    return MekanOneriCevap.kayittan(oneri)


@yonlendirici.post("/mekan-onerileri/{oneri_id}/onayla", response_model=MekanOneriOnayCevabi)
def mekan_onerisi_onayla(
    oneri_id: str,
    oturum: Session = Depends(oturum_al),
    _: None = Depends(yonetici_gerekli),
) -> MekanOneriOnayCevabi:
    oneri = oturum.query(MekanOneri).filter(MekanOneri.id == oneri_id).first()
    if oneri is None:
        raise HTTPException(status_code=404, detail="Oneri bulunamadi.")
    if oneri.durum == MekanOneriDurumu.ONAYLANDI.value and oneri.yer_id:
        return MekanOneriOnayCevabi(
            id=oneri.id,
            status=oneri.durum,
            yerId=oneri.yer_id,
            mesaj="Bu oneri zaten onaylanmis.",
        )
    if oneri.durum == MekanOneriDurumu.REDDEDILDI.value:
        raise HTTPException(status_code=409, detail="Reddedilmis oneri onaylanamaz.")

    yer = _oneri_yer_aktar(oturum, oneri)
    oneri.durum = MekanOneriDurumu.ONAYLANDI.value
    oneri.yer_id = yer.id
    oturum.commit()
    return MekanOneriOnayCevabi(
        id=oneri.id,
        status=oneri.durum,
        yerId=yer.id,
        mesaj="Oneri onaylandi ve Topluluk Kesfi olarak yayinlandi.",
    )


@yonlendirici.post("/mekan-onerileri/{oneri_id}/reddet", response_model=MekanOneriCevap)
def mekan_onerisi_reddet(
    oneri_id: str,
    red_nedeni: str | None = Form(default=None),
    oturum: Session = Depends(oturum_al),
    _: None = Depends(yonetici_gerekli),
) -> MekanOneriCevap:
    oneri = oturum.query(MekanOneri).filter(MekanOneri.id == oneri_id).first()
    if oneri is None:
        raise HTTPException(status_code=404, detail="Oneri bulunamadi.")
    if oneri.durum == MekanOneriDurumu.ONAYLANDI.value:
        raise HTTPException(status_code=409, detail="Onaylanmis oneri reddedilemez.")
    oneri.durum = MekanOneriDurumu.REDDEDILDI.value
    if red_nedeni:
        oneri.red_nedeni = red_nedeni.strip()[:500]
    oturum.commit()
    oturum.refresh(oneri)
    return MekanOneriCevap.kayittan(oneri)
