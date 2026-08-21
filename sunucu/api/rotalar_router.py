"""
Rota olusturma/getirme uc noktalari.

`POST /rotalar/olustur`, `talep`deki konaklama bilgisine gore hangi
senaryonun calisacagina karar verir:
  - `konaklama_yer_id` / `konaklama_enlem`+`boylam` / `konaklama_bolge_adi`
    verilmisse -> Senaryo 1 (konaklama bolgesi belli)
  - hicbiri verilmemisse -> eski Senaryo 2 (otel onerili, geriye uyumluluk)

Yeni Senaryo 2 akisi:
  - `POST /rotalar/olustur-alternatifler` -> 2-3 rota (otel secmeden)
  - `POST /rotalar/{id}/konaklama-bolgesi-oner` -> bolge + tavsiye metni
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from sunucu.api.semalar import (
    AlternatifRotalarCevap,
    GunPlani,
    KonaklamaBolgesiOnerisi,
    RotaCevap,
    RotaDuragi,
    RotaTalebi,
    RotaTercihleri as RotaTercihleriSemasi,
    SabitRotaCevap,
    YerOzet,
)
from sunucu.rota_motoru.rota_anlatim import rota_tavsiyesi_uret
from sunucu.rota_motoru.rota_olusturucu import (
    RotaOlusturulamadiHatasi,
    konaklama_bolgesi_oner,
    senaryo_1_rota_olustur,
    senaryo_2_alternatif_rotalar_olustur,
    senaryo_2_rota_olustur,
)
from sunucu.rota_motoru.veri_tipleri import AdayYer, RotaSonucu, RotaTercihleri as RotaTercihleriMotoru
from sunucu.veritabani.baglanti import oturum_al
from sunucu.veritabani.modeller import KullaniciRotasi, SabitRota, Sehir
from sunucu.veritabani.sorgular import yer_ve_koordinat_getir
from veri.ortak.sehir_ayarlari import bolge_merkezini_bul, sehir_anahtarini_isme_gore_bul, sehir_getir

yonlendirici = APIRouter(tags=["rotalar"])


def _tercihleri_donustur(tercihler: RotaTercihleriSemasi) -> RotaTercihleriMotoru:
    """API semasindaki (Pydantic/Enum) tercihleri, rota motorunun
    beklendigi saf Python tiplerine (str/float/bool) cevirir."""
    return RotaTercihleriMotoru(
        ilgi_agirliklari={eksen.value: agirlik for eksen, agirlik in tercihler.ilgi_agirliklari.items()},
        aktiviteler=[aktivite.value for aktivite in tercihler.aktiviteler],
        zorunlu_duraklar=list(tercihler.zorunlu_duraklar),
        ucuz_tercih_et=tercihler.ucuz_tercih_et,
        sakin_tercih_et=tercihler.sakin_tercih_et,
    )


def _aday_yerden_yer_ozet(aday: AdayYer) -> YerOzet:
    return YerOzet(
        id=aday.id,
        isim=aday.isim,
        ana_kategori=aday.ana_kategori,
        alt_kategori=aday.alt_kategori,
        ilce=aday.ilce,
        enlem=aday.enlem,
        boylam=aday.boylam,
        kaynakta_puan_ortalamasi=aday.kaynakta_puan_ortalamasi,
        duygu_skoru_ortalama=aday.duygu_skoru_ortalama,
        kapak_fotografi_url=aday.kapak_fotografi_url,
    )


def _rota_cevabini_olustur(sehir_anahtari: str, gun_sayisi: int, rota_sonucu: RotaSonucu) -> RotaCevap:
    gunler = [
        GunPlani(
            gun_no=gun.gun_no,
            duraklar=[
                RotaDuragi(
                    yer=_aday_yerden_yer_ozet(durak.yer),
                    sira=durak.sira,
                    onceki_duraktan_mesafe_metre=durak.onceki_duraktan_mesafe_metre,
                    tahmini_ziyaret_suresi_dk=durak.tahmini_ziyaret_suresi_dk,
                    skor_kirilimi=durak.skor_kirilimi,
                )
                for durak in gun.duraklar
            ],
            toplam_mesafe_metre=gun.toplam_mesafe_metre,
            toplam_sure_dakikasi=gun.toplam_sure_dakikasi,
        )
        for gun in rota_sonucu.gunler
    ]
    konaklama_onerisi = _aday_yerden_yer_ozet(rota_sonucu.konaklama_onerisi) if rota_sonucu.konaklama_onerisi else None
    bolge_onerisi = None
    if rota_sonucu.konaklama_bolgesi_adi:
        bolge_onerisi = KonaklamaBolgesiOnerisi(
            bolge_adi=rota_sonucu.konaklama_bolgesi_adi,
            gerekce=rota_sonucu.konaklama_bolgesi_gerekce,
            enlem=rota_sonucu.konaklama_bolgesi_enlem,
            boylam=rota_sonucu.konaklama_bolgesi_boylam,
            ornek_konaklamalar=[_aday_yerden_yer_ozet(k) for k in rota_sonucu.ornek_konaklamalar],
        )
    return RotaCevap(
        id=rota_sonucu.id or "",
        sehir_anahtari=sehir_anahtari,
        gun_sayisi=gun_sayisi,
        gunler=gunler,
        konaklama_onerisi=konaklama_onerisi,
        rota_tavsiyesi=rota_sonucu.rota_tavsiyesi,
        konaklama_bolgesi_onerisi=bolge_onerisi,
        alternatif_etiketi=rota_sonucu.alternatif_etiketi,
    )


def _sehir_bul(oturum: Session, sehir_anahtari: str) -> tuple[object, Sehir]:
    try:
        sehir_ayari = sehir_getir(sehir_anahtari)
    except KeyError as hata:
        raise HTTPException(status_code=404, detail=str(hata)) from hata

    sehir = oturum.query(Sehir).filter(Sehir.isim == sehir_ayari.isim).first()
    if sehir is None:
        raise HTTPException(
            status_code=404,
            detail=f"'{sehir_ayari.isim}' henuz veritabanina aktarilmamis. "
            f"Once 'python -m sunucu.veritabani.aktarim.calistir --sehir {sehir_anahtari}' calistir.",
        )
    return sehir_ayari, sehir


@yonlendirici.post("/rotalar/olustur", response_model=RotaCevap)
def rota_olustur(talep: RotaTalebi, oturum: Session = Depends(oturum_al)) -> RotaCevap:
    """Kullanici tercihlerine gore kisisellestirilmis bir rota olusturur.
    dokumanlar/kategori_taksonomisi.md ve rota_motoru/README.md'deki
    Senaryo 1 / Senaryo 2 ayrimini uygular."""
    _, sehir = _sehir_bul(oturum, talep.sehir_anahtari)
    tercihler = _tercihleri_donustur(talep.tercihler)

    try:
        if talep.konaklama_yer_id:
            sonuc = yer_ve_koordinat_getir(oturum, talep.konaklama_yer_id)
            if sonuc is None:
                raise HTTPException(status_code=404, detail=f"'{talep.konaklama_yer_id}' id'li konaklama yeri bulunamadi.")
            _, enlem, boylam = sonuc
            rota_sonucu = senaryo_1_rota_olustur(oturum, sehir.id, (enlem, boylam), talep.gun_sayisi, tercihler)
        elif talep.konaklama_enlem is not None and talep.konaklama_boylam is not None:
            rota_sonucu = senaryo_1_rota_olustur(
                oturum, sehir.id, (talep.konaklama_enlem, talep.konaklama_boylam), talep.gun_sayisi, tercihler
            )
        elif talep.konaklama_bolge_adi:
            merkez = bolge_merkezini_bul(talep.sehir_anahtari, talep.konaklama_bolge_adi)
            if merkez is None:
                raise HTTPException(
                    status_code=422,
                    detail=f"'{talep.konaklama_bolge_adi}' icin bilinen bir bolge merkezi yok.",
                )
            rota_sonucu = senaryo_1_rota_olustur(oturum, sehir.id, merkez, talep.gun_sayisi, tercihler)
            rota_sonucu.konaklama_bolgesi_adi = talep.konaklama_bolge_adi
            rota_sonucu.konaklama_bolgesi_enlem = merkez[0]
            rota_sonucu.konaklama_bolgesi_boylam = merkez[1]
            rota_sonucu.rota_tavsiyesi = rota_tavsiyesi_uret(
                rota_sonucu, tercihler, konaklama_bolgesi=talep.konaklama_bolge_adi
            )
        else:
            rota_sonucu = senaryo_2_rota_olustur(oturum, sehir.id, talep.gun_sayisi, tercihler)
    except RotaOlusturulamadiHatasi as hata:
        oturum.rollback()
        raise HTTPException(status_code=422, detail=str(hata)) from hata

    oturum.commit()
    return _rota_cevabini_olustur(talep.sehir_anahtari, talep.gun_sayisi, rota_sonucu)


@yonlendirici.post("/rotalar/olustur-alternatifler", response_model=AlternatifRotalarCevap)
def rota_alternatifleri_olustur(talep: RotaTalebi, oturum: Session = Depends(oturum_al)) -> AlternatifRotalarCevap:
    """Senaryo 2: konaklama oteli secmeden 2–3 alternatif rota uretir."""
    _, sehir = _sehir_bul(oturum, talep.sehir_anahtari)
    tercihler = _tercihleri_donustur(talep.tercihler)
    try:
        sonuclar = senaryo_2_alternatif_rotalar_olustur(
            oturum,
            sehir.id,
            talep.gun_sayisi,
            tercihler,
            alternatif_sayisi=talep.alternatif_sayisi,
        )
    except RotaOlusturulamadiHatasi as hata:
        oturum.rollback()
        raise HTTPException(status_code=422, detail=str(hata)) from hata

    oturum.commit()
    return AlternatifRotalarCevap(
        alternatifler=[_rota_cevabini_olustur(talep.sehir_anahtari, talep.gun_sayisi, r) for r in sonuclar]
    )


@yonlendirici.post("/rotalar/{rota_id}/konaklama-bolgesi-oner", response_model=RotaCevap)
def rota_konaklama_bolgesi_oner(rota_id: str, oturum: Session = Depends(oturum_al)) -> RotaCevap:
    """Secilen rotaya gore konaklama bolgesi + rota tavsiyesi uretir."""
    kayit = oturum.get(KullaniciRotasi, rota_id)
    if kayit is None:
        raise HTTPException(status_code=404, detail=f"'{rota_id}' id'li rota bulunamadi.")

    sehir = oturum.get(Sehir, kayit.sehir_id)
    sehir_anahtari = (sehir_anahtarini_isme_gore_bul(sehir.isim) if sehir else None) or ""
    if sehir is None:
        raise HTTPException(status_code=404, detail="Rota sehrine ulasilamadi.")

    # Kayitli JSON'dan RotaSonucu'ya yakin bir yapi kur (sadece bolge hesabi icin).
    from sunucu.rota_motoru.veri_tipleri import GunSonucu, RotaDuragiSonucu

    gunler_sonuc: list[GunSonucu] = []
    for gun_verisi in kayit.gunler:
        duraklar: list[RotaDuragiSonucu] = []
        for durak_verisi in gun_verisi.get("duraklar", []):
            sonuc = yer_ve_koordinat_getir(oturum, durak_verisi["yer_id"])
            if sonuc is None:
                continue
            yer, enlem, boylam = sonuc
            aday = AdayYer(
                id=yer.id,
                isim=yer.isim,
                ana_kategori=yer.ana_kategori,
                alt_kategori=yer.alt_kategori,
                enlem=enlem,
                boylam=boylam,
                ilce=yer.ilce,
                kaynakta_puan_ortalamasi=yer.kaynakta_puan_ortalamasi,
                duygu_skoru_ortalama=yer.duygu_skoru_ortalama,
                kapak_fotografi_url=yer.fotograf_urlleri[0] if yer.fotograf_urlleri else None,
            )
            duraklar.append(
                RotaDuragiSonucu(
                    yer=aday,
                    sira=durak_verisi["sira"],
                    onceki_duraktan_mesafe_metre=durak_verisi["onceki_duraktan_mesafe_metre"],
                    tahmini_ziyaret_suresi_dk=durak_verisi["tahmini_ziyaret_suresi_dk"],
                    skor_kirilimi=durak_verisi.get("skor_kirilimi", {}),
                )
            )
        gunler_sonuc.append(
            GunSonucu(
                gun_no=gun_verisi["gun_no"],
                duraklar=duraklar,
                toplam_mesafe_metre=gun_verisi.get("toplam_mesafe_metre", 0.0),
                toplam_sure_dakikasi=gun_verisi.get("toplam_sure_dakikasi", 0),
            )
        )

    rota_sonucu = RotaSonucu(gunler=gunler_sonuc, id=kayit.id)
    tercihler_ham = kayit.tercihler or {}
    tercihler = RotaTercihleriMotoru(
        ilgi_agirliklari=tercihler_ham.get("ilgi_agirliklari", {}),
        aktiviteler=tercihler_ham.get("aktiviteler", []),
        zorunlu_duraklar=tercihler_ham.get("zorunlu_duraklar", []),
        ucuz_tercih_et=bool(tercihler_ham.get("ucuz_tercih_et", False)),
        sakin_tercih_et=bool(tercihler_ham.get("sakin_tercih_et", False)),
    )
    rota_sonucu = konaklama_bolgesi_oner(oturum, sehir.id, sehir_anahtari, rota_sonucu, tercihler)
    gun_sayisi = tercihler_ham.get("gun_sayisi", len(gunler_sonuc))
    return _rota_cevabini_olustur(sehir_anahtari, gun_sayisi, rota_sonucu)


@yonlendirici.get("/rotalar/{rota_id}", response_model=RotaCevap)
def rota_getir(rota_id: str, oturum: Session = Depends(oturum_al)) -> RotaCevap:
    """Daha once olusturulmus (paylasilabilir linkli) bir rotayi getirir.
    Duraklarin GUNCEL yer bilgileri (isim, kaynak puani vb.) veritabanindan
    tazelenir; mesafe/sure/skor kirilimi gibi rotaya OZGU bilgiler ise
    olusturma anindaki haliyle (KullaniciRotasi.gunler) korunur."""
    kayit = oturum.get(KullaniciRotasi, rota_id)
    if kayit is None:
        raise HTTPException(status_code=404, detail=f"'{rota_id}' id'li rota bulunamadi.")

    sehir = oturum.get(Sehir, kayit.sehir_id)
    sehir_anahtari = (sehir_anahtarini_isme_gore_bul(sehir.isim) if sehir else None) or ""

    gunler: list[GunPlani] = []
    for gun_verisi in kayit.gunler:
        duraklar: list[RotaDuragi] = []
        for durak_verisi in gun_verisi.get("duraklar", []):
            sonuc = yer_ve_koordinat_getir(oturum, durak_verisi["yer_id"])
            if sonuc is None:
                continue  # yer sonradan silinmis olabilir -- rota gecmisi bozulmasin diye atlanir
            yer, enlem, boylam = sonuc
            duraklar.append(
                RotaDuragi(
                    yer=YerOzet.yerden_olustur(yer, enlem, boylam),
                    sira=durak_verisi["sira"],
                    onceki_duraktan_mesafe_metre=durak_verisi["onceki_duraktan_mesafe_metre"],
                    tahmini_ziyaret_suresi_dk=durak_verisi["tahmini_ziyaret_suresi_dk"],
                    skor_kirilimi=durak_verisi.get("skor_kirilimi", {}),
                )
            )
        gunler.append(
            GunPlani(
                gun_no=gun_verisi["gun_no"],
                duraklar=duraklar,
                toplam_mesafe_metre=gun_verisi.get("toplam_mesafe_metre", 0.0),
                toplam_sure_dakikasi=gun_verisi.get("toplam_sure_dakikasi", 0),
            )
        )

    konaklama_onerisi = None
    if kayit.konaklama_onerisi_yer_id:
        sonuc = yer_ve_koordinat_getir(oturum, kayit.konaklama_onerisi_yer_id)
        if sonuc is not None:
            yer, enlem, boylam = sonuc
            konaklama_onerisi = YerOzet.yerden_olustur(yer, enlem, boylam)

    return RotaCevap(
        id=kayit.id,
        sehir_anahtari=sehir_anahtari,
        gun_sayisi=kayit.tercihler.get("gun_sayisi", len(gunler)),
        gunler=gunler,
        konaklama_onerisi=konaklama_onerisi,
    )


@yonlendirici.get("/sabit-rotalar", response_model=list[SabitRotaCevap])
def sabit_rotalari_listele(
    bolge: str | None = Query(default=None, description="Orn. 'Karadeniz' -- verilmezse tum bolgeler donulur"),
    oturum: Session = Depends(oturum_al),
) -> list[SabitRotaCevap]:
    """Elle kuratorlugu yapilan hazir rotalari listeler (orn. Karya/Likya
    Yolu). Bunlar `sehir_id`'ye degil `bolge`'ye bagli oldugu icin (birden
    fazla sehiri kapsayabilirler) sehirden bagimsiz bir uc noktadir."""
    sorgu = oturum.query(SabitRota)
    if bolge:
        sorgu = sorgu.filter(SabitRota.bolge == bolge)
    return [SabitRotaCevap.yerden_olustur(sabit_rota) for sabit_rota in sorgu.order_by(SabitRota.isim).all()]
