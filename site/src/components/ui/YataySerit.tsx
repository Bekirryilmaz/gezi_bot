"use client";

import { useRef, useState, type ReactNode } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { cn } from "cn";
import { ODAK } from "@/lib/kart-sinif";

export function YataySerit({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [sayac, setSayac] = useState({ n: 1, m: 1 });

  const guncelle = () => {
    const el = ref.current;
    if (!el) return;
    const kartlar = el.querySelectorAll("[data-serit-oge]");
    const m = Math.max(kartlar.length, 1);
    const genislik = el.clientWidth;
    const n = Math.min(m, Math.floor(el.scrollLeft / Math.max(genislik * 0.4, 1)) + 1);
    setSayac({ n: Math.max(1, n), m });
  };

  const kaydir = (yon: -1 | 1) => {
    const el = ref.current;
    if (!el) return;
    el.scrollBy({ left: yon * el.clientWidth * 0.72, behavior: "smooth" });
  };

  return (
    <div className={cn("relative", className)}>
      <div
        ref={ref}
        onScroll={guncelle}
        className="yatay-serit flex snap-x snap-mandatory [scrollbar-width:none] gap-4 overflow-x-auto pb-2 [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden"
      >
        {children}
      </div>
      <div className="mt-4 flex items-center justify-between">
        <p className="text-ink/50 text-xs tabular-nums" aria-live="polite">
          {sayac.n}/{sayac.m}
        </p>
        <div className="flex gap-2">
          <button
            type="button"
            className={cn(
              "border-bordo/12 text-bordo hover:bg-kagit-koyu bg-tuz inline-flex size-11 cursor-pointer items-center justify-center rounded-[8px] border",
              ODAK,
            )}
            aria-label="Önceki"
            onClick={() => kaydir(-1)}
          >
            <ChevronLeft className="size-4" aria-hidden="true" />
          </button>
          <button
            type="button"
            className={cn(
              "border-bordo/12 text-bordo hover:bg-kagit-koyu bg-tuz inline-flex size-11 cursor-pointer items-center justify-center rounded-[8px] border",
              ODAK,
            )}
            aria-label="Sonraki"
            onClick={() => kaydir(1)}
          >
            <ChevronRight className="size-4" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>
  );
}

export function YataySeritOge({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div
      data-serit-oge
      className={cn("w-[min(80%,320px)] shrink-0 snap-start", className)}
    >
      {children}
    </div>
  );
}
