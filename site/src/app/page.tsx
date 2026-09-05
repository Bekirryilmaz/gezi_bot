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
      <HeroKapak sehirAnahtari={sehirAnahtar} yerSayisi={yerSayisi} />

      <section className="bolum bg-kagit">
        <div className="kabuk">
          <Reveal>
            <p className="yazi-govde text-ink/80 max-w-[42rem]">
              {TANIM_CUMLESI} İlk çıkış şehri {sehirIsim}; kapsam tüm Türkiye.
            </p>
          </Reveal>
          <Reveal delay={0.08}>
            <IstatistikBandi
              className="mt-12"
              ogeler={[
                ...(yerSayisi > 0 ? [{ deger: yerSayisi, etiket: "İşaretli yer" }] : []),
                {
                  deger: 1,
                  etiket: "Açık şehir",
                  baglam: `${sehirIsim}'da başladık`,
                },
                { deger: DENEYIM_EKSENLERI.length, etiket: "Deneyim ekseni" },
              ]}
            />
          </Reveal>
        </div>
      </section>

      <section className="bolum bg-kagit-koyu/60">
        <div className="kabuk">
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
                baslik: "Nereye gidilir?",
                metin: "Gezilecek yerleri deneyim eksenlerine göre sıralı gör.",
                href: `/sehir/${sehirAnahtar}`,
                cta: "Keşfe başla",
              },
              {
                baslik: "Hangi bölge sana göre?",
                metin: "İlçelerin tanıtımı ve ziyaretçi izlenimi, yan yana.",
                href: `/sehir/${sehirAnahtar}/bolgeler`,
                cta: "Bölgeyi tanı",
              },
              {
                baslik: "Kaç günün var?",
                metin: "Kaç günün varsa planı kur; her durağın gerekçesi açık.",
                href: `/sehir/${sehirAnahtar}/rota`,
                cta: "Rotanı kur",
              },
            ].map((o) => (
              <RevealOge key={o.baslik}>
                <article className="kart-kabuk flex h-full flex-col p-6">
                  <h3 className="yazi-alt text-bordo">{o.baslik}</h3>
                  <p className="yazi-govde text-ink/70 mt-3 flex-1">{o.metin}</p>
                  <div className="relative z-10 mt-6">
                    <Dugme href={o.href} varyant="bolum">
                      {o.cta}
                    </Dugme>
                  </div>
                  <span className="su-hatti" />
                </article>
              </RevealOge>
            ))}
          </RevealListe>
        </div>
      </section>

      <section className="bolum bg-kagit">
        <div className="kabuk">
          <Reveal>
            <BolumBasligi
              etiket="Nereye gidilir?"
              baslik="Açık şehir"
              ozet="Yeni şehir eklemek tasarımı değiştirmez; veri gelir, işaretlenir."
              aksiyon={{ href: `/sehir/${sehirAnahtar}`, etiket: "Keşfe başla" }}
            />
          </Reveal>
          <Reveal delay={0.1} className="mt-10">
            <SehirKarti
              varyant="vitrin"
              isim={sehirIsim}
              anahtar={sehirAnahtar}
              yerSayisi={yerSayisi || undefined}
              ozet={`${sehirIsim} ilk çıkış plajı. Gezilecek yerler işaretli; gün gün rota kurulur.`}
            />
          </Reveal>
        </div>
      </section>

      <section className="doku-koyu bg-bordo text-kagit bolum-doruk relative overflow-hidden">
        <div className="kabuk relative text-center">
          <Reveal>
            <h2 className="yazi-bolum">Rotanı kur, şehri oku.</h2>
            <p className="yazi-govde text-kagit/75 mx-auto mt-4 max-w-lg">
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
