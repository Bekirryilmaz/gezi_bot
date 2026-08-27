"use client";

import { MapContainer, Marker, TileLayer, useMap, useMapEvents } from "react-leaflet";
import { useEffect, useMemo } from "react";
import { DivIcon } from "leaflet";
import { TURKIYE_MERKEZ } from "@/lib/sehirler";
import "leaflet/dist/leaflet.css";

type Koordinat = { lat: number; lng: number };

type Props = {
  value: Koordinat | null;
  onChange: (konum: Koordinat) => void;
};

function pinIkon(): DivIcon {
  return new DivIcon({
    className: "rota-pin",
    html: `<span class="rota-pin-disk" style="background:#1f7a6b">+</span>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}

function HaritaOlaylari({ onChange }: { onChange: (konum: Koordinat) => void }) {
  useMapEvents({
    click(e) {
      onChange({ lat: e.latlng.lat, lng: e.latlng.lng });
    },
  });
  return null;
}

function Odaklan({ konum }: { konum: Koordinat | null }) {
  const harita = useMap();
  useEffect(() => {
    const guncelle = () => harita.invalidateSize();
    guncelle();
    const ilk = window.setTimeout(guncelle, 80);
    const ikinci = window.setTimeout(guncelle, 300);
    window.addEventListener("resize", guncelle);
    return () => {
      window.clearTimeout(ilk);
      window.clearTimeout(ikinci);
      window.removeEventListener("resize", guncelle);
    };
  }, [harita]);
  useEffect(() => {
    if (!konum) return;
    harita.invalidateSize();
    harita.flyTo([konum.lat, konum.lng], Math.max(harita.getZoom(), 12), { duration: 0.6 });
  }, [konum, harita]);
  return null;
}

export function KonumSecici({ value, onChange }: Props) {
  const ikon = useMemo(() => pinIkon(), []);

  return (
    <MapContainer
      center={value ? [value.lat, value.lng] : TURKIYE_MERKEZ}
      zoom={value ? 13 : 6}
      scrollWheelZoom
      className="z-0 h-full w-full rounded-2xl"
      style={{ height: "100%", width: "100%", minHeight: 420 }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <HaritaOlaylari onChange={onChange} />
      <Odaklan konum={value} />
      {value ? (
        <Marker
          position={[value.lat, value.lng]}
          icon={ikon}
          draggable
          eventHandlers={{
            dragend: (e) => {
              const nokta = e.target.getLatLng();
              onChange({ lat: nokta.lat, lng: nokta.lng });
            },
          }}
        />
      ) : null}
    </MapContainer>
  );
}
