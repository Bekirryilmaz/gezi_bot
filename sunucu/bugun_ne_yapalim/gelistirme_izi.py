"""Development/test stage counters; never part of a public response schema."""

from __future__ import annotations

import json
import logging
import os
from functools import wraps

logger = logging.getLogger("uvicorn.error")
COUNTERS = (
    "search_candidate_count",
    "geographic_filtered_count",
    "publication_eligible_count",
    "decision_evaluated_count",
    "hard_constraint_rejected_count",
    "unknown_critical_count",
    "selected_count",
)


def iz_guncelle(oturum, **alanlar):
    iz = oturum.info.get("faz25_trace")
    if iz is not None:
        iz.update(alanlar)


def iz_artir(oturum, alan, sayi=1):
    iz = oturum.info.get("faz25_trace")
    if iz is not None:
        iz[alan] += sayi


def gelistirme_izi(islev):
    @wraps(islev)
    def izle(oturum, talep, *, request_id, **kwargs):
        if os.environ.get("UYGULAMA_ORTAMI", "development").lower() not in {
            "development",
            "dev",
            "test",
            "testing",
        }:
            return islev(oturum, talep, request_id=request_id, **kwargs)
        iz = dict.fromkeys(COUNTERS, 0)
        iz.update(request_id=request_id, parsed_intent=None, final_state="unavailable")
        oturum.info["faz25_trace"] = iz
        try:
            cevap = islev(oturum, talep, request_id=request_id, **kwargs)
            iz["final_state"] = cevap.durum
            iz["selected_count"] = len(cevap.kesfet.secenekler) if cevap.kesfet else 0
            return cevap
        finally:
            # Structured intent only. No user text, coordinates, raw evidence, sentiment.
            logger.info("bugun_stage_trace %s", json.dumps(iz, ensure_ascii=False))

    return izle
