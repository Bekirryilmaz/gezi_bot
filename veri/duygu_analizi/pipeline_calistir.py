"""NLP gozlem adayi pipeline'i.

Ham yorumlari BERT ve seffaf konu kurallariyla isler; ancak ciktisi puan,
claim, yayin veya uygunluk degildir. Her cikti inceleme durumu ``bekliyor``
olan ``AdayGozlem`` kaydidir. Karar Motoru bu pipeline'a bagimli degildir.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import uuid
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from ortak.sabitler import DuyguEtiketi, VeriKaynagi
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session
from sunucu.bilgi.pilot_claimleri import kaynak_hakki_uygun_mu
from sunucu.veritabani.baglanti import (
    VERITABANI_URL,
    OturumUretici,
)
from sunucu.veritabani.bilgi_modelleri import (
    DahiliGozlemAdayi,
    KaynakPolitikasi,
    VeriBatch,
)
from sunucu.veritabani.modeller import Sehir, Yer, YerKaynak, Yorum
from tqdm import tqdm

from veri.duygu_analizi.gozlem_adayi import yorumdan_aday_gozlemler
from veri.duygu_analizi.model import MODEL_ADI, toplu_duygu_tahmin_et
from veri.ortak.dosya_araclari import bugunun_tarihi_dosya_adi, jsonl_yaz
from veri.ortak.gozlem_adayi_modeli import AdayGozlem
from veri.ortak.metin_araclari import konsolu_guvenli_hale_getir
from veri.ortak.sehir_ayarlari import sehir_getir
from veri.ortak.veri_yukleyiciler import tum_ham_yorumlari_yukle
from veri.ortak.yorum_modeli import HamYorum

DB_PIPELINE_KAYNAGI = "google_maps_internal_nlp"
DB_PIPELINE_SURUMU = "faz25.2-task3-v1"
EXTRACTOR_KURAL_SURUMU = "safe-extractor-v2"
VARSAYILAN_BATCH_SIZE = 250
MAKSIMUM_BATCH_SIZE = 2000
_SAYAC_ALANLARI = (
    "total",
    "processed",
    "matched",
    "no_match",
    "branch_ambiguous",
    "low_confidence",
    "skipped",
    "error",
    "candidate_count",
    "cache_hit",
    "inference_count",
)


def _yorumlari_isle(
    yorumlar: list[HamYorum], yigin_boyutu: int, *, politika: KaynakPolitikasi | None = None
) -> list[AdayGozlem]:
    """Model siniflarini yalniz konuya bagli inceleme adaylarina donusturur."""
    izinli, neden = kaynak_hakki_uygun_mu(politika, amac="ai_isleme")
    if not izinli or any(yorum.kaynak.value != politika.kaynak for yorum in yorumlar):
        raise PermissionError(neden or "kaynak_politikasi_eslesmiyor")
    metinler = [yorum.yorum_metni for yorum in yorumlar]
    genel_duygular = toplu_duygu_tahmin_et(metinler, yigin_boyutu=yigin_boyutu)
    adaylar: list[AdayGozlem] = []
    for ham_yorum, (duygu_etiketi, duygu_skoru) in tqdm(
        zip(yorumlar, genel_duygular),
        total=len(yorumlar),
        desc="NLP gozlem adayi",
        unit="yorum",
    ):
        adaylar.extend(yorumdan_aday_gozlemler(ham_yorum, duygu_etiketi, duygu_skoru))
    return adaylar


def _ozet_yazdir(
    sehir_isim: str, kaynak_bazli_adaylar: dict[VeriKaynagi, list[AdayGozlem]]
) -> None:
    tum_adaylar = [aday for liste in kaynak_bazli_adaylar.values() for aday in liste]
    if not tum_adaylar:
        print("[UYARI] Uretilebilen gozlem adayi yok.")
        return
    print(f"\n[BILGI] === '{sehir_isim}' NLP Gozlem Adayi Ozeti ===")
    print(f"[BILGI] Toplam inceleme adayi: {len(tum_adaylar)}")
    for kaynak, liste in kaynak_bazli_adaylar.items():
        print(f"[BILGI] {kaynak.value}: {len(liste)} inceleme adayi")


def _bos_sayaclar(toplam: int) -> dict[str, int]:
    return {alan: toplam if alan == "total" else 0 for alan in _SAYAC_ALANLARI}


def _dagilimlari_birlestir(
    hedef: dict[str, dict[str, int]],
    eklenecek: dict[str, Counter[str]],
) -> None:
    for dagilim_adi, sayac in eklenecek.items():
        dagilim = hedef.setdefault(dagilim_adi, {})
        for anahtar, adet in sayac.items():
            dagilim[anahtar] = int(dagilim.get(anahtar, 0)) + adet


def _raw_kaynak_yer_indeksi(sehir_anahtari: str) -> dict[str, set[str]]:
    """Ham Google review kimligini kaynak-yer kimliklerine baglar."""
    kaynak_bazli = tum_ham_yorumlari_yukle(
        sehir_anahtari,
        sessiz=True,
        kaynaklar={VeriKaynagi.GOOGLE_MAPS},
    )
    indeks: dict[str, set[str]] = {}
    for ham_yorum in kaynak_bazli.get(VeriKaynagi.GOOGLE_MAPS, []):
        if ham_yorum.kaynak_yorum_id:
            indeks.setdefault(ham_yorum.kaynak_yorum_id, set()).add(ham_yorum.kaynak_yer_id)
    return indeks


def _kaynak_yer_eslemeleri(
    oturum: Session,
    *,
    sehir_id: str,
    kaynak_yer_idleri: set[str],
) -> dict[str, tuple[str, str]]:
    if not kaynak_yer_idleri:
        return {}
    satirlar = oturum.execute(
        select(YerKaynak.kaynak_id, YerKaynak.yer_id, YerKaynak.sube_id)
        .join(Yer, Yer.id == YerKaynak.yer_id)
        .where(
            Yer.sehir_id == sehir_id,
            YerKaynak.kaynak == VeriKaynagi.GOOGLE_MAPS.value,
            YerKaynak.kaynak_id.in_(kaynak_yer_idleri),
        )
    )
    return {kaynak_id: (yer_id, sube_id) for kaynak_id, yer_id, sube_id in satirlar}


def _sube_durumu(
    yorum: Yorum,
    kaynak_yer_idleri: set[str],
    kaynak_yer_eslemeleri: dict[str, tuple[str, str]],
) -> tuple[str, str | None, str | None]:
    """Review lineage'ini fail-closed bicimde canonical subeye baglar."""
    if not kaynak_yer_idleri:
        return "no_match", None, None
    sirali_kaynaklar = sorted(kaynak_yer_idleri)
    bulunanlar = [
        kaynak_yer_eslemeleri[kaynak_id]
        for kaynak_id in sirali_kaynaklar
        if kaynak_id in kaynak_yer_eslemeleri
    ]
    kaynak_yer_id = sirali_kaynaklar[0]
    if len(bulunanlar) != len(sirali_kaynaklar):
        subeler = {sube_id for _, sube_id in bulunanlar}
        sube_id = next(iter(subeler)) if len(subeler) == 1 else None
        return "branch_ambiguous", kaynak_yer_id, sube_id
    subeler = {sube_id for _, sube_id in bulunanlar}
    yerler = {yer_id for yer_id, _ in bulunanlar}
    if len(subeler) != 1 or yerler != {yorum.yer_id}:
        sube_id = next(iter(subeler)) if len(subeler) == 1 else None
        return "branch_ambiguous", kaynak_yer_id, sube_id
    return "matched", kaynak_yer_id, next(iter(subeler))


def _onbellek_duygusu(yorum: Yorum) -> tuple[DuyguEtiketi, float] | None:
    if (
        yorum.analiz_model_adi != MODEL_ADI
        or yorum.duygu_etiketi is None
        or yorum.duygu_skoru is None
    ):
        return None
    try:
        return DuyguEtiketi(yorum.duygu_etiketi), float(yorum.duygu_skoru)
    except (TypeError, ValueError):
        return None


def _ham_yoruma_cevir(yorum: Yorum, kaynak_yer_id: str) -> HamYorum:
    return HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS,
        kaynak_yer_id=kaynak_yer_id,
        kaynak_yorum_id=yorum.kaynak_yorum_id,
        yazar_takma_adi=yorum.yazar_takma_adi,
        yorum_metni=yorum.yorum_metni,
        kaynakta_puan=yorum.kaynakta_puan,
        yorum_tarihi=yorum.yorum_tarihi,
        dil=yorum.dil,
        cekilme_zamani=yorum.cekilme_zamani or datetime.now(UTC),
    )


def _aday_db_degerleri(
    *,
    aday: AdayGozlem,
    batch_id: str,
    yorum: Yorum,
    kaynak_yer_id: str,
    sube_id: str | None,
    sube_guven_durumu: str,
) -> dict[str, Any]:
    subeli_aday = AdayGozlem.model_validate(
        aday.model_copy(update={"sube_adayi": sube_id}).model_dump(
            exclude={"otomatik_yayinlanabilir"}
        )
    )
    genel_duygu = subeli_aday.aile == "genel_duygu"
    karantina = sube_guven_durumu != "eslesti" or genel_duygu
    return {
        "veri_batch_id": batch_id,
        "yorum_id": yorum.id,
        "kaynak": subeli_aday.kaynak.value,
        "kaynak_kayit_id": subeli_aday.kaynak_kayit_id,
        "kaynak_yer_id": kaynak_yer_id,
        "sube_id": sube_id,
        "aile": subeli_aday.aile.value,
        "gozlem_turu": subeli_aday.gozlem_turu.value,
        "yon": subeli_aday.yon.value,
        "deger": subeli_aday.deger,
        "cikarim_yontemi": subeli_aday.cikarim_yontemi.value,
        "model_surumu": subeli_aday.model_surumu,
        "kural_surumu": subeli_aday.kural_surumu,
        "cikarim_guven_sinifi": subeli_aday.cikarim_guven_sinifi.value,
        "guven_kirilimi": subeli_aday.guven_kirilimi,
        "temporal_durum": subeli_aday.zamansal_durum.value,
        "gozlem_zamani": yorum.yorum_tarihi,
        "span_hash": subeli_aday.span_hash,
        "dahili_referans": subeli_aday.dahili_referans,
        "sube_guven_durumu": sube_guven_durumu,
        "kullanim_durumu": "karantina" if karantina else "aktif",
    }


def _adayi_upsert_et(oturum: Session, degerler: dict[str, Any]) -> None:
    tekil_alanlar = (
        "yorum_id",
        "model_surumu",
        "kural_surumu",
        "aile",
        "gozlem_turu",
        "yon",
        "span_hash",
    )
    guncellenebilir_alanlar = {
        alan: deger
        for alan, deger in degerler.items()
        if alan not in tekil_alanlar and alan != "yorum_id"
    }
    sorgu = insert(DahiliGozlemAdayi).values(**degerler)
    oturum.execute(
        sorgu.on_conflict_do_update(
            constraint="ux_dahili_gozlem_adayi_idempotent",
            set_=guncellenebilir_alanlar,
        )
    )


def _batch_kok_tanimi(
    *,
    sehir_anahtari: str,
    sehir_id: str,
    toplam: int,
    snapshot_upper_cursor: str | None,
    force_model: bool,
) -> dict[str, Any]:
    return {
        "source": DB_PIPELINE_KAYNAGI,
        "pipeline_surumu": DB_PIPELINE_SURUMU,
        "kural_surumu": EXTRACTOR_KURAL_SURUMU,
        "sehir": sehir_anahtari,
        "sehir_id": sehir_id,
        "model": MODEL_ADI,
        "force_model": force_model,
        "snapshot": {
            "upper_cursor": snapshot_upper_cursor,
            "total": toplam,
        },
        "checkpoint": {"yorum_id": None},
        "counters": _bos_sayaclar(toplam),
        "distributions": {
            "family": {},
            "type": {},
            "direction": {},
        },
        "batch_timings": [],
    }


def _snapshot_al(oturum: Session, *, sehir_id: str) -> tuple[str | None, int]:
    satir = oturum.execute(
        select(Yorum.id, func.count().over())
        .join(Yer, Yer.id == Yorum.yer_id)
        .where(
            Yer.sehir_id == sehir_id,
            Yorum.kaynak == VeriKaynagi.GOOGLE_MAPS.value,
        )
        .order_by(Yorum.id.desc())
        .limit(1)
    ).one_or_none()
    if satir is None:
        return None, 0
    return satir[0], int(satir[1])


def _batch_scope_dogrula(
    batch: VeriBatch,
    *,
    sehir_anahtari: str,
    sehir_id: str,
    force_model: bool,
) -> dict[str, Any]:
    kok = dict(batch.kok_tanimi or {})
    beklenen_scope = {
        "source": DB_PIPELINE_KAYNAGI,
        "pipeline_surumu": DB_PIPELINE_SURUMU,
        "kural_surumu": EXTRACTOR_KURAL_SURUMU,
        "sehir": sehir_anahtari,
        "sehir_id": sehir_id,
        "model": MODEL_ADI,
        "force_model": force_model,
    }
    uyusmayanlar = [
        alan for alan, beklenen in beklenen_scope.items() if kok.get(alan) != beklenen
    ]
    snapshot = kok.get("snapshot")
    checkpoint = kok.get("checkpoint")
    sayaclar = kok.get("counters")
    snapshot_gecerli = (
        isinstance(snapshot, dict)
        and isinstance(snapshot.get("total"), int)
        and snapshot["total"] >= 0
        and (
            (snapshot["total"] == 0 and snapshot.get("upper_cursor") is None)
            or (
                snapshot["total"] > 0
                and isinstance(snapshot.get("upper_cursor"), str)
            )
        )
        and isinstance(checkpoint, dict)
        and (
            checkpoint.get("yorum_id") is None
            or (
                isinstance(checkpoint.get("yorum_id"), str)
                and checkpoint["yorum_id"] <= snapshot["upper_cursor"]
            )
        )
        and isinstance(sayaclar, dict)
        and sayaclar.get("total") == snapshot["total"]
    )
    if batch.kaynak != DB_PIPELINE_KAYNAGI:
        uyusmayanlar.append("batch.source")
    if uyusmayanlar or not snapshot_gecerli:
        ayrinti = ",".join(sorted(set(uyusmayanlar))) or "snapshot"
        raise RuntimeError(f"Run-key scope uyusmazligi: {ayrinti}")
    return kok


def _rapor_dosyasi(
    *,
    sehir_anahtari: str,
    run_key: str,
    rapor_dosyasi: Path | None,
) -> Path:
    if rapor_dosyasi is not None:
        return Path(rapor_dosyasi)
    guvenli_kosu = re.sub(r"[^a-zA-Z0-9_.-]+", "_", run_key).strip("_")
    return (
        Path(__file__).resolve().parents[1]
        / "cikti"
        / "raporlar"
        / "dahili_nlp"
        / f"{sehir_anahtari}_{guvenli_kosu}.json"
    )


def _raporu_yaz(dosya: Path, rapor: dict[str, Any]) -> None:
    dosya.parent.mkdir(parents=True, exist_ok=True)
    dosya.write_text(
        json.dumps(rapor, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _kokten_rapor(
    *,
    kok: dict[str, Any],
    sehir_anahtari: str,
    run_key: str,
    dry_run: bool,
    resume: bool,
    force_model: bool,
    no_op: bool,
    baslama_zamani: datetime,
    tamamlanma_zamani: datetime | None,
) -> dict[str, Any]:
    sayaclar = _bos_sayaclar(0)
    sayaclar.update({alan: int(deger) for alan, deger in kok.get("counters", {}).items()})
    dagilimlar = kok.get(
        "distributions",
        {"family": {}, "type": {}, "direction": {}},
    )
    rapor: dict[str, Any] = {
        "pipeline_version": DB_PIPELINE_SURUMU,
        "run_key": run_key,
        "source": DB_PIPELINE_KAYNAGI,
        "model": MODEL_ADI,
        "rule_version": EXTRACTOR_KURAL_SURUMU,
        "city": sehir_anahtari,
        "dry_run": dry_run,
        "resume": resume,
        "force_model": force_model,
        "no_op": no_op,
        "started_at": baslama_zamani.isoformat(),
        "completed_at": tamamlanma_zamani.isoformat() if tamamlanma_zamani else None,
        **sayaclar,
        "family_distribution": dagilimlar.get("family", {}),
        "type_distribution": dagilimlar.get("type", {}),
        "direction_distribution": dagilimlar.get("direction", {}),
        "distributions": dagilimlar,
        "snapshot": kok.get("snapshot", {}),
        "batch_timings": kok.get("batch_timings", []),
    }
    return rapor


def _yerel_gelistirme_db_dogrula() -> None:
    ortam = os.environ.get("UYGULAMA_ORTAMI", "development").lower()
    host = make_url(VERITABANI_URL).host
    if ortam not in {"development", "dev", "test", "testing"} or host not in {
        "localhost",
        "127.0.0.1",
    }:
        raise RuntimeError("Dahili NLP batch pipeline yalniz yerel development/test DB'de calisir")


def _batch_hatasini_kaydet(
    *,
    batch_id: str,
    sure_ms: int,
) -> None:
    with OturumUretici() as oturum:
        batch = oturum.scalar(select(VeriBatch).where(VeriBatch.id == batch_id).with_for_update())
        if batch is None:
            return
        kok = dict(batch.kok_tanimi)
        sayaclar = dict(kok.get("counters", {}))
        sayaclar["error"] = int(sayaclar.get("error", 0)) + 1
        zamanlamalar = list(kok.get("batch_timings", []))
        zamanlamalar.append(
            {
                "batch_no": len(zamanlamalar) + 1,
                "processed": 0,
                "candidate_count": 0,
                "duration_ms": sure_ms,
                "status": "error",
            }
        )
        batch.kok_tanimi = {
            **kok,
            "counters": sayaclar,
            "batch_timings": zamanlamalar,
        }
        oturum.commit()


def _yorum_batchini_isle(
    *,
    oturum: Session,
    yorumlar: list[Yorum],
    batch_id: str | None,
    raw_indeks: dict[str, set[str]],
    kaynak_yer_eslemeleri: dict[str, tuple[str, str]],
    yigin_boyutu: int,
    force_model: bool,
    dry_run: bool,
) -> tuple[dict[str, int], dict[str, Counter[str]]]:
    sayaclar = _bos_sayaclar(0)
    dagilimlar = {
        "family": Counter(),
        "type": Counter(),
        "direction": Counter(),
    }
    eslesen_yorumlar: list[tuple[Yorum, str, str, str | None]] = []
    for yorum in yorumlar:
        sayaclar["processed"] += 1
        kaynak_yer_idleri = (
            raw_indeks.get(yorum.kaynak_yorum_id, set())
            if yorum.kaynak_yorum_id
            else set()
        )
        durum, kaynak_yer_id, sube_id = _sube_durumu(
            yorum,
            kaynak_yer_idleri,
            kaynak_yer_eslemeleri,
        )
        if durum == "no_match":
            sayaclar["no_match"] += 1
            continue
        if durum == "branch_ambiguous":
            sayaclar["branch_ambiguous"] += 1
        else:
            sayaclar["matched"] += 1
        assert kaynak_yer_id is not None
        eslesen_yorumlar.append((yorum, durum, kaynak_yer_id, sube_id))

    duygu_sonuclari: dict[str, tuple[DuyguEtiketi, float]] = {}
    inference_yorumlari: list[Yorum] = []
    for yorum, _, _, _ in eslesen_yorumlar:
        onbellek = None if force_model else _onbellek_duygusu(yorum)
        if onbellek is None:
            inference_yorumlari.append(yorum)
        else:
            duygu_sonuclari[yorum.id] = onbellek
            sayaclar["cache_hit"] += 1

    if inference_yorumlari:
        tahminler = toplu_duygu_tahmin_et(
            [yorum.yorum_metni for yorum in inference_yorumlari],
            yigin_boyutu=yigin_boyutu,
        )
        if len(tahminler) != len(inference_yorumlari):
            raise RuntimeError("Duygu modeli batch uzunlugu ile eslesmeyen sonuc dondurdu")
        for yorum, (etiket, skor) in zip(
            inference_yorumlari,
            tahminler,
            strict=True,
        ):
            duygu_sonuclari[yorum.id] = (DuyguEtiketi(etiket), float(skor))
            if not dry_run:
                yorum.duygu_etiketi = DuyguEtiketi(etiket).value
                yorum.duygu_skoru = float(skor)
                yorum.analiz_model_adi = MODEL_ADI
                yorum.analiz_zamani = datetime.now(UTC)
        sayaclar["inference_count"] += len(inference_yorumlari)

    for yorum, durum, kaynak_yer_id, sube_id in eslesen_yorumlar:
        etiket, skor = duygu_sonuclari[yorum.id]
        ham_yorum = _ham_yoruma_cevir(yorum, kaynak_yer_id)
        adaylar = yorumdan_aday_gozlemler(ham_yorum, etiket, skor)
        if not adaylar:
            sayaclar["skipped"] += 1
            continue
        assert batch_id is not None or dry_run
        sube_guven_durumu = "eslesti" if durum == "matched" else "branch_ambiguous"
        for aday in adaylar:
            if aday.cikarim_guven_sinifi.value == "dusuk":
                sayaclar["low_confidence"] += 1
            aile = aday.aile.value
            dagilimlar["family"][aile] += 1
            dagilimlar["type"][aday.gozlem_turu.value] += 1
            dagilimlar["direction"][aday.yon.value] += 1
            sayaclar["candidate_count"] += 1
            if not dry_run:
                degerler = _aday_db_degerleri(
                    aday=aday,
                    batch_id=batch_id,
                    yorum=yorum,
                    kaynak_yer_id=kaynak_yer_id,
                    sube_id=sube_id,
                    sube_guven_durumu=sube_guven_durumu,
                )
                _adayi_upsert_et(oturum, degerler)
    return sayaclar, dagilimlar


def veritabani_calistir(
    sehir_anahtari: str,
    *,
    dry_run: bool = False,
    batch_size: int = VARSAYILAN_BATCH_SIZE,
    resume: bool = False,
    force_model: bool = False,
    run_key: str | None = None,
    yigin_boyutu: int = 16,
    rapor_dosyasi: Path | None = None,
) -> dict[str, Any]:
    """Development yorumlarini resumable/idempotent batchlerle adaylara cevirir."""
    _yerel_gelistirme_db_dogrula()
    if (
        batch_size <= 0
        or batch_size > MAKSIMUM_BATCH_SIZE
        or yigin_boyutu <= 0
    ):
        raise ValueError("batch_size ve yigin_boyutu pozitif olmalidir")
    sehir = sehir_getir(sehir_anahtari)
    run_key = run_key or f"{DB_PIPELINE_SURUMU}:{sehir.anahtar}"
    rapor_yolu = _rapor_dosyasi(
        sehir_anahtari=sehir.anahtar,
        run_key=run_key,
        rapor_dosyasi=rapor_dosyasi,
    )
    baslama_zamani = datetime.now(UTC)

    with OturumUretici() as oturum:
        sehir_id = oturum.scalar(select(Sehir.id).where(Sehir.isim == sehir.isim))
        if sehir_id is None:
            raise RuntimeError(f"Development DB'de sehir bulunamadi: {sehir.isim}")
        politika = oturum.scalar(
            select(KaynakPolitikasi).where(KaynakPolitikasi.kaynak == VeriKaynagi.GOOGLE_MAPS.value)
        )
        izinli, neden = kaynak_hakki_uygun_mu(politika, amac="ai_isleme")
        if not izinli:
            raise PermissionError(neden or "google_maps_ai_isleme_izni_yok")

    batch_id: str | None = None
    if dry_run:
        with OturumUretici() as oturum:
            snapshot_upper_cursor, toplam = _snapshot_al(
                oturum,
                sehir_id=sehir_id,
            )
        kok = _batch_kok_tanimi(
            sehir_anahtari=sehir.anahtar,
            sehir_id=sehir_id,
            toplam=toplam,
            snapshot_upper_cursor=snapshot_upper_cursor,
            force_model=force_model,
        )
    else:
        with OturumUretici() as oturum:
            batch = oturum.scalar(
                select(VeriBatch)
                .where(
                    VeriBatch.kaynak == DB_PIPELINE_KAYNAGI,
                    VeriBatch.kosu_anahtari == run_key,
                )
                .with_for_update()
            )
            if batch is None:
                snapshot_upper_cursor, toplam = _snapshot_al(
                    oturum,
                    sehir_id=sehir_id,
                )
                yeni_kok = _batch_kok_tanimi(
                    sehir_anahtari=sehir.anahtar,
                    sehir_id=sehir_id,
                    toplam=toplam,
                    snapshot_upper_cursor=snapshot_upper_cursor,
                    force_model=force_model,
                )
                yeni_batch_id = str(uuid.uuid4())
                eklenen_batch_id = oturum.scalar(
                    insert(VeriBatch)
                    .values(
                        id=yeni_batch_id,
                        kaynak=DB_PIPELINE_KAYNAGI,
                        kosu_anahtari=run_key,
                        kok_tanimi=yeni_kok,
                        baslama_zamani=baslama_zamani,
                    )
                    .on_conflict_do_nothing(
                        constraint="ux_veri_batch_kaynak_kosu"
                    )
                    .returning(VeriBatch.id)
                )
                if eklenen_batch_id is not None:
                    batch_id = eklenen_batch_id
                    kok = yeni_kok
                    oturum.commit()
                    batch = None
                else:
                    batch = oturum.scalar(
                        select(VeriBatch)
                        .where(
                            VeriBatch.kaynak == DB_PIPELINE_KAYNAGI,
                            VeriBatch.kosu_anahtari == run_key,
                        )
                        .with_for_update()
                    )
                    if batch is None:
                        raise RuntimeError(
                            "Concurrent VeriBatch insert sonrasi batch bulunamadi"
                        )
            if batch is not None:
                kok = _batch_scope_dogrula(
                    batch,
                    sehir_anahtari=sehir.anahtar,
                    sehir_id=sehir_id,
                    force_model=force_model,
                )
            if batch is not None and batch.tamamlanma_zamani is not None:
                rapor = _kokten_rapor(
                    kok=kok,
                    sehir_anahtari=sehir.anahtar,
                    run_key=run_key,
                    dry_run=False,
                    resume=resume,
                    force_model=force_model,
                    no_op=True,
                    baslama_zamani=batch.baslama_zamani,
                    tamamlanma_zamani=batch.tamamlanma_zamani,
                )
                _raporu_yaz(rapor_yolu, rapor)
                return rapor
            if batch is not None and not resume:
                raise RuntimeError(
                    "Ayni run key ile tamamlanmamis batch var; --resume olmadan degistirilmedi"
                )
            if batch is not None:
                baslama_zamani = batch.baslama_zamani
                batch_id = batch.id
                oturum.commit()

    raw_indeks = _raw_kaynak_yer_indeksi(sehir.anahtar)
    tum_kaynak_yer_idleri = {
        kaynak_yer_id
        for kaynak_yer_idleri in raw_indeks.values()
        for kaynak_yer_id in kaynak_yer_idleri
    }
    with OturumUretici() as oturum:
        kaynak_yer_eslemeleri = _kaynak_yer_eslemeleri(
            oturum,
            sehir_id=sehir_id,
            kaynak_yer_idleri=tum_kaynak_yer_idleri,
        )

    while True:
        batch_baslangici = perf_counter()
        try:
            with OturumUretici() as oturum:
                if dry_run:
                    checkpoint = kok["checkpoint"]["yorum_id"]
                    batch = None
                else:
                    batch = oturum.scalar(
                        select(VeriBatch).where(VeriBatch.id == batch_id).with_for_update()
                    )
                    if batch is None:
                        raise RuntimeError("NLP VeriBatch kaydi bulunamadi")
                    kok = dict(batch.kok_tanimi)
                    checkpoint = kok["checkpoint"]["yorum_id"]
                snapshot_upper = kok["snapshot"]["upper_cursor"]
                if snapshot_upper is None:
                    yorumlar = []
                else:
                    sorgu = (
                        select(Yorum)
                        .join(Yer, Yer.id == Yorum.yer_id)
                        .where(
                            Yer.sehir_id == sehir_id,
                            Yorum.kaynak == VeriKaynagi.GOOGLE_MAPS.value,
                            Yorum.id <= snapshot_upper,
                        )
                        .order_by(Yorum.id)
                        .limit(batch_size)
                    )
                    if checkpoint:
                        sorgu = sorgu.where(Yorum.id > checkpoint)
                    yorumlar = list(oturum.scalars(sorgu))
                if not yorumlar:
                    if not dry_run:
                        batch.tamamlanma_zamani = datetime.now(UTC)
                        oturum.commit()
                    break

                batch_sayaclari, batch_dagilimlari = _yorum_batchini_isle(
                    oturum=oturum,
                    yorumlar=yorumlar,
                    batch_id=batch_id,
                    raw_indeks=raw_indeks,
                    kaynak_yer_eslemeleri=kaynak_yer_eslemeleri,
                    yigin_boyutu=yigin_boyutu,
                    force_model=force_model,
                    dry_run=dry_run,
                )
                sure_ms = max(0, round((perf_counter() - batch_baslangici) * 1000))
                sayaclar = dict(kok["counters"])
                for alan in _SAYAC_ALANLARI:
                    if alan != "total":
                        sayaclar[alan] = int(sayaclar.get(alan, 0)) + int(
                            batch_sayaclari.get(alan, 0)
                        )
                dagilimlar = {ad: dict(degerler) for ad, degerler in kok["distributions"].items()}
                _dagilimlari_birlestir(dagilimlar, batch_dagilimlari)
                zamanlamalar = list(kok["batch_timings"])
                zamanlamalar.append(
                    {
                        "batch_no": len(zamanlamalar) + 1,
                        "processed": batch_sayaclari["processed"],
                        "candidate_count": batch_sayaclari["candidate_count"],
                        "duration_ms": sure_ms,
                        "status": "completed",
                    }
                )
                kok = {
                    **kok,
                    "checkpoint": {"yorum_id": yorumlar[-1].id},
                    "counters": sayaclar,
                    "distributions": dagilimlar,
                    "batch_timings": zamanlamalar,
                }
                if not dry_run:
                    batch.kok_tanimi = kok
                    oturum.commit()
        except Exception:
            if not dry_run and batch_id is not None:
                _batch_hatasini_kaydet(
                    batch_id=batch_id,
                    sure_ms=max(
                        0,
                        round((perf_counter() - batch_baslangici) * 1000),
                    ),
                )
                with OturumUretici() as oturum:
                    hatali_batch = oturum.scalar(select(VeriBatch).where(VeriBatch.id == batch_id))
                    if hatali_batch is not None:
                        hatali_rapor = _kokten_rapor(
                            kok=hatali_batch.kok_tanimi,
                            sehir_anahtari=sehir.anahtar,
                            run_key=run_key,
                            dry_run=False,
                            resume=resume,
                            force_model=force_model,
                            no_op=False,
                            baslama_zamani=baslama_zamani,
                            tamamlanma_zamani=None,
                        )
                        _raporu_yaz(rapor_yolu, hatali_rapor)
            raise

    tamamlanma_zamani = datetime.now(UTC)
    if not dry_run:
        with OturumUretici() as oturum:
            batch = oturum.scalar(select(VeriBatch).where(VeriBatch.id == batch_id))
            if batch is None or batch.tamamlanma_zamani is None:
                raise RuntimeError("NLP batch basariyla tamamlanamadi")
            kok = dict(batch.kok_tanimi)
            tamamlanma_zamani = batch.tamamlanma_zamani
    rapor = _kokten_rapor(
        kok=kok,
        sehir_anahtari=sehir.anahtar,
        run_key=run_key,
        dry_run=dry_run,
        resume=resume,
        force_model=force_model,
        no_op=False,
        baslama_zamani=baslama_zamani,
        tamamlanma_zamani=tamamlanma_zamani,
    )
    _raporu_yaz(rapor_yolu, rapor)
    return rapor


def calistir(sehir_anahtari: str, yigin_boyutu: int = 16) -> Path | None:
    sehir = sehir_getir(sehir_anahtari)
    with OturumUretici() as oturum:
        politikalar = list(oturum.scalars(select(KaynakPolitikasi)))
        izinli_kaynaklar = {
            kaynak
            for kaynak in VeriKaynagi
            if any(
                p.kaynak == kaynak.value and kaynak_hakki_uygun_mu(p, amac="ai_isleme")[0]
                for p in politikalar
            )
        }
    if not izinli_kaynaklar:
        print("[ENGEL] Haklari dogrulanmis kaynak yok; ham yorum okunmadi.")
        return None
    kaynak_bazli_ham = tum_ham_yorumlari_yukle(sehir_anahtari, kaynaklar=izinli_kaynaklar)
    if not kaynak_bazli_ham:
        print("[ENGEL] Haklari dogrulanmis kaynaklardan islenebilir yorum yok; NLP calismadi.")
        return None

    toplam = sum(len(yorumlar) for yorumlar in kaynak_bazli_ham.values())
    print(f"[BILGI] Toplam {toplam} ham yorumdan gozlem adayi uretiliyor (model: {MODEL_ADI})...")
    kaynak_bazli_adaylar: dict[VeriKaynagi, list[AdayGozlem]] = {}
    kaynak_bazli_ham_saklama_hakki: dict[VeriKaynagi, bool] = {}
    for kaynak, yorumlar in kaynak_bazli_ham.items():
        print(f"[BILGI] '{kaynak.value}' isleniyor ({len(yorumlar)} yorum)...")
        with OturumUretici() as oturum:
            politika = oturum.scalar(
                select(KaynakPolitikasi).where(KaynakPolitikasi.kaynak == kaynak.value)
            )
            izinli, neden = kaynak_hakki_uygun_mu(politika, amac="ai_isleme")
            if not izinli:
                print(f"[ENGEL] {kaynak.value}: {neden}; model ve aday uretimi calismadi.")
                continue
            kaynak_bazli_adaylar[kaynak] = _yorumlari_isle(
                yorumlar, yigin_boyutu, politika=politika
            )
            kaynak_bazli_ham_saklama_hakki[kaynak] = kaynak_hakki_uygun_mu(
                politika,
                amac="uzun_sureli_saklama",
            )[0]

    cikti_dosyasi = (
        Path(__file__).resolve().parents[1]
        / "cikti"
        / "islenmis"
        / "gozlem_adaylari"
        / f"{sehir.anahtar}_{bugunun_tarihi_dosya_adi()}.jsonl"
    )
    tum_adaylar = [aday for liste in kaynak_bazli_adaylar.values() for aday in liste]
    if not tum_adaylar:
        print("[BILGI] Haklari dogrulanmis aday yok; cikti yazilmadi.")
        return None
    kalici_payloadlar = [
        aday.kalici_payload(
            ham_icerik_saklanabilir=kaynak_bazli_ham_saklama_hakki.get(kaynak, False)
        )
        for kaynak, adaylar in kaynak_bazli_adaylar.items()
        for aday in adaylar
    ]
    jsonl_yaz(cikti_dosyasi, kalici_payloadlar)
    print(f"[BILGI] Inceleme bekleyen gozlem adaylari yazildi: {cikti_dosyasi}")
    _ozet_yazdir(sehir.isim, kaynak_bazli_adaylar)
    return cikti_dosyasi


def _ayristirici_olustur() -> argparse.ArgumentParser:
    ayristirici = argparse.ArgumentParser(
        description="Development DB yorumlarindan dahili NLP adaylari uretir."
    )
    ayristirici.add_argument(
        "--sehir",
        required=True,
        help="veri/ortak/sehir_ayarlari.py icindeki sehir anahtari",
    )
    ayristirici.add_argument(
        "--dry-run",
        action="store_true",
        help="DB mutasyonu yapmadan gercek cikarim ve rapor uretir",
    )
    ayristirici.add_argument(
        "--batch-size",
        type=int,
        default=VARSAYILAN_BATCH_SIZE,
        help="Her transaction icinde islenecek Yorum sayisi",
    )
    ayristirici.add_argument(
        "--resume",
        action="store_true",
        help="Ayni run key icin tamamlanmamis checkpointten devam eder",
    )
    ayristirici.add_argument(
        "--force-model",
        action="store_true",
        help="Gecerli Yorum model cache'ini kullanmadan yeniden inference eder",
    )
    ayristirici.add_argument(
        "--run-key",
        help=f"Surumlu kosu anahtari (varsayilan: {DB_PIPELINE_SURUMU}:<sehir>)",
    )
    ayristirici.add_argument(
        "--yigin-boyutu", type=int, default=16, help="Modelin bir seferde isleyecegi yorum sayisi"
    )
    return ayristirici


def _ana() -> None:
    konsolu_guvenli_hale_getir()
    ayristirici = _ayristirici_olustur()
    argumanlar = ayristirici.parse_args()
    rapor = veritabani_calistir(
        argumanlar.sehir,
        dry_run=argumanlar.dry_run,
        batch_size=argumanlar.batch_size,
        resume=argumanlar.resume,
        force_model=argumanlar.force_model,
        run_key=argumanlar.run_key,
        yigin_boyutu=argumanlar.yigin_boyutu,
    )
    print(
        "[BILGI] DB NLP batch raporu: "
        f"processed={rapor['processed']} candidate={rapor['candidate_count']} "
        f"error={rapor['error']}"
    )


if __name__ == "__main__":
    _ana()
