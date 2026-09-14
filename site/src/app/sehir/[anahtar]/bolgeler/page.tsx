import { SayfaHero } from "@/components/layout/SayfaHero";
import { BosDurum } from "@/components/ui/BosDurum";
import { Dugme } from "@/components/ui/Dugme";
import { Reveal } from "@/components/hareket/Reveal";
import { apiDurumu, bolgeleriGetir, sehirleriGetir } from "@/lib/api";

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
    description: `${isim} ilçe ve bölge tanıtımları; bölgeyi tanı ve tek günlük rota oluştur.`,
  };
}

export default async function BolgelerSayfasi({ params }: Props) {
  const { anahtar } = await params;
  const [sehirSonucu, bolgeSonucu] = await Promise.allSettled([
    sehirleriGetir(),
    bolgeleriGetir(anahtar),
  ]);
  const sehirler = sehirSonucu.status === "fulfilled" ? sehirSonucu.value : [];
  const bolgeler = bolgeSonucu.status === "fulfilled" ? bolgeSonucu.value : [];
  const bolgeHatasi = bolgeSonucu.status === "rejected" ? bolgeSonucu.reason : null;
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const isim = sehir?.isim ?? anahtar;

  return (
    <main>
      <SayfaHero
        etiket="Bölgeler"
        baslik={`${isim} ve ilçeleri`}
        ozet="Şehri ve ilçelerini temel tanıtım bilgileriyle keşfet."
      />

      <div className="kabuk space-y-10 py-12">
        {bolgeHatasi ? (
          <BosDurum tip={apiDurumu(bolgeHatasi)} />
        ) : bolgeler.length === 0 ? (
          <BosDurum
            tip="hazirlaniyor"
            cta={{ href: `/sehir/${anahtar}`, etiket: "Keşfe dön" }}
          />
        ) : (
          bolgeler.map((bolge, i) => (
            <Reveal key={bolge.bolge_adi} delay={Math.min(i * 0.04, 0.2)}>
              <article className="kart-kabuk p-6 md:p-8">
                <div className="flex flex-wrap items-baseline justify-between gap-3">
                  <h2 className="yazi-alt text-bordo capitalize">
                    {bolge.bolge_adi}
                    <span className="text-ink/45 ml-3 font-sans text-base font-normal">
                      {bolge.ilce_mi ? " ilçe" : " şehir geneli"}
                    </span>
                  </h2>
                  <Dugme href={`/sehir/${anahtar}/rota`} varyant="bolum">
                    Bugünün rotasını kur
                  </Dugme>
                </div>

                <section className="mt-8">
                  <h3 className="etiket text-ink/45">Tanıtım</h3>
                  {bolge.tanitim_metni ? (
                    <p className="yazi-govde text-ink/85 mt-2 max-w-[42rem]">
                      {bolge.tanitim_metni}
                    </p>
                  ) : (
                    <p className="text-ink/55 mt-2">
                      Bu bölge için henüz derlenmiş bir tanıtım metni yok.
                    </p>
                  )}
                </section>

                <span className="su-hatti" />
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
