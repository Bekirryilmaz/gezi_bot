import type { NextConfig } from "next";

const API_HEDEF =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8125";

const nextConfig: NextConfig = {
  transpilePackages: ["leaflet", "react-leaflet"],
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.unsplash.com",
        pathname: "/**",
      },
    ],
  },
  async redirects() {
    return [
      { source: "/mekan-oner", destination: "/onerim-var", permanent: true },
    ];
  },
  async rewrites() {
    return [
      {
        source: "/backend/:path*",
        destination: `${API_HEDEF}/:path*`,
      },
      {
        source: "/yuklemeler/:path*",
        destination: `${API_HEDEF}/yuklemeler/:path*`,
      },
    ];
  },
};

export default nextConfig;
