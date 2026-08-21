"""
Playwright-tabanli toplayicilar (su an icin google_maps_toplayici.py) icin
SURECI DISARIDAN gozeten bir "nobetci" (supervisor/watchdog) betigi.

NEDEN GEREKLI (2026-08-03 Faz 6 gozlemi): Cok saatlik gercek bir taramada,
Google Maps toplayicisi bazen (muhtemelen tarayici surecinin CDP
baglantisinin ic durumu nedeniyle) TEK bir yerin islenmesinde SESSIZCE
tikanip kalabiliyor -- ne bir hata firlatiyor ne de zaman asimina ugruyor,
sadece sonsuza kadar bekliyor. `google_maps_toplayici.py` icindeki THREAD
tabanli `_ZamanAsimiBekcisi` bu durumu HER ZAMAN kurtaramiyor, cunku
Playwright'in senkron (sync) API'si es zamanli/thread-guvenli degildir --
ayni sureç icindeki farkli bir thread'den "sayfayi zorla kapat" cagrisi da
tikanmis ana thread'in arkasinda kilitlenebiliyor.

Bu yuzden GERCEK bir zorlama icin, isletim sistemi SEVIYESINDE bir dis
gozetim gerekir: bu betik toplayiciyi AYRI BIR SURECTE (subprocess) calistirir,
cikti dosyasinin degisme zamanini izler; belirli bir sure (`--durgunluk-esigi`,
varsayilan 180 sn) icinde YENI bir kayit eklenmezse SURECI ZORLA SONLANDIRIR
(isletim sistemi seviyesinde `Popen.kill()`, bu HER ZAMAN calisir -- bir
sureci "disaridan" oldurmek, bir thread'i "icten" kesmekten cok daha
guvenilirdir) ve `--devam-et <ayni dosya>` ile YENIDEN BASLATIR. Toplayicinin
kendi resume/`mevcut_kaynak_idlerini_yukle` mantigi sayesinde onceden
kaydedilmis yerler tekrar islenmez -- veri kaybi veya kopya OLMAZ, sadece
o anda tikanmis olan tek yer/terim kaybedilir (kabul edilebilir bir maliyet).

Calistirma (repo kokunden):
    python -m veri.toplayicilar.nobetci_calistir --sehir samsun --maks-sonuc 25 --maks-yorum 35 --ilce-bazli-arama

NOT: Bu betik su an ozellikle `google_maps_toplayici.py` icin yazilmistir
(cikti dosyasi adlandirma seklini bildigi icin); ileride TripAdvisor/Booking
icin de benzer bir gozetim istenirse aynı desen (cikti dosyasi + `--devam-et`
parametresi) tekrar kullanilabilir.
"""

from __future__ import annotations

import argparse
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path

from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.toplayicilar.ortak_araclar import mevcut_kaynak_idlerini_yukle


def _yerler_dosyasi_yolu(sehir_anahtari: str) -> Path:
    """Bu sehir icin izlenecek/devam edilecek yerler dosyasinin yolunu belirler.

    ONEMLI: Dosya adi TARIHE gore uretilir (`<sehir>_yerler_<tarih>.jsonl`), ama
    bu fonksiyon her deneme basinda YENIDEN CAGRILIRSA VE gece yarisini asan
    cok saatlik bir taramada tarih degisirse (`bugunun_tarihi_dosya_adi()`
    farkli bir gun donderir), nobetci FARKLI/BOS bir dosyaya yazmaya baslar --
    o ana kadar biriken TUM ilerleme (--devam-et zinciri) sessizce terk edilir.
    Bunu onlemek icin: once ayni sehir icin ZATEN VAR OLAN (herhangi bir
    tarihli) bir yerler dosyasi olup olmadigina bakilir, varsa EN SON
    degistirilen kullanilir; yoksa bugunun tarihiyle YENI bir dosya adi
    uretilir. `calistir()` bu fonksiyonu SADECE BIR KEZ (taramanin basinda)
    cagirir, boylece secilen dosya tum yeniden baslatmalar boyunca SABIT
    kalir."""
    sehir = sehir_getir(sehir_anahtari)
    kok = Path(__file__).resolve().parents[1] / "cikti" / "ham" / "google_maps"
    mevcut_dosyalar = sorted(kok.glob(f"{sehir.anahtar}_yerler_*.jsonl"), key=lambda p: p.stat().st_mtime)
    if mevcut_dosyalar:
        return mevcut_dosyalar[-1]
    return kok / f"{sehir.anahtar}_yerler_{bugunun_tarihi_dosya_adi()}.jsonl"


def _kayit_sayisi(dosya: Path) -> int:
    return len(mevcut_kaynak_idlerini_yukle(dosya))


def _stdout_okuyucu(surec: subprocess.Popen, satir_kuyrugu: "queue.Queue[str | None]") -> None:
    """Alt surecin stdout'unu AYRI bir thread'den okur ve kuyruga koyar.

    NEDEN GEREKLI: `surec.stdout.readline()` BLOKLAYICI bir cagridir. Bu okuma
    ana izleme dongusunde yapilirsa, alt surec uzun bir sure (durgunluk esigini
    fersah fersah asan bir sure) hic cikti uretmedigi durumda ana dongu
    `readline()` icinde sonsuza kadar beklemekte kalir ve durgunluk kontrolune
    (asagida) HICBIR ZAMAN geri donemez -- yani nobetcinin kendisi de tikanmis
    olur (2026-08-03 gercek taramada gozlemlenen tam olarak budur: 240 sn'lik
    esik asilmasina ragmen ~1 saat boyunca yeniden baslatma tetiklenmedi).
    Bu fonksiyon o riski ortadan kaldirir: okuma bu ayri thread'de bloklanabilir,
    ana thread ise kuyruguna kisa bir timeout ile bakip her zaman durgunluk
    kontrolune geri donebilir."""
    try:
        if surec.stdout is not None:
            for satir in surec.stdout:
                satir_kuyrugu.put(satir)
    except Exception:
        pass
    finally:
        satir_kuyrugu.put(None)


def calistir(
    sehir_anahtari: str,
    maks_sonuc: int = 25,
    maks_yorum: int = 35,
    ilce_bazli_arama: bool = True,
    durgunluk_esigi_saniye: float = 180.0,
    maks_yeniden_baslatma: int = 200,
) -> None:
    yerler_dosyasi = _yerler_dosyasi_yolu(sehir_anahtari)
    print(f"[NOBETCI] Izlenecek dosya: {yerler_dosyasi}")
    print(f"[NOBETCI] Durgunluk esigi: {durgunluk_esigi_saniye:.0f} sn -- bu sure icinde yeni kayit gelmezse surec yeniden baslatilir.")

    for deneme in range(1, maks_yeniden_baslatma + 1):
        komut = [
            sys.executable,
            "-u",  # PYTHONUNBUFFERED -- alt surecin ciktisini gecikmeden gormek icin
            "-m",
            "veri.toplayicilar.google_maps_toplayici",
            "--sehir",
            sehir_anahtari,
            "--maks-sonuc",
            str(maks_sonuc),
            "--maks-yorum",
            str(maks_yorum),
        ]
        if ilce_bazli_arama:
            komut.append("--ilce-bazli-arama")
        if yerler_dosyasi.exists():
            komut += ["--devam-et", str(yerler_dosyasi)]

        print(f"\n[NOBETCI] === Deneme {deneme}/{maks_yeniden_baslatma}: {' '.join(komut)} ===")
        onceki_kayit_sayisi = _kayit_sayisi(yerler_dosyasi)
        son_ilerleme_zamani = time.monotonic()

        surec = subprocess.Popen(
            komut,
            cwd=Path(__file__).resolve().parents[2],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )

        satir_kuyrugu: "queue.Queue[str | None]" = queue.Queue()
        okuyucu_thread = threading.Thread(target=_stdout_okuyucu, args=(surec, satir_kuyrugu), daemon=True)
        okuyucu_thread.start()

        try:
            while True:
                try:
                    satir = satir_kuyrugu.get(timeout=1.0)
                    if satir is not None:
                        print(satir.rstrip())
                except queue.Empty:
                    pass

                if surec.poll() is not None:
                    print(f"[NOBETCI] Alt surec kendi kendine sonlandi (cikis kodu: {surec.returncode}).")
                    break

                guncel_kayit_sayisi = _kayit_sayisi(yerler_dosyasi)
                if guncel_kayit_sayisi > onceki_kayit_sayisi:
                    onceki_kayit_sayisi = guncel_kayit_sayisi
                    son_ilerleme_zamani = time.monotonic()

                if time.monotonic() - son_ilerleme_zamani > durgunluk_esigi_saniye:
                    print(
                        f"\n[NOBETCI] {durgunluk_esigi_saniye:.0f} saniyedir yeni kayit gelmedi -- "
                        "surec tikanmis kabul edilip ZORLA SONLANDIRILIYOR."
                    )
                    surec.kill()
                    surec.wait(timeout=15)
                    break
        except KeyboardInterrupt:
            print("\n[NOBETCI] Kullanici tarafindan durduruldu, alt surec sonlandiriliyor.")
            surec.kill()
            raise
        finally:
            if surec.poll() is None:
                surec.kill()

        if surec.returncode == 0:
            print("[NOBETCI] Toplayici basariyla tamamlandi, nobetci kapaniyor.")
            return

    print(f"[NOBETCI] {maks_yeniden_baslatma} deneme sonunda hala tamamlanamadi -- mevcut veri korunmus halde birakildi, daha sonra tekrar denenebilir.")


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = argparse.ArgumentParser(
        description="google_maps_toplayici.py'yi disaridan gozeten, tikanirsa zorla yeniden baslatan nobetci."
    )
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    ayristirici.add_argument("--maks-sonuc", type=int, default=25, help="Arama terimi basina maksimum sonuc sayisi")
    ayristirici.add_argument("--maks-yorum", type=int, default=35, help="Yer basina maksimum yorum sayisi")
    ayristirici.add_argument(
        "--ilce-bazli-arama", action="store_true", default=True, help="Sehrin ilceleriyle de ek aramalar yap"
    )
    ayristirici.add_argument(
        "--durgunluk-esigi", type=float, default=180.0, help="Bu kadar saniye yeni kayit gelmezse surec yeniden baslatilir"
    )
    ayristirici.add_argument(
        "--maks-yeniden-baslatma", type=int, default=200, help="Toplam en fazla kac kez yeniden baslatilsin"
    )
    argumanlar = ayristirici.parse_args()
    calistir(
        argumanlar.sehir,
        maks_sonuc=argumanlar.maks_sonuc,
        maks_yorum=argumanlar.maks_yorum,
        ilce_bazli_arama=argumanlar.ilce_bazli_arama,
        durgunluk_esigi_saniye=argumanlar.durgunluk_esigi,
        maks_yeniden_baslatma=argumanlar.maks_yeniden_baslatma,
    )


if __name__ == "__main__":
    _ana()
