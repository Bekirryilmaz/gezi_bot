"use client";

import Image from "next/image";
import Link from "next/link";
import type { CityDetail } from "@/types/city";
import type { RegionalEvent } from "@/types/events";
import { KATEGORI_ETIKET } from "@/types/events";
import { REGIONAL_EVENTS } from "@/data/regionalEvents";
import {
  formatTarihKisa,
  getEventStatus,
  getNearestEventForCity,
} from "@/utils/eventDateUtils";

type Props = {
  city: CityDetail;
  onTakvimeGit: (etkinlikId?: string) => void;
};

function SpotlightKart({
  event,
  onTakvimeGit,
}: {
  event: RegionalEvent;
  onTakvimeGit: (etkinlikId?: string) => void;
}) {
  const durum = getEventStatus(event.startDate, event.endDate);
  const tarih = formatTarihKisa(event.startDate);
  const devam = durum.kind === "devam";
  const sayac = devam
    ? "Şu an Devam Ediyor!"
    : `${durum.daysUntilStart} Gün Kaldı`;

  return (
    <button
      type="button"
      onClick={() => onTakvimeGit(event.id)}
      className="w-full rounded-xl border-2 border-amber-400 bg-amber-50/50 p-3.5 text-left shadow-[0_8px_24px_rgba(245,158,11,0.18)] transition duration-200 hover:-translate-y-0.5 dark:bg-amber-950/20"
    >
      <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-amber-700">
        {devam || durum.kind === "yakin"
          ? "🎉 Festival zamanı yaklaşıyor"
          : "🔥 Bu ilde sıradaki etkinlik"}
      </p>
      <div className="mt-2.5 flex gap-3">
        <div className="flex h-[4.25rem] w-[4.25rem] shrink-0 flex-col items-center justify-center rounded-xl bg-teal-700 text-white shadow-sm">
          <span className="font-display text-2xl leading-none">{tarih.gun}</span>
          <span className="mt-0.5 text-[10px] font-semibold uppercase tracking-wide text-white/80">
            {tarih.ay}
          </span>
        </div>
        <div className="min-w-0 space-y-1.5">
          <h3 className="font-display text-lg leading-snug text-deniz">
            {event.title}
          </h3>
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="rounded-full bg-teal-700/10 px-2 py-0.5 text-[11px] font-medium text-teal-800">
              {KATEGORI_ETIKET[event.category]}
            </span>
            <span
              className={`rounded-full px-2 py-0.5 text-[11px] font-semibold ${durum.className}`}
            >
              {sayac}
            </span>
          </div>
        </div>
      </div>
    </button>
  );
}

export function CityShowcase({ city, onTakvimeGit }: Props) {
  const siradaki = getNearestEventForCity(REGIONAL_EVENTS, city.slug);

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

        {siradaki ? (
          <SpotlightKart event={siradaki} onTakvimeGit={onTakvimeGit} />
        ) : (
          <p className="rounded-lg border border-deniz/10 bg-kopuk/70 px-3 py-2.5 text-sm leading-relaxed text-ink/70">
            Bu il için yakın tarihte festival bulunmuyor.
          </p>
        )}

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
