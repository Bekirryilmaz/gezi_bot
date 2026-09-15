from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import and_, select
from sqlalchemy.orm import Session, aliased

from ortak.sabitler import OzelEtiket
from sunucu.bilgi.domain import BilgiDurumu
from sunucu.karar_motoru.domain import BilgiReferansi, KararAdayi, KararBaglami, KararMotoru, KararSonucu
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu
from sunucu.veritabani.karar_modelleri import KararIzi
from sunucu.veritabani.kimlik_modelleri import Sube, YerKimligi
from sunucu.veritabani.modeller import Sehir, Yer
from sunucu.veritabani.yayin_modelleri import YayinKaydi
from sunucu.yayin.domain import KullanimTuru, YayinUygunlukDurumu
from sunucu.yayin.servis import yayin_kaydi_kamusal_mi


def adaylari_toplu_getir(
    oturum: Session,
    yer_idleri: list[str],
    *,
    kullanim_turu: KullanimTuru = KullanimTuru.KARAR,
) -> list[KararAdayi]:
    """Yer/publication ve aktif claim projection'larini iki toplu sorguda getirir."""
    benzersiz = list(dict.fromkeys(yer_idleri))
    yer_yayini = aliased(YayinKaydi, name="yer_yayini")
    satirlar = oturum.execute(
        select(Yer, Sehir, Sube, YerKimligi, yer_yayini)
        .join(Sehir, Sehir.id == Yer.sehir_id)
        .join(Sube, Sube.legacy_yer_id == Yer.id)
        .join(YerKimligi, YerKimligi.id == Sube.yer_kimligi_id)
        .outerjoin(yer_yayini, and_(yer_yayini.nesne_turu == "yer", yer_yayini.nesne_id == Yer.id))
        .where(Yer.id.in_(benzersiz))
    ).all()
    sube_idleri = [str(satir.Sube.id) for satir in satirlar]

    claim_yayini = aliased(YayinKaydi, name="claim_yayini")
    claim_satirlari = (
        oturum.execute(
            select(Iddia, IddiaSurumu, claim_yayini)
            .join(
                IddiaSurumu,
                and_(IddiaSurumu.iddia_id == Iddia.id, IddiaSurumu.surum_no == Iddia.aktif_surum_no),
            )
            .outerjoin(
                claim_yayini,
                and_(claim_yayini.nesne_turu == "claim", claim_yayini.nesne_id == Iddia.id),
            )
            .where(Iddia.sube_id.in_(sube_idleri))
        ).all()
        if sube_idleri
        else []
    )

    bilgiler: dict[str, list[BilgiReferansi]] = {sube_id: [] for sube_id in sube_idleri}
    for satir in claim_satirlari:
        iddia, surum, yayin = satir.Iddia, satir.IddiaSurumu, satir.claim_yayini
        bilgiler[str(iddia.sube_id)].append(
            BilgiReferansi(
                iddia_id=str(iddia.id),
                aile=iddia.aile,
                surum_no=surum.surum_no,
                deger=surum.deger if surum.bilgi_durumu == BilgiDurumu.BILINIYOR.value else None,
                bilgi_durumu=BilgiDurumu(surum.bilgi_durumu),
                yayinlanabilir=yayin_kaydi_kamusal_mi(yayin, KullanimTuru.KARAR),
                yayin_surumu=getattr(yayin, "surum", None),
            )
        )

    adaylar: list[KararAdayi] = []
    for satir in satirlar:
        yer, sehir, sube, kimlik, yayin = (
            satir.Yer,
            satir.Sehir,
            satir.Sube,
            satir.YerKimligi,
            satir.yer_yayini,
        )
        durum = (
            YayinUygunlukDurumu(yayin.durum)
            if yayin_kaydi_kamusal_mi(yayin, kullanim_turu)
            else YayinUygunlukDurumu.YAYINLANAMAZ
        )
        adaylar.append(
            KararAdayi(
                yer_id=str(yer.id),
                canonical_id=str(kimlik.id),
                sube_id=str(sube.id),
                isim=yer.isim,
                sehir=sehir.isim,
                ilce=yer.ilce,
                yayin_durumu=durum,
                yayin_surumu=int(yayin.surum) if yayin is not None else 0,
                bilgiler=tuple(bilgiler.get(str(sube.id), ())),
                sponsorlu=yer.ozellikler.get(OzelEtiket.SPONSORLU_MEKAN.value)
                in (True, "true", "evet", "1", 1),
            )
        )
    siralama = {yer_id: i for i, yer_id in enumerate(benzersiz)}
    return sorted(adaylar, key=lambda aday: siralama.get(aday.yer_id, len(siralama)))


def kararlari_degerlendir(
    oturum: Session,
    baglam: KararBaglami,
    yer_idleri: list[str],
    *,
    request_id: str,
    correlation_id: str | None = None,
) -> tuple[list[KararSonucu], str]:
    trace_reference = f"decision:{request_id}:{uuid4().hex[:12]}"
    motor = KararMotoru()
    adaylar = adaylari_toplu_getir(oturum, yer_idleri)
    sonuclar = [motor.degerlendir(baglam, aday, trace_reference=trace_reference) for aday in adaylar]
    bulunan = {aday.yer_id for aday in adaylar}
    for yer_id in yer_idleri:
        if yer_id in bulunan:
            continue
        kapsam_disi = KararAdayi(
            yer_id=yer_id,
            canonical_id=yer_id,
            sube_id=yer_id,
            isim="Kapsam disi yer",
            sehir=baglam.cografi_baglam.sehir,
            ilce=None,
            yayin_durumu=YayinUygunlukDurumu.YAYINLANAMAZ,
            yayin_surumu=0,
        )
        sonuc = motor.degerlendir(baglam, kapsam_disi, trace_reference=trace_reference)
        sonuclar.append(replace(sonuc, yer_id=None, canonical_id=None, sube_id=None, yer_ismi=None))

    claim_surumleri = sorted({ref for sonuc in sonuclar for ref in sonuc.kullanilan_iddia_surumleri})
    nedenler = sorted(
        {
            gerekce.kod.value
            for sonuc in sonuclar
            for gerekce in (
                *sonuc.gerekceler,
                *sonuc.kritik_engeller,
                *sonuc.onemli_odunler,
                *sonuc.bilinmeyenler,
            )
        }
    )
    yayin_surumleri = sorted(
        {str(sonuc.yayin_surumu) for sonuc in sonuclar if sonuc.yayin_surumu is not None}
    )
    oturum.add(
        KararIzi(
            trace_reference=trace_reference,
            request_id=request_id,
            correlation_id=correlation_id or request_id,
            context_fingerprint=baglam.karar_parmak_izi(),
            politika_surumu=baglam.politika_surumu,
            bilgi_surumu=baglam.bilgi_surumu,
            claim_surumleri=claim_surumleri,
            yayin_surumleri=yayin_surumleri,
            reason_kodlari=nedenler,
            karar_zamani=datetime.now(timezone.utc),
        )
    )
    oturum.commit()
    return sonuclar, trace_reference
