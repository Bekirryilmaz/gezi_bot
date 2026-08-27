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
import { SAMSUN_MERKEZ } from "@/lib/ilceler";
import "leaflet/dist/leaflet.css";

type IlceOzellik = { id: string; name: string; slug: string };

type Props = {
  ilceler: DistrictDetail[];
  selectedDistrict: DistrictDetail | null;
  onSelect: (ilce: DistrictDetail) => void;
};

const STIL_VARSAYILAN: PathOptions = {
  fillColor: "#0f766e",
  fillOpacity: 0.15,
  color: "#0d9488",
  weight: 1.5,
};

const STIL_HOVER: PathOptions = {
  fillColor: "#0f766e",
  fillOpacity: 0.4,
  color: "#115e59",
  weight: 2.5,
};

const STIL_AKTIF: PathOptions = {
  fillColor: "#042f2e",
  fillOpacity: 0.6,
  color: "#0f172a",
  weight: 3,
};

function ozellikAl(feature?: Feature): IlceOzellik | null {
  const p = feature?.properties;
  if (!p || typeof p !== "object" || !("id" in p) || typeof p.id !== "string") {
    return null;
  }
  return p as IlceOzellik;
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
  const genelBakis = useRef(false);
  const selectedId = selectedDistrict?.id ?? null;

  const selectedIdRef = useRef(selectedId);
  const onSelectRef = useRef(onSelect);
  const ilcelerRef = useRef(ilceler);

  useEffect(() => {
    selectedIdRef.current = selectedId;
    onSelectRef.current = onSelect;
    ilcelerRef.current = ilceler;
  }, [selectedId, onSelect, ilceler]);

  const tumunuSigdir = useCallback(() => {
    const gj = katmanRef.current;
    if (!gj || genelBakis.current) return;
    const tumu = gj.getBounds();
    if (!tumu.isValid()) return;
    harita.fitBounds(tumu, { padding: [18, 18], maxZoom: 9, animate: false });
    genelBakis.current = true;
  }, [harita]);

  const stil = useCallback((feature?: Feature): PathOptions => {
    const oz = ozellikAl(feature);
    return oz?.id === selectedIdRef.current ? STIL_AKTIF : STIL_VARSAYILAN;
  }, []);

  const onEachFeature = useCallback((feature: Feature, layer: Layer) => {
    const oz = ozellikAl(feature);
    if (!oz) return;

    layer.bindTooltip(oz.name, {
      sticky: true,
      direction: "center",
      opacity: 1,
      className: "ilce-tooltip",
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
        const ilce = ilcelerRef.current.find((i) => i.id === oz.id);
        if (ilce) onSelectRef.current(ilce);
      },
    });
  }, []);

  useEffect(() => {
    const gj = katmanRef.current;
    if (!gj) return;

    gj.eachLayer((layer) => katmanStili(layer, selectedId));

    if (!genelBakis.current) {
      tumunuSigdir();
      return;
    }

    if (!selectedId) {
      harita.setView(SAMSUN_MERKEZ, 9);
      return;
    }

    gj.eachLayer((layer) => {
      const oz = ozellikAl((layer as Layer & { feature?: Feature }).feature);
      if (oz?.id !== selectedId) return;
      const getBounds = (layer as Layer & { getBounds?: () => LatLngBounds })
        .getBounds;
      if (typeof getBounds !== "function") return;
      harita.fitBounds(getBounds.call(layer), {
        padding: [32, 32],
        maxZoom: 12,
        animate: true,
        duration: 0.75,
      });
    });
  }, [selectedId, harita, geo, tumunuSigdir]);

  return (
    <GeoJSON
      ref={katmanRef}
      data={geo as GeoJsonObject}
      style={stil}
      onEachFeature={onEachFeature}
      eventHandlers={{ add: tumunuSigdir }}
    />
  );
}

export function DistrictMap({ ilceler, selectedDistrict, onSelect }: Props) {
  const [geo, setGeo] = useState<FeatureCollection | null>(null);

  useEffect(() => {
    let iptal = false;
    fetch("/data/samsun-ilceler.geojson")
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
  }, []);

  return (
    <div className="h-full min-h-[420px] w-full">
      <MapContainer
        center={SAMSUN_MERKEZ}
        zoom={9}
        scrollWheelZoom
        className="z-0 h-full w-full"
        style={{ height: "100%", width: "100%", minHeight: 420 }}
      >
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
