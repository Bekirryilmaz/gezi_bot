"use client";

import { useEffect } from "react";
import { useMap } from "react-leaflet";

export function HaritaBoyut({ tetik }: { tetik: string }) {
  const harita = useMap();

  useEffect(() => {
    const guncelle = () => harita.invalidateSize();
    guncelle();
    const ilk = window.setTimeout(guncelle, 80);
    const ikinci = window.setTimeout(guncelle, 400);
    window.addEventListener("resize", guncelle);
    return () => {
      window.clearTimeout(ilk);
      window.clearTimeout(ikinci);
      window.removeEventListener("resize", guncelle);
    };
  }, [harita, tetik]);

  return null;
}
