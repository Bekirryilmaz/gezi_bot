"""
Genel duygu analizi modeli sarmalayicisi (wrapper).

Acik kaynak, ucretsiz, sunucumuzda (Oracle Ampere ARM, CPU-only) calisabilecek
onceden egitilmis bir Turkce BERT modeli kullanilir -- kendi modelimizi
egitmek (buyuk etiketli veri + GPU gerektirir) bu projenin kapsaminda/
butcesinde degil.

Secilen model: incidelen/bert-base-turkish-sentiment-analysis-128k-cased
- BERTurk (dbmdz/bert-base-turkish-cased) uzerine, 150.000 Turkce e-ticaret
  yorumundan olusan DENGELI bir veri setiyle (TRSAv1) fine-tune edilmis.
- UC SINIFLI (Negative/Neutral/Positive) -- bizim DuyguEtiketi enum'umuzla
  (OLUMSUZ/NOTR/OLUMLU) DOGRUDAN eslesir. Bircok Turkce sentiment modeli
  (orn. savasy/bert-base-turkish-sentiment-cased) SADECE IKI SINIFLIDIR
  (olumlu/olumsuz), bu da "notr" yorumlari yapay bir esikle tahmin etmeyi
  gerektirirdi -- 3 sinifli bir model dogal olarak daha dogru.
- Apache/MIT tarzi acik lisansli, HuggingFace Hub'dan ucretsiz indirilir,
  CPU uzerinde makul hizda calisir (bert-base boyutunda, ~110M parametre).

Ilk calistirmada model (~440MB) HuggingFace'ten indirilip
~/.cache/huggingface/ altina kaydedilir, sonraki calistirmalarda internet
gerekmez (Oracle sunucuda tek seferlik indirme sonrasi offline calisir).
"""

from __future__ import annotations

from functools import lru_cache

from transformers import pipeline

from ortak.sabitler import DuyguEtiketi

MODEL_ADI = "incidelen/bert-base-turkish-sentiment-analysis-128k-cased"

_ETIKET_ESLEME: dict[str, DuyguEtiketi] = {
    "positive": DuyguEtiketi.OLUMLU,
    "negative": DuyguEtiketi.OLUMSUZ,
    "neutral": DuyguEtiketi.NOTR,
}


@lru_cache(maxsize=1)
def _siniflandirici():
    """Modeli sadece BIR KEZ yukler (agir bir islem, ~birkac saniye) ve
    tekrar tekrar kullanir. lru_cache ile "singleton" davranisi saglanir."""
    print(f"[BILGI] Duygu analizi modeli yukleniyor: {MODEL_ADI} (ilk calistirmada indirilir, biraz surebilir)...")
    return pipeline("text-classification", model=MODEL_ADI, top_k=None, truncation=True, max_length=256)


def duygu_tahmin_et(metin: str) -> tuple[DuyguEtiketi, float]:
    """Bir metnin genel duygusunu tahmin eder.

    Doner: (duygu_etiketi, duygu_skoru)
      - duygu_etiketi: OLUMLU / NOTR / OLUMSUZ (modelin en yuksek olasilikli sinifi)
      - duygu_skoru: -1 (tamamen olumsuz) ile +1 (tamamen olumlu) arasi SUREKLI
        bir deger. P(olumlu) - P(olumsuz) olarak hesaplanir -- boylece "notr"
        agirlikli ama hafif olumlu/olumsuz egilimli yorumlar da ayirt edilebilir
        (sadece 3 kategoriye sikismak yerine).
    """
    if not metin or not metin.strip():
        return DuyguEtiketi.NOTR, 0.0

    sonuclar = _siniflandirici()(metin)[0]  # [{'label': 'Positive', 'score': 0.9}, ...]
    olasiliklar = {s["label"].lower(): s["score"] for s in sonuclar}

    en_yuksek_etiket = max(sonuclar, key=lambda s: s["score"])["label"].lower()
    duygu_etiketi = _ETIKET_ESLEME.get(en_yuksek_etiket, DuyguEtiketi.NOTR)

    duygu_skoru = olasiliklar.get("positive", 0.0) - olasiliklar.get("negative", 0.0)
    duygu_skoru = max(-1.0, min(1.0, round(duygu_skoru, 4)))

    return duygu_etiketi, duygu_skoru


def toplu_duygu_tahmin_et(metinler: list[str], yigin_boyutu: int = 16) -> list[tuple[DuyguEtiketi, float]]:
    """Coklu metni, tek tek cagirmaktan daha verimli sekilde (model
    yiginlar/batch halinde calistirilarak) isler. Uzun listelerde
    (binlerce yorum) performans farki onemlidir."""
    if not metinler:
        return []

    siniflandirici = _siniflandirici()
    sonuclar: list[tuple[DuyguEtiketi, float]] = []

    for baslangic in range(0, len(metinler), yigin_boyutu):
        yigin = metinler[baslangic : baslangic + yigin_boyutu]
        # Bos metinleri modele gondermeden once isaretleyip sonradan NOTR ata --
        # bos string modelin tokenizer'inda hataya yol acabilir.
        gecerli_indeksler = [i for i, m in enumerate(yigin) if m and m.strip()]
        yigin_sonuclari = [None] * len(yigin)

        if gecerli_indeksler:
            model_ciktisi = siniflandirici([yigin[i] for i in gecerli_indeksler])
            for konum, i in enumerate(gecerli_indeksler):
                olasiliklar = {s["label"].lower(): s["score"] for s in model_ciktisi[konum]}
                en_yuksek_etiket = max(model_ciktisi[konum], key=lambda s: s["score"])["label"].lower()
                duygu_etiketi = _ETIKET_ESLEME.get(en_yuksek_etiket, DuyguEtiketi.NOTR)
                duygu_skoru = max(
                    -1.0, min(1.0, round(olasiliklar.get("positive", 0.0) - olasiliklar.get("negative", 0.0), 4))
                )
                yigin_sonuclari[i] = (duygu_etiketi, duygu_skoru)

        for i in range(len(yigin)):
            if yigin_sonuclari[i] is None:
                yigin_sonuclari[i] = (DuyguEtiketi.NOTR, 0.0)

        sonuclar.extend(yigin_sonuclari)

    return sonuclar
