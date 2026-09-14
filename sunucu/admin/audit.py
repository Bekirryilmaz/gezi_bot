from __future__ import annotations

import hashlib
import json

from sqlalchemy.orm import Session

from sunucu.veritabani.admin_modelleri import AdminAuditOlayi


def durum_referansi(deger: object | None) -> str | None:
    if deger is None:
        return None
    kodlu = json.dumps(deger, ensure_ascii=True, sort_keys=True, default=str).encode("utf-8")
    return f"sha256:{hashlib.sha256(kodlu).hexdigest()}"


def audit_yaz(oturum: Session, *, aktor_id: str, eylem: str, nesne_turu: str, nesne_id: str, onceki: object | None, yeni: object | None, gerekce: str, istek_id: str, korelasyon_id: str | None = None, meta: dict | None = None) -> AdminAuditOlayi:
    if not gerekce.strip():
        raise ValueError("Kritik admin islemi icin gerekce zorunludur")
    olay = AdminAuditOlayi(
        aktor_id=aktor_id,
        eylem=eylem,
        nesne_turu=nesne_turu,
        nesne_id=str(nesne_id),
        onceki_durum_ref=durum_referansi(onceki),
        yeni_durum_ref=durum_referansi(yeni),
        gerekce=gerekce.strip(),
        istek_id=istek_id,
        korelasyon_id=korelasyon_id or istek_id,
        meta={k: v for k, v in (meta or {}).items() if k not in {"parola", "token", "secret", "csrf"}},
    )
    oturum.add(olay)
    oturum.flush()
    return olay
