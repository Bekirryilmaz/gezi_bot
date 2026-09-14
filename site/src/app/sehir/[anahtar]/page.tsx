import { SayfaHero } from "@/components/layout/SayfaHero";
import { BosDurum } from "@/components/ui/BosDurum";
import { Dugme } from "@/components/ui/Dugme";
import { FiltreCip } from "@/components/ui/FiltreCip";
import { FiltreSatiri } from "@/components/ui/FiltreSatiri";
import { YerKarti } from "@/components/ui/YerKarti";
import { RevealListe, RevealOge } from "@/components/hareket/Reveal";
import { CTA_FILTRE_TEMIZLE } from "@/lib/marka";
import { apiDurumu, sehirleriGetir, yerleriGetir } from "@/lib/api";
import { ANA_KATEGORILER } from "@/lib/sabitler";

type Props = {
  params: Promise<{ anahtar: string }>;
  searchParams: Promise<{ kategori?: string }>;
};

export async function generateMetadata({ params }: Props) {
  const { anahtar } = await params;
  const sehirler = await sehirleriGetir().catch(() => []);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const isim = sehir?.isim ?? anahtar;
  return {
    title: `${isim} gezilecek yerler`,
    description: `${isim} gezilecek yerleri deneyim eksenlerine göre işaretli. Kategoriye göre süz, skor kırılımını oku, gün gün rota kur.`,
  };
}

export default async function SehirKesifSayfasi({ params, searchParams }: Props) {
  const { anahtar } = await params;
  const { kategori } = await searchParams;

  const [sehirSonucu, listeSonucu] = await Promise.allSettled([
    sehirleriGetir(),
    yerleriGetir(anahtar, {
      anaKategori: kategori,
      limit: 60,
    }),
  ]);
  const sehirler = sehirSonucu.status === "fulfilled" ? sehirSonucu.value : [];
  const liste =
    listeSonucu.status === "fulfilled"
      ? listeSonucu.value
      : { yerler: [], toplam_sayi: 0 };
  const listeHatasi = listeSonucu.status === "rejected" ? listeSonucu.reason : null;
  const yerler = liste.yerler;
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const baslik = sehir?.isim ?? anahtar;

  return (
    <main>
      <SayfaHero
        etiket="Keşfet"
        baslik={`${baslik} gezilecek yerler`}
        ozet="Önce cevap: bu listedeki yerler deneyim eksenlerine göre sıralanır. Kategori süz, bir karta gir, kırılımı oku."
      />

      <div className="bg-kagit/92 border-bordo/12 sticky top-14 z-40 border-b md:top-16">
        <div className="kabuk py-3">
          <FiltreSatiri>
            <FiltreCip
              href={`/sehir/${anahtar}`}
              aktif={!kategori}
              sayi={liste.toplam_sayi}
            >
              Tümü
            </FiltreCip>
            {ANA_KATEGORILER.filter((k) => k.deger !== "konaklama").map((k) => (
              <FiltreCip
                key={k.deger}
                href={`/sehir/${anahtar}?kategori=${k.deger}`}
                aktif={kategori === k.deger}
              >
                {k.etiket}
              </FiltreCip>
            ))}
          </FiltreSatiri>
        </div>
      </div>

      <div className="kabuk py-12">
        <p className="text-ink/50 text-sm tabular-nums">
          {liste.toplam_sayi.toLocaleString("tr-TR")} yer işaretli
        </p>

        {listeHatasi ? (
          <BosDurum className="mt-6" tip={apiDurumu(listeHatasi)} />
        ) : yerler.length === 0 ? (
          <BosDurum
            className="mt-6"
            tip={kategori ? "filtre" : "veri"}
            cta={
              kategori
                ? { href: `/sehir/${anahtar}`, etiket: CTA_FILTRE_TEMIZLE }
                : { href: `/sehir/${anahtar}/rota`, etiket: "Rotanı kur" }
            }
          />
        ) : (
          <RevealListe className="kart-liste mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {yerler.map((yer) => (
              <RevealOge key={yer.id}>
                <YerKarti yer={yer} />
              </RevealOge>
            ))}
          </RevealListe>
        )}

        <div className="mt-12 flex flex-wrap gap-3">
          <Dugme href={`/sehir/${anahtar}/rota`} varyant="birincil">
            Bu şehir için rota kur
          </Dugme>
          <Dugme href={`/sehir/${anahtar}/bolgeler`} varyant="hayalet">
            Bölgeyi tanı
          </Dugme>
        </div>
      </div>
    </main>
  );
}
