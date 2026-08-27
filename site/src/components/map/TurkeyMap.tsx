"use client";

import { GeoJSON, MapContainer, Marker, Polyline, Popup, TileLayer, Tooltip, useMap } from "react-leaflet";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type {
  GeoJSON as LeafletGeoJSON,
  LatLngBounds,
  Layer,
  LeafletMouseEvent,
  Marker as LeafletMarker,
  Path,
  PathOptions,
} from "leaflet";
import { DivIcon, DomEvent, latLngBounds } from "leaflet";
import type { Feature, FeatureCollection, GeoJsonObject } from "geojson";
import type { CityDetail } from "@/types/city";
import type { PopularRoute } from "@/data/popularRoutes";
import { TURKIYE_MERKEZ } from "@/lib/sehirler";
import "leaflet/dist/leaflet.css";

type IlOzellik = { id: string; name: string; slug: string };

type Props = {
  sehirler: CityDetail[];
  selectedProvince: CityDetail | null;
  onSelect: (sehir: CityDetail) => void;
  rotalar: PopularRoute[];
  selectedRoute: PopularRoute | null;
  onSelectRoute: (rota: PopularRoute) => void;
  odakSayac?: number;
};

const STIL_VARSAYILAN: PathOptions = {
  fillColor: "#0f766e",
  fillOpacity: 0.15,
  color: "#0d9488",
  weight: 1,
};

const STIL_HOVER: PathOptions = {
  fillColor: "#0f766e",
  fillOpacity: 0.45,
  color: "#115e59",
  weight: 2,
};

const STIL_AKTIF: PathOptions = {
  fillColor: "#042f2e",
  fillOpacity: 0.7,
  color: "#0f172a",
  weight: 2.5,
};

function ozellikAl(feature?: Feature): IlOzellik | null {
  const p = feature?.properties;
  if (!p || typeof p !== "object" || !("id" in p) || typeof p.id !== "string") {
    return null;
  }
  return p as IlOzellik;
}

function katmanStili(layer: Layer, selectedId: string | null) {
  const oz = ozellikAl((layer as Layer & { feature?: Feature }).feature);
  (layer as Path).setStyle(oz?.id === selectedId ? STIL_AKTIF : STIL_VARSAYILAN);
  if (oz?.id === selectedId) {
    (layer as Path).bringToFront();
  }
}

function IlPoligonlari({
  geo,
  sehirler,
  selectedProvince,
  onSelect,
  rotaOdakli,
}: {
  geo: FeatureCollection;
  sehirler: CityDetail[];
  selectedProvince: CityDetail | null;
  onSelect: (sehir: CityDetail) => void;
  rotaOdakli: boolean;
}) {
  const harita = useMap();
  const katmanRef = useRef<LeafletGeoJSON | null>(null);
  const ilkYukleme = useRef(true);
  const selectedId = selectedProvince?.id ?? null;

  const selectedIdRef = useRef(selectedId);
  const onSelectRef = useRef(onSelect);
  const sehirlerRef = useRef(sehirler);

  useEffect(() => {
    selectedIdRef.current = selectedId;
    onSelectRef.current = onSelect;
    sehirlerRef.current = sehirler;
  }, [selectedId, onSelect, sehirler]);

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
        const sehir = sehirlerRef.current.find((s) => s.id === oz.id);
        if (sehir) onSelectRef.current(sehir);
      },
    });
  }, []);

  useEffect(() => {
    const gj = katmanRef.current;
    if (!gj) return;

    gj.eachLayer((layer) => katmanStili(layer, selectedId));

    if (rotaOdakli) return;

    if (ilkYukleme.current) {
      ilkYukleme.current = false;
      return;
    }

    if (!selectedId) {
      harita.setView(TURKIYE_MERKEZ, 6);
      return;
    }

    gj.eachLayer((layer) => {
      const oz = ozellikAl((layer as Layer & { feature?: Feature }).feature);
      if (oz?.id !== selectedId) return;
      const getBounds = (layer as Layer & { getBounds?: () => LatLngBounds })
        .getBounds;
      if (typeof getBounds !== "function") return;
      harita.fitBounds(getBounds.call(layer), {
        padding: [28, 28],
        maxZoom: 9,
        animate: true,
        duration: 0.75,
      });
    });
  }, [selectedId, harita, geo, rotaOdakli]);

  return (
    <GeoJSON
      ref={katmanRef}
      data={geo as GeoJsonObject}
      style={stil}
      onEachFeature={onEachFeature}
    />
  );
}

function pinIkon(harf: "A" | "B", arkaplan: string): DivIcon {
  return new DivIcon({
    className: "rota-pin",
    html: `<span class="rota-pin-disk" style="background:${arkaplan}">${harf}</span>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    popupAnchor: [0, -16],
  });
}

function OdakRota({
  rota,
  odakSayac,
}: {
  rota: PopularRoute | null;
  odakSayac: number;
}) {
  const harita = useMap();
  useEffect(() => {
    if (!rota || rota.pathCoordinates.length < 2) return;
    const sinir = latLngBounds(rota.pathCoordinates);
    harita.flyToBounds(sinir, {
      padding: [36, 36],
      maxZoom: 8,
      duration: 0.9,
    });
  }, [rota, odakSayac, harita]);
  return null;
}

function RotaKatmani({
  rotalar,
  selectedRoute,
  onSelectRoute,
  odakSayac,
}: {
  rotalar: PopularRoute[];
  selectedRoute: PopularRoute | null;
  onSelectRoute: (rota: PopularRoute) => void;
  odakSayac: number;
}) {
  const onSelectRef = useRef(onSelectRoute);
  const startRef = useRef<LeafletMarker | null>(null);
  const endRef = useRef<LeafletMarker | null>(null);
  const selectedId = selectedRoute?.id ?? null;

  useEffect(() => {
    onSelectRef.current = onSelectRoute;
  }, [onSelectRoute]);

  const pinA = useMemo(() => pinIkon("A", "#1f7a6b"), []);
  const pinB = useMemo(() => pinIkon("B", "#7a2433"), []);

  useEffect(() => {
    if (!selectedRoute) return;
    const zaman = window.setTimeout(() => {
      startRef.current?.openPopup();
      endRef.current?.openPopup();
    }, 450);
    return () => window.clearTimeout(zaman);
  }, [selectedRoute, odakSayac]);

  return (
    <>
      {rotalar.map((rota) => {
        const secili = rota.id === selectedId;
        return (
          <Polyline
            key={rota.id}
            positions={rota.pathCoordinates}
            className={secili ? "rota-hatti-aktif" : "rota-hatti"}
            pathOptions={
              secili
                ? {
                    color: "#0f766e",
                    weight: 4,
                    dashArray: "6, 8",
                    opacity: 0.95,
                  }
                : {
                    color: "#0d9488",
                    weight: 2,
                    opacity: 0.32,
                  }
            }
            eventHandlers={{
              click: (e) => {
                DomEvent.stopPropagation(e);
                onSelectRef.current(rota);
              },
            }}
          />
        );
      })}
      {selectedRoute ? (
        <>
          <Marker
            ref={startRef}
            position={selectedRoute.startPoint.coordinates}
            icon={pinA}
            zIndexOffset={800}
            eventHandlers={{
              click: (e) => {
                DomEvent.stopPropagation(e);
                onSelectRef.current(selectedRoute);
              },
            }}
          >
            <Popup className="rota-popup" autoClose={false} closeOnClick={false}>
              Başlangıç: {selectedRoute.startPoint.name}
            </Popup>
            <Tooltip direction="top" offset={[0, -12]} opacity={1} className="ilce-tooltip">
              A · {selectedRoute.startPoint.name}
            </Tooltip>
          </Marker>
          <Marker
            ref={endRef}
            position={selectedRoute.endPoint.coordinates}
            icon={pinB}
            zIndexOffset={800}
            eventHandlers={{
              click: (e) => {
                DomEvent.stopPropagation(e);
                onSelectRef.current(selectedRoute);
              },
            }}
          >
            <Popup className="rota-popup" autoClose={false} closeOnClick={false}>
              Bitiş: {selectedRoute.endPoint.name}
            </Popup>
            <Tooltip direction="top" offset={[0, -12]} opacity={1} className="ilce-tooltip">
              B · {selectedRoute.endPoint.name}
            </Tooltip>
          </Marker>
        </>
      ) : null}
      <OdakRota rota={selectedRoute} odakSayac={odakSayac} />
    </>
  );
}

export function TurkeyMap({
  sehirler,
  selectedProvince,
  onSelect,
  rotalar,
  selectedRoute,
  onSelectRoute,
  odakSayac = 0,
}: Props) {
  const [geo, setGeo] = useState<FeatureCollection | null>(null);

  useEffect(() => {
    let iptal = false;
    fetch("/data/turkey-provinces.geojson")
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
        center={TURKIYE_MERKEZ}
        zoom={6}
        scrollWheelZoom
        className="z-0 h-full w-full"
        style={{ height: "100%", width: "100%", minHeight: 420 }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {geo ? (
          <IlPoligonlari
            geo={geo}
            sehirler={sehirler}
            selectedProvince={selectedProvince}
            onSelect={onSelect}
            rotaOdakli={selectedRoute != null}
          />
        ) : null}
        <RotaKatmani
          rotalar={rotalar}
          selectedRoute={selectedRoute}
          onSelectRoute={onSelectRoute}
          odakSayac={odakSayac}
        />
      </MapContainer>
    </div>
  );
}
