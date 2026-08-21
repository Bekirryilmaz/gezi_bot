import Link from "next/link";
import { SiteHeader } from "@/components/SiteHeader";
import { yerDetayiGetir } from "@/lib/api";
import { altKategoriEtiketi, kategoriEtiketi } from "@/lib/sabitler";

type Props = {
  params: Promise<{ id: string }>;
};

export async function generateMetadata({ params }: Props) {
  const { id } = await params;
  try {
    const yer = await yerDetayiGetir(id);
    return { title: yer.isim };
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
  } catch {
    return (
      <main className="atmosfer min-h-screen px-5 py-24">
        <p>Yer bulunamadı veya API’ye ulaşılamadı.</p>
        <Link href="/sehir/samsun" className="mt-4 inline-block text-yosun">
          ← Keşfe dön
        </Link>
      </main>
    );
  }

  const profil = yer.yer_profili as {
    fiyat_algisi?: { deger?: string };
    ulasim_kolayligi?: { deger?: string };
  };

  const tanitim =
    yer.tanitim_metni ||
    yer.aciklama ||
    null;

  return (
    <main className="atmosfer min-h-screen">
      <div className="relative bg-deniz-derin pb-14 pt-24 text-white">
        <SiteHeader />
        <div className="mx-auto max-w-6xl px-5 md:px-8">
          <Link href="/sehir/samsun" className="text-sm text-white/60 hover:text-white">
            ← Samsun keşif
          </Link>
          <h1 className="mt-4 font-display text-4xl leading-tight md:text-6xl">
            {yer.isim}
          </h1>
          <p className="mt-3 text-white/75">
            {kategoriEtiketi(yer.ana_kategori)} · {altKategoriEtiketi(yer.alt_kategori)}
            {yer.ilce ? ` · ${yer.ilce}` : ""}
          </p>
        </div>
      </div>

      <div className="mx-auto grid max-w-6xl gap-12 px-5 py-12 md:grid-cols-[1.4fr_1fr] md:px-8">
        <div className="space-y-12">
          <section>
            <h2 className="font-display text-2xl text-deniz md:text-3xl">Tanıtım</h2>
            {tanitim ? (
              <p className="mt-4 text-lg leading-relaxed text-ink/85">{tanitim}</p>
            ) : (
              <p className="mt-4 text-ink/55">
                Bu yer için henüz derlenmiş bir tanıtım metni yok.
              </p>
            )}
          </section>

          <section>
            <h2 className="font-display text-2xl text-deniz md:text-3xl">
              Kullanıcı deneyimleri
            </h2>
            {yer.duygu_ozeti ? (
              <p className="mt-4 text-lg leading-relaxed text-ink/85">{yer.duygu_ozeti}</p>
            ) : (
              <p className="mt-4 text-ink/55">
                Bu yer için henüz kullanıcı deneyimi özeti oluşturulmadı.
              </p>
            )}
          </section>
        </div>

        <aside className="space-y-6 text-sm">
          {yer.kaynakta_puan_ortalamasi != null && (
            <div>
              <p className="text-ink/45">Puan</p>
              <p className="font-display text-3xl text-yosun">
                {yer.kaynakta_puan_ortalamasi.toFixed(1)}
              </p>
            </div>
          )}
          {profil.fiyat_algisi?.deger &&
            profil.fiyat_algisi.deger !== "bilgi_yetersiz" && (
              <div>
                <p className="text-ink/45">Fiyat algısı</p>
                <p className="mt-1 capitalize text-ink">{profil.fiyat_algisi.deger}</p>
              </div>
            )}
          {profil.ulasim_kolayligi?.deger &&
            profil.ulasim_kolayligi.deger !== "bilgi_yetersiz" && (
              <div>
                <p className="text-ink/45">Ulaşım</p>
                <p className="mt-1 capitalize text-ink">
                  {profil.ulasim_kolayligi.deger}
                </p>
              </div>
            )}
          {yer.adres && (
            <div>
              <p className="text-ink/45">Adres</p>
              <p className="mt-1 text-ink">{yer.adres}</p>
            </div>
          )}
          {yer.telefon && (
            <div>
              <p className="text-ink/45">Telefon</p>
              <p className="mt-1 text-ink">{yer.telefon}</p>
            </div>
          )}
          {yer.web_sitesi && !yer.web_sitesi.includes("google.com/search") && (
            <a
              href={yer.web_sitesi}
              target="_blank"
              rel="noreferrer"
              className="inline-block text-yosun hover:underline"
            >
              Web sitesi →
            </a>
          )}
          <a
            href={googleMapsUrl(yer.enlem, yer.boylam, yer.isim)}
            target="_blank"
            rel="noreferrer"
            className="block text-yosun hover:underline"
          >
            Haritada aç →
          </a>
          <Link
            href={`/sehir/samsun/rota?konaklama_yer_id=${yer.id}`}
            className="block rounded-full bg-gunes px-4 py-2 text-center font-semibold text-deniz-derin"
          >
            Burayı konaklama üssü yap
          </Link>
        </aside>
      </div>
    </main>
  );
}
