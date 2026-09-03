import { SiteHeader } from "@/components/SiteHeader";
import { OneriFormu } from "@/components/oneri/OneriFormu";
import { OneriSekmeler } from "@/components/oneriler/OneriSekmeler";

export const metadata = {
  title: "Önerim Var",
  description:
    "Saklı bir koy, lezzet durağı veya manzara tepesi öner. Konumunu işaretle, hikâyesini anlat; incelemeden sonra Topluluk Keşfi olarak yayınlanır.",
};

export default function OnerimVarSayfasi() {
  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-14 pt-24 text-white">
        <SiteHeader />
        <div className="mx-auto max-w-6xl px-4 md:px-8">
          <p className="text-sm uppercase tracking-[0.2em] text-white/55">
            TOPLULUK KEŞFİ
          </p>
          <h1 className="mt-3 font-display text-2xl font-bold tracking-tight sm:text-3xl md:text-5xl">
            Bir Önerim Var!
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-relaxed text-white/80 md:text-lg">
            Kimsenin bilmediği saklı bir koy, ara sokakta kalmış enfes bir lezzet
            durağı ya da huzur bulduğun bir manzara tepesi mi var? Konumunu
            işaretle, hikayesini anlat, ŞAMANDIRA rotalarına birlikte ekleyelim.
          </p>
          <OneriSekmeler aktif="form" />
        </div>
      </div>
      <div className="mx-auto w-full max-w-5xl px-4 py-10 md:px-8">
        <div className="mx-auto w-full max-w-full overflow-visible rounded-2xl bg-white/80 p-4 shadow-[0_12px_40px_rgba(6,54,66,0.08)] sm:p-6 md:p-10">
          <OneriFormu />
        </div>
      </div>
    </main>
  );
}
