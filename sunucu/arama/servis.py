from __future__ import annotations

import base64
import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Float, and_, func, or_, select
from sqlalchemy.orm import Session, aliased

from ortak.sabitler import (
    AnaKategori,
    GezilecekYerAltKategori,
    KonaklamaAltKategori,
    YemeIcmeAltKategori,
)
from sunucu.arama.domain import (
    SOMUT_KOSULLAR,
    AramaSonucuTuru,
    EslesmeNedeni,
    kosul_durumu,
)
from sunucu.arama.normalizasyon import baglam_tokenini_cikar, turkce_arama_normalize
from sunucu.arama.semalar import (
    AramaCevabi,
    AramaCografyaSemasi,
    AramaFiltreBaglamiSemasi,
    AramaFiltreleriCevabi,
    AramaSonucuSemasi,
    AramaYerKimligiSemasi,
    FiltreSecenegiSemasi,
    IlceSecenegiSemasi,
    TurSecenegiSemasi,
)
from sunucu.bilgi.domain import BilgiDurumu
from sunucu.bugun_ne_yapalim.gelistirme_izi import iz_artir, iz_guncelle
from sunucu.karar_motoru.domain import KosulDurumu
from sunucu.karar_motoru.semalar import CografiBaglamSemasi, TercihSemasi, ZorunluKosulSemasi
from sunucu.veritabani.arama_modelleri import Ilce
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu
from sunucu.veritabani.kimlik_modelleri import Sube, YerKimligi
from sunucu.veritabani.modeller import Sehir, Yer
from sunucu.veritabani.yayin_modelleri import YayinKaydi
from sunucu.yayin.domain import KullanimTuru
from sunucu.yayin.servis import KAMUSAL_DURUMLAR, yayin_kaydi_kamusal_mi
from veri.ortak.sehir_ayarlari import sehir_anahtarini_isme_gore_bul


def _etiket(kod: str) -> str:
    ozel = {
        "gezilecek_yer": "Gezilecek yer",
        "yeme_icme": "Yeme içme",
        "konaklama": "Konaklama",
        "kahve_uzmanlik": "Kahve",
        "restoran_lokanta": "Restoran",
        "tarihi_kulturel": "Tarih ve kültür",
        "doga_manzara": "Doğa ve manzara",
    }
    return ozel.get(kod, kod.replace("_", " ").capitalize())


TUR_KODLARI = tuple(
    dict.fromkeys(
        [
            *(uye.value for uye in AnaKategori),
            *(uye.value for uye in GezilecekYerAltKategori),
            *(uye.value for uye in KonaklamaAltKategori),
            *(uye.value for uye in YemeIcmeAltKategori),
        ]
    )
)
TUR_ESLESMELERI = {turkce_arama_normalize(_etiket(kod)): kod for kod in TUR_KODLARI}
TUR_ESLESMELERI.update({"kafe": "kafe", "kahve": "kahve_uzmanlik", "restoran": "restoran_lokanta"})


@dataclass(frozen=True)
class _Aday:
    yer: Yer
    sehir: Sehir
    sube: Sube
    kimlik: YerKimligi
    ilce: Ilce | None
    benzerlik: float
    sonuc_turu: AramaSonucuTuru
    neden: EslesmeNedeni
    kosul_durumlari: dict[str, KosulDurumu]
    tercih_puani: int
    olumsuz_tercih: int


def _sehir_anahtari(sehir: Sehir) -> str:
    return sehir_anahtarini_isme_gore_bul(sehir.isim) or turkce_arama_normalize(sehir.isim)


def _kamusal_kosullar(yayin, kullanim: KullanimTuru) -> tuple:
    return (
        yayin.nesne_turu == "yer",
        yayin.nesne_id == Yer.id,
        yayin.aktif_mi.is_(True),
        yayin.durum.in_(KAMUSAL_DURUMLAR),
        yayin.izinli_kullanimlar.contains([kullanim.value]),
    )


def _sehir_coz(oturum: Session, deger: str | None) -> Sehir:
    sorgu = select(Sehir).where(Sehir.aktif_mi.is_(True))
    if deger:
        normalize = turkce_arama_normalize(deger)
        kimlik_mi = True
        try:
            UUID(deger)
        except ValueError:
            kimlik_mi = False
        sorgu = sorgu.where(
            or_(Sehir.id == deger, Sehir.arama_isim == normalize)
            if kimlik_mi
            else Sehir.arama_isim == normalize
        )
    else:
        sorgu = sorgu.order_by(Sehir.isim)
    sehir = oturum.scalar(sorgu.limit(1))
    if sehir is None:
        raise ValueError("Gecerli ve aktif bir sehir bulunamadi.")
    return sehir


def _ilce_coz(oturum: Session, ilce_id: str | None, sehir: Sehir) -> Ilce | None:
    if not ilce_id:
        return None
    try:
        UUID(ilce_id)
    except ValueError as hata:
        raise ValueError("Ilce filtresi canonical UUID olmalidir.") from hata
    ilce = oturum.scalar(select(Ilce).where(Ilce.id == ilce_id, Ilce.aktif_mi.is_(True)))
    if ilce is None:
        raise ValueError("Canonical ilce kimligi bulunamadi.")
    if str(ilce.sehir_id) != str(sehir.id):
        raise ValueError("Ilce secilen sehre ait degil.")
    return ilce


def _cursor_coz(cursor: str | None, imza: str) -> int:
    if not cursor:
        return 0
    try:
        veri = json.loads(base64.urlsafe_b64decode(cursor + "===").decode("utf-8"))
        if veri.get("i") != imza or not isinstance(veri.get("o"), int) or veri["o"] < 0:
            raise ValueError
        return veri["o"]
    except (ValueError, TypeError, json.JSONDecodeError, UnicodeDecodeError) as hata:
        raise ValueError("Cursor bu arama baglamina ait degil.") from hata


def _cursor_uret(offset: int, imza: str) -> str:
    ham = json.dumps({"i": imza, "o": offset}, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(ham).decode("ascii").rstrip("=")


def _claim_durumlari(
    oturum: Session, sube_idleri: list[str], kosul_kodlari: list[str]
) -> dict[str, dict[str, KosulDurumu]]:
    sonuc = {sube_id: {kod: KosulDurumu.DEGERLENDIRILEMIYOR for kod in kosul_kodlari} for sube_id in sube_idleri}
    if not sube_idleri or not kosul_kodlari:
        return sonuc
    aile_kodlari: dict[str, list[str]] = defaultdict(list)
    for kod in kosul_kodlari:
        aile_kodlari[SOMUT_KOSULLAR[kod].iddia_ailesi].append(kod)
    yayin = aliased(YayinKaydi, name="claim_yayini")
    satirlar = oturum.execute(
        select(Iddia, IddiaSurumu, yayin)
        .join(IddiaSurumu, and_(IddiaSurumu.iddia_id == Iddia.id, IddiaSurumu.surum_no == Iddia.aktif_surum_no))
        .outerjoin(yayin, and_(yayin.nesne_turu == "claim", yayin.nesne_id == Iddia.id))
        .where(Iddia.sube_id.in_(sube_idleri), Iddia.aile.in_(aile_kodlari))
    ).all()
    gecici: dict[tuple[str, str], set[KosulDurumu]] = defaultdict(set)
    for satir in satirlar:
        iddia, surum, yayin_kaydi = satir.Iddia, satir.IddiaSurumu, satir.claim_yayini
        kullanilabilir = (
            surum.bilgi_durumu == BilgiDurumu.BILINIYOR.value
            and yayin_kaydi_kamusal_mi(yayin_kaydi, KullanimTuru.KARAR)
        )
        for kod in aile_kodlari[iddia.aile]:
            gecici[(str(iddia.sube_id), kod)].add(
                kosul_durumu(SOMUT_KOSULLAR[kod], surum.deger, kullanilabilir=kullanilabilir)
            )
    for (sube_id, kod), durumlar in gecici.items():
        bilinen = durumlar - {KosulDurumu.DEGERLENDIRILEMIYOR}
        if len(bilinen) == 1:
            sonuc[sube_id][kod] = next(iter(bilinen))
        elif len(bilinen) > 1:
            sonuc[sube_id][kod] = KosulDurumu.DEGERLENDIRILEMIYOR
    return sonuc


def filtre_katalogunu_getir(oturum: Session, sehir_degeri: str | None) -> AramaFiltreleriCevabi:
    sehir = _sehir_coz(oturum, sehir_degeri)
    yer_yayini = aliased(YayinKaydi, name="filtre_yer_yayini")
    ilceler = oturum.scalars(
        select(Ilce)
        .join(Yer, Yer.ilce_id == Ilce.id)
        .join(yer_yayini, and_(yer_yayini.nesne_turu == "yer", yer_yayini.nesne_id == Yer.id))
        .where(
            Ilce.sehir_id == sehir.id,
            Ilce.aktif_mi.is_(True),
            yer_yayini.aktif_mi.is_(True),
            yer_yayini.durum.in_(KAMUSAL_DURUMLAR),
            yer_yayini.izinli_kullanimlar.contains([KullanimTuru.KESFET.value]),
        )
        .distinct()
        .order_by(Ilce.isim)
    ).all()
    yayin = aliased(YayinKaydi, name="claim_yayini")
    mevcut_aileler = set(
        oturum.scalars(
            select(Iddia.aile)
            .join(Sube, Sube.id == Iddia.sube_id)
            .join(IddiaSurumu, and_(IddiaSurumu.iddia_id == Iddia.id, IddiaSurumu.surum_no == Iddia.aktif_surum_no))
            .join(yayin, and_(yayin.nesne_turu == "claim", yayin.nesne_id == Iddia.id))
            .join(YerKimligi, YerKimligi.id == Sube.yer_kimligi_id)
            .where(
                YerKimligi.sehir_id == sehir.id,
                IddiaSurumu.bilgi_durumu == BilgiDurumu.BILINIYOR.value,
                yayin.aktif_mi.is_(True),
                yayin.durum.in_(KAMUSAL_DURUMLAR),
                yayin.izinli_kullanimlar.contains([KullanimTuru.KARAR.value]),
            )
            .distinct()
        ).all()
    )
    kosullar = [
        FiltreSecenegiSemasi(kod=tanim.kod, etiket=tanim.etiket, iddia_ailesi=tanim.iddia_ailesi)
        for tanim in SOMUT_KOSULLAR.values()
        if tanim.iddia_ailesi in mevcut_aileler
    ]
    return AramaFiltreleriCevabi(
        sehir_id=str(sehir.id),
        sehir_anahtari=_sehir_anahtari(sehir),
        ilceler=[IlceSecenegiSemasi(id=str(ilce.id), isim=ilce.isim, sehir_id=str(sehir.id)) for ilce in ilceler],
        turler=[TurSecenegiSemasi(kod=kod, etiket=_etiket(kod)) for kod in TUR_KODLARI],
        somut_kosullar=kosullar,
    )


def ara(
    oturum: Session,
    *,
    q: str,
    sehir_degeri: str | None,
    ilce_id: str | None,
    tur: str | None,
    zorunlu_kosullar: list[str],
    tercihler: list[str],
    limit: int,
    cursor: str | None,
) -> AramaCevabi:
    normalize_q = turkce_arama_normalize(q)
    if not normalize_q:
        raise ValueError("Arama sorgusu bos olamaz.")
    bilinmeyen_kosullar = (set(zorunlu_kosullar) | set(tercihler)) - set(SOMUT_KOSULLAR)
    if bilinmeyen_kosullar:
        raise ValueError(f"Desteklenmeyen somut kosul: {sorted(bilinmeyen_kosullar)[0]}")
    if tur is not None and tur not in TUR_KODLARI:
        raise ValueError("Desteklenmeyen mekan turu.")

    sehir = _sehir_coz(oturum, sehir_degeri)
    ilce = _ilce_coz(oturum, ilce_id, sehir)
    tum_ilceler = oturum.scalars(
        select(Ilce).where(Ilce.sehir_id == sehir.id, Ilce.aktif_mi.is_(True)).order_by(Ilce.isim)
    ).all()
    sorgu_ilcesi = next((x for x in tum_ilceler if x.arama_isim and x.arama_isim in normalize_q.split("  ")), None)
    # Cok kelimeli ilceler dahil, yalniz tam token sinirinda bul.
    if sorgu_ilcesi is None:
        sorgu_ilcesi = next(
            (x for x in sorted(tum_ilceler, key=lambda d: len(d.arama_isim), reverse=True)
             if baglam_tokenini_cikar(normalize_q, x.arama_isim) != normalize_q),
            None,
        )
    if ilce is None and sorgu_ilcesi is not None:
        ilce = sorgu_ilcesi

    ad_sorgusu = baglam_tokenini_cikar(normalize_q, sehir.arama_isim)
    if ilce is not None:
        ad_sorgusu = baglam_tokenini_cikar(ad_sorgusu, ilce.arama_isim)
    sorgu_turu = TUR_ESLESMELERI.get(normalize_q)
    etkin_tur = tur or sorgu_turu
    if sorgu_turu:
        ad_sorgusu = ""

    yer_yayini = aliased(YayinKaydi, name="yer_yayini")
    benzerlik = func.similarity(Yer.arama_isim, ad_sorgusu) if ad_sorgusu else func.cast(0, Float)
    sorgu = (
        select(Yer, Sehir, Sube, YerKimligi, Ilce, yer_yayini, benzerlik.label("benzerlik"))
        .join(Sehir, Sehir.id == Yer.sehir_id)
        .join(Sube, Sube.legacy_yer_id == Yer.id)
        .join(YerKimligi, YerKimligi.id == Sube.yer_kimligi_id)
        .outerjoin(Ilce, Ilce.id == Yer.ilce_id)
        .outerjoin(yer_yayini, and_(yer_yayini.nesne_turu == "yer", yer_yayini.nesne_id == Yer.id))
        .where(
            Yer.sehir_id == sehir.id,
            Sube.durum == "aktif",
            Sube.yonlendirilen_sube_id.is_(None),
            YerKimligi.durum == "aktif",
            *_kamusal_kosullar(yer_yayini, KullanimTuru.ARAMA),
        )
    )
    if ilce is not None:
        sorgu = sorgu.where(Yer.ilce_id == ilce.id)
    if etkin_tur:
        if etkin_tur in {uye.value for uye in AnaKategori}:
            sorgu = sorgu.where(Yer.ana_kategori == etkin_tur)
        else:
            sorgu = sorgu.where(Yer.alt_kategori == etkin_tur)
    if ad_sorgusu:
        metin_kosullari = [Yer.arama_isim == ad_sorgusu, Yer.arama_isim.startswith(ad_sorgusu)]
        if len(ad_sorgusu) >= 3:
            # pg_trgm varsayilan 0.3 esigi; `%` operatoru GIN trigram indeksini kullanabilir.
            metin_kosullari.append(Yer.arama_isim.op("%") (ad_sorgusu))
        sorgu = sorgu.where(or_(*metin_kosullari))

    if oturum.info.get("faz25_trace") is not None:
        iz_guncelle(oturum, search_candidate_count=oturum.scalar(
            sorgu.with_only_columns(func.count(func.distinct(Yer.id)))
        ))
    if ilce is not None:
        sorgu = sorgu.where(Yer.ilce_id == ilce.id)
    if oturum.info.get("faz25_trace") is not None:
        iz_guncelle(oturum, geographic_filtered_count=oturum.scalar(
            sorgu.with_only_columns(func.count(func.distinct(Yer.id)))
        ))
    sorgu = sorgu.where(*_kamusal_kosullar(yer_yayini, KullanimTuru.ARAMA))
    satirlar = oturum.execute(sorgu).all()
    iz_guncelle(oturum, publication_eligible_count=len(satirlar))
    kosul_kodlari = list(dict.fromkeys([*zorunlu_kosullar, *tercihler]))
    durumlar = _claim_durumlari(oturum, [str(s.Sube.id) for s in satirlar], kosul_kodlari)
    adaylar: list[_Aday] = []
    degerlendirilemeyen = 0
    for satir in satirlar:
        yer, sube = satir.Yer, satir.Sube
        aday_durumlari = durumlar[str(sube.id)]
        hard = [aday_durumlari[kod] for kod in zorunlu_kosullar]
        if any(durum is KosulDurumu.DEGERLENDIRILEMIYOR for durum in hard):
            degerlendirilemeyen += 1
            iz_artir(oturum, "unknown_critical_count")
            continue
        if any(durum is KosulDurumu.UYGUN_DEGIL for durum in hard):
            iz_artir(oturum, "hard_constraint_rejected_count")
            continue
        if not ad_sorgusu:
            sonuc_turu, neden = AramaSonucuTuru.BAGLAMSAL_ADAY, EslesmeNedeni.BAGLAM
        elif yer.arama_isim == ad_sorgusu:
            sonuc_turu, neden = AramaSonucuTuru.YER_KIMLIGI, EslesmeNedeni.TAM_AD
        elif yer.arama_isim.startswith(ad_sorgusu):
            sonuc_turu, neden = AramaSonucuTuru.YER_KIMLIGI, EslesmeNedeni.AD_BASLANGICI
        else:
            sonuc_turu, neden = AramaSonucuTuru.BAGLAMSAL_ADAY, EslesmeNedeni.YAZIM_YAKINLIGI
        tercih_puani = sum(1 for kod in tercihler if aday_durumlari[kod] is KosulDurumu.UYGUN)
        olumsuz_tercih = sum(1 for kod in tercihler if aday_durumlari[kod] is KosulDurumu.UYGUN_DEGIL)
        adaylar.append(
            _Aday(yer, satir.Sehir, sube, satir.YerKimligi, satir.Ilce, float(satir.benzerlik or 0),
                  sonuc_turu, neden, aday_durumlari, tercih_puani, olumsuz_tercih)
        )
    tur_sirasi = {AramaSonucuTuru.YER_KIMLIGI: 0, AramaSonucuTuru.BAGLAMSAL_ADAY: 1}
    adaylar.sort(key=lambda a: (
        -a.tercih_puani, a.olumsuz_tercih, tur_sirasi[a.sonuc_turu], -a.benzerlik,
        a.yer.arama_isim, str(a.yer.id),
    ))

    cografya = AramaCografyaSemasi(
        sehir_id=str(sehir.id), sehir_anahtari=_sehir_anahtari(sehir), sehir_ismi=sehir.isim,
        ilce_id=str(ilce.id) if ilce else None, ilce_ismi=ilce.isim if ilce else None,
    )
    semantik: list[AramaSonucuSemasi] = []
    if normalize_q == sehir.arama_isim:
        semantik.append(AramaSonucuSemasi(sonuc_turu=AramaSonucuTuru.SEHIR, etiket=sehir.isim, cografya=cografya, eslesme_nedeni=EslesmeNedeni.SEHIR))
    if sorgu_ilcesi is not None and normalize_q == sorgu_ilcesi.arama_isim:
        semantik.append(AramaSonucuSemasi(sonuc_turu=AramaSonucuTuru.ILCE, etiket=sorgu_ilcesi.isim, cografya=cografya, eslesme_nedeni=EslesmeNedeni.ILCE))
    if sorgu_turu:
        semantik.append(AramaSonucuSemasi(sonuc_turu=AramaSonucuTuru.KATEGORI, etiket=_etiket(sorgu_turu), cografya=cografya, ana_kategori=sorgu_turu if sorgu_turu in {x.value for x in AnaKategori} else None, alt_kategori=None if sorgu_turu in {x.value for x in AnaKategori} else sorgu_turu, eslesme_nedeni=EslesmeNedeni.KATEGORI))
    sonuclar = semantik + [
        AramaSonucuSemasi(
            sonuc_turu=a.sonuc_turu, etiket=a.yer.isim,
            yer=AramaYerKimligiSemasi(place_id=str(a.yer.id), canonical_id=str(a.kimlik.id), branch_id=str(a.sube.id), isim=a.yer.isim),
            cografya=AramaCografyaSemasi(sehir_id=str(a.sehir.id), sehir_anahtari=_sehir_anahtari(a.sehir), sehir_ismi=a.sehir.isim, ilce_id=str(a.ilce.id) if a.ilce else None, ilce_ismi=a.ilce.isim if a.ilce else None),
            ana_kategori=a.yer.ana_kategori, alt_kategori=a.yer.alt_kategori,
            eslesme_nedeni=a.neden, kosul_durumlari=a.kosul_durumlari,
        ) for a in adaylar
    ]

    imza_ham = json.dumps({"q": normalize_q, "s": str(sehir.id), "i": str(ilce.id) if ilce else None, "t": etkin_tur, "z": sorted(zorunlu_kosullar), "p": sorted(tercihler)}, sort_keys=True)
    imza = hashlib.sha256(imza_ham.encode()).hexdigest()[:16]
    offset = _cursor_coz(cursor, imza)
    sayfa = sonuclar[offset : offset + limit]
    sonraki = _cursor_uret(offset + limit, imza) if offset + limit < len(sonuclar) else None
    filtreler = AramaFiltreBaglamiSemasi(
        sehir_id=str(sehir.id), ilce_id=str(ilce.id) if ilce else None, tur=etkin_tur,
        cografi_baglam=CografiBaglamSemasi(sehir=sehir.isim, ilce=ilce.isim if ilce else None),
        zorunlu_kosullar=[ZorunluKosulSemasi(**SOMUT_KOSULLAR[kod].zorunlu_kosul().__dict__) for kod in zorunlu_kosullar],
        tercihler=[TercihSemasi(**SOMUT_KOSULLAR[kod].tercih().__dict__) for kod in tercihler],
    )
    return AramaCevabi(sorgu=q, sonuclar=sayfa, uygulanan_filtreler=filtreler, sonraki_cursor=sonraki, degerlendirilemeyen_aday_sayisi=degerlendirilemeyen)
