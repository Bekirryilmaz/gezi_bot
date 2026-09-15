import { KesfetKararAlani } from "@/components/kesfet/KesfetKararAlani";
import { BosDurum } from "@/components/ui/BosDurum";
import { apiDurumu, aramaFiltreleriniGetir, sehirKapsaminiGetir } from "@/lib/api";
import { filtreleriUrlOku } from "@/lib/arama-state";

type Props = {
  params: Promise<{ anahtar: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

export async function generateMetadata({ params }: Props) {
  const { anahtar } = await params;
  const kapsam = await sehirKapsaminiGetir(anahtar).catch(() => null);
  const isim = kapsam?.sehir_ismi ?? anahtar;
  return {
    title: `${isim} için Keşfet`,
    description: `${isim} kapsamındaki yayımlanmış yerleri ziyaret amacın, zorunlu koşulların ve önemli bilgi sınırlarıyla değerlendir.`,
  };
}

function urlParams(ham: Record<string, string | string[] | undefined>): URLSearchParams {
  const sonuc = new URLSearchParams();
  for (const [anahtar, deger] of Object.entries(ham)) {
    if (Array.isArray(deger)) deger.forEach((oge) => sonuc.append(anahtar, oge));
    else if (deger !== undefined) sonuc.set(anahtar, deger);
  }
  return sonuc;
}

export default async function SehirKesfetSayfasi({ params, searchParams }: Props) {
  const { anahtar } = await params;
  const ham = await searchParams;
  const ilk = filtreleriUrlOku(urlParams({ ...ham, sehir: anahtar }));
  const [kapsamSonucu, katalogSonucu] = await Promise.allSettled([
    sehirKapsaminiGetir(anahtar),
    aramaFiltreleriniGetir(anahtar),
  ]);
  if (kapsamSonucu.status === "rejected" || katalogSonucu.status === "rejected") {
    const hata =
      kapsamSonucu.status === "rejected"
        ? kapsamSonucu.reason
        : katalogSonucu.status === "rejected"
          ? katalogSonucu.reason
          : new Error("Kapsam yüklenemedi.");
    return (
      <main className="bg-kagit px-5 pt-28 pb-16">
        <div className="kabuk">
          <BosDurum tip={apiDurumu(hata)} />
        </div>
      </main>
    );
  }
  return (
    <main className="bg-kagit min-h-screen pt-24 pb-16">
      <div className="kabuk">
        <KesfetKararAlani
          kapsam={kapsamSonucu.value}
          filtreKatalogu={katalogSonucu.value}
          ilkSorgu={ilk.q}
          ilkFiltreler={ilk.filtreler}
        />
      </div>
    </main>
  );
}
