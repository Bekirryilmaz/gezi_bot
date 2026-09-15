from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from sunucu.arama.domain import AramaSonucuTuru, SOMUT_KOSULLAR
from sunucu.arama.semalar import AramaSonucuSemasi
from sunucu.arama.servis import ara
from sunucu.bugun_ne_yapalim.gelistirme_izi import iz_artir, iz_guncelle
from sunucu.karar_motoru.domain import KararAdayi, KararSonucu, KosulDurumu, NedenKodu
from sunucu.karar_motoru.semalar import KararSonucuSemasi
from sunucu.karar_motoru.servis import kararlari_degerlendir
from sunucu.karar_motoru.siralama import oneri_listesini_sec
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
        if gerekce.kod
        in {NedenKodu.TERCIH_DESTEKLENIYOR, NedenKodu.DENEYIM_SINYALI_DESTEKLIYOR}
    )


_AMAC_CUMLESI = {
    "kahve_icmek": "Kahve için uygun bir yer",
    "yemek_yemek": "Yemek için uygun bir yer",
    "tatli_yemek": "Tatlı için uygun bir yer",
    "kahvalti_yapmak": "Kahvaltı için uygun bir yer",
    "tarihi_kulturel_ziyaret": "Tarih ve kültür gezisi için uygun bir yer",
    "eglence": "Eğlence için uygun bir yer",
    "acik_hava": "Açık hava için uygun bir yer",
}

_DENEYIM_ETIKETI = {
    "sohbet": "sohbet",
    "sohbet_uygunlugu": "sohbet",
    "sessiz_ortam": "sakinlik",
    "aile_uygunlugu": "aile",
    "cocuk_uygunlugu": "çocuk",
    "calisma_uygunlugu": "çalışma",
    "manzara": "manzara",
    "kahvalti": "kahvaltı",
    "tatli": "tatlı",
    "wifi": "bağlantı",
    "otopark": "otopark",
    "acik_alan": "açık alan",
}


def _neden_metni(baglam_amac: str | None, karar: KararSonucu) -> str:
    amac_cumle = _AMAC_CUMLESI.get(baglam_amac or "", "Bu ziyaret için uygun bir yer")
    parcalar = [f"{amac_cumle}."]
    dogrulananlar = [
        SOMUT_KOSULLAR[g.ilgili_kosul].etiket
        for g in karar.gerekceler
        if g.kod is NedenKodu.ZORUNLU_KOSUL_DOGRULANDI and g.ilgili_kosul in SOMUT_KOSULLAR
    ]
    if dogrulananlar:
        parcalar.append(f"{', '.join(dogrulananlar)} isteğini yayımlanmış bilgiyle karşılıyor.")
    deneyim_etiketleri: list[str] = []
    for gerekce in karar.gerekceler:
        if gerekce.kod is not NedenKodu.DENEYIM_SINYALI_DESTEKLIYOR:
            continue
        etiket = _DENEYIM_ETIKETI.get(gerekce.ilgili_kosul or "", "")
        if etiket and etiket not in deneyim_etiketleri:
            deneyim_etiketleri.append(etiket)
    if deneyim_etiketleri:
        parcalar.append(
            f"{', '.join(deneyim_etiketleri)} deneyimi açısından destekleyici sinyal var."
        )
    return " ".join(parcalar)


def _fark_metni(aday: _DegerlendirilmisAday, ilk: _DegerlendirilmisAday | None) -> str:
    deneyim = [
        gerekce.ilgili_kosul
        for gerekce in aday.karar.gerekceler
        if gerekce.kod is NedenKodu.DENEYIM_SINYALI_DESTEKLIYOR
    ]
    if deneyim:
        etiketler = [
            _DENEYIM_ETIKETI.get(kod or "", "")
            for kod in deneyim
        ]
        etiketler = [etiket for etiket in etiketler if etiket]
        if etiketler:
            return f"{', '.join(etiketler)} deneyimi açısından destekleyici sinyal var."
        return "Deneyim sinyali bu tercihi destekliyor."
    tercihler = tuple(
        gerekce.ilgili_kosul or ""
        for gerekce in aday.karar.gerekceler
        if gerekce.kod is NedenKodu.TERCIH_DESTEKLENIYOR
    )
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


def kesfet_degerlendir(
    oturum: Session,
    talep: KesfetDegerlendirmeTalebi,
    *,
    request_id: str,
    giris_kanali: str = "kesfet",
) -> KesfetDegerlendirmeCevabi:
    baglam = talep.baglam.domaine(giris_kanali)
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
        # Arama sirasi amac claim'ini bilmez. Ilk 50'yi kesmek, alfabetik olarak
        # daha sonra gelen ama yayimlanmis amac claim'i olan yerleri Karar
        # Motoruna hic ulastirmiyordu. Bu ic cagri, kamusal API sayfa boyutu
        # degil; sehir/kategori kapsamindaki aday havuzudur.
        limit=2_000,
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
            durum="insufficient" if arama_cevabi.degerlendirilemeyen_aday_sayisi else "empty",
            secenekler=[],
            kimlik_eslesmeleri=kimlik_eslesmeleri,
            kullanilan_baglam={"sorgu": talep.sorgu, "amac": baglam.amac, **arama_cevabi.uygulanan_filtreler.model_dump()},
            sinirlama_nedeni="Bu aramada ve seçtiğin bölgede uygunluğunu doğrulayabildiğimiz yer bulamadık.",
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
    kararlar, trace, karar_aday_listesi = kararlari_degerlendir(
        oturum, baglam, yer_idleri, request_id=request_id
    )
    karar_adaylari = {aday.yer_id: aday for aday in karar_aday_listesi}
    iz_guncelle(oturum, decision_evaluated_count=len(kararlar))
    iz_artir(oturum, "unknown_critical_count", sum(
        karar.uygunluk is KosulDurumu.DEGERLENDIRILEMIYOR for karar in kararlar
    ))
    iz_artir(oturum, "hard_constraint_rejected_count", sum(
        any(g.kod is NedenKodu.ZORUNLU_KOSUL_SAGLANMIYOR for g in karar.kritik_engeller)
        for karar in kararlar
    ))
    karar_by_id = {karar.yer_id: karar for karar in kararlar if karar.yer_id}
    degerlendirilen: list[_DegerlendirilmisAday] = []
    uygun_karar_adaylari: list[KararAdayi] = []
    for sonuc in yer_sonuclari:
        assert sonuc.yer is not None
        karar = karar_by_id.get(sonuc.yer.place_id)
        if karar is None or karar.uygunluk is not KosulDurumu.UYGUN:
            continue
        karar_adayi = karar_adaylari.get(sonuc.yer.place_id)
        if karar_adayi is None:
            continue
        imza = (
            *_desteklenen_tercihler(karar),
            sonuc.alt_kategori or sonuc.ana_kategori or "",
            sonuc.cografya.ilce_id or "",
        )
        degerlendirilen.append(_DegerlendirilmisAday(sonuc, karar, imza))
        uygun_karar_adaylari.append(karar_adayi)
    secilen_adaylar = oneri_listesini_sec(baglam, uygun_karar_adaylari, talep.hedef_sayi)
    degerlenen_by_id = {
        aday.arama.yer.place_id: aday for aday in degerlendirilen if aday.arama.yer is not None
    }
    secilen = [
        degerlenen_by_id[aday.yer_id]
        for aday in secilen_adaylar
        if aday.yer_id in degerlenen_by_id
    ]
    secenekler: list[KesfetSecenegiSemasi] = []
    ilk = secilen[0] if secilen else None
    for aday in secilen:
        assert aday.arama.yer is not None
        secenekler.append(
            KesfetSecenegiSemasi(
                yer=aday.arama.yer,
                cografya=aday.arama.cografya,
                ana_kategori=aday.arama.ana_kategori,
                alt_kategori=aday.arama.alt_kategori,
                neden_bu=_neden_metni(baglam.amac, aday.karar),
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
        sinir = "Yerler bulundu; ancak isteğine uygun olup olmadıklarını henüz doğrulayamadık."
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
