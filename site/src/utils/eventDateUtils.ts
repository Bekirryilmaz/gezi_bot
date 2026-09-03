import type { RegionalEvent } from "@/types/events";

export type EventStatusKind = "devam" | "yakin" | "gelecek" | "bitti";

export type EventStatus = {
  kind: EventStatusKind;
  label: string;
  className: string;
  daysUntilStart: number;
  isBannerWorthy: boolean;
};

const MS_GUN = 86_400_000;

const AY_KISA = [
  "Oca",
  "Şub",
  "Mar",
  "Nis",
  "May",
  "Haz",
  "Tem",
  "Ağu",
  "Eyl",
  "Eki",
  "Kas",
  "Ara",
];

const AY_UZUN = [
  "Ocak",
  "Şubat",
  "Mart",
  "Nisan",
  "Mayıs",
  "Haziran",
  "Temmuz",
  "Ağustos",
  "Eylül",
  "Ekim",
  "Kasım",
  "Aralık",
];

export function parseISODate(iso: string): Date {
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(y, (m ?? 1) - 1, d ?? 1);
}

export function gunBaslangici(tarih: Date = new Date()): Date {
  return new Date(tarih.getFullYear(), tarih.getMonth(), tarih.getDate());
}

export function takvimGunFarki(hedef: Date, kaynak: Date): number {
  return Math.round(
    (gunBaslangici(hedef).getTime() - gunBaslangici(kaynak).getTime()) / MS_GUN,
  );
}

export function getEventStatus(
  startDate: string,
  endDate: string,
  now: Date = new Date(),
): EventStatus {
  const bugun = gunBaslangici(now);
  const baslangic = gunBaslangici(parseISODate(startDate));
  const bitis = gunBaslangici(parseISODate(endDate));
  const daysUntilStart = takvimGunFarki(baslangic, bugun);

  if (bugun.getTime() > bitis.getTime()) {
    return {
      kind: "bitti",
      label: "Sona Erdi",
      className: "bg-kopuk text-ink/55 border border-deniz/10",
      daysUntilStart,
      isBannerWorthy: false,
    };
  }

  if (bugun.getTime() >= baslangic.getTime() && bugun.getTime() <= bitis.getTime()) {
    return {
      kind: "devam",
      label: "Devam Ediyor",
      className: "bg-emerald-500 text-white animate-pulse shadow-sm",
      daysUntilStart: 0,
      isBannerWorthy: true,
    };
  }

  if (daysUntilStart > 0 && daysUntilStart <= 30) {
    return {
      kind: "yakin",
      label: `${daysUntilStart} Gün Kaldı`,
      className: "bg-amber-500/10 text-amber-600 border border-amber-500/30",
      daysUntilStart,
      isBannerWorthy: true,
    };
  }

  return {
    kind: "gelecek",
    label: "Gelecek Dönem",
    className: "bg-teal-700/10 text-teal-800 border border-teal-700/20",
    daysUntilStart,
    isBannerWorthy: false,
  };
}

export function formatTarihKisa(iso: string): { gun: string; ay: string } {
  const d = parseISODate(iso);
  return { gun: String(d.getDate()), ay: AY_KISA[d.getMonth()] ?? "" };
}

export function formatTarihUzun(iso: string): string {
  const d = parseISODate(iso);
  return `${d.getDate()} ${AY_UZUN[d.getMonth()]} ${d.getFullYear()}`;
}

export function formatTarihAraligi(startDate: string, endDate: string): string {
  const a = parseISODate(startDate);
  const b = parseISODate(endDate);
  if (a.getTime() === b.getTime()) {
    return formatTarihUzun(startDate);
  }
  if (a.getMonth() === b.getMonth() && a.getFullYear() === b.getFullYear()) {
    return `${a.getDate()}–${b.getDate()} ${AY_UZUN[a.getMonth()]} ${a.getFullYear()}`;
  }
  if (a.getFullYear() === b.getFullYear()) {
    return `${a.getDate()} ${AY_UZUN[a.getMonth()]} – ${b.getDate()} ${AY_UZUN[b.getMonth()]} ${a.getFullYear()}`;
  }
  return `${formatTarihUzun(startDate)} – ${formatTarihUzun(endDate)}`;
}

const DURUM_SIRA: Record<EventStatusKind, number> = {
  devam: 0,
  yakin: 1,
  gelecek: 2,
  bitti: 3,
};

export function getNearestEventForCity(
  events: RegionalEvent[],
  citySlug: string,
  now: Date = new Date(),
): RegionalEvent | null {
  const today = gunBaslangici(now);
  const cityEvents = events
    .filter((e) => e.citySlug === citySlug)
    .filter((e) => gunBaslangici(parseISODate(e.endDate)).getTime() >= today.getTime())
    .sort(
      (a, b) =>
        parseISODate(a.startDate).getTime() - parseISODate(b.startDate).getTime(),
    );

  return cityEvents.length > 0 ? cityEvents[0] : null;
}

export function etkinlikSirala(
  events: RegionalEvent[],
  now: Date = new Date(),
): RegionalEvent[] {
  return [...events].sort((a, b) => {
    const sa = getEventStatus(a.startDate, a.endDate, now);
    const sb = getEventStatus(b.startDate, b.endDate, now);
    if (sa.kind !== sb.kind) {
      return DURUM_SIRA[sa.kind] - DURUM_SIRA[sb.kind];
    }
    return parseISODate(a.startDate).getTime() - parseISODate(b.startDate).getTime();
  });
}

