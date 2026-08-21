"""
Bolge Profili ("sehir/ilce tanitim duygu analizi") cikarma mantigi.

Girdi: veri/duygu_analizi/pipeline_calistir.py'nin urettigi IslenmisYorum
kayitlari icinden, `kaynak_yer_id` alani "bolge:<sehir_anahtari>:<slug>"
bicimindeki (yani Eksi Sozluk'un bolge-geneli, bkz. eksi_sozluk_toplayici.py)
kayitlar. Cikti: her bolge (sehir merkezi + her ilce) icin
veri/ortak/bolge_profili_modeli.py::BolgeProfili.

Tasarim felsefesi yer_profili_cikarici.py ile AYNIDIR: anlasilir/aciklanabilir
kalmak icin kara-kutu bir model yerine anahtar-kelime tabanli konu_analizi.py
ciktisi (konu_duygulari) agregre edilir. Az veri olan bolgeler (orn. Eksi
Sozluk'te hic entry'si olmayan kucuk bir ilce) icin skor `None` birakilir --
uydurma bir izlenim verilmez.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from ortak.sabitler import DuyguEtiketi, VeriKaynagi
from veri.ortak.bolge_profili_modeli import BolgeKonuOzeti, BolgeProfili
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.ortak.yorum_modeli import IslenmisYorum

# yer_profili_cikarici.py::_AZ_VERI_ESIGI ile ayni ruhta: bunun altinda kalan
# yorum sayisiyla genel bir duygu skoru/etiketi hesaplamak yerine
# "bilgi_yetersiz" (None) birakilir.
_AZ_VERI_ESIGI = 3
# Ortalama duygu skorunun "olumlu"/"olumsuz" sayilabilmesi icin esik --
# anlatim_uretici.py::_genel_acilis_cumlesi'ndeki esikle AYNI tutulur ki
# ayni skor her iki yerde de ayni sekilde yorumlanmis olsun.
_DUYGU_ESIGI = 0.3
# Bir bolge icin en fazla kac on-plana-cikan konu raporlanacagi.
_ON_PLANA_CIKAN_KONU_ADEDI = 5


def yorumlari_bolgelere_bagla(islenmis_yorumlar: list[IslenmisYorum]) -> dict[str, list[IslenmisYorum]]:
    """`kaynak_yer_id` alani "bolge:<sehir_anahtari>:<slug>" bicimindeki
    (Eksi Sozluk'un bolge-geneli, bkz. eksi_sozluk_toplayici.py) yorumlari,
    TAM `kaynak_yer_id` degerine gore gruplar. Diger tum yorumlar (belirli
    bir yere ait olanlar) burada YOK SAYILIR -- onlar yer_profili_cikarici.py
    tarafindan islenir."""
    sonuc: dict[str, list[IslenmisYorum]] = defaultdict(list)
    for yorum in islenmis_yorumlar:
        if yorum.kaynak == VeriKaynagi.EKSI_SOZLUK and yorum.kaynak_yer_id.startswith("bolge:"):
            sonuc[yorum.kaynak_yer_id].append(yorum)
    return dict(sonuc)


def _bolge_anahtarini_ayristir(bolge_kaynak_yer_id: str) -> tuple[str, str]:
    """"bolge:<sehir_anahtari>:<slug>" -> (sehir_anahtari, slug). Slug,
    sehir_ayarlari.py::bolge_slug ile uretilmis oldugu icin, orijinal
    (okunur) bolge adina donusturmek icin `SehirAyari.bolge_adini_slugtan_
    bul` kullanilmalidir (bkz. bolge_profili_olustur)."""
    _on_ek, sehir_anahtari, slug = bolge_kaynak_yer_id.split(":", 2)
    return sehir_anahtari, slug


def _on_plana_cikan_konulari_bul(yorumlar: list[IslenmisYorum]) -> list[BolgeKonuOzeti]:
    konu_sayaci: Counter[str] = Counter()
    konu_duygu_dagilimi: dict[str, Counter] = defaultdict(Counter)
    for yorum in yorumlar:
        for konu_duygusu in yorum.konu_duygulari:
            konu_sayaci[konu_duygusu.konu] += 1
            konu_duygu_dagilimi[konu_duygusu.konu][konu_duygusu.duygu_etiketi] += 1

    sonuc: list[BolgeKonuOzeti] = []
    for konu, bahsedilme_sayisi in konu_sayaci.most_common(_ON_PLANA_CIKAN_KONU_ADEDI):
        baskin_duygu = konu_duygu_dagilimi[konu].most_common(1)[0][0]
        sonuc.append(BolgeKonuOzeti(konu=konu, duygu_etiketi=baskin_duygu, bahsedilme_sayisi=bahsedilme_sayisi))
    return sonuc


def _genel_duygu_hesapla(yorumlar: list[IslenmisYorum]) -> tuple[float | None, DuyguEtiketi | None]:
    if len(yorumlar) < _AZ_VERI_ESIGI:
        return None, None
    ortalama = sum(yorum.duygu_skoru for yorum in yorumlar) / len(yorumlar)
    if ortalama >= _DUYGU_ESIGI:
        etiket = DuyguEtiketi.OLUMLU
    elif ortalama <= -_DUYGU_ESIGI:
        etiket = DuyguEtiketi.OLUMSUZ
    else:
        etiket = DuyguEtiketi.NOTR
    return round(ortalama, 3), etiket


def bolge_profili_olustur(bolge_kaynak_yer_id: str, yorumlar: list[IslenmisYorum]) -> BolgeProfili:
    sehir_anahtari, slug = _bolge_anahtarini_ayristir(bolge_kaynak_yer_id)
    sehir = sehir_getir(sehir_anahtari)
    bolge_adi = sehir.bolge_adini_slugtan_bul(slug)
    ilce_mi = bolge_adi != sehir.anahtar

    genel_duygu_skoru, genel_duygu_etiketi = _genel_duygu_hesapla(yorumlar)

    return BolgeProfili(
        sehir_anahtari=sehir_anahtari,
        bolge_adi=bolge_adi,
        ilce_mi=ilce_mi,
        genel_duygu_skoru=genel_duygu_skoru,
        genel_duygu_etiketi=genel_duygu_etiketi,
        on_plana_cikan_konular=_on_plana_cikan_konulari_bul(yorumlar),
        kullanilan_yorum_sayisi=len(yorumlar),
    )


def bolge_profillerini_olustur(islenmis_yorumlar: list[IslenmisYorum]) -> list[BolgeProfili]:
    """Ana giris noktasi: TUM islenmis yorumlardan, bulunan HER bolge icin
    (duygu_ozeti henuz doldurulmamis) bir BolgeProfili uretir. `duygu_ozeti`,
    veri/duygu_analizi/bolge_profili_pipeline_calistir.py tarafindan
    anlatim_uretici.py::bolge_tanitim_metni_uret ile doldurulur."""
    bolgesel_yorumlar = yorumlari_bolgelere_bagla(islenmis_yorumlar)
    return [bolge_profili_olustur(anahtar, yorumlar) for anahtar, yorumlar in bolgesel_yorumlar.items()]
