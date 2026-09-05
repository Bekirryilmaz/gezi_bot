import { CTA_BIRINCIL, CTA_IKINCIL, SLOGAN, TANIM_CUMLESI } from "@/lib/marka";
import { DENEYIM_EKSENLERI } from "@/lib/sabitler";
import { Dugme } from "@/components/ui/Dugme";
import { Plaka } from "@/components/ui/Plaka";

export function HeroKapak({
  sehirAnahtari = "samsun",
  yerSayisi = 0,
}: {
  sehirAnahtari?: string;
  yerSayisi?: number;
}) {
  const kanit = [
    yerSayisi > 0 ? `${yerSayisi.toLocaleString("tr-TR")}\u00a0yer` : null,
    `${DENEYIM_EKSENLERI.length}\u00a0deneyim ekseni`,
  ]
    .filter(Boolean)
    .join(" · ");

  return (
    <section className="bg-kagit pt-24 md:pt-28">
      <div className="kabuk grid items-end gap-10 pb-16 md:grid-cols-12 md:pb-24">
        <div className="md:col-span-5">
          <p className="etiket text-ink/55">Gezi rehberi</p>
          <h1 className="yazi-kapak text-bordo mt-3 max-w-xl">
            {SLOGAN.replace(/\.$/, "")}
          </h1>
          <p className="yazi-govde text-ink/80 mt-6 max-w-xl">{TANIM_CUMLESI}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Dugme href={`/sehir/${sehirAnahtari}/rota`} varyant="birincil">
              {CTA_BIRINCIL}
            </Dugme>
            <Dugme href={`/sehir/${sehirAnahtari}`} varyant="ikincil">
              {CTA_IKINCIL}
            </Dugme>
          </div>
          {kanit ? (
            <p className="text-ink/55 mt-6 text-sm tabular-nums">{kanit}</p>
          ) : null}
        </div>
        <div className="md:col-span-7" aria-hidden="true">
          <Plaka oran="hero" kenarli={false} className="md:w-[calc(100%+4rem)]" />
        </div>
      </div>
    </section>
  );
}
