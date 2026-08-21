import Link from "next/link";
import { altKategoriEtiketi, kategoriEtiketi } from "@/lib/sabitler";
import type { YerOzet } from "@/lib/types";

type Props = {
  yer: YerOzet;
};

export function YerSatiri({ yer }: Props) {
  const puan =
    yer.kaynakta_puan_ortalamasi != null
      ? yer.kaynakta_puan_ortalamasi.toFixed(1)
      : yer.duygu_skoru_ortalama != null
        ? `${(yer.duygu_skoru_ortalama * 5).toFixed(1)}*`
        : null;

  return (
    <Link
      href={`/yer/${yer.id}`}
      className="group grid grid-cols-[1fr_auto] items-baseline gap-x-4 border-b border-[var(--cizgi)] py-4 transition hover:bg-white/50"
    >
      <div>
        <h3 className="font-display text-xl text-ink transition group-hover:text-deniz md:text-2xl">
          {yer.isim}
        </h3>
        <p className="mt-1 text-sm text-ink/60">
          {kategoriEtiketi(yer.ana_kategori)}
          {" · "}
          {altKategoriEtiketi(yer.alt_kategori)}
          {yer.ilce ? ` · ${yer.ilce}` : ""}
        </p>
      </div>
      {puan ? (
        <span className="text-sm font-medium tabular-nums text-yosun">{puan}</span>
      ) : (
        <span className="text-sm text-ink/35">—</span>
      )}
    </Link>
  );
}
