import { SiteHeader } from "@/components/SiteHeader";
import { OneriYonetim } from "@/components/oneri/MekanOneriYonetim";

export const metadata = {
  title: "Öneriler",
  robots: { index: false, follow: false },
};

export default function YonetimOnerilerSayfasi() {
  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-10 pt-24 text-white">
        <SiteHeader />
        <div className="mx-auto max-w-6xl px-5 md:px-8">
          <p className="text-sm uppercase tracking-[0.2em] text-white/55">Yönetim</p>
          <h1 className="mt-3 font-display text-4xl">Öneriler</h1>
          <p className="mt-3 max-w-2xl text-white/75">
            Bekleyen keşifleri onayla; onaylananlar Topluluk Keşfi etiketiyle yer
            listesine geçer.
          </p>
        </div>
      </div>
      <div className="mx-auto max-w-6xl px-5 py-10 md:px-8">
        <OneriYonetim />
      </div>
    </main>
  );
}
