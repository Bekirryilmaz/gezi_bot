"use client";

import {
  GeoJSON,
  MapContainer,
  TileLayer,
  useMap,
} from "react-leaflet";
import { useCallback, useEffect, useRef, useState } from "react";
import type {
  GeoJSON as LeafletGeoJSON,
  LatLngBounds,
  Layer,
  LeafletMouseEvent,
  Path,
  PathOptions,
} from "leaflet";
import { DomEvent } from "leaflet";
import type { Feature, FeatureCollection, GeoJsonObject } from "geojson";
import type { DistrictDetail } from "@/types/discovery";
import { ilceGeoYolu } from "@/lib/ilceGeo";
import { TURKIYE_MERKEZ } from "@/lib/sehirler";
import { useMobilDokunma } from "@/hooks/useMobilDokunma";
import { HaritaBoyut } from "@/components/map/HaritaBoyut";
import "leaflet/dist/leaflet.css";

type IlceOzellik = { id: string; name: string; slug: string };

type Props = {
  sehirSlug: string;
  ilceler: DistrictDetail[];
  selectedDistrict: DistrictDetail | null;
  onSelect: (ilce: DistrictDetail) => void;
};

const STIL_VARSAYILAN: PathOptions = {
  fillColor: "#0d9488",
  fillOpacity: 0.12,
  color: "#0f766e",
  weight: 1.8,
};

const STIL_HOVER: PathOptions = {
  fillColor: "#0d9488",
  fillOpacity: 0.35,
  color: "#115e59",
  weight: 2.5,
};

const STIL_AKTIF: PathOptions = {
  fillColor: "#042f2e",
  fillOpacity: 0.55,
  color: "#0f172a",
  weight: 3,
};

function ozellikAl(feature?: Feature): IlceOzellik | null {
  const p = feature?.properties;
  if (!p || typeof p !== "object") return null;
  const name =
    (typeof p.name === "string" && p.name) ||
    (typeof p.ilce_adi === "string" && p.ilce_adi) ||
    "";
  const id =
    (typeof p.id === "string" && p.id) ||
    (typeof p.slug === "string" && p.slug) ||
    "";
  if (!id && !name) return null;
  const slug = typeof p.slug === "string" && p.slug ? p.slug : id || name.toLocaleLowerCase("tr-TR");
  return { id: id || slug, name: name || slug, slug };
}

function katmanStili(layer: Layer, selectedId: string | null) {
  const oz = ozellikAl((layer as Layer & { feature?: Feature }).feature);
  (layer as Path).setStyle(
    oz?.id === selectedId ? STIL_AKTIF : STIL_VARSAYILAN,
  );
  if (oz?.id === selectedId) {
    (layer as Path).bringToFront();
  }
}

function IlcePoligonlari({
  geo,
  ilceler,
  selectedDistrict,
  onSelect,
}: {
  geo: FeatureCollection;
  ilceler: DistrictDetail[];
  selectedDistrict: DistrictDetail | null;
  onSelect: (ilce: DistrictDetail) => void;
}) {
  const harita = useMap();
  const katmanRef = useRef<LeafletGeoJSON | null>(null);
  const ilSigdirildi = useRef(false);
  const selectedId = selectedDistrict?.id ?? null;

  const selectedIdRef = useRef(selectedId);
  const onSelectRef = useRef(onSelect);
  const ilcelerRef = useRef(ilceler);

  useEffect(() => {
    selectedIdRef.current = selectedId;
    onSelectRef.current = onSelect;
    ilcelerRef.current = ilceler;
  }, [selectedId, onSelect, ilceler]);

  const iliSigdir = useCallback(() => {
    const gj = katmanRef.current;
    if (!gj) return;
    const tumu = gj.getBounds();
    if (!tumu.isValid()) return;
    harita.fitBounds(tumu, {
      padding: [20, 20],
      maxZoom: 10,
      animate: true,
      duration: 0.75,
    });
    harita.invalidateSize();
    ilSigdirildi.current = true;
  }, [harita]);

  const stil = useCallback((feature?: Feature): PathOptions => {
    const oz = ozellikAl(feature);
    return oz?.id === selectedIdRef.current ? STIL_AKTIF : STIL_VARSAYILAN;
  }, []);

  const onEachFeature = useCallback((feature: Feature, layer: Layer) => {
    const oz = ozellikAl(feature);
    if (!oz) return;

    layer.bindTooltip(`<strong>${oz.name}</strong>`, {
      sticky: true,
      direction: "center",
      opacity: 1,
      className: "ilce-tooltip custom-map-tooltip",
    });

    layer.on({
      mouseover: (e: LeafletMouseEvent) => {
        const hedef = e.target as Path;
        if (oz.id !== selectedIdRef.current) {
          hedef.setStyle(STIL_HOVER);
        }
        hedef.bringToFront();
      },
      mouseout: (e: LeafletMouseEvent) => {
        const hedef = e.target as Path;
        hedef.setStyle(
          oz.id === selectedIdRef.current ? STIL_AKTIF : STIL_VARSAYILAN,
        );
        katmanRef.current?.eachLayer((l) => {
          katmanStili(l, selectedIdRef.current);
        });
      },
      click: (e: LeafletMouseEvent) => {
        DomEvent.stopPropagation(e);
        const ilce =
          ilcelerRef.current.find((i) => i.id === oz.id || i.slug === oz.slug) ??
          ({
            id: oz.id,
            name: oz.name,
            slug: oz.slug,
            coordinates: [0, 0],
            vibe: "",
            highlights: {
              attractions: [],
              gastronomy: [],
              travelTips: {
                tip: "",
                bestTimeToVisit: "",
                atmosphere: "",
                transport: "",
              },
            },
          } satisfies DistrictDetail);
        onSelectRef.current(ilce);
        const getBounds = (layer as Layer & { getBounds?: () => LatLngBounds })
          .getBounds;
        if (typeof getBounds === "function") {
          harita.fitBounds(getBounds.call(layer), {
            padding: [30, 30],
            maxZoom: 12,
            animate: true,
            duration: 0.75,
          });
        }
      },
    });
  }, [harita]);

  useEffect(() => {
    ilSigdirildi.current = false;
  }, [geo]);

  useEffect(() => {
    const gj = katmanRef.current;
    if (!gj) return;

    gj.eachLayer((layer) => katmanStili(layer, selectedId));

    if (!ilSigdirildi.current) {
      iliSigdir();
      return;
    }

    if (!selectedId) return;

    gj.eachLayer((layer) => {
      const oz = ozellikAl((layer as Layer & { feature?: Feature }).feature);
      if (oz?.id !== selectedId) return;
      const getBounds = (layer as Layer & { getBounds?: () => LatLngBounds })
        .getBounds;
      if (typeof getBounds !== "function") return;
      harita.fitBounds(getBounds.call(layer), {
        padding: [30, 30],
        maxZoom: 12,
        animate: true,
        duration: 0.75,
      });
    });
  }, [selectedId, harita, geo, iliSigdir]);

  return (
    <GeoJSON
      ref={katmanRef}
      data={geo as GeoJsonObject}
      style={stil}
      onEachFeature={onEachFeature}
      eventHandlers={{ add: iliSigdir }}
    />
  );
}

export function DistrictMap({
  sehirSlug,
  ilceler,
  selectedDistrict,
  onSelect,
}: Props) {
  const [geo, setGeo] = useState<FeatureCollection | null>(null);

  useEffect(() => {
    let iptal = false;
    setGeo(null);
    fetch(ilceGeoYolu(sehirSlug))
      .then((r) => {
        if (!r.ok) throw new Error(`GeoJSON ${r.status}`);
        return r.json() as Promise<FeatureCollection>;
      })
      .then((data) => {
        if (!iptal) setGeo(data);
      })
      .catch(() => {
        if (!iptal) setGeo(null);
      });
    return () => {
      iptal = true;
    };
  }, [sehirSlug]);

  const merkez = ilceler[0]?.coordinates ?? TURKIYE_MERKEZ;
  const mobil = useMobilDokunma();

  return (
    <div className="h-full w-full max-w-full">
      <MapContainer
        key={sehirSlug}
        center={merkez}
        zoom={8}
        dragging={!mobil}
        scrollWheelZoom={!mobil}
        touchZoom
        doubleClickZoom={!mobil}
        className="z-0 h-full w-full max-w-full"
        style={{ height: "100%", width: "100%" }}
      >
        <HaritaBoyut tetik={sehirSlug + (geo ? "-ok" : "")} />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {geo ? (
          <IlcePoligonlari
            geo={geo}
            ilceler={ilceler}
            selectedDistrict={selectedDistrict}
            onSelect={onSelect}
          />
        ) : null}
      </MapContainer>
    </div>
  );
}
