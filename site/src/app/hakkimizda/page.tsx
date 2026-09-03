import Image from "next/image";
import { SiteHeader } from "@/components/SiteHeader";
import { IlberQuotesSlider } from "@/components/hakkimizda/IlberQuotesSlider";
import { OurLensSection } from "@/components/hakkimizda/OurLensSection";
import { EcoManifestoSection } from "@/components/hakkimizda/EcoManifestoSection";

export const metadata = {
  title: {
    absolute: "Hakkımızda | ŞAMANDIRA",
  },
  description:
    "Rotanın pusulası. İki öğrencinin seyir defteri, denizdeki şamandıra metaforu ve sahici keşif.",
};

const DEGERLER = [
  {
    ikon: "🧭",
    baslik: "Gerçek & Yaşanmış Deneyim",
    metin:
      "Algoritmaların masa başında uydurduğu değil; bizzat adımladığımız, suyunu içtiğimiz, yerlisinden dinlediğimiz sahici rotalar.",
  },
  {
    ikon: "🌊",
    baslik: "Rotanı Kişiselleştir",
    metin:
      "Herkesin tatil anlayışı bir değil. Kimi sisli yaylanın sessizliğini arar, kimi ara sokaktaki fırının çıtır pidesini. ŞAMANDIRA tek bir kalıba sokmaz, ruh haline göre yol çizer.",
  },
  {
    ikon: "🌿",
    baslik: "Doğaya ve Kültüre Saygı",
    metin:
      "Ayak izimizden başka hiçbir şey bırakmadığımız; yerel esnafı koruyan, saklı koyları ve vadileri tahrip etmeden keşfeden sorumlu gezginlik anlayışı.",
  },
] as const;

export default function HakkimizdaSayfasi() {
  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-16 pt-24 text-white">
        <SiteHeader />
        <div className="mx-auto max-w-6xl space-y-6 px-4 md:px-8">
          <p className="text-sm tracking-[0.2em] text-white/55">
            ROTANIN PUSULASI & BİZ KİMİZ
          </p>
          <h1 className="font-display text-2xl font-bold leading-tight tracking-tight sm:text-3xl md:text-5xl">
            Yolda Öğrenen İki Öğrencinin Seyir Defteri
          </h1>
          <p className="max-w-4xl text-base leading-relaxed text-white/80 md:text-lg">
            ŞAMANDIRA, her yıl sırt çantasını alıp Türkiye&apos;nin farklı bir
            coğrafyasına doğru yola çıkan iki üniversite öğrencisinin ortak
            hayaliyle kuruldu. Bizim için seyahat etmek; ezbere hazırlanmış
            popüler mekan listelerini tüketmek değil, sokakların kokusunu içine
            çekmek, yerlinin çay içtiği kahvede oturmak ve haritada adı geçmeyen
            patikaları keşfetmektir. Çünkü inanıyoruz ki; ayak basılmadan,
            kaybolunmadan ve yerinde yaşanmadan hiçbir bilgi gerçek değerine
            ulaşamaz.
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-6xl space-y-16 px-4 py-12 md:space-y-20 md:px-8 md:py-16">
        <section className="grid items-stretch gap-8 overflow-hidden rounded-2xl border border-teal-100/60 bg-white/70 shadow-sm backdrop-blur lg:grid-cols-2">
          <div className="relative min-h-[240px] overflow-hidden lg:min-h-full">
            <Image
              src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=80"
              alt="Açık denizde ufuğa uzanan kıyı"
              fill
              className="object-cover"
              sizes="(max-width: 1024px) 100vw, 50vw"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-deniz-derin/70 via-deniz-derin/20 to-transparent lg:bg-gradient-to-r" />
          </div>
          <div className="space-y-6 p-4 md:p-10">
            <h2 className="font-display text-2xl font-bold tracking-tight text-deniz sm:text-3xl md:text-4xl">
              Denizde Bir Sınır, Karada Bir Rehber: Neden ŞAMANDIRA?
            </h2>
            <div className="space-y-6 text-base leading-relaxed text-slate-700 md:text-lg">
              <p>
                Denizcilikte şamandıra; hırçın dalgaların arasında gemilere
                güvenli rotayı fısıldayan, kayalıkları ve sığ suları haber veren,
                rotasından sapan denizciye yönünü hatırlatan en kadim kılavuzdur.
                Açık denizde fırtına kopsa da o sabit kalır; sınırı korur,
                derinliği gösterir ve tehlikeli sulardan uzak tutar.
              </p>
              <p>
                Biz de çıktığımız bu yolculukta aynısını yapmak istedik:
                İnternetin bilgi kirliliğiyle dolu, herkesi aynı tekdüze
                mekanlara yönlendiren ve yerel ruhu yansıtmayan kalabalık
                sularında gezginlere bir şamandıra olmak. Samsun’dan başlayıp tüm
                Karadeniz’e ve Türkiye’ye uzanırken; rotanızı kaybetmeden, yerel
                lezzetin ve el değmemiş doğanın tam kalbine güvenle demir
                atmanızı sağlamak için buradayız.
              </p>
            </div>
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="font-display text-3xl text-deniz md:text-4xl">
            3 Temel Değerimiz
          </h2>
          <ul className="grid gap-8 md:grid-cols-3">
            {DEGERLER.map((deger) => (
              <li
                key={deger.baslik}
                className="rounded-2xl border border-teal-100/60 bg-white/70 p-4 shadow-sm backdrop-blur md:p-6"
              >
                <p className="text-3xl" aria-hidden>
                  {deger.ikon}
                </p>
                <h3 className="mt-4 font-display text-xl text-deniz">
                  {deger.baslik}
                </h3>
                <p className="mt-3 leading-relaxed text-slate-700">{deger.metin}</p>
              </li>
            ))}
          </ul>
        </section>

        <IlberQuotesSlider />
        <OurLensSection />
        <EcoManifestoSection />
      </div>
    </main>
  );
}
