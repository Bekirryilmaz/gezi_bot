from sunucu.arama.domain import SOMUT_KOSULLAR, kosul_durumu
from sunucu.arama.normalizasyon import turkce_arama_normalize
from sunucu.karar_motoru.domain import KosulDurumu


def test_turkce_i_ve_diacritic_normalizasyonu():
    assert {turkce_arama_normalize(x) for x in ("İLKADIM", "ilkadım", "Ilkadim")} == {"ilkadim"}
    assert turkce_arama_normalize("  Kahve Dünyası!!! ") == "kahve dunyasi"
    assert turkce_arama_normalize("ŞĞÜÖÇ") == "sguoc"


def test_hard_kosul_unknown_true_veya_false_degil():
    tanim = SOMUT_KOSULLAR["otopark"]
    assert kosul_durumu(tanim, None, kullanilabilir=False) is KosulDurumu.DEGERLENDIRILEMIYOR
    assert kosul_durumu(tanim, {"var": True}, kullanilabilir=True) is KosulDurumu.UYGUN
    assert kosul_durumu(tanim, {"var": False}, kullanilabilir=True) is KosulDurumu.UYGUN_DEGIL
