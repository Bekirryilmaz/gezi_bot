"use client";

import { useEffect, useMemo, useState } from "react";
import { DistrictMapYukle } from "@/components/map/DistrictMapYukle";
import { DistrictShowcase } from "@/components/discovery/DistrictShowcase";
import { SeciciMenu } from "@/components/oneri/SeciciMenu";
import { TURKIYE_SEHIRLERI, sehirBul, VARSAYILAN_IL_ID } from "@/lib/sehirler";
import { IL_SECICI_ACIK } from "@/lib/kesfetOzellik";
import { HARITA_KUTU_SINIFI } from "@/lib/haritaKutu";
import { ilceGeoYolu, ilceleriGeojsonDan, varsayilanIlce } from "@/lib/ilceGeo";
import type { CityDetail } from "@/types/city";
import type { DistrictDetail } from "@/types/discovery";
import type { FeatureCollection } from "geojson";

const IL_SECENEKLERI = [...TURKIYE_SEHIRLERI]
  .sort((a, b) => a.name.localeCompare(b.name, "tr"))
  .map((il) => ({ id: il.slug, etiket: il.name }));

type Props = {
  sehirAnahtari?: string;
  baslangicId?: string;
};

export function KesfetPaneli({
  sehirAnahtari = VARSAYILAN_IL_ID,
}: Props) {
  const ilkSehir =
    (IL_SECICI_ACIK
      ? sehirBul(sehirAnahtari)
      : sehirBul(VARSAYILAN_IL_ID)) ?? TURKIYE_SEHIRLERI[0];
  const [sehir, setSehir] = useState<CityDetail>(ilkSehir);
  const [ilceler, setIlceler] = useState<DistrictDetail[]>([]);
  const [selectedDistrict, setSelectedDistrict] = useState<DistrictDetail | null>(null);
  const [yukleniyor, setYukleniyor] = useState(true);

  useEffect(() => {
    let iptal = false;
    setYukleniyor(true);
    fetch(ilceGeoYolu(sehir.slug))
      .then((r) => {
        if (!r.ok) throw new Error(`GeoJSON ${r.status}`);
        return r.json() as Promise<FeatureCollection>;
      })
      .then((geo) => {
        if (iptal) return;
        const liste = ilceleriGeojsonDan(geo, sehir);
        setIlceler(liste);
        setSelectedDistrict(varsayilanIlce(liste, sehir.slug) ?? null);
        setYukleniyor(false);
      })
      .catch(() => {
        if (iptal) return;
        setIlceler([]);
        setSelectedDistrict(null);
        setYukleniyor(false);
      });
    return () => {
      iptal = true;
    };
  }, [sehir]);

  const sehirSec = (slug: string) => {
    const bulunan = sehirBul(slug);
    if (bulunan) setSehir(bulunan);
  };

  const ilceSayisi = useMemo(() => ilceler.length, [ilceler]);

  return (
    <div className="space-y-8">
      {IL_SECICI_ACIK ? (
        <div className="relative z-20 max-w-md">
          <SeciciMenu
            etiket="İl"
            yerTutucu="İl seçin"
            deger={sehir.slug}
            secenekler={IL_SECENEKLERI}
            onSec={(id) => sehirSec(id)}
          />
        </div>
      ) : null}

      <div className={`relative ${HARITA_KUTU_SINIFI} border border-[var(--cizgi)] shadow-[0_12px_40px_rgba(6,54,66,0.12)]`}>
        <DistrictMapYukle
          sehirSlug={sehir.slug}
          ilceler={ilceler}
          selectedDistrict={selectedDistrict}
          onSelect={setSelectedDistrict}
        />
        {yukleniyor ? (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-deniz-derin/80 text-sm text-kopuk/80">
            {sehir.name} ilçe sınırları yükleniyor…
          </div>
        ) : null}
      </div>

      {ilceSayisi > 0 ? (
        <div className="flex flex-wrap gap-2">
          {ilceler.map((ilce) => {
            const secili = selectedDistrict?.id === ilce.id;
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
      ) : !yukleniyor ? (
        <p className="text-sm text-ink/60">Bu il için ilçe sınırı bulunamadı.</p>
      ) : null}

      {selectedDistrict ? (
        <DistrictShowcase
          key={`${sehir.slug}-${selectedDistrict.id}`}
          district={selectedDistrict}
          sehirAnahtari={sehir.slug}
        />
      ) : null}
    </div>
  );
}
