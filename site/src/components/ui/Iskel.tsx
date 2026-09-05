import { cn } from "cn";
import type { PlakaOran } from "./Plaka";

const ORAN: Record<PlakaOran, string> = {
  kart: "aspect-[16/10]",
  hero: "aspect-[4/5] md:h-[min(78vh,640px)] md:aspect-auto",
  genis: "aspect-[16/10] md:aspect-[2/1]",
  dikey: "aspect-[4/5]",
};

export function PlakaIskel({
  oran = "kart",
  className,
}: {
  oran?: PlakaOran;
  className?: string;
}) {
  return (
    <div
      className={cn("iskel-parlama w-full rounded-[4px]", ORAN[oran], className)}
      aria-hidden="true"
    />
  );
}

export function YerKartiIskel({ className }: { className?: string }) {
  return (
    <div className={cn("kart-kabuk flex flex-col", className)} aria-hidden="true">
      <PlakaIskel oran="kart" />
      <div className="flex flex-1 flex-col gap-2 p-4">
        <div className="iskel-parlama h-[2.5em] rounded-sm" />
        <div className="iskel-parlama h-4 w-1/3 rounded-sm" />
        <div className="iskel-parlama h-[2.5em] rounded-sm" />
        <div className="h-7" />
      </div>
    </div>
  );
}

export function ListeIskel({
  satir = 4,
  className,
}: {
  satir?: number;
  className?: string;
}) {
  return (
    <ul className={cn("space-y-3", className)} aria-hidden="true">
      {Array.from({ length: satir }, (_, i) => (
        <li key={i} className="flex h-16 items-center gap-3">
          <div className="iskel-parlama size-10 shrink-0 rounded-sm" />
          <div className="min-w-0 flex-1 space-y-2">
            <div className="iskel-parlama h-4 w-2/3 rounded-sm" />
            <div className="iskel-parlama h-3 w-1/3 rounded-sm" />
          </div>
        </li>
      ))}
    </ul>
  );
}

export function MetinIskel({ className }: { className?: string }) {
  return (
    <div className={cn("space-y-2", className)} aria-hidden="true">
      <div className="iskel-parlama h-4 w-full rounded-sm" />
      <div className="iskel-parlama h-4 w-full rounded-sm" />
      <div className="iskel-parlama h-4 w-[60%] rounded-sm" />
    </div>
  );
}

export { Skeleton } from "./skeleton";
