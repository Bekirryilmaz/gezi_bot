import Link from "next/link";
import { cn } from "cn";
import { KART_KABUK } from "@/lib/kart-sinif";

export function BolgeKarti({
  ad,
  ozet,
  yerSayisi,
  href,
  className,
}: {
  ad: string;
  ozet?: string;
  yerSayisi?: number;
  href: string;
  className?: string;
}) {
  return (
    <article className={cn(KART_KABUK, "p-5", className)}>
      <p className="etiket text-ink/55">Bölge</p>
      <h3 className="yazi-alt text-bordo mt-2 min-w-0">
        <Link
          href={href}
          className="group-hover:decoration-bordo/40 group-hover:underline group-hover:underline-offset-2 after:absolute after:inset-0"
        >
          {ad}
        </Link>
      </h3>
      {yerSayisi != null ? (
        <p className="text-ink/55 mt-2 text-xs tabular-nums">
          {`${yerSayisi.toLocaleString("tr-TR")}\u00a0yer`}
        </p>
      ) : null}
      {ozet ? (
        <p className="yazi-indeks text-ink/70 mt-3 line-clamp-2 min-h-[2.5em]">{ozet}</p>
      ) : (
        <p className="min-h-[2.5em]" />
      )}
      <p className="etiket text-bordo relative z-10 mt-4">Bölgeyi tanı</p>
      <span className="su-hatti" />
    </article>
  );
}
