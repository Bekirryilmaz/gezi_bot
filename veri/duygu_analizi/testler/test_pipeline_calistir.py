import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from threading import Barrier
from types import SimpleNamespace

import pytest
from ortak.sabitler import VeriKaynagi
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sunucu.veritabani import modeller
from sunucu.veritabani.baglanti import OturumUretici as GercekOturumUretici
from sunucu.veritabani.baglanti import motor
from veri.duygu_analizi import pipeline_calistir
from veri.ortak.dosya_araclari import jsonl_yaz
from veri.ortak.gozlem_adayi_modeli import AdayGozlem, CikarimGuvenSinifi
from veri.ortak.yorum_modeli import HamYorum


class _SahteOturum:
    def __init__(self, politika):
        self.politika = politika

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def scalars(self, sorgu):
        return [self.politika]

    def scalar(self, sorgu):
        return self.politika


def test_calistir_ai_only_politikada_raw_span_ve_yazar_kalici_ciktiya_yazmaz(
    monkeypatch,
    tmp_path,
):
    politika = SimpleNamespace(
        kaynak=VeriKaynagi.GOOGLE_MAPS.value,
        kamusal_gosterim="yasak",
        turev_iddia="yasak",
        ai_isleme="izinli",
        uzun_sureli_saklama="bilinmiyor",
        gecerli_baslangic=None,
        gecerli_bitis=None,
    )
    yorum = HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS,
        kaynak_yer_id="sentetik-yer",
        kaynak_yorum_id="sentetik-yorum",
        yorum_metni="sentetik gizli span",
    )
    aday = AdayGozlem(
        kaynak=yorum.kaynak,
        kaynak_kayit_id=yorum.kaynak_yorum_id,
        yer_adayi=yorum.kaynak_yer_id,
        span=yorum.yorum_metni,
        konu="wifi",
        aile="wifi",
        yon="support",
        deger=True,
        gozlem_turu="fact_signal",
        tahmini_gozlem={"yon": "destek", "deger": True},
        cikarim_yontemi="deterministik_kural",
        model_surumu="sentetik-model-v1",
        kural_surumu="sentetik-kural-v1",
        cikarim_guven_sinifi=CikarimGuvenSinifi.DUSUK,
        guven_kirilimi={"genel_bert_kullanildi": False},
    )
    gecici_cikti = tmp_path / "adaylar.jsonl"

    monkeypatch.setattr(
        pipeline_calistir,
        "OturumUretici",
        lambda: _SahteOturum(politika),
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "sehir_getir",
        lambda anahtar: SimpleNamespace(anahtar=anahtar, isim="Sentetik Sehir"),
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {VeriKaynagi.GOOGLE_MAPS: [yorum]},
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "_yorumlari_isle",
        lambda *args, **kwargs: [aday],
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "jsonl_yaz",
        lambda dosya, kayitlar: jsonl_yaz(gecici_cikti, kayitlar),
    )

    sonuc = pipeline_calistir.calistir("sentetik")
    yazilanlar = [
        json.loads(satir) for satir in gecici_cikti.read_text(encoding="utf-8").splitlines()
    ]

    assert sonuc is not None
    assert len(yazilanlar) == 1
    assert "span" not in yazilanlar[0]
    assert "yazar_takma_adi" not in yazilanlar[0]
    assert yazilanlar[0]["span_hash"] == aday.span_hash
    assert yazilanlar[0]["dahili_referans"] == aday.dahili_referans
    assert yazilanlar[0]["otomatik_yayinlanabilir"] is False


@pytest.fixture
def db_pipeline_ortami(monkeypatch):
    baglanti = motor.connect()
    dis_islem = baglanti.begin()

    def oturum_uretici():
        return Session(
            bind=baglanti,
            join_transaction_mode="create_savepoint",
            expire_on_commit=False,
        )

    monkeypatch.setattr(pipeline_calistir, "OturumUretici", oturum_uretici)
    try:
        yield oturum_uretici
    finally:
        dis_islem.rollback()
        baglanti.close()


def _db_verisi_ekle(
    oturum_uretici,
    monkeypatch,
    *,
    yorum_metinleri: list[str],
    onbellekli_indeksler: set[int] | None = None,
    ikinci_sube: bool = False,
    yorum_idleri: list[str] | None = None,
):
    ek = uuid.uuid4().hex
    sehir_ismi = f"Pipeline Test Sehri {ek}"
    monkeypatch.setattr(
        pipeline_calistir,
        "sehir_getir",
        lambda anahtar: SimpleNamespace(anahtar=anahtar, isim=sehir_ismi),
    )
    onbellekli_indeksler = onbellekli_indeksler or set()
    with oturum_uretici() as oturum:
        politika = oturum.scalar(
            select(modeller.KaynakPolitikasi).where(
                modeller.KaynakPolitikasi.kaynak == VeriKaynagi.GOOGLE_MAPS.value
            )
        )
        if politika is None:
            politika = modeller.KaynakPolitikasi(
                kaynak=VeriKaynagi.GOOGLE_MAPS.value,
                ai_isleme="izinli",
            )
            oturum.add(politika)
        else:
            politika.ai_isleme = "izinli"
        sehir = modeller.Sehir(isim=sehir_ismi)
        oturum.add(sehir)
        oturum.flush()

        yerler = []
        subeler = []
        for indeks in range(2 if ikinci_sube else 1):
            yer = modeller.Yer(
                sehir_id=sehir.id,
                isim=f"Sentetik Yer {indeks} {ek}",
                ana_kategori="yeme_icme",
                alt_kategori="kafe",
                konum=f"SRID=4326;POINT({36.3 + indeks / 100} {41.3 + indeks / 100})",
            )
            kimlik = modeller.YerKimligi(sehir_id=sehir.id)
            oturum.add_all([yer, kimlik])
            oturum.flush()
            sube = modeller.Sube(
                yer_kimligi_id=kimlik.id,
                legacy_yer_id=yer.id,
                guncel_isim=yer.isim,
            )
            oturum.add(sube)
            oturum.flush()
            yerler.append(yer)
            subeler.append(sube)

        kaynaklar = []
        for indeks, (yer, sube) in enumerate(zip(yerler, subeler, strict=True), 1):
            kaynak = modeller.YerKaynak(
                yer_id=yer.id,
                kaynak=VeriKaynagi.GOOGLE_MAPS.value,
                kaynak_id=f"source-place-{indeks}-{ek}",
                sube_id=sube.id,
            )
            oturum.add(kaynak)
            kaynaklar.append(kaynak)
        oturum.flush()

        yorumlar = []
        for indeks, metin in enumerate(yorum_metinleri):
            onbellekli = indeks in onbellekli_indeksler
            yorum = modeller.Yorum(
                id=yorum_idleri[indeks] if yorum_idleri else None,
                yer_id=yerler[0].id,
                kaynak=VeriKaynagi.GOOGLE_MAPS.value,
                kaynak_yorum_id=f"review-{indeks}-{ek}",
                yazar_takma_adi=f"gizli-yazar-{indeks}",
                yorum_metni=metin,
                yorum_tarihi=datetime(2026, 9, 1 + indeks, tzinfo=UTC),
                duygu_etiketi="notr" if onbellekli else None,
                duygu_skoru=0.0 if onbellekli else None,
                analiz_model_adi=pipeline_calistir.MODEL_ADI if onbellekli else None,
            )
            oturum.add(yorum)
            yorumlar.append(yorum)
        oturum.commit()
        return SimpleNamespace(
            ek=ek,
            sehir_ismi=sehir_ismi,
            yerler=yerler,
            subeler=subeler,
            kaynaklar=kaynaklar,
            yorumlar=yorumlar,
        )


def _ham_yorum(
    db_yorumu,
    kaynak_yer_id: str,
) -> HamYorum:
    return HamYorum(
        kaynak=VeriKaynagi.GOOGLE_MAPS,
        kaynak_yer_id=kaynak_yer_id,
        kaynak_yorum_id=db_yorumu.kaynak_yorum_id,
        yazar_takma_adi=db_yorumu.yazar_takma_adi,
        yorum_metni=db_yorumu.yorum_metni,
        yorum_tarihi=db_yorumu.yorum_tarihi,
    )


def _pipeline_sayilari(oturum_uretici) -> tuple[int, int, int]:
    with oturum_uretici() as oturum:
        return (
            oturum.scalar(select(func.count()).select_from(modeller.VeriBatch)),
            oturum.scalar(select(func.count()).select_from(modeller.DahiliGozlemAdayi)),
            oturum.scalar(
                select(func.count())
                .select_from(modeller.Yorum)
                .where(modeller.Yorum.analiz_model_adi == pipeline_calistir.MODEL_ADI)
            ),
        )


def test_db_policy_reddinde_ham_loader_hic_cagrilmaz(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=[],
    )
    with db_pipeline_ortami() as oturum:
        politika = oturum.scalar(
            select(modeller.KaynakPolitikasi).where(
                modeller.KaynakPolitikasi.kaynak == VeriKaynagi.GOOGLE_MAPS.value
            )
        )
        politika.ai_isleme = "yasak"
        oturum.commit()
    loader_cagrildi = False

    def ham_loader(*args, **kwargs):
        nonlocal loader_cagrildi
        loader_cagrildi = True
        return {}

    monkeypatch.setattr(pipeline_calistir, "tum_ham_yorumlari_yukle", ham_loader)

    with pytest.raises(PermissionError):
        pipeline_calistir.veritabani_calistir(
            "sentetik",
            dry_run=True,
            rapor_dosyasi=tmp_path / "policy.json",
        )

    assert loader_cagrildi is False


@pytest.mark.parametrize("dry_run", [False, True])
def test_db_kosu_baslangic_snapshotindan_sonra_eklenen_yorumu_disarida_tutar(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
    dry_run,
):
    ilk_id = "00000000-0000-0000-0000-000000000010"
    yeni_id = "ffffffff-ffff-ffff-ffff-ffffffffffff"
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=["WiFi var."],
        yorum_idleri=[ilk_id],
    )
    hamlar = [
        _ham_yorum(veri.yorumlar[0], veri.kaynaklar[0].kaynak_id),
        HamYorum(
            kaynak=VeriKaynagi.GOOGLE_MAPS,
            kaynak_yer_id=veri.kaynaklar[0].kaynak_id,
            kaynak_yorum_id=f"review-yeni-{veri.ek}",
            yorum_metni="Otopark var.",
        ),
    ]
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {VeriKaynagi.GOOGLE_MAPS: hamlar},
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "toplu_duygu_tahmin_et",
        lambda metinler, yigin_boyutu: [
            (pipeline_calistir.DuyguEtiketi.NOTR, 0.0) for _ in metinler
        ],
    )
    asil_kok_uret = pipeline_calistir._batch_kok_tanimi
    yeni_eklendi = False

    def snapshot_sonrasi_kok_uret(*args, **kwargs):
        nonlocal yeni_eklendi
        kok = asil_kok_uret(*args, **kwargs)
        if not yeni_eklendi:
            with db_pipeline_ortami() as oturum:
                oturum.add(
                    modeller.Yorum(
                        id=yeni_id,
                        yer_id=veri.yerler[0].id,
                        kaynak=VeriKaynagi.GOOGLE_MAPS.value,
                        kaynak_yorum_id=f"review-yeni-{veri.ek}",
                        yorum_metni="Otopark var.",
                    )
                )
                oturum.commit()
            yeni_eklendi = True
        return kok

    monkeypatch.setattr(
        pipeline_calistir,
        "_batch_kok_tanimi",
        snapshot_sonrasi_kok_uret,
    )
    kosu = f"faz25.2-task3:snapshot-v1:{dry_run}:{veri.ek}"

    rapor = pipeline_calistir.veritabani_calistir(
        "sentetik",
        dry_run=dry_run,
        batch_size=1,
        run_key=kosu,
        rapor_dosyasi=tmp_path / f"snapshot-{dry_run}.json",
    )

    assert rapor["total"] == 1
    assert rapor["processed"] == 1
    assert rapor["snapshot"]["upper_cursor"] == ilk_id
    with db_pipeline_ortami() as oturum:
        yeni = oturum.get(modeller.Yorum, yeni_id)
        assert yeni.analiz_model_adi is None
        if not dry_run:
            batch = oturum.scalar(
                select(modeller.VeriBatch).where(
                    modeller.VeriBatch.kosu_anahtari == kosu
                )
            )
            assert batch.kok_tanimi["snapshot"] == {
                "upper_cursor": ilk_id,
                "total": 1,
            }


def test_db_empty_input_bos_snapshotla_guvenle_tamamlanir(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=[],
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {},
    )

    rapor = pipeline_calistir.veritabani_calistir(
        "sentetik",
        run_key=f"faz25.2-task3:empty-v1:{uuid.uuid4().hex}",
        rapor_dosyasi=tmp_path / "empty.json",
    )

    assert rapor["total"] == 0
    assert rapor["processed"] == 0
    assert rapor["snapshot"] == {"upper_cursor": None, "total": 0}


def test_db_complete_run_scope_city_mismatchinde_noop_yerine_fail_closed(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=[],
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {},
    )
    kosu = f"faz25.2-task3:scope-v1:{veri.ek}"
    pipeline_calistir.veritabani_calistir(
        "sentetik",
        run_key=kosu,
        rapor_dosyasi=tmp_path / "scope-ilk.json",
    )
    with db_pipeline_ortami() as oturum:
        batch = oturum.scalar(
            select(modeller.VeriBatch).where(modeller.VeriBatch.kosu_anahtari == kosu)
        )
        batch.kok_tanimi = {
            **batch.kok_tanimi,
            "sehir_id": str(uuid.uuid4()),
        }
        oturum.commit()

    with pytest.raises(RuntimeError, match="scope"):
        pipeline_calistir.veritabani_calistir(
            "sentetik",
            run_key=kosu,
            rapor_dosyasi=tmp_path / "scope-ikinci.json",
        )


def test_db_no_match_yorum_icin_model_ve_cache_calistirilmaz(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=["WiFi var."],
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {},
    )

    def model_cagrilmamali(*args, **kwargs):
        raise AssertionError("no_match yorum modele gitmemeli")

    monkeypatch.setattr(
        pipeline_calistir,
        "toplu_duygu_tahmin_et",
        model_cagrilmamali,
    )
    rapor = pipeline_calistir.veritabani_calistir(
        "sentetik",
        run_key=f"faz25.2-task3:no-match-v1:{veri.ek}",
        rapor_dosyasi=tmp_path / "no-match.json",
    )

    assert rapor["no_match"] == 1
    assert rapor["inference_count"] == 0
    with db_pipeline_ortami() as oturum:
        yorum = oturum.get(modeller.Yorum, veri.yorumlar[0].id)
        assert yorum.analiz_model_adi is None


def test_db_batch_sonundaki_hata_candidate_cache_ve_checkpointi_birlikte_geri_alir(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=["WiFi var."],
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {
            VeriKaynagi.GOOGLE_MAPS: [
                _ham_yorum(veri.yorumlar[0], veri.kaynaklar[0].kaynak_id)
            ]
        },
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "toplu_duygu_tahmin_et",
        lambda metinler, yigin_boyutu: [
            (pipeline_calistir.DuyguEtiketi.NOTR, 0.0)
        ],
    )

    def commit_oncesi_hata(*args, **kwargs):
        raise RuntimeError("candidate-cache-sonrasi-hata")

    monkeypatch.setattr(
        pipeline_calistir,
        "_dagilimlari_birlestir",
        commit_oncesi_hata,
    )
    kosu = f"faz25.2-task3:rollback-v1:{veri.ek}"

    with pytest.raises(RuntimeError, match="candidate-cache-sonrasi"):
        pipeline_calistir.veritabani_calistir(
            "sentetik",
            run_key=kosu,
            rapor_dosyasi=tmp_path / "rollback.json",
        )

    with db_pipeline_ortami() as oturum:
        batch = oturum.scalar(
            select(modeller.VeriBatch).where(modeller.VeriBatch.kosu_anahtari == kosu)
        )
        yorum = oturum.get(modeller.Yorum, veri.yorumlar[0].id)
        aday_sayisi = oturum.scalar(
            select(func.count())
            .select_from(modeller.DahiliGozlemAdayi)
            .where(modeller.DahiliGozlemAdayi.yorum_id == yorum.id)
        )
        assert aday_sayisi == 0
        assert yorum.analiz_model_adi is None
        assert batch.kok_tanimi["checkpoint"]["yorum_id"] is None


@pytest.mark.parametrize(
    ("batch_size", "yigin_boyutu"),
    [(0, 16), (2001, 16), (1, 0)],
)
def test_db_batch_ve_model_yigin_sinirlari_fail_fast(
    batch_size,
    yigin_boyutu,
):
    with pytest.raises(ValueError):
        pipeline_calistir.veritabani_calistir(
            "samsun",
            dry_run=True,
            batch_size=batch_size,
            yigin_boyutu=yigin_boyutu,
        )


def test_db_dry_run_gercek_cikarimi_raporlar_ama_hicbir_tabloyu_degistirmez(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=["WiFi var ama genel hava siradandi."],
    )
    hamlar = [_ham_yorum(veri.yorumlar[0], veri.kaynaklar[0].kaynak_id)]
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {VeriKaynagi.GOOGLE_MAPS: hamlar},
    )
    model_cagrilari = []

    def sahte_model(metinler, yigin_boyutu):
        model_cagrilari.append(list(metinler))
        return [(pipeline_calistir.DuyguEtiketi.NOTR, 0.0) for _ in metinler]

    monkeypatch.setattr(pipeline_calistir, "toplu_duygu_tahmin_et", sahte_model)
    once = _pipeline_sayilari(db_pipeline_ortami)
    rapor_dosyasi = tmp_path / "dry-run.json"

    rapor = pipeline_calistir.veritabani_calistir(
        "sentetik",
        dry_run=True,
        batch_size=1,
        run_key="faz25.2-task3:test-dry-run-v1",
        rapor_dosyasi=rapor_dosyasi,
    )

    assert _pipeline_sayilari(db_pipeline_ortami) == once
    assert model_cagrilari == [["WiFi var ama genel hava siradandi."]]
    assert rapor["processed"] == 1
    assert rapor["matched"] == 1
    assert rapor["candidate_count"] == 1
    assert rapor["inference_count"] == 1
    assert rapor["dry_run"] is True
    assert rapor["family_distribution"] == {"wifi": 1}
    assert rapor["type_distribution"] == {"fact_signal": 1}
    assert rapor["direction_distribution"] == {"support": 1}
    assert json.loads(rapor_dosyasi.read_text(encoding="utf-8")) == rapor


def test_db_gercek_kosu_aday_ekler_ve_complete_tekrari_noop_olur(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=["WiFi var."],
    )
    hamlar = [_ham_yorum(veri.yorumlar[0], veri.kaynaklar[0].kaynak_id)]
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {VeriKaynagi.GOOGLE_MAPS: hamlar},
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "toplu_duygu_tahmin_et",
        lambda metinler, yigin_boyutu: [
            (pipeline_calistir.DuyguEtiketi.NOTR, 0.0) for _ in metinler
        ],
    )
    kosu = f"faz25.2-task3:insert-v1:{veri.ek}"

    ilk = pipeline_calistir.veritabani_calistir(
        "sentetik",
        batch_size=1,
        run_key=kosu,
        rapor_dosyasi=tmp_path / "ilk.json",
    )
    ikinci = pipeline_calistir.veritabani_calistir(
        "sentetik",
        batch_size=1,
        run_key=kosu,
        rapor_dosyasi=tmp_path / "ikinci.json",
    )

    with db_pipeline_ortami() as oturum:
        adaylar = list(
            oturum.scalars(
                select(modeller.DahiliGozlemAdayi).where(
                    modeller.DahiliGozlemAdayi.yorum_id == veri.yorumlar[0].id
                )
            )
        )
        batch = oturum.scalar(
            select(modeller.VeriBatch).where(modeller.VeriBatch.kosu_anahtari == kosu)
        )
    assert ilk["candidate_count"] == 1
    assert ikinci["no_op"] is True
    assert len(adaylar) == 1
    assert adaylar[0].kullanim_durumu == "aktif"
    assert adaylar[0].sube_guven_durumu == "eslesti"
    assert adaylar[0].gozlem_zamani == veri.yorumlar[0].yorum_tarihi
    assert batch.tamamlanma_zamani is not None


def test_db_batch_hatasi_checkpoint_son_committen_ilerlemez_ve_resume_tamamlar(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=["WiFi var.", "Otopark var.", "Bahcesi var."],
        yorum_idleri=[
            "00000000-0000-0000-0000-000000000001",
            "00000000-0000-0000-0000-000000000002",
            "00000000-0000-0000-0000-000000000003",
        ],
    )
    hamlar = [_ham_yorum(yorum, veri.kaynaklar[0].kaynak_id) for yorum in veri.yorumlar]
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {VeriKaynagi.GOOGLE_MAPS: hamlar},
    )
    cagrilar = 0

    def ikinci_batchte_hata(metinler, yigin_boyutu):
        nonlocal cagrilar
        cagrilar += 1
        if cagrilar == 2:
            raise RuntimeError("enjekte-edilmis-batch-hatasi")
        return [(pipeline_calistir.DuyguEtiketi.NOTR, 0.0) for _ in metinler]

    monkeypatch.setattr(
        pipeline_calistir,
        "toplu_duygu_tahmin_et",
        ikinci_batchte_hata,
    )
    kosu = f"faz25.2-task3:resume-v1:{veri.ek}"
    hatali_rapor_dosyasi = tmp_path / "hatali.json"

    with pytest.raises(RuntimeError, match="enjekte-edilmis"):
        pipeline_calistir.veritabani_calistir(
            "sentetik",
            batch_size=1,
            run_key=kosu,
            rapor_dosyasi=hatali_rapor_dosyasi,
        )

    ilk_cursor = min(yorum.id for yorum in veri.yorumlar)
    hatali_rapor = json.loads(hatali_rapor_dosyasi.read_text(encoding="utf-8"))
    assert hatali_rapor["error"] == 1
    assert hatali_rapor["completed_at"] is None
    with db_pipeline_ortami() as oturum:
        batch = oturum.scalar(
            select(modeller.VeriBatch).where(modeller.VeriBatch.kosu_anahtari == kosu)
        )
        aday_sayisi = oturum.scalar(
            select(func.count())
            .select_from(modeller.DahiliGozlemAdayi)
            .where(modeller.DahiliGozlemAdayi.veri_batch_id == batch.id)
        )
        assert batch.kok_tanimi["checkpoint"]["yorum_id"] == ilk_cursor
        assert batch.tamamlanma_zamani is None
        assert aday_sayisi == 1

    yeni_id = "ffffffff-ffff-ffff-ffff-ffffffffffff"
    with db_pipeline_ortami() as oturum:
        yeni_yorum = modeller.Yorum(
            id=yeni_id,
            yer_id=veri.yerler[0].id,
            kaynak=VeriKaynagi.GOOGLE_MAPS.value,
            kaynak_yorum_id=f"review-resume-yeni-{veri.ek}",
            yorum_metni="Canli muzik var.",
        )
        oturum.add(yeni_yorum)
        oturum.commit()
    hamlar.append(_ham_yorum(yeni_yorum, veri.kaynaklar[0].kaynak_id))

    monkeypatch.setattr(
        pipeline_calistir,
        "toplu_duygu_tahmin_et",
        lambda metinler, yigin_boyutu: [
            (pipeline_calistir.DuyguEtiketi.NOTR, 0.0) for _ in metinler
        ],
    )
    rapor = pipeline_calistir.veritabani_calistir(
        "sentetik",
        batch_size=1,
        resume=True,
        run_key=kosu,
        rapor_dosyasi=tmp_path / "resume.json",
    )
    assert rapor["processed"] == 3
    with db_pipeline_ortami() as oturum:
        batch = oturum.scalar(
            select(modeller.VeriBatch).where(modeller.VeriBatch.kosu_anahtari == kosu)
        )
        assert batch.kok_tanimi["checkpoint"]["yorum_id"] == max(
            yorum.id for yorum in veri.yorumlar
        )
        assert batch.tamamlanma_zamani is not None
        yeni_yorum = oturum.get(modeller.Yorum, yeni_id)
        assert yeni_yorum.analiz_model_adi is None


def test_db_cache_yalniz_eksik_subseti_inference_eder_force_hepsini_yeniler(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=["WiFi var.", "Otopark var."],
        onbellekli_indeksler={0},
    )
    hamlar = [_ham_yorum(yorum, veri.kaynaklar[0].kaynak_id) for yorum in veri.yorumlar]
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {VeriKaynagi.GOOGLE_MAPS: hamlar},
    )
    model_girdileri = []

    def sahte_model(metinler, yigin_boyutu):
        model_girdileri.append(list(metinler))
        return [(pipeline_calistir.DuyguEtiketi.NOTR, 0.0) for _ in metinler]

    monkeypatch.setattr(pipeline_calistir, "toplu_duygu_tahmin_et", sahte_model)
    rapor = pipeline_calistir.veritabani_calistir(
        "sentetik",
        batch_size=2,
        run_key=f"faz25.2-task3:cache-v1:{veri.ek}",
        rapor_dosyasi=tmp_path / "cache.json",
    )
    assert rapor["cache_hit"] == 1
    assert rapor["inference_count"] == 1
    assert model_girdileri == [["Otopark var."]]

    model_girdileri.clear()
    zorla = pipeline_calistir.veritabani_calistir(
        "sentetik",
        batch_size=2,
        force_model=True,
        run_key=f"faz25.2-task3:force-v1:{veri.ek}",
        rapor_dosyasi=tmp_path / "force.json",
    )
    assert zorla["cache_hit"] == 0
    assert zorla["inference_count"] == 2
    beklenen_sira = [
        yorum.yorum_metni for yorum in sorted(veri.yorumlar, key=lambda yorum: yorum.id)
    ]
    assert model_girdileri == [beklenen_sira]
    with db_pipeline_ortami() as oturum:
        aday_sayisi = oturum.scalar(
            select(func.count())
            .select_from(modeller.DahiliGozlemAdayi)
            .where(modeller.DahiliGozlemAdayi.yorum_id.in_([yorum.id for yorum in veri.yorumlar]))
        )
    assert aday_sayisi == 2


def test_db_branch_mismatch_adayi_karantinaya_alir(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=["WiFi var."],
        ikinci_sube=True,
    )
    hamlar = [_ham_yorum(veri.yorumlar[0], veri.kaynaklar[1].kaynak_id)]
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {VeriKaynagi.GOOGLE_MAPS: hamlar},
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "toplu_duygu_tahmin_et",
        lambda metinler, yigin_boyutu: [
            (pipeline_calistir.DuyguEtiketi.NOTR, 0.0) for _ in metinler
        ],
    )

    rapor = pipeline_calistir.veritabani_calistir(
        "sentetik",
        batch_size=1,
        run_key=f"faz25.2-task3:mismatch-v1:{veri.ek}",
        rapor_dosyasi=tmp_path / "mismatch.json",
    )

    with db_pipeline_ortami() as oturum:
        aday = oturum.scalar(
            select(modeller.DahiliGozlemAdayi).where(
                modeller.DahiliGozlemAdayi.yorum_id == veri.yorumlar[0].id
            )
        )
    assert rapor["branch_ambiguous"] == 1
    assert aday.sube_guven_durumu == "branch_ambiguous"
    assert aday.kullanim_durumu == "karantina"


def test_db_ayni_review_birden_cok_source_place_ayni_subede_guvenlidir(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=["Otopark var."],
    )
    with db_pipeline_ortami() as oturum:
        ikinci_kaynak = modeller.YerKaynak(
            yer_id=veri.yerler[0].id,
            kaynak=VeriKaynagi.GOOGLE_MAPS.value,
            kaynak_id=f"source-place-alias-{veri.ek}",
            sube_id=veri.subeler[0].id,
        )
        oturum.add(ikinci_kaynak)
        oturum.commit()
        ikinci_kaynak_id = ikinci_kaynak.kaynak_id
    hamlar = [
        _ham_yorum(veri.yorumlar[0], veri.kaynaklar[0].kaynak_id),
        _ham_yorum(veri.yorumlar[0], ikinci_kaynak_id),
    ]
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {VeriKaynagi.GOOGLE_MAPS: hamlar},
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "toplu_duygu_tahmin_et",
        lambda metinler, yigin_boyutu: [
            (pipeline_calistir.DuyguEtiketi.NOTR, 0.0) for _ in metinler
        ],
    )

    rapor = pipeline_calistir.veritabani_calistir(
        "sentetik",
        batch_size=1,
        run_key=f"faz25.2-task3:multi-place-v1:{veri.ek}",
        rapor_dosyasi=tmp_path / "multi-place.json",
    )

    assert rapor["matched"] == 1
    assert rapor["branch_ambiguous"] == 0
    with db_pipeline_ortami() as oturum:
        aday = oturum.scalar(
            select(modeller.DahiliGozlemAdayi).where(
                modeller.DahiliGozlemAdayi.yorum_id == veri.yorumlar[0].id
            )
        )
    assert aday.sube_guven_durumu == "eslesti"


def test_db_raporu_raw_metin_ve_yazar_sizdirmaz(
    monkeypatch,
    tmp_path,
    db_pipeline_ortami,
):
    veri = _db_verisi_ekle(
        db_pipeline_ortami,
        monkeypatch,
        yorum_metinleri=["GIZLI_SENTETIK_METIN WiFi var."],
    )
    hamlar = [_ham_yorum(veri.yorumlar[0], veri.kaynaklar[0].kaynak_id)]
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {VeriKaynagi.GOOGLE_MAPS: hamlar},
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "toplu_duygu_tahmin_et",
        lambda metinler, yigin_boyutu: [
            (pipeline_calistir.DuyguEtiketi.NOTR, 0.0) for _ in metinler
        ],
    )
    rapor_dosyasi = tmp_path / "guvenli.json"

    pipeline_calistir.veritabani_calistir(
        "sentetik",
        dry_run=True,
        run_key=f"faz25.2-task3:guvenli-v1:{veri.ek}",
        rapor_dosyasi=rapor_dosyasi,
    )

    rapor_metni = rapor_dosyasi.read_text(encoding="utf-8")
    assert "GIZLI_SENTETIK_METIN" not in rapor_metni
    assert "gizli-yazar" not in rapor_metni


def test_db_concurrent_ilk_baslangic_tek_batch_uretir(
    monkeypatch,
    tmp_path,
):
    ek = uuid.uuid4().hex
    sehir_ismi = f"Concurrent Pipeline Sehri {ek}"
    kosu = f"faz25.2-task3:concurrent-v1:{ek}"
    politika_eklendi = False
    onceki_ai_isleme = None
    with GercekOturumUretici() as oturum:
        politika = oturum.scalar(
            select(modeller.KaynakPolitikasi).where(
                modeller.KaynakPolitikasi.kaynak == VeriKaynagi.GOOGLE_MAPS.value
            )
        )
        if politika is None:
            politika = modeller.KaynakPolitikasi(
                kaynak=VeriKaynagi.GOOGLE_MAPS.value,
                ai_isleme="izinli",
            )
            oturum.add(politika)
            politika_eklendi = True
        else:
            onceki_ai_isleme = politika.ai_isleme
            politika.ai_isleme = "izinli"
        sehir = modeller.Sehir(isim=sehir_ismi)
        oturum.add(sehir)
        oturum.commit()
        sehir_id = sehir.id

    monkeypatch.setattr(
        pipeline_calistir,
        "sehir_getir",
        lambda anahtar: SimpleNamespace(anahtar=anahtar, isim=sehir_ismi),
    )
    monkeypatch.setattr(
        pipeline_calistir,
        "tum_ham_yorumlari_yukle",
        lambda *args, **kwargs: {},
    )
    kok_barrier = Barrier(2)
    asil_kok_uret = pipeline_calistir._batch_kok_tanimi

    def eszamanli_kok_uret(*args, **kwargs):
        sonuc = asil_kok_uret(*args, **kwargs)
        kok_barrier.wait(timeout=10)
        return sonuc

    monkeypatch.setattr(
        pipeline_calistir,
        "_batch_kok_tanimi",
        eszamanli_kok_uret,
    )

    def calistir(indeks):
        try:
            rapor = pipeline_calistir.veritabani_calistir(
                "concurrent",
                run_key=kosu,
                rapor_dosyasi=tmp_path / f"concurrent-{indeks}.json",
            )
            return ("ok", rapor["no_op"])
        except Exception as hata:
            return ("error", hata)

    try:
        with ThreadPoolExecutor(max_workers=2) as havuz:
            sonuclar = list(havuz.map(calistir, range(2)))
        hatalar = [sonuc[1] for sonuc in sonuclar if sonuc[0] == "error"]
        assert not any(isinstance(hata, IntegrityError) for hata in hatalar)
        assert any(sonuc[0] == "ok" and sonuc[1] is False for sonuc in sonuclar)
        assert all(
            sonuc[0] == "ok"
            or (
                isinstance(sonuc[1], RuntimeError)
                and "tamamlanmamis batch" in str(sonuc[1])
            )
            for sonuc in sonuclar
        )
        with GercekOturumUretici() as oturum:
            batch_sayisi = oturum.scalar(
                select(func.count())
                .select_from(modeller.VeriBatch)
                .where(
                    modeller.VeriBatch.kaynak
                    == pipeline_calistir.DB_PIPELINE_KAYNAGI,
                    modeller.VeriBatch.kosu_anahtari == kosu,
                )
            )
        assert batch_sayisi == 1
    finally:
        with GercekOturumUretici() as oturum:
            oturum.execute(
                delete(modeller.VeriBatch).where(
                    modeller.VeriBatch.kaynak
                    == pipeline_calistir.DB_PIPELINE_KAYNAGI,
                    modeller.VeriBatch.kosu_anahtari == kosu,
                )
            )
            oturum.execute(delete(modeller.Sehir).where(modeller.Sehir.id == sehir_id))
            politika = oturum.scalar(
                select(modeller.KaynakPolitikasi).where(
                    modeller.KaynakPolitikasi.kaynak
                    == VeriKaynagi.GOOGLE_MAPS.value
                )
            )
            if politika_eklendi:
                oturum.delete(politika)
            else:
                politika.ai_isleme = onceki_ai_isleme
            oturum.commit()


def test_cli_db_pipeline_flaglerini_ve_legacy_yigin_boyutunu_kabul_eder() -> None:
    args = pipeline_calistir._ayristirici_olustur().parse_args(
        [
            "--sehir",
            "samsun",
            "--dry-run",
            "--batch-size",
            "25",
            "--resume",
            "--force-model",
            "--run-key",
            "faz25.2-task3:manuel-v1",
            "--yigin-boyutu",
            "8",
        ]
    )
    assert args.sehir == "samsun"
    assert args.dry_run is True
    assert args.batch_size == 25
    assert args.resume is True
    assert args.force_model is True
    assert args.run_key == "faz25.2-task3:manuel-v1"
    assert args.yigin_boyutu == 8


def test_cli_sehir_argumani_zorunludur() -> None:
    with pytest.raises(SystemExit):
        pipeline_calistir._ayristirici_olustur().parse_args([])
