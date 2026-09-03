import type { Metadata, Viewport } from "next";
import { Fraunces, Sora } from "next/font/google";
import { SiteFooter } from "@/components/SiteFooter";
import "./globals.css";

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

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
    default: "ŞAMANDIRA — Karadeniz’de senin rotan",
    template: "%s · ŞAMANDIRA",
  },
  description:
    "Samsun’dan başlayan kişisel gezi platformu. İlçeleri haritada keşfet, hava durumuna bak, gün gün rota kur.",
  applicationName: "ŞAMANDIRA",
  openGraph: {
    type: "website",
    locale: "tr_TR",
    siteName: "ŞAMANDIRA",
    title: "ŞAMANDIRA — Karadeniz’de senin rotan",
    description:
      "Samsun’dan başlayan kişisel gezi platformu. İlçeleri haritada keşfet, hava durumuna bak, gün gün rota kur.",
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="tr" className={`${sora.variable} ${fraunces.variable} h-full w-full overflow-x-hidden`}>
      <body className="flex min-h-full w-full max-w-full flex-col overflow-x-hidden antialiased">
        <div className="min-w-0 max-w-full flex-1">{children}</div>
        <SiteFooter />
      </body>
    </html>
  );
}
