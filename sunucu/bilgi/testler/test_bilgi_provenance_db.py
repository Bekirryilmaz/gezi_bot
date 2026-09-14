from datetime import datetime, timezone

from sqlalchemy.orm import Session

from sunucu.veritabani.baglanti import motor
from sunucu.veritabani.bilgi_modelleri import Gozlem, Iddia, IddiaSurumu, KanitBaglantisi, VeriBatch
from sunucu.veritabani.kimlik_modelleri import Sube


def test_claim_evidence_provenance_ve_zamanlar_dbde_ayri():
    baglanti = motor.connect(); islem = baglanti.begin(); oturum = Session(bind=baglanti)
    try:
        sube = oturum.query(Sube).first(); assert sube
        simdi = datetime.now(timezone.utc)
        batch = VeriBatch(kaynak="test", kosu_anahtari="pytest-provenance", baslama_zamani=simdi)
        oturum.add(batch); oturum.flush()
        gozlem = Gozlem(veri_batch_id=batch.id, kaynak="test", kaynak_kayit_id="1", cekilme_zamani=simdi, kaynakta_gozlemlenme_zamani=None, icerik_hash="a" * 64)
        oturum.add(gozlem); oturum.flush()
        iddia = Iddia(sube_id=sube.id, aile="otopark", kapsam={"alan": "giris"})
        oturum.add(iddia); oturum.flush()
        surum = IddiaSurumu(iddia_id=iddia.id, surum_no=1, deger={"var": True}, bilgi_durumu="biliniyor", yayin_durumu="taslak")
        oturum.add(surum); oturum.flush()
        oturum.add(KanitBaglantisi(iddia_surumu_id=surum.id, gozlem_id=gozlem.id, rol="destekleyen")); oturum.flush()
        assert surum.iddia_id == iddia.id and gozlem.veri_batch_id == batch.id
        assert gozlem.kaynakta_gozlemlenme_zamani is None
        assert gozlem.cekilme_zamani is not None
    finally:
        oturum.close(); islem.rollback(); baglanti.close()

