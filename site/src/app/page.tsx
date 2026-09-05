import { HeroKapak } from "@/components/hero/HeroKapak";
import { BolumBasligi } from "@/components/ui/BolumBasligi";
import { Dugme } from "@/components/ui/Dugme";
import { IstatistikBandi } from "@/components/ui/IstatistikBandi";
import { SehirKarti } from "@/components/ui/SehirKarti";
import { Reveal, RevealListe, RevealOge } from "@/components/hareket/Reveal";
import { CTA_BIRINCIL, TANIM_CUMLESI } from "@/lib/marka";
import { sehirleriGetir, yerleriGetir } from "@/lib/api";
import { DENEYIM_EKSENLERI } from "@/lib/sabitler";

export default async function AnaSayfa() {
  let sehirIsim = "Samsun";
  let sehirAnahtar = "samsun";
  let yerSayisi = 0;
  try {
    const [sehirler, liste] = await Promise.all([
      sehirleriGetir(),
      yerleriGetir("samsun", { limit: 1 }),
    ]);
    sehirIsim = sehirler[0]?.isim ?? "Samsun";
    sehirAnahtar = sehirler[0]?.anahtar ?? "samsun";
    yerSayisi = liste.toplam_sayi;
  } catch {
    // API kapaliysa marka yine ayakta kalsin
  }

  return (
    <main>
      <HeroKapak sehirAnahtari={sehirAnahtar} />

      <section className="bg-kagit px-5 py-20 md:px-8">
        <div className="mx-auto max-w-6xl">
          <Reveal>
            <p className="text-ink/80 max-w-2xl text-[17px] leading-relaxed">
              {TANIM_CUMLESI} İlk çıkış şehri {sehirIsim}; kapsam tüm Türkiye.
            </p>
          </Reveal>
          <Reveal delay={0.08}>
            <IstatistikBandi
              className="mt-12"
              ogeler={[
                {
                  deger: yerSayisi > 0 ? yerSayisi.toLocaleString("tr-TR") : "—",
                  etiket: "İşaretli yer",
                },
                { deger: "1", etiket: "Açık şehir" },
                {
                  deger: String(DENEYIM_EKSENLERI.length),
                  etiket: "Deneyim ekseni",
                },
              ]}
            />
          </Reveal>
        </div>
      </section>

      <section className="bg-kagit-koyu/50 px-5 py-20 md:px-8">
        <div className="mx-auto max-w-6xl">
          <Reveal>
            <BolumBasligi
              etiket="Ne yapar?"
              baslik="Şehri üç yoldan oku"
              ozet="Keşif listesi, ilçe profilleri ve gün gün rota — hepsi aynı skor dilinde."
            />
          </Reveal>
          <RevealListe className="mt-10 grid gap-5 md:grid-cols-3">
            {[
              {
                baslik: "Keşfet",
                metin: "Gezilecek yerleri deneyim eksenlerine göre sıralı gör.",
                href: `/sehir/${sehirAnahtar}`,
              },
              {
                baslik: "Bölgeler",
                metin: "İlçelerin tanıtımı ve ziyaretçi izlenimi, yan yana.",
                href: `/sehir/${sehirAnahtar}/bolgeler`,
              },
              {
                baslik: "Rota",
                metin: "Kaç günün varsa planı kur; her durağın gerekçesi açık.",
                href: `/sehir/${sehirAnahtar}/rota`,
              },
            ].map((o) => (
              <RevealOge key={o.baslik}>
                <div className="kart-isik border-deniz/10 flex h-full flex-col rounded-2xl border bg-white p-6">
                  <h3 className="font-display text-deniz-derin text-2xl">{o.baslik}</h3>
                  <p className="text-ink/70 mt-3 flex-1 text-sm leading-relaxed">
                    {o.metin}
                  </p>
                  <div className="mt-6">
                    <Dugme href={o.href} varyant="hayalet">
                      İncele
                    </Dugme>
                  </div>
                </div>
              </RevealOge>
            ))}
          </RevealListe>
        </div>
      </section>

      <section className="bg-kagit px-5 py-20 md:px-8">
        <div className="mx-auto max-w-6xl">
          <Reveal>
            <BolumBasligi
              etiket="Şehir"
              baslik="Açık şehir"
              ozet="Yeni şehir eklemek tasarımı değiştirmez; veri gelir, işaretlenir."
            />
          </Reveal>
          <Reveal delay={0.1} className="mt-10">
            <SehirKarti
              isim={sehirIsim}
              anahtar={sehirAnahtar}
              yerSayisi={yerSayisi || undefined}
              ozet={`${sehirIsim} ilk çıkış plajı. Gezilecek yerler işaretli; gün gün rota kurulur.`}
            />
          </Reveal>
        </div>
      </section>

      <section className="bg-deniz-derin text-kopuk relative overflow-hidden px-5 py-24 md:px-8">
        <div
          className="pointer-events-none absolute inset-0"
          aria-hidden="true"
          style={{
            background:
              "radial-gradient(600px 240px at 80% 20%, #d6402c44, transparent 60%)",
          }}
        />
        <div className="relative mx-auto max-w-6xl text-center">
          <Reveal>
            <h2 className="font-display text-4xl tracking-[-0.02em] md:text-6xl">
              Rotanı kur, şehri oku.
            </h2>
            <p className="text-kopuk/70 mx-auto mt-4 max-w-lg">
              Kaç günün ve ne aradığın belli olsun; gerisini skor kırılımı taşır.
            </p>
            <div className="mt-8 flex justify-center">
              <Dugme href={`/sehir/${sehirAnahtar}/rota`} varyant="birincil">
                {CTA_BIRINCIL}
              </Dugme>
            </div>
          </Reveal>
        </div>
      </section>
    </main>
  );
}
