"""
Veri aktarimi -- ana calistirma betigi.

`veri/cikti/islenmis/` altindaki EN GUNCEL BirlesikYer, IslenmisYorum ve
YerProfili JSONL dosyalarini okuyup PostgreSQL veritabanina (sunucu/veritabani)
aktarir. Sirasiyla:
  1. Sehir satirini upsert eder
  2. Yerleri + kaynak referanslarini aktarir (yer_aktar.py)
  3. Yorumlari aktarir + duygu_skoru_ortalama'yi gunceller (yorum_aktar.py)
  4. Yer profillerini (fiyat/ulasim/kalabalik/ziyaretci + tanitim metni) aktarir (profil_aktar.py)
  5. Bolge (sehir/ilce) profillerini aktarir (bolge_profil_aktar.py)

Bu betik idempotenttir: defalarca calistirilabilir, ayni yer/yorum
tekrar tekrar eklenmez (bkz. her modulun kendi docstring'i).

Calistirma (repo kokunden):
    python -m sunucu.veritabani.aktarim.calistir --sehir samsun

On kosul: asagidaki veri katmani komutlarinin en az bir kez calistirilmis
olmasi gerekir:
    python -m veri.esleme.eslestirici --sehir samsun
    python -m veri.duygu_analizi.pipeline_calistir --sehir samsun
    python -m veri.duygu_analizi.profil_pipeline_calistir --sehir samsun
    python -m veri.duygu_analizi.bolge_profili_pipeline_calistir --sehir samsun
"""

from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.orm import Session

from sunucu.veritabani.aktarim.bolge_profil_aktar import bolge_profillerini_aktar
from sunucu.veritabani.aktarim.profil_aktar import profilleri_aktar
from sunucu.veritabani.aktarim.tanitim_aktar import bolge_tanitimlarini_aktar, yer_tanitimlarini_aktar
from sunucu.veritabani.aktarim.yer_aktar import yer_yukle_veya_olustur
from sunucu.veritabani.aktarim.yorum_aktar import yorumlari_aktar
from sunucu.veritabani.baglanti import OturumUretici
from sunucu.veritabani.modeller import Sehir
from sunucu.veritabani.bilgi_modelleri import Gozlem, VeriBatch
from veri.ortak.birlesik_yer_modeli import BirlesikYer
from veri.ortak.bolge_profili_modeli import BolgeProfili
from veri.ortak.dosya_araclari import jsonl_oku
from veri.ortak.sehir_ayarlari import SehirAyari, sehir_getir
from veri.ortak.yer_profili_modeli import YerProfili
from veri.ortak.yorum_modeli import IslenmisYorum


def _veri_cikti_kok() -> Path:
    # Bu dosya sunucu/veritabani/aktarim/ altinda, repo koku parents[3]
    return Path(__file__).resolve().parents[3] / "veri" / "cikti" / "islenmis"


def _en_guncel_dosyayi_bul(klasor: Path, desen: str) -> Path | None:
    if not klasor.exists():
        return None
    adaylar = sorted(klasor.glob(desen))  # dosya adlari tarih icerir, siralama = kronolojik
    return adaylar[-1] if adaylar else None


def _birlesik_yerleri_yukle(sehir_anahtari: str) -> tuple[list[BirlesikYer], Path | None]:
    dosya = _en_guncel_dosyayi_bul(_veri_cikti_kok() / "birlesik_yerler", f"{sehir_anahtari}_*.jsonl")
    if dosya is None:
        return [], None
    return [BirlesikYer(**kayit) for kayit in jsonl_oku(dosya)], dosya


def _batch_sagla(oturum: Session, dosya: Path) -> VeriBatch:
    icerik_hash = hashlib.sha256(dosya.read_bytes()).hexdigest()
    kosu = f"{dosya.name}:{icerik_hash}"
    batch = oturum.query(VeriBatch).filter_by(kaynak="birlesik_yerler", kosu_anahtari=kosu).first()
    if batch:
        return batch
    zaman = datetime.fromtimestamp(dosya.stat().st_mtime, timezone.utc)
    batch = VeriBatch(kaynak="birlesik_yerler", kosu_anahtari=kosu, kok_tanimi={"dosya": dosya.name, "sha256": icerik_hash}, baslama_zamani=zaman, tamamlanma_zamani=zaman)
    oturum.add(batch)
    oturum.flush()
    return batch


def _gozlemleri_sagla(oturum: Session, batch: VeriBatch, yer: BirlesikYer) -> None:
    for ref in yer.kaynaklar:
        if ref.cekilme_zamani is None:
            continue
        oz = hashlib.sha256(f"{ref.kaynak.value}|{ref.kaynak_id}|{ref.cekilme_zamani.isoformat()}".encode()).hexdigest()
        varsa = oturum.query(Gozlem).filter_by(veri_batch_id=batch.id, kaynak=ref.kaynak.value, kaynak_kayit_id=ref.kaynak_id, icerik_hash=oz).first()
        if not varsa:
            oturum.add(Gozlem(veri_batch_id=batch.id, kaynak=ref.kaynak.value, kaynak_kayit_id=ref.kaynak_id, kaynak_url=ref.kaynak_url, olay_zamani=ref.olay_zamani, kaynakta_gozlemlenme_zamani=ref.kaynakta_gozlemlenme_zamani, cekilme_zamani=ref.cekilme_zamani, icerik_hash=oz))


def _islenmis_yorumlari_yukle(sehir_anahtari: str) -> list[IslenmisYorum]:
    dosya = _en_guncel_dosyayi_bul(_veri_cikti_kok() / "yorumlar", f"{sehir_anahtari}_*.jsonl")
    if dosya is None:
        return []
    return [IslenmisYorum(**kayit) for kayit in jsonl_oku(dosya)]


def _yer_profillerini_yukle(sehir_anahtari: str) -> list[YerProfili]:
    dosya = _en_guncel_dosyayi_bul(_veri_cikti_kok() / "yer_profilleri", f"{sehir_anahtari}_*.jsonl")
    if dosya is None:
        return []
    return [YerProfili(**kayit) for kayit in jsonl_oku(dosya)]


def _bolge_profillerini_yukle(sehir_anahtari: str) -> list[BolgeProfili]:
    dosya = _en_guncel_dosyayi_bul(_veri_cikti_kok() / "bolge_profilleri", f"{sehir_anahtari}_*.jsonl")
    if dosya is None:
        return []
    return [BolgeProfili(**kayit) for kayit in jsonl_oku(dosya)]


def _tanitim_kayitlarini_yukle(sehir_anahtari: str, tur: str) -> list[dict]:
    dosya = _en_guncel_dosyayi_bul(_veri_cikti_kok() / "tanitimlar", f"{sehir_anahtari}_{tur}_*.jsonl")
    if dosya is None:
        return []
    return list(jsonl_oku(dosya))


def _sehri_yukle_veya_olustur(oturum: Session, sehir_ayari: SehirAyari) -> Sehir:
    sehir = oturum.query(Sehir).filter(Sehir.isim == sehir_ayari.isim).first()
    if sehir is None:
        sehir = Sehir(
            isim=sehir_ayari.isim,
            plaka_kodu=sehir_ayari.plaka_kodu,
            bolge=sehir_ayari.bolge,
        )
        oturum.add(sehir)
        oturum.flush()
    return sehir


def calistir(sehir_anahtari: str) -> None:
    sehir_ayari = sehir_getir(sehir_anahtari)
    oturum = OturumUretici()

    try:
        sehir = _sehri_yukle_veya_olustur(oturum, sehir_ayari)
        print(f"[BILGI] Sehir hazir: {sehir.isim} ({sehir.id})")

        birlesik_yerler, birlesik_dosya = _birlesik_yerleri_yukle(sehir_anahtari)
        if not birlesik_yerler:
            print(
                f"[UYARI] '{sehir_ayari.isim}' icin birlesik yer kataloğu bulunamadi. "
                f"Once 'python -m veri.esleme.eslestirici --sehir {sehir_anahtari}' calistir."
            )
            return

        assert birlesik_dosya is not None
        batch = _batch_sagla(oturum, birlesik_dosya)
        yer_kimligi_haritasi: dict[str, str] = {}
        for birlesik_yer in birlesik_yerler:
            yer = yer_yukle_veya_olustur(oturum, sehir.id, birlesik_yer, batch.id)
            _gozlemleri_sagla(oturum, batch, birlesik_yer)
            yer_kimligi_haritasi[birlesik_yer.yer_kimligi] = yer.id
        oturum.commit()
        print(
            f"[BILGI] {len(birlesik_yerler)} yer islendi -> veritabaninda {len(yer_kimligi_haritasi)} tekil yer "
            "(yeni eklenen VE guncellenen dahil, bkz. yer_aktar.py idempotentlik notu)."
        )

        islenmis_yorumlar = _islenmis_yorumlari_yukle(sehir_anahtari)
        if islenmis_yorumlar:
            yorum_sonucu = yorumlari_aktar(oturum, islenmis_yorumlar)
            oturum.commit()
            print(
                f"[BILGI] Yorumlar aktarildi: {yorum_sonucu.eklenen} yeni, {yorum_sonucu.guncellenen} guncellendi, "
                f"{yorum_sonucu.baglanamayan} yere baglanamadi (bkz. veri/README.md - Eksi Sozluk sinirlamasi)."
            )
        else:
            print(f"[UYARI] '{sehir_ayari.isim}' icin islenmis yorum bulunamadi, bu adim atlandi.")

        yer_profilleri = _yer_profillerini_yukle(sehir_anahtari)
        if yer_profilleri:
            profil_sonucu = profilleri_aktar(oturum, yer_kimligi_haritasi, yer_profilleri)
            oturum.commit()
            print(
                f"[BILGI] Yer profilleri aktarildi: {profil_sonucu.guncellenen} guncellendi, "
                f"{profil_sonucu.eslenemeyen} yere eslenemedi."
            )
        else:
            print(f"[UYARI] '{sehir_ayari.isim}' icin yer profili bulunamadi, bu adim atlandi.")

        bolge_profilleri = _bolge_profillerini_yukle(sehir_anahtari)
        if bolge_profilleri:
            bolge_sonucu = bolge_profillerini_aktar(oturum, sehir.id, bolge_profilleri)
            oturum.commit()
            print(
                f"[BILGI] Bolge profilleri aktarildi: {bolge_sonucu.eklenen} yeni, {bolge_sonucu.guncellenen} guncellendi."
            )
        else:
            print(f"[UYARI] '{sehir_ayari.isim}' icin bolge profili bulunamadi, bu adim atlandi.")

        yer_tanitimlar = _tanitim_kayitlarini_yukle(sehir_anahtari, "yer")
        if yer_tanitimlar:
            t_sonuc = yer_tanitimlarini_aktar(oturum, yer_kimligi_haritasi, yer_tanitimlar)
            oturum.commit()
            print(
                f"[BILGI] Yer tanitimlari aktarildi: {t_sonuc.yer_guncellenen} guncellendi, "
                f"{t_sonuc.yer_eslenemeyen} eslenemedi."
            )
        else:
            print(f"[UYARI] Yer tanitim JSONL yok -- 'python -m veri.duygu_analizi.tanitim_pipeline_calistir' calistir.")

        bolge_tanitimlar = _tanitim_kayitlarini_yukle(sehir_anahtari, "bolge")
        if bolge_tanitimlar:
            n = bolge_tanitimlarini_aktar(oturum, sehir.id, bolge_tanitimlar)
            oturum.commit()
            print(f"[BILGI] Bolge tanitimlari aktarildi: {n} guncellendi.")

        print("[BILGI] Aktarim tamamlandi.")
    except Exception:
        oturum.rollback()
        raise
    finally:
        oturum.close()


def _ana() -> None:
    ayristirici = argparse.ArgumentParser(description="JSONL cikti dosyalarini PostgreSQL veritabanina aktarir.")
    ayristirici.add_argument("--sehir", default="samsun", help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari")
    argumanlar = ayristirici.parse_args()
    calistir(argumanlar.sehir)


if __name__ == "__main__":
    _ana()
