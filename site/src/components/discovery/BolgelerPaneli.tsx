"use client";

import { useCallback, useState } from "react";
import { TurkeyMapYukle } from "@/components/map/TurkeyMapYukle";
import { CityShowcase } from "@/components/discovery/CityShowcase";
import { PopularRoutesSection } from "@/components/discovery/PopularRoutesSection";
import { TURKIYE_SEHIRLERI } from "@/data/cities";
import { POPULER_ROTALAR, type PopularRoute } from "@/data/popularRoutes";
import { VARSAYILAN_IL_ID } from "@/lib/sehirler";
import type { CityDetail } from "@/types/city";

const ILK_SEHIR: CityDetail =
  TURKIYE_SEHIRLERI.find((s) => s.id === VARSAYILAN_IL_ID) ?? TURKIYE_SEHIRLERI[0];

export function BolgelerPaneli() {
  const [selectedProvince, setSelectedProvince] = useState<CityDetail>(ILK_SEHIR);
  const [activeRouteId, setActiveRouteId] = useState<string | null>(null);
  const [odakSayac, setOdakSayac] = useState(0);

  const selectedRoute =
    POPULER_ROTALAR.find((r) => r.id === activeRouteId) ?? null;

  const ilSec = useCallback((sehir: CityDetail) => {
    setSelectedProvince(sehir);
    setActiveRouteId(null);
  }, []);

  const rotaSecHaritadan = useCallback((rota: PopularRoute) => {
    setActiveRouteId(rota.id);
    setOdakSayac((n) => n + 1);
    window.requestAnimationFrame(() => {
      document
        .getElementById(`rota-kart-${rota.id}`)
        ?.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  }, []);

  const rotaSecKarttan = useCallback((rota: PopularRoute) => {
    setActiveRouteId(rota.id);
    setOdakSayac((n) => n + 1);
    document
      .getElementById("turkiye-haritasi")
      ?.scrollIntoView({ behavior: "smooth", block: "center" });
  }, []);

  return (
    <div className="space-y-16">
      <div className="grid gap-8 lg:grid-cols-[minmax(0,1.4fr)_minmax(280px,0.9fr)] lg:items-start">
        <div
          id="turkiye-haritasi"
          className="h-[min(70vh,560px)] min-h-[420px] overflow-hidden rounded-2xl border border-[var(--cizgi)] shadow-[0_12px_40px_rgba(6,54,66,0.12)]"
        >
          <TurkeyMapYukle
            sehirler={TURKIYE_SEHIRLERI}
            selectedProvince={selectedProvince}
            onSelect={ilSec}
            rotalar={POPULER_ROTALAR}
            selectedRoute={selectedRoute}
            onSelectRoute={rotaSecHaritadan}
            odakSayac={odakSayac}
          />
        </div>
        <CityShowcase key={selectedProvince.id} city={selectedProvince} />
      </div>
      <PopularRoutesSection
        activeRouteId={activeRouteId}
        onSelectRoute={rotaSecKarttan}
      />
    </div>
  );
}
