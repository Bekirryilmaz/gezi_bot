from datetime import datetime, timedelta, timezone

import pytest

from sunucu.bilgi.domain import BilgiDurumu, HakDurumu
from sunucu.yayin.domain import KullanimTuru, YayinGirdisi, YayinNedeni, YayinUygunlukDurumu, yayin_uygunlugunu_degerlendir


def _girdi(**degisiklikler) -> YayinGirdisi:
    taban = dict(canonical_gecerli=True, sube_gecerli=True)
    taban.update(degisiklikler)
    return YayinGirdisi(**taban)


def test_yayinlanabilir_ve_sinirli_durumlar_boolean_degil_anlamli_sonuc_uretir():
    assert yayin_uygunlugunu_degerlendir(_girdi(), KullanimTuru.DETAY).durum is YayinUygunlukDurumu.YAYINLANABILIR
    sonuc = yayin_uygunlugunu_degerlendir(_girdi(sinirli=True), KullanimTuru.DETAY)
    assert sonuc.durum is YayinUygunlukDurumu.SINIRLI_YAYINLANABILIR
    assert sonuc.nedenler == (YayinNedeni.SINIRLI_POLITIKA,)


@pytest.mark.parametrize(
    ("degisiklik", "neden"),
    [
        ({"canonical_gecerli": False}, YayinNedeni.CANONICAL_GECERSIZ),
        ({"sube_gecerli": False}, YayinNedeni.SUBE_GECERSIZ),
        ({"iddia_aktif": False}, YayinNedeni.IDDIA_PASIF),
        ({"surum_gecerli": False}, YayinNedeni.SURUM_GECERSIZ),
        ({"hak_durumu": HakDurumu.YASAK}, YayinNedeni.HAK_UYGUN_DEGIL),
        ({"bilgi_durumu": BilgiDurumu.CELISKILI}, YayinNedeni.CELISKILI),
        ({"geri_cekilmis": True}, YayinNedeni.GERI_CEKILMIS),
    ],
)
def test_hard_gate_yayinlanamaz(degisiklik, neden):
    sonuc = yayin_uygunlugunu_degerlendir(_girdi(**degisiklik), KullanimTuru.DETAY)
    assert sonuc.durum is YayinUygunlukDurumu.YAYINLANAMAZ
    assert neden in sonuc.nedenler
    assert not sonuc.kamusal_kullanilabilir


@pytest.mark.parametrize("degisiklik", [{"hak_durumu": HakDurumu.BILINMIYOR}, {"bilgi_durumu": BilgiDurumu.BILINMIYOR}, {"bilgi_durumu": BilgiDurumu.ESKIMIS}])
def test_bilinmeyen_ve_eskimis_yeniden_dogrulama_ister(degisiklik):
    assert yayin_uygunlugunu_degerlendir(_girdi(**degisiklik), KullanimTuru.ARAMA).durum is YayinUygunlukDurumu.YENIDEN_DOGRULAMA_GEREKLI


def test_zaman_ve_kullanim_kapsami_gate():
    simdi = datetime.now(timezone.utc)
    sonuc = yayin_uygunlugunu_degerlendir(_girdi(gecerlilik_bitisi=simdi - timedelta(seconds=1), izinli_kullanimlar=frozenset({KullanimTuru.DETAY})), KullanimTuru.ROTA_ADAYI, simdi=simdi)
    assert set(sonuc.nedenler) == {YayinNedeni.ZAMAN_KAPSAMI_DISINDA, YayinNedeni.KULLANIM_IZNI_YOK}
