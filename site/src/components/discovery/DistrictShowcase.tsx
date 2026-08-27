"use client";

import Image from "next/image";
import Link from "next/link";
import type { DistrictDetail, KesifKategorisi } from "@/types/discovery";

const KATEGORI_ROZET: Record<KesifKategorisi, string> = {
  doga: "Doğa",
  tarih: "Tarih",
  sahil: "Sahil",
  kultur: "Kültür",
};

type Props = {
  district: DistrictDetail;
  sehirAnahtari?: string;
};

function GorselKart({
  src,
  alt,
  rozet,
  baslik,
  aciklama,
}: {
  src: string;
  alt: string;
  rozet: string;
  baslik: string;
  aciklama: string;
}) {
  return (
    <article className="overflow-hidden rounded-xl bg-white shadow-[0_8px_24px_rgba(6,54,66,0.08)]">
      <div className="relative aspect-video">
        <Image
          src={src}
          alt={alt}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, 50vw"
        />
        <span className="absolute left-3 top-3 rounded-full bg-deniz-derin/85 px-2.5 py-0.5 text-xs font-medium text-kopuk">
          {rozet}
        </span>
      </div>
      <div className="p-4">
        <h3 className="font-medium text-ink">{baslik}</h3>
        <p className="mt-1 text-sm leading-snug text-ink/65">{aciklama}</p>
      </div>
    </article>
  );
}

export function DistrictShowcase({ district, sehirAnahtari = "samsun" }: Props) {
  return (
    <section className="space-y-6">
      <header className="flex flex-wrap items-center gap-3">
        <h2 className="font-display text-3xl text-deniz md:text-4xl">{district.name}</h2>
        <span className="rounded-full bg-yosun/15 px-3 py-1 text-sm font-medium text-yosun">
          {district.vibe}
        </span>
      </header>

      <div>
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-ink/45">
          Gezilecek ve Tarihi Yerler
        </p>
        <div className="grid gap-4 md:grid-cols-2">
          {district.highlights.attractions.slice(0, 2).map((yer) => (
            <GorselKart
              key={yer.name}
              src={yer.image}
              alt={yer.name}
              rozet={KATEGORI_ROZET[yer.category]}
              baslik={yer.name}
              aciklama={yer.desc}
            />
          ))}
        </div>
      </div>

      {district.highlights.gastronomy.length > 0 ? (
        <div>
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-ink/45">
            Yöresel Lezzet
          </p>
          <div
            className={`grid gap-4 ${
              district.highlights.gastronomy.length > 1 ? "md:grid-cols-2" : ""
            }`}
          >
            {district.highlights.gastronomy.slice(0, 2).map((yemek) => (
              <GorselKart
                key={yemek.name}
                src={yemek.image}
                alt={yemek.name}
                rozet="Lezzet"
                baslik={yemek.name}
                aciklama={yemek.desc}
              />
            ))}
          </div>
        </div>
      ) : null}

      <p className="rounded-xl bg-deniz/10 px-4 py-3 text-sm text-ink/80">
        <span className="font-medium text-deniz">Turist ipucu · </span>
        {district.highlights.travelTips.tip}
      </p>

      <Link
        href={`/sehir/${sehirAnahtari}/rota?konaklama_bolge=${encodeURIComponent(district.name)}`}
        className="inline-flex rounded-full bg-gunes px-5 py-2.5 text-sm font-semibold text-deniz-derin transition hover:brightness-105"
      >
        {district.name} Üzerinden Rota Kur →
      </Link>
    </section>
  );
}
