import Link from "next/link";
import { cn } from "cn";
import { CTA_IKINCIL } from "@/lib/marka";
import { KART_KABUK } from "@/lib/kart-sinif";
import { Dugme } from "./Dugme";
import { Plaka } from "./Plaka";

export type SehirKartiVaryant = "vitrin" | "izgara" | "serit";

export function SehirKarti({
  isim,
  anahtar,
  ozet,
  yerSayisi,
  ilceSayisi,
  kapak,
  plakaYerine,
  varyant = "izgara",
  className,
}: {
  isim: string;
  anahtar: string;
  ozet: string;
  yerSayisi?: number;
  ilceSayisi?: number;
  kapak?: string | null;
  /**
   * Vitrin varyantinda fotograf yokken plaka kutusunu dolduran editoryal
   * icerik (ilce indeksi gibi). Fotograf gelirse plaka geri gelir; kutu orani
   * ve kart yuksekligi degismez (yon.md 0.6).
   */
  plakaYerine?: React.ReactNode;
  varyant?: SehirKartiVaryant;
  className?: string;
}) {
  const sayiSatiri = [
    yerSayisi != null ? `${yerSayisi.toLocaleString("tr-TR")}\u00a0yer` : null,
    ilceSayisi != null ? `${ilceSayisi.toLocaleString("tr-TR")}\u00a0ilçe` : null,
  ]
    .filter(Boolean)
    .join(" · ");

  if (varyant === "vitrin") {
    return (
      <article
        className={cn("kart-kabuk grid overflow-hidden md:grid-cols-12", className)}
      >
        <div className="min-w-0 p-6 md:col-span-5 md:p-10">
          <p className="etiket text-ink/55">Şehir</p>
          <h3 className="yazi-bolum text-bordo mt-3">
            <Link href={`/sehir/${anahtar}`} className="after:absolute after:inset-0">
              {isim}
            </Link>
          </h3>
          {sayiSatiri ? (
            <p className="text-ink/55 mt-3 text-sm tabular-nums">{sayiSatiri}</p>
          ) : null}
          <p className="yazi-govde text-ink/75 mt-4 max-w-md">{ozet}</p>
          <div className="relative z-10 mt-6">
            <Dugme href={`/sehir/${anahtar}`} varyant="bolum">
              {CTA_IKINCIL}
            </Dugme>
          </div>
        </div>
        <div className="md:col-span-7">
          {!kapak && plakaYerine ? (
            plakaYerine
          ) : (
            <Plaka kaynak={kapak} alt="" oran="genis" kenarli={false} />
          )}
        </div>
        <span className="su-hatti" />
      </article>
    );
  }

  return (
    <article className={cn(KART_KABUK, className)}>
      <Plaka kaynak={kapak} alt="" oran={varyant === "serit" ? "kart" : "genis"} />
      <div className="flex min-w-0 flex-1 flex-col p-4">
        <p className="etiket text-ink/55">Şehir</p>
        <h3 className="yazi-alt text-bordo mt-2">
          <Link href={`/sehir/${anahtar}`} className="after:absolute after:inset-0">
            {isim}
          </Link>
        </h3>
        {sayiSatiri ? (
          <p className="text-ink/55 mt-2 text-xs tabular-nums">{sayiSatiri}</p>
        ) : null}
        <p className="yazi-indeks text-ink/70 mt-2 line-clamp-2 min-h-[2.5em]">{ozet}</p>
      </div>
      <span className="su-hatti" />
    </article>
  );
}
