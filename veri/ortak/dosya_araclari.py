"""
JSONL (JSON Lines) okuma/yazma yardimci fonksiyonlari.

Neden JSONL: her satir bagimsiz bir JSON nesnesi oldugu icin (1) insan gozuyle
satir satir okunabilir, (2) toplama islemi yarida kesilse bile o ana kadar
yazilan satirlar bozulmaz, (3) yeni kayitlar dosyanin sonuna eklenebilir
(append), (4) buyuk dosyalari bellege tamamen yuklemeden isleyebiliriz.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import date, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel


def _json_donusturucu(deger: Any) -> Any:
    """json.dumps'in anlamadigi tipleri (datetime, date, Enum) metne cevirir."""
    if isinstance(deger, (datetime, date)):
        return deger.isoformat()
    if hasattr(deger, "value"):  # Enum
        return deger.value
    raise TypeError(f"'{type(deger)}' tipi JSON'a donusturulemiyor")


def jsonl_yaz(
    dosya_yolu: str | Path,
    kayitlar: list[BaseModel | dict[str, Any]],
    ekle_modu: bool = False,
) -> None:
    """Pydantic modellerinden olusan bir listeyi JSONL dosyasina yazar.

    ekle_modu=True ise dosyanin sonuna ekler (var olan veriyi silmez),
    ekle_modu=False ise dosyayi bastan yazar.
    """
    dosya_yolu = Path(dosya_yolu)
    dosya_yolu.parent.mkdir(parents=True, exist_ok=True)
    kip = "a" if ekle_modu else "w"
    with dosya_yolu.open(kip, encoding="utf-8") as dosya:
        for kayit in kayitlar:
            payload = kayit.model_dump(mode="json") if isinstance(kayit, BaseModel) else kayit
            satir = json.dumps(payload, ensure_ascii=False, default=_json_donusturucu)
            dosya.write(satir + "\n")


def jsonl_tek_satir_ekle(dosya_yolu: str | Path, kayit: BaseModel) -> None:
    """Tek bir kaydi dosyanin sonuna ekler. Uzun suren scraping islerinde
    (Google Maps, TripAdvisor gibi) her kayittan sonra diske yazmak icin
    kullanilir -- islem yarida kesilirse veri kaybi olmaz."""
    dosya_yolu = Path(dosya_yolu)
    dosya_yolu.parent.mkdir(parents=True, exist_ok=True)
    with dosya_yolu.open("a", encoding="utf-8") as dosya:
        satir = json.dumps(
            kayit.model_dump(mode="json"),
            ensure_ascii=False,
            default=_json_donusturucu,
        )
        dosya.write(satir + "\n")


def jsonl_oku(dosya_yolu: str | Path) -> Iterator[dict]:
    """Bir JSONL dosyasini satir satir okuyup sozluk (dict) olarak dondurur.

    Dosya yoksa veya bossa hicbir sey dondurmez (hata firlatmaz), cunku ilk
    calistirmada cikti dosyasi henuz olusmamis olabilir.
    """
    dosya_yolu = Path(dosya_yolu)
    if not dosya_yolu.exists():
        return
    with dosya_yolu.open("r", encoding="utf-8") as dosya:
        for satir_no, satir in enumerate(dosya, start=1):
            satir = satir.strip()
            if not satir:
                continue
            try:
                yield json.loads(satir)
            except json.JSONDecodeError as hata:
                # Bozuk bir satir yuzunden tum dosyayi kaybetmeyelim, sadece
                # uyarip devam edelim -- kalite kontrol raporunda bu tarz
                # sorunlar ayrica listelenir.
                print(f"[UYARI] {dosya_yolu} dosyasinin {satir_no}. satiri okunamadi: {hata}")


def bugunun_tarihi_dosya_adi() -> str:
    """Cikti dosyalarini tarihe gore adlandirmak icin: 2026-08-03 gibi."""
    return date.today().isoformat()
