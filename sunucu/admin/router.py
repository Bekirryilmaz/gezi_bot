from __future__ import annotations

import os
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from sqlalchemy import String, cast
from sqlalchemy.orm import Session

from sunucu.admin.semalar import (
    AdminKimlikCevabi,
    AdminLoginTalebi,
    AuditCevabi,
    BirinciElGozlemCevabi,
    BirinciElGozlemTalebi,
    BirlestirmeCevabi,
    ClaimIncelemeCevabi,
    ClaimOzetCevabi,
    ClaimSayfasiCevabi,
    DahiliSinyalOzetCevabi,
    DahiliSinyalSayfasiCevabi,
    EslemeAdayiCevabi,
    GrupIncelemeCevabi,
    GrupIncelemeTalebi,
    GrupKuyrukCevabi,
    IkinciIncelemeTalebi,
    IncelemeDosyasiCevabi,
    IncelemeKomutu,
    PilotOzetCevabi,
)
from sunucu.admin.workflow import (
    claim_yayin_onizle,
    ikinci_incelemeyi_onayla,
    inceleme_komutu_gonder,
    nesne_sehir_id,
    nesne_yetkisini_dogrula,
)
from sunucu.auth.rbac import Yetki
from sunucu.auth.servis import (
    CSRF_COOKIE,
    OTURUM_COOKIE,
    AdminBaglami,
    admin_baglami_al,
    oturum_ac,
    parola_dogrula,
    yetki_gerekli,
)
from sunucu.veritabani.admin_modelleri import AdminAuditOlayi, AdminKullanici, IncelemeDosyasi
from sunucu.veritabani.baglanti import oturum_al
from sunucu.veritabani.bilgi_modelleri import (
    DahiliSinyalOzeti,
    Gozlem,
    Iddia,
    IddiaSurumu,
    KanitBaglantisi,
    KaynakPolitikasi,
)
from sunucu.veritabani.kimlik_modelleri import EslemeAdayi, Sube, YerBirlestirmesi
from sunucu.veritabani.modeller import Yer

yonlendirici = APIRouter()


def _istek_id(request: Request) -> str:
    return (
        getattr(request.state, "request_id", None)
        or request.headers.get("X-Request-ID")
        or str(uuid.uuid4())
    )


@yonlendirici.post("/login", response_model=AdminKimlikCevabi)
def login(
    talep: AdminLoginTalebi, request: Request, yanit: Response, oturum: Session = Depends(oturum_al)
) -> AdminKimlikCevabi:
    kullanici = (
        oturum.query(AdminKullanici)
        .filter_by(eposta=talep.eposta.strip().lower(), aktif_mi=True)
        .first()
    )
    if not kullanici or not parola_dogrula(talep.parola, kullanici):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="E-posta veya parola gecersiz."
        )
    kayit, token, csrf = oturum_ac(
        oturum,
        kullanici,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    oturum.commit()
    guvenli = os.environ.get("UYGULAMA_ORTAMI", "development").lower() in {
        "production",
        "prod",
        "canli",
    }
    yanit.set_cookie(
        OTURUM_COOKIE,
        token,
        httponly=True,
        secure=guvenli,
        samesite="strict",
        max_age=max(0, int((kayit.sona_erme_zamani - datetime.now(UTC)).total_seconds())),
        path="/",
    )
    yanit.set_cookie(
        CSRF_COOKIE,
        csrf,
        httponly=False,
        secure=guvenli,
        samesite="strict",
        max_age=max(0, int((kayit.sona_erme_zamani - datetime.now(UTC)).total_seconds())),
        path="/",
    )
    roller = sorted(
        {
            satir[0]
            for satir in oturum.query(
                __import__("sunucu.veritabani.admin_modelleri", fromlist=["AdminRol"]).AdminRol.kod
            )
            .join(
                __import__(
                    "sunucu.veritabani.admin_modelleri", fromlist=["AdminKullaniciRolu"]
                ).AdminKullaniciRolu
            )
            .filter(
                __import__(
                    "sunucu.veritabani.admin_modelleri", fromlist=["AdminKullaniciRolu"]
                ).AdminKullaniciRolu.kullanici_id
                == kullanici.id
            )
            .all()
        }
    )
    from sunucu.auth.rbac import yetkileri_birlestir

    return AdminKimlikCevabi(
        id=kullanici.id,
        eposta=kullanici.eposta,
        gorunen_ad=kullanici.gorunen_ad,
        roller=roller,
        yetkiler=sorted(y.value for y in yetkileri_birlestir(set(roller))),
        csrf_token=csrf,
    )


@yonlendirici.get("/me", response_model=AdminKimlikCevabi)
def me(baglam: AdminBaglami = Depends(admin_baglami_al)) -> AdminKimlikCevabi:
    return AdminKimlikCevabi(
        id=baglam.kullanici.id,
        eposta=baglam.kullanici.eposta,
        gorunen_ad=baglam.kullanici.gorunen_ad,
        roller=sorted(baglam.roller),
        yetkiler=sorted(y.value for y in baglam.yetkiler),
    )


@yonlendirici.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    yanit: Response,
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(admin_baglami_al),
) -> None:
    baglam.oturum.iptal_zamani = datetime.now(UTC)
    oturum.commit()
    yanit.delete_cookie(OTURUM_COOKIE, path="/")
    yanit.delete_cookie(CSRF_COOKIE, path="/")


@yonlendirici.get("/kuyruk", response_model=list[IncelemeDosyasiCevabi])
def kuyruk(
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR)),
) -> list[IncelemeDosyasi]:
    sorgu = oturum.query(IncelemeDosyasi).filter(IncelemeDosyasi.durum != "tamamlandi")
    dosyalar = (
        sorgu.order_by(
            IncelemeDosyasi.oncelik_puani.desc(),
            IncelemeDosyasi.risk_sinifi.desc(),
            IncelemeDosyasi.olusturulma_zamani,
        )
        .limit(200)
        .all()
    )
    return [
        d
        for d in dosyalar
        if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, d.nesne_turu, d.nesne_id))
    ]


@yonlendirici.get("/kimlik/esleme-adaylari", response_model=list[EslemeAdayiCevabi])
def esleme_adaylari(
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR)),
) -> list[EslemeAdayiCevabi]:
    adaylar = (
        oturum.query(EslemeAdayi)
        .filter_by(durum="bekliyor")
        .order_by(EslemeAdayi.confidence.desc())
        .limit(200)
        .all()
    )
    return [
        EslemeAdayiCevabi(
            id=a.id,
            sol_sube_id=a.sol_sube_id,
            sag_sube_id=a.sag_sube_id,
            confidence=a.confidence,
            belirsizlik=a.belirsizlik,
            durum=a.durum,
        )
        for a in adaylar
        if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, "esleme_adayi", a.id))
    ]


@yonlendirici.get("/kimlik/birlestirmeler", response_model=list[BirlestirmeCevabi])
def birlestirmeler(
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR)),
) -> list[BirlestirmeCevabi]:
    kayitlar = (
        oturum.query(YerBirlestirmesi)
        .filter_by(aktif_mi=True)
        .order_by(YerBirlestirmesi.birlestirme_zamani.desc())
        .limit(200)
        .all()
    )
    return [
        BirlestirmeCevabi(
            id=k.id,
            kaynak_sube_id=k.kaynak_sube_id,
            hedef_sube_id=k.hedef_sube_id,
            birlestirme_zamani=k.birlestirme_zamani,
        )
        for k in kayitlar
        if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, "sube", k.kaynak_sube_id))
    ]


@yonlendirici.get("/claimler", response_model=ClaimSayfasiCevabi)
def claimler(
    aile: str | None = Query(default=None, max_length=40),
    durum: str | None = Query(default=None, max_length=30),
    mekan: str | None = Query(default=None, max_length=120),
    sayfa: int = Query(default=1, ge=1),
    sayfa_boyutu: int = Query(default=25, ge=1, le=100),
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR)),
) -> ClaimSayfasiCevabi:
    sorgu = (
        oturum.query(Iddia, IddiaSurumu, Sube, Yer, IncelemeDosyasi, KanitBaglantisi, Gozlem)
        .join(
            IddiaSurumu,
            (IddiaSurumu.iddia_id == Iddia.id) & (IddiaSurumu.surum_no == Iddia.aktif_surum_no),
        )
        .join(Sube, Sube.id == Iddia.sube_id)
        .join(Yer, Yer.id == Sube.legacy_yer_id)
        .join(
            IncelemeDosyasi,
            (IncelemeDosyasi.nesne_turu == "claim")
            & (IncelemeDosyasi.nesne_id == cast(Iddia.id, String))
            & (IncelemeDosyasi.dosya_turu == "claim_candidate"),
        )
        .join(
            KanitBaglantisi,
            (KanitBaglantisi.iddia_surumu_id == IddiaSurumu.id)
            & (KanitBaglantisi.rol == "supporting"),
        )
        .join(Gozlem, Gozlem.id == KanitBaglantisi.gozlem_id)
    )
    if aile:
        sorgu = sorgu.filter(Iddia.aile == aile)
    if durum:
        sorgu = sorgu.filter(IncelemeDosyasi.durum == durum)
    if mekan:
        sorgu = sorgu.filter(Sube.guncel_isim.ilike(f"%{mekan.strip()}%"))
    satirlar = [
        satir
        for satir in sorgu.order_by(Sube.guncel_isim, Iddia.aile, Iddia.id).all()
        if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, "claim", satir.Iddia.id))
    ]
    toplam = len(satirlar)
    baslangic = (sayfa - 1) * sayfa_boyutu
    kayitlar = []
    for satir in satirlar[baslangic : baslangic + sayfa_boyutu]:
        iddia, surum, sube, yer, dosya, _, gozlem = satir
        kayitlar.append(
            ClaimOzetCevabi(
                id=iddia.id,
                sube_id=iddia.sube_id,
                yer_id=yer.id,
                mekan_adi=sube.guncel_isim,
                aile=iddia.aile,
                aktif_surum_no=iddia.aktif_surum_no,
                durum=dosya.durum,
                risk_sinifi=dosya.risk_sinifi,
                kaynak=gozlem.kaynak,
                kaynak_kayit_id=gozlem.kaynak_kayit_id,
                kaynak_alani=iddia.kapsam.get("kaynak_alani"),
                candidate_deger=surum.deger.get("deger") if isinstance(surum.deger, dict) else None,
            )
        )
    return ClaimSayfasiCevabi(
        kayitlar=kayitlar,
        toplam=toplam,
        sayfa=sayfa,
        sayfa_boyutu=sayfa_boyutu,
    )


@yonlendirici.get("/claimler/{claim_id}", response_model=ClaimIncelemeCevabi)
def claim_detay(
    claim_id: str,
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.CLAIM_INCELE)),
) -> ClaimIncelemeCevabi:
    iddia = oturum.get(Iddia, claim_id)
    if not iddia:
        raise HTTPException(status_code=404, detail="Claim bulunamadi.")
    nesne_yetkisini_dogrula(oturum, baglam, "claim", claim_id)
    sube = oturum.get(Sube, iddia.sube_id)
    yer = oturum.get(Yer, sube.legacy_yer_id) if sube and sube.legacy_yer_id else None
    surum = (
        oturum.query(IddiaSurumu)
        .filter_by(iddia_id=claim_id, surum_no=iddia.aktif_surum_no)
        .first()
    )
    baglar = (
        oturum.query(KanitBaglantisi).filter_by(iddia_surumu_id=surum.id).all() if surum else []
    )
    kanitlar = []
    for bag in baglar:
        gozlem = oturum.get(Gozlem, bag.gozlem_id)
        kanitlar.append(
            {
                "id": bag.id,
                "rol": bag.rol,
                "gerekce": bag.gerekce,
                "gozlem_id": bag.gozlem_id,
                "kaynak": gozlem.kaynak if gozlem else None,
                "kaynak_kayit_id": gozlem.kaynak_kayit_id if gozlem else None,
                "kaynak_url": gozlem.kaynak_url if gozlem else None,
                "cekilme_zamani": gozlem.cekilme_zamani if gozlem else None,
                "icerik_ozeti": gozlem.icerik_ozeti if gozlem else {},
            }
        )
    tarihler = [k["cekilme_zamani"] for k in kanitlar if k["cekilme_zamani"]]
    kaynaklar = sorted({str(k["kaynak"]) for k in kanitlar if k["kaynak"]})
    politikalar = {
        p.kaynak: p
        for p in oturum.query(KaynakPolitikasi).filter(KaynakPolitikasi.kaynak.in_(kaynaklar)).all()
    }
    kaynak_haklari = [
        {
            "kaynak": kaynak,
            "kamusal_gosterim": politikalar[kaynak].kamusal_gosterim
            if kaynak in politikalar
            else "politika_yok",
            "turev_iddia": politikalar[kaynak].turev_iddia
            if kaynak in politikalar
            else "politika_yok",
            "ai_isleme": politikalar[kaynak].ai_isleme if kaynak in politikalar else "politika_yok",
            "uzun_sureli_saklama": politikalar[kaynak].uzun_sureli_saklama
            if kaynak in politikalar
            else "politika_yok",
            "dayanak_notu": politikalar[kaynak].dayanak_notu if kaynak in politikalar else None,
        }
        for kaynak in kaynaklar
    ]
    public_deger = surum.deger.get("deger") if surum and isinstance(surum.deger, dict) else None
    return ClaimIncelemeCevabi(
        id=iddia.id,
        sube_id=iddia.sube_id,
        yer_id=yer.id if yer else None,
        mekan_adi=sube.guncel_isim if sube else "Bilinmeyen sube",
        aile=iddia.aile,
        kapsam=iddia.kapsam,
        aktif_surum_no=iddia.aktif_surum_no,
        surum={
            "id": surum.id,
            "surum_no": surum.surum_no,
            "deger": surum.deger,
            "bilgi_durumu": surum.bilgi_durumu,
            "yayin_durumu": surum.yayin_durumu,
        }
        if surum
        else None,
        supporting_evidence=[k for k in kanitlar if k["rol"] == "supporting"],
        counter_evidence=[k for k in kanitlar if k["rol"] == "counter"],
        kanit_ozeti={
            "observation_sayisi": len(kanitlar),
            "supporting_sayisi": sum(k["rol"] == "supporting" for k in kanitlar),
            "counter_sayisi": sum(k["rol"] == "counter" for k in kanitlar),
            "ilk_tarih": min(tarihler) if tarihler else None,
            "son_tarih": max(tarihler) if tarihler else None,
        },
        kaynak_haklari=kaynak_haklari,
        yayin_onizleme=claim_yayin_onizle(oturum, iddia),
        public_preview={
            "mekan": sube.guncel_isim if sube else None,
            "sube_id": iddia.sube_id,
            "aile": iddia.aile,
            "deger": public_deger,
            "bilgi_durumu": surum.bilgi_durumu if surum else "bilinmiyor",
            "kapsam": iddia.kapsam,
        },
    )


@yonlendirici.post(
    "/incelemeler", response_model=IncelemeDosyasiCevabi, status_code=status.HTTP_201_CREATED
)
def komut_gonder(
    talep: IncelemeKomutu,
    request: Request,
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(admin_baglami_al),
) -> IncelemeDosyasi:
    dosya = inceleme_komutu_gonder(
        oturum,
        baglam=baglam,
        eylem=talep.eylem,
        nesne_turu=talep.nesne_turu,
        nesne_id=talep.nesne_id,
        gerekce=talep.gerekce,
        payload=talep.payload,
        istek_id=_istek_id(request),
        beklenen_surum=talep.beklenen_surum,
    )
    oturum.commit()
    oturum.refresh(dosya)
    return dosya


@yonlendirici.post("/incelemeler/{dosya_id}/ikinci-onay", response_model=IncelemeDosyasiCevabi)
def ikinci_onay(
    dosya_id: str,
    talep: IkinciIncelemeTalebi,
    request: Request,
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(admin_baglami_al),
) -> IncelemeDosyasi:
    dosya = oturum.query(IncelemeDosyasi).filter_by(id=dosya_id).with_for_update().first()
    if not dosya:
        raise HTTPException(status_code=404, detail="Inceleme dosyasi bulunamadi.")
    ikinci_incelemeyi_onayla(
        oturum,
        dosya=dosya,
        baglam=baglam,
        gerekce=talep.gerekce,
        beklenen_surum=talep.beklenen_surum,
        istek_id=_istek_id(request),
    )
    oturum.commit()
    oturum.refresh(dosya)
    return dosya


@yonlendirici.get("/audit", response_model=list[AuditCevabi])
def audit_listele(
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.AUDIT_GOR)),
) -> list[AdminAuditOlayi]:
    olaylar = (
        oturum.query(AdminAuditOlayi)
        .order_by(AdminAuditOlayi.olusturulma_zamani.desc())
        .limit(500)
        .all()
    )
    if not baglam.kullanici.kapsam:
        return olaylar
    return [
        olay
        for olay in olaylar
        if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, olay.nesne_turu, olay.nesne_id))
    ]


@yonlendirici.get("/dahili-sinyaller", response_model=DahiliSinyalSayfasiCevabi)
def dahili_sinyaller(
    aile: str | None = Query(default=None, max_length=50),
    durum: str | None = Query(default=None, max_length=30),
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR)),
) -> DahiliSinyalSayfasiCevabi:
    sorgu = (
        oturum.query(DahiliSinyalOzeti, Sube, Yer)
        .join(Sube, Sube.id == DahiliSinyalOzeti.sube_id)
        .join(Yer, Yer.id == Sube.legacy_yer_id)
    )
    if aile:
        sorgu = sorgu.filter(DahiliSinyalOzeti.aile == aile)
    if durum:
        sorgu = sorgu.filter(DahiliSinyalOzeti.durum == durum)
    kayitlar = []
    for ozet, sube, yer in sorgu.order_by(Sube.guncel_isim, DahiliSinyalOzeti.aile).limit(300):
        if not baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, "sube", sube.id)):
            continue
        govde = dict(ozet.ozet or {})
        kayitlar.append(
            DahiliSinyalOzetCevabi(
                id=ozet.id,
                sube_id=sube.id,
                yer_id=yer.id,
                mekan_adi=yer.isim,
                aile=ozet.aile,
                guven_sinifi=ozet.guven_sinifi,
                durum=ozet.durum,
                preference_eligible=bool(govde.get("preference_eligible")),
                unique_review_count=govde.get("unique_review_count"),
                conflict_level=govde.get("conflict_level"),
            )
        )
    return DahiliSinyalSayfasiCevabi(kayitlar=kayitlar, toplam=len(kayitlar))


@yonlendirici.get("/dahili-sinyaller/{ozet_id}", response_model=DahiliSinyalOzetCevabi)
def dahili_sinyal_detay(
    ozet_id: str,
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR)),
) -> DahiliSinyalOzetCevabi:
    satir = (
        oturum.query(DahiliSinyalOzeti, Sube, Yer)
        .join(Sube, Sube.id == DahiliSinyalOzeti.sube_id)
        .join(Yer, Yer.id == Sube.legacy_yer_id)
        .filter(DahiliSinyalOzeti.id == ozet_id)
        .first()
    )
    if satir is None:
        raise HTTPException(status_code=404, detail="Dahili sinyal bulunamadi.")
    ozet, sube, yer = satir
    nesne_yetkisini_dogrula(oturum, baglam, "sube", sube.id)
    govde = dict(ozet.ozet or {})
    return DahiliSinyalOzetCevabi(
        id=ozet.id,
        sube_id=sube.id,
        yer_id=yer.id,
        mekan_adi=yer.isim,
        aile=ozet.aile,
        guven_sinifi=ozet.guven_sinifi,
        durum=ozet.durum,
        preference_eligible=bool(govde.get("preference_eligible")),
        unique_review_count=govde.get("unique_review_count"),
        conflict_level=govde.get("conflict_level"),
    )


@yonlendirici.post("/gozlemler", response_model=BirinciElGozlemCevabi)
def birinci_el_gozlem(
    talep: BirinciElGozlemTalebi,
    request: Request,
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.CLAIM_INCELE)),
) -> BirinciElGozlemCevabi:
    from sunucu.admin.gozlem_servisi import birinci_el_gozlem_yaz

    sonuc = birinci_el_gozlem_yaz(
        oturum,
        baglam=baglam,
        sube_id=talep.sube_id,
        aile=talep.aile,
        deger=talep.deger,
        ozet=talep.ozet,
        gerekce=talep.gerekce,
        istek_id=_istek_id(request),
    )
    oturum.commit()
    return BirinciElGozlemCevabi(**sonuc)


@yonlendirici.get("/kuyruk/gruplar", response_model=GrupKuyrukCevabi)
def kuyruk_gruplari(
    aile: str | None = Query(default=None, max_length=50),
    pilot: bool = Query(default=False),
    sehir: str = Query(default="Samsun", max_length=80),
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR)),
) -> GrupKuyrukCevabi:
    from sunucu.admin.grup_kuyruk import grup_adaylarini_listele, grup_ozetini_kur
    from sunucu.bilgi.pilot_havuzu import havuzu_sec, sehir_idsini_bul, veritabanindan_adaylar

    sube_idleri = None
    if pilot:
        sehir_id = sehir_idsini_bul(oturum, sehir)
        havuz = havuzu_sec(veritabanindan_adaylar(oturum, sehir_id))
        sube_idleri = {a.sube_id for a in havuz}
    kayitlar = grup_adaylarini_listele(oturum, aile=aile, sube_idleri=sube_idleri)
    kayitlar = [
        k
        for k in kayitlar
        if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, "claim", k["iddia_id"]))
    ]
    return GrupKuyrukCevabi(**grup_ozetini_kur(kayitlar))


@yonlendirici.post("/grup-inceleme", response_model=GrupIncelemeCevabi)
def grup_inceleme(
    talep: GrupIncelemeTalebi,
    request: Request,
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.YAYINLA)),
) -> GrupIncelemeCevabi:
    from sunucu.admin.grup_inceleme import grup_incelemeyi_uygula

    sonuc = grup_incelemeyi_uygula(
        oturum,
        baglam=baglam,
        dosya_idleri=talep.dosya_idleri,
        gerekce=talep.gerekce,
        istek_id=_istek_id(request),
        eylem=talep.eylem,
    )
    oturum.commit()
    return GrupIncelemeCevabi(**sonuc.sozluk())


@yonlendirici.get("/pilot", response_model=PilotOzetCevabi)
def pilot_ozet(
    sehir: str = Query(default="Samsun", max_length=80),
    oturum: Session = Depends(oturum_al),
    baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR)),
) -> PilotOzetCevabi:
    from sunucu.bilgi.pilot_havuzu import (
        gold_sec,
        havuz_ozeti,
        havuzu_sec,
        sehir_idsini_bul,
        veritabanindan_adaylar,
    )
    from sunucu.bilgi.pilot_kapsam import (
        havuz_kapsamini_kur,
        kuyruk_sayimi,
        matris_kolon_ozeti,
        nlp_kapsam_ozeti,
        rota_durum_ozeti,
        rota_simulasyonu,
    )

    sehir_id = sehir_idsini_bul(oturum, sehir)
    if not baglam.kapsam_izinli_mi(sehir_id):
        raise HTTPException(status_code=403, detail="Sehir kapsami disinda.")
    adaylar = veritabanindan_adaylar(oturum, sehir_id)
    havuz = havuzu_sec(adaylar)
    gold = gold_sec(havuz)
    gold_idleri = {a.sube_id for a in gold}
    kayitlar = havuz_kapsamini_kur(oturum, havuz, gold_idleri=gold_idleri)
    return PilotOzetCevabi(
        sehir=sehir,
        havuz=havuz_ozeti(havuz),
        gold_sayisi=len(gold),
        rota_durum=rota_durum_ozeti(kayitlar),
        matris_ozet=matris_kolon_ozeti(kayitlar),
        nlp=nlp_kapsam_ozeti(kayitlar),
        simulasyon=rota_simulasyonu(kayitlar),
        kuyruk=kuyruk_sayimi(oturum),
        kayitlar=kayitlar,
    )
