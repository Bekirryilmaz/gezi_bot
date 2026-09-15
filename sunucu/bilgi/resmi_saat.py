"""Pilot rota-kritik resmi calisma saati katalogu. Tahmin ve Google yorumu yok."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException
from ortak.sabitler import CalismaSaatiDurumu
from sqlalchemy.orm import Session

from sunucu.admin.gozlem_servisi import birinci_el_gozlem_yaz
from sunucu.admin.grup_inceleme import grup_incelemeyi_uygula
from sunucu.auth.servis import AdminBaglami
from sunucu.bilgi.calisma_saati import calisma_saati_degerini_al, calisma_saatini_ayristir
from sunucu.bilgi.pilot_havuzu import PilotAday
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu

# T.C. Kultur ve Turizm Bakanligi Samsun Il Mudurlugu; cekilme 2026-09-16.
# Yalniz parse edilebilir haftalik sozdizimi. Mevsimsel/TL ucret uydurulmaz.
RESMI_CALISMA_SAATLERI: tuple[dict[str, Any], ...] = (
    {
        "anahtar": "gazi_muzesi",
        "isim_icerir": "Gazi Müzesi",
        "isim_haric": (),
        "saat": "Mo-Su 08:30-16:30",
        "kaynak_url": "https://samsun.ktb.gov.tr/TR-216752/gazi-muzesi.html",
        "ozet": "KTB Samsun Gazi Muzesi resmi sayfasi: her gun 08:30-16:30.",
    },
    {
        "anahtar": "samsun_kent_muzesi",
        "isim_icerir": "Samsun Kent Müzesi",
        "isim_haric": (),
        "saat": "Mo 13:00-17:00; Tu-Su 08:00-17:00",
        "kaynak_url": "https://samsun.ktb.gov.tr/TR-230223/muzeler.html",
        "ozet": (
            "KTB Samsun muzeler listesi: Kent Muzesi Pzt 13:00-17:00, "
            "diger gunler 08:00-17:00."
        ),
    },
    {
        "anahtar": "amazon_koyu",
        "isim_icerir": "Amazon Köyü",
        "isim_haric": ("Amazon Anıtı",),
        "saat": "Mo 12:00-17:00; Tu-Su 08:30-17:00",
        "kaynak_url": "https://samsun.ktb.gov.tr/TR-230223/muzeler.html",
        "ozet": (
            "KTB Samsun muzeler listesi: Amazon Koyu Pzt 12:00-17:00, "
            "diger gunler 08:30-17:00."
        ),
    },
    {
        "anahtar": "bandirma_gemi_muze",
        "isim_icerir": "Bandırma Gemi",
        "isim_haric": (),
        "saat": "Mo 12:00-16:45; Tu-Su 08:00-16:45",
        "kaynak_url": "https://samsun.ktb.gov.tr/TR-362756/bandirma-gemi-muze-ve-milli-mucadele-park-acik-alan-muzesi.html",
        "ozet": "KTB Bandirma Gemi-Muze sayfasi: Pzt 12:00-16:45, diger gunler 08:00-16:45.",
    },
    {
        "anahtar": "canik_oyuncak_muzesi",
        "isim_icerir": "Canik Oyuncak Müzesi",
        "isim_haric": (),
        "saat": "Tu-Sa 10:00-16:00",
        "kaynak_url": "https://samsun.ktb.gov.tr/TR-230223/muzeler.html",
        "ozet": (
            "KTB Samsun muzeler listesi: Oyuncak Muzesi Sali-Ctesi 10:00-16:00; "
            "Pzt ve Pazar kapali."
        ),
    },
)

RESMI_SAAT_ATLANAN: tuple[dict[str, str], ...] = (
    {
        "isim_icerir": "Arkeoloji Ve Etnografya",
        "neden": "ktb_tasinma_hizmet_disi",
    },
    {
        "isim_icerir": "Samsun Müzesi",
        "neden": "guncel_haftalik_saat_yok",
    },
    {
        "isim_icerir": "Tekkeköy Mağaraları",
        "neden": "resmi_haftalik_saat_yok",
    },
    {
        "isim_icerir": "Nerik",
        "neden": "oren_yeri_saat_yok",
    },
    {
        "isim_icerir": "İlkadım Anıtı",
        "neden": "acik_hava_anit_saat_yok",
    },
    {
        "isim_icerir": "Amazon Anıtı",
        "neden": "acik_hava_anit_saat_yok",
    },
    {
        "isim_icerir": "SAAT KULESİ",
        "neden": "acik_hava_anit_saat_yok",
    },
    {
        "isim_icerir": "Tarihi Köprü",
        "neden": "acik_hava_yapi_saat_yok",
    },
    {
        "isim_icerir": "Çınar Ağacı",
        "neden": "acik_hava_dogal_saat_yok",
    },
    {
        "isim_icerir": "Göğceli Camii",
        "neden": "cami_resmi_haftalik_saat_yok",
    },
    {
        "isim_icerir": "Gökgöl Camii",
        "neden": "cami_resmi_haftalik_saat_yok",
    },
    {
        "isim_icerir": "Çakallı Han",
        "neden": "resmi_haftalik_saat_yok",
    },
    {
        "isim_icerir": "Ambarköy Açık Hava",
        "neden": "ayni_kurum_saatine_birlestirilmedi",
    },
)


@dataclass(frozen=True)
class ResmiSaatEslesme:
    anahtar: str
    saat: str
    kaynak_url: str
    ozet: str


def resmi_saati_esle(isim: str) -> ResmiSaatEslesme | None:
    for kayit in RESMI_CALISMA_SAATLERI:
        if any(parca and parca in isim for parca in kayit["isim_haric"]):
            continue
        if kayit["isim_icerir"] in isim:
            ayristirma = calisma_saatini_ayristir(kayit["saat"])
            if ayristirma.durum is not CalismaSaatiDurumu.KNOWN:
                return None
            return ResmiSaatEslesme(
                anahtar=kayit["anahtar"],
                saat=kayit["saat"],
                kaynak_url=kayit["kaynak_url"],
                ozet=kayit["ozet"],
            )
    return None


def resmi_saat_atlama_nedeni(isim: str) -> str | None:
    for kayit in RESMI_SAAT_ATLANAN:
        if kayit["isim_icerir"] in isim:
            return kayit["neden"]
    return None


def _yayimli_known_saat_var(oturum: Session, sube_id: str) -> bool:
    iddia = (
        oturum.query(Iddia)
        .filter_by(sube_id=sube_id, aile="calisma_saatleri")
        .order_by(Iddia.olusturulma_zamani.desc())
        .first()
    )
    if iddia is None or not iddia.aktif_surum_no:
        return False
    surum = (
        oturum.query(IddiaSurumu)
        .filter_by(iddia_id=iddia.id, surum_no=iddia.aktif_surum_no)
        .first()
    )
    if surum is None or surum.yayin_durumu not in {"yayinlandi", "sinirli"}:
        return False
    ayristirma = calisma_saatini_ayristir(calisma_saati_degerini_al(surum.deger))
    return ayristirma.durum is CalismaSaatiDurumu.KNOWN


def resmi_saatleri_isle(
    oturum: Session,
    *,
    baglam: AdminBaglami | None,
    havuz: list[PilotAday],
    yaz: bool,
    gerekce: str,
) -> dict[str, Any]:
    cekilme = datetime.now(UTC)
    ozet: dict[str, Any] = {
        "aday": 0,
        "yazilan": 0,
        "yayinlanan": 0,
        "atlanan": [],
        "hatalar": [],
        "cekilme_zamani": cekilme.isoformat(),
        "otomatik_yayin": False,
        "kaynak": "ktb_samsun_resmi",
    }
    for aday in havuz:
        eslesme = resmi_saati_esle(aday.isim)
        if eslesme is None:
            neden = resmi_saat_atlama_nedeni(aday.isim)
            if neden:
                ozet["atlanan"].append({"isim": aday.isim, "neden": neden})
            continue
        ozet["aday"] += 1
        if _yayimli_known_saat_var(oturum, aday.sube_id):
            ozet["atlanan"].append(
                {"isim": aday.isim, "neden": "yayimli_known_saat_var", "anahtar": eslesme.anahtar}
            )
            continue
        if not yaz:
            ozet["atlanan"].append(
                {"isim": aday.isim, "neden": "dry_run", "anahtar": eslesme.anahtar}
            )
            continue
        if baglam is None:
            ozet["hatalar"].append({"isim": aday.isim, "neden": "baglam_yok"})
            continue
        try:
            gozlem = birinci_el_gozlem_yaz(
                oturum,
                baglam=baglam,
                sube_id=aday.sube_id,
                aile="calisma_saatleri",
                deger=eslesme.saat,
                ozet=eslesme.ozet,
                gerekce=gerekce,
                istek_id=f"faz255-resmi-saat-{eslesme.anahtar}",
                kaynak_url=eslesme.kaynak_url,
            )
        except HTTPException as hata:
            detay = hata.detail
            ozet["hatalar"].append(
                {"isim": aday.isim, "neden": detay if isinstance(detay, str) else str(detay)}
            )
            continue
        ozet["yazilan"] += 1
        inceleme = grup_incelemeyi_uygula(
            oturum,
            baglam=baglam,
            dosya_idleri=[gozlem["inceleme_dosyasi_id"]],
            gerekce=gerekce,
            istek_id=f"faz255-saat-inceleme-{eslesme.anahtar}",
        )
        if gozlem["inceleme_dosyasi_id"] in inceleme.onaylanan:
            ozet["yayinlanan"] += 1
        else:
            ozet["hatalar"].append(
                {
                    "isim": aday.isim,
                    "neden": inceleme.atlanan or inceleme.hatalar or "inceleme_onaylanmadi",
                }
            )
    return ozet
