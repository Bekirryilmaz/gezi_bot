import { Suspense } from "react";
import { CTA_BIRINCIL, CTA_IKINCIL, SLOGAN, TANIM_CUMLESI } from "@/lib/marka";
import { Dugme } from "@/components/ui/Dugme";
import { Manyetik } from "@/components/hareket/Manyetik";
import { istatistikleriGetir } from "@/lib/api";
import { KAPAK_MASAUSTU, KAPAK_MOBIL } from "@/lib/hero-kapak";
import type { SehirIstatistikleri } from "@/lib/types";
import { HeroUfukGecikmeli } from "./HeroUfukGecikmeli";

function kanitSatiri(i: SehirIstatistikleri | null): string | undefined {
  if (!i || i.yer_sayisi === 0) return undefined;
  const sayi = (n: number) => n.toLocaleString("tr-TR");
  return `${sayi(i.yer_sayisi)} işaretli yer · ${sayi(i.ilce_sayisi)} ilçe · ${sayi(
    i.bolge_profili_sayisi,
  )} bölge profili`;
}

async function HeroKanit({ sehirAnahtari }: { sehirAnahtari: string }) {
  const istatistik = await istatistikleriGetir(sehirAnahtari).catch(() => null);
  const kanit = kanitSatiri(istatistik);
  if (!kanit) return null;
  return (
    <p className="border-bordo/12 text-ink/55 mt-10 border-t pt-4 text-sm tabular-nums">
      {kanit}
    </p>
  );
}

const KAPAK_SINIF =
  "hero-kapak-gorsel absolute inset-0 size-full object-cover motion-reduce:transform-none";

function HeroKapakGorsel() {
  return (
    <picture>
      <source media="(min-width: 768px)" srcSet={KAPAK_MASAUSTU.avif} type="image/avif" />
      <source media="(min-width: 768px)" srcSet={KAPAK_MASAUSTU.webp} type="image/webp" />
      <source srcSet={KAPAK_MOBIL.avif} type="image/avif" />
      <img
        src={KAPAK_MOBIL.webp}
        alt=""
        width={KAPAK_MOBIL.genislik}
        height={KAPAK_MOBIL.yukseklik}
        fetchPriority="high"
        decoding="sync"
        className={KAPAK_SINIF}
      />
    </picture>
  );
}

/**
 * yon-v2 2.1 — asimetrik split: metin sol 5/12, plaka sag 7/12.
 * Kapak tek statik kare (LCP); hareket HeroUfuk kanvasindan.
 */
export function HeroKapak({ sehirAnahtari = "samsun" }: { sehirAnahtari?: string }) {
  return (
    <section className="hero-kapak bg-kagit relative flex flex-col overflow-x-clip pt-14 md:pt-16 lg:block">
      <link
        rel="preload"
        as="image"
        href={KAPAK_MOBIL.avif}
        type="image/avif"
        media="(max-width: 767px)"
        fetchPriority="high"
      />
      <link
        rel="preload"
        as="image"
        href={KAPAK_MASAUSTU.avif}
        type="image/avif"
        media="(min-width: 768px)"
        fetchPriority="high"
      />
      <div className="kabuk relative order-2 grid lg:order-none lg:grid-cols-12">
        <div className="pt-8 pb-14 md:pt-10 md:pb-16 lg:col-span-5 lg:flex lg:min-h-[calc(78vh+3rem)] lg:flex-col lg:justify-center lg:py-0">
          <p className="etiket text-ink/55">Gezi rehberi</p>
          <h1 className="yazi-hero text-bordo mt-4">{SLOGAN}</h1>
          <p className="yazi-govde text-ink/80 mt-6 max-w-[34rem]">{TANIM_CUMLESI}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Manyetik>
              <Dugme href={`/sehir/${sehirAnahtari}/rota`} varyant="birincil">
                {CTA_BIRINCIL}
              </Dugme>
            </Manyetik>
            <Dugme href={`/sehir/${sehirAnahtari}`} varyant="ikincil">
              {CTA_IKINCIL}
            </Dugme>
          </div>
          <Suspense fallback={null}>
            <HeroKanit sehirAnahtari={sehirAnahtari} />
          </Suspense>
        </div>
      </div>

      <div
        className="hero-plaka plaka-murekkep bg-kagit-koyu order-1 mt-4 aspect-[4/5] max-h-[46svh] sm:aspect-[16/10] sm:max-h-[44svh] lg:order-none lg:mt-0 lg:aspect-auto lg:max-h-none"
        aria-hidden="true"
      >
        <HeroKapakGorsel />
        <HeroUfukGecikmeli className="pointer-events-none absolute inset-0 size-full motion-reduce:hidden" />
        <div className="hero-ufuk-logo" aria-hidden="true">
          <img
            src="/logo/karo-seffaf.png"
            alt=""
            width={80}
            height={80}
            decoding="async"
            loading="lazy"
            fetchPriority="low"
          />
          <span className="hero-ufuk-nabiz" />
        </div>
        <span className="hero-ufuk-grain" />
      </div>
    </section>
  );
}
