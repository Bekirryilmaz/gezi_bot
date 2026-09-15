from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import uuid
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from sunucu.bilgi.domain import HakDurumu
from sunucu.veritabani.admin_modelleri import IncelemeDosyasi
from sunucu.veritabani.baglanti import OturumUretici
from sunucu.veritabani.bilgi_modelleri import (
    Gozlem,
    Iddia,
    IddiaSurumu,
    KanitBaglantisi,
    KaynakPolitikasi,
    VeriBatch,
)
from sunucu.veritabani.kimlik_modelleri import Sube
from sunucu.veritabani.modeller import Yer, YerKaynak
from sunucu.veritabani.yayin_modelleri import YayinKaydi

OSM_KAYNAK = "openstreetmap"
VARSAYILAN_KATEGORILER = ("kafe", "restoran_lokanta", "tarihi_kulturel")
AMAC_ESLEMESI = {
    "kafe": ("kahve_icmek",),
    "restoran_lokanta": ("yemek_yemek",),
    "tarihi_kulturel": ("tarihi_kulturel_ziyaret",),
    "tatli_pastane": ("tatli_yemek",),
    "eglence_aktivite": ("eglence",),
    "doga_manzara": ("acik_hava",),
    "plaj_su": ("acik_hava",),
}

# Sayisal esik bilincli olarak yoktur. Bu aileler ancak operasyon karariyla
# azami yasa kavusur; o zamana kadar yeniden toplama/dogrulama olayi eskitir.
FRESHNESS_POLITIKALARI: dict[str, dict[str, str | int | None]] = {
    "amac_destegi": {
        "kategori": "yer_turu",
        "gerekce": "Kaynak siniflandirmasi degisebilir.",
        "yeniden_dogrulama": "Yeni OSM cekimi veya tur degisikligi.",
        "azami_yas_gun": None,
    },
    "yer_turu": {
        "kategori": "yer_turu",
        "gerekce": "Faaliyet veya kullanim degisebilir.",
        "yeniden_dogrulama": "Yeni OSM cekimi veya kimlik duzeltmesi.",
        "azami_yas_gun": None,
    },
    "adres": {
        "kategori": "kimlik_cografya",
        "gerekce": "Adres yapisal ama degisebilir.",
        "yeniden_dogrulama": "Yeni OSM cekimi veya adres duzeltmesi.",
        "azami_yas_gun": None,
    },
    "telefon": {
        "kategori": "iletisim",
        "gerekce": "Isletmeciyle hizli degisebilir.",
        "yeniden_dogrulama": "Yeni OSM cekimi veya isletmeci degisikligi.",
        "azami_yas_gun": None,
    },
    "web_sitesi": {
        "kategori": "iletisim",
        "gerekce": "Alan adi ve isletmeci degisebilir.",
        "yeniden_dogrulama": "Yeni OSM cekimi veya isletmeci degisikligi.",
        "azami_yas_gun": None,
    },
    "wifi": {
        "kategori": "olanak",
        "gerekce": "Hizmet sunumu degisebilir.",
        "yeniden_dogrulama": "Yeni OSM cekimi veya yerel dogrulama.",
        "azami_yas_gun": None,
    },
    "tekerlekli_sandalye_erisimi": {
        "kategori": "fiziksel_erisim",
        "gerekce": "Tadilat veya kullanilan bolum kapsami degisebilir.",
        "yeniden_dogrulama": "Yeni OSM cekimi ve kritik kullanimda insan kontrolu.",
        "azami_yas_gun": None,
    },
    "ucretsiz": {
        "kategori": "maliyet",
        "gerekce": "Ucret politikasi degisebilir.",
        "yeniden_dogrulama": "Yeni OSM cekimi veya resmi tarife kontrolu.",
        "azami_yas_gun": None,
    },
}

OSM_HAK_DAYANAGI = (
    "Repo README.md OSM atfini/ODbL'yi korur; veri/toplayicilar/osm_toplayici.py "
    "OSM verisini ticari kullanima uygun acik veri olarak tanimlar. Resmi kosullar: "
    "https://www.openstreetmap.org/copyright (ODbL, OpenStreetMap ve katilimcilari atfi, "
    "turev veritabani icin ayni lisans kosulu)."
)


@dataclass(frozen=True)
class AdayKaydi:
    kaynak_kayit_id: str
    aile: str
    kaynak_alani: str
    deger: Any
    kapsam: dict[str, Any]
    cekilme_zamani: datetime
    kaynak_url: str | None
    icerik_ozeti: dict[str, Any]


@dataclass
class PilotOzet:
    kaynak_satiri: int = 0
    secilen_yer: int = 0
    eslesen_sube: int = 0
    eslesmeyen_sube: int = 0
    aday_toplam: int = 0
    yeni_gozlem: int = 0
    yeni_claim: int = 0
    yeni_surum: int = 0
    yeni_inceleme: int = 0
    ayni_aday: int = 0
    hak_nedeniyle_engellenen: int = 0
    geri_cekilmis_kaynak_engeli: int = 0
    aileler: dict[str, int] | None = None

    def sozluk(self) -> dict[str, Any]:
        sonuc = asdict(self)
        sonuc["aileler"] = dict(sorted((self.aileler or {}).items()))
        return sonuc


def _uuid5(anahtar: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"samandira:pilot-claim:{anahtar}"))


def _json_hash(deger: Any) -> str:
    ham = json.dumps(deger, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(ham.encode("utf-8")).hexdigest()


def _zaman(deger: str | None) -> datetime:
    if not deger:
        return datetime.now(UTC)
    sonuc = datetime.fromisoformat(deger.replace("Z", "+00:00"))
    return sonuc if sonuc.tzinfo else sonuc.replace(tzinfo=UTC)


_BOS_YER_TUTUCULAR = {"-", "n/a", "na", "none", "null", "unknown", "bilinmiyor", "yok"}
_TELEFON_KARAKTERLERI = re.compile(r"^\+?[0-9 ()\-./]+$")


def kaynak_boolean_normalize(deger: Any, *, aile: str) -> bool | None:
    """Yalniz acik ve ailece anlamli degerleri boolean'a cevirir.

    Candidate katmani bazen normalized JSON yerine ham kaynak degeriyle de
    cagrilabilir. Python'in ``bool('no') is True`` davranisi burada kullanilmaz.
    ``customers`` ve ``limited`` olumlu iddia icin yeterince kesin degildir.
    """
    if isinstance(deger, bool):
        return deger
    if isinstance(deger, int) and deger in {0, 1}:
        return bool(deger)
    if not isinstance(deger, str):
        return None
    temiz = deger.casefold().strip()
    if temiz in {"yes", "true", "1", "evet"}:
        return True
    if temiz in {"no", "false", "0", "hayir", "hayır"}:
        return False
    if aile == "wifi" and temiz == "wlan":
        return True
    return None


def telefon_candidate_degeri(deger: Any) -> str | None:
    if not isinstance(deger, str):
        return None
    temiz = deger.strip()
    if temiz.casefold() in _BOS_YER_TUTUCULAR or not _TELEFON_KARAKTERLERI.fullmatch(temiz):
        return None
    rakamlar = re.sub(r"\D", "", temiz)
    if not 7 <= len(rakamlar) <= 15 or len(set(rakamlar)) == 1:
        return None
    return temiz


def web_sitesi_candidate_degeri(deger: Any) -> str | None:
    if not isinstance(deger, str):
        return None
    temiz = deger.strip()
    if temiz.casefold() in _BOS_YER_TUTUCULAR:
        return None
    ayrik = urlparse(temiz)
    if ayrik.scheme not in {"http", "https"} or not ayrik.hostname or "." not in ayrik.hostname:
        return None
    return temiz


def metin_candidate_degeri(deger: Any) -> str | None:
    if not isinstance(deger, str):
        return None
    temiz = deger.strip()
    return temiz if temiz and temiz.casefold() not in _BOS_YER_TUTUCULAR else None


def kaynak_haklari_uygun_mu(
    politika: KaynakPolitikasi | None, *, simdi: datetime | None = None
) -> tuple[bool, str | None]:
    simdi = simdi or datetime.now(UTC)
    if politika is None:
        return False, "kaynak_politikasi_yok"
    if politika.gecerli_baslangic and politika.gecerli_baslangic > simdi:
        return False, "kaynak_politikasi_henuz_gecerli_degil"
    if politika.gecerli_bitis and politika.gecerli_bitis <= simdi:
        return False, "kaynak_politikasi_geri_cekilmis_veya_suresi_dolmus"
    alanlar = (
        politika.kamusal_gosterim,
        politika.turev_iddia,
        politika.ai_isleme,
        politika.uzun_sureli_saklama,
    )
    if any(deger != HakDurumu.IZINLI.value for deger in alanlar):
        return False, "display_derivative_processing_retention_hakki_yetersiz"
    return True, None


def osm_politikasini_uygula(oturum: Session) -> KaynakPolitikasi:
    politika = oturum.query(KaynakPolitikasi).filter_by(kaynak=OSM_KAYNAK).first()
    if politika is None:
        politika = KaynakPolitikasi(kaynak=OSM_KAYNAK)
        oturum.add(politika)
    politika.kamusal_gosterim = HakDurumu.IZINLI.value
    politika.turev_iddia = HakDurumu.IZINLI.value
    politika.ai_isleme = HakDurumu.IZINLI.value
    politika.uzun_sureli_saklama = HakDurumu.IZINLI.value
    politika.dayanak_notu = OSM_HAK_DAYANAGI
    politika.gecerli_baslangic = datetime.now(UTC)
    politika.gecerli_bitis = None
    oturum.flush()
    return politika


def osm_satirlarini_oku(dosya: Path) -> list[dict[str, Any]]:
    satirlar: list[dict[str, Any]] = []
    with dosya.open("r", encoding="utf-8") as akim:
        for satir in akim:
            if satir.strip():
                satirlar.append(json.loads(satir))
    return satirlar


def _aday_sayisi(satir: dict[str, Any]) -> int:
    return len(satirdan_adaylar(satir))


def pilot_satirlarini_sec(
    satirlar: Iterable[dict[str, Any]],
    *,
    kategoriler: set[str],
    ilceler: set[str] | None,
    kategori_basina_limit: int | None,
    asgari_aday_sayisi: int = 1,
) -> list[dict[str, Any]]:
    ilce_norm = {x.casefold().strip() for x in ilceler} if ilceler else None
    uygun = [
        satir
        for satir in satirlar
        if satir.get("kaynak") == OSM_KAYNAK
        and satir.get("alt_kategori") in kategoriler
        and _aday_sayisi(satir) >= asgari_aday_sayisi
        and (ilce_norm is None or str(satir.get("ilce") or "").casefold().strip() in ilce_norm)
    ]
    sonuc: list[dict[str, Any]] = []
    for kategori in sorted(kategoriler):
        grup = [s for s in uygun if s.get("alt_kategori") == kategori]
        grup.sort(key=lambda s: (-_aday_sayisi(s), str(s.get("kaynak_id") or "")))
        sonuc.extend(grup if kategori_basina_limit is None else grup[:kategori_basina_limit])
    return sonuc


def satirdan_adaylar(satir: dict[str, Any]) -> list[AdayKaydi]:
    kategori = str(satir["alt_kategori"])
    ortak_kapsam = {
        "sehir": satir.get("sehir"),
        "ilce": satir.get("ilce"),
        "ana_kategori": satir.get("ana_kategori"),
        "alt_kategori": kategori,
        "sube_kapsami": "tam_sube",
    }
    ortak = {
        "kaynak_kayit_id": str(satir["kaynak_id"]),
        "cekilme_zamani": _zaman(satir.get("cekilme_zamani")),
        "kaynak_url": satir.get("kaynak_url"),
    }
    adaylar: list[AdayKaydi] = []

    def ekle(aile: str, alan: str, deger: Any, *, kapsam: dict[str, Any] | None = None) -> None:
        adaylar.append(
            AdayKaydi(
                **ortak,
                aile=aile,
                kaynak_alani=alan,
                deger=deger,
                kapsam={**ortak_kapsam, "kaynak_alani": alan, **(kapsam or {})},
                icerik_ozeti={
                    "kaynak_alani": alan,
                    "deger": deger,
                    "kaynak_kayit_id": satir["kaynak_id"],
                    "kaynak_ismi": satir.get("isim"),
                    "konum": {"enlem": satir.get("enlem"), "boylam": satir.get("boylam")},
                },
            )
        )

    ekle(
        "yer_turu",
        "ana_kategori+alt_kategori",
        {"ana_kategori": satir["ana_kategori"], "alt_kategori": kategori},
    )
    amaclar = AMAC_ESLEMESI.get(kategori)
    if amaclar:
        ekle(
            "amac_destegi",
            "alt_kategori",
            list(amaclar),
            kapsam={"cikarim_turu": "deterministik_dar_tur_eslemesi"},
        )
    adres = metin_candidate_degeri(satir.get("adres"))
    telefon = telefon_candidate_degeri(satir.get("telefon"))
    web_sitesi = web_sitesi_candidate_degeri(satir.get("web_sitesi"))
    for alan, deger in (("adres", adres), ("telefon", telefon), ("web_sitesi", web_sitesi)):
        if deger is not None:
            ekle(alan, alan, deger)
    ozellikler = satir.get("ozellikler") or {}
    for kaynak_alani, aile in (
        ("wifi", "wifi"),
        ("engelli_erisimi", "tekerlekli_sandalye_erisimi"),
        ("ucretsiz", "ucretsiz"),
    ):
        deger = kaynak_boolean_normalize(ozellikler.get(kaynak_alani), aile=aile)
        if deger is not None:
            ekle(aile, f"ozellikler.{kaynak_alani}", deger)
    return adaylar


def _batch_getir(oturum: Session, dosya: Path, satirlar: list[dict[str, Any]]) -> VeriBatch:
    dosya_hash = _json_hash(satirlar)
    kosu = f"pilot:{dosya.name}:{dosya_hash[:16]}"
    batch = oturum.query(VeriBatch).filter_by(kaynak=OSM_KAYNAK, kosu_anahtari=kosu).first()
    if batch:
        return batch
    zamanlar = [_zaman(s.get("cekilme_zamani")) for s in satirlar]
    batch = VeriBatch(
        id=_uuid5(f"batch:{kosu}"),
        kaynak=OSM_KAYNAK,
        kosu_anahtari=kosu,
        kok_tanimi={"dosya": str(dosya), "sha256": dosya_hash, "kayit_sayisi": len(satirlar)},
        baslama_zamani=min(zamanlar) if zamanlar else datetime.now(UTC),
        cekilme_baslangici=min(zamanlar) if zamanlar else None,
        cekilme_bitisi=max(zamanlar) if zamanlar else None,
        tamamlanma_zamani=max(zamanlar) if zamanlar else None,
    )
    oturum.add(batch)
    oturum.flush()
    return batch


def _inceleme_ekle(oturum: Session, iddia: Iddia, surum: IddiaSurumu) -> bool:
    dosya_id = _uuid5(f"review:{iddia.id}:{surum.surum_no}")
    if oturum.get(IncelemeDosyasi, dosya_id):
        return False
    oturum.add(
        IncelemeDosyasi(
            id=dosya_id,
            dosya_turu="claim_candidate",
            nesne_turu="claim",
            nesne_id=iddia.id,
            durum="bekliyor",
            risk_sinifi="kritik" if iddia.aile == "tekerlekli_sandalye_erisimi" else "normal",
            onerilen_eylem="claim_approve",
            komut_payload={"iddia_surumu_id": surum.id, "uretim": "structured_osm_v1"},
            acan_aktor_id=None,
            karar_gerekcesi=(
                "Yapilandirilmis OSM alanindan deterministik candidate; "
                "insan incelemesi bekliyor."
            ),
        )
    )
    return True


def adaylari_yaz(
    oturum: Session,
    *,
    dosya: Path,
    satirlar: list[dict[str, Any]],
    dry_run: bool,
) -> PilotOzet:
    ozet = PilotOzet(kaynak_satiri=len(satirlar), secilen_yer=len(satirlar), aileler={})
    politika = oturum.query(KaynakPolitikasi).filter_by(kaynak=OSM_KAYNAK).first()
    hak_uygun, hak_nedeni = kaynak_haklari_uygun_mu(politika)
    tum_adaylar = [(satir, aday) for satir in satirlar for aday in satirdan_adaylar(satir)]
    ozet.aday_toplam = len(tum_adaylar)
    ozet.aileler = dict(Counter(aday.aile for _, aday in tum_adaylar))
    if not hak_uygun:
        ozet.hak_nedeniyle_engellenen = len(tum_adaylar)
        if hak_nedeni == "kaynak_politikasi_geri_cekilmis_veya_suresi_dolmus":
            ozet.geri_cekilmis_kaynak_engeli = len(tum_adaylar)
        return ozet
    if dry_run:
        return ozet

    batch = _batch_getir(oturum, dosya, satirlar)
    kaynak_baglari = {
        str(kaynak_id): str(sube_id)
        for kaynak_id, sube_id in oturum.query(YerKaynak.kaynak_id, YerKaynak.sube_id)
        .filter(YerKaynak.kaynak == OSM_KAYNAK)
        .all()
    }
    eslesen_kayitlar: set[str] = set()
    for _, aday in tum_adaylar:
        sube_id = kaynak_baglari.get(aday.kaynak_kayit_id)
        if not sube_id:
            continue
        eslesen_kayitlar.add(aday.kaynak_kayit_id)
        gozlem_hash = _json_hash({"aile": aday.aile, "deger": aday.deger, "kapsam": aday.kapsam})
        gozlem_id = _uuid5(
            f"observation:{batch.id}:{aday.kaynak_kayit_id}:{aday.kaynak_alani}:{gozlem_hash}"
        )
        gozlem = oturum.get(Gozlem, gozlem_id)
        if gozlem is None:
            gozlem = Gozlem(
                id=gozlem_id,
                veri_batch_id=batch.id,
                kaynak=OSM_KAYNAK,
                kaynak_kayit_id=aday.kaynak_kayit_id,
                kaynak_url=aday.kaynak_url,
                kaynakta_gozlemlenme_zamani=None,
                cekilme_zamani=aday.cekilme_zamani,
                dogrulanma_zamani=None,
                icerik_ozeti=aday.icerik_ozeti,
                icerik_hash=gozlem_hash,
            )
            oturum.add(gozlem)
            oturum.flush()
            ozet.yeni_gozlem += 1

        claim_id = _uuid5(f"claim:{sube_id}:{aday.aile}:{_json_hash(aday.kapsam)}")
        iddia = oturum.get(Iddia, claim_id)
        if iddia is None:
            iddia = Iddia(id=claim_id, sube_id=sube_id, aile=aday.aile, kapsam=aday.kapsam)
            oturum.add(iddia)
            oturum.flush()
            ozet.yeni_claim += 1
        onceki = (
            oturum.query(IddiaSurumu)
            .filter_by(iddia_id=iddia.id, surum_no=iddia.aktif_surum_no)
            .first()
            if iddia.aktif_surum_no
            else None
        )
        if onceki and onceki.deger == {"deger": aday.deger}:
            ozet.ayni_aday += 1
            continue
        if onceki and (
            onceki.yayin_durumu == "geri_cekilmis" or onceki.bilgi_durumu == "geri_cekilmis"
        ):
            ozet.geri_cekilmis_kaynak_engeli += 1
            continue
        surum_no = (iddia.aktif_surum_no or 0) + 1
        surum = IddiaSurumu(
            iddia_id=iddia.id,
            surum_no=surum_no,
            deger={"deger": aday.deger},
            bilgi_durumu="celiskili" if onceki else "biliniyor",
            guven_sinifi="belirsiz",
            gecerlilik_baslangici=aday.cekilme_zamani,
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
                gerekce=f"Yapilandirilmis kaynak alani: {aday.kaynak_alani}",
            )
        )
        if onceki:
            onceki_baglar = (
                oturum.query(KanitBaglantisi)
                .filter_by(iddia_surumu_id=onceki.id, rol="supporting")
                .all()
            )
            for bag in onceki_baglar:
                oturum.add(
                    KanitBaglantisi(
                        iddia_surumu_id=surum.id,
                        gozlem_id=bag.gozlem_id,
                        rol="counter",
                        gerekce="Onceki aktif surumle yapilandirilmis deger celiskisi.",
                    )
                )
        iddia.aktif_surum_no = surum_no
        if _inceleme_ekle(oturum, iddia, surum):
            ozet.yeni_inceleme += 1
        ozet.yeni_surum += 1
    ozet.eslesen_sube = len(eslesen_kayitlar)
    ozet.eslesmeyen_sube = len({str(s["kaynak_id"]) for s in satirlar} - eslesen_kayitlar)
    oturum.flush()
    return ozet


def coverage_raporu(oturum: Session, *, kategoriler: set[str]) -> dict[str, Any]:
    pilot_yer = (
        oturum.query(Yer.id)
        .join(YerKaynak, YerKaynak.yer_id == Yer.id)
        .filter(YerKaynak.kaynak == OSM_KAYNAK, Yer.alt_kategori.in_(kategoriler))
        .distinct()
        .subquery()
    )
    toplam = oturum.query(func.count()).select_from(pilot_yer).scalar() or 0
    yayinli_claimler = (
        oturum.query(Iddia.aile, Iddia.sube_id, IddiaSurumu.bilgi_durumu)
        .join(Sube, Sube.id == Iddia.sube_id)
        .join(pilot_yer, pilot_yer.c.id == Sube.legacy_yer_id)
        .join(
            IddiaSurumu,
            and_(IddiaSurumu.iddia_id == Iddia.id, IddiaSurumu.surum_no == Iddia.aktif_surum_no),
        )
        .join(YayinKaydi, and_(YayinKaydi.nesne_turu == "claim", YayinKaydi.nesne_id == Iddia.id))
        .filter(
            YayinKaydi.aktif_mi.is_(True),
            YayinKaydi.durum.in_(("yayinlanabilir", "sinirli_yayinlanabilir")),
        )
        .all()
    )
    aile_yerleri: dict[str, set[str]] = {}
    claimli_yerler: set[str] = set()
    durumlar = Counter()
    for aile, sube_id, durum in yayinli_claimler:
        claimli_yerler.add(str(sube_id))
        aile_yerleri.setdefault(aile, set()).add(str(sube_id))
        durumlar[durum] += 1
    bekleyen = (
        oturum.query(IncelemeDosyasi)
        .filter(
            IncelemeDosyasi.dosya_turu == "claim_candidate", IncelemeDosyasi.durum != "tamamlandi"
        )
        .count()
    )
    aktif_durumlar = Counter(
        durum
        for (durum,) in (
            oturum.query(IddiaSurumu.bilgi_durumu)
            .join(Iddia, Iddia.id == IddiaSurumu.iddia_id)
            .join(Sube, Sube.id == Iddia.sube_id)
            .join(pilot_yer, pilot_yer.c.id == Sube.legacy_yer_id)
            .filter(IddiaSurumu.surum_no == Iddia.aktif_surum_no)
            .all()
        )
    )
    hak_engelli = (
        oturum.query(KaynakPolitikasi).filter(KaynakPolitikasi.kaynak == OSM_KAYNAK).first()
    )
    hak_uygun, _ = kaynak_haklari_uygun_mu(hak_engelli)
    return {
        "pilot_kategorileri": sorted(kategoriler),
        "toplam_yer": int(toplam),
        "claimi_olan_yer": len(claimli_yerler),
        "claim_ailesi_coverage": {
            aile: {"yer": len(ids), "oran": round(len(ids) / toplam, 4) if toplam else 0}
            for aile, ids in sorted(aile_yerleri.items())
        },
        "unknown_orani": round((toplam - len(claimli_yerler)) / toplam, 4) if toplam else 0,
        "stale": aktif_durumlar["eskimis"],
        "conflicting": aktif_durumlar["celiskili"],
        "hak_nedeniyle_kullanilamayan_oran": 0 if hak_uygun else 1,
        "admin_review_bekleyen": bekleyen,
        "yayinlanmis_claim": len(yayinli_claimler),
    }


def _varsayilan_osm_dosyasi() -> Path:
    kok = Path(__file__).resolve().parents[2]
    dosyalar = sorted((kok / "veri" / "cikti" / "ham" / "osm").glob("samsun_*.jsonl"))
    if not dosyalar:
        raise FileNotFoundError("Samsun OSM JSONL dosyasi bulunamadi.")
    return dosyalar[-1]


def _ana() -> None:
    ayristirici = argparse.ArgumentParser(
        description="Gercek OSM verisinden guvenli Samsun pilot claim candidate'lari uretir."
    )
    ayristirici.add_argument("--dosya", type=Path, default=None)
    ayristirici.add_argument("--kategori", action="append", dest="kategoriler")
    ayristirici.add_argument("--ilce", action="append", dest="ilceler")
    ayristirici.add_argument("--kategori-basina-limit", type=int, default=20)
    ayristirici.add_argument(
        "--asgari-aday-sayisi",
        type=int,
        default=1,
        help="Veri-zenginlik kapisi: yer turu dahil en az kac yapilandirilmis aday gerekli.",
    )
    ayristirici.add_argument(
        "--yaz",
        action="store_true",
        help="Yalniz development DB'ye candidate ve inceleme kaydi yazar.",
    )
    ayristirici.add_argument(
        "--osm-politikasini-uygula",
        action="store_true",
        help="Repo ve resmi ODbL dayanagina bagli OSM hak kaydini uygular.",
    )
    ayristirici.add_argument(
        "--summary", action="store_true", help="Mevcut pilot coverage raporunu da yazdirir."
    )
    args = ayristirici.parse_args()
    if args.yaz and os.environ.get("UYGULAMA_ORTAMI", "development").lower() in {
        "production",
        "prod",
        "canli",
    }:
        raise SystemExit("Production ortaminda yazma engellendi.")
    dosya = args.dosya or _varsayilan_osm_dosyasi()
    kategoriler = set(args.kategoriler or VARSAYILAN_KATEGORILER)
    tum = osm_satirlarini_oku(dosya)
    secilen = pilot_satirlarini_sec(
        tum,
        kategoriler=kategoriler,
        ilceler=set(args.ilceler) if args.ilceler else None,
        kategori_basina_limit=args.kategori_basina_limit,
        asgari_aday_sayisi=args.asgari_aday_sayisi,
    )
    with OturumUretici() as oturum:
        if args.osm_politikasini_uygula:
            if not args.yaz:
                raise SystemExit("Kaynak politikasi degisikligi icin --yaz da gereklidir.")
            osm_politikasini_uygula(oturum)
        ozet = adaylari_yaz(oturum, dosya=dosya, satirlar=secilen, dry_run=not args.yaz)
        if args.yaz:
            oturum.commit()
        print(
            json.dumps(
                {
                    "mod": "candidate-only" if args.yaz else "dry-run",
                    "otomatik_yayin": False,
                    "ozet": ozet.sozluk(),
                },
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )
        if args.summary:
            print(
                json.dumps(
                    {"coverage": coverage_raporu(oturum, kategoriler=kategoriler)},
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                )
            )


if __name__ == "__main__":
    _ana()
