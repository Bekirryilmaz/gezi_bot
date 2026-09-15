from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import String, cast
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from sunucu.api.uygulama import admin_uygulama, uygulama
from sunucu.admin.workflow import inceleme_komutu_gonder
from sunucu.auth.rbac import yetkileri_birlestir
from sunucu.auth.servis import AdminBaglami, admin_olustur
from sunucu.veritabani.admin_modelleri import (
    AdminAuditOlayi,
    AdminOturum,
    AdminRol,
    IncelemeDosyasi,
)
from sunucu.veritabani.baglanti import motor, oturum_al
from sunucu.veritabani.bilgi_modelleri import Iddia, IddiaSurumu
from sunucu.veritabani.kimlik_modelleri import EslemeAdayi, Sube
from sunucu.veritabani.modeller import Yer


@pytest.fixture()
def admin_ortami():
    baglanti = motor.connect(); islem = baglanti.begin(); oturum = Session(bind=baglanti)
    def ayni_oturum():
        yield oturum
    uygulama.dependency_overrides[oturum_al] = ayni_oturum
    admin_uygulama.dependency_overrides[oturum_al] = ayni_oturum
    ek = uuid.uuid4().hex
    yonetici = admin_olustur(oturum, eposta=f"yonetici-{ek}@test.local", gorunen_ad="Yonetici", parola="cok-guvenli-test-parolasi", roller={"yonetici"})
    gozlemci = admin_olustur(oturum, eposta=f"gozlemci-{ek}@test.local", gorunen_ad="Gozlemci", parola="cok-guvenli-test-parolasi", roller={"gozlemci"})
    risk = admin_olustur(oturum, eposta=f"risk-{ek}@test.local", gorunen_ad="Risk", parola="cok-guvenli-test-parolasi", roller={"risk_onayci"})
    oturum.flush()
    try:
        yield TestClient(uygulama), oturum, yonetici, gozlemci, risk
    finally:
        uygulama.dependency_overrides.clear(); admin_uygulama.dependency_overrides.clear()
        oturum.close(); islem.rollback(); baglanti.close()


def _login(client: TestClient, eposta: str) -> str:
    yanit = client.post("/v1/admin/login", json={"eposta": eposta, "parola": "cok-guvenli-test-parolasi"})
    assert yanit.status_code == 200, yanit.text
    return yanit.json()["csrf_token"]


def test_admin_auth_rbac_ve_public_admin_dto_ayrimi(admin_ortami):
    client, _, _, gozlemci, _ = admin_ortami
    assert client.get("/v1/admin/me").status_code == 401
    csrf = _login(client, gozlemci.eposta)
    assert client.get("/v1/admin/me").status_code == 200
    assert client.get("/v1/admin/audit").status_code == 403
    assert client.post("/v1/admin/logout", headers={"X-CSRF-Token": "yanlis"}).status_code == 403
    assert client.post("/v1/admin/logout", headers={"X-CSRF-Token": csrf}).status_code == 204
    assert "/v1/admin/login" not in uygulama.openapi()["paths"]
    assert "/login" in admin_uygulama.openapi()["paths"]


def test_merge_authorization_ve_idor_default_deny(admin_ortami):
    client, oturum, _, gozlemci, _ = admin_ortami
    yerler = oturum.query(Yer).limit(2).all(); assert len(yerler) == 2
    aday = EslemeAdayi(sol_sube_id=yerler[0].id, sag_sube_id=yerler[1].id, confidence=0.7, belirsizlik={})
    oturum.add(aday); oturum.flush()
    csrf = _login(client, gozlemci.eposta)
    cevap = client.post("/v1/admin/incelemeler", headers={"X-CSRF-Token": csrf}, json={"eylem": "canonical_merge", "nesne_turu": "esleme_adayi", "nesne_id": aday.id, "gerekce": "Yetkisiz merge denenmemeli", "payload": {"hedef_sube_id": yerler[0].id}})
    assert cevap.status_code == 403
    gozlemci.kapsam = [str(uuid.uuid4())]; oturum.flush()
    assert client.get("/v1/admin/kimlik/esleme-adaylari").json() == []


def test_kritik_islem_ayni_kisi_onaylayamaz_ikinci_inceleme_audit_uretir(admin_ortami):
    client, oturum, yonetici, _, risk = admin_ortami
    yer = oturum.query(Yer).first(); assert yer is not None
    csrf = _login(client, yonetici.eposta)
    cevap = client.post("/v1/admin/incelemeler", headers={"X-CSRF-Token": csrf}, json={"eylem": "withdraw", "nesne_turu": "yer", "nesne_id": yer.id, "gerekce": "Yanlis olumlu bilginin yayini durdurulsun", "payload": {"gerekce_kodu": "dogruluk"}})
    assert cevap.status_code == 201
    dosya = cevap.json(); assert dosya["durum"] == "ikinci_inceleme_bekliyor"
    kendi = client.post(f"/v1/admin/incelemeler/{dosya['id']}/ikinci-onay", headers={"X-CSRF-Token": csrf}, json={"gerekce": "Kendi onayim olmamali", "beklenen_surum": dosya["surum"]})
    assert kendi.status_code == 409
    client.cookies.clear(); risk_csrf = _login(client, risk.eposta)
    onay = client.post(f"/v1/admin/incelemeler/{dosya['id']}/ikinci-onay", headers={"X-CSRF-Token": risk_csrf}, json={"gerekce": "Bagimsiz ikinci inceleme tamamlandi", "beklenen_surum": dosya["surum"]})
    assert onay.status_code == 200, onay.text
    assert onay.json()["durum"] == "tamamlandi"
    assert oturum.query(AdminAuditOlayi).filter_by(nesne_id=str(yer.id)).count() >= 2


def test_audit_db_trigger_ile_update_delete_edilemez(admin_ortami):
    _, oturum, yonetici, _, _ = admin_ortami
    olay = AdminAuditOlayi(aktor_id=yonetici.id, eylem="test", nesne_turu="test", nesne_id="1", gerekce="Append only dogrulamasi", istek_id="test", korelasyon_id="test", meta={})
    oturum.add(olay); oturum.flush()
    savepoint = oturum.begin_nested()
    with pytest.raises(DBAPIError):
        olay.gerekce = "degistirilemez"; oturum.flush()
    savepoint.rollback()


def test_tekerlekli_sandalye_claimi_ikinci_inceleme_ister(admin_ortami):
    _, oturum, yonetici, _, _ = admin_ortami
    iddia = oturum.query(Iddia).filter_by(aile="tekerlekli_sandalye_erisimi").first()
    if iddia is None:
        pytest.skip("Development fixture kritik claim icermiyor.")
    sahte_oturum = AdminOturum(
        kullanici_id=yonetici.id,
        token_hash=uuid.uuid4().hex,
        csrf_hash=uuid.uuid4().hex,
        sona_erme_zamani=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    baglam = AdminBaglami(
        yonetici,
        sahte_oturum,
        frozenset({"yonetici"}),
        yetkileri_birlestir({"yonetici"}),
    )
    dosya = inceleme_komutu_gonder(
        oturum,
        baglam=baglam,
        eylem="claim_approve",
        nesne_turu="claim",
        nesne_id=str(iddia.id),
        gerekce="Kritik erisim claimi bagimsiz inceleme beklemeli",
        payload={},
        istek_id=f"test-{uuid.uuid4()}",
    )
    assert dosya.onerilen_eylem == "kritik_claim_yayini"
    assert dosya.durum == "ikinci_inceleme_bekliyor"


def test_claim_kuyrugu_aile_durum_mekan_ve_sayfalama_sunar(admin_ortami):
    client, oturum, yonetici, _, _ = admin_ortami
    ornek = (
        oturum.query(Iddia)
        .filter_by(aile="wifi")
        .join(IncelemeDosyasi, IncelemeDosyasi.nesne_id == cast(Iddia.id, String))
        .filter(IncelemeDosyasi.durum == "bekliyor")
        .first()
    )
    if ornek is None:
        pytest.skip("Development fixture bekleyen wifi claim'i icermiyor.")
    csrf = _login(client, yonetici.eposta)
    cevap = client.get("/v1/admin/claimler?aile=wifi&durum=bekliyor&sayfa=1&sayfa_boyutu=2")
    assert cevap.status_code == 200, cevap.text
    govde = cevap.json()
    assert govde["sayfa"] == 1 and govde["sayfa_boyutu"] == 2
    assert govde["toplam"] >= len(govde["kayitlar"]) >= 1
    assert all(kayit["aile"] == "wifi" and kayit["durum"] == "bekliyor" for kayit in govde["kayitlar"])
    assert all(kayit["mekan_adi"] and kayit["kaynak_alani"] == "ozellikler.wifi" for kayit in govde["kayitlar"])
    detay = client.get(f"/v1/admin/claimler/{govde['kayitlar'][0]['id']}")
    assert detay.status_code == 200
    assert detay.json()["mekan_adi"] and detay.json()["public_preview"]["aile"] == "wifi"
    client.post("/v1/admin/logout", headers={"X-CSRF-Token": csrf})


def test_admin_dahili_sinyal_ve_birinci_el_gozlem_public_yayinlamaz(admin_ortami):
    client, oturum, yonetici, gozlemci, _ = admin_ortami
    yer = oturum.query(Yer).first()
    assert yer is not None
    sube = oturum.query(Sube).filter_by(legacy_yer_id=yer.id).one()
    csrf = _login(client, gozlemci.eposta)
    assert client.get("/v1/admin/dahili-sinyaller").status_code == 200
    yasak = client.post(
        "/v1/admin/gozlemler",
        headers={"X-CSRF-Token": csrf},
        json={
            "sube_id": sube.id,
            "aile": "wifi",
            "deger": True,
            "ozet": "Mekanda wifi dogrulandi yerinde.",
            "gerekce": "Birinci el gozlem kaydi icin yeterli gerekce.",
        },
    )
    assert yasak.status_code == 403
    client.post("/v1/admin/logout", headers={"X-CSRF-Token": csrf})
    csrf = _login(client, yonetici.eposta)
    cevap = client.post(
        "/v1/admin/gozlemler",
        headers={"X-CSRF-Token": csrf},
        json={
            "sube_id": sube.id,
            "aile": "wifi",
            "deger": True,
            "ozet": "Mekanda wifi dogrulandi yerinde.",
            "gerekce": "Birinci el gozlem kaydi icin yeterli gerekce.",
        },
    )
    assert cevap.status_code == 200, cevap.text
    govde = cevap.json()
    assert govde["otomatik_yayin"] is False
    assert govde["yayin_durumu"] == "inceleme_bekliyor"
    iddia = oturum.get(Iddia, govde["iddia_id"])
    assert iddia is not None
    surum = (
        oturum.query(IddiaSurumu)
        .filter_by(iddia_id=iddia.id, surum_no=iddia.aktif_surum_no)
        .one()
    )
    assert surum.yayin_durumu == "inceleme_bekliyor"
    assert "/v1/admin/dahili-sinyaller" not in __import__("sunucu.api.uygulama", fromlist=["uygulama"]).uygulama.openapi()["paths"]
    client.post("/v1/admin/logout", headers={"X-CSRF-Token": csrf})
