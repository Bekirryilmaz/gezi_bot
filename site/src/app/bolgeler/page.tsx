import { SiteHeader } from "@/components/SiteHeader";
import { BolgelerPaneli } from "@/components/discovery/BolgelerPaneli";

export const metadata = {
  title: "Bölgeler",
  description:
    "Türkiye’nin dört bir yanı, kendi ritminle. 81 ili haritada gez; tescilli yürüyüşler, ikonik yolculuklar ve festival takvimini keşfet.",
  openGraph: {
    siteName: "ŞAMANDIRA",
    title: "Bölgeler · ŞAMANDIRA",
  },
};

const BOLGELER_OZET =
  "Her coğrafya ayrı bir hikâye, her viraj yeni bir his. Karadeniz’in sisli yaylalarından Akdeniz’in antik patikalarına, bozkırın dinginliğinden Ege’nin zeytin kokulu kıyılarına kadar Türkiye’nin en özel rotalarını keşfet. İster adımlarını tarihe bas, ister direksiyonu manzaraya kır.";

export default function BolgelerSayfasi() {
  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-14 pt-24 text-white">
        <SiteHeader />
        <div className="mx-auto max-w-6xl px-4 md:px-8">
          <p className="text-sm tracking-[0.2em] text-white/55">
            KEŞİF & COĞRAFYA
          </p>
          <h1 className="mt-3 font-display text-2xl font-bold tracking-tight sm:text-3xl md:text-5xl">
            Türkiye’nin Dört Bir Yanı, Kendi Ritminle
          </h1>
          <p className="mt-5 max-w-3xl text-base leading-relaxed text-white/80 md:text-lg">
            {BOLGELER_OZET}
          </p>
        </div>
      </div>
      <div className="mx-auto max-w-6xl px-4 py-10 md:px-8">
        <BolgelerPaneli />
      </div>
    </main>
  );
}
