from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from sunucu.auth.rbac import Yetki, yetkileri_birlestir
from sunucu.veritabani.admin_modelleri import AdminKullanici, AdminKullaniciRolu, AdminOturum, AdminRol
from sunucu.veritabani.baglanti import oturum_al

OTURUM_COOKIE = "samandira_admin_oturum"
CSRF_COOKIE = "samandira_admin_csrf"
_PBKDF2_TUR = 600_000


def _sha256(deger: str) -> str:
    return hashlib.sha256(deger.encode("utf-8")).hexdigest()


def parola_hashle(parola: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", parola.encode("utf-8"), bytes.fromhex(salt), _PBKDF2_TUR).hex()


def parola_dogrula(parola: str, kullanici: AdminKullanici) -> bool:
    return hmac.compare_digest(parola_hashle(parola, kullanici.parola_salt), kullanici.parola_hash)


def admin_olustur(oturum: Session, *, eposta: str, gorunen_ad: str, parola: str, roller: set[str], kapsam: list[str] | None = None) -> AdminKullanici:
    if len(parola) < 14:
        raise ValueError("Admin parolasi en az 14 karakter olmalidir")
    salt = secrets.token_hex(32)
    kullanici = AdminKullanici(eposta=eposta.strip().lower(), gorunen_ad=gorunen_ad, parola_salt=salt, parola_hash=parola_hashle(parola, salt), kapsam=kapsam or [])
    oturum.add(kullanici)
    oturum.flush()
    for kod in roller:
        rol = oturum.query(AdminRol).filter_by(kod=kod).one()
        oturum.add(AdminKullaniciRolu(kullanici_id=kullanici.id, rol_id=rol.id))
    oturum.flush()
    return kullanici


def oturum_ac(oturum: Session, kullanici: AdminKullanici, *, ip: str | None, user_agent: str | None) -> tuple[AdminOturum, str, str]:
    token = secrets.token_urlsafe(48)
    csrf = secrets.token_urlsafe(32)
    sure_dk = int(os.environ.get("ADMIN_OTURUM_SURESI_DK", "480"))
    kayit = AdminOturum(
        kullanici_id=kullanici.id,
        token_hash=_sha256(token),
        csrf_hash=_sha256(csrf),
        sona_erme_zamani=datetime.now(timezone.utc) + timedelta(minutes=sure_dk),
        ip_izi=_sha256(ip) if ip else None,
        user_agent_izi=_sha256(user_agent) if user_agent else None,
    )
    oturum.add(kayit)
    oturum.flush()
    return kayit, token, csrf


@dataclass(frozen=True)
class AdminBaglami:
    kullanici: AdminKullanici
    oturum: AdminOturum
    roller: frozenset[str]
    yetkiler: frozenset[Yetki]

    def kapsam_izinli_mi(self, kapsam_id: str | None) -> bool:
        return not self.kullanici.kapsam or (kapsam_id is not None and kapsam_id in self.kullanici.kapsam)


def _rolleri_al(oturum: Session, kullanici_id: str) -> frozenset[str]:
    satirlar = oturum.query(AdminRol.kod).join(AdminKullaniciRolu, AdminKullaniciRolu.rol_id == AdminRol.id).filter(AdminKullaniciRolu.kullanici_id == kullanici_id).all()
    return frozenset(kod for (kod,) in satirlar)


def admin_baglami_al(request: Request, oturum: Session = Depends(oturum_al), authorization: str | None = Header(default=None)) -> AdminBaglami:
    bearer = authorization[7:].strip() if authorization and authorization.lower().startswith("bearer ") else None
    token = bearer or request.cookies.get(OTURUM_COOKIE)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin oturumu gerekli.")
    kayit = oturum.query(AdminOturum).filter_by(token_hash=_sha256(token)).first()
    simdi = datetime.now(timezone.utc)
    if not kayit or kayit.iptal_zamani or kayit.sona_erme_zamani <= simdi:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin oturumu gecersiz veya sona ermis.")
    kullanici = oturum.get(AdminKullanici, kayit.kullanici_id)
    if not kullanici or not kullanici.aktif_mi:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin hesabi etkin degil.")
    if request.method not in {"GET", "HEAD", "OPTIONS"} and bearer is None:
        csrf = request.headers.get("X-CSRF-Token")
        if not csrf or not hmac.compare_digest(_sha256(csrf), kayit.csrf_hash):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF dogrulamasi basarisiz.")
    roller = _rolleri_al(oturum, kullanici.id)
    return AdminBaglami(kullanici, kayit, roller, yetkileri_birlestir(set(roller)))


def yetki_gerekli(yetki: Yetki):
    def _bagimlilik(baglam: AdminBaglami = Depends(admin_baglami_al)) -> AdminBaglami:
        if yetki not in baglam.yetkiler:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bu islem icin yetkiniz yok.")
        return baglam
    return _bagimlilik
