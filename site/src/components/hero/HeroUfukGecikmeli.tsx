"use client";

import dynamic from "next/dynamic";

/** RSC'de ssr:false yasak; kapak LCP'sini kanvas JS'ten ayirir. */
export const HeroUfukGecikmeli = dynamic(
  () => import("./HeroUfuk").then((m) => m.HeroUfuk),
  { ssr: false },
);
