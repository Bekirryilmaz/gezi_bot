"""Intent korpusunu development DB uzerinde calistirip ayrintili trace uretir."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select

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


def raporla() -> dict[str, Any]:
    korpus = json.loads(KORPUS.read_text(encoding="utf-8"))
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
                mesaj = cevap.durum_aciklamasi
                anlasilan = cevap.anlasilan_ihtiyac.model_dump(mode="json")
                karar_baglami = cevap.baglam.model_dump(mode="json")
            except Exception as hata:  # rapor teknik hatayi da ayri siniflar
                durum, search_aday, publication_sonrasi, karar = "technical", 0, 0, []
                mesaj = f"{type(hata).__name__}: {hata}"
                anlasilan = {}
                karar_baglami = {}
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
                    "kullanici_state": durum,
                    "kullanici_mesaji": mesaj,
                    "sonuc_dogru_mu": dogru,
                    "sorun_sinifi": sinif,
                }
            )
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
        "published_claim": len(yayinli),
        "published_claimli_mekan": len({x.sube_id for x in yayinli}),
        "izler": izler,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cikti", type=Path)
    args = parser.parse_args()
    rapor = raporla()
    metin = json.dumps(rapor, ensure_ascii=False, indent=2, default=str)
    if args.cikti:
        args.cikti.parent.mkdir(parents=True, exist_ok=True)
        args.cikti.write_text(metin + "\n", encoding="utf-8")
    print(
        json.dumps({k: v for k, v in rapor.items() if k != "izler"}, ensure_ascii=False, indent=2)
    )


if __name__ == "__main__":
    main()
