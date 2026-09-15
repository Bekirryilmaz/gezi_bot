from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from ortak.sabitler import DuyguEtiketi, VeriKaynagi
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
        ("açık alan yok", "acik_alan"),
        ("çok pahalı", "fiyat_algisi"),
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


def test_dahili_agregasyon_unique_review_karantina_ve_temporal_unknown_ayirir():
    from sunucu.bilgi.aggregation import dahili_tercih_kapisi

    now = datetime.now(UTC)

    def gozlem(**kwargs):
        temel = dict(
            branch_id="sube-1",
            family="wifi",
            evidence_id="span-1",
            source="google_maps",
            direction="support",
            observed_at=None,
            valid_until=None,
            branch_confidence="verified",
            rights_status="allowed",
            verified=False,
            observation_id="yorum-1",
            epistemic_type="fact_signal",
            review_id="yorum-1",
            kullanim_durumu="aktif",
        )
        temel.update(kwargs)
        return SignalObservation(**temel)

    sinyaller = aggregate(
        [
            gozlem(),
            gozlem(evidence_id="span-2"),
            gozlem(
                evidence_id="span-3",
                direction="counter",
                epistemic_type="experience_signal",
                review_id="yorum-2",
                observation_id="yorum-2",
            ),
            gozlem(
                family="genel_duygu",
                evidence_id="span-4",
                review_id="yorum-3",
                observation_id="yorum-3",
                epistemic_type="sentiment_signal",
            ),
            gozlem(
                family="otopark",
                evidence_id="span-5",
                review_id="yorum-4",
                observation_id="yorum-4",
                kullanim_durumu="karantina",
            ),
        ],
        now=now,
    )
    wifi = next(sinyal for sinyal in sinyaller if sinyal["family"] == "wifi")
    assert wifi["unique_review_count"] == 2
    assert wifi["fact_support_count"] == 1
    assert wifi["experience_counter_count"] == 1
    assert wifi["temporal_unknown"] is True
    assert wifi["source_diversity"] == 1
    assert wifi["guven_sinifi"] == "kalibre_edilmedi"
    assert wifi["durum"] == "karar_disi"
    assert dahili_tercih_kapisi(wifi)["preference_eligible"] is False
    assert {sinyal["family"] for sinyal in sinyaller} == {"wifi"}
    assert promotion_gate(wifi, risk="factual")["automatic_publication"] is False


def test_sentiment_signal_agregasyona_girmez():
    now = datetime.now(UTC)
    sinyaller = aggregate(
        [
            SignalObservation(
                "sube-1",
                "yemek",
                "span-1",
                "google_maps",
                "support",
                now,
                None,
                "verified",
                "allowed",
                False,
                "yorum-1",
                "sentiment_signal",
                "yorum-1",
                "aktif",
            )
        ],
        now=now,
    )
    assert sinyaller == []


def test_dahili_kalibrasyon_zayif_sinyali_karar_disinda_tutar():
    from sunucu.bilgi.aggregation import dahili_tercih_kapisi, guven_sinifini_uygula

    zayif = {
        "family": "wifi",
        "unique_review_count": 2,
        "supporting_observation_count": 2,
        "counter_observation_count": 0,
        "conflict_level": "none",
        "branch_confidence": "verified",
        "rights_status": "allowed",
        "temporal_unknown": True,
        "source_diversity": 1,
        "guven_sinifi": "kalibre_edilmedi",
        "durum": "karar_disi",
    }
    orta = dict(zayif, unique_review_count=6, supporting_observation_count=6)
    esikler = {"zayif_max_unique_review": 3, "orta_max_unique_review": 8}
    zayif_sonuc = guven_sinifini_uygula(zayif, esikler)
    orta_sonuc = guven_sinifini_uygula(orta, esikler)
    assert zayif_sonuc["guven_sinifi"] == "zayif"
    assert zayif_sonuc["durum"] == "karar_disi"
    assert dahili_tercih_kapisi(zayif_sonuc)["preference_eligible"] is False
    assert orta_sonuc["guven_sinifi"] == "orta"
    assert orta_sonuc["durum"] == "aktif"
    assert dahili_tercih_kapisi(orta_sonuc)["preference_eligible"] is True


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


def test_ai_isleme_hakki_internal_nlp_icin_yeterlidir(monkeypatch):
    from veri.duygu_analizi import pipeline_calistir

    politika = SimpleNamespace(
        kaynak=VeriKaynagi.GOOGLE_MAPS.value,
        kamusal_gosterim="yasak",
        turev_iddia="yasak",
        ai_isleme="izinli",
        uzun_sureli_saklama="bilinmiyor",
        gecerli_baslangic=None,
        gecerli_bitis=None,
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "toplu_duygu_tahmin_et",
        lambda *args, **kwargs: [(DuyguEtiketi.NOTR, 0.0)],
    )
    yorum = HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS,
        kaynak_yer_id="sentetik",
        yorum_metni="wifi var",
    )

    adaylar = pipeline_calistir._yorumlari_isle([yorum], 16, politika=politika)

    assert len(adaylar) == 1
    assert adaylar[0].gozlem_turu.value == "fact_signal"
    assert adaylar[0].otomatik_yayinlanabilir is False


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
