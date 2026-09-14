from __future__ import annotations

import argparse
import getpass

from sunucu.auth.rbac import ROL_YETKILERI
from sunucu.auth.servis import admin_olustur
from sunucu.veritabani.baglanti import OturumUretici


def main() -> None:
    parser = argparse.ArgumentParser(description="Ilk ic admin kullanicisini guvenli bicimde olusturur.")
    parser.add_argument("--eposta", required=True)
    parser.add_argument("--ad", required=True)
    parser.add_argument("--roller", default="yonetici")
    args = parser.parse_args()
    parola = getpass.getpass("Admin parolasi (en az 14 karakter): ")
    roller = {rol.strip() for rol in args.roller.split(",") if rol.strip()}
    bilinmeyen = roller - set(ROL_YETKILERI)
    if bilinmeyen:
        raise SystemExit(f"Bilinmeyen roller: {', '.join(sorted(bilinmeyen))}")
    with OturumUretici.begin() as oturum:
        admin_olustur(oturum, eposta=args.eposta, gorunen_ad=args.ad, parola=parola, roller=roller)
    print("Admin kullanicisi olusturuldu.")


if __name__ == "__main__":
    main()
