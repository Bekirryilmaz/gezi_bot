from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from ortak.sabitler import VeriKaynagi
from sunucu.bilgi.aggregation import SignalObservation, aggregate, promotion_gate
from sunucu.bugun_ne_yapalim.gelistirme_izi import gelistirme_izi
from veri.duygu_analizi.gozlem_adayi import yorumdan_yapisal_sinyal_adaylari
from veri.ortak.yorum_modeli import HamYorum


@pytest.mark.parametrize(
    "phrase,family",
    [
        ("sakin değil", "sessiz_ortam"),
        ("sessiz değil", "sessiz_ortam"),
        ("çok gürültülü", "sessiz_ortam"),
        ("otopark yok", "otopark"),
        ("wifi yok", "wifi"),
        ("wifi çekmiyor", "wifi"),
        ("çocukla gidilmez", "cocuk_uygunlugu"),
        ("manzarası yok", "manzara"),
        ("açık alan yok", "acik_hava"),
        ("çok pahalı", "uygun_fiyat"),
        ("çalışmaya uygun değil", "calisma_uygunlugu"),
    ],
)
def test_explicit_counter_never_supports(phrase, family):
    review = HamYorum(kaynak=VeriKaynagi.GOOGLE_MAPS, kaynak_yer_id="synthetic", yorum_metni=phrase)
    relevant = [a for a in yorumdan_yapisal_sinyal_adaylari(review, 0.99) if a.konu == family]
    assert relevant
    assert all(a.tahmini_gozlem["yon"] == "karsi" for a in relevant)
    assert all(not a.otomatik_yayinlanabilir for a in relevant)


def test_duplicates_counter_rights_and_branches():
    now = datetime.now(UTC)

    def observation(branch="a", direction="support", rights="allowed", evidence="x"):
        return SignalObservation(
            branch,
            "wifi",
            evidence,
            "first_party",
            direction,
            now,
            now + timedelta(days=1),
            "verified",
            rights,
            True,
        )

    signals = aggregate(
        [
            observation(),
            observation(),
            observation(direction="counter"),
            observation(branch="b", rights="unknown"),
        ],
        now=now,
    )
    first, second = signals
    assert first["supporting_observation_count"] == 1
    assert first["counter_observation_count"] == 1
    assert first["unique_evidence_count"] == 1
    assert first["conflict_level"] == "conflicting"
    assert "counter_evidence_review" in promotion_gate(first, risk="factual")["reasons"]
    assert "rights_blocked" in promotion_gate(second, risk="factual")["reasons"]


def test_no_invented_freshness_or_subjective_threshold():
    row = SignalObservation(
        "a", "sessiz_ortam", "x", "first_party", "support", None, None, "unknown", "allowed"
    )
    signal = aggregate([row])[0]
    result = promotion_gate(signal, risk="subjective")
    assert signal["freshness"] == "unknown"
    assert not result["admin_review_eligible"]
    assert "subjective_gate_uncalibrated" in result["reasons"]
    assert result["automatic_publication"] is False


def test_rights_gate_runs_before_model(monkeypatch):
    from veri.duygu_analizi import pipeline_calistir

    def forbidden(*args, **kwargs):
        pytest.fail("model must not run for unknown rights")

    monkeypatch.setattr(pipeline_calistir, "toplu_duygu_tahmin_et", forbidden)
    review = HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS, kaynak_yer_id="synthetic", yorum_metni="wifi var"
    )
    with pytest.raises(PermissionError, match="kaynak_politikasi_yok"):
        pipeline_calistir._yorumlari_isle([review], 16)


def test_trace_early_return_and_public_separation(monkeypatch):
    monkeypatch.setenv("UYGULAMA_ORTAMI", "test")
    session = SimpleNamespace(info={})

    @gelistirme_izi
    def service(oturum, talep, *, request_id):
        return SimpleNamespace(durum="clarification", kesfet=None)

    response = service(session, None, request_id="synthetic")
    assert session.info["faz25_trace"]["final_state"] == "clarification"
    assert session.info["faz25_trace"]["selected_count"] == 0
    assert not hasattr(response, "parsed_intent")
    monkeypatch.setenv("UYGULAMA_ORTAMI", "production")
    other_session = SimpleNamespace(info={})
    service(other_session, None, request_id="synthetic")
    assert not other_session.info


def test_parking_unknown_is_insufficient_and_budget_is_concrete(monkeypatch):
    from sunucu.bugun_ne_yapalim.semalar import BugunNeYapalimTalebi
    from sunucu.bugun_ne_yapalim.servis import bugun_ne_yapalim
    from sunucu.veritabani.baglanti import OturumUretici

    monkeypatch.setenv("UYGULAMA_ORTAMI", "test")
    with OturumUretici() as oturum:
        parking = bugun_ne_yapalim(
            oturum,
            BugunNeYapalimTalebi(serbest_metin="otopark şart yemek"),
            request_id="parking-unknown",
        )
        assert parking.durum == "insufficient"
        assert not parking.kesfet.secenekler
        assert "Otopark" in parking.dogrulanamayan_ihtiyaclar
        budget = bugun_ne_yapalim(
            oturum,
            BugunNeYapalimTalebi(serbest_metin="en fazla 500 tl yemek"),
            request_id="budget-unknown",
        )
        assert "Güncel fiyatın bütçe sınırını karşılaması" in budget.dogrulanamayan_ihtiyaclar
