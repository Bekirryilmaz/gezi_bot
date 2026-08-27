"use client";

import { useEffect, useState } from "react";
import { havaDurumuGetir } from "@/services/weather";
import type { WeatherData } from "@/types/weather";

type Kaynak = {
  enlem: number;
  boylam: number;
  veri: WeatherData | null;
  hata: string | null;
  durum: "yukleniyor" | "hazir" | "hata";
};

export function useWeather(enlem: number, boylam: number) {
  const [kaynak, setKaynak] = useState<Kaynak>(() => ({
    enlem,
    boylam,
    veri: null,
    hata: null,
    durum: "yukleniyor",
  }));

  if (kaynak.enlem !== enlem || kaynak.boylam !== boylam) {
    setKaynak({
      enlem,
      boylam,
      veri: null,
      hata: null,
      durum: "yukleniyor",
    });
  }

  useEffect(() => {
    const denetleyici = new AbortController();

    havaDurumuGetir(enlem, boylam, denetleyici.signal)
      .then((veri) => {
        setKaynak((onceki) =>
          onceki.enlem === enlem && onceki.boylam === boylam
            ? { ...onceki, veri, hata: null, durum: "hazir" }
            : onceki,
        );
      })
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setKaynak((onceki) =>
          onceki.enlem === enlem && onceki.boylam === boylam
            ? {
                ...onceki,
                hata: err instanceof Error ? err.message : "Hava durumu alınamadı",
                durum: "hata",
              }
            : onceki,
        );
      });

    return () => denetleyici.abort();
  }, [enlem, boylam]);

  return {
    veri: kaynak.veri,
    durum: kaynak.durum,
    hata: kaynak.hata,
    yukleniyor: kaynak.durum === "yukleniyor",
  };
}
