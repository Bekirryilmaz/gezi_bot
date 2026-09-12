"use client";

import { useEffect, useRef } from "react";
import type { HaritaIsareti } from "@/lib/harita";
import { haritaScrubNoktasi, OFM_STIL_URL } from "@/lib/harita";
import { boyaHaritaStili } from "@/lib/harita-stil";

type MapLibre = typeof import("maplibre-gl");

/**
 * MapLibre + OpenFreeMap. SSR yok; rAF/scroll'da setState yok.
 * 3d-web-experience: pitch sinirli, DPR tavan 2, cooperative scroll, remove() teardown.
 */
export function HaritaSahne({
  isaretler,
  merkez,
  onSec,
  onHazir,
}: {
  isaretler: HaritaIsareti[];
  merkez: { enlem: number; boylam: number };
  onSec: (id: string) => void;
  onHazir?: () => void;
}) {
  const kutuRef = useRef<HTMLDivElement>(null);
  const onSecRef = useRef(onSec);
  const onHazirRef = useRef(onHazir);

  useEffect(() => {
    onSecRef.current = onSec;
    onHazirRef.current = onHazir;
  }, [onSec, onHazir]);

  useEffect(() => {
    const kutu = kutuRef.current;
    if (!kutu) return;

    let iptal = false;
    let harita: InstanceType<MapLibre["Map"]> | null = null;
    const isaretDugumleri: Array<{ remove: () => void }> = [];
    let raf = 0;
    let calisiyor = false;
    let kullaniciTutuyor = false;
    let hedefScrub = 0;
    let mevcutScrub = 0;

    const scrubOku = () => {
      const dikey = kutu.getBoundingClientRect();
      const pay = window.innerHeight + dikey.height;
      const gecen = window.innerHeight - dikey.top;
      hedefScrub = Math.min(1, Math.max(0, gecen / pay));
    };

    const adim = () => {
      if (iptal || !harita) {
        calisiyor = false;
        return;
      }
      const fark = hedefScrub - mevcutScrub;
      if (!kullaniciTutuyor && Math.abs(fark) > 0.0009) {
        mevcutScrub += fark * 0.12;
        const kamera = haritaScrubNoktasi(isaretler, merkez, mevcutScrub);
        harita.jumpTo(kamera);
        raf = requestAnimationFrame(adim);
        return;
      }
      calisiyor = false;
    };

    const baslat = () => {
      if (calisiyor || iptal || !harita || document.hidden) return;
      calisiyor = true;
      raf = requestAnimationFrame(adim);
    };

    const onScroll = () => {
      scrubOku();
      baslat();
    };
    const onDown = () => {
      kullaniciTutuyor = true;
    };
    const onUp = () => {
      kullaniciTutuyor = false;
    };
    const onSekme = () => {
      if (document.hidden) {
        cancelAnimationFrame(raf);
        calisiyor = false;
        return;
      }
      baslat();
    };

    window.addEventListener("scroll", onScroll, { passive: true });
    kutu.addEventListener("pointerdown", onDown);
    window.addEventListener("pointerup", onUp);
    document.addEventListener("visibilitychange", onSekme);

    (async () => {
      const maplibre = await import("maplibre-gl");
      await import("maplibre-gl/dist/maplibre-gl.css");
      if (iptal) return;
      maplibre.setWorkerUrl("/maplibre/maplibre-gl-worker.mjs");

      const ham = await fetch(OFM_STIL_URL).then((r) => r.json());
      if (iptal) return;
      const stil = boyaHaritaStili(ham);
      const kamera0 = haritaScrubNoktasi(isaretler, merkez, 0);

      harita = new maplibre.Map({
        container: kutu,
        style: stil as never,
        center: kamera0.center,
        zoom: kamera0.zoom,
        pitch: kamera0.pitch,
        bearing: kamera0.bearing,
        cooperativeGestures: true,
        scrollZoom: false,
        attributionControl: { compact: true },
        pixelRatio: Math.min(window.devicePixelRatio || 1, 2),
        maxPitch: 45,
        fadeDuration: 180,
      });

      harita.on("error", () => {
        onHazirRef.current?.();
      });
      harita.on("load", () => {
        if (iptal || !harita) return;
        for (const isaret of isaretler) {
          const el = document.createElement("button");
          el.type = "button";
          el.className = "harita-isik";
          el.setAttribute("aria-label", isaret.ad);
          el.addEventListener("click", (e) => {
            e.stopPropagation();
            onSecRef.current(isaret.id);
            kullaniciTutuyor = true;
            harita?.easeTo({
              center: [isaret.boylam, isaret.enlem],
              zoom: 11.15,
              pitch: 36,
              duration: 640,
              essential: true,
            });
            window.setTimeout(() => {
              kullaniciTutuyor = false;
            }, 720);
          });
          const m = new maplibre.Marker({ element: el, anchor: "center" })
            .setLngLat([isaret.boylam, isaret.enlem])
            .addTo(harita);
          isaretDugumleri.push(m);
        }
        onHazirRef.current?.();
        scrubOku();
        baslat();
      });
    })().catch(() => {
      onHazirRef.current?.();
    });

    return () => {
      iptal = true;
      cancelAnimationFrame(raf);
      window.removeEventListener("scroll", onScroll);
      kutu.removeEventListener("pointerdown", onDown);
      window.removeEventListener("pointerup", onUp);
      document.removeEventListener("visibilitychange", onSekme);
      for (const m of isaretDugumleri) m.remove();
      harita?.remove();
    };
  }, [isaretler, merkez]);

  return (
    <div
      ref={kutuRef}
      className="harita-kanvas absolute inset-0 size-full"
      data-harita-kanvas
    />
  );
}
