"""Birinci el admin gozlemini mevcut claim inceleme akisina yazar; otomatik yayin yoktur."""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException, status
from ortak.sabitler import CalismaSaatiDurumu, VeriKaynagi
from sqlalchemy.orm import Session

from sunucu.admin.audit import audit_yaz
from sunucu.admin.workflow import nesne_yetkisini_dogrula
from sunucu.auth.servis import AdminBaglami
from sunucu.bilgi.calisma_saati import calisma_saati_degerini_al, calisma_saati_kaydini_kur
from sunucu.bilgi.domain import HakDurumu
from sunucu.veritabani.admin_modelleri import IncelemeDosyasi
from sunucu.veritabani.bilgi_modelleri import (
    Gozlem,
    Iddia,
    IddiaSurumu,
    KanitBaglantisi,
    KaynakPolitikasi,
    VeriBatch,
)
from sunucu.veritabani.kimlik_modelleri import Sube


def _hash(deger: Any) -> str:
    ham = json.dumps(deger, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(ham.encode("utf-8")).hexdigest()


def site_ici_politikasini_uygula(oturum: Session) -> KaynakPolitikasi:
    kaynak = VeriKaynagi.SITE_ICI.value
    politika = oturum.query(KaynakPolitikasi).filter_by(kaynak=kaynak).first()
    if politika is None:
        politika = KaynakPolitikasi(kaynak=kaynak)
        oturum.add(politika)
    politika.kamusal_gosterim = HakDurumu.IZINLI.value
    politika.turev_iddia = HakDurumu.IZINLI.value
    politika.ai_isleme = HakDurumu.IZINLI.value
    politika.uzun_sureli_saklama = HakDurumu.IZINLI.value
    politika.dayanak_notu = "Birinci el admin gozlemi; otomatik yayin yoktur."
    politika.gecerli_baslangic = datetime.now(UTC)
    politika.gecerli_bitis = None
    oturum.flush()
    return politika


def birinci_el_gozlem_yaz(
    oturum: Session,
    *,
    baglam: AdminBaglami,
    sube_id: str,
    aile: str,
    deger: Any,
    ozet: str,
    gerekce: str,
    istek_id: str,
    kaynak_url: str | None = None,
) -> dict[str, Any]:
    nesne_yetkisini_dogrula(oturum, baglam, "sube", sube_id)
    sube = oturum.get(Sube, sube_id)
    if sube is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sube bulunamadi.")
    site_ici_politikasini_uygula(oturum)
    simdi = datetime.now(UTC)
    kosu = f"admin-gozlem:{simdi.date().isoformat()}"
    batch = (
        oturum.query(VeriBatch)
        .filter_by(kaynak=VeriKaynagi.SITE_ICI.value, kosu_anahtari=kosu)
        .first()
    )
    if batch is None:
        batch = VeriBatch(
            kaynak=VeriKaynagi.SITE_ICI.value,
            kosu_anahtari=kosu,
            kok_tanimi={"kanal": "admin_birinci_el", "otomatik_yayin": False},
            baslama_zamani=simdi,
        )
        oturum.add(batch)
        oturum.flush()
    icerik = {
        "aile": aile,
        "deger": deger,
        "ozet": ozet.strip(),
        "aktor_id": baglam.kullanici.id,
        "sube_id": sube_id,
        "kaynak_url": kaynak_url,
    }
    gozlem = Gozlem(
        veri_batch_id=batch.id,
        kaynak=VeriKaynagi.SITE_ICI.value,
        kaynak_kayit_id=str(uuid.uuid4()),
        kaynak_url=kaynak_url,
        cekilme_zamani=simdi,
        dogrulanma_zamani=None,
        icerik_ozeti=icerik,
        icerik_hash=_hash(icerik),
    )
    oturum.add(gozlem)
    oturum.flush()
    kapsam = {"kaynak": "site_ici", "sube_kapsami": "tam_sube"}
    iddia = (
        oturum.query(Iddia)
        .filter_by(sube_id=sube_id, aile=aile)
        .order_by(Iddia.olusturulma_zamani.desc())
        .first()
    )
    if iddia is None:
        iddia = Iddia(sube_id=sube_id, aile=aile, kapsam=kapsam)
        oturum.add(iddia)
        oturum.flush()
    surum_no = (iddia.aktif_surum_no or 0) + 1
    surum_deger: dict[str, Any] = {"deger": deger}
    if aile == "calisma_saatleri":
        ham = deger if isinstance(deger, str) else calisma_saati_degerini_al(deger)
        kayit = calisma_saati_kaydini_kur(
            ham=ham,
            kaynak=VeriKaynagi.SITE_ICI.value,
            gozlemlenme_zamani=simdi,
            cekilme_zamani=simdi,
            ham_referans=kaynak_url,
        )
        if kayit.durum not in {
            CalismaSaatiDurumu.KNOWN,
            CalismaSaatiDurumu.PARTIALLY_KNOWN,
        }:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Birinci el calisma saati desteklenen sozdiziminde olmali.",
            )
        surum_deger = kayit.sozluk()
        surum_deger["deger"] = kayit.ayristirma.ham
    surum = IddiaSurumu(
        iddia_id=iddia.id,
        surum_no=surum_no,
        deger=surum_deger,
        bilgi_durumu="biliniyor",
        guven_sinifi="belirsiz",
        gecerlilik_baslangici=simdi,
        dogrulanma_zamani=None,
        yayin_durumu="inceleme_bekliyor",
        ai_tarafindan_uretildi=False,
    )
    oturum.add(surum)
    oturum.flush()
    oturum.add(
        KanitBaglantisi(
            iddia_surumu_id=surum.id,
            gozlem_id=gozlem.id,
            rol="supporting",
            gerekce="Birinci el admin gozlemi; insan incelemesi bekliyor.",
        )
    )
    iddia.aktif_surum_no = surum_no
    dosya = IncelemeDosyasi(
        dosya_turu="claim_candidate",
        nesne_turu="claim",
        nesne_id=iddia.id,
        durum="bekliyor",
        risk_sinifi="normal",
        onerilen_eylem="claim_approve",
        komut_payload={
            "iddia_surumu_id": surum.id,
            "uretim": "admin_birinci_el_v1",
            "public": False,
        },
        acan_aktor_id=baglam.kullanici.id,
        karar_gerekcesi=gerekce,
    )
    oturum.add(dosya)
    oturum.flush()
    audit_yaz(
        oturum,
        aktor_id=baglam.kullanici.id,
        eylem="birinci_el_gozlem",
        nesne_turu="claim",
        nesne_id=iddia.id,
        onceki=None,
        yeni={"gozlem_id": gozlem.id, "surum_no": surum_no, "otomatik_yayin": False},
        gerekce=gerekce,
        istek_id=istek_id,
    )
    return {
        "gozlem_id": gozlem.id,
        "iddia_id": iddia.id,
        "iddia_surumu_id": surum.id,
        "inceleme_dosyasi_id": dosya.id,
        "yayin_durumu": surum.yayin_durumu,
        "otomatik_yayin": False,
    }
