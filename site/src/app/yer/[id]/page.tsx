import Link from "next/link";

import { BaglamliKararOzeti } from "@/components/kesfet/BaglamliKararOzeti";
import { SayfaHero } from "@/components/layout/SayfaHero";
import { BosDurum } from "@/components/ui/BosDurum";
import { Plaka } from "@/components/ui/Plaka";
import { apiDurumu, kamusalYerDetayiGetir } from "@/lib/api";
import { altKategoriEtiketi, kategoriEtiketi } from "@/lib/sabitler";

type Props = {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ donus?: string }>;
};

function guvenliDonus(deger: string | undefined, varsayilan: string): string {
  if (!deger || !deger.startsWith("/sehir/") || deger.startsWith("//")) return varsayilan;
  return deger;
}

function degerMetni(deger: unknown): string {
  if (typeof deger === "string") return deger;
  if (typeof deger === "number" || typeof deger === "boolean") return String(deger);
  if (deger && typeof deger === "object" && "deger" in deger)
    return degerMetni((deger as { deger: unknown }).deger);
  return "Yayımlanmış bilgi mevcut; kapsamı aşağıda belirtilmiştir.";
}

export async function generateMetadata({ params }: Props) {
  const { id } = await params;
  try {
    const detay = await kamusalYerDetayiGetir(id);
    return {
      title: detay.yer.isim,
      description:
        detay.aciklama?.slice(0, 155) ??
        `${detay.yer.isim} için yayımlanmış pratik bilgiler ve karar sınırları.`,
    };
  } catch {
    return { title: "Yer" };
  }
}

function haritaUrl(enlem: number, boylam: number, isim: string): string {
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${isim} @${enlem},${boylam}`)}`;
}

export default async function YerDetaySayfasi({ params, searchParams }: Props) {
  const { id } = await params;
  const { donus } = await searchParams;
  let detay;
  try {
    detay = await kamusalYerDetayiGetir(id);
  } catch (hata) {
    return (
      <main className="bg-kagit px-5 pt-28 pb-16">
        <div className="kabuk">
          <BosDurum
            tip={apiDurumu(hata)}
            baslik={apiDurumu(hata) === "empty" ? "Yer bulunamadı" : undefined}
            cta={{ href: "/sehir/samsun", etiket: "Keşfet'e dön" }}
          />
        </div>
      </main>
    );
  }
  const varsayilanDonus = `/sehir/${detay.cografya.sehir_anahtari}`;
  const donusYolu = guvenliDonus(donus, varsayilanDonus);
  return (
    <main>
      <SayfaHero
        etiket={[
          kategoriEtiketi(detay.ana_kategori),
          detay.cografya.ilce_ismi,
          detay.cografya.sehir_ismi,
        ]
          .filter(Boolean)
          .join(" · ")}
        baslik={detay.yer.isim}
        ozet={`${altKategoriEtiketi(detay.alt_kategori)} — tam yer ve şube kimliğiyle yayımlanmış karar bilgileri.`}
      />
      <div className="kabuk grid gap-12 py-12 lg:grid-cols-[minmax(0,1.45fr)_22rem]">
        <div className="space-y-10">
          <Plaka
            kaynak={detay.fotograf_urlleri[0]}
            alt=""
            oran="genis"
            kategori={detay.ana_kategori}
          />
          <BaglamliKararOzeti yerId={id} ilkDetay={detay} />
          <section aria-labelledby="pratik-baslik">
            <h2 id="pratik-baslik" className="yazi-alt text-bordo">
              Gitmeden önce bilmen gerekenler
            </h2>
            {detay.pratik_bilgiler.length ? (
              <dl className="mt-5 grid gap-5 sm:grid-cols-2">
                {detay.pratik_bilgiler.map((bilgi, sira) => (
                  <div
                    key={`${bilgi.aile}-${sira}`}
                    className="border-deniz/15 rounded-2xl border p-4"
                  >
                    <dt className="font-semibold">{bilgi.aile.replaceAll("_", " ")}</dt>
                    <dd className="text-ink/75 mt-2">{degerMetni(bilgi.deger)}</dd>
                    <dd className="text-ink/50 mt-3 text-sm">{bilgi.guncellik_anlami}</dd>
                  </div>
                ))}
              </dl>
            ) : (
              <div className="border-bordo/15 mt-5 rounded-2xl border p-5">
                <p className="font-semibold">Bu koşulu henüz doğrulayamıyoruz</p>
                <p className="text-ink/65 mt-2">
                  Development verisinde yayımlanmış somut condition claim’i yok. Kimlik
                  bilgisini ziyaret koşulu gibi göstermiyoruz.
                </p>
              </div>
            )}
          </section>
          <section aria-labelledby="kapsam-baslik">
            <h2 id="kapsam-baslik" className="yazi-alt text-bordo">
              Bilginin kapsamı
            </h2>
            <p className="text-ink/65 mt-4">{detay.kapsam_anlami}</p>
            <h3 className="mt-6 font-semibold">{detay.duzeltme_girisi.etiket}</h3>
            <p className="text-ink/65 mt-2">{detay.duzeltme_girisi.aciklama}</p>
          </section>
        </div>
        <aside className="space-y-6 lg:sticky lg:top-24 lg:self-start">
          <section className="border-deniz/12 rounded-3xl border p-5">
            <h2 className="font-semibold">Tam olarak hangi yer?</h2>
            <dl className="mt-4 grid gap-4 text-sm">
              <div>
                <dt className="text-ink/45">Şube kimliği</dt>
                <dd className="mt-1 break-all">{detay.yer.branch_id}</dd>
              </div>
              <div>
                <dt className="text-ink/45">Yer türü</dt>
                <dd className="mt-1">{altKategoriEtiketi(detay.alt_kategori)}</dd>
              </div>
              <div>
                <dt className="text-ink/45">Konum</dt>
                <dd className="mt-1">
                  {[detay.cografya.ilce_ismi, detay.cografya.sehir_ismi]
                    .filter(Boolean)
                    .join(", ")}
                </dd>
              </div>
            </dl>
          </section>
          {detay.adres ? (
            <section>
              <h2 className="text-ink/45 text-sm">Adres</h2>
              <p className="mt-1">{detay.adres}</p>
            </section>
          ) : null}
          <a
            href={haritaUrl(detay.enlem, detay.boylam, detay.yer.isim)}
            target="_blank"
            rel="noreferrer"
            className="text-bordo block min-h-11 py-2 font-semibold underline underline-offset-4"
          >
            Haritada yol tarifini aç
          </a>
          {detay.web_sitesi && !detay.web_sitesi.includes("google.com/search") ? (
            <a
              href={detay.web_sitesi}
              target="_blank"
              rel="noreferrer"
              className="text-bordo block min-h-11 py-2 underline underline-offset-4"
            >
              Resmî web sitesini aç
            </a>
          ) : null}
          {detay.cografya.ilce_id ? (
            <Link
              href={`/sehir/${detay.cografya.sehir_anahtari}/ilce/${detay.cografya.ilce_id}`}
              className="text-bordo block min-h-11 py-2 underline underline-offset-4"
            >
              {detay.cografya.ilce_ismi} bağlamını aç
            </Link>
          ) : null}
          <Link
            href={donusYolu}
            className="text-bordo block min-h-11 py-2 underline underline-offset-4"
          >
            Keşfet bağlamına dön
          </Link>
        </aside>
      </div>
    </main>
  );
}
