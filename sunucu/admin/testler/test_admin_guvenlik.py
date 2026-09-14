from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from sunucu.api.uygulama import admin_uygulama, uygulama
from sunucu.auth.servis import admin_olustur
from sunucu.veritabani.admin_modelleri import AdminAuditOlayi, AdminRol
from sunucu.veritabani.baglanti import motor, oturum_al
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
