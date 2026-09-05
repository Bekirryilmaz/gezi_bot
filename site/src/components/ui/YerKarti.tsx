import Link from "next/link";
import Image from "next/image";
import { cn } from "cn";
import { altKategoriEtiketi, kategoriEtiketi } from "@/lib/sabitler";
import type { YerOzet } from "@/lib/types";
import { Rozet } from "./Rozet";

export function YerKarti({ yer, className }: { yer: YerOzet; className?: string }) {
  const puan =
    yer.kaynakta_puan_ortalamasi != null
      ? yer.kaynakta_puan_ortalamasi.toFixed(1)
      : yer.duygu_skoru_ortalama != null
        ? (yer.duygu_skoru_ortalama * 5).toFixed(1)
        : null;

  return (
    <Link
      href={`/yer/${yer.id}`}
      className={cn(
        "group kart-isik border-deniz/10 focus-visible:ring-samandira relative flex cursor-pointer flex-col overflow-hidden rounded-2xl border bg-white transition-[transform,box-shadow] duration-200 hover:-translate-y-0.5 hover:shadow-[0_12px_40px_-18px_rgba(6,54,66,0.35)] focus-visible:ring-2 focus-visible:outline-none",
        className,
      )}
    >
      <div className="from-deniz to-deniz-derin relative aspect-[16/9] overflow-hidden bg-gradient-to-br">
        {yer.kapak_fotografi_url?.startsWith("/") ? (
          <Image
            src={yer.kapak_fotografi_url}
            alt=""
            fill
            sizes="(max-width: 768px) 100vw, 33vw"
            className="object-cover transition-transform duration-500 group-hover:scale-[1.03]"
          />
        ) : (
          <div
            className="absolute inset-0 opacity-40"
            style={{
              background:
                "radial-gradient(circle at 70% 20%, #d6402c55, transparent 45%), linear-gradient(160deg, #0a4d5c, #063642)",
            }}
            aria-hidden="true"
          />
        )}
        {puan ? (
          <span className="bg-kagit/95 text-deniz-derin absolute top-3 right-3 rounded-full px-2.5 py-1 text-xs font-semibold tabular-nums">
            {puan}
          </span>
        ) : null}
      </div>
      <div className="flex flex-1 flex-col gap-2 p-4">
        <h3 className="font-display text-deniz-derin group-hover:text-deniz text-xl leading-snug tracking-[-0.01em]">
          {yer.isim}
        </h3>
        <div className="mt-auto flex flex-wrap items-center gap-1.5">
          <Rozet ton="sis">{kategoriEtiketi(yer.ana_kategori)}</Rozet>
          {yer.ilce ? <Rozet ton="deniz">{yer.ilce}</Rozet> : null}
          <span className="text-ink/45 text-[11px]">
            {altKategoriEtiketi(yer.alt_kategori)}
          </span>
        </div>
      </div>
    </Link>
  );
}
