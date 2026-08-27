import Image from "next/image";

const KARELER = [
  {
    src: "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=800&q=80",
    yer: "Sisli yayla",
    donus: "-rotate-2",
  },
  {
    src: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
    yer: "Saklı koy",
    donus: "rotate-1",
  },
  {
    src: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=800&q=80",
    yer: "Orman yolu",
    donus: "-rotate-1",
  },
  {
    src: "https://images.unsplash.com/photo-1439066615861-d1af74d74000?auto=format&fit=crop&w=800&q=80",
    yer: "Dağ gölü",
    donus: "rotate-2",
  },
] as const;

export function OurLensSection() {
  return (
    <section className="space-y-10">
      <div className="max-w-3xl">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-ink/45">
          Objektifimizden
        </p>
        <h2 className="mt-2 font-display text-3xl text-deniz md:text-4xl">
          Kendi Objektifimizden: Sadece Bizde Kalmasın İstedik
        </h2>
        <p className="mt-5 text-base leading-relaxed text-ink/80 md:text-lg">
          ŞAMANDIRA’da gördüğünüz birçok kare ve rota; sırt çantamızla
          adımladığımız yollarda, kendi objektifimizden yansıyan gerçek anlardan
          oluşuyor. Karadeniz’in sisli bir yaylasında sabahladığımızda ya da
          kimsenin bilmediği bir koya ayak bastığımızda hissettiğimiz o
          heyecanın yalnızca bizim anılarımızda saklı kalmasına gönlümüz razı
          olmadı. Keşfetmenin güzelliği, onu doğru insanlarla paylaşınca
          çoğalıyor.
        </p>
      </div>

      <ul className="grid grid-cols-2 gap-4 md:gap-6 lg:grid-cols-4">
        {KARELER.map((kare) => (
          <li
            key={kare.yer}
            className={`${kare.donus} hover:rotate-0 transition duration-300`}
          >
            <figure className="rounded-xl border-2 border-white/10 bg-white p-2 pb-8 shadow-[0_12px_28px_rgba(6,54,66,0.16)]">
              <div className="relative aspect-[4/5] overflow-hidden rounded-lg">
                <Image
                  src={kare.src}
                  alt={kare.yer}
                  fill
                  className="object-cover"
                  sizes="(max-width: 768px) 50vw, 25vw"
                />
                <span className="absolute left-2 top-2 rounded-full bg-deniz-derin/88 px-2 py-0.5 text-[10px] font-medium text-kopuk">
                  Bizim Kadrajımızdan
                </span>
              </div>
              <figcaption className="mt-3 px-1 text-center font-display text-sm text-deniz">
                {kare.yer}
              </figcaption>
            </figure>
          </li>
        ))}
      </ul>
    </section>
  );
}
