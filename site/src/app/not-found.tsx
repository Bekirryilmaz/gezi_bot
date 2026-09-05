import { LogoKaro } from "@/components/marka/LogoKaro";
import { Dugme } from "@/components/ui/Dugme";
import { SAYFA_404_BASLIK } from "@/lib/marka";

export default function BulunamadiSayfasi() {
  return (
    <main className="bg-kagit text-ink relative flex min-h-[100svh] flex-col items-center justify-center overflow-hidden px-5 pt-24 pb-16">
      <div
        className="pointer-events-none absolute inset-x-0 top-[42%] flex items-center px-8"
        aria-hidden="true"
      >
        <span className="bg-ink/20 h-px flex-1" />
        <span className="mx-3">
          <LogoKaro boyut={64} dekoratif />
        </span>
        <span className="bg-ink/20 h-px flex-1" />
      </div>
      <div className="relative z-10 max-w-lg text-center">
        <p className="text-ink/55 text-[11px] tracking-[0.28em] uppercase">404</p>
        <h1 className="font-display mt-4 text-4xl tracking-[-0.02em] text-balance md:text-5xl">
          {SAYFA_404_BASLIK}
        </h1>
        <p className="text-ink/70 mt-4 text-sm leading-relaxed text-pretty">
          Bu adres bir şamandıra değil. Keşfe dön veya gün gün rotanı kur.
        </p>
        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Dugme href="/sehir/samsun" varyant="birincil">
            Keşfe başla
          </Dugme>
          <Dugme href="/sehir/samsun/rota" varyant="ikincil">
            Rotanı kur
          </Dugme>
        </div>
      </div>
    </main>
  );
}
