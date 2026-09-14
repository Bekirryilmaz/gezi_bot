from types import SimpleNamespace

from sqlalchemy.orm import Session

from sunucu.veritabani.aktarim.calistir import _batch_sagla
from sunucu.veritabani.baglanti import motor


def test_ayni_dosya_batchi_idempotent():
    dosya = SimpleNamespace(
        name="samsun_2026-09-15.jsonl",
        read_bytes=lambda: b'{"ornek":true}\n',
        stat=lambda: SimpleNamespace(st_mtime=1_789_416_000),
    )
    baglanti = motor.connect(); islem = baglanti.begin(); oturum = Session(bind=baglanti)
    try:
        ilk = _batch_sagla(oturum, dosya)
        ikinci = _batch_sagla(oturum, dosya)
        assert ilk.id == ikinci.id
    finally:
        oturum.close(); islem.rollback(); baglanti.close()
