"""
Kaynaklar arasi ayni fiziksel yeri tekillestiren esleme (deduplication) betigi.

Problem: ayni fiziksel yer (orn. "Amazon Koyu") OpenStreetMap'te, Google
Maps'te VE TripAdvisor'da 3 AYRI ham kayit (veri/ortak/yer_modeli.py::Yer)
olarak elimize gecer. Bu betik bu kayitlari tespit edip TEK bir
veri/ortak/birlesik_yer_modeli.py::BirlesikYer kaydina indirger; boylece
veritabanina 3 kez ayni yer yazilmaz, puanlar/ozellikler birlesir ve rota
algoritmasi tek bir tutarli katalog uzerinden calisir.

Esleme mantigi (kural tabanli, ML/embedding GEREKTIRMEZ -- anlasilir ve
gozle denetlenebilir kalmasi icin bilinçli tercih):

1. Iki kaydin AYNI YER olmasi icin UCU KOSUL da saglanmali:
   a) Ana kategorileri AYNI olmali (bir restoranla bir tarihi alan, konumlari
      cakissa bile ASLA birlestirilmez -- orn. bir kale icindeki kafe).
   b) Aralarindaki cografi mesafe belirli bir esigin (varsayilan 150 metre)
      ALTINDA olmali (haversine formulu ile hesaplanir).
   c) Isimleri arasindaki bulanik (fuzzy) benzerlik belirli bir esigin
      (varsayilan 82/100) USTUNDE olmali (rapidfuzz ile).
2. Ikili eslesmeler bulundugunda, "Birlesik-Kume" (union-find) veri yapisiyla
   ZINCIRLEME eslesmeler de yakalanir: A-B eslesirse ve B-C eslesirse, A/B/C
   ayni kumede sayilir (A-C dogrudan karsilastirilmamis olsa bile).
3. Performans: N^2 karsilastirma yerine, yerler ~500m'lik cografi
   "izgara (grid)" hucrelerine gruplanir; sadece komsu hucrelerdeki
   adaylarla karsilastirma yapilir. Bu, sehir sayisi arttikca (Karadeniz
   genislemesi) olcekli kalmasini saglar.
4. Bir kumedeki (ayni yerin farkli kaynaklardaki kopyalarinin) alanlari
   KAYNAK ONCELIK SIRASINA gore birlestirilir (bkz. KAYNAK_ONCELIGI):
   Google Maps ve TripAdvisor gibi insan-kuratorlu kaynaklar isim/adres/
   telefon icin, OSM ise genis kapsamli temel veri icin tercih edilir.

Calistirma (repo kokunden):
    python -m veri.esleme.eslestirici --sehir samsun
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from rapidfuzz import fuzz

from ortak.sabitler import VeriKaynagi
from veri.ortak.birlesik_yer_modeli import BirlesikYer, KaynakReferansi
from ortak.cografya_araclari import haversine_metre
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_yaz
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir, turkce_kucuk_harf
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.ortak.veri_yukleyiciler import tum_ham_yerleri_yukle
from veri.ortak.yer_modeli import OzellikSeti, Yer
from ortak.esleme_politikasi import EslemeSonucu, eslemeyi_degerlendir

# Alanlari birlestirirken hangi kaynagin once tercih edilecegi (basdan sona
# oncelik sirasi). Google Maps/TripAdvisor genelde daha temiz/guncel isim,
# adres, telefon bilgisi tasir; OSM en genis kapsamli TEMEL veridir ama
# metaveri (telefon, web sitesi) siklikla eksiktir.
KAYNAK_ONCELIGI: list[VeriKaynagi] = [
    VeriKaynagi.GOOGLE_MAPS,
    VeriKaynagi.BOOKING_COM,
    VeriKaynagi.TRIPADVISOR,
    VeriKaynagi.OPENSTREETMAP,
]

VARSAYILAN_MESAFE_ESIGI_METRE = 150.0
# NOT: Esik degeri, rapidfuzz.fuzz.WRatio kullanilarak sececildi (bkz.
# _isim_benzerligi). Basit "token_sort_ratio" denendiginde, bir kaynagin
# isme aciklayici ek kelimeler eklemesi (orn. OSM'de "Amazon Koyu" iken
# Google Maps'te "Amazon Koyu Tabiat Parki") skoru gercekci olmayan sekilde
# dusuruyordu (~63/100); WRatio bu senaryoda dogru sonuc verirken (~90/100)
# gercekten FARKLI iki yeri (orn. "Amazon Koyu" ile "Liman Restoran") hala
# net sekilde ayirt edebiliyor (~40/100).
VARSAYILAN_ISIM_BENZERLIK_ESIGI = 80.0

# Cografi izgara hucre boyu (derece). ~0.005 derece ~ 500-550m -- mesafe
# esiginden (150m) belirgin sekilde buyuk tutuluyor ki hucre sinirina yakin
# duşen ciftler komsu hucre taramasiyla kacirilmasin.
_IZGARA_HUCRE_BOYU = 0.005


def _isim_benzerligi(isim1: str, isim2: str) -> float:
    """0-100 arasi bulanik metin benzerligi. rapidfuzz.fuzz.WRatio
    kullanilir cunku bir kaynagin isme aciklayici ek kelimeler eklemesi
    durumunda (orn. 'Amazon Koyu' ile 'Amazon Koyu Tabiat Parki') diger
    basit yontemlerden (orn. token_sort_ratio) daha gercekci/yuksek bir
    benzerlik skoru uretir, ayni zamanda gercekten alakasiz iki ismi de
    (orn. 'Amazon Koyu' ile 'Liman Restoran') net sekilde ayirt edebilir."""
    return fuzz.WRatio(turkce_kucuk_harf(isim1.strip()), turkce_kucuk_harf(isim2.strip()))


def _ayni_yer_mi(
    yer1: Yer,
    yer2: Yer,
    mesafe_esigi_metre: float,
    isim_benzerlik_esigi: float,
) -> bool:
    mesafe = haversine_metre(yer1.enlem, yer1.boylam, yer2.enlem, yer2.boylam)
    isim = _isim_benzerligi(yer1.isim, yer2.isim)
    if mesafe > mesafe_esigi_metre or isim < isim_benzerlik_esigi:
        return False
    sonuc = eslemeyi_degerlendir(
        ayni_kaynak=yer1.kaynak == yer2.kaynak,
        ayni_kategori=yer1.ana_kategori == yer2.ana_kategori,
        isim_benzerligi=isim,
        mesafe_metre=mesafe,
        telefon_eslesiyor=bool(yer1.telefon and yer1.telefon == yer2.telefon),
        adres_eslesiyor=bool(yer1.adres and yer1.adres == yer2.adres),
    )
    return sonuc.sonuc is EslemeSonucu.OTOMATIK_KABUL


class _BirlesikKumeler:
    """Basit "union-find" (disjoint-set) veri yapisi. Zincirleme eslesmeleri
    (A-B eslesir, B-C eslesir -> A/B/C ayni kume) verimli sekilde yakalar."""

    def __init__(self, eleman_sayisi: int) -> None:
        self._ebeveyn = list(range(eleman_sayisi))
        self._uyeler = {i: {i} for i in range(eleman_sayisi)}

    def bul(self, x: int) -> int:
        while self._ebeveyn[x] != x:
            self._ebeveyn[x] = self._ebeveyn[self._ebeveyn[x]]  # yol sikistirma
            x = self._ebeveyn[x]
        return x

    def birlestir(self, x: int, y: int) -> None:
        kok_x, kok_y = self.bul(x), self.bul(y)
        if kok_x != kok_y:
            self._ebeveyn[kok_y] = kok_x
            self._uyeler[kok_x].update(self._uyeler.pop(kok_y))

    def uyeler(self, x: int) -> set[int]:
        return set(self._uyeler[self.bul(x)])


def _izgara_anahtari(enlem: float, boylam: float) -> tuple[int, int]:
    return (int(enlem // _IZGARA_HUCRE_BOYU), int(boylam // _IZGARA_HUCRE_BOYU))


def _komsu_izgara_anahtarlari(anahtar: tuple[int, int]) -> list[tuple[int, int]]:
    er, ar = anahtar
    return [(er + de, ar + da) for de in (-1, 0, 1) for da in (-1, 0, 1)]


def _tum_ham_yerleri_yukle(sehir_anahtari: str) -> list[Yer]:
    """veri/ortak/veri_yukleyiciler.py'deki paylasilan yukleyiciyi kullanip
    kaynak-bazli sozlugu tek bir duz listeye acar (esleme kaynak ayrimi
    yapmadan TUM kayitlar arasinda calisir)."""
    kaynak_bazli = tum_ham_yerleri_yukle(sehir_anahtari)
    tum_yerler: list[Yer] = []
    for kaynak, yerler in kaynak_bazli.items():
        print(f"[BILGI] {kaynak.value}: {len(yerler)} yer okundu.")
        tum_yerler.extend(yerler)
    return tum_yerler


def _puanlari_birlestir(kume: list[Yer]) -> tuple[float | None, int | None]:
    """Kumedeki kaynaklarin puanlarini, yorum SAYISIYLA agirlikli ortalama
    alarak birlestirir (100 yorumlu 4.5 puan, 3 yorumlu 5.0 puandan daha
    'guvenilir' sayilmali). Hicbir kaynakta yorum sayisi yoksa duz ortalama
    kullanilir."""
    agirlikli_toplam = 0.0
    toplam_agirlik = 0
    duz_puanlar: list[float] = []

    for yer in kume:
        if yer.kaynakta_puan_ortalamasi is None:
            continue
        duz_puanlar.append(yer.kaynakta_puan_ortalamasi)
        if yer.kaynakta_puan_sayisi:
            agirlikli_toplam += yer.kaynakta_puan_ortalamasi * yer.kaynakta_puan_sayisi
            toplam_agirlik += yer.kaynakta_puan_sayisi

    if toplam_agirlik > 0:
        puan_ortalamasi = round(agirlikli_toplam / toplam_agirlik, 2)
    elif duz_puanlar:
        puan_ortalamasi = round(sum(duz_puanlar) / len(duz_puanlar), 2)
    else:
        puan_ortalamasi = None

    puan_sayisi_toplami = sum(yer.kaynakta_puan_sayisi or 0 for yer in kume) or None
    return puan_ortalamasi, puan_sayisi_toplami


def _ozellikleri_birlestir(kume_oncelik_sirali: list[Yer]) -> OzellikSeti:
    """OzellikSeti'nin her alani icin, oncelik sirasindaki ilk NON-NULL
    degeri alir (orn. OSM'de ucretsiz_mi bilgisi varsa ama Google Maps'te
    yoksa, OSM'ninki kullanilir -- oncelik sirasi sadece IKI kaynak da ayni
    alani doldurmussa devreye girer)."""
    birlesik = OzellikSeti()
    for alan_adi in OzellikSeti.model_fields:
        for yer in kume_oncelik_sirali:
            deger = getattr(yer.ozellikler, alan_adi)
            if deger is not None:
                setattr(birlesik, alan_adi, deger)
                break
    return birlesik


def _ilk_dolu_deger(kume_oncelik_sirali: list[Yer], alan_adi: str) -> object | None:
    for yer in kume_oncelik_sirali:
        deger = getattr(yer, alan_adi)
        if deger:
            return deger
    return None


def _kumeyi_birlestir(kume: list[Yer], sehir_isim: str) -> BirlesikYer:
    oncelik_sirasi = {kaynak: i for i, kaynak in enumerate(KAYNAK_ONCELIGI)}
    kume_oncelik_sirali = sorted(kume, key=lambda yer: oncelik_sirasi.get(yer.kaynak, len(KAYNAK_ONCELIGI)))

    isim = _ilk_dolu_deger(kume_oncelik_sirali, "isim") or kume[0].isim
    ilk = kume_oncelik_sirali[0]

    ortalama_enlem = sum(yer.enlem for yer in kume) / len(kume)
    ortalama_boylam = sum(yer.boylam for yer in kume) / len(kume)

    fotograf_urlleri: list[str] = []
    for yer in kume_oncelik_sirali:
        for url in yer.fotograf_urlleri:
            if url not in fotograf_urlleri:
                fotograf_urlleri.append(url)

    aktiviteler = sorted({aktivite for yer in kume for aktivite in yer.aktiviteler}, key=lambda a: a.value)

    puan_ortalamasi, puan_sayisi = _puanlari_birlestir(kume)

    kaynaklar = [
        KaynakReferansi(
            kaynak=yer.kaynak,
            kaynak_id=yer.kaynak_id,
            kaynak_url=yer.kaynak_url,
            cekilme_zamani=yer.cekilme_zamani,
            kaynakta_gozlemlenme_zamani=yer.kaynakta_gozlemlenme_zamani,
            olay_zamani=yer.olay_zamani,
            kaynakta_puan_ortalamasi=yer.kaynakta_puan_ortalamasi,
            kaynakta_puan_sayisi=yer.kaynakta_puan_sayisi,
        )
        for yer in kume
    ]

    return BirlesikYer(
        isim=str(isim),
        ana_kategori=ilk.ana_kategori,
        alt_kategori=ilk.alt_kategori,
        sehir=sehir_isim,
        ilce=_ilk_dolu_deger(kume_oncelik_sirali, "ilce"),
        adres=_ilk_dolu_deger(kume_oncelik_sirali, "adres"),
        aciklama=_ilk_dolu_deger(kume_oncelik_sirali, "aciklama"),
        telefon=_ilk_dolu_deger(kume_oncelik_sirali, "telefon"),
        web_sitesi=_ilk_dolu_deger(kume_oncelik_sirali, "web_sitesi"),
        enlem=ortalama_enlem,
        boylam=ortalama_boylam,
        ozellikler=_ozellikleri_birlestir(kume_oncelik_sirali),
        aktiviteler=aktiviteler,
        fotograf_urlleri=fotograf_urlleri,
        kaynakta_puan_ortalamasi=puan_ortalamasi,
        kaynakta_puan_sayisi=puan_sayisi,
        kaynaklar=kaynaklar,
    )


def calistir(
    sehir_anahtari: str,
    mesafe_esigi_metre: float = VARSAYILAN_MESAFE_ESIGI_METRE,
    isim_benzerlik_esigi: float = VARSAYILAN_ISIM_BENZERLIK_ESIGI,
) -> list[BirlesikYer]:
    sehir = sehir_getir(sehir_anahtari)

    tum_yerler = _tum_ham_yerleri_yukle(sehir_anahtari)
    if not tum_yerler:
        print(f"[UYARI] '{sehir.isim}' icin hicbir kaynaktan ham Yer verisi bulunamadi. Once toplayicilari calistir.")
        return []
    print(f"[BILGI] Toplam {len(tum_yerler)} ham yer kaydi okundu, esleme basliyor...")

    # Cografi izgaraya gore grupla -- sadece komsu hucrelerdeki adaylarla
    # karsilastirma yapilacak (N^2 yerine yaklasik N*ortalama_hucre_yogunlugu).
    izgara: dict[tuple[int, int], list[int]] = defaultdict(list)
    for i, yer in enumerate(tum_yerler):
        izgara[_izgara_anahtari(yer.enlem, yer.boylam)].append(i)

    kumeler = _BirlesikKumeler(len(tum_yerler))
    karsilastirma_sayisi = 0
    eslesme_sayisi = 0

    for i, yer in enumerate(tum_yerler):
        anahtar = _izgara_anahtari(yer.enlem, yer.boylam)
        adaylar: set[int] = set()
        for komsu_anahtar in _komsu_izgara_anahtarlari(anahtar):
            adaylar.update(izgara.get(komsu_anahtar, []))

        for j in adaylar:
            if j <= i:
                continue  # her cifti bir kez karsilastir
            karsilastirma_sayisi += 1
            if _ayni_yer_mi(yer, tum_yerler[j], mesafe_esigi_metre, isim_benzerlik_esigi):
                # Complete-link kapisi: A-B ve B-C eslesmesi, A-C de guclu
                # degilse union-find zinciriyle kalici kume yaratamaz.
                guvenli = all(
                    _ayni_yer_mi(tum_yerler[a], tum_yerler[b], mesafe_esigi_metre, isim_benzerlik_esigi)
                    for a in kumeler.uyeler(i)
                    for b in kumeler.uyeler(j)
                )
                if guvenli:
                    kumeler.birlestir(i, j)
                    eslesme_sayisi += 1

    print(f"[BILGI] {karsilastirma_sayisi} ikili karsilastirma yapildi, {eslesme_sayisi} eslesme bulundu.")

    kume_gruplari: dict[int, list[int]] = defaultdict(list)
    for i in range(len(tum_yerler)):
        kume_gruplari[kumeler.bul(i)].append(i)

    birlesik_yerler: list[BirlesikYer] = []
    coklu_kaynakli_sayisi = 0
    for indeksler in kume_gruplari.values():
        kume = [tum_yerler[i] for i in indeksler]
        try:
            birlesik = _kumeyi_birlestir(kume, sehir.isim)
        except Exception as hata:
            isimler = ", ".join(y.isim for y in kume)
            print(f"[UYARI] Kume birlestirilemedi ({isimler}): {hata}")
            continue
        birlesik_yerler.append(birlesik)
        if birlesik.kac_kaynaktan_dogrulandi > 1:
            coklu_kaynakli_sayisi += 1

    print(
        f"[BILGI] Sonuc: {len(tum_yerler)} ham kayit -> {len(birlesik_yerler)} tekil yer "
        f"({coklu_kaynakli_sayisi} tanesi birden fazla kaynaktan dogrulandi)."
    )

    cikti_dosyasi = (
        Path(__file__).resolve().parents[1] / "cikti" / "islenmis" / "birlesik_yerler"
        / f"{sehir.anahtar}_{bugunun_tarihi_dosya_adi()}.jsonl"
    )
    jsonl_yaz(cikti_dosyasi, birlesik_yerler)
    print(f"[BILGI] Birlesik yerler yazildi: {cikti_dosyasi}")

    _coklu_kaynakli_ornekleri_raporla(birlesik_yerler, sehir.anahtar)

    return birlesik_yerler


def _coklu_kaynakli_ornekleri_raporla(birlesik_yerler: list[BirlesikYer], sehir_anahtari: str, ornek_sayisi: int = 15) -> None:
    """Elle goz atip esleme kalitesini dogrulaman icin, birden fazla
    kaynaktan gelen bazi ornek eslesmeleri okunabilir bir Turkce rapora
    yazar. (Eksik/aykiri veri odakli GENEL kalite raporu ayri bir betikte
    -- veri/kalite_kontrol/ -- ele alinacak; bu rapor SADECE eslemenin
    dogrulugunu gozle kontrol etmek icindir.)"""
    coklu_kaynakli = [y for y in birlesik_yerler if y.kac_kaynaktan_dogrulandi > 1]
    if not coklu_kaynakli:
        print("[BILGI] Birden fazla kaynaktan dogrulanan yer bulunamadi (rapor olusturulmadi).")
        return

    rapor_dosyasi = (
        Path(__file__).resolve().parents[1] / "cikti" / "raporlar" / f"esleme_{sehir_anahtari}_{bugunun_tarihi_dosya_adi()}.md"
    )
    rapor_dosyasi.parent.mkdir(parents=True, exist_ok=True)

    satirlar = [
        f"# Esleme Raporu - {sehir_anahtari}",
        "",
        f"Toplam {len(birlesik_yerler)} tekil yerden {len(coklu_kaynakli)} tanesi birden fazla kaynaktan dogrulandi.",
        "",
        "Asagidaki liste, esleme mantiginin DOGRU calistigini gozle kontrol etmen icindir. ",
        "Yanlislikla birlestirilmis (farkli iki yerin ayni sanilmasi) veya "
        "kacirilmis (ayni yerin ayri kalmasi) durumlar varsa, "
        "`eslestirici.py` icindeki `mesafe_esigi_metre`/`isim_benzerlik_esigi` degerlerini ayarla.",
        "",
    ]
    for yer in coklu_kaynakli[:ornek_sayisi]:
        satirlar.append(f"## {yer.isim} ({yer.alt_kategori})")
        satirlar.append(f"- Konum: {yer.enlem:.5f}, {yer.boylam:.5f}")
        for kaynak_ref in yer.kaynaklar:
            satirlar.append(f"  - {kaynak_ref.kaynak.value}: `{kaynak_ref.kaynak_id}`")
        satirlar.append("")

    rapor_dosyasi.write_text("\n".join(satirlar), encoding="utf-8")
    print(f"[BILGI] Esleme ornek raporu yazildi: {rapor_dosyasi}")


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(description="Kaynaklar arasi ayni yeri tekillestirir.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    ayristirici.add_argument(
        "--mesafe-esigi", type=float, default=VARSAYILAN_MESAFE_ESIGI_METRE, help="Metre cinsinden azami mesafe"
    )
    ayristirici.add_argument(
        "--isim-benzerlik-esigi", type=float, default=VARSAYILAN_ISIM_BENZERLIK_ESIGI, help="0-100 arasi azami isim benzerligi"
    )
    argumanlar = ayristirici.parse_args()
    calistir(
        argumanlar.sehir,
        mesafe_esigi_metre=argumanlar.mesafe_esigi,
        isim_benzerlik_esigi=argumanlar.isim_benzerlik_esigi,
    )


if __name__ == "__main__":
    _ana()
