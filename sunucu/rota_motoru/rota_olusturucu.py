"""
Rota olusturma orkestratoru.

skorlama.py -> kumeleme.py -> siralama.py zincirini birlestirip iki
senaryoyu yonetir:
  - Senaryo 1 (konaklama belli): kullanici konaklama noktasini biliyor,
    algoritma o noktadan gunlere yayilan bir rota olusturur.
  - Senaryo 2 (konaklama belli degil): once en iyi adaylarin agirlik
    merkezine en yakin/en kaliteli konaklamayi ONERIR, sonra Senaryo 1'i
    o onerilen nokta ile calistirir (kod tekrarini onler).

Sonuc, izlenebilirlik ve paylasilabilir link icin `KullaniciRotasi`
tablosuna kaydedilir (bkz. `_rotayi_kaydet`) -- ama COMMIT etmez, bu
sorumluluk cagiran API uc noktasina (`sunucu/api/rotalar_router.py`) aittir.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from ortak.cografya_araclari import haversine_metre
from ortak.sabitler import AnaKategori
from sunucu.rota_motoru.kumeleme import SkorluYer, agirlik_merkezi_hesapla, gunlere_boluster
from sunucu.rota_motoru.rota_anlatim import konaklama_bolgesi_gerekce_uret, rota_tavsiyesi_uret
from sunucu.rota_motoru.siralama import gun_rotasini_sirala
from sunucu.rota_motoru.skorlama import yer_uygunluk_puani
from sunucu.rota_motoru.veri_tipleri import AdayYer, GunSonucu, RotaDuragiSonucu, RotaSonucu, RotaTercihleri
from sunucu.rota_motoru.zaman_butcesi import ulasim_suresi_tahmini_dk, ziyaret_suresi_tahmini_dk
from sunucu.veritabani.modeller import KullaniciRotasi, Yer
from sunucu.veritabani.sorgular import sehir_yerlerini_getir
from veri.ortak.sehir_ayarlari import bolge_merkezini_bul

# Gunde hedeflenen gezilecek-yer durak sayisi (yeme_icme haric -- o ayrica eklenir).
_HEDEF_GUNLUK_DURAK_SAYISI = 4
# Kumelemeden once havuzda tutulacak aday sayisi = gun_sayisi * hedef * bu carpan.
# Carpan, kumeleme+zaman butcesi budamasi sirasinda secenek birakmak icin > 1.
_ADAY_HAVUZU_CARPANI = 3
# Senaryo 2'de konaklama onerisi icin, agirlik merkezine en yakin kac
# konaklamanin arasindan (kaliteye gore) secim yapilacagi.
_KONAKLAMA_ADAY_SAYISI = 10
# Bir gune yemek durak adayi secerken, gunun cografi merkezine en yakin
# kac restoran arasindan (skora gore) secim yapilacagi.
_YEMEK_ADAY_SAYISI = 5
# Konaklama noktasindan bu mesafeden UZAK yerler aday havuzuna hic girmez.
# Sebep: dokumanlar/kategori_taksonomisi.md'deki varsayilan deneyim puanlari
# ALT KATEGORI bazinda (yer'e ozel degil) verildigi icin, sehrin cok uzak bir
# ilcesindeki bir anit ile merkezdeki bir anit ayni puani alabilir -- mesafe
# filtresi olmadan gunluk rota, tek bir sehir gezisi yerine yanlislikla
# onlarca km'lik il-capinda bir geziye donusebilir.
_MAKSIMUM_ADAY_MESAFESI_METRE = 40_000


class RotaOlusturulamadiHatasi(ValueError):
    """Rota olusturmak icin yeterli veri yoksa (orn. sehirde hic yer/konaklama
    yoksa) firlatilir -- API katmani bunu 422/404 gibi bir HTTP hatasina cevirir."""


def _yer_orm_den_aday_uret(yer: Yer, enlem: float, boylam: float) -> AdayYer:
    ozellikler = yer.ozellikler or {}
    return AdayYer(
        id=yer.id,
        isim=yer.isim,
        ana_kategori=yer.ana_kategori,
        alt_kategori=yer.alt_kategori,
        enlem=enlem,
        boylam=boylam,
        deneyim_puanlari=yer.deneyim_puanlari or {},
        yer_profili=yer.yer_profili or {},
        aktiviteler=yer.aktiviteler or [],
        ortalama_ziyaret_suresi_dk=ozellikler.get("ortalama_ziyaret_suresi_dk"),
        kaynakta_puan_ortalamasi=yer.kaynakta_puan_ortalamasi,
        duygu_skoru_ortalama=yer.duygu_skoru_ortalama,
        kapak_fotografi_url=yer.fotograf_urlleri[0] if yer.fotograf_urlleri else None,
        ilce=yer.ilce,
    )


def _adaylari_getir(oturum: Session, sehir_id: str, ana_kategori: AnaKategori) -> list[AdayYer]:
    yerler_ve_koordinatlar = sehir_yerlerini_getir(oturum, sehir_id, ana_kategoriler=[ana_kategori.value])
    return [_yer_orm_den_aday_uret(yer, enlem, boylam) for yer, enlem, boylam in yerler_ve_koordinatlar]


def _en_iyi_n_adayi_sec(
    adaylar: list[AdayYer],
    tercihler: RotaTercihleri,
    n: int,
    referans_nokta: tuple[float, float] | None = None,
) -> list[SkorluYer]:
    """En yuksek skorlu `n` adayi secer. `referans_nokta` verilmisse
    (Senaryo 1'de konaklama noktasi), `_MAKSIMUM_ADAY_MESAFESI_METRE`'den
    uzak adaylar zorunlu duraklar HARIC havuza hic girmez (bkz. yukaridaki
    sabitin gerekcesi)."""
    if referans_nokta is not None:
        adaylar = [
            aday
            for aday in adaylar
            if aday.id in tercihler.zorunlu_duraklar
            or haversine_metre(referans_nokta[0], referans_nokta[1], aday.enlem, aday.boylam) <= _MAKSIMUM_ADAY_MESAFESI_METRE
        ]

    skorlanmis = [SkorluYer(yer=aday, skor=yer_uygunluk_puani(aday, tercihler)) for aday in adaylar]
    skorlanmis.sort(key=lambda sy: sy.skor.toplam_puan, reverse=True)
    return skorlanmis[:n]


def _gune_yemek_yeri_sec(
    gunluk_yerler: list[SkorluYer],
    yeme_icme_adaylari: list[AdayYer],
    tercihler: RotaTercihleri,
    kullanilmis_idler: set[str],
    varsayilan_merkez: tuple[float, float],
) -> SkorluYer | None:
    """Gunun (gezilecek yer duraklarinin) cografi merkezine en yakin
    restoran/kafe adaylari arasindan en yuksek skorluyu secer -- boylece
    hem 'yakin' hem 'kaliteli/tercihe uygun' bir ogle/aksam yemegi durak
    onerisi eklenmis olur. Aym restoran birden fazla gune eklenmez."""
    uygun_adaylar = [aday for aday in yeme_icme_adaylari if aday.id not in kullanilmis_idler]
    if not uygun_adaylar:
        return None

    gun_merkezi = agirlik_merkezi_hesapla([sy.yer for sy in gunluk_yerler]) if gunluk_yerler else varsayilan_merkez
    uygun_adaylar.sort(key=lambda a: haversine_metre(gun_merkezi[0], gun_merkezi[1], a.enlem, a.boylam))
    en_yakinlar = uygun_adaylar[:_YEMEK_ADAY_SAYISI]

    skorlu_adaylar = [SkorluYer(yer=aday, skor=yer_uygunluk_puani(aday, tercihler)) for aday in en_yakinlar]
    skorlu_adaylar.sort(key=lambda sy: sy.skor.toplam_puan, reverse=True)
    return skorlu_adaylar[0] if skorlu_adaylar else None


def _gun_sonucu_olustur(gun_no: int, siralanmis: list[SkorluYer], baslangic_noktasi: tuple[float, float]) -> GunSonucu:
    duraklar: list[RotaDuragiSonucu] = []
    toplam_mesafe = 0.0
    toplam_sure = 0
    onceki_nokta = baslangic_noktasi

    for sira, skorlu_yer in enumerate(siralanmis, start=1):
        hedef_nokta = (skorlu_yer.yer.enlem, skorlu_yer.yer.boylam)
        mesafe = haversine_metre(onceki_nokta[0], onceki_nokta[1], hedef_nokta[0], hedef_nokta[1])
        ziyaret_suresi = ziyaret_suresi_tahmini_dk(skorlu_yer.yer)
        ulasim_suresi = ulasim_suresi_tahmini_dk(onceki_nokta, hedef_nokta)

        duraklar.append(
            RotaDuragiSonucu(
                yer=skorlu_yer.yer,
                sira=sira,
                onceki_duraktan_mesafe_metre=round(mesafe, 1),
                tahmini_ziyaret_suresi_dk=ziyaret_suresi,
                skor_kirilimi=skorlu_yer.skor.kirilim,
            )
        )
        toplam_mesafe += mesafe
        toplam_sure += ziyaret_suresi + ulasim_suresi
        onceki_nokta = hedef_nokta

    return GunSonucu(gun_no=gun_no, duraklar=duraklar, toplam_mesafe_metre=round(toplam_mesafe, 1), toplam_sure_dakikasi=toplam_sure)


def _rotayi_kaydet(
    oturum: Session,
    sehir_id: str,
    gun_sayisi: int,
    tercihler: RotaTercihleri,
    rota_sonucu: RotaSonucu,
) -> str:
    """Sonucu `KullaniciRotasi` olarak veritabanina yazar (flush eder,
    COMMIT ETMEZ -- bu cagiran API uc noktasinin sorumlulugundadir).
    Donen id, paylasilabilir rota linki icin kullanilir."""
    gunler_json = [
        {
            "gun_no": gun.gun_no,
            "toplam_mesafe_metre": gun.toplam_mesafe_metre,
            "toplam_sure_dakikasi": gun.toplam_sure_dakikasi,
            "duraklar": [
                {
                    "yer_id": durak.yer.id,
                    "sira": durak.sira,
                    "onceki_duraktan_mesafe_metre": durak.onceki_duraktan_mesafe_metre,
                    "tahmini_ziyaret_suresi_dk": durak.tahmini_ziyaret_suresi_dk,
                    "skor_kirilimi": durak.skor_kirilimi,
                }
                for durak in gun.duraklar
            ],
        }
        for gun in rota_sonucu.gunler
    ]
    kayit = KullaniciRotasi(
        sehir_id=sehir_id,
        tercihler={
            "gun_sayisi": gun_sayisi,
            "ilgi_agirliklari": tercihler.ilgi_agirliklari,
            "aktiviteler": tercihler.aktiviteler,
            "zorunlu_duraklar": tercihler.zorunlu_duraklar,
            "ucuz_tercih_et": tercihler.ucuz_tercih_et,
            "sakin_tercih_et": tercihler.sakin_tercih_et,
        },
        gunler=gunler_json,
        konaklama_onerisi_yer_id=rota_sonucu.konaklama_onerisi.id if rota_sonucu.konaklama_onerisi else None,
    )
    oturum.add(kayit)
    oturum.flush()
    return kayit.id


def senaryo_1_rota_olustur(
    oturum: Session,
    sehir_id: str,
    konaklama_noktasi: tuple[float, float],
    gun_sayisi: int,
    tercihler: RotaTercihleri,
    *,
    kaydet: bool = True,
) -> RotaSonucu:
    """Konaklama noktasi BELLI oldugunda kullanilir (Senaryo 1)."""
    gezilecek_adaylar = _adaylari_getir(oturum, sehir_id, AnaKategori.GEZILECEK_YER)
    if not gezilecek_adaylar:
        raise RotaOlusturulamadiHatasi("Bu sehir icin veritabaninda gezilecek yer bulunamadi.")
    yeme_icme_adaylari = _adaylari_getir(oturum, sehir_id, AnaKategori.YEME_ICME)

    havuz_boyutu = gun_sayisi * _HEDEF_GUNLUK_DURAK_SAYISI * _ADAY_HAVUZU_CARPANI
    en_iyi_adaylar = _en_iyi_n_adayi_sec(gezilecek_adaylar, tercihler, havuz_boyutu, referans_nokta=konaklama_noktasi)
    gunlere_bolunmus = gunlere_boluster(en_iyi_adaylar, gun_sayisi, konaklama_noktasi)

    kullanilmis_yeme_icme_idleri: set[str] = set()
    gunler: list[GunSonucu] = []
    for gun_no in range(1, gun_sayisi + 1):
        gunluk_yerler = gunlere_bolunmus.get(gun_no, [])

        yemek_secimi = _gune_yemek_yeri_sec(
            gunluk_yerler, yeme_icme_adaylari, tercihler, kullanilmis_yeme_icme_idleri, konaklama_noktasi
        )
        if yemek_secimi is not None:
            gunluk_yerler = [*gunluk_yerler, yemek_secimi]
            kullanilmis_yeme_icme_idleri.add(yemek_secimi.yer.id)

        siralanmis = gun_rotasini_sirala(gunluk_yerler, konaklama_noktasi)
        gunler.append(_gun_sonucu_olustur(gun_no, siralanmis, konaklama_noktasi))

    rota_sonucu = RotaSonucu(gunler=gunler)
    rota_sonucu.rota_tavsiyesi = rota_tavsiyesi_uret(rota_sonucu, tercihler)
    if kaydet:
        rota_sonucu.id = _rotayi_kaydet(oturum, sehir_id, gun_sayisi, tercihler, rota_sonucu)
    return rota_sonucu


def _en_iyi_konaklamayi_bul(oturum: Session, sehir_id: str, merkez_nokta: tuple[float, float]) -> AdayYer | None:
    konaklama_adaylari = _adaylari_getir(oturum, sehir_id, AnaKategori.KONAKLAMA)
    if not konaklama_adaylari:
        return None

    konaklama_adaylari.sort(key=lambda a: haversine_metre(merkez_nokta[0], merkez_nokta[1], a.enlem, a.boylam))
    en_yakinlar = konaklama_adaylari[:_KONAKLAMA_ADAY_SAYISI]
    en_yakinlar.sort(key=lambda a: a.kaynakta_puan_ortalamasi or 0, reverse=True)
    return en_yakinlar[0]


def senaryo_2_rota_olustur(
    oturum: Session,
    sehir_id: str,
    gun_sayisi: int,
    tercihler: RotaTercihleri,
) -> RotaSonucu:
    """Konaklama noktasi BELLI OLMADIGINDA kullanilir (Senaryo 2): once en
    iyi adaylarin agirlik merkezine en yakin/en kaliteli konaklamayi
    onerir, sonra Senaryo 1'i o noktayla calistirir."""
    gezilecek_adaylar = _adaylari_getir(oturum, sehir_id, AnaKategori.GEZILECEK_YER)
    if not gezilecek_adaylar:
        raise RotaOlusturulamadiHatasi("Bu sehir icin veritabaninda gezilecek yer bulunamadi.")

    havuz_boyutu = gun_sayisi * _HEDEF_GUNLUK_DURAK_SAYISI * _ADAY_HAVUZU_CARPANI
    en_iyi_adaylar = _en_iyi_n_adayi_sec(gezilecek_adaylar, tercihler, havuz_boyutu)
    merkez_nokta = agirlik_merkezi_hesapla([sy.yer for sy in en_iyi_adaylar])

    konaklama_onerisi = _en_iyi_konaklamayi_bul(oturum, sehir_id, merkez_nokta)
    if konaklama_onerisi is None:
        raise RotaOlusturulamadiHatasi("Bu sehir icin veritabaninda konaklama yeri bulunamadi, Senaryo 2 calistirilamiyor.")

    konaklama_noktasi = (konaklama_onerisi.enlem, konaklama_onerisi.boylam)
    # kaydet=False: asil kayit asagida, konaklama_onerisi bilgisiyle BIRLIKTE yapilir.
    rota_sonucu = senaryo_1_rota_olustur(oturum, sehir_id, konaklama_noktasi, gun_sayisi, tercihler, kaydet=False)
    rota_sonucu.konaklama_onerisi = konaklama_onerisi
    rota_sonucu.rota_tavsiyesi = rota_tavsiyesi_uret(rota_sonucu, tercihler)
    rota_sonucu.id = _rotayi_kaydet(oturum, sehir_id, gun_sayisi, tercihler, rota_sonucu)
    return rota_sonucu


def _tercih_varyanti(tercihler: RotaTercihleri, odak_ekseni: str | None, etiket: str) -> tuple[RotaTercihleri, str]:
    """Senaryo 2 alternatifleri icin ilgi agirliklarini hafifce kaydirir."""
    yeni_agirliklar = dict(tercihler.ilgi_agirliklari)
    if odak_ekseni:
        for eksen in list(yeni_agirliklar):
            yeni_agirliklar[eksen] = max(0.05, yeni_agirliklar[eksen] * 0.55)
        yeni_agirliklar[odak_ekseni] = max(yeni_agirliklar.get(odak_ekseni, 0.0), 0.85)
    elif not yeni_agirliklar:
        yeni_agirliklar = {
            "tarihi_kulturel_puani": 0.6,
            "gastronomi_puani": 0.5,
            "doga_macera_puani": 0.5,
        }
    return (
        RotaTercihleri(
            ilgi_agirliklari=yeni_agirliklar,
            aktiviteler=list(tercihler.aktiviteler),
            zorunlu_duraklar=list(tercihler.zorunlu_duraklar),
            ucuz_tercih_et=tercihler.ucuz_tercih_et,
            sakin_tercih_et=tercihler.sakin_tercih_et,
        ),
        etiket,
    )


def senaryo_2_alternatif_rotalar_olustur(
    oturum: Session,
    sehir_id: str,
    gun_sayisi: int,
    tercihler: RotaTercihleri,
    *,
    alternatif_sayisi: int = 3,
) -> list[RotaSonucu]:
    """Konaklama oteli secmeden 2–3 alternatif rota uretir. Her alternatif,
    farkli ilgi agirligi / aday havuzu kaymasi ile gunlere bolunur; konaklama
    noktasi olarak adaylarin agirlik merkezi kullanilir (otel dayatma yok)."""
    gezilecek_adaylar = _adaylari_getir(oturum, sehir_id, AnaKategori.GEZILECEK_YER)
    if not gezilecek_adaylar:
        raise RotaOlusturulamadiHatasi("Bu sehir icin veritabaninda gezilecek yer bulunamadi.")

    varyantlar = [
        _tercih_varyanti(tercihler, None, "Dengeli keşif"),
        _tercih_varyanti(tercihler, "tarihi_kulturel_puani", "Tarih & kültür ağırlıklı"),
        _tercih_varyanti(tercihler, "doga_macera_puani", "Doğa & manzara ağırlıklı"),
    ][: max(2, min(alternatif_sayisi, 3))]

    havuz_boyutu = gun_sayisi * _HEDEF_GUNLUK_DURAK_SAYISI * _ADAY_HAVUZU_CARPANI
    sonuclar: list[RotaSonucu] = []
    kullanilan_yer_setleri: list[frozenset[str]] = []

    for idx, (varyant, etiket) in enumerate(varyantlar):
        skorlu = _en_iyi_n_adayi_sec(gezilecek_adaylar, varyant, havuz_boyutu + idx * 4)
        # Onceki alternatiflerle ayni durak kumesi cikmasin diye hafif kaydir.
        if idx > 0 and skorlu:
            kaydir = min(len(skorlu) - 1, idx * 3)
            skorlu = skorlu[kaydir:] + skorlu[:kaydir]
        merkez = agirlik_merkezi_hesapla([sy.yer for sy in skorlu]) if skorlu else (gezilecek_adaylar[0].enlem, gezilecek_adaylar[0].boylam)
        # Merkezi biraz kaydirarak kumeleme farki yarat (otel dayatma yok).
        merkez = (merkez[0] + idx * 0.008, merkez[1] - idx * 0.006)
        rota = senaryo_1_rota_olustur(oturum, sehir_id, merkez, gun_sayisi, varyant, kaydet=True)
        yer_idler = frozenset(d.yer.id for g in rota.gunler for d in g.duraklar)
        if yer_idler in kullanilan_yer_setleri:
            etiket = f"{etiket} (yakın varyant)"
        kullanilan_yer_setleri.append(yer_idler)
        rota.alternatif_etiketi = etiket
        rota.konaklama_onerisi = None  # otel onerme; bolge sonraki adimda
        rota.rota_tavsiyesi = rota_tavsiyesi_uret(rota, varyant)
        sonuclar.append(rota)
        if len(sonuclar) >= alternatif_sayisi:
            break

    if not sonuclar:
        raise RotaOlusturulamadiHatasi("Alternatif rota uretilemedi.")
    return sonuclar


def _rota_durak_merkezi(rota: RotaSonucu) -> tuple[float, float] | None:
    noktalar = [(d.yer.enlem, d.yer.boylam) for g in rota.gunler for d in g.duraklar]
    if not noktalar:
        return None
    return (
        sum(n[0] for n in noktalar) / len(noktalar),
        sum(n[1] for n in noktalar) / len(noktalar),
    )


def _baskin_ilceyi_bul(rota: RotaSonucu, sehir_anahtari: str) -> str | None:
    from collections import Counter

    sayac: Counter[str] = Counter()
    for gun in rota.gunler:
        for durak in gun.duraklar:
            if durak.yer.ilce:
                sayac[durak.yer.ilce] += 1
    if sayac:
        return sayac.most_common(1)[0][0]

    merkez = _rota_durak_merkezi(rota)
    if merkez is None:
        return None
    try:
        from veri.ortak.sehir_ayarlari import sehir_getir

        ayar = sehir_getir(sehir_anahtari)
    except KeyError:
        return None
    en_yakin = None
    en_yakin_mesafe = float("inf")
    for adi, koordinat in ayar.ilce_merkezleri.items():
        if adi == ayar.anahtar or len(koordinat) < 2:
            continue
        mesafe = haversine_metre(merkez[0], merkez[1], float(koordinat[0]), float(koordinat[1]))
        if mesafe < en_yakin_mesafe:
            en_yakin_mesafe = mesafe
            en_yakin = adi
    return en_yakin


def konaklama_bolgesi_oner(
    oturum: Session,
    sehir_id: str,
    sehir_anahtari: str,
    rota: RotaSonucu,
    tercihler: RotaTercihleri | None = None,
) -> RotaSonucu:
    """Secilen rotanin duraklarina gore konaklama BOLGESI (ilce/bant) onerir;
    istege bagli birkac yakin konaklama tesisini destekleyici listeler."""
    bolge_adi = _baskin_ilceyi_bul(rota, sehir_anahtari)
    merkez = bolge_merkezini_bul(sehir_anahtari, bolge_adi) if bolge_adi else None
    if merkez is None:
        merkez = _rota_durak_merkezi(rota)
    if bolge_adi is None and merkez is not None:
        bolge_adi = _baskin_ilceyi_bul(rota, sehir_anahtari) or "şehir merkezi"

    durak_sayisi = sum(len(g.duraklar) for g in rota.gunler)
    rota.konaklama_bolgesi_adi = bolge_adi
    if bolge_adi:
        rota.konaklama_bolgesi_gerekce = konaklama_bolgesi_gerekce_uret(bolge_adi, durak_sayisi)
    if merkez is not None:
        rota.konaklama_bolgesi_enlem = merkez[0]
        rota.konaklama_bolgesi_boylam = merkez[1]
        yakin_konaklamalar = _adaylari_getir(oturum, sehir_id, AnaKategori.KONAKLAMA)
        yakin_konaklamalar.sort(key=lambda a: haversine_metre(merkez[0], merkez[1], a.enlem, a.boylam))
        rota.ornek_konaklamalar = yakin_konaklamalar[:5]

    rota.rota_tavsiyesi = rota_tavsiyesi_uret(rota, tercihler, konaklama_bolgesi=bolge_adi)
    return rota
