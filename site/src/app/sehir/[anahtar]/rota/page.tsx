import { SayfaHero } from "@/components/layout/SayfaHero";
import { GunlukRotaSihirbazi } from "@/components/GunlukRotaSihirbazi";
import { sehirleriGetir } from "@/lib/api";

type Props = {
  params: Promise<{ anahtar: string }>;
};

export async function generateMetadata({ params }: Props) {
  const { anahtar } = await params;
  const sehirler = await sehirleriGetir().catch(() => []);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const isim = sehir?.isim ?? anahtar;
  return {
    title: `${isim} rota planlayıcı`,
    description: `${isim} için ilgi alanlarına göre tek günlük Akıllı Rota oluştur.`,
    robots: { index: false, follow: true },
  };
}

export default async function RotaSayfasi({ params }: Props) {
  const { anahtar } = await params;
  const sehirler = await sehirleriGetir().catch(() => []);
  const sehir = sehirler.find((s) => s.anahtar === anahtar);
  const isim = sehir?.isim ?? anahtar;

  return (
    <main>
      <SayfaHero
        etiket="Rota"
        baslik={`${isim} için rotan`}
        ozet="Bugün ne aradığını seç; Akıllı Rota tek günlük bir plan oluştursun."
      />

      <div className="kabuk py-12">
        <GunlukRotaSihirbazi sehirAnahtari={anahtar} sehirIsim={isim} />
      </div>
    </main>
  );
}
