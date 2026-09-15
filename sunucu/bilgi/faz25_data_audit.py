import json
import os
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import select, text
from sqlalchemy.engine import make_url

from sunucu.bilgi.aggregation import SignalObservation, aggregate, promotion_gate
from sunucu.bilgi.pilot_claimleri import kaynak_haklari_uygun_mu
from sunucu.veritabani.baglanti import VERITABANI_URL, OturumUretici
from sunucu.veritabani.bilgi_modelleri import (
    Gozlem,
    Iddia,
    IddiaSurumu,
    KanitBaglantisi,
    KaynakPolitikasi,
)
from sunucu.veritabani.kimlik_modelleri import Sube
from sunucu.veritabani.yayin_modelleri import YayinKaydi
from sunucu.yayin.domain import KullanimTuru
from sunucu.yayin.servis import yayin_kaydi_kamusal_mi

if os.environ.get("UYGULAMA_ORTAMI", "development").lower() not in {
    "development",
    "dev",
    "test",
    "testing",
} or make_url(VERITABANI_URL).host not in {"localhost", "127.0.0.1"}:
    raise RuntimeError("FAZ25 audit is restricted to local development/test DB")
now = datetime.now(UTC)
families = [
    "amac_destegi",
    "wifi",
    "otopark",
    "sessiz_ortam",
    "sohbet_uygunlugu",
    "aile_uygunlugu",
    "cocuk_uygunlugu",
    "calisma_uygunlugu",
    "manzara",
    "uygun_fiyat",
    "fiyat",
    "calisma_saati",
    "acik_alan",
    "acik_hava",
    "canli_muzik",
    "tekerlekli_sandalye_erisimi",
    "ziyaret_suresi",
    "ulasim",
]
with OturumUretici() as s:
    total = s.execute(text("select count(*) from yerler")).scalar_one()
    policies = {p.kaynak: p for p in s.scalars(select(KaynakPolitikasi))}
    publications = {
        str(p.nesne_id): p
        for p in s.scalars(select(YayinKaydi).where(YayinKaydi.nesne_turu == "claim"))
    }
    rows = s.execute(
        select(Iddia, IddiaSurumu, Sube)
        .join(IddiaSurumu, IddiaSurumu.iddia_id == Iddia.id)
        .join(Sube, Sube.id == Iddia.sube_id)
    ).all()
    usable = defaultdict(dict)
    pending = defaultdict(set)
    stale = defaultdict(set)
    conflict = defaultdict(set)
    for claim, v, branch in rows:
        place = str(branch.legacy_yer_id)
        if v.yayin_durumu == "inceleme_bekliyor":
            pending[claim.aile].add(place)
        if v.bilgi_durumu == "eskimis" or (v.gecerlilik_bitisi and v.gecerlilik_bitisi <= now):
            stale[claim.aile].add(place)
        if v.bilgi_durumu == "celiskili":
            conflict[claim.aile].add(place)
        if v.surum_no != claim.aktif_surum_no:
            continue
        if v.bilgi_durumu != "biliniyor" or not yayin_kaydi_kamusal_mi(
            publications.get(str(claim.id)), KullanimTuru.KARAR
        ):
            continue
        if v.gecerlilik_bitisi and v.gecerlilik_bitisi <= now:
            continue
        usable[claim.aile][place] = v.deger.get("deger")
    coverage = []
    for family in families:
        values = usable[family]
        false = sum(v is False for v in values.values())
        true = len(values) - false
        coverage.append(
            {
                "family": family,
                "known_true_or_value": true,
                "known_false": false,
                "unknown": total - true - false,
                "stale": len(stale[family]),
                "conflicting": len(conflict[family]),
                "review_pending": len(pending[family]),
            }
        )
    purposes = []
    for purpose in [
        "kahve_icmek",
        "yemek_yemek",
        "tarihi_kulturel_ziyaret",
        "tatli_yemek",
        "kahvalti_yapmak",
        "eglence",
        "calisma",
        "birlikte_vakit",
        "cocukla_aktivite",
    ]:
        known = sum(isinstance(v, list) and purpose in v for v in usable["amac_destegi"].values())
        purposes.append(
            {"purpose": purpose, "known_support": known, "unknown": total - known, "known_false": 0}
        )
    signals = []
    evidence = s.execute(
        select(Iddia, IddiaSurumu, KanitBaglantisi, Gozlem)
        .join(IddiaSurumu, IddiaSurumu.iddia_id == Iddia.id)
        .join(KanitBaglantisi, KanitBaglantisi.iddia_surumu_id == IddiaSurumu.id)
        .join(Gozlem, Gozlem.id == KanitBaglantisi.gozlem_id)
    ).all()
    roles = Counter()
    for claim, v, link, o in evidence:
        roles[link.rol] += 1
        if link.rol not in {"destek", "karsi", "destekleyen", "curuten", "supporting", "counter"}:
            continue
        allowed = kaynak_haklari_uygun_mu(policies.get(o.kaynak), simdi=now)[0]
        if not allowed:
            continue
        signals.append(
            SignalObservation(
                str(claim.sube_id),
                claim.aile,
                o.kaynak_kayit_id,
                o.kaynak,
                "counter" if link.rol in {"karsi", "curuten", "counter"} else "support",
                o.olay_zamani or o.kaynakta_gozlemlenme_zamani,
                v.gecerlilik_bitisi,
                "unknown",  # Content verification alone is not branch identity verification.
                "allowed",
                bool(o.dogrulanma_zamani),
                observation_id=str(o.id),
            )
        )
    aggregates = aggregate(signals, now=now)
    for a in aggregates:
        a["promotion_gate"] = promotion_gate(
            a,
            risk="factual"
            if a["family"] in {"yer_turu", "adres", "web_sitesi", "telefon", "wifi", "otopark"}
            else "subjective",
        )
    counts = dict(
        s.execute(
            text(
                "select (select count(*) from gozlemler) observation_count,(select "
                "count(*) from iddialar) claim_candidate_count,(select count(*) from "
                "iddia_surumleri where yayin_durumu='inceleme_bekliyor') "
                "pending_count,(select count(distinct sube_id) from iddialar i join "
                "iddia_surumleri v on v.iddia_id=i.id where "
                "v.yayin_durumu='inceleme_bekliyor') review_ready_branches,(select "
                "count(*) from iddia_surumleri where yayin_durumu in "
                "('yayinlandi','sinirli')) public_claim_count"
            )
        )
        .mappings()
        .one()
    )
    district = dict(
        s.execute(
            text(
                "select count(*) total,count(ilce_id) canonical,count(ilce) "
                "text,count(konum) coordinates from yerler"
            )
        )
        .mappings()
        .one()
    )
    result = {
        "counts": counts,
        "family_coverage": coverage,
        "purpose_coverage": purposes,
        "coverage_denominator": total,
        "coverage_note": (
            "unknown includes pending/stale/conflicting; these are diagnostic overlays, "
            "not extra partition categories. Purpose lists are not closed-world false evidence."
        ),
        "aggregate_signals": aggregates,
        "aggregate_distribution": {
            "groups": len(aggregates),
            "source_diversity": dict(Counter(a["source_diversity"] for a in aggregates)),
            "supporting_count": dict(
                Counter(a["supporting_observation_count"] for a in aggregates)
            ),
            "promotion_reasons": dict(
                Counter(r for a in aggregates for r in a["promotion_gate"]["reasons"])
            ),
            "eligible": sum(a["promotion_gate"]["admin_review_eligible"] for a in aggregates),
            "evidence_roles": dict(roles),
        },
        "review_rights": {
            "source": "google_maps",
            "reviews": 19609,
            "policy_present": "google_maps" in policies,
            "processing_run": False,
            "blocked_before_model": True,
            "new_aday_gozlem": 0,
            "new_claim_candidate": 0,
        },
        "canonical_district": district,
    }
Path("veri/cikti/raporlar/faz25_1_data_coverage_aggregation.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
)
print(
    json.dumps(
        {k: v for k, v in result.items() if k != "aggregate_signals"},
        ensure_ascii=False,
        default=str,
    )
)
