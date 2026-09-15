from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from sunucu.arama.domain import SOMUT_KOSULLAR
from sunucu.arama.normalizasyon import turkce_arama_normalize
from sunucu.bugun_ne_yapalim.semalar import (
    BugunBaglamiSemasi,
    BugunNeYapalimCevabi,
    BugunNeYapalimTalebi,
    NetlestirmeSemasi,
)
from sunucu.karar_motoru.semalar import (
    CografiBaglamSemasi,
    KararBaglamiSemasi,
    TercihSemasi,
    ZamanBaglamiSemasi,
    ZorunluKosulSemasi,
)
from sunucu.kesfet.semalar import (
    KesfetAramaBaglamiSemasi,
    KesfetDegerlendirmeCevabi,
    KesfetDegerlendirmeTalebi,
)
from sunucu.kesfet.servis import kesfet_degerlendir
from sunucu.veritabani.arama_modelleri import Ilce
from sunucu.veritabani.modeller import Sehir

ISTANBUL = ZoneInfo("Europe/Istanbul")
AMAC_ETIKETLERI = {
    "kahve_icmek": "kahve içmek",
    "yemek_yemek": "yemek yemek",
    "tarihi_kulturel_ziyaret": "tarih-kültür ziyareti",
}
AMAC_SORGULARI = {
    "kahve_icmek": "kafe",
    "yemek_yemek": "yeme içme",
    "tarihi_kulturel_ziyaret": "tarih ve kültür",
}


@dataclass(frozen=True)
class CozulmusNiyet:
    amac: str | None
    ilce: str | None
    kisi_baglami: str | None
    istenen_zaman: str | None
    sure_dakika: int | None
    ulasim_bicimi: str | None
    butce_ust_siniri: float | None
    zorunlu_kosullar: tuple[str, ...]
    tercihler: tuple[str, ...]


def _amac_bul(metin: str) -> str | None:
    eslesmeler = (
        ("kahve_icmek", ("kahve", "kafe", "cafe")),
        ("yemek_yemek", ("yemek", "restoran", "lokanta", "kahvalti")),
        ("tarihi_kulturel_ziyaret", ("tarih", "muze", "kultur", "anit")),
    )
    bulunan = [
        amac for amac, kelimeler in eslesmeler if any(kelime in metin for kelime in kelimeler)
    ]
    return bulunan[0] if len(bulunan) == 1 else None


def _sure_bul(metin: str) -> int | None:
    eslesme = re.search(r"\b(\d{1,3})\s*(saat|dakika|dk)\b", metin)
    if not eslesme:
        return None
    sayi = int(eslesme.group(1))
    return sayi * 60 if eslesme.group(2) == "saat" else sayi


def _butce_bul(metin: str) -> float | None:
    eslesme = re.search(
        r"(?:en fazla|butce(?:m)?|maksimum|max)\s*(\d+(?:[.,]\d+)?)\s*(?:tl|₺)", metin
    )
    return float(eslesme.group(1).replace(",", ".")) if eslesme else None


def _coz(talep: BugunNeYapalimTalebi, ilceler: list[Ilce]) -> CozulmusNiyet:
    metin = turkce_arama_normalize(talep.serbest_metin or "")
    yapisal = talep.niyet
    ilce = yapisal.ilce
    if not ilce:
        ilce = next(
            (aday.isim for aday in ilceler if aday.arama_isim and aday.arama_isim in metin), None
        )
    zorunlu = list(dict.fromkeys(yapisal.zorunlu_kosullar))
    tercihler = list(dict.fromkeys(yapisal.tercihler))
    wifi_geciyor = "wifi" in metin or "wi fi" in metin
    if wifi_geciyor and any(k in metin for k in ("kesin", "sart", "zorunlu", "mutlaka")):
        zorunlu.append("wifi")
    elif wifi_geciyor:
        tercihler.append("wifi")
    if "sakin" in metin or "sessiz" in metin:
        tercihler.append("sessiz_ortam")
    if "otopark" in metin:
        hedef = (
            zorunlu
            if any(k in metin for k in ("kesin", "sart", "zorunlu", "mutlaka"))
            else tercihler
        )
        hedef.append("otopark")
    kisi = yapisal.kisi_baglami
    if not kisi:
        kisi = next(
            (
                etiket
                for anahtar, etiket in (
                    ("arkadas", "arkadaşlarla"),
                    ("esim", "eşimle"),
                    ("cocuk", "çocuklarla"),
                    ("tek bas", "tek başıma"),
                )
                if anahtar in metin
            ),
            None,
        )
    zaman = yapisal.istenen_zaman
    if not zaman:
        zaman = "bu akşam" if "bu aksam" in metin else "şimdi" if "simdi" in metin else "bugün"
    ulasim = yapisal.ulasim_bicimi
    if not ulasim:
        ulasim = next(
            (
                deger
                for anahtar, deger in (
                    ("yuruy", "yürüyerek"),
                    ("toplu tasima", "toplu taşıma"),
                    ("bisiklet", "bisiklet"),
                    ("arabay", "otomobil"),
                )
                if anahtar in metin
            ),
            None,
        )
    return CozulmusNiyet(
        amac=yapisal.amac or _amac_bul(metin),
        ilce=ilce,
        kisi_baglami=kisi,
        istenen_zaman=zaman,
        sure_dakika=yapisal.sure_dakika or _sure_bul(metin),
        ulasim_bicimi=ulasim,
        butce_ust_siniri=yapisal.butce_ust_siniri
        if yapisal.butce_ust_siniri is not None
        else _butce_bul(metin),
        zorunlu_kosullar=tuple(dict.fromkeys(zorunlu)),
        tercihler=tuple(dict.fromkeys(tercihler)),
    )


def _ozet(sehir: str, niyet: CozulmusNiyet) -> str:
    parcalar = [niyet.ilce or sehir]
    if niyet.amac:
        parcalar.append(AMAC_ETIKETLERI[niyet.amac])
    if niyet.kisi_baglami:
        parcalar.append(niyet.kisi_baglami)
    if niyet.istenen_zaman:
        parcalar.append(niyet.istenen_zaman)
    if niyet.sure_dakika:
        parcalar.append(f"{niyet.sure_dakika} dakika")
    if niyet.ulasim_bicimi:
        parcalar.append(niyet.ulasim_bicimi)
    if niyet.butce_ust_siniri is not None:
        parcalar.append(f"en fazla {niyet.butce_ust_siniri:g} TL")
    parcalar.extend(
        f"{SOMUT_KOSULLAR[kod].etiket} zorunlu"
        for kod in niyet.zorunlu_kosullar
        if kod in SOMUT_KOSULLAR
    )
    parcalar.extend(
        f"{SOMUT_KOSULLAR[kod].etiket} tercih" for kod in niyet.tercihler if kod in SOMUT_KOSULLAR
    )
    return "Şunu anladım: " + ", ".join(parcalar) + "."


def bugun_ne_yapalim(
    oturum: Session,
    talep: BugunNeYapalimTalebi,
    *,
    request_id: str,
    simdi: datetime | None = None,
) -> BugunNeYapalimCevabi:
    an = simdi or datetime.now(ISTANBUL)
    if an.tzinfo is None:
        an = an.replace(tzinfo=ISTANBUL)
    sehir_normal = turkce_arama_normalize(talep.niyet.sehir)
    sehir = oturum.scalar(
        select(Sehir).where(Sehir.aktif_mi.is_(True), Sehir.arama_isim == sehir_normal)
    )
    if sehir is None:
        raise ValueError("Gecerli ve aktif bir sehir bulunamadi.")
    ilceler = list(
        oturum.scalars(select(Ilce).where(Ilce.sehir_id == sehir.id, Ilce.aktif_mi.is_(True)))
    )
    niyet = _coz(talep, ilceler)
    ilce_nesnesi = next((aday for aday in ilceler if aday.isim == niyet.ilce), None)
    if niyet.ilce and ilce_nesnesi is None:
        raise ValueError("Secilen ilce bu sehre ait degil.")
    zorunlu = [kod for kod in niyet.zorunlu_kosullar if kod in SOMUT_KOSULLAR]
    tercihler = [kod for kod in niyet.tercihler if kod in SOMUT_KOSULLAR and kod not in zorunlu]
    baslangic = an.timetz().replace(tzinfo=None) if niyet.istenen_zaman == "şimdi" else None
    baglam = KararBaglamiSemasi(
        amac=niyet.amac,
        cografi_baglam=CografiBaglamSemasi(sehir=sehir.isim, ilce=niyet.ilce),
        zaman=ZamanBaglamiSemasi(
            ziyaret_tarihi=an.date(), baslangic=baslangic, degerlendirme_zamani=an
        ),
        ulasim_bicimi=niyet.ulasim_bicimi,
        butce_ust_siniri=niyet.butce_ust_siniri,
        sure_ust_siniri_dakika=niyet.sure_dakika,
        zorunlu_kosullar=[
            ZorunluKosulSemasi(**SOMUT_KOSULLAR[kod].zorunlu_kosul().__dict__) for kod in zorunlu
        ],
        tercihler=[TercihSemasi(**SOMUT_KOSULLAR[kod].tercih().__dict__) for kod in tercihler],
        reddedilen_yerler=talep.haric_yerler,
    )
    bugun = BugunBaglamiSemasi(
        degerlendirme_zamani=an.isoformat(),
        saat_dilimi="Europe/Istanbul",
        ziyaret_tarihi=an.date().isoformat(),
        aciklik_aciklamasi=(
            "Bu pilot kapsamda güvenilir çalışma saati claim'i yok; "
            "'şu an açık' sonucu üretmiyoruz."
        ),
    )
    ozet = _ozet(sehir.isim, niyet)
    if niyet.amac is None:
        return BugunNeYapalimCevabi(
            durum="clarification",
            anlasilan_ihtiyac_ozeti=ozet,
            netlestirme=NetlestirmeSemasi(
                soru="Ne yapmak istiyorsun?",
                alan="amac",
                secenekler=[
                    {"deger": kod, "etiket": etiket.capitalize()}
                    for kod, etiket in AMAC_ETIKETLERI.items()
                ],
            ),
            baglam=baglam,
            bugun_baglami=bugun,
        )
    sorgu = AMAC_SORGULARI[niyet.amac]
    desteklenmeyen = [kod for kod in niyet.zorunlu_kosullar if kod not in SOMUT_KOSULLAR]
    if desteklenmeyen or niyet.butce_ust_siniri is not None:
        nedenler = []
        if desteklenmeyen:
            etiketler = ", ".join(kod.replace("_", " ") for kod in desteklenmeyen)
            nedenler.append(f"{etiketler} için yayımlanmış bir claim sözleşmemiz yok")
        if niyet.butce_ust_siniri is not None:
            nedenler.append("bütçe sınırını doğrulayacak yayımlanmış fiyat claim'i yok")
        kesfet = KesfetDegerlendirmeCevabi(
            durum="insufficient",
            secenekler=[],
            kullanilan_baglam={"sorgu": sorgu, "amac": niyet.amac, "sehir": sehir.isim},
            sinirlama_nedeni=(
                "; ".join(nedenler).capitalize() + ". Koşulu yok sayıp seçenek önermedik."
            ),
        )
        return BugunNeYapalimCevabi(
            durum="insufficient",
            anlasilan_ihtiyac_ozeti=ozet,
            baglam=baglam,
            bugun_baglami=bugun,
            kesfet=kesfet,
            kesfet_sorgusu=sorgu,
        )
    kesfet = kesfet_degerlendir(
        oturum,
        KesfetDegerlendirmeTalebi(
            sorgu=sorgu,
            baglam=baglam,
            arama=KesfetAramaBaglamiSemasi(ilce_id=str(ilce_nesnesi.id) if ilce_nesnesi else None),
            haric_yerler=talep.haric_yerler,
        ),
        request_id=request_id,
        giris_kanali="bugun_ne_yapalim",
    )
    return BugunNeYapalimCevabi(
        durum=kesfet.durum,
        anlasilan_ihtiyac_ozeti=ozet,
        baglam=baglam,
        bugun_baglami=bugun,
        kesfet=kesfet,
        kesfet_sorgusu=sorgu,
    )
