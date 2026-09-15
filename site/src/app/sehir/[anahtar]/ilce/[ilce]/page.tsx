import { redirect } from "next/navigation";

import { SayfaHero } from "@/components/layout/SayfaHero";
import { BosDurum } from "@/components/ui/BosDurum";
import { apiDurumu, ilceDetayiniGetir } from "@/lib/api";

type Props = { params: Promise<{ anahtar: string; ilce: string }> };

export default async function IlceSayfasi({ params }: Props) {
  const { anahtar, ilce } = await params;
  let detay;
  try {
    detay = await ilceDetayiniGetir(anahtar, ilce);
  } catch (hata) {
    return (
      <main className="bg-kagit px-5 pt-28 pb-16">
        <div className="kabuk">
          <BosDurum tip={apiDurumu(hata)} baslik="İlçe bulunamadı" />
        </div>
      </main>
    );
  }
  if (!detay.ayri_sayfa_var) redirect(detay.kesfet_url);
  return (
    <main>
      <SayfaHero
        etiket={`${detay.cografya.sehir_ismi} · İlçe`}
        baslik={detay.cografya.ilce_ismi}
        ozet={detay.kapsam_aciklamasi}
      />
      <div className="kabuk py-12">
        <ul className="grid gap-4">
          {detay.ozgun_karar_bilgileri.map((bilgi) => (
            <li key={bilgi} className="border-deniz/12 rounded-2xl border p-5">
              {bilgi}
            </li>
          ))}
        </ul>
        <a
          href={detay.kesfet_url}
          className="text-bordo mt-8 inline-block min-h-11 py-2 font-semibold underline"
        >
          Bu ilçede Keşfet
        </a>
      </div>
    </main>
  );
}
