from __future__ import annotations

from dataclasses import asdict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from sunucu.admin.audit import audit_yaz
from sunucu.auth.rbac import KRITIK_EYLEMLER, Yetki
from sunucu.auth.servis import AdminBaglami
from sunucu.bilgi.domain import BilgiDurumu, HakDurumu
from sunucu.kimlik.servis import birlestir, bol
from sunucu.veritabani.admin_modelleri import IncelemeDosyasi
from sunucu.veritabani.bilgi_modelleri import Gozlem, Iddia, IddiaSurumu, KanitBaglantisi, KaynakPolitikasi
from sunucu.veritabani.kimlik_modelleri import EslemeAdayi, EslemeKarari, Sube, YerBirlestirmesi, YerKimligi
from sunucu.veritabani.yayin_modelleri import EtkiBaglantisi, YayinKaydi
from sunucu.yayin.domain import KullanimTuru, YayinGirdisi, YayinUygunlukDurumu, yayin_uygunlugunu_degerlendir
from sunucu.yayin.servis import etki_bagi_ekle, gecersizlestirme_olayi_uret, geri_cek, olayi_isle

EYLEM_YETKISI = {
    "esleme_reddet": Yetki.KIMLIK_DUZENLE,
    "canonical_merge": Yetki.KRITIK_MERGE_SPLIT,
    "split": Yetki.KRITIK_MERGE_SPLIT,
    "claim_approve": Yetki.YAYINLA,
    "kritik_claim_yayini": Yetki.YAYINLA,
    "claim_limit": Yetki.CLAIM_INCELE,
    "claim_stale": Yetki.CLAIM_INCELE,
    "withdraw": Yetki.GERI_CEK,
    "hak_degisikligi": Yetki.HAK_DEGISTIR,
}
KRITIK_CLAIM_AILELERI = frozenset({"giris_basamak", "fiziksel_erisim", "calisma_saati", "ziyaret_kosulu"})


def nesne_sehir_id(oturum: Session, nesne_turu: str, nesne_id: str) -> str | None:
    if nesne_turu == "claim":
        iddia = oturum.get(Iddia, nesne_id)
        sube = oturum.get(Sube, iddia.sube_id) if iddia else None
        kimlik = oturum.get(YerKimligi, sube.yer_kimligi_id) if sube else None
        return str(kimlik.sehir_id) if kimlik else None
    if nesne_turu in {"sube", "yer"}:
        sube = oturum.get(Sube, nesne_id)
        kimlik = oturum.get(YerKimligi, sube.yer_kimligi_id) if sube else None
        return str(kimlik.sehir_id) if kimlik else None
    if nesne_turu == "esleme_adayi":
        aday = oturum.get(EslemeAdayi, nesne_id)
        return nesne_sehir_id(oturum, "sube", aday.sol_sube_id) if aday else None
    return None


def nesne_yetkisini_dogrula(oturum: Session, baglam: AdminBaglami, nesne_turu: str, nesne_id: str) -> None:
    if not baglam.kapsam_izinli_mi(nesne_sehir_id(oturum, nesne_turu, nesne_id)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bu nesne admin kapsamınızda degil.")


def claim_yayin_onizle(oturum: Session, iddia: Iddia, kullanim: KullanimTuru = KullanimTuru.DETAY) -> dict:
    sube = oturum.get(Sube, iddia.sube_id)
    kimlik = oturum.get(YerKimligi, sube.yer_kimligi_id) if sube else None
    surum = oturum.query(IddiaSurumu).filter_by(iddia_id=iddia.id, surum_no=iddia.aktif_surum_no).first()
    baglar = oturum.query(KanitBaglantisi).filter_by(iddia_surumu_id=surum.id).all() if surum else []
    destekler = [bag for bag in baglar if bag.rol == "supporting"]
    haklar: list[str] = []
    for bag in destekler:
        gozlem = oturum.get(Gozlem, bag.gozlem_id)
        politika = oturum.query(KaynakPolitikasi).filter_by(kaynak=gozlem.kaynak).first() if gozlem else None
        haklar.append(politika.turev_iddia if politika else HakDurumu.BILINMIYOR.value)
    hak = HakDurumu.IZINLI if haklar and all(deger == HakDurumu.IZINLI.value for deger in haklar) else (HakDurumu.YASAK if any(deger == HakDurumu.YASAK.value for deger in haklar) else HakDurumu.BILINMIYOR)
    girdi = YayinGirdisi(
        canonical_gecerli=bool(kimlik and kimlik.durum == "aktif"),
        sube_gecerli=bool(sube and sube.durum == "aktif" and not sube.yonlendirilen_sube_id),
        iddia_aktif=bool(iddia.aktif_surum_no),
        surum_gecerli=bool(surum and surum.yayin_durumu != "geri_cekilmis"),
        hak_durumu=hak,
        bilgi_durumu=BilgiDurumu(surum.bilgi_durumu) if surum else BilgiDurumu.BILINMIYOR,
        geri_cekilmis=bool(surum and surum.yayin_durumu == "geri_cekilmis"),
        gecerlilik_baslangici=surum.gecerlilik_baslangici if surum else None,
        gecerlilik_bitisi=surum.gecerlilik_bitisi if surum else None,
        sinirli=bool(surum and surum.yayin_durumu == "sinirli"),
    )
    sonuc = yayin_uygunlugunu_degerlendir(girdi, kullanim)
    return {"durum": sonuc.durum.value, "neden_kodlari": [neden.value for neden in sonuc.nedenler], "kullanim": kullanim.value, "etkilenen_public_alanlar": ["yer_detay", "yer_liste", "arama", "rota_adayi", "paylasim", "cache"]}


def _yayin_kaydi_guncelle(oturum: Session, *, nesne_turu: str, nesne_id: str, durum: str, nedenler: list[str]) -> YayinKaydi:
    kayit = oturum.query(YayinKaydi).filter_by(nesne_turu=nesne_turu, nesne_id=nesne_id).with_for_update().first()
    if not kayit:
        kayit = YayinKaydi(nesne_turu=nesne_turu, nesne_id=nesne_id, durum=durum, neden_kodlari=nedenler, izinli_kullanimlar=[k.value for k in KullanimTuru])
        oturum.add(kayit)
    else:
        kayit.durum = durum
        kayit.neden_kodlari = nedenler
        kayit.surum += 1
    oturum.flush()
    return kayit


def _komutu_uygula(oturum: Session, dosya: IncelemeDosyasi, aktor_id: str, gerekce: str, istek_id: str) -> dict:
    eylem, payload = dosya.onerilen_eylem or "", dosya.komut_payload or {}
    onceki: dict = {"durum": dosya.durum, "surum": dosya.surum}
    if eylem == "esleme_reddet":
        aday = oturum.get(EslemeAdayi, dosya.nesne_id)
        if not aday:
            raise HTTPException(status_code=404, detail="Esleme adayi bulunamadi.")
        aday.durum = "red"
        oturum.add(EslemeKarari(aday_id=aday.id, karar="red", gerekce=gerekce, confidence=aday.confidence, manuel_override=True))
    elif eylem == "canonical_merge":
        aday = oturum.get(EslemeAdayi, dosya.nesne_id)
        if not aday:
            raise HTTPException(status_code=404, detail="Esleme adayi bulunamadi.")
        kayit = birlestir(oturum, aday, payload["hedef_sube_id"], gerekce, manuel_override=True)
        for sube_id in {aday.sol_sube_id, aday.sag_sube_id}:
            olay = gecersizlestirme_olayi_uret(oturum, olay_anahtari=f"merge:{kayit.id}:{sube_id}", kaynak_turu="yer", kaynak_id=sube_id, olay_turu="canonical_merge")
            olayi_isle(oturum, olay)
    elif eylem == "split":
        birlesme = oturum.get(YerBirlestirmesi, payload.get("birlesme_id", dosya.nesne_id))
        if not birlesme:
            raise HTTPException(status_code=404, detail="Birlestirme kaydi bulunamadi.")
        bol(oturum, birlesme, gerekce)
        olay = gecersizlestirme_olayi_uret(oturum, olay_anahtari=f"split:{birlesme.id}:{dosya.id}", kaynak_turu="yer", kaynak_id=birlesme.kaynak_sube_id, olay_turu="split")
        olayi_isle(oturum, olay)
    elif eylem in {"claim_approve", "kritik_claim_yayini", "claim_limit", "claim_stale"}:
        iddia = oturum.get(Iddia, dosya.nesne_id)
        if not iddia:
            raise HTTPException(status_code=404, detail="Claim bulunamadi.")
        surum = oturum.query(IddiaSurumu).filter_by(iddia_id=iddia.id, surum_no=iddia.aktif_surum_no).with_for_update().first()
        if not surum:
            raise HTTPException(status_code=409, detail="Claim aktif surumu yok.")
        onizleme = claim_yayin_onizle(oturum, iddia)
        if eylem in {"claim_approve", "kritik_claim_yayini"} and onizleme["durum"] not in {YayinUygunlukDurumu.YAYINLANABILIR.value, YayinUygunlukDurumu.SINIRLI_YAYINLANABILIR.value}:
            raise HTTPException(status_code=409, detail={"mesaj": "Claim yayin kapisini gecemedi.", **onizleme})
        if eylem in {"claim_approve", "kritik_claim_yayini"}:
            surum.yayin_durumu = "yayinlandi"
            durum, nedenler = YayinUygunlukDurumu.YAYINLANABILIR.value, ["admin_onayli"]
        elif eylem == "claim_limit":
            surum.yayin_durumu = "sinirli"
            durum, nedenler = YayinUygunlukDurumu.SINIRLI_YAYINLANABILIR.value, [payload.get("sinir_kodu", "admin_sinirli")]
        else:
            surum.bilgi_durumu = BilgiDurumu.ESKIMIS.value
            surum.yayin_durumu = "yeniden_dogrulama"
            durum, nedenler = YayinUygunlukDurumu.YENIDEN_DOGRULAMA_GEREKLI.value, ["eskimis"]
        _yayin_kaydi_guncelle(oturum, nesne_turu="claim", nesne_id=iddia.id, durum=durum, nedenler=nedenler)
        sube = oturum.get(Sube, iddia.sube_id)
        if sube and sube.legacy_yer_id:
            etki_bagi_ekle(oturum, "claim", iddia.id, "yer", sube.legacy_yer_id, "place_projection")
        olay = gecersizlestirme_olayi_uret(oturum, olay_anahtari=f"claim:{iddia.id}:{dosya.id}:{eylem}", kaynak_turu="claim", kaynak_id=iddia.id, olay_turu=eylem)
        olayi_isle(oturum, olay)
    elif eylem == "withdraw":
        geri_cek(oturum, nesne_turu=dosya.nesne_turu, nesne_id=dosya.nesne_id, aktor_id=aktor_id, gerekce_kodu=payload.get("gerekce_kodu", "admin_geri_cekme"), gerekce=gerekce, kapsam=payload.get("kapsam"), istek_id=istek_id)
        if dosya.nesne_turu == "claim":
            iddia = oturum.get(Iddia, dosya.nesne_id)
            surum = oturum.query(IddiaSurumu).filter_by(iddia_id=iddia.id, surum_no=iddia.aktif_surum_no).first() if iddia else None
            if surum:
                surum.yayin_durumu = "geri_cekilmis"
                surum.bilgi_durumu = BilgiDurumu.GERI_CEKILMIS.value
    elif eylem == "hak_degisikligi":
        politika = oturum.get(KaynakPolitikasi, dosya.nesne_id)
        if not politika:
            raise HTTPException(status_code=404, detail="Kaynak politikasi bulunamadi.")
        alan = payload.get("alan")
        if alan not in {"kamusal_gosterim", "turev_iddia", "ai_isleme", "uzun_sureli_saklama"}:
            raise HTTPException(status_code=422, detail="Gecersiz hak alani.")
        setattr(politika, alan, HakDurumu(payload["deger"]).value)
    else:
        raise HTTPException(status_code=422, detail="Desteklenmeyen admin eylemi.")
    dosya.durum = "tamamlandi"
    dosya.karar_gerekcesi = gerekce
    dosya.surum += 1
    yeni = {"durum": dosya.durum, "surum": dosya.surum, "eylem": eylem}
    audit_yaz(oturum, aktor_id=aktor_id, eylem=eylem, nesne_turu=dosya.nesne_turu, nesne_id=dosya.nesne_id, onceki=onceki, yeni=yeni, gerekce=gerekce, istek_id=istek_id, meta={"inceleme_dosyasi_id": str(dosya.id)})
    oturum.flush()
    return yeni


def inceleme_komutu_gonder(oturum: Session, *, baglam: AdminBaglami, eylem: str, nesne_turu: str, nesne_id: str, gerekce: str, payload: dict, istek_id: str, beklenen_surum: int | None = None) -> IncelemeDosyasi:
    if eylem == "claim_approve":
        iddia = oturum.get(Iddia, nesne_id)
        if iddia and iddia.aile in KRITIK_CLAIM_AILELERI:
            eylem = "kritik_claim_yayini"
    gerekli = EYLEM_YETKISI.get(eylem)
    if not gerekli or gerekli not in baglam.yetkiler:
        raise HTTPException(status_code=403, detail="Bu admin eylemi icin yetkiniz yok.")
    nesne_yetkisini_dogrula(oturum, baglam, nesne_turu, nesne_id)
    kritik = eylem in KRITIK_EYLEMLER
    dosya = IncelemeDosyasi(dosya_turu="kimlik" if "merge" in eylem or eylem == "split" or eylem == "esleme_reddet" else "claim", nesne_turu=nesne_turu, nesne_id=nesne_id, durum="ikinci_inceleme_bekliyor" if kritik else "isleniyor", risk_sinifi="kritik" if kritik else "normal", onerilen_eylem=eylem, komut_payload=payload, acan_aktor_id=baglam.kullanici.id, karar_gerekcesi=gerekce)
    oturum.add(dosya)
    oturum.flush()
    audit_yaz(oturum, aktor_id=baglam.kullanici.id, eylem="inceleme_talebi", nesne_turu=nesne_turu, nesne_id=nesne_id, onceki=None, yeni={"dosya_id": str(dosya.id), "eylem": eylem, "risk": dosya.risk_sinifi}, gerekce=gerekce, istek_id=istek_id)
    if not kritik:
        _komutu_uygula(oturum, dosya, baglam.kullanici.id, gerekce, istek_id)
    return dosya


def ikinci_incelemeyi_onayla(oturum: Session, *, dosya: IncelemeDosyasi, baglam: AdminBaglami, gerekce: str, beklenen_surum: int, istek_id: str) -> IncelemeDosyasi:
    if Yetki.IKINCI_INCELE not in baglam.yetkiler:
        raise HTTPException(status_code=403, detail="Ikinci inceleme yetkisi gerekli.")
    if str(dosya.acan_aktor_id) == str(baglam.kullanici.id):
        raise HTTPException(status_code=409, detail="Islem sahibi kendi kritik islemini onaylayamaz.")
    if dosya.durum != "ikinci_inceleme_bekliyor":
        raise HTTPException(status_code=409, detail="Dosya ikinci inceleme beklemiyor.")
    if dosya.surum != beklenen_surum:
        raise HTTPException(status_code=409, detail="Inceleme dosyasi baska bir islemle degisti.")
    nesne_yetkisini_dogrula(oturum, baglam, dosya.nesne_turu, dosya.nesne_id)
    dosya.ikinci_inceleyen_id = baglam.kullanici.id
    _komutu_uygula(oturum, dosya, baglam.kullanici.id, gerekce, istek_id)
    return dosya
