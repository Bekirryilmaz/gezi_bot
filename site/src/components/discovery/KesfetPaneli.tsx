"use client";

import { useState } from "react";
import { DistrictMapYukle } from "@/components/map/DistrictMapYukle";
import { DistrictShowcase } from "@/components/discovery/DistrictShowcase";
import { SAMSUN_ILCELERI } from "@/data/districts";
import { VARSAYILAN_ILCE_ID } from "@/lib/ilceler";
import type { DistrictDetail } from "@/types/discovery";

const ILK_ILCE: DistrictDetail = SAMSUN_ILCELERI[0];

type Props = {
  sehirAnahtari?: string;
  baslangicId?: string;
};

export function KesfetPaneli({
  sehirAnahtari = "samsun",
  baslangicId = VARSAYILAN_ILCE_ID,
}: Props) {
  const ilceler = SAMSUN_ILCELERI;
  const [selectedDistrict, setSelectedDistrict] = useState<DistrictDetail>(
    () => ilceler.find((i) => i.id === baslangicId) ?? ILK_ILCE,
  );

  return (
    <div className="space-y-8">
      <div className="h-[min(70vh,520px)] min-h-[420px] overflow-hidden rounded-2xl border border-[var(--cizgi)] shadow-[0_12px_40px_rgba(6,54,66,0.12)]">
        <DistrictMapYukle
          ilceler={ilceler}
          selectedDistrict={selectedDistrict}
          onSelect={setSelectedDistrict}
        />
      </div>
      <div className="flex flex-wrap gap-2">
        {ilceler.map((ilce) => {
          const secili = selectedDistrict.id === ilce.id;
          return (
            <button
              key={ilce.id}
              type="button"
              onClick={() => setSelectedDistrict(ilce)}
              className={`rounded-full px-3 py-1.5 text-sm transition ${
                secili
                  ? "bg-deniz text-white shadow-sm"
                  : "bg-white/70 text-ink hover:bg-white"
              }`}
            >
              {ilce.name}
            </button>
          );
        })}
      </div>
      <DistrictShowcase
        key={selectedDistrict.id}
        district={selectedDistrict}
        sehirAnahtari={sehirAnahtari}
      />
    </div>
  );
}
