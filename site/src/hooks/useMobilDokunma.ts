"use client";

import { useEffect, useState } from "react";

const MOBIL_SORGU = "(max-width: 767px)";

/** 768px altı: harita sürüklemesi kapalı, sayfa kaydı serbest. */
export function useMobilDokunma() {
  const [mobil, setMobil] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia(MOBIL_SORGU);
    const uygula = () => setMobil(mq.matches);
    uygula();
    mq.addEventListener("change", uygula);
    return () => mq.removeEventListener("change", uygula);
  }, []);

  return mobil;
}
