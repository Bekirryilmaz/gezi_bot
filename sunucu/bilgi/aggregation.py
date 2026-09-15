"""Internal branch/family evidence summaries. This module cannot publish claims."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime


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


def aggregate(observations: list[SignalObservation], *, now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(UTC)
    groups = defaultdict(list)
    for observation in observations:
        if observation.direction not in {"support", "counter"}:
            raise ValueError("Observation direction must be explicit")
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
        results.append(
            {
                "branch_id": branch,
                "family": family,
                "supporting_observation_count": support,
                "counter_observation_count": counter,
                "unique_evidence_count": len({(r.source, r.evidence_id) for r in unique}),
                "source_diversity": len({r.source for r in unique}),
                "date_range": [min(dates).isoformat(), max(dates).isoformat()] if dates else None,
                "freshness": freshness,
                "conflict_level": "conflicting" if support and counter else "none",
                "counter_share": counter / (support + counter),
                "branch_confidence": "verified"
                if all(r.branch_confidence == "verified" for r in rows)
                else "unknown",
                "rights_status": rights,
                "verified_evidence_count": sum(r.verified for r in unique),
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
