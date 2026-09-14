from sunucu.api.uygulama import uygulama
from sunucu.karar_motoru.semalar import KararSonucuSemasi


YASAK = {
    "yorum_metni", "yazar_takma_adi", "ham_evidence", "ai_reasoning", "internal_score",
    "duygu_yuzdesi", "model_confidence", "sponsor", "kullanilan_iddia_surumleri",
}


def anahtarlari_yur(value):
    if isinstance(value, dict):
        for anahtar, alt in value.items():
            yield anahtar
            yield from anahtarlari_yur(alt)
    elif isinstance(value, list):
        for alt in value:
            yield from anahtarlari_yur(alt)


def test_versioned_karar_endpointi_openapi_ve_public_allow_list():
    openapi = uygulama.openapi()
    assert "/v1/kararlar/degerlendir" in openapi["paths"]
    sema = KararSonucuSemasi.model_json_schema()
    assert set(anahtarlari_yur(sema)).isdisjoint(YASAK)


def test_teknik_hata_bos_sonuc_degil_503(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlalchemy.exc import OperationalError
    from sunucu.api.altyapi import ApiGuvenlikMiddleware
    from sunucu.karar_motoru.router import yonlendirici

    def patla(*args, **kwargs):
        raise OperationalError("select", {}, Exception("db yok"))
    monkeypatch.setattr("sunucu.karar_motoru.router.kararlari_degerlendir", patla)
    mini = FastAPI(); mini.add_middleware(ApiGuvenlikMiddleware); mini.include_router(yonlendirici)
    yanit = TestClient(mini).post("/v1/kararlar/degerlendir", json={
        "baglam": {"cografi_baglam": {"sehir": "samsun"}}, "aday_yer_idleri": ["00000000-0000-0000-0000-000000000001"]
    })
    assert yanit.status_code == 503
    assert yanit.json()["hata"]["durum"] == "unavailable"
