import { SayfaHero } from "@/components/layout/SayfaHero";
import { BosDurum } from "@/components/ui/BosDurum";
import { Dugme } from "@/components/ui/Dugme";
import { DuyguOzeti } from "@/components/ui/DuyguOzeti";
import { Reveal } from "@/components/hareket/Reveal";
import { bolgeleriGetir, sehirleriGetir } from "@/lib/api";
import { duyguEtiketi } from "@/lib/sabitler";

type Props = {
  params: Promise<{ anahtar: string }>;
};

export async function generateMetadata({ params }: Props) {
  const { anahtar } = await params;
  const sehirler = await sehirleriGetir().catch(() => []);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const isim = sehir?.isim ?? anahtar;
  return {
    title: `${isim} bölgeleri`,
    description: `${isim} ilçe ve bölge profilleri: tanıtım ile ziyaretçi izlenimi yan yana. Konaklama üssü seçip rota kur.`,
  };
}

export default async function BolgelerSayfasi({ params }: Props) {
  const { anahtar } = await params;
  const [sehirler, bolgeler] = await Promise.all([
    sehirleriGetir().catch(() => []),
    bolgeleriGetir(anahtar).catch(() => []),
  ]);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const isim = sehir?.isim ?? anahtar;

  return (
    <main>
      <SayfaHero
        etiket="Bölgeler"
        baslik={`${isim} ve ilçeleri`}
        ozet="Önce tanıtım, sonra orada yaşayanların ve gidenlerin ortak izlenimi."
      />

      <div className="mx-auto max-w-6xl space-y-10 px-5 py-12 md:px-8">
        {bolgeler.length === 0 ? (
          <BosDurum cta={{ href: `/sehir/${anahtar}`, etiket: "Keşfe dön" }} />
        ) : (
          bolgeler.map((bolge, i) => (
            <Reveal key={bolge.bolge_adi} delay={Math.min(i * 0.04, 0.2)}>
              <article className="border-deniz/10 rounded-2xl border bg-white p-6 md:p-8">
                <div className="flex flex-wrap items-baseline justify-between gap-3">
                  <h2 className="font-display text-deniz text-3xl tracking-[-0.02em] capitalize">
                    {bolge.bolge_adi}
                    <span className="text-ink/45 ml-3 font-sans text-base font-normal">
                      {bolge.ilce_mi ? "ilçe" : "şehir geneli"}
                    </span>
                  </h2>
                  <Dugme
                    href={`/sehir/${anahtar}/rota?konaklama_bolge=${encodeURIComponent(bolge.bolge_adi)}`}
                    varyant="hayalet"
                  >
                    Bu bölgeden rota kur
                  </Dugme>
                </div>

                <section className="mt-8">
                  <h3 className="text-ink/45 text-[11px] font-medium tracking-[0.24em] uppercase">
                    Tanıtım
                  </h3>
                  {bolge.tanitim_metni ? (
                    <p className="text-ink/85 mt-2 max-w-3xl text-lg leading-relaxed">
                      {bolge.tanitim_metni}
                    </p>
                  ) : (
                    <p className="text-ink/55 mt-2">
                      Bu bölge için henüz derlenmiş bir tanıtım metni yok.
                    </p>
                  )}
                </section>

                <section className="mt-8">
                  <h3 className="text-ink/45 text-[11px] font-medium tracking-[0.24em] uppercase">
                    Kullanıcı deneyimleri
                  </h3>
                  {bolge.duygu_ozeti ? (
                    <DuyguOzeti
                      className="mt-3"
                      metin={bolge.duygu_ozeti}
                      etiket={duyguEtiketi(bolge.genel_duygu_etiketi)}
                    />
                  ) : (
                    <p className="text-ink/55 mt-2">
                      Bu bölge için henüz kullanıcı deneyimi özeti yok.
                    </p>
                  )}
                </section>
              </article>
            </Reveal>
          ))
        )}

        <Dugme href={`/sehir/${anahtar}`} varyant="ikincil">
          Keşfe dön
        </Dugme>
      </div>
    </main>
  );
}
