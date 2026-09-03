"use client";

import { useEffect, useMemo } from "react";
import Image from "next/image";
import { AnimatePresence, motion } from "framer-motion";
import { CalendarDays, MapPin, Ticket } from "lucide-react";
import { SeciciMenu } from "@/components/oneri/SeciciMenu";
import { REGIONAL_EVENTS } from "@/data/regionalEvents";
import { TURKIYE_SEHIRLERI } from "@/data/cities";
import {
  KATEGORI_ETIKET,
  type RegionalEvent,
  type TicketOrAccess,
} from "@/types/events";
import {
  etkinlikSirala,
  formatTarihAraligi,
  formatTarihKisa,
  getEventStatus,
  getNearestEventForCity,
} from "@/utils/eventDateUtils";

const BILET_ETIKET: Record<TicketOrAccess, string> = {
  Ucretsiz: "Ücretsiz",
  Biletli: "Biletli",
  "Katılıma Açık": "Katılıma Açık",
};

const IL_SECENEKLERI = [
  { id: "tumu", etiket: "Tüm Türkiye (Tüm Etkinlikler)", ikon: "📍" },
  ...[...TURKIYE_SEHIRLERI]
    .sort((a, b) => a.name.localeCompare(b.name, "tr"))
    .map((il) => ({ id: il.slug, etiket: il.name })),
];

function EtkinlikKarti({
  event,
  vurgulu,
  odakli,
  onSec,
}: {
  event: RegionalEvent;
  vurgulu: boolean;
  odakli: boolean;
  onSec: (event: RegionalEvent) => void;
}) {
  const durum = getEventStatus(event.startDate, event.endDate);
  const tarih = formatTarihKisa(event.startDate);

  return (
    <article
      id={`etkinlik-kart-${event.id}`}
      className={`overflow-hidden rounded-xl bg-white shadow-[0_8px_24px_rgba(6,54,66,0.08)] transition duration-200 hover:-translate-y-1 ${
        vurgulu
          ? "ring-2 ring-teal-600 ring-offset-2"
          : odakli
            ? "ring-2 ring-amber-400"
            : ""
      }`}
    >
      <button
        type="button"
        onClick={() => onSec(event)}
        className="flex w-full flex-col text-left sm:flex-row"
      >
        <div className="flex shrink-0 flex-row items-center gap-3 bg-teal-700 px-4 py-3 text-white sm:w-[5.5rem] sm:flex-col sm:justify-center sm:gap-0 sm:px-3 sm:py-6">
          <span className="font-display text-3xl leading-none">{tarih.gun}</span>
          <span className="text-xs font-semibold uppercase tracking-wide text-white/80">
            {tarih.ay}
          </span>
        </div>
        <div className="min-w-0 flex-1">
          <div className="relative aspect-[16/9] sm:aspect-[2/1]">
            {event.imageUrl ? (
              <Image
                src={event.imageUrl}
                alt={event.title}
                fill
                className="object-cover"
                sizes="(max-width: 768px) 100vw, (max-width: 1280px) 50vw, 33vw"
              />
            ) : (
              <div className="h-full w-full bg-kopuk" />
            )}
            <span className="absolute left-3 top-3 rounded-full bg-deniz-derin/88 px-2.5 py-1 text-[11px] font-medium text-kopuk">
              {KATEGORI_ETIKET[event.category]}
            </span>
            <span
              className={`absolute right-3 top-3 rounded-full px-2.5 py-1 text-[11px] font-semibold ${durum.className}`}
            >
              {durum.label}
            </span>
          </div>
          <div className="space-y-2 p-4">
            <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-amber-600">
              {event.badge}
            </p>
            <h3 className="font-display text-xl leading-snug text-deniz">
              {event.title}
            </h3>
            <p className="flex items-center gap-1.5 text-sm text-ink/60">
              <MapPin className="h-3.5 w-3.5 shrink-0 text-yosun" aria-hidden />
              {event.district
                ? `${event.cityName} · ${event.district}`
                : event.cityName}
            </p>
            <p className="line-clamp-2 text-sm leading-snug text-ink/70">
              {event.summary}
            </p>
            <div className="flex flex-wrap items-center gap-2 text-[11px] text-ink/65">
              <span className="inline-flex items-center gap-1 rounded-full bg-kopuk px-2 py-1">
                <CalendarDays className="h-3.5 w-3.5" aria-hidden />
                {formatTarihAraligi(event.startDate, event.endDate)}
              </span>
              <span className="inline-flex items-center gap-1 rounded-full bg-kopuk px-2 py-1">
                <Ticket className="h-3.5 w-3.5" aria-hidden />
                {BILET_ETIKET[event.ticketOrAccess]}
              </span>
            </div>
          </div>
        </div>
      </button>
    </article>
  );
}

export function EventCalendarSection({
  selectedCitySlug,
  odakEtkinlikId,
  odakSayac,
  onCityChange,
  onEtkinlikSec,
}: {
  selectedCitySlug: string | null;
  odakEtkinlikId: string | null;
  odakSayac: number;
  onCityChange: (citySlug: string | null) => void;
  onEtkinlikSec: (event: RegionalEvent) => void;
}) {
  useEffect(() => {
    if (odakSayac === 0) return;
    const t = window.setTimeout(() => {
      const hedef = odakEtkinlikId
        ? document.getElementById(`etkinlik-kart-${odakEtkinlikId}`)
        : document.getElementById("festival-takvimi");
      hedef?.scrollIntoView({
        behavior: "smooth",
        block: odakEtkinlikId ? "center" : "start",
      });
    }, 120);
    return () => window.clearTimeout(t);
  }, [odakSayac, odakEtkinlikId]);

  const { liste, enYakinId } = useMemo(() => {
    const ham = selectedCitySlug
      ? REGIONAL_EVENTS.filter((e) => e.citySlug === selectedCitySlug)
      : REGIONAL_EVENTS;

    const sirali = etkinlikSirala(ham);
    const enYakin = selectedCitySlug
      ? getNearestEventForCity(ham, selectedCitySlug)
      : null;

    if (!enYakin) {
      return { liste: sirali, enYakinId: null as string | null };
    }

    return {
      liste: [enYakin, ...sirali.filter((e) => e.id !== enYakin.id)],
      enYakinId: enYakin.id,
    };
  }, [selectedCitySlug]);

  return (
    <section id="festival-takvimi" className="space-y-6 scroll-mt-24">
      <header className="max-w-3xl">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-ink/45">
          Etkinlikler & Festival Takvimi
        </p>
        <h2 className="mt-2 font-display text-3xl text-deniz md:text-4xl">
          Türkiye Kültür, Sanat & Festival Takvimi
        </h2>
        <p className="mt-3 text-sm leading-relaxed text-ink/70 md:text-base">
          Dönemsel festivaller, hasat şenlikleri ve Kültür Yolu durakları. Bir
          karta dokununca harita o ile uçar.
        </p>
      </header>

      <div className="relative z-20 mx-auto my-2 w-full max-w-xl">
        <div className="relative flex items-center rounded-2xl border border-teal-100/80 bg-white p-2 shadow-sm transition-all focus-within:ring-2 focus-within:ring-teal-600">
          <MapPin className="ml-3 h-5 w-5 shrink-0 text-teal-600" aria-hidden />
          <span className="ml-2 hidden shrink-0 text-sm font-medium text-slate-500 sm:inline">
            Şehir Seçin
          </span>
          <div className="min-w-0 flex-1">
            <SeciciMenu
              etiket=""
              yerTutucu="Şehir seçin"
              deger={selectedCitySlug ?? "tumu"}
              secenekler={IL_SECENEKLERI}
              onSec={(id) => onCityChange(id === "tumu" ? null : id)}
            />
          </div>
        </div>
      </div>

      <AnimatePresence mode="wait">
        {liste.length === 0 ? (
          <motion.p
            key={`bos-${selectedCitySlug ?? "tumu"}`}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.3 }}
            className="rounded-xl border border-deniz/10 bg-white p-6 text-sm text-ink/65"
          >
            Bu il için planlanmış etkinlik bulunmamaktadır.
          </motion.p>
        ) : (
          <motion.div
            key={`liste-${selectedCitySlug ?? "tumu"}`}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.3 }}
            className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3"
          >
            {liste.map((event) => (
              <EtkinlikKarti
                key={event.id}
                event={event}
                vurgulu={event.id === enYakinId}
                odakli={odakEtkinlikId === event.id}
                onSec={onEtkinlikSec}
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
