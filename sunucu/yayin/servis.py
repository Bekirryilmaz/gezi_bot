from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from sunucu.yayin.domain import KullanimTuru, YayinUygunlukDurumu
from sunucu.veritabani.yayin_modelleri import (
    EtkiBaglantisi,
    GecersizlestirmeOlayi,
    GeriCekmeKaydi,
    PublicProjection,
    YayinKaydi,
)

KAMUSAL_DURUMLAR = {
    YayinUygunlukDurumu.YAYINLANABILIR.value,
    YayinUygunlukDurumu.SINIRLI_YAYINLANABILIR.value,
}


def yayin_kaydi_kamusal_mi(kayit: YayinKaydi | None, kullanim: KullanimTuru) -> bool:
    return bool(
        kayit
        and kayit.aktif_mi
        and kayit.durum in KAMUSAL_DURUMLAR
        and kullanim.value in kayit.izinli_kullanimlar
    )


def etki_bagi_ekle(
    oturum: Session,
    kaynak_turu: str,
    kaynak_id: str,
    hedef_turu: str,
    hedef_id: str,
    bag_turu: str,
) -> EtkiBaglantisi:
    mevcut = oturum.query(EtkiBaglantisi).filter_by(
        kaynak_turu=kaynak_turu,
        kaynak_id=kaynak_id,
        hedef_turu=hedef_turu,
        hedef_id=hedef_id,
        bag_turu=bag_turu,
    ).first()
    if mevcut:
        mevcut.aktif_mi = True
        return mevcut
    kayit = EtkiBaglantisi(
        kaynak_turu=kaynak_turu,
        kaynak_id=kaynak_id,
        hedef_turu=hedef_turu,
        hedef_id=hedef_id,
        bag_turu=bag_turu,
    )
    oturum.add(kayit)
    oturum.flush()
    return kayit


def gecersizlestirme_olayi_uret(
    oturum: Session,
    *,
    olay_anahtari: str,
    kaynak_turu: str,
    kaynak_id: str,
    olay_turu: str,
    payload: dict | None = None,
) -> GecersizlestirmeOlayi:
    mevcut = oturum.query(GecersizlestirmeOlayi).filter_by(olay_anahtari=olay_anahtari).first()
    if mevcut:
        return mevcut
    olay = GecersizlestirmeOlayi(
        olay_anahtari=olay_anahtari,
        kaynak_turu=kaynak_turu,
        kaynak_id=kaynak_id,
        olay_turu=olay_turu,
        payload=payload or {},
    )
    try:
        with oturum.begin_nested():
            oturum.add(olay)
            oturum.flush()
    except IntegrityError:
        return oturum.query(GecersizlestirmeOlayi).filter_by(olay_anahtari=olay_anahtari).one()
    return olay


def olayi_isle(oturum: Session, olay: GecersizlestirmeOlayi) -> None:
    if olay.islenme_zamani is not None:
        return
    etkilenen = {(olay.kaynak_turu, str(olay.kaynak_id))}
    kuyruk = list(etkilenen)
    while kuyruk:
        tur, nesne_id = kuyruk.pop(0)
        baglar = oturum.query(EtkiBaglantisi).filter_by(kaynak_turu=tur, kaynak_id=nesne_id, aktif_mi=True).all()
        for bag in baglar:
            hedef = (bag.hedef_turu, str(bag.hedef_id))
            if hedef not in etkilenen:
                etkilenen.add(hedef)
                kuyruk.append(hedef)
    simdi = datetime.now(timezone.utc)
    for tur, nesne_id in etkilenen:
        oturum.query(PublicProjection).filter_by(nesne_turu=tur, nesne_id=nesne_id).update(
            {PublicProjection.gecersiz_mi: True, PublicProjection.gecersizlestirme_zamani: simdi},
            synchronize_session="fetch",
        )
    olay.deneme_sayisi += 1
    olay.islenme_zamani = simdi
    olay.payload = {**(olay.payload or {}), "etkilenenler": sorted(f"{t}:{i}" for t, i in etkilenen)}
    oturum.flush()


def geri_cek(
    oturum: Session,
    *,
    nesne_turu: str,
    nesne_id: str,
    aktor_id: str,
    gerekce_kodu: str,
    gerekce: str,
    kapsam: dict | None = None,
    istek_id: str,
) -> GeriCekmeKaydi:
    yayin = oturum.query(YayinKaydi).filter_by(nesne_turu=nesne_turu, nesne_id=nesne_id).with_for_update().first()
    if yayin:
        yayin.durum = YayinUygunlukDurumu.YAYINLANAMAZ.value
        yayin.neden_kodlari = ["geri_cekilmis", gerekce_kodu]
        yayin.surum += 1
    kayit = GeriCekmeKaydi(
        nesne_turu=nesne_turu,
        nesne_id=nesne_id,
        kapsam=kapsam or {},
        gerekce_kodu=gerekce_kodu,
        gerekce=gerekce,
        aktor_id=aktor_id,
    )
    oturum.add(kayit)
    oturum.flush()
    olay = gecersizlestirme_olayi_uret(
        oturum,
        olay_anahtari=f"withdraw:{nesne_turu}:{nesne_id}:{istek_id}",
        kaynak_turu=nesne_turu,
        kaynak_id=nesne_id,
        olay_turu="geri_cekme",
        payload={"geri_cekme_id": str(kayit.id)},
    )
    olayi_isle(oturum, olay)
    return kayit
