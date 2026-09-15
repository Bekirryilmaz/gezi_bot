import pytest
from ortak.sabitler import (
    KARAR_DISI_DAHILI_SINYAL_AILELERI,
    CikarimYontemi,
    DuyguEtiketi,
    GozlemTuru,
    SinyalYonu,
    VeriKaynagi,
)
from veri.duygu_analizi.gozlem_adayi import (
    YAPISAL_SINYAL_KURALLARI,
    yorumdan_aday_gozlemler,
    yorumdan_yapisal_sinyal_adaylari,
)
from veri.ortak.gozlem_adayi_modeli import AdayGozlem, CikarimGuvenSinifi
from veri.ortak.yorum_modeli import HamYorum


def _canonical_aday(**degisiklikler):
    alanlar = {
        "kaynak": VeriKaynagi.EKSI_SOZLUK,
        "kaynak_kayit_id": "sentetik-yorum-1",
        "yer_adayi": "sentetik-yer-1",
        "sube_adayi": "sentetik-sube-1",
        "span": "wifi var",
        "konu": "wifi",
        "aile": "wifi",
        "yon": SinyalYonu.SUPPORT,
        "deger": True,
        "gozlem_turu": GozlemTuru.FACT_SIGNAL,
        "tahmini_gozlem": {"yon": "destek", "deger": True},
        "cikarim_yontemi": CikarimYontemi.DETERMINISTIK_KURAL,
        "model_surumu": "sentetik-model-v1",
        "kural_surumu": "sentetik-kural-v1",
        "cikarim_guven_sinifi": CikarimGuvenSinifi.DUSUK,
        "guven_kirilimi": {"genel_bert_kullanildi": False},
    }
    alanlar.update(degisiklikler)
    return AdayGozlem(**alanlar)


def test_nlp_yalniz_inceleme_bekleyen_gozlem_adayi_uretir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS,
        kaynak_yer_id="place-1",
        kaynak_yorum_id="review-1",
        yorum_metni="Manzarasi harikaydi ama fiyatlar biraz yuksekti.",
    )
    adaylar = yorumdan_aday_gozlemler(yorum, DuyguEtiketi.OLUMLU, 0.91)
    assert adaylar
    assert {aday.inceleme_durumu.value for aday in adaylar} == {"bekliyor"}
    assert all(not aday.otomatik_yayinlanabilir for aday in adaylar)
    payload = [aday.model_dump(mode="json") for aday in adaylar]
    metin = str(payload)
    for yasak in ("mekan_puani", "uygunluk", "claim", "duygu_yuzdesi", "duygu_skoru"):
        assert yasak not in metin
    assert {aday.aile for aday in adaylar} >= {"manzara", "fiyat_algisi"}
    assert {aday.gozlem_turu.value for aday in adaylar} <= {
        "fact_signal",
        "experience_signal",
        "sentiment_signal",
    }


def test_nlp_adayi_kaynak_span_model_ve_guven_sinifi_tasir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="yer-adayi",
        yorum_metni="Ortam sakin ve temizdi.",
    )
    aday = next(
        aday
        for aday in yorumdan_aday_gozlemler(yorum, DuyguEtiketi.OLUMLU, 0.5)
        if aday.aile == "sessiz_ortam"
    )
    assert aday.kaynak is VeriKaynagi.EKSI_SOZLUK
    assert aday.yer_adayi == "yer-adayi"
    assert aday.span
    assert aday.model_surumu
    assert aday.cikarim_guven_sinifi.value == "dusuk"
    assert aday.guven_kirilimi["genel_bert_kullanildi"] is False


def test_aday_gozlem_exact_eski_shapei_surumsuz_okur():
    aday = AdayGozlem(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_kayit_id="sentetik-yorum-1",
        yer_adayi="sentetik-yer-1",
        sube_adayi="sentetik-sube-1",
        span="wifi var",
        konu="wifi",
        tahmini_gozlem={"yon": "destek", "deger": True},
        model_surumu="sentetik-model-v1",
        cikarim_guven_sinifi=CikarimGuvenSinifi.DUSUK,
    )

    assert aday.sozlesme_surumu.value == "legacy"
    assert aday.aile == "wifi"
    assert aday.yon.value == "support"
    assert aday.deger is True
    assert aday.gozlem_turu.value == "fact_signal"
    assert aday.cikarim_yontemi
    assert aday.kural_surumu
    assert aday.guven_kirilimi
    assert aday.zamansal_durum.value == "unknown"
    assert len(aday.span_hash) == 64
    assert aday.dahili_referans
    assert aday.otomatik_yayinlanabilir is False


@pytest.mark.parametrize("konu", ["servis", "personel", "temizlik"])
def test_noncanonical_legacy_aday_model_dump_roundtripinde_legacy_kalir(konu):
    eski_payload = {
        "kaynak": VeriKaynagi.EKSI_SOZLUK,
        "yer_adayi": "sentetik-yer-1",
        "span": f"{konu} iyiydi",
        "konu": konu,
        "tahmini_gozlem": {"yon": "destek", "deger": True},
        "model_surumu": "tarihi-model-v1",
        "cikarim_guven_sinifi": CikarimGuvenSinifi.DUSUK,
    }

    ilk = AdayGozlem.model_validate(eski_payload)
    serialize_edilmis = ilk.model_dump()
    ikinci = AdayGozlem.model_validate(serialize_edilmis)

    assert serialize_edilmis["sozlesme_surumu"] == "legacy"
    assert ikinci.sozlesme_surumu.value == "legacy"
    assert ikinci.aile == konu


def test_yonsuz_legacy_aday_model_dump_roundtripinde_legacy_kalir():
    eski_payload = {
        "kaynak": VeriKaynagi.EKSI_SOZLUK,
        "yer_adayi": "sentetik-yer-1",
        "span": "genel bir tarihi gozlem",
        "konu": "servis",
        "tahmini_gozlem": {"duygu": "notr"},
        "model_surumu": "tarihi-model-v1",
        "cikarim_guven_sinifi": CikarimGuvenSinifi.DUSUK,
    }

    ilk = AdayGozlem.model_validate(eski_payload)
    serialize_edilmis = ilk.model_dump()
    ikinci = AdayGozlem.model_validate(serialize_edilmis)

    assert serialize_edilmis["sozlesme_surumu"] == "legacy"
    assert ikinci.sozlesme_surumu.value == "legacy"
    assert ikinci.yon is None


def test_canonical_benzeri_eksik_payload_legacye_dusmez():
    with pytest.raises(ValueError):
        AdayGozlem(
            kaynak=VeriKaynagi.EKSI_SOZLUK,
            kaynak_kayit_id="sentetik-yorum-1",
            yer_adayi="sentetik-yer-1",
            span="wifi var",
            konu="wifi",
            aile="wifi",
            tahmini_gozlem={"yon": "destek", "deger": True},
            model_surumu="sentetik-model-v1",
            cikarim_guven_sinifi=CikarimGuvenSinifi.DUSUK,
        )


def test_explicit_legacy_canonical_izleri_bypass_edemez():
    with pytest.raises(ValueError):
        AdayGozlem(
            sozlesme_surumu="legacy",
            kaynak=VeriKaynagi.EKSI_SOZLUK,
            kaynak_kayit_id="sentetik-yorum-1",
            yer_adayi="sentetik-yer-1",
            span="wifi var",
            konu="wifi",
            aile="wifi",
            tahmini_gozlem={"yon": "destek", "deger": True},
            model_surumu="sentetik-model-v1",
            cikarim_guven_sinifi=CikarimGuvenSinifi.DUSUK,
        )


def test_tam_model_shapeindeki_canonical_producer_legacy_bypass_edemez():
    canonical_payload = _canonical_aday().model_dump()
    canonical_payload["sozlesme_surumu"] = "legacy"

    with pytest.raises(ValueError):
        AdayGozlem.model_validate(canonical_payload)


@pytest.mark.parametrize(
    "degisiklikler",
    [
        {"aile": "canonical_degil", "konu": "canonical_degil"},
        {"yon": SinyalYonu.SUPPORT, "deger": False},
        {
            "gozlem_turu": GozlemTuru.SENTIMENT_SIGNAL,
            "yon": SinyalYonu.SUPPORT,
            "deger": "olumsuz",
        },
        {"yon": None, "tahmini_gozlem": {}},
        {
            "gozlem_turu": GozlemTuru.EXPERIENCE_SIGNAL,
            "deger": "keyfi_deger",
            "tahmini_gozlem": {"yon": "destek", "deger": "keyfi_deger"},
        },
        {
            "gozlem_turu": GozlemTuru.SENTIMENT_SIGNAL,
            "deger": "olumlu",
            "tahmini_gozlem": {"yon": "destek", "deger": "olumlu"},
        },
        {"kaynak_kayit_id": None},
    ],
)
def test_canonical_aday_gecersiz_aile_yon_tur_deger_bilesimini_reddeder(degisiklikler):
    with pytest.raises(ValueError):
        _canonical_aday(**degisiklikler)


def test_otomatik_yayin_yasagi_json_serializationda_da_yer_alir():
    payload = _canonical_aday().model_dump(mode="json")
    assert payload["otomatik_yayinlanabilir"] is False


def test_dahili_referans_tum_kimlik_bilesenleriyle_deterministik_ve_benzersizdir():
    taban = _canonical_aday()
    ayni = _canonical_aday()
    cesitler = [
        _canonical_aday(kaynak_kayit_id="sentetik-yorum-2"),
        _canonical_aday(aile="otopark", konu="otopark"),
        _canonical_aday(
            gozlem_turu=GozlemTuru.EXPERIENCE_SIGNAL,
            deger="kotu_degil",
            tahmini_gozlem={"yon": "destek", "deger": "kotu_degil"},
        ),
        _canonical_aday(
            yon=SinyalYonu.COUNTER,
            deger=False,
            tahmini_gozlem={"yon": "karsi", "deger": False},
        ),
        _canonical_aday(span="wifi mevcut"),
        _canonical_aday(model_surumu="sentetik-model-v2"),
        _canonical_aday(kural_surumu="sentetik-kural-v2"),
    ]

    assert taban.dahili_referans == ayni.dahili_referans
    assert len({taban.dahili_referans, *(aday.dahili_referans for aday in cesitler)}) == 8


def test_disaridan_verilen_span_hash_ve_referans_guvenli_yeniden_uretilir():
    temiz = _canonical_aday()
    degistirilmis = _canonical_aday(
        span_hash="0" * 64,
        dahili_referans="guvenilmeyen-referans",
    )
    assert degistirilmis.span_hash == temiz.span_hash
    assert degistirilmis.dahili_referans == temiz.dahili_referans


def test_safe_extractor_fact_ve_experience_turlerini_acik_tasir():
    ornekler = [
        ("wifi var", "wifi", "support", "fact_signal", True),
        ("wifi yok", "wifi", "counter", "fact_signal", False),
        ("wifi çok yavaş", "wifi", "counter", "experience_signal", "cok_yavas"),
        ("sakin değil", "sessiz_ortam", "counter", "experience_signal", False),
        ("otopark yok", "otopark", "counter", "fact_signal", False),
        ("çocukla gidilmez", "cocuk_uygunlugu", "counter", "experience_signal", False),
        (
            "çocuklarla çok rahat",
            "cocuk_uygunlugu",
            "support",
            "experience_signal",
            True,
        ),
        ("manzarası yok", "manzara", "counter", "fact_signal", False),
        ("bahçesi var", "acik_alan", "support", "fact_signal", True),
        ("çok pahalı", "fiyat_algisi", "counter", "experience_signal", "pahali"),
        ("uygun fiyatlı", "fiyat_algisi", "support", "experience_signal", "uygun"),
        (
            "laptopla çalışılmaz",
            "calisma_uygunlugu",
            "counter",
            "experience_signal",
            False,
        ),
        (
            "ders çalışmak için ideal",
            "calisma_uygunlugu",
            "support",
            "experience_signal",
            True,
        ),
        (
            "rezervasyonsuz yer bulamadık",
            "rezervasyon",
            "counter",
            "experience_signal",
            "rezervasyonsuz_yer_bulunamadi",
        ),
        (
            "canlı müzik çok yüksek",
            "canli_muzik",
            "counter",
            "experience_signal",
            "cok_yuksek",
        ),
    ]
    for metin, aile, yon, gozlem_turu, deger in ornekler:
        yorum = HamYorum(
            kaynak=VeriKaynagi.EKSI_SOZLUK,
            kaynak_yer_id="sentetik-yer",
            yorum_metni=metin,
        )
        adaylar = [a for a in yorumdan_yapisal_sinyal_adaylari(yorum, 0.99) if a.aile == aile]
        assert len(adaylar) == 1, metin
        aday = adaylar[0]
        assert aday.yon.value == yon, metin
        assert aday.gozlem_turu.value == gozlem_turu, metin
        assert aday.deger == deger, metin
        assert aday.cikarim_yontemi == "deterministik_kural", metin
        assert aday.kural_surumu == "safe-extractor-v2", metin
        assert aday.cikarim_guven_sinifi.value in {"orta", "yuksek"}, metin
        assert aday.guven_kirilimi["genel_bert_kullanildi"] is False, metin
        assert aday.guven_kirilimi["bert_buyuklugunden_turetilmedi"] is True, metin
        assert aday.otomatik_yayinlanabilir is False, metin


def test_safe_extractor_ayni_yorumda_iki_aspect_uretir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni="Bahçesi var ama wifi çok yavaş.",
    )
    adaylar = yorumdan_yapisal_sinyal_adaylari(yorum, -0.99)
    assert {(aday.aile, aday.yon.value, aday.gozlem_turu.value) for aday in adaylar} == {
        ("acik_alan", "support", "fact_signal"),
        ("wifi", "counter", "experience_signal"),
    }


def test_negation_tekil_regexler_yerine_genel_mekanizmayla_islenir():
    assert all(r"\bdegil\b" not in kural.desen for kural in YAPISAL_SINYAL_KURALLARI)


@pytest.mark.parametrize(
    "metin,aile,beklenen_deger",
    [
        ("wifi çok yavaş değil", "wifi", "cok_yavas_degil"),
        ("fiyatlar yüksek değil", "fiyat_algisi", "pahali_degil"),
        ("ses çok yüksek değil", "sessiz_ortam", True),
        ("canlı müzik çok yüksek değil", "canli_muzik", "cok_yuksek_degil"),
        ("wifi yok değil", "wifi", True),
    ],
)
def test_yakin_negation_genel_mekanizmayla_yonu_supporta_cevirir(
    metin, aile, beklenen_deger
):
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni=metin,
    )
    adaylar = [a for a in yorumdan_yapisal_sinyal_adaylari(yorum, 0.99) if a.aile == aile]
    assert len(adaylar) == 1
    assert adaylar[0].yon is SinyalYonu.SUPPORT
    assert adaylar[0].deger == beklenen_deger


@pytest.mark.parametrize(
    "metin,aile,beklenen_deger",
    [
        ("wifi cok yavas degildi", "wifi", "cok_yavas_degil"),
        ("wifi çok yavaş değildi", "wifi", "cok_yavas_degil"),
        ("fiyatlar yuksek degilmis", "fiyat_algisi", "pahali_degil"),
        ("fiyatlar yüksek değilmiş", "fiyat_algisi", "pahali_degil"),
        ("ses cok yuksek degildir", "sessiz_ortam", True),
        ("ses çok yüksek değildir", "sessiz_ortam", True),
        ("canli muzik cok yuksek degildi", "canli_muzik", "cok_yuksek_degil"),
        ("canlı müzik çok yüksek değildi", "canli_muzik", "cok_yuksek_degil"),
    ],
)
def test_yakin_negation_cekimleri_yonu_supporta_cevirir(
    metin, aile, beklenen_deger
):
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni=metin,
    )
    aday = next(
        aday
        for aday in yorumdan_yapisal_sinyal_adaylari(yorum, 0.0)
        if aday.aile == aile
    )
    assert aday.yon is SinyalYonu.SUPPORT
    assert aday.deger == beklenen_deger


def test_uzak_negation_aspect_yonunu_cevirmez():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni="Wifi çok yavaş ama servis kötü değildi.",
    )
    aday = next(
        aday
        for aday in yorumdan_yapisal_sinyal_adaylari(yorum, 0.0)
        if aday.aile == "wifi"
    )
    assert aday.yon is SinyalYonu.COUNTER
    assert aday.deger == "cok_yavas"


@pytest.mark.parametrize(
    "metin,aile,beklenen_yon,beklenen_deger",
    [
        ("kalabalık değil", "kalabaliklik", "counter", "sakin"),
        ("deniz görünmüyor", "manzara", "counter", "gorunmuyor"),
        ("denizi göremedik", "manzara", "counter", "goremedik"),
        ("wifi kötü değil", "wifi", "support", "kotu_degil"),
        ("çok pahalı değil", "fiyat_algisi", "support", "pahali_degil"),
        ("gürültülü değil", "sessiz_ortam", "support", True),
    ],
)
def test_explicit_negation_dar_desenden_once_dogru_yonu_uretir(
    metin, aile, beklenen_yon, beklenen_deger
):
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni=metin,
    )
    adaylar = [a for a in yorumdan_yapisal_sinyal_adaylari(yorum, 0.99) if a.aile == aile]
    assert len(adaylar) == 1
    assert adaylar[0].yon.value == beklenen_yon
    assert adaylar[0].deger == beklenen_deger


def test_park_sorunu_experience_counter_olarak_cikarilir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni="Park sorunu yaşadık.",
    )
    aday = yorumdan_yapisal_sinyal_adaylari(yorum, 0.99)[0]
    assert aday.aile == "otopark"
    assert aday.yon.value == "counter"
    assert aday.gozlem_turu.value == "experience_signal"


def test_notr_aspect_sentiment_adayi_uretmez():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni="Manzarası var.",
    )
    adaylar = yorumdan_aday_gozlemler(yorum, DuyguEtiketi.NOTR, 0.0)
    assert all(aday.gozlem_turu is not GozlemTuru.SENTIMENT_SIGNAL for aday in adaylar)


def test_explicit_aspect_guveni_bert_skorundan_turemez():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni="Manzarası güzeldi.",
    )
    dusuk = yorumdan_aday_gozlemler(yorum, DuyguEtiketi.OLUMSUZ, -0.99)
    yuksek = yorumdan_aday_gozlemler(yorum, DuyguEtiketi.OLUMLU, 0.99)
    dusuk_aspect = next(
        a for a in dusuk if a.aile == "manzara" and a.gozlem_turu is not GozlemTuru.SENTIMENT_SIGNAL
    )
    yuksek_aspect = next(
        a
        for a in yuksek
        if a.aile == "manzara" and a.gozlem_turu is not GozlemTuru.SENTIMENT_SIGNAL
    )
    assert dusuk_aspect.cikarim_guven_sinifi == yuksek_aspect.cikarim_guven_sinifi
    assert dusuk_aspect.cikarim_guven_sinifi.value in {"orta", "yuksek"}
    assert dusuk_aspect.guven_kirilimi["genel_bert_kullanildi"] is False
    assert yuksek_aspect.guven_kirilimi["genel_bert_kullanildi"] is False
    assert dusuk_aspect.guven_kirilimi["bert_buyuklugunden_turetilmedi"] is True


def test_genel_bert_karar_disi_sentiment_candidate_uretir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        kaynak_yorum_id="sentetik-yorum",
        yorum_metni="Genel olarak beğendim.",
    )
    adaylar = yorumdan_aday_gozlemler(yorum, DuyguEtiketi.OLUMLU, 0.82)
    assert len(adaylar) == 1
    aday = adaylar[0]
    assert aday.aile == "genel_duygu"
    assert aday.gozlem_turu is GozlemTuru.SENTIMENT_SIGNAL
    assert aday.yon is SinyalYonu.SUPPORT
    assert aday.deger == "olumlu"
    assert aday.guven_kirilimi["genel_bert_kullanildi"] is True
    assert aday.tahmini_gozlem["karar_sinyali"] is False
    assert aday.aile in KARAR_DISI_DAHILI_SINYAL_AILELERI


def test_yeni_producer_canonical_v1i_explicit_uretir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni="Wifi var.",
    )
    aday = yorumdan_yapisal_sinyal_adaylari(yorum, 0.0)[0]
    assert aday.sozlesme_surumu.value == "canonical-v1"
    assert "sozlesme_surumu" in aday.model_fields_set


def test_review_id_yokken_tam_yorum_fingerprint_referansi_ayristirir():
    def referans(metin):
        yorum = HamYorum(
            kaynak=VeriKaynagi.EKSI_SOZLUK,
            kaynak_yer_id="sentetik-yer",
            yorum_metni=metin,
        )
        return next(
            aday.dahili_referans
            for aday in yorumdan_yapisal_sinyal_adaylari(yorum, 0.0)
            if aday.aile == "wifi"
        )

    ilk = referans("Wifi var. İlk sentetik yorum bağlamı.")
    ilk_tekrar = referans("Wifi var. İlk sentetik yorum bağlamı.")
    ikinci = referans("Wifi var. İkinci sentetik yorum bağlamı.")
    assert ilk == ilk_tekrar
    assert ilk != ikinci


def test_yapisal_sinyal_genel_begeni_claimi_uretmez():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni="Güzel, mükemmel, kaliteli, romantik ve en iyi mekan.",
    )
    assert yorumdan_yapisal_sinyal_adaylari(yorum, 0.9) == []


def test_yapisal_guven_duygu_skorundan_bagimsizdir():
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni="Otopark var.",
    )
    for skor in (-0.99, 0.0, 0.99):
        aday = yorumdan_yapisal_sinyal_adaylari(yorum, skor)[0]
        assert aday.cikarim_guven_sinifi.value == "yuksek"
        assert aday.guven_kirilimi["bert_buyuklugunden_turetilmedi"] is True


def test_genel_konu_yapisal_karsi_sinyali_bastirmaz(monkeypatch):
    from types import SimpleNamespace

    from veri.duygu_analizi import gozlem_adayi

    monkeypatch.setattr(
        gozlem_adayi,
        "konulari_tespit_et",
        lambda *args, **kwargs: [
            SimpleNamespace(
                konu="otopark", gecen_ifade="otopark", duygu_etiketi=DuyguEtiketi.OLUMLU
            )
        ],
    )
    yorum = HamYorum(
        kaynak=VeriKaynagi.EKSI_SOZLUK,
        kaynak_yer_id="sentetik-yer",
        yorum_metni="Otopark yok ama yemek harika.",
    )
    adaylar = yorumdan_aday_gozlemler(yorum, DuyguEtiketi.OLUMLU, 0.99)
    yapisal = [a for a in adaylar if a.tahmini_gozlem["bilgi_turu"] == "yapisal_sinyal_adayi"]
    assert len(yapisal) == 1
    assert yapisal[0].tahmini_gozlem["yon"] == "karsi"
