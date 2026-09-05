import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Şamandıra",
    short_name: "Şamandıra",
    description: "Karadeniz'in kişisel gezi rehberi — keşfet, oku, gün gün rotanı kur.",
    start_url: "/",
    display: "standalone",
    background_color: "#063642",
    theme_color: "#0a4d5c",
    lang: "tr",
  };
}
