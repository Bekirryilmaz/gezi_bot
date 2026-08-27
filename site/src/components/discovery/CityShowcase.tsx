"use client";

import Image from "next/image";
import Link from "next/link";
import type { CityDetail } from "@/types/city";

type Props = {
  city: CityDetail;
};

export function CityShowcase({ city }: Props) {
  return (
    <article className="overflow-hidden rounded-xl bg-white shadow-[0_8px_24px_rgba(6,54,66,0.08)]">
      <div className="relative aspect-video">
        <Image
          src={city.coverImage}
          alt={city.name}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, 40vw"
          priority={city.available}
        />
      </div>
      <div className="space-y-4 p-5">
        <header className="flex flex-wrap items-center gap-3">
          <h2 className="font-display text-3xl text-deniz">{city.name}</h2>
          <span className="rounded-full bg-yosun/15 px-3 py-1 text-sm font-medium text-yosun">
            {city.region}
          </span>
        </header>
        <p className="text-sm leading-relaxed text-ink/75 md:text-base">
          {city.summary}
        </p>
        <div className="flex flex-wrap gap-2">
          {city.highlights.map((rozet) => (
            <span
              key={rozet}
              className="rounded-full bg-deniz/10 px-3 py-1 text-xs font-medium text-deniz"
            >
              {rozet}
            </span>
          ))}
        </div>
        {city.available ? (
          <Link
            href={`/sehir/${city.slug}`}
            className="inline-flex rounded-full bg-gunes px-5 py-2.5 text-sm font-semibold text-deniz-derin transition hover:brightness-105"
          >
            Şehri Keşfet →
          </Link>
        ) : (
          <p className="inline-flex rounded-full bg-ink/10 px-3 py-1.5 text-sm font-medium text-ink/55">
            Yakında Keşfe Açılacak
          </p>
        )}
      </div>
    </article>
  );
}
