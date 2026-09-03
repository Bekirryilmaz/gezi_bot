"use client";

import dynamic from "next/dynamic";

export const DistrictMapYukle = dynamic(
  () => import("./DistrictMap").then((m) => m.DistrictMap),
  {
    ssr: false,
    loading: () => (
      <div
        className="flex h-full w-full items-center justify-center bg-deniz-derin text-sm text-kopuk/70"
        aria-busy="true"
      >
        Harita yükleniyor…
      </div>
    ),
  },
);
