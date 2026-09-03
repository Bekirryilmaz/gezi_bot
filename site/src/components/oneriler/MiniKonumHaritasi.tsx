"use client";

import { MapContainer, Marker, TileLayer } from "react-leaflet";
import { useMemo } from "react";
import { DivIcon } from "leaflet";
import "leaflet/dist/leaflet.css";

function pinIkon(): DivIcon {
  return new DivIcon({
    className: "rota-pin",
    html: `<span class="rota-pin-disk" style="background:#1f7a6b">+</span>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}

export function MiniKonumHaritasi({ lat, lng }: { lat: number; lng: number }) {
  const ikon = useMemo(() => pinIkon(), []);
  return (
    <MapContainer
      center={[lat, lng]}
      zoom={13}
      dragging={false}
      scrollWheelZoom={false}
      touchZoom
      className="z-0 h-full w-full max-w-full rounded-2xl"
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[lat, lng]} icon={ikon} />
    </MapContainer>
  );
}
