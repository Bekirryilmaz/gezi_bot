"""
IslenmisYorum (JSONL) -> Yorum (PostgreSQL) aktarimi.

Baglanti mantigi: her IslenmisYorum, `(kaynak, kaynak_yer_id)` ciftiyle
`YerKaynak` tablosunda aranir. Eksi Sozluk kayitlari icin `kaynak_yer_id`
bir yer degil bir sehir/baslik anahtaridir, bu yuzden hicbir YerKaynak'a
eslesmez ve baglanamayan sayilir -- bu, `veri/duygu_analizi/yer_profili_cikarici.py`
ve `veri/README.md` icinde de belgelenen, bilinen ve bilincli kabul edilmis
bir sinirlamadir.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func
from sqlalchemy.orm import Session

from sunucu.veritabani.modeller import Yer, YerKaynak, Yorum
from veri.ortak.yorum_modeli import IslenmisYorum


@dataclass
class YorumAktarimSonucu:
    eklenen: int = 0
    guncellenen: int = 0
    baglanamayan: int = 0
    etkilenen_yer_idleri: set[str] | None = None

    def __post_init__(self) -> None:
        if self.etkilenen_yer_idleri is None:
            self.etkilenen_yer_idleri = set()


def _yeri_kaynaktan_bul(oturum: Session, kaynak: str, kaynak_yer_id: str) -> Yer | None:
    kaynak_kaydi = (
        oturum.query(YerKaynak).filter(YerKaynak.kaynak == kaynak, YerKaynak.kaynak_id == kaynak_yer_id).first()
    )
    return kaynak_kaydi.yer if kaynak_kaydi else None


def _yorum_anahtari(yer_id: str, yorum: IslenmisYorum) -> tuple:
    """`kaynak_yorum_id` varsa onunla, yoksa (bazi kaynaklarda yorumun
    kendine ait bir kimligi olmayabilir) yer+kaynak+metin ile tekillik
    anahtari uretir -- veritabani semasi degismeden (NULL kaynak_yorum_id'ler
    unique kisit tarafindan ayirt edilemez) hem ayni calistirma icinde HEM
    de calistirmalar arasinda ayni yorumun ikinci kez eklenmesini onler."""
    if yorum.kaynak_yorum_id:
        return (yer_id, yorum.kaynak.value, yorum.kaynak_yorum_id)
    return (yer_id, yorum.kaynak.value, None, yorum.yorum_metni)


def _var_olan_yorumu_bul(oturum: Session, yer_id: str, yorum: IslenmisYorum) -> Yorum | None:
    sorgu = oturum.query(Yorum).filter(Yorum.yer_id == yer_id, Yorum.kaynak == yorum.kaynak.value)
    if yorum.kaynak_yorum_id:
        return sorgu.filter(Yorum.kaynak_yorum_id == yorum.kaynak_yorum_id).first()
    return sorgu.filter(Yorum.yorum_metni == yorum.yorum_metni).first()


def _yorumu_uygula(hedef: Yorum, kaynak_yorum: IslenmisYorum) -> None:
    hedef.yazar_takma_adi = kaynak_yorum.yazar_takma_adi
    hedef.yorum_metni = kaynak_yorum.yorum_metni
    hedef.kaynakta_puan = kaynak_yorum.kaynakta_puan
    hedef.yorum_tarihi = kaynak_yorum.yorum_tarihi
    hedef.dil = kaynak_yorum.dil
    hedef.duygu_skoru = kaynak_yorum.duygu_skoru
    hedef.duygu_etiketi = kaynak_yorum.duygu_etiketi.value
    hedef.konu_duygulari = [konu.model_dump(mode="json") for konu in kaynak_yorum.konu_duygulari]
    hedef.analiz_model_adi = kaynak_yorum.analiz_model_adi
    hedef.analiz_zamani = kaynak_yorum.analiz_zamani


def yorumlari_aktar(oturum: Session, islenmis_yorumlar: list[IslenmisYorum]) -> YorumAktarimSonucu:
    sonuc = YorumAktarimSonucu()
    # Ayni yorumun (orn. kaynak toplama hatasi yuzunden) TEK bir JSONL
    # dosyasinda birden fazla kez gecmesi ihtimaline karsi, bu calistirma
    # icinde islenen kayitlari da izlemek gerekir -- session autoflush kapali
    # oldugu icin (bkz. baglanti.py) DB sorgusu tek basina bunu yakalayamaz.
    bu_calistirmada_islenenler: dict[tuple, Yorum] = {}

    for kaynak_yorum in islenmis_yorumlar:
        yer = _yeri_kaynaktan_bul(oturum, kaynak_yorum.kaynak.value, kaynak_yorum.kaynak_yer_id)
        if yer is None:
            sonuc.baglanamayan += 1
            continue

        anahtar = _yorum_anahtari(yer.id, kaynak_yorum)
        var_olan = bu_calistirmada_islenenler.get(anahtar) or _var_olan_yorumu_bul(oturum, yer.id, kaynak_yorum)
        if var_olan is not None:
            _yorumu_uygula(var_olan, kaynak_yorum)
            sonuc.guncellenen += 1
        else:
            var_olan = Yorum(
                yer_id=yer.id,
                kaynak=kaynak_yorum.kaynak.value,
                kaynak_yorum_id=kaynak_yorum.kaynak_yorum_id,
            )
            _yorumu_uygula(var_olan, kaynak_yorum)
            oturum.add(var_olan)
            sonuc.eklenen += 1

        bu_calistirmada_islenenler[anahtar] = var_olan
        sonuc.etkilenen_yer_idleri.add(yer.id)

    oturum.flush()
    _duygu_skoru_ortalamalarini_guncelle(oturum, sonuc.etkilenen_yer_idleri)
    return sonuc


def _duygu_skoru_ortalamalarini_guncelle(oturum: Session, yer_idleri: set[str]) -> None:
    """Her etkilenen Yer icin `duygu_skoru_ortalama`'yi veritabanindaki
    TUM yorumlarin ortalamasiyla yeniden hesaplar (sadece bu calistirmada
    islenen yorumlarla degil) -- boylece birden fazla asamada (orn. once
    Google Maps, sonra TripAdvisor) yorum eklense bile ortalama her zaman
    dogru kalir."""
    for yer_id in yer_idleri:
        ortalama = (
            oturum.query(func.avg(Yorum.duygu_skoru)).filter(Yorum.yer_id == yer_id).scalar()
        )
        yer = oturum.get(Yer, yer_id)
        if yer is not None:
            yer.duygu_skoru_ortalama = float(ortalama) if ortalama is not None else None
    oturum.flush()
