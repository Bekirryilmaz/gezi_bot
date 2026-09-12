"use client";

import { useEffect, useRef, useState, type ComponentType } from "react";
import type { HaritaIsareti } from "@/lib/harita";
import { HaritaKapak, HaritaKapakDugmeleri } from "./HaritaKapak";
import { HaritaPlakaPaneli } from "./HaritaPlakaPaneli";

type SahneOzellik = {
  isaretler: HaritaIsareti[];
  merkez: { enlem: number; boylam: number };
  onSec: (id: string) => void;
  onHazir?: () => void;
};

/**
 * Katlanana kadar 0 karo: IO esikten once maplibre import edilmez.
 * Reduced-motion: statik kapak (kanvas/karo yok).
 */
export function HaritaGecikmeli({
  isaretler,
  merkez,
  sehirIsim,
}: {
  isaretler: HaritaIsareti[];
  merkez: { enlem: number; boylam: number };
  sehirIsim: string;
}) {
  const kutuRef = useRef<HTMLDivElement>(null);
  const [Sahne, setSahne] = useState<ComponentType<SahneOzellik> | null>(null);
  const [kapakUstte, setKapakUstte] = useState(true);
  const [dugmeAcik, setDugmeAcik] = useState(false);
  const [secilenId, setSecilenId] = useState<string | null>(null);
  const secilen = isaretler.find((i) => i.id === secilenId) ?? null;

  useEffect(() => {
    const kutu = kutuRef.current;
    if (!kutu) return;

    const azalt = window.matchMedia("(prefers-reduced-motion: reduce)");
    const gozlem = new IntersectionObserver(
      ([girdi]) => {
        if (!girdi?.isIntersecting) return;
        gozlem.disconnect();
        setDugmeAcik(true);
        if (azalt.matches) return;
        void import("./HaritaSahne").then((m) => {
          setSahne(() => m.HaritaSahne);
        });
      },
      { threshold: 0.12, rootMargin: "0px" },
    );
    gozlem.observe(kutu);
    return () => gozlem.disconnect();
  }, []);

  return (
    <div className="grid gap-5 lg:grid-cols-12 lg:items-stretch">
      <div
        ref={kutuRef}
        data-harita-sahne
        data-harita-yuklu={Sahne && !kapakUstte ? "1" : "0"}
        className="harita-sahne border-bordo/12 relative overflow-hidden rounded-[12px] border lg:col-span-7"
      >
        {Sahne ? (
          <Sahne
            isaretler={isaretler}
            merkez={merkez}
            onSec={setSecilenId}
            onHazir={() => setKapakUstte(false)}
          />
        ) : null}
        <div
          className={`absolute inset-0 z-[2] ${
            kapakUstte ? "opacity-100" : "pointer-events-none opacity-0"
          }`}
          style={{
            transition: "opacity var(--sure-orta) var(--ease-giris)",
          }}
        >
          <HaritaKapak
            isaretler={isaretler}
            merkez={merkez}
            sehirIsim={sehirIsim}
            secilenId={secilenId}
          />
          {dugmeAcik &&
            (Sahne && !kapakUstte ? null : (
              <HaritaKapakDugmeleri
                isaretler={isaretler}
                merkez={merkez}
                secilenId={secilenId}
                onSec={setSecilenId}
              />
            ))}
        </div>
      </div>
      <div className="lg:col-span-5">
        <HaritaPlakaPaneli isaret={secilen} sehirIsim={sehirIsim} />
      </div>
    </div>
  );
}
