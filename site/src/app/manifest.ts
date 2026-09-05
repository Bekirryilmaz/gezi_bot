import type { MetadataRoute } from "next";
import { TANIM_CUMLESI } from "@/lib/marka";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Şamandıra",
    short_name: "Şamandıra",
    description: TANIM_CUMLESI,
    start_url: "/",
    display: "standalone",
    background_color: "#F4EFE7",
    theme_color: "#6C0000",
    lang: "tr",
    icons: [
      {
        src: "/logo/icon-192.png",
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: "/logo/icon-512.png",
        sizes: "512x512",
        type: "image/png",
      },
      {
        src: "/logo/icon-512-maskable.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "maskable",
      },
    ],
  };
}
