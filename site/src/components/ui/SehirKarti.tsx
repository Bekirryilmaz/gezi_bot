import Link from "next/link";
import { cn } from "cn";
import { Dugme } from "./Dugme";

export function SehirKarti({
  isim,
  anahtar,
  ozet,
  yerSayisi,
  className,
}: {
  isim: string;
  anahtar: string;
  ozet: string;
  yerSayisi?: number;
  className?: string;
}) {
  return (
    <article
      className={cn(
        "border-deniz/10 flex flex-col rounded-2xl border bg-white p-6",
        className,
      )}
    >
      <p className="text-kumsal text-[11px] tracking-[0.24em] uppercase">Şehir</p>
      <h3 className="font-display text-deniz-derin mt-2 text-3xl tracking-[-0.02em]">
        <Link
          href={`/sehir/${anahtar}`}
          className="hover:text-deniz focus-visible:ring-samandira cursor-pointer focus-visible:ring-2 focus-visible:outline-none"
        >
          {isim}
        </Link>
      </h3>
      <p className="text-ink/70 mt-3 flex-1 text-sm leading-relaxed">{ozet}</p>
      {yerSayisi != null ? (
        <p className="text-ink/45 mt-4 text-xs tabular-nums">{yerSayisi} yer işaretli</p>
      ) : null}
      <div className="mt-5 flex flex-wrap gap-2">
        <Dugme href={`/sehir/${anahtar}`} varyant="ikincil">
          Keşfet
        </Dugme>
        <Dugme href={`/sehir/${anahtar}/rota`} varyant="hayalet">
          Rotanı kur
        </Dugme>
      </div>
    </article>
  );
}
