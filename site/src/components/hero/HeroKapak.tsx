import { CTA_BIRINCIL, CTA_IKINCIL, SLOGAN, TANIM_CUMLESI } from "@/lib/marka";
import { Dugme } from "@/components/ui/Dugme";

export function HeroKapak({ sehirAnahtari = "samsun" }: { sehirAnahtari?: string }) {
  return (
    <section className="bg-kagit pt-24 md:pt-28">
      <div className="mx-auto grid max-w-6xl items-end gap-10 px-5 pb-16 md:grid-cols-12 md:px-8 md:pb-24">
        <div className="md:col-span-5">
          <p className="text-ink/55 text-[11px] tracking-[0.24em] uppercase">
            Gezi rehberi
          </p>
          <h1 className="font-display mt-3 max-w-xl text-[2.35rem] leading-[0.98] tracking-[-0.03em] text-balance sm:text-5xl md:text-6xl lg:text-[5.5rem]">
            {SLOGAN.replace(/\.$/, "")}
          </h1>
          <p className="text-ink/80 mt-6 max-w-xl text-[16px] leading-relaxed text-pretty md:text-[17px]">
            {TANIM_CUMLESI}
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Dugme href={`/sehir/${sehirAnahtari}/rota`} varyant="birincil">
              {CTA_BIRINCIL}
            </Dugme>
            <Dugme href={`/sehir/${sehirAnahtari}`} varyant="ikincil">
              {CTA_IKINCIL}
            </Dugme>
          </div>
        </div>
        <div className="md:col-span-7">
          <div
            className="bg-kagit-koyu aspect-[4/5] w-full md:aspect-[4/3] md:h-[min(78vh,640px)] md:w-[calc(100%+4rem)]"
            aria-hidden="true"
          />
        </div>
      </div>
    </section>
  );
}
