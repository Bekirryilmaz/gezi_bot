"""Tek gunluk kamusal rota ve salt-okunur tarihsel rota uclari."""

from __future__ import annotations

import hashlib
from threading import Lock

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from sunucu.api.semalar import (
    GunPlani,
    GunlukPlanCevap,
    GunlukPlanTalebi,
    KonaklamaBolgesiOnerisi,
    RotaCevap,
    RotaDuragi,
    RotaTalebi,
    RotaTercihleri as RotaTercihleriSemasi,
    SabitRotaCevap,
    YerOzet,
)
from sunucu.rota_motoru.rota_olusturucu import (
    RotaOlusturulamadiHatasi,
    gunluk_rota_olustur,
)
from sunucu.rota_motoru.veri_tipleri import AdayYer, RotaSonucu, RotaTercihleri as RotaTercihleriMotoru
from sunucu.veritabani.baglanti import oturum_al
from sunucu.veritabani.modeller import KullaniciRotasi, SabitRota, Sehir
from sunucu.veritabani.sorgular import yer_ve_koordinat_getir
from veri.ortak.sehir_ayarlari import sehir_anahtarini_isme_gore_bul, sehir_getir

yonlendirici = APIRouter(tags=["rotalar"])
_IDEMPOTENCY_KAYITLARI: dict[str, tuple[str, GunlukPlanCevap]] = {}
_IDEMPOTENCY_KILIDI = Lock()
_IDEMPOTENCY_KAPASITESI = 1_000


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
        kapak_fotografi_url=aday.kapak_fotografi_url,
        ticari_bildirim=("sponsorlu" if aday.ozellik_isaretli("sponsorlu_mekan") else None),
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


def _gunluk_plan_cevabini_olustur(sehir_anahtari: str, rota_sonucu: RotaSonucu) -> GunlukPlanCevap:
    if len(rota_sonucu.gunler) != 1:
        raise RuntimeError("Kamusal gunluk plan motoru tam olarak bir gun dondurmelidir.")
    gun = rota_sonucu.gunler[0]
    return GunlukPlanCevap(
        id=rota_sonucu.id or "",
        sehir_anahtari=sehir_anahtari,
        duraklar=[
            RotaDuragi(
                yer=_aday_yerden_yer_ozet(durak.yer),
                sira=durak.sira,
                onceki_duraktan_mesafe_metre=durak.onceki_duraktan_mesafe_metre,
                tahmini_ziyaret_suresi_dk=durak.tahmini_ziyaret_suresi_dk,
            )
            for durak in gun.duraklar
        ],
        toplam_mesafe_metre=gun.toplam_mesafe_metre,
        toplam_sure_dakikasi=gun.toplam_sure_dakikasi,
        rota_tavsiyesi=rota_sonucu.rota_tavsiyesi,
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


@yonlendirici.post(
    "/v1/gunluk-planlar",
    response_model=GunlukPlanCevap,
    status_code=status.HTTP_201_CREATED,
)
def gunluk_plan_olustur(
    talep: GunlukPlanTalebi,
    yanit: Response,
    idempotency_anahtari: str = Header(
        ...,
        alias="Idempotency-Key",
        min_length=8,
        max_length=128,
        pattern=r"^[A-Za-z0-9._:-]+$",
    ),
    oturum: Session = Depends(oturum_al),
) -> GunlukPlanCevap:
    """Konaklama veya cok-gun alani olmadan tek gunluk MVP plani uretir."""
    istek_izi = hashlib.sha256(talep.model_dump_json().encode("utf-8")).hexdigest()
    with _IDEMPOTENCY_KILIDI:
        onceki = _IDEMPOTENCY_KAYITLARI.get(idempotency_anahtari)
    if onceki:
        onceki_iz, onceki_cevap = onceki
        if onceki_iz != istek_izi:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Idempotency-Key farkli bir istek govdesiyle daha once kullanildi.",
            )
        yanit.status_code = status.HTTP_200_OK
        yanit.headers["X-Idempotency-Key"] = idempotency_anahtari
        return onceki_cevap

    _, sehir = _sehir_bul(oturum, talep.sehir_anahtari)
    try:
        rota_sonucu = gunluk_rota_olustur(oturum, sehir.id, _tercihleri_donustur(talep.tercihler))
    except RotaOlusturulamadiHatasi as hata:
        oturum.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(hata)) from hata

    cevap = _gunluk_plan_cevabini_olustur(talep.sehir_anahtari, rota_sonucu)
    oturum.commit()
    with _IDEMPOTENCY_KILIDI:
        if len(_IDEMPOTENCY_KAYITLARI) >= _IDEMPOTENCY_KAPASITESI:
            _IDEMPOTENCY_KAYITLARI.pop(next(iter(_IDEMPOTENCY_KAYITLARI)))
        _IDEMPOTENCY_KAYITLARI[idempotency_anahtari] = (istek_izi, cevap)
    yanit.headers["X-Idempotency-Key"] = idempotency_anahtari
    return cevap


def _legacy_kapali() -> None:
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="Cok gunlu rota ve konaklama akisi kullanımdan kaldirildi; /v1/gunluk-planlar kullanin.",
    )


@yonlendirici.post("/rotalar/olustur", include_in_schema=False)
def rota_olustur(_talep: RotaTalebi) -> None:
    _legacy_kapali()


@yonlendirici.post("/rotalar/olustur-alternatifler", include_in_schema=False)
def rota_alternatifleri_olustur(_talep: RotaTalebi) -> None:
    _legacy_kapali()


@yonlendirici.post("/rotalar/{rota_id}/konaklama-bolgesi-oner", include_in_schema=False)
def rota_konaklama_bolgesi_oner(_rota_id: str) -> None:
    _legacy_kapali()


@yonlendirici.get("/rotalar/{rota_id}", response_model=RotaCevap, include_in_schema=False)
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


@yonlendirici.get("/sabit-rotalar", response_model=list[SabitRotaCevap], include_in_schema=False)
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
