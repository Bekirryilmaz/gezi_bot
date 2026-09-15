"""Intent korpusunu development DB uzerinde calistirip ayrintili trace uretir."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select

from sunucu.arama.normalizasyon import turkce_arama_normalize
from sunucu.bugun_ne_yapalim.intent import metni_coz
from sunucu.bugun_ne_yapalim.semalar import BugunNeYapalimTalebi
from sunucu.bugun_ne_yapalim.servis import bugun_ne_yapalim
from sunucu.veritabani.baglanti import OturumUretici
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu

KORPUS = Path(__file__).parent / "testler" / "intent_korpusu.json"


def _uyuyor_mu(cozum: dict[str, object], beklenen: dict[str, object]) -> bool:
    for alan in ("kisi_baglami", "ana_amac"):
        if alan in beklenen and cozum.get(alan) != beklenen[alan]:
            return False
    for beklenen_alan, gercek_alan in (
        ("aktiviteler_icerir", "aktiviteler"),
        ("alt_amaclar_icerir", "alt_amaclar"),
        ("zorunlu_icerir", "zorunlu_kosullar"),
        ("tercihler_icerir", "tercihler"),
    ):
        if not set(beklenen.get(beklenen_alan, [])).issubset(set(cozum.get(gercek_alan, []))):
            return False
    return True


def raporla(ilk: int | None = None) -> dict[str, Any]:
    korpus = json.loads(KORPUS.read_text(encoding="utf-8"))
    if ilk is not None:
        korpus = korpus[:ilk]
    izler: list[dict[str, Any]] = []
    dagilim: Counter[str] = Counter()
    parse_dagilimi: Counter[str] = Counter()
    urun_dagilimi: Counter[str] = Counter()
    with OturumUretici() as oturum:
        yayinli = oturum.execute(
            select(Iddia.aile, Iddia.sube_id)
            .join(IddiaSurumu, IddiaSurumu.iddia_id == Iddia.id)
            .where(IddiaSurumu.yayin_durumu.in_(("yayinlandi", "sinirli")))
        ).all()
        for sira, ornek in enumerate(korpus, 1):
            cozum = metni_coz(ornek["input"])
            dogru = _uyuyor_mu(cozum, ornek["beklenen"])
            try:
                cevap = bugun_ne_yapalim(
                    oturum,
                    BugunNeYapalimTalebi(serbest_metin=ornek["input"]),
                    request_id=f"intent-corpus-{sira}",
                )
                durum = cevap.durum
                search_aday = (
                    len(cevap.kesfet.secenekler) + cevap.kesfet.degerlendirilemeyen_aday_sayisi
                    if cevap.kesfet
                    else 0
                )
                publication_sonrasi = len(cevap.kesfet.secenekler) if cevap.kesfet else 0
                karar = (
                    [x.karar_sonucu.karar_turu for x in cevap.kesfet.secenekler]
                    if cevap.kesfet
                    else []
                )
                gerekce_kodlari = []
                secili_yerler: list[str] = []
                if cevap.kesfet:
                    secili_yerler = [secenek.yer.isim for secenek in cevap.kesfet.secenekler]
                    for secenek in cevap.kesfet.secenekler:
                        gerekce_kodlari.extend(g.kod for g in secenek.karar_sonucu.gerekceler)
                fact_destek = any(
                    kod in {"amac_destekleniyor", "zorunlu_kosul_dogrulandi", "tercih_destekleniyor"}
                    for kod in gerekce_kodlari
                )
                experience_destek = "deneyim_sinyali_destekliyor" in gerekce_kodlari
                unknown = bool(
                    cevap.kesfet
                    and any(
                        secenek.karar_sonucu.bilinmeyenler or secenek.karar_sonucu.kritik_engeller
                        for secenek in cevap.kesfet.secenekler
                    )
                )
                mesaj = cevap.durum_aciklamasi
                anlasilan = cevap.anlasilan_ihtiyac.model_dump(mode="json")
                karar_baglami = cevap.baglam.model_dump(mode="json")
                norm_isimler = [turkce_arama_normalize(ad) for ad in secili_yerler]
                duplicate_oneri = len(norm_isimler) - len(set(norm_isimler))
                kirli_isim = any(
                    len((ad or "").strip()) < 2 or not any(karakter.isalpha() for karakter in ad)
                    for ad in secili_yerler
                )
            except Exception as hata:  # rapor teknik hatayi da ayri siniflar
                durum, search_aday, publication_sonrasi, karar = "technical", 0, 0, []
                mesaj = f"{type(hata).__name__}: {hata}"
                anlasilan = {}
                karar_baglami = {}
                fact_destek = False
                experience_destek = False
                unknown = False
                secili_yerler = []
                duplicate_oneri = 0
                kirli_isim = False
            if not dogru:
                sinif = "intent_parser"
                sonuc = "yanlis"
            elif durum == "clarification":
                sinif = "expected_insufficient"
                sonuc = "netlestirme"
            elif durum == "technical":
                sinif = "technical"
                sonuc = "yanlis"
            elif durum == "insufficient":
                sinif = (
                    "claim_family_missing" if cozum["desteklenmeyen_istekler"] else "data_coverage"
                )
                sonuc = "kabul_edilebilir"
            else:
                sinif = "expected_insufficient" if cozum["desteklenmeyen_istekler"] else "taxonomy"
                sonuc = "dogru"
            dagilim[sonuc] += 1
            parse_sinifi = "beklenen_alanlarla_uyumlu" if dogru else "beklenen_alanlarla_uyumsuz"
            parse_dagilimi[parse_sinifi] += 1
            urun_dagilimi[durum] += 1
            izler.append(
                {
                    "sira": sira,
                    **cozum,
                    "sehir": anlasilan.get("sehir"),
                    "ilce": anlasilan.get("ilce"),
                    "zaman": anlasilan.get("zaman"),
                    "sure": karar_baglami.get("sure_ust_siniri_dakika"),
                    "ulasim": anlasilan.get("ulasim"),
                    "butce": anlasilan.get("butce_ust_siniri"),
                    "hard_constraint": anlasilan.get("zorunlu_kosullar", []),
                    "preference": anlasilan.get("tercihler", []),
                    "netlestirme_gerekiyor": durum == "clarification",
                    "karar_baglami": karar_baglami,
                    "full_trace": dict(oturum.info.get("faz25_trace", {})),
                    "search_aday_sayisi": oturum.info.get("faz25_trace", {}).get(
                        "search_candidate_count"
                    ),
                    "publication_sonrasi_aday_sayisi": oturum.info.get("faz25_trace", {}).get(
                        "publication_eligible_count"
                    ),
                    "secili_sonuc_sayisi": publication_sonrasi,
                    "secili_ve_degerlendirilemeyen_toplami": search_aday,
                    "aday_olcum_siniri": "Sifir erken cikista calistirilmayan asamayi ifade eder.",
                    "decision_sonucu": karar,
                    "secili_yerler": secili_yerler,
                    "fact_destek": fact_destek,
                    "experience_destek": experience_destek,
                    "unknown": unknown,
                    "duplicate_oneri": duplicate_oneri,
                    "kirli_isim": kirli_isim,
                    "kullanici_state": durum,
                    "kullanici_mesaji": mesaj,
                    "sonuc_dogru_mu": dogru,
                    "sorun_sinifi": sinif,
                }
            )
    fact_destek_sayisi = sum(1 for iz in izler if iz.get("fact_destek"))
    experience_destek_sayisi = sum(1 for iz in izler if iz.get("experience_destek"))
    unknown_sayisi = sum(1 for iz in izler if iz.get("unknown"))
    return {
        "uretilme_zamani": datetime.now().astimezone().isoformat(),
        "toplam": len(korpus),
        "dagilim": dict(dagilim),
        "dagilim_aciklamasi": (
            "Parse ve veri durumunu birlikte siniflar; saf intent basari olcumu degildir."
        ),
        "parse_beklenti_uyumu": dict(parse_dagilimi),
        "parse_olcum_siniri": (
            "Korpusun tanimli beklenen alanlari denetlenir; tam semantik dogruluk "
            "veya gercek kullanici basarisi iddiasi degildir."
        ),
        "urun_state_dagilimi": dict(urun_dagilimi),
        "fact_destek_sorgu": fact_destek_sayisi,
        "experience_destek_sorgu": experience_destek_sayisi,
        "unknown_sorgu": unknown_sayisi,
        "duplicate_oneri_toplam": sum(int(iz.get("duplicate_oneri") or 0) for iz in izler),
        "kirli_isim_sızıntı": sum(1 for iz in izler if iz.get("kirli_isim")),
        "benzersiz_onerilen_yer": len(
            {ad for iz in izler for ad in iz.get("secili_yerler") or []}
        ),
        "coverage_unknown_sorgu": sum(1 for iz in izler if iz["kullanici_state"] == "insufficient"),
        "published_claim": len(yayinli),
        "published_claimli_mekan": len({x.sube_id for x in yayinli}),
        "izler": izler,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cikti", type=Path)
    parser.add_argument("--ilk", type=int)
    args = parser.parse_args()
    rapor = raporla(ilk=args.ilk)
    metin = json.dumps(rapor, ensure_ascii=False, indent=2, default=str)
    if args.cikti:
        args.cikti.parent.mkdir(parents=True, exist_ok=True)
        args.cikti.write_text(metin + "\n", encoding="utf-8")
    print(
        json.dumps({k: v for k, v in rapor.items() if k != "izler"}, ensure_ascii=False, indent=2)
    )


if __name__ == "__main__":
    main()
