"""Kullanici mekan onerisi gonderme + yonetici onay/red."""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
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
from sunucu.api.semalar import (
    EditorialGuncelle,
    GorunurlukGuncelle,
    MekanOneriCevap,
    MekanOneriGonderimCevabi,
    MekanOneriKoordinat,
    MekanOneriOnayCevabi,
    ToplulukEditorial,
    ToplulukGorunurluk,
    ToplulukUlasim,
    ToplulukYaziCevap,
    YorumCevap,
    YorumOlusturGovde,
)
from sunucu.veritabani.baglanti import oturum_al
from sunucu.veritabani.modeller import MekanOneri, OneriYorum, Sehir, Yer, YerKaynak
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


def _slug_uret(baslik: str, sehir: str, kayit_id: str) -> str:
    ham = turkce_kucuk_harf(f"{baslik} {sehir}")
    temiz = re.sub(r"[^a-z0-9]+", "-", ham).strip("-")[:80]
    kisa = kayit_id.replace("-", "")[:8]
    return f"{temiz}-{kisa}" if temiz else kisa


def _blog_kategori(kategori: str) -> str:
    if kategori == "kamp_karavan":
        return "kamp_alani"
    return kategori


def _yorum_sayisi(oturum: Session, oneri_id: str) -> int:
    return (
        oturum.query(OneriYorum)
        .filter(OneriYorum.oneri_id == oneri_id, OneriYorum.durum == "yayinda")
        .count()
    )


def _yazi_cevap(oneri: MekanOneri, yorum_sayisi: int) -> ToplulukYaziCevap:
    gorseller = list(oneri.onayli_fotograflar or []) or list(oneri.fotograf_urlleri or [])
    editorial = None
    if oneri.tarih_baglam or oneri.editor_notu or oneri.yayin_zamani:
        editorial = ToplulukEditorial(
            historicalContext=oneri.tarih_baglam,
            adminNotes=oneri.editor_notu,
            publishedAt=oneri.yayin_zamani.isoformat() if oneri.yayin_zamani else "",
        )
    return ToplulukYaziCevap(
        id=oneri.id,
        slug=oneri.slug,
        title=oneri.baslik,
        category=_blog_kategori(oneri.kategori),
        city=oneri.sehir,
        district=oneri.ilce,
        coordinates=MekanOneriKoordinat(lat=oneri.enlem, lng=oneri.boylam),
        directions=oneri.adres_tarifi or "",
        transportation=ToplulukUlasim(
            carAccess=oneri.araba_erisimi or "",
            walkingDistance=oneri.yurume_mesafesi or "",
            roadCondition=oneri.yol_durumu or "",
        ),
        userStory=oneri.aciklama,
        specialTip=oneri.ziyaretci_tuyosu,
        approvedImages=gorseller,
        submitterEmail="",
        adminEditorial=editorial,
        visibleFields=ToplulukGorunurluk(
            showDirections=bool(oneri.gorunur_tarif),
            showTransportation=bool(oneri.gorunur_ulasim),
            showExactCoordinates=bool(oneri.gorunur_koordinat),
            showSpecialTip=bool(oneri.gorunur_tuyo),
        ),
        likesCount=oneri.begeni_sayisi or 0,
        commentsCount=yorum_sayisi,
        status=oneri.durum,
    )


def _yayin_bul(oturum: Session, anahtar: str) -> MekanOneri | None:
    oneri = (
        oturum.query(MekanOneri)
        .filter(
            MekanOneri.durum == MekanOneriDurumu.ONAYLANDI.value,
            MekanOneri.slug == anahtar,
        )
        .first()
    )
    if oneri:
        return oneri
    return (
        oturum.query(MekanOneri)
        .filter(
            MekanOneri.durum == MekanOneriDurumu.ONAYLANDI.value,
            MekanOneri.id == anahtar,
        )
        .first()
    )


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
    if oneri.adres_tarifi:
        aciklama_parcalari.append(f"Adres tarifi: {oneri.adres_tarifi}")
    ulasim = [
        f"Arac: {oneri.araba_erisimi}" if oneri.araba_erisimi else "",
        f"Yol: {oneri.yol_durumu}" if oneri.yol_durumu else "",
        f"Yurume: {oneri.yurume_mesafesi}" if oneri.yurume_mesafesi else "",
        f"Toplu tasima: {oneri.toplu_tasima}" if oneri.toplu_tasima else "",
    ]
    ulasim_metni = " · ".join(p for p in ulasim if p)
    if ulasim_metni:
        aciklama_parcalari.append(f"Ulasim: {ulasim_metni}")
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
    adres_tarifi: str = Form(...),
    araba_erisimi: str = Form(...),
    yurume_mesafesi: str = Form(...),
    yol_durumu: str = Form(...),
    toplu_tasima: str = Form(...),
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
    tarif = adres_tarifi.strip()
    araba = araba_erisimi.strip()
    yurume = yurume_mesafesi.strip()
    yol = yol_durumu.strip()
    toplu = toplu_tasima.strip()
    tuyo = ziyaretci_tuyosu.strip() if ziyaretci_tuyosu else None

    if len(baslik) < 3 or len(baslik) > 200:
        raise HTTPException(status_code=400, detail="Mekan adi 3-200 karakter olmali.")
    if kategori not in {k.value for k in MekanOneriKategori}:
        raise HTTPException(status_code=400, detail="Gecersiz kategori.")
    if len(sehir) < 2 or len(ilce) < 2:
        raise HTTPException(status_code=400, detail="Sehir ve ilce zorunludur.")
    if len(aciklama) < 20 or len(aciklama) > 2500:
        raise HTTPException(status_code=400, detail="Aciklama 20-2500 karakter olmali.")
    if len(tarif) < 10 or len(tarif) > 1500:
        raise HTTPException(status_code=400, detail="Adres tarifi 10-1500 karakter olmali.")
    if araba not in {"kolay", "zor", "4x4_gerekli", "aracsiz_ulasilamaz"}:
        raise HTTPException(status_code=400, detail="Arac erisimini sec.")
    if len(yurume) < 2 or len(yurume) > 200:
        raise HTTPException(status_code=400, detail="Yurume mesafesi zorunludur.")
    if len(yol) < 2 or len(yol) > 120:
        raise HTTPException(status_code=400, detail="Yol tipini gir.")
    if len(toplu) < 2 or len(toplu) > 300:
        raise HTTPException(status_code=400, detail="Toplu tasima bilgisini gir.")
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
    kayit_id = str(uuid.uuid4())
    oneri = MekanOneri(
        id=kayit_id,
        slug=_slug_uret(baslik, sehir, kayit_id),
        baslik=baslik,
        kategori=kategori,
        sehir=sehir,
        ilce=ilce,
        aciklama=aciklama,
        ziyaretci_tuyosu=tuyo,
        adres_tarifi=tarif,
        araba_erisimi=araba,
        yurume_mesafesi=yurume,
        yol_durumu=yol,
        toplu_tasima=toplu,
        enlem=enlem,
        boylam=boylam,
        fotograf_urlleri=urller,
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
    return [
        MekanOneriCevap.kayittan(kayit, comments_count=_yorum_sayisi(oturum, kayit.id))
        for kayit in sorgu.limit(200).all()
    ]


@yonlendirici.get("/mekan-onerileri/yayinlar", response_model=list[ToplulukYaziCevap])
def yayinlanan_oneriler(oturum: Session = Depends(oturum_al)) -> list[ToplulukYaziCevap]:
    kayitlar = (
        oturum.query(MekanOneri)
        .filter(MekanOneri.durum == MekanOneriDurumu.ONAYLANDI.value)
        .order_by(MekanOneri.olusturulma_zamani.desc())
        .limit(120)
        .all()
    )
    return [_yazi_cevap(k, _yorum_sayisi(oturum, k.id)) for k in kayitlar]


@yonlendirici.get("/mekan-onerileri/yayinlar/{anahtar}", response_model=ToplulukYaziCevap)
def yayin_detay(anahtar: str, oturum: Session = Depends(oturum_al)) -> ToplulukYaziCevap:
    oneri = _yayin_bul(oturum, anahtar)
    if oneri is None:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi.")
    return _yazi_cevap(oneri, _yorum_sayisi(oturum, oneri.id))


@yonlendirici.get("/mekan-onerileri/yayinlar/{anahtar}/yorumlar", response_model=list[YorumCevap])
def yayin_yorumlari(anahtar: str, oturum: Session = Depends(oturum_al)) -> list[YorumCevap]:
    oneri = _yayin_bul(oturum, anahtar)
    if oneri is None:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi.")
    kayitlar = (
        oturum.query(OneriYorum)
        .filter(OneriYorum.oneri_id == oneri.id, OneriYorum.durum == "yayinda")
        .order_by(OneriYorum.olusturulma_zamani.desc())
        .limit(100)
        .all()
    )
    return [
        YorumCevap(
            id=y.id,
            postId=y.oneri_id,
            authorName=y.yazar_adi,
            content=y.icerik,
            createdAt=y.olusturulma_zamani.isoformat() if y.olusturulma_zamani else "",
            status=y.durum,
        )
        for y in kayitlar
    ]


@yonlendirici.post("/mekan-onerileri/yayinlar/{anahtar}/yorumlar", response_model=YorumCevap)
def yayin_yorum_ekle(
    anahtar: str,
    govde: YorumOlusturGovde,
    oturum: Session = Depends(oturum_al),
) -> YorumCevap:
    oneri = _yayin_bul(oturum, anahtar)
    if oneri is None:
        raise HTTPException(status_code=404, detail="Yazi bulunamadi.")
    ad = govde.authorName.strip()
    icerik = govde.content.strip()
    if len(ad) < 2 or len(ad) > 80:
        raise HTTPException(status_code=400, detail="Isim 2-80 karakter olmali.")
    if len(icerik) < 4 or len(icerik) > 1200:
        raise HTTPException(status_code=400, detail="Yorum 4-1200 karakter olmali.")
    yorum = OneriYorum(
        oneri_id=oneri.id,
        yazar_adi=ad,
        icerik=icerik,
        durum="yayinda",
    )
    oturum.add(yorum)
    oturum.commit()
    oturum.refresh(yorum)
    return YorumCevap(
        id=yorum.id,
        postId=yorum.oneri_id,
        authorName=yorum.yazar_adi,
        content=yorum.icerik,
        createdAt=yorum.olusturulma_zamani.isoformat() if yorum.olusturulma_zamani else "",
        status=yorum.durum,
    )


@yonlendirici.patch("/mekan-onerileri/{oneri_id}/gorunurluk", response_model=MekanOneriCevap)
def gorunurluk_guncelle(
    oneri_id: str,
    govde: GorunurlukGuncelle,
    oturum: Session = Depends(oturum_al),
    _: None = Depends(yonetici_gerekli),
) -> MekanOneriCevap:
    oneri = oturum.query(MekanOneri).filter(MekanOneri.id == oneri_id).first()
    if oneri is None:
        raise HTTPException(status_code=404, detail="Oneri bulunamadi.")
    if govde.showDirections is not None:
        oneri.gorunur_tarif = govde.showDirections
    if govde.showTransportation is not None:
        oneri.gorunur_ulasim = govde.showTransportation
    if govde.showExactCoordinates is not None:
        oneri.gorunur_koordinat = govde.showExactCoordinates
    if govde.showSpecialTip is not None:
        oneri.gorunur_tuyo = govde.showSpecialTip
    oturum.commit()
    oturum.refresh(oneri)
    return MekanOneriCevap.kayittan(oneri, comments_count=_yorum_sayisi(oturum, oneri.id))


@yonlendirici.patch("/mekan-onerileri/{oneri_id}/editorial", response_model=MekanOneriCevap)
def editorial_guncelle(
    oneri_id: str,
    govde: EditorialGuncelle,
    oturum: Session = Depends(oturum_al),
    _: None = Depends(yonetici_gerekli),
) -> MekanOneriCevap:
    oneri = oturum.query(MekanOneri).filter(MekanOneri.id == oneri_id).first()
    if oneri is None:
        raise HTTPException(status_code=404, detail="Oneri bulunamadi.")
    if govde.historicalContext is not None:
        oneri.tarih_baglam = govde.historicalContext.strip()[:4000] or None
    if govde.adminNotes is not None:
        oneri.editor_notu = govde.adminNotes.strip()[:2000] or None
    oturum.commit()
    oturum.refresh(oneri)
    return MekanOneriCevap.kayittan(oneri, comments_count=_yorum_sayisi(oturum, oneri.id))


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
    if not oneri.slug:
        oneri.slug = _slug_uret(oneri.baslik, oneri.sehir, oneri.id)
    if not oneri.onayli_fotograflar:
        oneri.onayli_fotograflar = list(oneri.fotograf_urlleri or [])
    oneri.yayin_zamani = datetime.now(timezone.utc)
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
