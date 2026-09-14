import Link from "next/link";
import { SayfaHero } from "@/components/layout/SayfaHero";
import { BosDurum } from "@/components/ui/BosDurum";
import { Dugme } from "@/components/ui/Dugme";
import { Plaka } from "@/components/ui/Plaka";
import { Rozet } from "@/components/ui/Rozet";
import { apiDurumu, yerDetayiGetir } from "@/lib/api";
import { altKategoriEtiketi, kategoriEtiketi } from "@/lib/sabitler";

type Props = {
  params: Promise<{ id: string }>;
};

export async function generateMetadata({ params }: Props) {
  const { id } = await params;
  try {
    const yer = await yerDetayiGetir(id);
    return {
      title: yer.isim,
      description:
        yer.tanitim_metni?.slice(0, 155) ||
        yer.aciklama?.slice(0, 155) ||
        `${yer.isim} — ${kategoriEtiketi(yer.ana_kategori)}. Şamandıra gezilecek yerler rehberi.`,
    };
  } catch {
    return { title: "Yer" };
  }
}

function googleMapsUrl(enlem: number, boylam: number, isim: string): string {
  const sorgu = encodeURIComponent(`${isim} @${enlem},${boylam}`);
  return `https://www.google.com/maps/search/?api=1&query=${sorgu}`;
}

export default async function YerDetaySayfasi({ params }: Props) {
  const { id } = await params;
  let yer;
  try {
    yer = await yerDetayiGetir(id);
  } catch (hata) {
    return (
      <main className="bg-kagit px-5 pt-28 pb-16">
        <div className="kabuk">
          <BosDurum
            tip={apiDurumu(hata)}
            baslik={apiDurumu(hata) === "empty" ? "Yer bulunamadı" : undefined}
            metin={
              apiDurumu(hata) === "empty"
                ? "Keşfe dönüp başka bir işaret seçebilirsin."
                : undefined
            }
            cta={{ href: "/sehir/samsun", etiket: "Keşfe dön" }}
          />
        </div>
      </main>
    );
  }

  const tanitim = yer.tanitim_metni || yer.aciklama || null;

  return (
    <main>
      <SayfaHero
        etiket={[kategoriEtiketi(yer.ana_kategori), yer.ilce].filter(Boolean).join(" · ")}
        baslik={yer.isim}
        ozet={`${altKategoriEtiketi(yer.alt_kategori)} — temel yer bilgileri ve tanıtım.`}
      />

      <div className="kabuk grid gap-12 py-12 md:grid-cols-[1.4fr_1fr]">
        <div className="space-y-12">
          <Plaka
            kaynak={yer.kapak_fotografi_url ?? yer.fotograf_urlleri[0]}
            alt=""
            oran="genis"
            kategori={yer.ana_kategori}
          />
          <section>
            <h2 className="yazi-alt text-bordo">Tanıtım</h2>
            {tanitim ? (
              <p className="yazi-govde text-ink/85 mt-4">{tanitim}</p>
            ) : (
              <p className="text-ink/55 mt-4">Bu yer için henüz yeterli izlenim yok.</p>
            )}
          </section>
        </div>

        <aside className="yazi-indeks space-y-6">
          {yer.ticari_bildirim === "sponsorlu" ? (
            <Rozet tur="sponsorlu">Sponsorlu</Rozet>
          ) : null}
          <Rozet tur="kategori">{kategoriEtiketi(yer.ana_kategori)}</Rozet>
          {yer.adres && (
            <div>
              <p className="text-ink/45">Adres</p>
              <p className="text-ink mt-1">{yer.adres}</p>
            </div>
          )}
          {yer.telefon && (
            <div>
              <p className="text-ink/45">Telefon</p>
              <p className="text-ink mt-1">{yer.telefon}</p>
            </div>
          )}
          {yer.web_sitesi && !yer.web_sitesi.includes("google.com/search") && (
            <a
              href={yer.web_sitesi}
              target="_blank"
              rel="noreferrer"
              className="text-bordo decoration-deniz cursor-pointer underline decoration-1 underline-offset-4 hover:decoration-2"
            >
              Web sitesi
            </a>
          )}
          <a
            href={googleMapsUrl(yer.enlem, yer.boylam, yer.isim)}
            target="_blank"
            rel="noreferrer"
            className="text-bordo decoration-deniz block cursor-pointer underline decoration-1 underline-offset-4 hover:decoration-2"
          >
            Haritada aç
          </a>
          <Dugme href="/sehir/samsun/rota" varyant="birincil">
            Bugünün rotasını kur
          </Dugme>
          <Link
            href="/sehir/samsun"
            className="text-bordo decoration-deniz block cursor-pointer text-sm underline decoration-1 underline-offset-4 hover:decoration-2"
          >
            Keşfe dön
          </Link>
        </aside>
      </div>
    </main>
  );
}
