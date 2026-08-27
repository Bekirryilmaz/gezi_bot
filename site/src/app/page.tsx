import Link from "next/link";
import { SiteHeader } from "@/components/SiteHeader";
import { sehirleriGetir } from "@/lib/api";

export default async function AnaSayfa() {
  let sehirIsim = "Samsun";
  try {
    const sehirler = await sehirleriGetir();
    sehirIsim = sehirler[0]?.isim ?? "Samsun";
  } catch {
    // API kapalıysa marka yine ayakta kalsın
  }

  return (
    <main>
      <section className="hero-dalga relative min-h-[100svh] overflow-hidden text-white">
        <SiteHeader />
        <div className="anim-nefes pointer-events-none absolute -right-16 top-24 h-64 w-64 rounded-full bg-bordo/30 blur-3xl" />
        <div className="relative mx-auto flex min-h-[100svh] max-w-6xl flex-col justify-end px-5 pb-16 pt-28 md:px-8 md:pb-20">
          <p className="anim-yukselt font-display text-5xl leading-none tracking-tight md:text-7xl lg:text-8xl">
            ŞAMANDIRA
          </p>
          <h1 className="anim-yukselt-gec mt-5 max-w-xl font-display text-2xl font-medium leading-snug text-white/95 md:text-3xl">
            {sehirIsim} kıyısında, sana özel bir gezi yolu.
          </h1>
          <p className="anim-yukselt-daha-gec mt-4 max-w-md text-base text-white/80 md:text-lg">
            İlçeleri haritada oku, havaya bak, gün gün rotanı kur.
          </p>
          <div className="anim-yukselt-daha-gec mt-8 flex flex-wrap gap-3">
            <Link
              href="/kesfet"
              className="rounded-full bg-gunes px-6 py-3 text-sm font-semibold text-deniz-derin transition hover:brightness-105"
            >
              Keşfe başla
            </Link>
            <Link
              href="/sehir/samsun/rota"
              className="rounded-full border border-white/40 px-6 py-3 text-sm font-medium text-white transition hover:bg-white/10"
            >
              Rota oluştur
            </Link>
          </div>
        </div>
      </section>

      <section className="atmosfer px-5 py-20 md:px-8">
        <div className="mx-auto grid max-w-6xl gap-12 md:grid-cols-3">
          {[
            {
              baslik: "Keşfet",
              metin: "Samsun’un 17 ilçesini haritada seç; vibe, lezzet, ipucu.",
              href: "/kesfet",
            },
            {
              baslik: "Bölgeler",
              metin: "81 ili haritada seç; kısa özet, bölge ve öne çıkanlar.",
              href: "/bolgeler",
            },
            {
              baslik: "Rota",
              metin: "Hava durumuna bak, ilgi alanına göre gün gün plan kur.",
              href: "/sehir/samsun/rota",
            },
          ].map((oge) => (
            <Link key={oge.baslik} href={oge.href} className="group block">
              <h2 className="font-display text-3xl text-deniz transition group-hover:text-bordo">
                {oge.baslik}
              </h2>
              <p className="mt-3 text-ink/70">{oge.metin}</p>
              <span className="mt-4 inline-block text-sm font-medium text-bordo">
                İncele →
              </span>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
