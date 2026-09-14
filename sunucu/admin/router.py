from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from sunucu.admin.semalar import AdminKimlikCevabi, AdminLoginTalebi, AuditCevabi, BirlestirmeCevabi, ClaimIncelemeCevabi, ClaimOzetCevabi, EslemeAdayiCevabi, IkinciIncelemeTalebi, IncelemeDosyasiCevabi, IncelemeKomutu
from sunucu.admin.workflow import claim_yayin_onizle, inceleme_komutu_gonder, ikinci_incelemeyi_onayla, nesne_sehir_id, nesne_yetkisini_dogrula
from sunucu.auth.rbac import Yetki
from sunucu.auth.servis import CSRF_COOKIE, OTURUM_COOKIE, AdminBaglami, admin_baglami_al, oturum_ac, parola_dogrula, yetki_gerekli
from sunucu.veritabani.admin_modelleri import AdminAuditOlayi, AdminKullanici, IncelemeDosyasi
from sunucu.veritabani.baglanti import oturum_al
from sunucu.veritabani.bilgi_modelleri import Gozlem, Iddia, IddiaSurumu, KanitBaglantisi
from sunucu.veritabani.kimlik_modelleri import EslemeAdayi, YerBirlestirmesi

yonlendirici = APIRouter()


def _istek_id(request: Request) -> str:
    return getattr(request.state, "request_id", None) or request.headers.get("X-Request-ID") or str(uuid.uuid4())


@yonlendirici.post("/login", response_model=AdminKimlikCevabi)
def login(talep: AdminLoginTalebi, request: Request, yanit: Response, oturum: Session = Depends(oturum_al)) -> AdminKimlikCevabi:
    kullanici = oturum.query(AdminKullanici).filter_by(eposta=talep.eposta.strip().lower(), aktif_mi=True).first()
    if not kullanici or not parola_dogrula(talep.parola, kullanici):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-posta veya parola gecersiz.")
    kayit, token, csrf = oturum_ac(oturum, kullanici, ip=request.client.host if request.client else None, user_agent=request.headers.get("user-agent"))
    oturum.commit()
    guvenli = os.environ.get("UYGULAMA_ORTAMI", "development").lower() in {"production", "prod", "canli"}
    yanit.set_cookie(OTURUM_COOKIE, token, httponly=True, secure=guvenli, samesite="strict", max_age=max(0, int((kayit.sona_erme_zamani - datetime.now(timezone.utc)).total_seconds())), path="/")
    yanit.set_cookie(CSRF_COOKIE, csrf, httponly=False, secure=guvenli, samesite="strict", max_age=max(0, int((kayit.sona_erme_zamani - datetime.now(timezone.utc)).total_seconds())), path="/")
    roller = sorted({satir[0] for satir in oturum.query(__import__("sunucu.veritabani.admin_modelleri", fromlist=["AdminRol"]).AdminRol.kod).join(__import__("sunucu.veritabani.admin_modelleri", fromlist=["AdminKullaniciRolu"]).AdminKullaniciRolu).filter(__import__("sunucu.veritabani.admin_modelleri", fromlist=["AdminKullaniciRolu"]).AdminKullaniciRolu.kullanici_id == kullanici.id).all()})
    from sunucu.auth.rbac import yetkileri_birlestir
    return AdminKimlikCevabi(id=kullanici.id, eposta=kullanici.eposta, gorunen_ad=kullanici.gorunen_ad, roller=roller, yetkiler=sorted(y.value for y in yetkileri_birlestir(set(roller))), csrf_token=csrf)


@yonlendirici.get("/me", response_model=AdminKimlikCevabi)
def me(baglam: AdminBaglami = Depends(admin_baglami_al)) -> AdminKimlikCevabi:
    return AdminKimlikCevabi(id=baglam.kullanici.id, eposta=baglam.kullanici.eposta, gorunen_ad=baglam.kullanici.gorunen_ad, roller=sorted(baglam.roller), yetkiler=sorted(y.value for y in baglam.yetkiler))


@yonlendirici.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(yanit: Response, oturum: Session = Depends(oturum_al), baglam: AdminBaglami = Depends(admin_baglami_al)) -> None:
    baglam.oturum.iptal_zamani = datetime.now(timezone.utc)
    oturum.commit()
    yanit.delete_cookie(OTURUM_COOKIE, path="/")
    yanit.delete_cookie(CSRF_COOKIE, path="/")


@yonlendirici.get("/kuyruk", response_model=list[IncelemeDosyasiCevabi])
def kuyruk(oturum: Session = Depends(oturum_al), baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR))) -> list[IncelemeDosyasi]:
    sorgu = oturum.query(IncelemeDosyasi).filter(IncelemeDosyasi.durum != "tamamlandi")
    dosyalar = sorgu.order_by(IncelemeDosyasi.risk_sinifi.desc(), IncelemeDosyasi.olusturulma_zamani).limit(200).all()
    return [d for d in dosyalar if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, d.nesne_turu, d.nesne_id))]


@yonlendirici.get("/kimlik/esleme-adaylari", response_model=list[EslemeAdayiCevabi])
def esleme_adaylari(oturum: Session = Depends(oturum_al), baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR))) -> list[EslemeAdayiCevabi]:
    adaylar = oturum.query(EslemeAdayi).filter_by(durum="bekliyor").order_by(EslemeAdayi.confidence.desc()).limit(200).all()
    return [EslemeAdayiCevabi(id=a.id, sol_sube_id=a.sol_sube_id, sag_sube_id=a.sag_sube_id, confidence=a.confidence, belirsizlik=a.belirsizlik, durum=a.durum) for a in adaylar if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, "esleme_adayi", a.id))]


@yonlendirici.get("/kimlik/birlestirmeler", response_model=list[BirlestirmeCevabi])
def birlestirmeler(oturum: Session = Depends(oturum_al), baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR))) -> list[BirlestirmeCevabi]:
    kayitlar = oturum.query(YerBirlestirmesi).filter_by(aktif_mi=True).order_by(YerBirlestirmesi.birlestirme_zamani.desc()).limit(200).all()
    return [BirlestirmeCevabi(id=k.id, kaynak_sube_id=k.kaynak_sube_id, hedef_sube_id=k.hedef_sube_id, birlestirme_zamani=k.birlestirme_zamani) for k in kayitlar if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, "sube", k.kaynak_sube_id))]


@yonlendirici.get("/claimler", response_model=list[ClaimOzetCevabi])
def claimler(oturum: Session = Depends(oturum_al), baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.INCELEME_GOR))) -> list[ClaimOzetCevabi]:
    kayitlar = oturum.query(Iddia).order_by(Iddia.olusturulma_zamani.desc()).limit(200).all()
    return [ClaimOzetCevabi(id=k.id, sube_id=k.sube_id, aile=k.aile, aktif_surum_no=k.aktif_surum_no) for k in kayitlar if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, "claim", k.id))]


@yonlendirici.get("/claimler/{claim_id}", response_model=ClaimIncelemeCevabi)
def claim_detay(claim_id: str, oturum: Session = Depends(oturum_al), baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.CLAIM_INCELE))) -> ClaimIncelemeCevabi:
    iddia = oturum.get(Iddia, claim_id)
    if not iddia:
        raise HTTPException(status_code=404, detail="Claim bulunamadi.")
    nesne_yetkisini_dogrula(oturum, baglam, "claim", claim_id)
    surum = oturum.query(IddiaSurumu).filter_by(iddia_id=claim_id, surum_no=iddia.aktif_surum_no).first()
    baglar = oturum.query(KanitBaglantisi).filter_by(iddia_surumu_id=surum.id).all() if surum else []
    kanitlar = []
    for bag in baglar:
        gozlem = oturum.get(Gozlem, bag.gozlem_id)
        kanitlar.append({"id": bag.id, "rol": bag.rol, "gerekce": bag.gerekce, "gozlem_id": bag.gozlem_id, "kaynak": gozlem.kaynak if gozlem else None, "icerik_ozeti": gozlem.icerik_ozeti if gozlem else {}})
    return ClaimIncelemeCevabi(id=iddia.id, sube_id=iddia.sube_id, aile=iddia.aile, kapsam=iddia.kapsam, aktif_surum_no=iddia.aktif_surum_no, surum={"id": surum.id, "surum_no": surum.surum_no, "deger": surum.deger, "bilgi_durumu": surum.bilgi_durumu, "yayin_durumu": surum.yayin_durumu} if surum else None, supporting_evidence=[k for k in kanitlar if k["rol"] == "supporting"], counter_evidence=[k for k in kanitlar if k["rol"] == "counter"], yayin_onizleme=claim_yayin_onizle(oturum, iddia))


@yonlendirici.post("/incelemeler", response_model=IncelemeDosyasiCevabi, status_code=status.HTTP_201_CREATED)
def komut_gonder(talep: IncelemeKomutu, request: Request, oturum: Session = Depends(oturum_al), baglam: AdminBaglami = Depends(admin_baglami_al)) -> IncelemeDosyasi:
    dosya = inceleme_komutu_gonder(oturum, baglam=baglam, eylem=talep.eylem, nesne_turu=talep.nesne_turu, nesne_id=talep.nesne_id, gerekce=talep.gerekce, payload=talep.payload, istek_id=_istek_id(request), beklenen_surum=talep.beklenen_surum)
    oturum.commit()
    oturum.refresh(dosya)
    return dosya


@yonlendirici.post("/incelemeler/{dosya_id}/ikinci-onay", response_model=IncelemeDosyasiCevabi)
def ikinci_onay(dosya_id: str, talep: IkinciIncelemeTalebi, request: Request, oturum: Session = Depends(oturum_al), baglam: AdminBaglami = Depends(admin_baglami_al)) -> IncelemeDosyasi:
    dosya = oturum.query(IncelemeDosyasi).filter_by(id=dosya_id).with_for_update().first()
    if not dosya:
        raise HTTPException(status_code=404, detail="Inceleme dosyasi bulunamadi.")
    ikinci_incelemeyi_onayla(oturum, dosya=dosya, baglam=baglam, gerekce=talep.gerekce, beklenen_surum=talep.beklenen_surum, istek_id=_istek_id(request))
    oturum.commit()
    oturum.refresh(dosya)
    return dosya


@yonlendirici.get("/audit", response_model=list[AuditCevabi])
def audit_listele(oturum: Session = Depends(oturum_al), baglam: AdminBaglami = Depends(yetki_gerekli(Yetki.AUDIT_GOR))) -> list[AdminAuditOlayi]:
    olaylar = oturum.query(AdminAuditOlayi).order_by(AdminAuditOlayi.olusturulma_zamani.desc()).limit(500).all()
    if not baglam.kullanici.kapsam:
        return olaylar
    return [olay for olay in olaylar if baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, olay.nesne_turu, olay.nesne_id))]
