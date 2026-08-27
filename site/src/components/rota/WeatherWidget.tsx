"use client";

import {
  Cloud,
  CloudDrizzle,
  CloudFog,
  CloudLightning,
  CloudRain,
  CloudSnow,
  CloudSun,
  Droplets,
  Sun,
  Wind,
} from "lucide-react";
import { useWeather } from "@/hooks/useWeather";
import { wmoAciklamasi } from "@/services/weather";

type Props = {
  enlem: number;
  boylam: number;
  konumEtiketi?: string;
};

function WmoIkon({ kod, className }: { kod: number; className?: string }) {
  const ortak = { className, strokeWidth: 1.6, "aria-hidden": true as const };
  if (kod === 0) return <Sun {...ortak} />;
  if (kod >= 1 && kod <= 2) return <CloudSun {...ortak} />;
  if (kod === 3) return <Cloud {...ortak} />;
  if (kod === 45 || kod === 48) return <CloudFog {...ortak} />;
  if (kod >= 51 && kod <= 57) return <CloudDrizzle {...ortak} />;
  if ((kod >= 61 && kod <= 67) || (kod >= 80 && kod <= 82)) {
    return <CloudRain {...ortak} />;
  }
  if ((kod >= 71 && kod <= 77) || kod === 85 || kod === 86) {
    return <CloudSnow {...ortak} />;
  }
  if (kod >= 95) return <CloudLightning {...ortak} />;
  return <Cloud {...ortak} />;
}

function gunEtiketi(isoTarih: string): string {
  const tarih = new Date(`${isoTarih}T12:00:00`);
  return new Intl.DateTimeFormat("tr-TR", { weekday: "short" }).format(tarih);
}

function WeatherSkeleton() {
  return (
    <div
      className="overflow-hidden rounded-2xl border border-[var(--cizgi)] bg-white/70"
      aria-busy="true"
      aria-live="polite"
    >
      <div className="flex flex-col gap-6 p-5 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center gap-4">
          <div className="h-14 w-14 animate-pulse rounded-full bg-deniz/10" />
          <div className="space-y-2">
            <div className="h-8 w-24 animate-pulse rounded bg-deniz/10" />
            <div className="h-4 w-36 animate-pulse rounded bg-deniz/10" />
          </div>
        </div>
        <div className="flex gap-4">
          <div className="h-10 w-20 animate-pulse rounded bg-deniz/10" />
          <div className="h-10 w-20 animate-pulse rounded bg-deniz/10" />
        </div>
      </div>
      <div className="grid grid-cols-5 gap-2 border-t border-[var(--cizgi)] p-3">
        {Array.from({ length: 5 }, (_, i) => (
          <div key={i} className="h-20 animate-pulse rounded-xl bg-deniz/10" />
        ))}
      </div>
    </div>
  );
}

export function WeatherWidget({ enlem, boylam, konumEtiketi = "Samsun" }: Props) {
  const { veri, durum, hata } = useWeather(enlem, boylam);

  if (durum === "yukleniyor") {
    return <WeatherSkeleton />;
  }

  if (durum === "hata" || !veri) {
    return (
      <div
        role="alert"
        className="rounded-2xl border border-bordo/25 bg-bordo/5 px-5 py-4 text-sm text-bordo"
      >
        {hata ?? "Hava durumu yüklenemedi."} Open-Meteo’ya ulaşılamıyor olabilir.
      </div>
    );
  }

  return (
    <section
      aria-label={`${konumEtiketi} hava durumu`}
      className="overflow-hidden rounded-2xl border border-[var(--cizgi)] bg-white/80 shadow-[0_8px_30px_rgba(6,54,66,0.06)]"
    >
      <div className="flex flex-col gap-6 p-5 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-full bg-deniz/10 text-deniz">
            <WmoIkon kod={veri.current.weatherCode} className="h-8 w-8" />
          </div>
          <div>
            <p className="text-sm text-ink/50">{konumEtiketi} · şimdi</p>
            <p className="font-display text-4xl leading-none text-deniz">
              {Math.round(veri.current.temperature)}°
            </p>
            <p className="mt-1 text-sm text-ink/70">{veri.current.description}</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-5 text-sm text-ink/70">
          <span className="inline-flex items-center gap-1.5">
            <Droplets className="h-4 w-4 text-yosun" aria-hidden />
            Nem %{Math.round(veri.current.humidity)}
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Wind className="h-4 w-4 text-yosun" aria-hidden />
            Rüzgar {Math.round(veri.current.windSpeed)} km/s
          </span>
        </div>
      </div>

      <ol className="grid grid-cols-5 gap-px bg-[var(--cizgi)]">
        {veri.daily.slice(0, 5).map((gun) => (
            <li
              key={gun.date}
              className="bg-kopuk/80 px-2 py-3 text-center"
              title={wmoAciklamasi(gun.weatherCode)}
            >
              <p className="text-xs font-medium uppercase tracking-wide text-ink/45">
                {gunEtiketi(gun.date)}
              </p>
              <WmoIkon kod={gun.weatherCode} className="mx-auto mt-2 h-5 w-5 text-deniz" />
              <p className="mt-2 text-sm tabular-nums text-ink">
                <span className="font-medium">{Math.round(gun.maxTemp)}°</span>
                <span className="text-ink/40"> / {Math.round(gun.minTemp)}°</span>
              </p>
            </li>
          ))}
      </ol>
    </section>
  );
}
