import type { Metadata } from "next";
import { Fraunces, Sora } from "next/font/google";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { HareketSaglayici } from "@/components/hareket/HareketSaglayici";
import { TANIM_CUMLESI, TITLE_ANA, TITLE_SABLON } from "@/lib/marka";
import "./globals.css";

const sora = Sora({
  variable: "--font-sora",
  subsets: ["latin", "latin-ext"],
  weight: ["400", "500", "600"],
});

const fraunces = Fraunces({
  variable: "--font-fraunces",
  subsets: ["latin", "latin-ext"],
  weight: ["500", "600"],
  style: ["normal", "italic"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://xn--amandra-vfb22b.com"),
  title: {
    default: TITLE_ANA,
    template: TITLE_SABLON,
  },
  description: TANIM_CUMLESI,
  icons: {
    icon: [
      { url: "/favicon.ico" },
      { url: "/logo/icon-16.png", sizes: "16x16", type: "image/png" },
      { url: "/logo/icon-32.png", sizes: "32x32", type: "image/png" },
      { url: "/logo/icon-48.png", sizes: "48x48", type: "image/png" },
    ],
    apple: "/apple-touch-icon.png",
  },
  openGraph: {
    title: TITLE_ANA,
    description: TANIM_CUMLESI,
    images: [{ url: "/og-default.png", width: 1200, height: 630 }],
    locale: "tr_TR",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: TITLE_ANA,
    description: TANIM_CUMLESI,
    images: ["/og-default.png"],
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="tr"
      data-scroll-behavior="smooth"
      className={`${sora.variable} ${fraunces.variable} h-full`}
    >
      <body className="flex min-h-full flex-col antialiased">
        <HareketSaglayici>
          <SiteHeader />
          <div className="flex-1">{children}</div>
          <SiteFooter />
        </HareketSaglayici>
      </body>
    </html>
  );
}
