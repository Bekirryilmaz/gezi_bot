import Link from "next/link";
import { cn } from "cn";
import { KART_KABUK } from "@/lib/kart-sinif";
import { Plaka } from "./Plaka";
import { Rozet } from "./Rozet";

export function RehberKarti({
  baslik,
  ozet,
  href,
  etiket = "Rehber",
  okumaDk,
  tarih,
  kapak,
  className,
}: {
  baslik: string;
  ozet: string;
  href: string;
  etiket?: string;
  okumaDk?: number;
  tarih?: Date | string;
  kapak?: string | null;
  className?: string;
}) {
  const tarihMetin = tarih
    ? new Intl.DateTimeFormat("tr-TR", {
        day: "numeric",
        month: "long",
        year: "numeric",
      }).format(typeof tarih === "string" ? new Date(tarih) : tarih)
    : null;

  return (
    <article className={cn(KART_KABUK, className)}>
      <Plaka kaynak={kapak} alt="" oran="kart" />
      <div className="flex min-w-0 flex-1 flex-col gap-2 p-4">
        <Rozet tur="durum">{etiket}</Rozet>
        <h3 className="min-w-0">
          <Link
            href={href}
            className="yazi-kart text-bordo group-hover:decoration-bordo/40 group-hover:underline group-hover:underline-offset-2 after:absolute after:inset-0"
          >
            {baslik}
          </Link>
        </h3>
        <p className="yazi-indeks text-ink/70 line-clamp-2 min-h-[2.5em]">{ozet}</p>
        <p className="text-ink/50 text-xs tabular-nums">
          {okumaDk != null ? `${okumaDk}\u00a0dk` : null}
          {okumaDk != null && tarihMetin ? " · " : null}
          {tarihMetin}
        </p>
      </div>
      <span className="su-hatti" />
    </article>
  );
}
