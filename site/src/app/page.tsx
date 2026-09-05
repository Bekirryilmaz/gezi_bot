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
        <div className="anim-nefes bg-yosun/25 pointer-events-none absolute top-24 -right-16 h-64 w-64 rounded-full blur-3xl" />
        <div className="relative mx-auto flex min-h-[100svh] max-w-6xl flex-col justify-end px-5 pt-28 pb-16 md:px-8 md:pb-20">
          <p className="anim-yukselt font-display text-5xl leading-none tracking-tight md:text-7xl lg:text-8xl">
            Şamandıra
          </p>
          <h1 className="anim-yukselt-gec font-display mt-5 max-w-xl text-2xl leading-snug font-medium text-white/95 md:text-3xl">
            {sehirIsim} kıyısında, sana özel bir gezi yolu.
          </h1>
          <p className="anim-yukselt-daha-gec mt-4 max-w-md text-base text-white/80 md:text-lg">
            Yerleri oku, ilçeleri hisset, gün gün rotanı kur.
          </p>
          <div className="anim-yukselt-daha-gec mt-8 flex flex-wrap gap-3">
            <Link
              href="/sehir/samsun"
              className="bg-gunes text-deniz-derin rounded-full px-6 py-3 text-sm font-semibold transition hover:brightness-105"
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
              metin: "Binlerce yer, yorumlardan süzülmüş duygu özetleriyle.",
              href: "/sehir/samsun",
            },
            {
              baslik: "Bölgeler",
              metin: "Şehir ve ilçeleri anlatanlar ne diyor, tek bakışta.",
              href: "/sehir/samsun/bolgeler",
            },
            {
              baslik: "Rota",
              metin:
                "İlgi alanına göre gün gün plan; konaklama senin veya bizim önerimiz.",
              href: "/sehir/samsun/rota",
            },
          ].map((oge) => (
            <Link key={oge.baslik} href={oge.href} className="group block">
              <h2 className="font-display text-deniz group-hover:text-yosun text-3xl transition">
                {oge.baslik}
              </h2>
              <p className="text-ink/70 mt-3">{oge.metin}</p>
              <span className="text-yosun mt-4 inline-block text-sm font-medium">
                İncele →
              </span>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
