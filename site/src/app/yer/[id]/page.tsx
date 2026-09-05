import Link from "next/link";
import { SayfaHero } from "@/components/layout/SayfaHero";
import { BosDurum } from "@/components/ui/BosDurum";
import { Dugme } from "@/components/ui/Dugme";
import { DuyguOzeti } from "@/components/ui/DuyguOzeti";
import { Plaka } from "@/components/ui/Plaka";
import { Rozet } from "@/components/ui/Rozet";
import { SkorKirilim } from "@/components/ui/SkorKirilim";
import { yerDetayiGetir } from "@/lib/api";
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
        yer.duygu_ozeti?.slice(0, 155) ||
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
  } catch {
    return (
      <main className="bg-kagit px-5 pt-28 pb-16">
        <div className="kabuk">
          <BosDurum
            tip="hata"
            baslik="Yer bulunamadı"
            metin="Pusula şaştı — keşfe dönüp başka bir işaret seçebilirsin."
            cta={{ href: "/sehir/samsun", etiket: "Keşfe dön" }}
          />
        </div>
      </main>
    );
  }

  const profil = yer.yer_profili as {
    fiyat_algisi?: { deger?: string };
    ulasim_kolayligi?: { deger?: string };
  };

  const tanitim = yer.tanitim_metni || yer.aciklama || null;

  return (
    <main>
      <SayfaHero
        etiket={[kategoriEtiketi(yer.ana_kategori), yer.ilce].filter(Boolean).join(" · ")}
        baslik={yer.isim}
        ozet={`${altKategoriEtiketi(yer.alt_kategori)} — skorlar türetilmiş metrik; ham yorum metni yok.`}
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

          <section>
            <h2 className="yazi-alt text-bordo">Kullanıcı deneyimleri</h2>
            {yer.duygu_ozeti ? (
              <DuyguOzeti className="mt-4" metin={yer.duygu_ozeti} />
            ) : (
              <p className="text-ink/55 mt-4">
                Bu yer için henüz kullanıcı deneyimi özeti oluşturulmadı.
              </p>
            )}
          </section>

          {Object.keys(yer.deneyim_puanlari ?? {}).length > 0 ? (
            <section>
              <h2 className="yazi-alt text-bordo">Skor kırılımı</h2>
              <p className="text-ink/55 mt-2 text-sm">
                Her önerinin nedeni açık: eksenler ayrı puanlanır.
              </p>
              <div className="mt-5 max-w-md">
                <SkorKirilim kirilim={yer.deneyim_puanlari} />
              </div>
            </section>
          ) : null}
        </div>

        <aside className="yazi-indeks space-y-6">
          {yer.kaynakta_puan_ortalamasi != null && (
            <div>
              <p className="etiket text-ink/45">Puan</p>
              <p className="yazi-sayi text-bordo mt-1 text-4xl">
                {yer.kaynakta_puan_ortalamasi.toFixed(1)}
              </p>
            </div>
          )}
          <Rozet tur="kategori">{kategoriEtiketi(yer.ana_kategori)}</Rozet>
          {profil.fiyat_algisi?.deger &&
            profil.fiyat_algisi.deger !== "bilgi_yetersiz" && (
              <div>
                <p className="text-ink/45">Fiyat algısı</p>
                <p className="text-ink mt-1 capitalize">{profil.fiyat_algisi.deger}</p>
              </div>
            )}
          {profil.ulasim_kolayligi?.deger &&
            profil.ulasim_kolayligi.deger !== "bilgi_yetersiz" && (
              <div>
                <p className="text-ink/45">Ulaşım</p>
                <p className="text-ink mt-1 capitalize">
                  {profil.ulasim_kolayligi.deger}
                </p>
              </div>
            )}
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
          <Dugme
            href={`/sehir/samsun/rota?konaklama_yer_id=${yer.id}`}
            varyant="birincil"
          >
            Burayı konaklama üssü yap
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
