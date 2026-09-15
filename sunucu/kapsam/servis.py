from __future__ import annotations

import hashlib

from sqlalchemy import and_, select
from sqlalchemy.orm import Session, aliased

from sunucu.bilgi.domain import BilgiDurumu
from sunucu.kapsam.semalar import (
    DuzeltmeGirisiSemasi,
    IlceDetayiSemasi,
    IlceKapsamiSemasi,
    KamusalCografyaSemasi,
    KamusalYerDetayiSemasi,
    SehirKapsamiSemasi,
    YayimlanmisBilgiSemasi,
)
from sunucu.karar_motoru.semalar import KararBaglamiSemasi, KararSonucuSemasi, YerKimligiSemasi
from sunucu.karar_motoru.servis import adaylari_toplu_getir
from sunucu.karar_motoru.domain import KararMotoru
from sunucu.veritabani.arama_modelleri import Ilce
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu
from sunucu.veritabani.kimlik_modelleri import Sube, YerKimligi
from sunucu.veritabani.modeller import Sehir, Yer
from sunucu.veritabani.sorgular import yer_ve_koordinat_getir
from sunucu.veritabani.yayin_modelleri import PublicProjection, YayinKaydi
from sunucu.yayin.domain import KullanimTuru
from sunucu.yayin.servis import KAMUSAL_DURUMLAR
from veri.ortak.sehir_ayarlari import sehir_anahtarini_isme_gore_bul


def _slug(metin: str) -> str:
    from sunucu.arama.normalizasyon import turkce_arama_normalize

    return turkce_arama_normalize(metin).replace(" ", "-")


def _sehir_bul(oturum: Session, anahtar: str) -> Sehir:
    from sunucu.arama.normalizasyon import turkce_arama_normalize

    sehir = oturum.scalar(
        select(Sehir).where(Sehir.aktif_mi.is_(True), Sehir.arama_isim == turkce_arama_normalize(anahtar))
    )
    if sehir is None:
        raise LookupError("Şehir kapsamı bulunamadı.")
    return sehir


def _kamusal_yayin(kullanim: KullanimTuru):
    return (
        YayinKaydi.aktif_mi.is_(True),
        YayinKaydi.durum.in_(KAMUSAL_DURUMLAR),
        YayinKaydi.izinli_kullanimlar.contains([kullanim.value]),
    )


def _ilce_projection(oturum: Session, ilce_id: str) -> tuple[YayinKaydi, PublicProjection] | None:
    satir = oturum.execute(
        select(YayinKaydi, PublicProjection)
        .join(PublicProjection, and_(PublicProjection.nesne_turu == "ilce", PublicProjection.nesne_id == YayinKaydi.nesne_id))
        .where(
            YayinKaydi.nesne_turu == "ilce",
            YayinKaydi.nesne_id == ilce_id,
            PublicProjection.gecersiz_mi.is_(False),
            *_kamusal_yayin(KullanimTuru.DETAY),
        )
    ).first()
    return (satir.YayinKaydi, satir.PublicProjection) if satir else None


def sehir_kapsami_getir(oturum: Session, anahtar: str) -> SehirKapsamiSemasi:
    sehir = _sehir_bul(oturum, anahtar)
    yer_yayini = aliased(YayinKaydi, name="yer_yayini")
    yer_satirlari = oturum.execute(
        select(Yer.ilce_id, Yer.ana_kategori, Yer.alt_kategori, yer_yayini.surum)
        .join(yer_yayini, and_(yer_yayini.nesne_turu == "yer", yer_yayini.nesne_id == Yer.id))
        .where(
            Yer.sehir_id == sehir.id,
            yer_yayini.aktif_mi.is_(True),
            yer_yayini.durum.in_(KAMUSAL_DURUMLAR),
            yer_yayini.izinli_kullanimlar.contains([KullanimTuru.KESFET.value]),
        )
    ).all()
    ilceler = oturum.scalars(
        select(Ilce).where(Ilce.sehir_id == sehir.id, Ilce.aktif_mi.is_(True)).order_by(Ilce.isim)
    ).all()
    ilce_projection_idleri = set(
        oturum.scalars(
            select(YayinKaydi.nesne_id)
            .join(
                PublicProjection,
                and_(
                    PublicProjection.nesne_turu == "ilce",
                    PublicProjection.nesne_id == YayinKaydi.nesne_id,
                    PublicProjection.gecersiz_mi.is_(False),
                ),
            )
            .where(YayinKaydi.nesne_turu == "ilce", *_kamusal_yayin(KullanimTuru.DETAY))
        ).all()
    )
    ilce_turleri: dict[str, set[str]] = {str(ilce.id): set() for ilce in ilceler}
    for satir in yer_satirlari:
        if satir.ilce_id is not None:
            ilce_turleri.setdefault(str(satir.ilce_id), set()).add(satir.alt_kategori or satir.ana_kategori)

    claim_yayini = aliased(YayinKaydi, name="claim_yayini")
    claim_aileleri = set(
        oturum.scalars(
            select(Iddia.aile)
            .join(Sube, Sube.id == Iddia.sube_id)
            .join(YerKimligi, YerKimligi.id == Sube.yer_kimligi_id)
            .join(IddiaSurumu, and_(IddiaSurumu.iddia_id == Iddia.id, IddiaSurumu.surum_no == Iddia.aktif_surum_no))
            .join(claim_yayini, and_(claim_yayini.nesne_turu == "claim", claim_yayini.nesne_id == Iddia.id))
            .where(
                YerKimligi.sehir_id == sehir.id,
                IddiaSurumu.bilgi_durumu == BilgiDurumu.BILINIYOR.value,
                claim_yayini.aktif_mi.is_(True),
                claim_yayini.durum.in_(KAMUSAL_DURUMLAR),
                claim_yayini.izinli_kullanimlar.contains([KullanimTuru.KARAR.value]),
            )
            .distinct()
        ).all()
    )
    sehir_anahtari = sehir_anahtarini_isme_gore_bul(sehir.isim) or _slug(sehir.isim)
    ilce_cevaplari = []
    projection_idleri = {str(x) for x in ilce_projection_idleri}
    for ilce in ilceler:
        kimlik = str(ilce.id)
        turler = sorted(ilce_turleri.get(kimlik, set()))
        if not turler and kimlik not in projection_idleri:
            continue
        ilce_cevaplari.append(
            IlceKapsamiSemasi(
                id=kimlik,
                isim=ilce.isim,
                slug=_slug(ilce.isim),
                yayinlanmis_yer_turleri=turler,
                ayri_sayfa_var=kimlik in projection_idleri,
                kesfet_url=f"/sehir/{sehir_anahtari}?ilce={kimlik}",
            )
        )
    surum_ham = ":".join(str(s.surum) for s in yer_satirlari) + ":" + ":".join(sorted(claim_aileleri))
    karar_var = bool(claim_aileleri)
    return SehirKapsamiSemasi(
        sehir_id=str(sehir.id),
        sehir_anahtari=sehir_anahtari,
        sehir_ismi=sehir.isim,
        manifest_surumu=hashlib.sha256(surum_ham.encode()).hexdigest()[:16],
        kimlik_aramasi_destekleniyor=bool(yer_satirlari),
        karar_kapsami_destekleniyor=karar_var,
        yayinlanmis_yer_sayisi=len(yer_satirlari),
        desteklenen_yer_turleri=sorted({s.alt_kategori or s.ana_kategori for s in yer_satirlari}),
        desteklenen_iddia_aileleri=sorted(claim_aileleri),
        ilceler=ilce_cevaplari,
        kapsam_aciklamasi=(
            "Bu şehirde yayımlanmış karar bilgisine dayanan ihtiyaç değerlendirmeleri var."
            if karar_var
            else "Yer kimlikleri aranabilir; ziyaret koşullarına ilişkin yayımlanmış claim bulunmadığı için uygunluğu henüz doğrulayamıyoruz."
        ),
    )


def ilce_detayi_getir(oturum: Session, anahtar: str, ilce_id: str) -> IlceDetayiSemasi:
    sehir = _sehir_bul(oturum, anahtar)
    ilce = oturum.scalar(select(Ilce).where(Ilce.id == ilce_id, Ilce.aktif_mi.is_(True)))
    if ilce is None or str(ilce.sehir_id) != str(sehir.id):
        raise LookupError("İlçe bu şehrin canonical kapsamında bulunamadı.")
    sehir_anahtari = sehir_anahtarini_isme_gore_bul(sehir.isim) or _slug(sehir.isim)
    projection = _ilce_projection(oturum, str(ilce.id))
    payload = projection[1].payload if projection else {}
    bilgiler = [x for x in payload.get("ozgun_karar_bilgileri", []) if isinstance(x, str)]
    turler = sorted(
        {
            tur
            for tur in
            oturum.scalars(
                select(Yer.alt_kategori)
                .join(YayinKaydi, and_(YayinKaydi.nesne_turu == "yer", YayinKaydi.nesne_id == Yer.id))
                .where(Yer.ilce_id == ilce.id, *_kamusal_yayin(KullanimTuru.KESFET))
            ).all()
            if tur
        }
    )
    return IlceDetayiSemasi(
        cografya=KamusalCografyaSemasi(
            sehir_id=str(sehir.id), sehir_anahtari=sehir_anahtari, sehir_ismi=sehir.isim,
            ilce_id=str(ilce.id), ilce_slug=_slug(ilce.isim), ilce_ismi=ilce.isim,
        ),
        ayri_sayfa_var=bool(projection and bilgiler),
        ozgun_karar_bilgileri=bilgiler,
        yayinlanmis_yer_turleri=turler,
        kesfet_url=f"/sehir/{sehir_anahtari}?ilce={ilce.id}",
        kapsam_aciklamasi=(
            "Bu ilçe için yayımlanmış özgün karar bilgisi bulunuyor."
            if projection and bilgiler
            else "Bu ilçe için ayrı bir anlatı yayımlamıyoruz; canonical ilçe filtresiyle Keşfet'e devam edebilirsin."
        ),
    )


def _guncellik_anlami(surum: IddiaSurumu) -> str:
    if surum.gecerlilik_bitisi:
        return f"Bu bilgi {surum.gecerlilik_bitisi.date().isoformat()} tarihine kadar olan kapsam için yayımlandı."
    if surum.dogrulanma_zamani:
        return f"Bu alan en son {surum.dogrulanma_zamani.date().isoformat()} tarihinde doğrulandı."
    return "Bu bilginin ayrı bir doğrulama tarihi yayımlanmamış; yalnız belirtilen kapsamda kullanıyoruz."


def yer_detayi_getir(
    oturum: Session,
    yer_id: str,
    *,
    baglam_semasi: KararBaglamiSemasi | None = None,
) -> KamusalYerDetayiSemasi:
    temel = yer_ve_koordinat_getir(oturum, yer_id, kullanim=KullanimTuru.DETAY)
    if temel is None:
        raise LookupError("Yer bulunamadı veya kamusal detay yayını kapalı.")
    yer, enlem, boylam = temel
    kimlik_satiri = oturum.execute(
        select(Sube, YerKimligi, Sehir, Ilce)
        .join(YerKimligi, YerKimligi.id == Sube.yer_kimligi_id)
        .join(Sehir, Sehir.id == YerKimligi.sehir_id)
        .outerjoin(Ilce, Ilce.id == yer.ilce_id)
        .where(Sube.legacy_yer_id == yer.id, Sube.durum == "aktif", YerKimligi.durum == "aktif")
    ).first()
    if kimlik_satiri is None:
        raise LookupError("Yer kimliği veya şube yayına uygun değil.")
    sube, kimlik, sehir, ilce = kimlik_satiri.Sube, kimlik_satiri.YerKimligi, kimlik_satiri.Sehir, kimlik_satiri.Ilce
    claim_yayini = aliased(YayinKaydi, name="claim_yayini")
    claimler = oturum.execute(
        select(Iddia, IddiaSurumu, claim_yayini)
        .join(IddiaSurumu, and_(IddiaSurumu.iddia_id == Iddia.id, IddiaSurumu.surum_no == Iddia.aktif_surum_no))
        .join(claim_yayini, and_(claim_yayini.nesne_turu == "claim", claim_yayini.nesne_id == Iddia.id))
        .where(
            Iddia.sube_id == sube.id,
            IddiaSurumu.bilgi_durumu == BilgiDurumu.BILINIYOR.value,
            claim_yayini.aktif_mi.is_(True),
            claim_yayini.durum.in_(KAMUSAL_DURUMLAR),
            claim_yayini.izinli_kullanimlar.contains([KullanimTuru.DETAY.value]),
        )
        .order_by(Iddia.aile, IddiaSurumu.surum_no.desc())
    ).all()
    bilgiler = [
        YayimlanmisBilgiSemasi(
            aile=s.Iddia.aile,
            deger=s.IddiaSurumu.deger,
            kapsam=s.Iddia.kapsam,
            gecerlilik_baslangici=s.IddiaSurumu.gecerlilik_baslangici,
            gecerlilik_bitisi=s.IddiaSurumu.gecerlilik_bitisi,
            dogrulanma_zamani=s.IddiaSurumu.dogrulanma_zamani,
            guncellik_anlami=_guncellik_anlami(s.IddiaSurumu),
        )
        for s in claimler
    ]
    karar = None
    kritik_bilinmeyenler: list[str] = []
    if baglam_semasi is not None:
        baglam = baglam_semasi.domaine("yer_detay")
        aday = adaylari_toplu_getir(oturum, [yer_id], kullanim_turu=KullanimTuru.DETAY)
        if aday:
            karar_domain = KararMotoru().degerlendir(baglam, aday[0])
            karar = KararSonucuSemasi.domainden(karar_domain)
            kritik_bilinmeyenler = [b.mesaj for b in karar_domain.bilinmeyenler]
    if not bilgiler:
        kritik_bilinmeyenler.append("Bu yerin ziyaret koşullarını henüz yayımlanmış claim'lerle doğrulayamıyoruz.")
    sehir_anahtari = sehir_anahtarini_isme_gore_bul(sehir.isim) or _slug(sehir.isim)
    return KamusalYerDetayiSemasi(
        yer=YerKimligiSemasi(place_id=str(yer.id), canonical_id=str(kimlik.id), branch_id=str(sube.id), isim=yer.isim),
        cografya=KamusalCografyaSemasi(
            sehir_id=str(sehir.id), sehir_anahtari=sehir_anahtari, sehir_ismi=sehir.isim,
            ilce_id=str(ilce.id) if ilce else None, ilce_slug=_slug(ilce.isim) if ilce else None,
            ilce_ismi=ilce.isim if ilce else None,
        ),
        ana_kategori=yer.ana_kategori,
        alt_kategori=yer.alt_kategori,
        adres=yer.adres,
        aciklama=yer.aciklama,
        telefon=yer.telefon,
        web_sitesi=yer.web_sitesi,
        enlem=enlem,
        boylam=boylam,
        fotograf_urlleri=yer.fotograf_urlleri,
        pratik_bilgiler=bilgiler,
        karar_sonucu=karar,
        kritik_bilinmeyenler=list(dict.fromkeys(kritik_bilinmeyenler)),
        kapsam_anlami=(
            "Pratik bilgiler yalnız her claim'in yanında belirtilen zaman ve alan kapsamı için geçerlidir."
            if bilgiler
            else "Kimlik ve temel konum yayımlanmış olsa da ziyaret koşulları için doğrulanmış claim kapsamı yok."
        ),
        duzeltme_girisi=DuzeltmeGirisiSemasi(
            aciklama="Kamusal düzeltme formu henüz açık değil. Yanlış bir bilgi olumlu karar gerekçesi olarak kullanılmamalı.",
            href=None,
        ),
    )
