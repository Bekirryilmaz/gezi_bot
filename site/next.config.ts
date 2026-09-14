import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import type { NextConfig } from "next";

const API_HEDEF = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8125";

/** MapLibre v6 worker — Turbopack/Next paketlemesi worker+shared dosyasini kopyalar. */
const MAPLIBRE_DIST = path.join(
  path.dirname(createRequire(import.meta.url).resolve("maplibre-gl/package.json")),
  "dist",
);
const MAPLIBRE_PUBLIC = path.join(process.cwd(), "public", "maplibre");
mkdirSync(MAPLIBRE_PUBLIC, { recursive: true });
for (const dosya of ["maplibre-gl-worker.mjs", "maplibre-gl-shared.mjs"]) {
  const hedef = path.join(MAPLIBRE_PUBLIC, dosya);
  if (!existsSync(hedef)) copyFileSync(path.join(MAPLIBRE_DIST, dosya), hedef);
}

const nextConfig: NextConfig = {
  // 127.0.0.1 varsayilan allowlist'te yok; modul script Origin 403 olmasin
  allowedDevOrigins: ["127.0.0.1"],
  experimental: {
    optimizePackageImports: ["lucide-react", "radix-ui"],
  },
  async rewrites() {
    return [
      {
        source: "/backend/:path*",
        destination: `${API_HEDEF}/:path*`,
      },
    ];
  },
};

export default nextConfig;
