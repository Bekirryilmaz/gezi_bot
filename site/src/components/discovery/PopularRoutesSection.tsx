"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Image from "next/image";
import { ChevronDown, Clock, Compass, Footprints, Car, MapPin } from "lucide-react";
import {
  POPULER_ROTALAR,
  type PopularRoute,
} from "@/data/popularRoutes";

type Filtre = "tumu" | "trekking" | "roadtrip" | "kultur_doga";

const FILTRELER: { id: Filtre; etiket: string }[] = [
  { id: "tumu", etiket: "Tümü" },
  { id: "trekking", etiket: "Ödüllü Yürüyüş Yolları" },
  { id: "roadtrip", etiket: "Manzaralı Yolculuklar (Road Trip)" },
  { id: "kultur_doga", etiket: "Kültür & Doğa" },
];

const MASAUSTU_SORGU = "(min-width: 1024px)";

function filtreyeUyan(rota: PopularRoute, filtre: Filtre): boolean {
  if (filtre === "tumu") return true;
  if (filtre === "trekking") return rota.category === "trekking";
  if (filtre === "roadtrip") return rota.category === "roadtrip";
  return rota.category === "kultur_tren" || rota.category === "doga_kanyon";
}

function ZorlukRozeti({ seviye }: { seviye: PopularRoute["difficulty"] }) {
  const sinif =
    seviye === "Kolay"
      ? "bg-yosun/15 text-yosun"
      : seviye === "Orta"
        ? "bg-deniz/10 text-deniz"
        : "bg-bordo/12 text-bordo";
  return (
    <span className={`rounded-full px-2 py-0.5 text-[11px] font-medium ${sinif}`}>
      {seviye}
    </span>
  );
}

function KategoriIkon({ category }: { category: PopularRoute["category"] }) {
  const sinif = "h-3.5 w-3.5 shrink-0";
  if (category === "roadtrip") return <Car className={sinif} aria-hidden />;
  if (category === "kultur_tren") return <Compass className={sinif} aria-hidden />;
  return <Footprints className={sinif} aria-hidden />;
}

function RotaKarti({
  rota,
  secili,
  onSec,
  gorselYukle,
}: {
  rota: PopularRoute;
  secili: boolean;
  onSec: (rota: PopularRoute) => void;
  gorselYukle: boolean;
}) {
  return (
    <article
      id={`rota-kart-${rota.id}`}
      className={`overflow-hidden rounded-xl bg-white shadow-[0_8px_24px_rgba(6,54,66,0.08)] transition duration-300 hover:-translate-y-1 ${
        secili ? "ring-2 ring-deniz" : ""
      }`}
    >
      <button
        type="button"
        onClick={() => onSec(rota)}
        className="w-full text-left"
      >
      <div className="relative aspect-video bg-kopuk">
        {gorselYukle ? (
          <Image
            src={rota.imageUrl}
            alt={rota.title}
            fill
            loading="lazy"
            className="object-cover"
            sizes="(max-width: 768px) 100vw, (max-width: 1280px) 50vw, 25vw"
          />
        ) : null}
        <span className="absolute left-3 top-3 max-w-[85%] rounded-full bg-deniz-derin/88 px-2.5 py-1 text-[11px] font-medium leading-snug text-kopuk">
          {rota.badge}
        </span>
      </div>
      <div className="space-y-3 p-4">
        <header>
          <h3 className="font-display text-xl text-deniz">{rota.title}</h3>
          <p className="mt-1 flex items-center gap-1.5 text-sm text-ink/60">
            <MapPin className="h-3.5 w-3.5 shrink-0 text-yosun" aria-hidden />
            {rota.location}
          </p>
        </header>
        <div className="flex flex-wrap items-center gap-2 text-xs text-ink/70">
          <span className="inline-flex items-center gap-1 rounded-full bg-kopuk px-2 py-1">
            <Clock className="h-3.5 w-3.5" aria-hidden />
            {rota.duration}
          </span>
          <span className="inline-flex items-center gap-1 rounded-full bg-kopuk px-2 py-1">
            <Compass className="h-3.5 w-3.5" aria-hidden />
            {rota.distance}
          </span>
          <span className="inline-flex items-center gap-1 rounded-full bg-kopuk px-2 py-1">
            <KategoriIkon category={rota.category} />
            <ZorlukRozeti seviye={rota.difficulty} />
          </span>
        </div>
        <p className="line-clamp-2 text-sm leading-snug text-ink/70">{rota.summary}</p>
        <div className="flex flex-wrap gap-1.5">
          {rota.highlights.map((nokta) => (
            <span
              key={nokta}
              className="rounded-full bg-deniz/10 px-2 py-0.5 text-[11px] font-medium text-deniz"
            >
              {nokta}
            </span>
          ))}
        </div>
        <p className="text-xs font-medium text-yosun">{rota.bestSeason}</p>
      </div>
      </button>
      <div className="px-4 pb-4">
        <button
          type="button"
          onClick={() => onSec(rota)}
          className="rounded-full bg-deniz px-3.5 py-1.5 text-xs font-semibold text-white transition hover:bg-deniz-derin"
        >
          Haritada Gör
        </button>
      </div>
    </article>
  );
}

export function PopularRoutesSection({
  activeRouteId,
  onSelectRoute,
}: {
  activeRouteId: string | null;
  onSelectRoute: (rota: PopularRoute) => void;
}) {
  const bolumRef = useRef<HTMLElement>(null);
  const [filtre, setFiltre] = useState<Filtre>("tumu");
  const [isExpanded, setIsExpanded] = useState(false);

  const rotalar = useMemo(
    () => POPULER_ROTALAR.filter((r) => filtreyeUyan(r, filtre)),
    [filtre],
  );

  useEffect(() => {
    const mq = window.matchMedia(MASAUSTU_SORGU);
    setIsExpanded(mq.matches);
  }, []);

  useEffect(() => {
    if (activeRouteId) setIsExpanded(true);
  }, [activeRouteId]);

  function acKapa() {
    setIsExpanded((onceki) => {
      const yeni = !onceki;
      if (yeni && !window.matchMedia(MASAUSTU_SORGU).matches) {
        window.requestAnimationFrame(() => {
          bolumRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        });
      }
      return yeni;
    });
  }

  const icerikId = "populer-rotalar-icerik";
  const rotaSayisi = POPULER_ROTALAR.length;

  return (
    <section ref={bolumRef} id="populer-rotalar" className="w-full scroll-mt-24">
      <button
        type="button"
        onClick={acKapa}
        className="group flex w-full items-center justify-between rounded-2xl border border-teal-100 bg-white p-4 shadow-sm transition-all duration-200 hover:shadow-md md:p-5"
        aria-expanded={isExpanded}
        aria-controls={icerikId}
      >
        <div className="flex min-w-0 items-center gap-3 text-left">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-teal-50 text-teal-700 transition-colors group-hover:bg-teal-600 group-hover:text-white">
            <Compass className="h-5 w-5" aria-hidden />
          </div>
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-teal-600">
                Rotalar
              </span>
              <span className="rounded-full bg-teal-50 px-2 py-0.5 text-[11px] font-medium text-teal-800">
                {rotaSayisi} İkonik Rota
              </span>
            </div>
            <h2 className="text-sm font-bold leading-snug text-slate-800 sm:text-base md:text-lg">
              Türkiye’nin En Çok Tercih Edilen ve İkonik Rotaları
            </h2>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-2 text-sm font-semibold text-teal-700">
          <span className="hidden sm:inline">
            {isExpanded ? "Rotaları Gizle" : "Rotaları Göster"}
          </span>
          <ChevronDown
            className={`h-5 w-5 transition-transform duration-300 ${
              isExpanded ? "rotate-180 text-teal-600" : "text-slate-400"
            }`}
            aria-hidden
          />
        </div>
      </button>

      <div
        id={icerikId}
        className={`grid transition-all duration-500 ease-in-out ${
          isExpanded
            ? "mt-6 grid-rows-[1fr] opacity-100"
            : "pointer-events-none grid-rows-[0fr] opacity-0"
        }`}
      >
        <div className="min-h-0 overflow-hidden">
          <div
            className="mb-6 flex flex-wrap gap-2"
            role="tablist"
            aria-label="Rota kategorileri"
          >
            {FILTRELER.map((f) => {
              const aktif = filtre === f.id;
              return (
                <button
                  key={f.id}
                  type="button"
                  role="tab"
                  aria-selected={aktif}
                  onClick={() => setFiltre(f.id)}
                  className={`rounded-full px-3.5 py-1.5 text-sm transition ${
                    aktif
                      ? "bg-deniz text-white shadow-sm"
                      : "bg-white/70 text-ink hover:bg-white"
                  }`}
                >
                  {f.etiket}
                </button>
              );
            })}
          </div>

          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {rotalar.map((rota) => (
              <RotaKarti
                key={rota.id}
                rota={rota}
                secili={activeRouteId === rota.id}
                onSec={onSelectRoute}
                gorselYukle={isExpanded}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
