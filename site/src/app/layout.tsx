import type { Metadata } from "next";
import { Fraunces, Sora } from "next/font/google";
import { SiteFooter } from "@/components/SiteFooter";
import "./globals.css";

const sora = Sora({
  variable: "--font-sora",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

const fraunces = Fraunces({
  variable: "--font-fraunces",
  subsets: ["latin"],
  weight: ["500", "600", "700"],
});

export const metadata: Metadata = {
  title: {
    default: "Rotam — Karadeniz’de senin rotan",
    template: "%s · Rotam",
  },
  description:
    "Samsun’dan başlayan kişisel gezi platformu. Yerleri keşfet, bölgeleri oku, gün gün rota kur.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="tr" className={`${sora.variable} ${fraunces.variable} h-full`}>
      <body className="flex min-h-full flex-col antialiased">
        <div className="flex-1">{children}</div>
        <SiteFooter />
      </body>
    </html>
  );
}
