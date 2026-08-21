"""
Turkce veri kalite kontrol raporlama betigi.

Amac: veri/esleme/eslestirici.py'nin urettigi BirlesikYer kataloğunu VE ham
kaynak (Yer/HamYorum) verisini gozden gecirip "hangi alanlar eksik",
"hangi kayitlar supheli/aykiri", "hangi iki kayit belki ayni yerdi ama
eslesme kacirildi" gibi sorulara Turkce, okunabilir bir markdown raporuyla
cevap verir.

ONEMLI: Bu betik veriyi HICBIR SEKILDE DEGISTIRMEZ, sadece RAPORLAR.
Bulunan sorunlara gore ne yapilacagina (kategori eslemesini guncellemek,
bir toplayicinin secicisini duzeltmek, esleme esiklerini ayarlamak vb.)
HER ZAMAN sen (veya bu raporu okuyan gelistirici) manuel karar verir --
otomatik "duzeltme" kasitli olarak yapilmaz cunku bu, veri kalitesi
sorunlarini sessizce maskeleyebilir.

Calistirma (repo kokunden):
    python -m veri.kalite_kontrol.rapor_olustur --sehir samsun
"""

from __future__ import annotations

import argparse
import statistics
from collections import Counter
from pathlib import Path

from rapidfuzz import fuzz

from ortak.sabitler import VeriKaynagi
from veri.ortak.birlesik_yer_modeli import BirlesikYer
from ortak.cografya_araclari import haversine_metre
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_oku
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir, turkce_kucuk_harf
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.ortak.veri_yukleyiciler import tum_ham_yerleri_yukle, tum_ham_yorumlari_yukle
from veri.ortak.yer_modeli import OzellikSeti
from veri.ortak.yorum_modeli import HamYorum

# Turkiye'nin kabaca disini (enlem/boylam) belirleyen sinir kutusu. Bunun
# disindaki bir nokta, "veri toplama/ayristirma sirasinda bir hata olmus"
# demektir (orn. enlem/boylam yer degistirmis, eksi isaret kaybolmus) --
# veri setinin buyuklugunden BAGIMSIZ, her zaman gecerli bir kontrol.
_TURKIYE_ENLEM_ARALIGI = (35.0, 43.0)
_TURKIYE_BOYLAM_ARALIGI = (25.0, 45.0)

# Istatistiksel aykiri deger tespiti icin ORTALAMA/STANDART SAPMA yerine
# MEDYAN/MAD (medyan mutlak sapma) kullanilir. Sebep: ortalama ve standart
# sapma, tam da tespit etmeye calistigimiz asiri uc degerlerden GUCLU
# SEKILDE ETKILENIR (bir tek asiri uzak nokta, standart sapmayi sismirip
# kendisini 'normal' gosterebilir -- 'aykiri deger maskeleme' sorunu).
# Medyan ve MAD ise az sayida asiri deger karsisinda DAHA SAGLAM
# (robust) kalir. Esik BILEREK genis tutulur cunku bir il genelinde
# (orn. Samsun'un sahil boyunca ~150km yayilmasi gibi) DOGAL bir cografi
# yayilim, hatali bir veriyle karistirilmamali.
_AYKIRI_DEGER_MAD_ESIGI = 8.0
_AYKIRI_DEGER_MIN_KAYIT_SAYISI = 10
# Normal dagilimda MAD'i standart sapmaya cevirmek icin kullanilan sabit
# (istatistikte yaygin kullanilan bir katsayidir).
_MAD_TUTARLILIK_KATSAYISI = 1.4826

# "Belki ayni yerdi ama eslestirici.py kacirdi" supheli ciftlerini bulmak
# icin kullanilan, eslestiriciden DAHA GEVSEK esikler (yani esleme
# esiginden dusuk kalan ama yine de dikkat cekici olan ciftleri yakalar).
_SUPHELI_MESAFE_ESIGI_METRE = 300.0
_SUPHELI_ISIM_BENZERLIK_ESIGI = 60.0

def _cikti_kok() -> Path:
    return Path(__file__).resolve().parents[1] / "cikti"


def _en_guncel_birlesik_katalogu_bul(sehir_anahtari: str) -> Path | None:
    klasor = _cikti_kok() / "islenmis" / "birlesik_yerler"
    if not klasor.exists():
        return None
    adaylar = sorted(klasor.glob(f"{sehir_anahtari}_*.jsonl"))
    return adaylar[-1] if adaylar else None  # dosya adlari tarih icerdigi icin siralama = kronolojik


def _birlesik_yerleri_yukle(dosya: Path) -> list[BirlesikYer]:
    yerler = []
    for kayit in jsonl_oku(dosya):
        try:
            yerler.append(BirlesikYer(**kayit))
        except Exception as hata:
            print(f"[UYARI] {dosya.name} icinde okunamayan kayit: {hata}")
    return yerler


def _ham_yer_sayilarini_say(sehir_anahtari: str) -> dict[VeriKaynagi, int]:
    """Esleme oncesi, her kaynaktan kac HAM Yer kaydi geldigini sayar
    (kaynak-bazli kapsama olcumu icin)."""
    return {kaynak: len(yerler) for kaynak, yerler in tum_ham_yerleri_yukle(sehir_anahtari).items()}


def _eksik_alan_oranlari(birlesik_yerler: list[BirlesikYer]) -> dict[str, float]:
    toplam = len(birlesik_yerler)
    if toplam == 0:
        return {}

    temel_alanlar = ["adres", "telefon", "web_sitesi", "aciklama"]
    oranlar: dict[str, float] = {}
    for alan in temel_alanlar:
        dolu = sum(1 for y in birlesik_yerler if getattr(y, alan))
        oranlar[alan] = round(100 * dolu / toplam, 1)

    oranlar["fotograf_urlleri"] = round(100 * sum(1 for y in birlesik_yerler if y.fotograf_urlleri) / toplam, 1)

    for alan in OzellikSeti.model_fields:
        dolu = sum(1 for y in birlesik_yerler if getattr(y.ozellikler, alan) is not None)
        oranlar[f"ozellik:{alan}"] = round(100 * dolu / toplam, 1)

    return oranlar


def _kategori_dagilimi(birlesik_yerler: list[BirlesikYer]) -> Counter:
    return Counter(f"{y.ana_kategori.value}/{y.alt_kategori}" for y in birlesik_yerler)


def _kaynak_kapsam_dagilimi(birlesik_yerler: list[BirlesikYer]) -> Counter:
    """Kac yerin 1, 2 veya 3+ farkli kaynaktan dogrulandigini sayar --
    yuksek 'tek kaynakli' orani, esleme esiklerinin fazla siki olabilecegine
    ya da ilgili kaynaklarin o bolgede zayif kapsama sagladigina isaret eder."""
    return Counter(min(y.kac_kaynaktan_dogrulandi, 3) for y in birlesik_yerler)


def _turkiye_sinirlari_disinda_mi(y: BirlesikYer) -> bool:
    return not (_TURKIYE_ENLEM_ARALIGI[0] <= y.enlem <= _TURKIYE_ENLEM_ARALIGI[1]) or not (
        _TURKIYE_BOYLAM_ARALIGI[0] <= y.boylam <= _TURKIYE_BOYLAM_ARALIGI[1]
    )


def _cografi_aykiri_degerleri_bul(birlesik_yerler: list[BirlesikYer]) -> tuple[list[BirlesikYer], list[tuple[BirlesikYer, float]]]:
    # Not: `y not in kesin_aykiri` gibi liste-icerik karsilastirmasi yerine
    # tek gecisli bir filtre kullaniyoruz -- hem daha hizli (O(n) vs O(n^2))
    # hem de pydantic modellerinin ICERIK esitligine (deger karsilastirmasi)
    # degil, hangi KAYDIN aykiri oldugu bilgisine dayanir.
    kesin_aykiri = [y for y in birlesik_yerler if _turkiye_sinirlari_disinda_mi(y)]
    turkiye_ici = [y for y in birlesik_yerler if not _turkiye_sinirlari_disinda_mi(y)]

    istatistiksel_aykiri: list[tuple[BirlesikYer, float]] = []
    if len(turkiye_ici) >= _AYKIRI_DEGER_MIN_KAYIT_SAYISI:
        # Agirlik merkezi olarak ORTALAMA yerine MEDYAN enlem/boylam kullanilir
        # (medyan da asiri degerlerden ortalama kadar etkilenmez).
        medyan_enlem = statistics.median(y.enlem for y in turkiye_ici)
        medyan_boylam = statistics.median(y.boylam for y in turkiye_ici)
        mesafeler = [haversine_metre(y.enlem, y.boylam, medyan_enlem, medyan_boylam) for y in turkiye_ici]
        medyan_mesafe = statistics.median(mesafeler)
        mutlak_sapmalar = [abs(m - medyan_mesafe) for m in mesafeler]
        mad = statistics.median(mutlak_sapmalar)
        if mad > 0:
            esik = medyan_mesafe + _AYKIRI_DEGER_MAD_ESIGI * _MAD_TUTARLILIK_KATSAYISI * mad
            for y, mesafe in zip(turkiye_ici, mesafeler):
                if mesafe > esik:
                    istatistiksel_aykiri.append((y, mesafe))

    return kesin_aykiri, istatistiksel_aykiri


def _supheli_esiglenmemis_ciftleri_bul(birlesik_yerler: list[BirlesikYer]) -> list[tuple[BirlesikYer, BirlesikYer, float, float]]:
    """Ayni kategoride, birbirine yakin VE ismi biraz benzeyen ama FARKLI
    BirlesikYer kayitlari olarak kalmis ciftleri bulur -- bunlar
    eslestirici.py'nin kacirdigi gercek eslesmeler olabilir (esikleri
    gevsetmeyi dusunmelisin) YA DA gercekten farkli ama benzer isimli iki
    komsu yer olabilir (orn. 'Liman Restoran' ve 'Liman Kafe') -- bu yuzden
    OTOMATIK birlestirilmezler, sadece elle kontrol icin listelenir."""
    supheli: list[tuple[BirlesikYer, BirlesikYer, float, float]] = []
    for i, yer1 in enumerate(birlesik_yerler):
        for yer2 in birlesik_yerler[i + 1 :]:
            if yer1.ana_kategori != yer2.ana_kategori:
                continue
            mesafe = haversine_metre(yer1.enlem, yer1.boylam, yer2.enlem, yer2.boylam)
            if mesafe > _SUPHELI_MESAFE_ESIGI_METRE:
                continue
            benzerlik = fuzz.WRatio(turkce_kucuk_harf(yer1.isim.strip()), turkce_kucuk_harf(yer2.isim.strip()))
            if benzerlik >= _SUPHELI_ISIM_BENZERLIK_ESIGI:
                supheli.append((yer1, yer2, mesafe, benzerlik))
    return supheli


def _yorum_kalite_ozeti(yorumlar_kaynak_bazli: dict[VeriKaynagi, list[HamYorum]]) -> dict[VeriKaynagi, dict[str, float | int]]:
    KISA_YORUM_ESIGI_KARAKTER = 15
    ozet: dict[VeriKaynagi, dict[str, float | int]] = {}
    for kaynak, yorumlar in yorumlar_kaynak_bazli.items():
        toplam = len(yorumlar)
        uzunluklar = [len(y.yorum_metni) for y in yorumlar]
        kisa_sayisi = sum(1 for u in uzunluklar if u < KISA_YORUM_ESIGI_KARAKTER)
        yazarsiz_sayisi = sum(1 for y in yorumlar if not y.yazar_takma_adi)
        ozet[kaynak] = {
            "toplam": toplam,
            "ortalama_uzunluk": round(statistics.mean(uzunluklar), 1) if uzunluklar else 0,
            "kisa_yorum_orani": round(100 * kisa_sayisi / toplam, 1) if toplam else 0.0,
            "yazarsiz_orani": round(100 * yazarsiz_sayisi / toplam, 1) if toplam else 0.0,
        }
    return ozet


def _raporu_olustur(
    sehir_isim: str,
    ham_yer_sayilari: dict[VeriKaynagi, int],
    birlesik_yerler: list[BirlesikYer],
    kesin_aykiri: list[BirlesikYer],
    istatistiksel_aykiri: list[tuple[BirlesikYer, float]],
    supheli_ciftler: list[tuple[BirlesikYer, BirlesikYer, float, float]],
    yorum_ozeti: dict[VeriKaynagi, dict[str, float | int]],
) -> str:
    satirlar = [f"# Veri Kalite Raporu - {sehir_isim}", ""]

    satirlar.append("## 1. Ham Veri Kapsamasi (Esleme Oncesi)")
    satirlar.append("")
    if ham_yer_sayilari:
        satirlar.append("| Kaynak | Ham Yer Sayisi |")
        satirlar.append("|---|---|")
        for kaynak, sayi in ham_yer_sayilari.items():
            satirlar.append(f"| {kaynak.value} | {sayi} |")
    else:
        satirlar.append("Hicbir kaynaktan ham veri bulunamadi. Once toplayicilari calistir.")
    satirlar.append("")

    satirlar.append("## 2. Birlesik Yer Katalogu Ozeti")
    satirlar.append("")
    if not birlesik_yerler:
        satirlar.append(
            "Birlesik yer kataloğu bulunamadi. Once `python -m veri.esleme.eslestirici --sehir <sehir>` calistir."
        )
        satirlar.append("")
    else:
        satirlar.append(f"Toplam **{len(birlesik_yerler)}** tekil yer.")
        satirlar.append("")
        satirlar.append("### Kaynak Kapsam Dagilimi (kac farkli kaynaktan dogrulandi)")
        satirlar.append("")
        kapsam = _kaynak_kapsam_dagilimi(birlesik_yerler)
        for adet_kaynak in sorted(kapsam):
            etiket = f"{adet_kaynak}+ kaynak" if adet_kaynak == 3 else f"{adet_kaynak} kaynak"
            satirlar.append(f"- {etiket}: {kapsam[adet_kaynak]} yer")
        satirlar.append("")

        satirlar.append("### Kategori Dagilimi")
        satirlar.append("")
        for kategori, adet in sorted(_kategori_dagilimi(birlesik_yerler).items(), key=lambda x: -x[1]):
            satirlar.append(f"- {kategori}: {adet}")
        satirlar.append("")

        satirlar.append("### Eksik Alan Oranlari (ne kadari BOS/bilinmiyor)")
        satirlar.append("")
        satirlar.append("| Alan | Eksik Oran (%) |")
        satirlar.append("|---|---|")
        eksik_oranlar = {k: round(100 - v, 1) for k, v in _eksik_alan_oranlari(birlesik_yerler).items()}
        for alan, eksik_oran in sorted(eksik_oranlar.items(), key=lambda x: -x[1]):
            satirlar.append(f"| {alan} | {eksik_oran} |")
        satirlar.append("")

        satirlar.append("## 3. Aykiri / Supheli Kayitlar")
        satirlar.append("")
        if kesin_aykiri:
            satirlar.append(f"**{len(kesin_aykiri)} kayit Turkiye sinirlarinin ACIKCA disinda** (muhtemelen enlem/boylam hatasi):")
            satirlar.append("")
            for y in kesin_aykiri:
                satirlar.append(f"- {y.isim}: enlem={y.enlem}, boylam={y.boylam}")
            satirlar.append("")
        else:
            satirlar.append("Turkiye sinirlari disinda kesin aykiri kayit bulunamadi.")
            satirlar.append("")

        if istatistiksel_aykiri:
            satirlar.append(
                f"**{len(istatistiksel_aykiri)} kayit, veri setinin kendi cografi dagilimina gore istatistiksel "
                f"olarak asiri uzak** (medyandan {_AYKIRI_DEGER_MAD_ESIGI}+ MAD):"
            )
            satirlar.append("")
            for y, mesafe in sorted(istatistiksel_aykiri, key=lambda t: -t[1]):
                satirlar.append(f"- {y.isim} ({y.alt_kategori}): merkeze uzakligi ~{mesafe / 1000:.1f} km")
            satirlar.append("")
        elif len(birlesik_yerler) >= _AYKIRI_DEGER_MIN_KAYIT_SAYISI:
            satirlar.append("Istatistiksel cografi aykiri deger bulunamadi.")
            satirlar.append("")

        satirlar.append("## 4. Kacirilmis Olabilecek Eslesmeler (Supheli Ciftler)")
        satirlar.append("")
        satirlar.append(
            "Asagidaki ciftler AYNI kategoride, birbirine yakin ve isimleri biraz benziyor ama "
            "`eslestirici.py` bunlari BIRLESTIRMEDI (esikler asilmadi). Gercekten ayni yer olup olmadiklarini "
            "elle kontrol et; oyleyse `eslestirici.py`'deki esikleri gevsetmeyi degerlendir."
        )
        satirlar.append("")
        if supheli_ciftler:
            for yer1, yer2, mesafe, benzerlik in sorted(supheli_ciftler, key=lambda t: -t[3]):
                satirlar.append(
                    f"- '{yer1.isim}' <-> '{yer2.isim}' (mesafe: {mesafe:.0f}m, isim benzerligi: {benzerlik:.0f}/100)"
                )
        else:
            satirlar.append("Supheli (kacirilmis olabilecek) cift bulunamadi.")
        satirlar.append("")

    satirlar.append("## 5. Ham Yorum Verisi Ozeti")
    satirlar.append("")
    if yorum_ozeti:
        satirlar.append("| Kaynak | Toplam Yorum | Ort. Uzunluk (karakter) | Kisa Yorum Orani (%) | Yazarsiz Oran (%) |")
        satirlar.append("|---|---|---|---|---|")
        for kaynak, ozet in yorum_ozeti.items():
            satirlar.append(
                f"| {kaynak.value} | {ozet['toplam']} | {ozet['ortalama_uzunluk']} | "
                f"{ozet['kisa_yorum_orani']} | {ozet['yazarsiz_orani']} |"
            )
    else:
        satirlar.append("Hicbir kaynaktan ham yorum verisi bulunamadi.")
    satirlar.append("")

    return "\n".join(satirlar)


def calistir(sehir_anahtari: str) -> Path:
    sehir = sehir_getir(sehir_anahtari)

    print(f"[BILGI] '{sehir.isim}' icin kalite raporu hazirlaniyor...")
    ham_yer_sayilari = _ham_yer_sayilarini_say(sehir_anahtari)

    birlesik_dosya = _en_guncel_birlesik_katalogu_bul(sehir_anahtari)
    birlesik_yerler = _birlesik_yerleri_yukle(birlesik_dosya) if birlesik_dosya else []
    if birlesik_dosya:
        print(f"[BILGI] Birlesik katalog okundu: {birlesik_dosya.name} ({len(birlesik_yerler)} yer)")
    else:
        print("[UYARI] Birlesik yer kataloğu bulunamadi -- once veri/esleme/eslestirici.py calistirilmali.")

    kesin_aykiri, istatistiksel_aykiri = _cografi_aykiri_degerleri_bul(birlesik_yerler)
    supheli_ciftler = _supheli_esiglenmemis_ciftleri_bul(birlesik_yerler)

    yorumlar_kaynak_bazli = tum_ham_yorumlari_yukle(sehir_anahtari)
    yorum_ozeti = _yorum_kalite_ozeti(yorumlar_kaynak_bazli)

    rapor_metni = _raporu_olustur(
        sehir.isim, ham_yer_sayilari, birlesik_yerler, kesin_aykiri, istatistiksel_aykiri, supheli_ciftler, yorum_ozeti
    )

    rapor_dosyasi = _cikti_kok() / "raporlar" / f"kalite_{sehir_anahtari}_{bugunun_tarihi_dosya_adi()}.md"
    rapor_dosyasi.parent.mkdir(parents=True, exist_ok=True)
    rapor_dosyasi.write_text(rapor_metni, encoding="utf-8")

    print(f"[BILGI] Rapor yazildi: {rapor_dosyasi}")
    print(
        f"[BILGI] Ozet: {len(birlesik_yerler)} yer, {len(kesin_aykiri)} kesin aykiri, "
        f"{len(istatistiksel_aykiri)} istatistiksel aykiri, {len(supheli_ciftler)} supheli cift."
    )
    return rapor_dosyasi


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(description="Turkce veri kalite kontrol raporu olusturur.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    argumanlar = ayristirici.parse_args()
    calistir(argumanlar.sehir)


if __name__ == "__main__":
    _ana()
