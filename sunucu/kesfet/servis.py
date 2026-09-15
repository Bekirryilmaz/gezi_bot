from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from sunucu.arama.domain import AramaSonucuTuru, SOMUT_KOSULLAR
from sunucu.arama.semalar import AramaSonucuSemasi
from sunucu.arama.servis import ara
from sunucu.karar_motoru.domain import KararSonucu, KosulDurumu, NedenKodu
from sunucu.karar_motoru.semalar import KararSonucuSemasi
from sunucu.karar_motoru.servis import kararlari_degerlendir
from sunucu.kesfet.semalar import (
    KesfetDegerlendirmeCevabi,
    KesfetDegerlendirmeTalebi,
    KesfetSecenegiSemasi,
)


@dataclass(frozen=True)
class _DegerlendirilmisAday:
    arama: AramaSonucuSemasi
    karar: KararSonucu
    imza: tuple[str, ...]


def _desteklenen_tercihler(karar: KararSonucu) -> tuple[str, ...]:
    return tuple(
        gerekce.ilgili_kosul or ""
        for gerekce in karar.gerekceler
        if gerekce.kod is NedenKodu.TERCIH_DESTEKLENIYOR
    )


def _fark_metni(aday: _DegerlendirilmisAday, ilk: _DegerlendirilmisAday | None) -> str:
    tercihler = _desteklenen_tercihler(aday.karar)
    if tercihler:
        etiketler = [SOMUT_KOSULLAR[kod].etiket for kod in tercihler if kod in SOMUT_KOSULLAR]
        if etiketler:
            return f"{', '.join(etiketler)} tercihini yayımlanmış bilgiyle destekliyor."
    if ilk is not None and aday.arama.cografya.ilce_id != ilk.arama.cografya.ilce_id:
        return f"{aday.arama.cografya.ilce_ismi or aday.arama.cografya.sehir_ismi} coğrafyasında bir seçenek."
    if ilk is not None and aday.arama.alt_kategori != ilk.arama.alt_kategori:
        tur = (aday.arama.alt_kategori or aday.arama.ana_kategori or "mekân").replace("_", " ")
        return f"{tur.capitalize()} türüyle ilk seçenekten ayrılıyor."
    tur = (aday.arama.alt_kategori or aday.arama.ana_kategori or "mekân").replace("_", " ")
    return f"{tur.capitalize()} kimliği ve konumu yayımlanmış bir seçenek."


def _secim_yap(adaylar: list[_DegerlendirilmisAday], hedef: int) -> list[_DegerlendirilmisAday]:
    """Önce farklı destek imzalarını korur; yeni bir puan veya yeniden sıralama üretmez."""
    secilen: list[_DegerlendirilmisAday] = []
    gorulen: set[tuple[str, ...]] = set()
    for aday in adaylar:
        if aday.imza in gorulen:
            continue
        secilen.append(aday)
        gorulen.add(aday.imza)
        if len(secilen) == hedef:
            return secilen
    for aday in adaylar:
        if aday in secilen:
            continue
        secilen.append(aday)
        if len(secilen) == hedef:
            break
    return secilen


def kesfet_degerlendir(
    oturum: Session,
    talep: KesfetDegerlendirmeTalebi,
    *,
    request_id: str,
) -> KesfetDegerlendirmeCevabi:
    baglam = talep.baglam.domaine("kesfet")
    zorunlu_kodlari = [k.kod for k in baglam.zorunlu_kosullar if k.kod in SOMUT_KOSULLAR]
    tercih_kodlari = [t.kod for t in baglam.tercihler if t.kod in SOMUT_KOSULLAR]
    arama_cevabi = ara(
        oturum,
        q=talep.sorgu,
        sehir_degeri=baglam.cografi_baglam.sehir,
        ilce_id=talep.arama.ilce_id,
        tur=talep.arama.tur,
        zorunlu_kosullar=zorunlu_kodlari,
        tercihler=tercih_kodlari,
        limit=50,
        cursor=None,
    )
    haric = set(talep.haric_yerler) | set(baglam.reddedilen_yerler)
    yer_sonuclari = [
        sonuc
        for sonuc in arama_cevabi.sonuclar
        if sonuc.yer is not None and sonuc.yer.place_id not in haric and sonuc.yer.canonical_id not in haric
    ]
    kimlik_eslesmeleri = [
        sonuc.yer
        for sonuc in yer_sonuclari
        if sonuc.sonuc_turu is AramaSonucuTuru.YER_KIMLIGI and sonuc.yer is not None
    ][:5]
    if not yer_sonuclari:
        return KesfetDegerlendirmeCevabi(
            durum="empty",
            secenekler=[],
            kimlik_eslesmeleri=kimlik_eslesmeleri,
            kullanilan_baglam={"sorgu": talep.sorgu, "amac": baglam.amac, **arama_cevabi.uygulanan_filtreler.model_dump()},
            sinirlama_nedeni="Bu arama ve coğrafyada yayımlanmış aday bulamadık; koşulları kendiliğimizden genişletmedik.",
            degerlendirilemeyen_aday_sayisi=arama_cevabi.degerlendirilemeyen_aday_sayisi,
        )

    # Bir yer adıyla bulunabilirlik öneri değildir. Amaç yoksa kimlik eşleşmeleri ayrı verilir.
    if not baglam.amac:
        return KesfetDegerlendirmeCevabi(
            durum="insufficient",
            secenekler=[],
            kimlik_eslesmeleri=kimlik_eslesmeleri,
            kullanilan_baglam={"sorgu": talep.sorgu, "amac": None, **arama_cevabi.uygulanan_filtreler.model_dump()},
            sinirlama_nedeni="Bir yer önerebilmemiz için ziyaret amacını bilmemiz gerekiyor. Adla bulunan yerleri yine de açabilirsin.",
            degerlendirilemeyen_aday_sayisi=arama_cevabi.degerlendirilemeyen_aday_sayisi,
        )

    yer_idleri = [sonuc.yer.place_id for sonuc in yer_sonuclari if sonuc.yer]
    kararlar, trace = kararlari_degerlendir(oturum, baglam, yer_idleri, request_id=request_id)
    karar_by_id = {karar.yer_id: karar for karar in kararlar if karar.yer_id}
    degerlendirilen: list[_DegerlendirilmisAday] = []
    for sonuc in yer_sonuclari:
        assert sonuc.yer is not None
        karar = karar_by_id.get(sonuc.yer.place_id)
        if karar is None or karar.uygunluk is not KosulDurumu.UYGUN:
            continue
        imza = (
            *_desteklenen_tercihler(karar),
            sonuc.alt_kategori or sonuc.ana_kategori or "",
            sonuc.cografya.ilce_id or "",
        )
        degerlendirilen.append(_DegerlendirilmisAday(sonuc, karar, imza))
    secilen = _secim_yap(degerlendirilen, talep.hedef_sayi)
    secenekler: list[KesfetSecenegiSemasi] = []
    ilk = secilen[0] if secilen else None
    for aday in secilen:
        assert aday.arama.yer is not None
        neden = next(
            (g.mesaj for g in aday.karar.gerekceler if g.kod is not NedenKodu.YAYIN_UYGUN),
            "Bu ziyaret amacı için yayımlanmış karar bilgisiyle değerlendirildi.",
        )
        secenekler.append(
            KesfetSecenegiSemasi(
                yer=aday.arama.yer,
                cografya=aday.arama.cografya,
                ana_kategori=aday.arama.ana_kategori,
                alt_kategori=aday.arama.alt_kategori,
                neden_bu=neden,
                anlamli_fark=_fark_metni(aday, None if aday is ilk else ilk),
                karar_sonucu=KararSonucuSemasi.domainden(aday.karar),
            )
        )
    bilinmeyen_sayisi = (
        arama_cevabi.degerlendirilemeyen_aday_sayisi
        + sum(1 for karar in kararlar if karar.uygunluk is KosulDurumu.DEGERLENDIRILEMIYOR)
    )
    durum = "success" if len(secenekler) >= 3 else "insufficient"
    if secenekler:
        sinir = (
            f"Yalnız {len(secenekler)} destekli seçenek bulduk; sayıyı doldurmak için zayıf aday eklemedik."
            if len(secenekler) < 3
            else f"İlk kümeyi {len(secenekler)} destekli seçenekle sınırladık; daha fazla sonuç açık isteğinle değerlendirilir."
        )
    else:
        sinir = "Adaylar bulundu; ancak bu amaç veya kritik koşullar için yeterli yayımlanmış karar bilgisi yok."
    return KesfetDegerlendirmeCevabi(
        durum=durum,
        secenekler=secenekler,
        kimlik_eslesmeleri=kimlik_eslesmeleri,
        kullanilan_baglam={"sorgu": talep.sorgu, "amac": baglam.amac, **arama_cevabi.uygulanan_filtreler.model_dump()},
        sinirlama_nedeni=sinir,
        degerlendirilemeyen_aday_sayisi=bilinmeyen_sayisi,
        daha_fazla_var_mi=len(degerlendirilen) > len(secilen),
        trace_reference=trace,
    )

