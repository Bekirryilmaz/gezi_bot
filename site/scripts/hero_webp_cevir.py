"""Ham hero JPG karelerini WebP sequence'e cevirir.

- site/public/hero/kareler_ham/*.jpg -> site/public/hero/sequence/frame_XXXX.webp
- Sadece okur; ham klasore dokunmaz.
"""

from pathlib import Path

from PIL import Image

KAYNAK = Path(__file__).resolve().parents[1] / "public" / "hero" / "kareler_ham"
HEDEF = Path(__file__).resolve().parents[1] / "public" / "hero" / "sequence"
MAX_GENISLIK = 1920
KALITE = 65
STEP = 4  # her 4 karede 1 al


def main() -> None:
    dosyalar = sorted(KAYNAK.glob("*.jpg"))[::STEP]
    if not dosyalar:
        raise SystemExit(f"JPG bulunamadi: {KAYNAK}")

    # Eski ciktilari temizle
    if HEDEF.exists():
        for eski in HEDEF.glob("*.webp"):
            eski.unlink()
    HEDEF.mkdir(parents=True, exist_ok=True)

    cozunurlukler = set()
    for i, yol in enumerate(dosyalar, start=1):
        with Image.open(yol) as im:
            im = im.convert("RGB")
            if im.width > MAX_GENISLIK:
                oran = MAX_GENISLIK / im.width
                yeni = (MAX_GENISLIK, round(im.height * oran))
                im = im.resize(yeni, Image.LANCZOS)
            cozunurlukler.add(f"{im.width}x{im.height}")
            cikti = HEDEF / f"frame_{i:04d}.webp"
            im.save(cikti, "WEBP", quality=KALITE, method=6)
        if i % 100 == 0:
            print(f"{i}/{len(dosyalar)}...")

    ham_boyut = sum(p.stat().st_size for p in dosyalar)
    webp_dosyalar = sorted(HEDEF.glob("frame_*.webp"))
    webp_boyut = sum(p.stat().st_size for p in webp_dosyalar)

    print("\n=== RAPOR ===")
    print(f"Kare sayisi: {len(dosyalar)} -> {len(webp_dosyalar)}")
    print(f"Ham klasor: {ham_boyut / 1024 / 1024:.1f} MB")
    print(f"Sequence:   {webp_boyut / 1024 / 1024:.1f} MB")
    print(f"Cozunurluk: {', '.join(sorted(cozunurlukler))}")
    print(f"Ortalama kare: {webp_boyut / len(webp_dosyalar) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
