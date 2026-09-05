import { SayfaHero } from "@/components/layout/SayfaHero";
import { RotaSihirbazi } from "@/components/RotaSihirbazi";
import { bolgeleriGetir, sehirleriGetir } from "@/lib/api";

type Props = {
  params: Promise<{ anahtar: string }>;
  searchParams: Promise<{
    konaklama_yer_id?: string;
    konaklama_bolge?: string;
  }>;
};

export async function generateMetadata({ params }: Props) {
  const { anahtar } = await params;
  const sehirler = await sehirleriGetir().catch(() => []);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const isim = sehir?.isim ?? anahtar;
  return {
    title: `${isim} rota planlayıcı`,
    description: `${isim} için gün gün rota kur. Konaklama bölgen belli olsun veya alternatiflerden seç; her durağın skor kırılımı açık.`,
    robots: { index: false, follow: true },
  };
}

export default async function RotaSayfasi({ params, searchParams }: Props) {
  const { anahtar } = await params;
  const sorgu = await searchParams;
  const [sehirler, bolgeler] = await Promise.all([
    sehirleriGetir().catch(() => []),
    bolgeleriGetir(anahtar).catch(() => []),
  ]);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const isim = sehir?.isim ?? anahtar;

  return (
    <main>
      <SayfaHero
        etiket="Rota"
        baslik={`${isim} için rotan`}
        ozet="Kaç günün ve ne aradığın belli olsun. Konaklama bölgen varsa oradan başla; yoksa alternatiflerden birini seç."
      />

      <div className="mx-auto max-w-6xl px-5 py-12 md:px-8">
        <RotaSihirbazi
          sehirAnahtari={anahtar}
          sehirIsim={isim}
          baslangicKonaklamaYerId={sorgu.konaklama_yer_id ?? null}
          baslangicKonaklamaBolge={sorgu.konaklama_bolge ?? null}
          bolgeler={bolgeler}
        />
      </div>
    </main>
  );
}
