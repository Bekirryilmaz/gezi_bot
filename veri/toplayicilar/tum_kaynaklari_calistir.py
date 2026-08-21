"""
Tum ham veri toplayicilarini SIRAYLA, TEK bir komutla calistiran orkestrator.

Amac: saatlerce surecek bir veri toplama oturumunu tek bir komutla (orn.
gece boyu, gozetimsiz) baslatabilmek. Her kaynak KENDI try/except blogunda
calisir -- biri (orn. TripAdvisor engellenirse) basarisiz olursa digerleri
yine de calisir, tek bir kaynagin sorunu butun geceyi bosa harcatmaz.

Calistirma (repo kokunden):
    python -m veri.toplayicilar.tum_kaynaklari_calistir --sehir samsun

ONEMLI (bkz. tripadvisor_toplayici.py VE booking_toplayici.py'deki
2026-08-03 kanarya testi notlari): Hem TripAdvisor (bot korumasi) hem
Booking.com (Turkiye'ye ozel YASAL erisim kisitlamasi -- bkz.
booking_toplayici.py modul dokstring'i) kullanicinin KENDI EV IP'sinden
test edildiginde ENGELLENDI. Bu yuzden bu orkestrator HER IKISINI DE
VARSAYILAN OLARAK ATLAR. Tekrar denemek istersen (orn. farkli bir
agdan/bolgeden):
    python -m veri.toplayicilar.tum_kaynaklari_calistir --sehir samsun --tripadvisor-dene --booking-dene

Diger kaynaklardan birini atlamak icin --atla kullanilabilir, orn:
    python -m veri.toplayicilar.tum_kaynaklari_calistir --sehir samsun --atla eksi_sozluk
"""

from __future__ import annotations

import argparse
import time
import traceback

from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir


def _baslik_yazdir(metin: str) -> None:
    cizgi = "=" * 70
    print(f"\n{cizgi}\n{metin}\n{cizgi}")


def _google_maps_calistir(sehir_anahtari: str) -> None:
    from veri.toplayicilar.google_maps_toplayici import calistir as gmaps_calistir

    gmaps_calistir(sehir_anahtari, maks_sonuc_terim_basi=25, maks_yorum_yer_basi=35, ilce_bazli_arama=True)


def _eksi_sozluk_calistir(sehir_anahtari: str) -> None:
    from veri.toplayicilar.eksi_sozluk_toplayici import calistir as eksi_calistir

    eksi_calistir(sehir_anahtari, maks_sayfa_baslik_basi=10)


def _tripadvisor_calistir(sehir_anahtari: str) -> None:
    from veri.toplayicilar.tripadvisor_toplayici import calistir as ta_calistir

    ta_calistir(sehir_anahtari, maks_sonuc_kategori_basi=20, maks_yorum_yer_basi=30)


def _booking_calistir(sehir_anahtari: str) -> None:
    from veri.toplayicilar.booking_toplayici import calistir as booking_calistir

    booking_calistir(sehir_anahtari, maks_sonuc=40, maks_yorum_yer_basi=40)


# Kaynak anahtari -> (goruntulenen isim, calistirma fonksiyonu). Sira,
# gerceklestirilecek calisma sirasidir -- Google Maps en guvenilir/yuksek
# hacimli kaynak oldugu icin ilk, en riskli/engel ihtimali yuksek kaynaklar
# (TripAdvisor) sona konur ki digerleri her turlu tamamlanmis olsun.
_KAYNAKLAR: dict[str, tuple[str, "callable"]] = {
    "google_maps": ("Google Maps", _google_maps_calistir),
    "eksi_sozluk": ("Eksi Sozluk", _eksi_sozluk_calistir),
    "booking": ("Booking.com", _booking_calistir),
    "tripadvisor": ("TripAdvisor", _tripadvisor_calistir),
}


def calistir(
    sehir_anahtari: str,
    atlanacak_kaynaklar: list[str] | None = None,
    tripadvisor_dene: bool = False,
    booking_dene: bool = False,
) -> None:
    atlanacak_kaynaklar = set(atlanacak_kaynaklar or [])
    if not tripadvisor_dene:
        # bkz. tripadvisor_toplayici.py'deki 2026-08-03 kanarya testi notu --
        # ev IP'sinden bile engellendigi icin varsayilan davranis bu kaynagi
        # denemeden atlamaktir (zaman kaybini onlemek icin).
        atlanacak_kaynaklar.add("tripadvisor")
    if not booking_dene:
        # bkz. booking_toplayici.py'deki 2026-08-03 kanarya testi notu --
        # Turkiye'ye ozel YASAL kisitlama nedeniyle ev IP'sinden engellendi.
        atlanacak_kaynaklar.add("booking")
    baslangic = time.monotonic()

    sonuclar: dict[str, str] = {}
    for anahtar, (isim, fonksiyon) in _KAYNAKLAR.items():
        if anahtar in atlanacak_kaynaklar:
            print(f"[BILGI] '{isim}' --atla ile atlandi.")
            sonuclar[isim] = "atlandi"
            continue

        _baslik_yazdir(f"KAYNAK: {isim}")
        kaynak_baslangic = time.monotonic()
        try:
            fonksiyon(sehir_anahtari)
            sonuclar[isim] = "tamamlandi"
        except Exception as hata:
            print(f"[HATA] '{isim}' calisirken beklenmeyen bir hata olustu, diger kaynaklara geciliyor:")
            traceback.print_exc()
            sonuclar[isim] = f"HATA: {hata}"
        gecen = time.monotonic() - kaynak_baslangic
        print(f"[BILGI] '{isim}' bu asamada {gecen / 60:.1f} dakika surdu.")

    toplam_dakika = (time.monotonic() - baslangic) / 60
    _baslik_yazdir("TUM KAYNAKLAR TAMAMLANDI")
    for isim, durum in sonuclar.items():
        print(f"[BILGI]   {isim}: {durum}")
    print(f"[BILGI] Toplam sure: {toplam_dakika:.1f} dakika.")
    print(
        "[BILGI] Sirada: 'python -m veri.esleme.eslestirici --sehir "
        f"{sehir_anahtari}' ile eslestirme, ardindan duygu analizi pipeline'lari."
    )


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(
        description="Tum ham veri toplayicilarini (Google Maps, Eksi Sozluk, Booking, TripAdvisor) sirayla calistirir."
    )
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    ayristirici.add_argument(
        "--atla",
        nargs="+",
        choices=list(_KAYNAKLAR.keys()),
        default=None,
        help="Atlanacak kaynak(lar), orn: --atla booking",
    )
    ayristirici.add_argument(
        "--tripadvisor-dene",
        action="store_true",
        help="TripAdvisor'i (varsayilan olarak atlanir, bkz. modul dokstring'i) yine de dene",
    )
    ayristirici.add_argument(
        "--booking-dene",
        action="store_true",
        help="Booking.com'u (varsayilan olarak atlanir, bkz. modul dokstring'i) yine de dene",
    )
    argumanlar = ayristirici.parse_args()
    calistir(
        argumanlar.sehir,
        atlanacak_kaynaklar=argumanlar.atla,
        tripadvisor_dene=argumanlar.tripadvisor_dene,
        booking_dene=argumanlar.booking_dene,
    )


if __name__ == "__main__":
    _ana()
