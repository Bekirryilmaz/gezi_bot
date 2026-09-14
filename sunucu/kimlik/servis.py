from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from sunucu.veritabani.kimlik_modelleri import EslemeAdayi, EslemeKarari, Sube, YerAlias, YerBirlestirmesi, YerKimligi
from sunucu.veritabani.modeller import Yer, YerKaynak


def legacy_yer_icin_kimlik_sagla(oturum: Session, yer: Yer) -> Sube:
    sube = oturum.query(Sube).filter(Sube.legacy_yer_id == yer.id).first()
    if sube:
        return sube
    kimlik = YerKimligi(id=yer.id, sehir_id=yer.sehir_id)
    sube = Sube(id=yer.id, yer_kimligi_id=yer.id, legacy_yer_id=yer.id, guncel_isim=yer.isim)
    oturum.add_all([kimlik, sube, YerAlias(sube_id=yer.id, alias_turu="legacy_yer_id", alias_degeri=str(yer.id))])
    oturum.flush()
    return sube


def alias_coz(oturum: Session, alias_turu: str, alias_degeri: str) -> Sube | None:
    alias = oturum.query(YerAlias).filter_by(alias_turu=alias_turu, alias_degeri=alias_degeri, aktif_mi=True).first()
    if not alias:
        return None
    sube = oturum.get(Sube, alias.sube_id)
    while sube and sube.yonlendirilen_sube_id:
        sube = oturum.get(Sube, sube.yonlendirilen_sube_id)
    return sube


def aday_kaydet(oturum: Session, sol_sube_id: str, sag_sube_id: str, confidence: float, belirsizlik: dict) -> EslemeAdayi:
    sol, sag = sorted((sol_sube_id, sag_sube_id))
    mevcut = oturum.query(EslemeAdayi).filter_by(sol_sube_id=sol, sag_sube_id=sag).first()
    if mevcut:
        return mevcut
    aday = EslemeAdayi(sol_sube_id=sol, sag_sube_id=sag, confidence=confidence, belirsizlik=belirsizlik)
    oturum.add(aday)
    oturum.flush()
    return aday


def birlestir(oturum: Session, aday: EslemeAdayi, hedef_sube_id: str, gerekce: str, *, manuel_override: bool) -> YerBirlestirmesi:
    if not manuel_override and aday.confidence < 0.98:
        raise ValueError("belirsiz esleme kalici birlestirilemez")
    kaynak_id = aday.sag_sube_id if aday.sol_sube_id == hedef_sube_id else aday.sol_sube_id
    karar = EslemeKarari(aday_id=aday.id, karar="kabul", gerekce=gerekce, confidence=aday.confidence, manuel_override=manuel_override)
    oturum.add(karar); oturum.flush()
    kaynaklar = oturum.query(YerKaynak).filter(YerKaynak.sube_id == kaynak_id).all()
    tasinan = [str(k.id) for k in kaynaklar]
    for kaynak in kaynaklar:
        kaynak.sube_id = hedef_sube_id
    kaynak_sube = oturum.get(Sube, kaynak_id)
    kaynak_sube.durum = "birlestirildi"; kaynak_sube.yonlendirilen_sube_id = hedef_sube_id
    kayit = YerBirlestirmesi(kaynak_sube_id=kaynak_id, hedef_sube_id=hedef_sube_id, karar_id=karar.id, tasinan_kaynak_idleri=tasinan)
    oturum.add(kayit); aday.durum = "kabul"; oturum.flush()
    return kayit


def bol(oturum: Session, birlesme: YerBirlestirmesi, gerekce: str, *, manuel_override: bool = True) -> EslemeKarari:
    if not birlesme.aktif_mi:
        raise ValueError("birlesme zaten geri alinmis")
    oturum.query(YerKaynak).filter(YerKaynak.id.in_(birlesme.tasinan_kaynak_idleri)).update({YerKaynak.sube_id: birlesme.kaynak_sube_id}, synchronize_session=False)
    kaynak = oturum.get(Sube, birlesme.kaynak_sube_id)
    kaynak.durum = "aktif"; kaynak.yonlendirilen_sube_id = None
    birlesme.aktif_mi = False; birlesme.geri_alinma_zamani = datetime.now(timezone.utc)
    karar = EslemeKarari(aday_id=None, karar="split", gerekce=gerekce, manuel_override=manuel_override)
    oturum.add(karar); oturum.flush()
    return karar

