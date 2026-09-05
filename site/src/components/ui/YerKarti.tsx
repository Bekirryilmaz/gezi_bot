import Link from "next/link";
import type { ReactNode } from "react";
import { cn } from "cn";
import { KART_KABUK } from "@/lib/kart-sinif";
import { altKategoriEtiketi, kategoriEtiketi } from "@/lib/sabitler";
import type { YerOzet } from "@/lib/types";
import { Plaka } from "./Plaka";
import { Rozet, RozetKati } from "./Rozet";

export function YerKarti({
  yer,
  href,
  ozet,
  sponsorlu = false,
  klasik = false,
  className,
}: {
  yer: YerOzet;
  href?: string;
  ozet?: string;
  sponsorlu?: boolean;
  klasik?: boolean;
  className?: string;
}) {
  const baglanti = href ?? `/yer/${yer.id}`;
  const puan =
    yer.kaynakta_puan_ortalamasi != null
      ? yer.kaynakta_puan_ortalamasi.toFixed(1)
      : yer.duygu_skoru_ortalama != null
        ? (yer.duygu_skoru_ortalama * 5).toFixed(1)
        : null;
  const ozetMetin = ozet ?? altKategoriEtiketi(yer.alt_kategori);
  const rozetler: ReactNode[] = [];
  if (sponsorlu) {
    rozetler.push(
      <Rozet key="sp" tur="sponsorlu">
        Sponsorlu
      </Rozet>,
    );
  }
  if (klasik) {
    rozetler.push(
      <Rozet key="kl" tur="klasik">
        Şehrin Klasiği
      </Rozet>,
    );
  }
  rozetler.push(
    <Rozet key="kat" tur="kategori">
      {kategoriEtiketi(yer.ana_kategori)}
    </Rozet>,
  );

  return (
    <article className={cn(KART_KABUK, className)}>
      <Plaka
        kaynak={yer.kapak_fotografi_url}
        alt=""
        oran="kart"
        kategori={yer.ana_kategori}
        rozet={puan ? <Rozet tur="skor">{puan}</Rozet> : null}
      />
      <div className="flex min-w-0 flex-1 flex-col gap-2 p-4">
        <h3 className="min-w-0">
          <Link
            href={baglanti}
            className="yazi-kart text-bordo group-hover:decoration-bordo/40 group-hover:underline group-hover:underline-offset-2 after:absolute after:inset-0"
          >
            {yer.isim}
          </Link>
        </h3>
        <p className="yazi-indeks text-ink/55 min-h-5 truncate">{yer.ilce ?? "\u00a0"}</p>
        <p className="yazi-indeks text-ink/70 line-clamp-2 min-h-[2.5em]">{ozetMetin}</p>
        <RozetKati ogeler={rozetler} />
      </div>
      <span className="su-hatti" />
    </article>
  );
}
