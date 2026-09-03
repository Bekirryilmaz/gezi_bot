import { SiteHeader } from "@/components/SiteHeader";
import { KesfetPaneli } from "@/components/discovery/KesfetPaneli";

export const metadata = {
  title: "Samsun",
  description:
    "Samsun’un 17 ilçesini haritada gez. Vibe, yöresel lezzet ve seyahat ipuçları.",
  openGraph: {
    siteName: "ŞAMANDIRA",
    title: "Samsun · ŞAMANDIRA",
  },
};

const SAMSUN_OZET =
  "Karadeniz’in incisi Samsun; 19 Mayıs ruhunu taşıyan tarihi mirası, Kızılırmak ve Yeşilırmak deltalarının verimli doğası, kilometrelerce uzanan Atakum sahili ve zengin mutfak kültürüyle keşfedilmeyi bekleyen 17 farklı karaktere sahip.";

export default async function KesfetSayfasi() {
  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-14 pt-24 text-white">
        <SiteHeader />
        <div className="mx-auto max-w-6xl px-4 md:px-8">
          <p className="text-sm uppercase tracking-[0.2em] text-white/55">Keşfet</p>
          <h1 className="mt-3 font-display text-2xl font-bold tracking-tight sm:text-3xl md:text-5xl">
            Samsun
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-relaxed text-white/80 md:text-lg">
            {SAMSUN_OZET}
          </p>
        </div>
      </div>
      <div className="mx-auto max-w-6xl px-4 py-10 md:px-8">
        <KesfetPaneli sehirAnahtari="samsun" />
      </div>
    </main>
  );
}
