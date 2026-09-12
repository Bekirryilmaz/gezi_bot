"use client";

import { useEffect, useRef, useState, type ComponentType, type ReactNode } from "react";
import type { HaritaIsareti } from "@/lib/harita";

type GecikmeliOzellik = {
  isaretler: HaritaIsareti[];
  merkez: { enlem: number; boylam: number };
  sehirIsim: string;
};

/**
 * Ilk JS'e isaret listesi ve maplibre girmez. Katlaninca JSON + chunk.
 */
export function HaritaKapi({ children }: { children: ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const [Sahne, setSahne] = useState<ComponentType<GecikmeliOzellik> | null>(null);
  const [veri, setVeri] = useState<GecikmeliOzellik | null>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const gozlem = new IntersectionObserver(
      ([girdi]) => {
        if (!girdi?.isIntersecting) return;
        gozlem.disconnect();
        const ham = document.getElementById("harita-veri")?.textContent;
        if (!ham) return;
        try {
          setVeri(JSON.parse(ham) as GecikmeliOzellik);
        } catch {
          return;
        }
        void import("./HaritaGecikmeli").then((m) => {
          setSahne(() => m.HaritaGecikmeli);
        });
      },
      { threshold: 0.08, rootMargin: "0px" },
    );
    gozlem.observe(el);
    return () => gozlem.disconnect();
  }, []);

  if (Sahne && veri) {
    return <Sahne {...veri} />;
  }

  return <div ref={ref}>{children}</div>;
}
