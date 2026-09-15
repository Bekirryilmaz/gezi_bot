"""Internal branch/family evidence summaries. This module cannot publish claims."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime

from ortak.sabitler import KARAR_DISI_DAHILI_SINYAL_AILELERI

AGREGASYON_SURUMU = "faz25.2-agg-v1"


@dataclass(frozen=True)
class SignalObservation:
    branch_id: str
    family: str
    evidence_id: str
    source: str
    direction: str
    observed_at: datetime | None
    valid_until: datetime | None
    branch_confidence: str
    rights_status: str
    verified: bool = False
    observation_id: str | None = None
    epistemic_type: str | None = None
    review_id: str | None = None
    kullanim_durumu: str = "aktif"


def _yorum_kimligi(row: SignalObservation) -> str:
    return row.review_id or row.observation_id or row.evidence_id


def aggregate(observations: list[SignalObservation], *, now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(UTC)
    groups = defaultdict(list)
    for observation in observations:
        if observation.direction not in {"support", "counter"}:
            raise ValueError("Observation direction must be explicit")
        if observation.kullanim_durumu != "aktif":
            continue
        if observation.family in KARAR_DISI_DAHILI_SINYAL_AILELERI:
            continue
        if observation.epistemic_type == "sentiment_signal":
            continue
        groups[(observation.branch_id, observation.family)].append(observation)
    results = []
    for (branch, family), rows in sorted(groups.items()):
        evidence = {}
        for row in rows:
            # One source item can have multiple extraction spans. Count it once per direction.
            evidence[(row.source, row.observation_id or row.evidence_id, row.direction)] = row
        unique = list(evidence.values())
        support = sum(r.direction == "support" for r in unique)
        counter = sum(r.direction == "counter" for r in unique)
        dates = [r.observed_at for r in unique if r.observed_at is not None]
        rights = "allowed" if all(r.rights_status == "allowed" for r in rows) else "blocked"
        freshness = (
            "unknown"
            if any(r.observed_at is None or r.valid_until is None for r in unique)
            else "stale"
            if any(r.valid_until <= now for r in unique)
            else "current"
        )
        yorum_yonleri: dict[tuple[str, str], set[str]] = defaultdict(set)
        for row in unique:
            yorum_yonleri[(_yorum_kimligi(row), row.direction)].add(row.epistemic_type or "")
        fact_support = sum(
            "fact_signal" in turler
            for (yorum, yon), turler in yorum_yonleri.items()
            if yon == "support"
        )
        experience_counter = sum(
            "experience_signal" in turler
            for (yorum, yon), turler in yorum_yonleri.items()
            if yon == "counter"
        )
        experience_support = sum(
            "experience_signal" in turler
            for (yorum, yon), turler in yorum_yonleri.items()
            if yon == "support"
        )
        fact_counter = sum(
            "fact_signal" in turler
            for (yorum, yon), turler in yorum_yonleri.items()
            if yon == "counter"
        )
        results.append(
            {
                "branch_id": branch,
                "family": family,
                "supporting_observation_count": support,
                "counter_observation_count": counter,
                "unique_evidence_count": len({(r.source, r.evidence_id) for r in unique}),
                "unique_review_count": len({_yorum_kimligi(r) for r in unique}),
                "fact_support_count": fact_support,
                "fact_counter_count": fact_counter,
                "experience_support_count": experience_support,
                "experience_counter_count": experience_counter,
                "source_diversity": len({r.source for r in unique}),
                "date_range": [min(dates).isoformat(), max(dates).isoformat()] if dates else None,
                "freshness": freshness,
                "temporal_unknown": any(r.observed_at is None for r in unique),
                "conflict_level": "conflicting" if support and counter else "none",
                "counter_share": counter / (support + counter),
                "branch_confidence": "verified"
                if all(r.branch_confidence == "verified" for r in rows)
                else "unknown",
                "rights_status": rights,
                "verified_evidence_count": sum(r.verified for r in unique),
                "guven_sinifi": "kalibre_edilmedi",
                "durum": "karar_disi",
                "agregasyon_surumu": AGREGASYON_SURUMU,
                "kirilim": {
                    "source_diversity": len({r.source for r in unique}),
                    "temporal_unknown": any(r.observed_at is None for r in unique),
                    "karantina_haric": True,
                    "genel_duygu_haric": True,
                },
            }
        )
    return results


def promotion_gate(signal: dict, *, risk: str) -> dict:
    """Fail closed. Passing means admin review eligible, never public eligible.

    The current real evidence distribution is single-source/unverified. There is
    no calibrated count threshold or subjective auto-promotion in this release.
    A factual observation must have explicit human branch and validity verification.
    """
    reasons = []
    if signal["rights_status"] != "allowed":
        reasons.append("rights_blocked")
    if signal["branch_confidence"] != "verified":
        reasons.append("branch_unverified")
    if signal["freshness"] != "current":
        reasons.append("freshness_unverified")
    if signal["conflict_level"] == "conflicting":
        reasons.append("counter_evidence_review")
    if not signal["supporting_observation_count"]:
        reasons.append("no_support")
    if not signal["verified_evidence_count"]:
        reasons.append("no_verified_evidence")
    if risk != "factual":
        reasons.append("subjective_gate_uncalibrated")
    return {
        "admin_review_eligible": not reasons,
        "reasons": reasons,
        "automatic_publication": False,
    }


def guven_sinifini_uygula(signal: dict, esikler: dict[str, int]) -> dict:
    """Dagilimdan uretilen esikleri uygular; zayif sinyali karar disinda tutar."""
    unique_review = int(signal.get("unique_review_count") or 0)
    zayif_max = int(esikler["zayif_max_unique_review"])
    orta_max = int(esikler["orta_max_unique_review"])
    if unique_review <= zayif_max:
        sinif = "zayif"
    elif unique_review <= orta_max:
        sinif = "orta"
    else:
        sinif = "guclu"
    karar_hazir = (
        sinif in {"orta", "guclu"}
        and signal.get("conflict_level") == "none"
        and signal.get("branch_confidence") == "verified"
        and signal.get("rights_status") == "allowed"
        and int(signal.get("supporting_observation_count") or 0) > 0
    )
    guncel = dict(signal)
    guncel["guven_sinifi"] = sinif
    guncel["durum"] = "aktif" if karar_hazir else "karar_disi"
    guncel["kirilim"] = {
        **dict(signal.get("kirilim") or {}),
        "kalibrasyon": {
            "zayif_max_unique_review": zayif_max,
            "orta_max_unique_review": orta_max,
            "unique_review_count": unique_review,
        },
    }
    return guncel


def dahili_tercih_kapisi(signal: dict) -> dict:
    """Dahili aggregate yalniz kalibre orta/guclu destekte tercih kaniti olabilir."""
    reasons = []
    if signal.get("guven_sinifi") in {None, "kalibre_edilmedi", "zayif"}:
        reasons.append("weak_or_uncalibrated")
    if signal.get("durum") != "aktif":
        reasons.append("not_decision_ready")
    if signal.get("conflict_level") == "conflicting":
        reasons.append("conflicting")
    if not signal.get("supporting_observation_count"):
        reasons.append("no_support")
    return {
        "preference_eligible": not reasons,
        "reasons": reasons,
        "hard_constraint_eligible": False,
        "automatic_publication": False,
    }
