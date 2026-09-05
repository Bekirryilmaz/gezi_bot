import Link from "next/link";
import { cn } from "cn";
import { KART_KABUK } from "@/lib/kart-sinif";

export function RotaKarti({
  gunSayisi,
  duraklar,
  eksen,
  href,
  className,
}: {
  gunSayisi: number;
  duraklar: string[];
  eksen?: string;
  href: string;
  className?: string;
}) {
  return (
    <article className={cn(KART_KABUK, "p-5", className)}>
      <p className="yazi-sayi text-bordo text-[2.5rem]">
        {gunSayisi}
        <span className="yazi-indeks text-ink/55 ml-2 font-sans font-normal">gün</span>
      </p>
      {eksen ? <p className="etiket text-ink/55 mt-2">{eksen}</p> : null}
      <ol className="mt-4 space-y-1">
        {duraklar.slice(0, 4).map((d, i) => (
          <li key={`${d}-${i}`} className="yazi-indeks text-ink/75 min-w-0 truncate">
            <span className="text-ink/40 mr-2 tabular-nums">{i + 1}</span>
            {d}
          </li>
        ))}
      </ol>
      <h3 className="mt-5">
        <Link
          href={href}
          className="etiket text-bordo group-hover:underline after:absolute after:inset-0"
        >
          Rotayı gör
        </Link>
      </h3>
      <span className="su-hatti" />
    </article>
  );
}
