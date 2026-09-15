from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from sunucu.arama.domain import SOMUT_KOSULLAR
from sunucu.arama.normalizasyon import turkce_arama_normalize
from sunucu.bugun_ne_yapalim.gelistirme_izi import gelistirme_izi, iz_guncelle
from sunucu.bugun_ne_yapalim.intent import (
    AMAC_ETIKETLERI,
    AMAC_SORGULARI,
    KARARDA_DESTEKLENEN_AMACLAR,
    metni_coz,
)
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
KISI_ETIKETLERI = {
    "partner": "partnerinle",
    "aile": "ailenle",
    "arkadaslar": "arkadaşlarınla",
    "cocuklar": "çocuklarla",
    "yalniz": "tek başına",
}
ISTEK_ETIKETLERI = {
    **AMAC_ETIKETLERI,
    "sohbet_uygunlugu": "sohbet için uygunluk",
    "sessiz_ortam": "sakinlik / ses düzeyi",
    "manzara": "manzara",
    "uygun_fiyat": "fiyat düzeyi",
    "yakinda": "yakınlık",
    "aile_uygunlugu": "aileyle kullanım",
    "cocuk_uygunlugu": "çocuklarla kullanım",
    "calisma_uygunlugu": "çalışma / laptop uygunluğu",
    "acik_hava": "açık hava alanı",
    "canli_muzik": "canlı müzik",
    "rezervasyon": "rezervasyon",
    "muze_turu": "müze olarak ziyaret edilebilmesi",
}


@dataclass(frozen=True)
class CozulmusNiyet:
    amac: str | None
    alt_amaclar: tuple[str, ...]
    aktiviteler: tuple[str, ...]
    ziyaret_baglamlari: tuple[str, ...]
    ilce: str | None
    kisi_baglami: str | None
    istenen_zaman: str | None
    sure_dakika: int | None
    ulasim_bicimi: str | None
    butce_ust_siniri: float | None
    zorunlu_kosullar: tuple[str, ...]
    tercihler: tuple[str, ...]
    desteklenmeyen_istekler: tuple[str, ...]
    normalize_edilmis_input: str
    celisen_niyet: bool


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
    dil = metni_coz(talep.serbest_metin or "")
    yapisal = talep.niyet
    ilce = yapisal.ilce
    if not ilce:
        ilce = next(
            (aday.isim for aday in ilceler if aday.arama_isim and aday.arama_isim in metin), None
        )
    zorunlu = list(dict.fromkeys(yapisal.zorunlu_kosullar))
    tercihler = list(dict.fromkeys(yapisal.tercihler))
    zorunlu.extend(dil["zorunlu_kosullar"])
    tercihler.extend(dil["tercihler"])
    kisi = yapisal.kisi_baglami
    if not kisi:
        kisi = dil["kisi_baglami"]
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
                    ("arabamiz yok", "araçsız"),
                    ("arabam yok", "araçsız"),
                )
                if anahtar in metin
            ),
            None,
        )
    return CozulmusNiyet(
        amac=yapisal.amac or dil["ana_amac"],
        alt_amaclar=tuple(dil["alt_amaclar"]),
        aktiviteler=tuple(dil["aktiviteler"]),
        ziyaret_baglamlari=tuple(dil["ziyaret_baglamlari"]),
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
        desteklenmeyen_istekler=tuple(dil["desteklenmeyen_istekler"]),
        normalize_edilmis_input=str(dil["normalize_edilmis_input"]),
        celisen_niyet=bool(dil["celisen_niyet"]),
    )


def _ozet(sehir: str, niyet: CozulmusNiyet) -> str:
    parcalar = [niyet.ilce or sehir]
    if niyet.kisi_baglami:
        parcalar.append(KISI_ETIKETLERI.get(niyet.kisi_baglami, niyet.kisi_baglami))
    if niyet.amac:
        parcalar.append(AMAC_ETIKETLERI[niyet.amac])
    parcalar.extend(a.replace("_", " ") for a in niyet.aktiviteler)
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


def _anlasilan_ihtiyac(sehir: str, niyet: CozulmusNiyet) -> dict[str, object]:
    return {
        "kisi_baglami": niyet.kisi_baglami,
        "ana_amac": niyet.amac,
        "alt_amaclar": list(niyet.alt_amaclar),
        "aktiviteler": list(niyet.aktiviteler),
        "ziyaret_baglamlari": list(niyet.ziyaret_baglamlari),
        "sehir": sehir,
        "ilce": niyet.ilce,
        "zaman": niyet.istenen_zaman,
        "ulasim": niyet.ulasim_bicimi,
        "butce_ust_siniri": niyet.butce_ust_siniri,
        "zorunlu_kosullar": list(niyet.zorunlu_kosullar),
        "tercihler": list(niyet.tercihler),
        "desteklenmeyen_istekler": list(niyet.desteklenmeyen_istekler),
    }


def _dogrulanamayanlar(niyet: CozulmusNiyet) -> list[str]:
    bilinmeyenler = [
        ISTEK_ETIKETLERI.get(kod, kod.replace("_", " ")) for kod in niyet.desteklenmeyen_istekler
    ]
    if any(
        alt not in {"gezme", "birlikte_vakit", "aileyle_vakit"}
        and not (niyet.amac == "calisma" and alt == "kahve_icmek")
        for alt in niyet.alt_amaclar
    ):
        bilinmeyenler.append("Birden fazla etkinliğin aynı planda birleştirilmesi")
    if niyet.butce_ust_siniri is not None:
        bilinmeyenler.append("Güncel fiyatın bütçe sınırını karşılaması")
    return bilinmeyenler


@gelistirme_izi
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
            "Güncel çalışma saatlerini doğrulayamadığımız için "
            "şu an açık olduğunu söyleyemiyoruz."
        ),
    )
    ozet = _ozet(sehir.isim, niyet)
    anlasilan = _anlasilan_ihtiyac(sehir.isim, niyet)
    iz_guncelle(oturum, parsed_intent=anlasilan)
    dogrulanamayanlar = _dogrulanamayanlar(niyet)
    if niyet.amac is None or niyet.celisen_niyet:
        return BugunNeYapalimCevabi(
            durum="clarification",
            anlasilan_ihtiyac_ozeti=ozet,
            anlasilan_ihtiyac=anlasilan,
            durum_aciklamasi=(
                "Niyetin bir bölümünü anladık; sonucu gerçekten değiştirecek "
                "tek noktayı netleştirelim."
            ),
            dogrulanamayan_ihtiyaclar=dogrulanamayanlar,
            netlestirme=NetlestirmeSemasi(
                soru="Nasıl bir şey düşünüyorsunuz?",
                alan="amac",
                secenekler=[
                    {"deger": kod, "etiket": AMAC_ETIKETLERI[kod].capitalize()}
                    for kod in ("kahve_icmek", "yemek_yemek", "gezme", "eglence")
                ],
            ),
            baglam=baglam,
            bugun_baglami=bugun,
        )
    sorgu = AMAC_SORGULARI[niyet.amac]
    desteklenmeyen = [kod for kod in niyet.zorunlu_kosullar if kod not in SOMUT_KOSULLAR]
    amac_desteklenmiyor = niyet.amac not in KARARDA_DESTEKLENEN_AMACLAR
    if desteklenmeyen or niyet.butce_ust_siniri is not None or amac_desteklenmiyor:
        nedenler = []
        if desteklenmeyen:
            etiketler = ", ".join(
                ISTEK_ETIKETLERI.get(kod, kod.replace("_", " ")) for kod in desteklenmeyen
            )
            nedenler.append(f"{etiketler} konusunda henüz yeterli doğrulanmış bilgimiz yok")
        if niyet.butce_ust_siniri is not None:
            nedenler.append("bütçe sınırını karşılaştırabileceğimiz güncel fiyat bilgisi yok")
        if amac_desteklenmiyor:
            nedenler.append(
                f"{AMAC_ETIKETLERI[niyet.amac]} için henüz yeterli doğrulanmış bilgimiz yok"
            )
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
            anlasilan_ihtiyac=anlasilan,
            durum_aciklamasi=(
                "Ne aradığını anladık; ancak bu ihtiyacı güvenilir biçimde "
                "değerlendirecek doğrulanmış bilgi henüz yeterli değil."
            ),
            dogrulanamayan_ihtiyaclar=dogrulanamayanlar,
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
    if not kesfet.secenekler and kesfet.degerlendirilemeyen_aday_sayisi:
        dogrulanamayanlar.extend(SOMUT_KOSULLAR[kod].etiket for kod in zorunlu)
    for secenek in kesfet.secenekler:
        for gerekce in (*secenek.karar_sonucu.bilinmeyenler, *secenek.karar_sonucu.onemli_odunler):
            if gerekce.kod == "tercih_bilinmiyor" and gerekce.ilgili_kosul in SOMUT_KOSULLAR:
                dogrulanamayanlar.append(SOMUT_KOSULLAR[gerekce.ilgili_kosul].etiket)
    dogrulanamayanlar = list(dict.fromkeys(dogrulanamayanlar))
    return BugunNeYapalimCevabi(
        durum=kesfet.durum,
        anlasilan_ihtiyac_ozeti=ozet,
        anlasilan_ihtiyac=anlasilan,
        durum_aciklamasi=(
            "Niyetini anladık ve doğrulayabildiğimiz kısmıyla seçenekleri değerlendirdik."
            if kesfet.secenekler
            else "Niyetini anladık; doğrulanmış aday kapsamımız bu istek için yeterli değil."
        ),
        dogrulanamayan_ihtiyaclar=dogrulanamayanlar,
        baglam=baglam,
        bugun_baglami=bugun,
        kesfet=kesfet,
        kesfet_sorgusu=sorgu,
    )
