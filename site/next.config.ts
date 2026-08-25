import type { NextConfig } from "next";

const API_HEDEF =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8125";

const nextConfig: NextConfig = {
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
