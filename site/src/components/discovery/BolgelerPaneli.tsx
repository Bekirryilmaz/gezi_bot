"use client";

import { useCallback, useState } from "react";
import { TurkeyMapYukle } from "@/components/map/TurkeyMapYukle";
import { CityShowcase } from "@/components/discovery/CityShowcase";
import { PopularRoutesSection } from "@/components/discovery/PopularRoutesSection";
import { EventCalendarSection } from "@/components/discovery/EventCalendarSection";
import { TURKIYE_SEHIRLERI } from "@/data/cities";
import { POPULER_ROTALAR, type PopularRoute } from "@/data/popularRoutes";
import { VARSAYILAN_IL_ID, sehirBul } from "@/lib/sehirler";
import { HARITA_KUTU_SINIFI } from "@/lib/haritaKutu";
import type { CityDetail } from "@/types/city";
import type { RegionalEvent } from "@/types/events";

const ILK_SEHIR: CityDetail =
  TURKIYE_SEHIRLERI.find((s) => s.id === VARSAYILAN_IL_ID) ?? TURKIYE_SEHIRLERI[0];

export function BolgelerPaneli() {
  const [selectedProvince, setSelectedProvince] = useState<CityDetail>(ILK_SEHIR);
  const [selectedCity, setSelectedCity] = useState<string | null>(ILK_SEHIR.slug);
  const [activeRouteId, setActiveRouteId] = useState<string | null>(null);
  const [odakSayac, setOdakSayac] = useState(0);
  const [ilOdakSayac, setIlOdakSayac] = useState(0);
  const [takvimOdakId, setTakvimOdakId] = useState<string | null>(null);
  const [takvimOdakSayac, setTakvimOdakSayac] = useState(0);

  const selectedRoute =
    POPULER_ROTALAR.find((r) => r.id === activeRouteId) ?? null;

  const ilSec = useCallback((sehir: CityDetail) => {
    setSelectedProvince(sehir);
    setSelectedCity(sehir.slug);
    setActiveRouteId(null);
    setIlOdakSayac((n) => n + 1);
  }, []);

  const takvimIlSec = useCallback((citySlug: string | null) => {
    if (!citySlug) {
      setSelectedCity(null);
      return;
    }
    const sehir = sehirBul(citySlug);
    if (!sehir) return;
    setSelectedProvince(sehir);
    setSelectedCity(sehir.slug);
    setActiveRouteId(null);
    setIlOdakSayac((n) => n + 1);
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

  const takvimeGit = useCallback((etkinlikId?: string) => {
    setTakvimOdakId(etkinlikId ?? null);
    setSelectedCity(selectedProvince.slug);
    setTakvimOdakSayac((n) => n + 1);
  }, [selectedProvince.slug]);

  const etkinlikHaritada = useCallback((event: RegionalEvent) => {
    const sehir = sehirBul(event.citySlug);
    if (!sehir) return;
    setSelectedProvince(sehir);
    setSelectedCity(sehir.slug);
    setActiveRouteId(null);
    setIlOdakSayac((n) => n + 1);
    setTakvimOdakId(event.id);
    document
      .getElementById("turkiye-haritasi")
      ?.scrollIntoView({ behavior: "smooth", block: "center" });
  }, []);

  return (
    <div className="space-y-16">
      <div className="grid gap-8 lg:grid-cols-[minmax(0,1.4fr)_minmax(280px,0.9fr)] lg:items-start">
        <div
          id="turkiye-haritasi"
          className={`${HARITA_KUTU_SINIFI} border border-[var(--cizgi)] shadow-[0_12px_40px_rgba(6,54,66,0.12)]`}
        >
          <TurkeyMapYukle
            sehirler={TURKIYE_SEHIRLERI}
            selectedProvince={selectedProvince}
            onSelect={ilSec}
            rotalar={POPULER_ROTALAR}
            selectedRoute={selectedRoute}
            onSelectRoute={rotaSecHaritadan}
            odakSayac={odakSayac}
            ilOdakSayac={ilOdakSayac}
          />
        </div>
        <CityShowcase
          key={selectedProvince.id}
          city={selectedProvince}
          onTakvimeGit={takvimeGit}
        />
      </div>
      <PopularRoutesSection
        activeRouteId={activeRouteId}
        onSelectRoute={rotaSecKarttan}
      />
      <EventCalendarSection
        selectedCitySlug={selectedCity}
        odakEtkinlikId={takvimOdakId}
        odakSayac={takvimOdakSayac}
        onCityChange={takvimIlSec}
        onEtkinlikSec={etkinlikHaritada}
      />
    </div>
  );
}
