import { Suspense } from "react";
import ScrollHero from "@/components/hero/ScrollHero";
import { HaritaBolum } from "@/components/harita/HaritaBolum";
import { BolumBasligi } from "@/components/ui/BolumBasligi";
import { BosDurum } from "@/components/ui/BosDurum";
import { KesilenAyrac } from "@/components/ui/KesilenAyrac";
import { Dugme } from "@/components/ui/Dugme";
import { IlceIndeksi } from "@/components/ui/IlceIndeksi";
import { IstatistikBandi } from "@/components/ui/IstatistikBandi";
import { Plaka } from "@/components/ui/Plaka";
import { SehirKarti } from "@/components/ui/SehirKarti";
import { Reveal, RevealListe, RevealOge } from "@/components/hareket/Reveal";
import { Manyetik } from "@/components/hareket/Manyetik";
import { LogoKaro } from "@/components/marka/LogoKaro";
import { CTA_BIRINCIL, GUVEN_CUMLESI, TANIM_CUMLESI } from "@/lib/marka";
import { haritaIsaretleriniKur, haritaMerkeziniBul } from "@/lib/harita";
import {
  apiDurumu,
  bolgeleriGetir,
  istatistikleriGetir,
  sehirleriGetir,
} from "@/lib/api";
import { DENEYIM_EKSENLERI } from "@/lib/sabitler";
import type { BolgeProfili } from "@/lib/types";
import { BugunNeYapalimAlani } from "@/components/bugun/BugunNeYapalimAlani";
import { aramaFiltreleriniGetir } from "@/lib/api";

/** yon.md 4.2 (3) — "ne yapar?" uc karti; plakalar atmosfer, yer fotografi degil. */
const YOLLAR = [
  {
    anahtar: "kesif",
    baslik: "Nereye gidilir?",
    metin:
      "Gezilecek yerler, yeme-içme ve konaklama tek listede; deneyim eksenlerine göre sıralı.",
    href: (s: string) => `/sehir/${s}`,
    cta: "Keşfe başla",
  },
  {
    anahtar: "bolge",
    baslik: "Hangi bölge sana göre?",
    metin: "İlçelerin temel tanıtımlarını oku; şehri bölge bölge keşfet.",
    href: (s: string) => `/sehir/${s}/bolgeler`,
    cta: "Bölgeyi tanı",
  },
  {
    anahtar: "rota",
    baslik: "Bugün Ne Yapalım?",
    metin: "Bugünkü niyetini yaz; doğrulanmış bilgiden az sayıda hedefli seçenek bul.",
    href: () => "/#bugun-ne-yapalim",
    cta: "Bugün için bak",
  },
] as const;

/** Tanitimi olan ilk ilce; yoksa sehir geneli. Yorum hacmi siralama sinyali degildir. */
function teaserBolgesi(bolgeler: BolgeProfili[]): BolgeProfili | null {
  return (
    bolgeler.find((bolge) => bolge.ilce_mi && bolge.tanitim_metni) ??
    bolgeler.find((bolge) => bolge.tanitim_metni) ??
    null
  );
}

export default function AnaSayfa() {
  return (
    <main>
      <ScrollHero />
      <Suspense fallback={<AnaSayfaIskel />}>
        <AnaSayfaGovde />
      </Suspense>
    </main>
  );
}

function AnaSayfaIskel() {
  return (
    <section className="doku-koyu bg-murekkep text-kagit bolum" aria-hidden="true">
      <div className="kabuk min-h-48" />
    </section>
  );
}

async function AnaSayfaGovde() {
  // Sehir anahtari veriden gelir (sehir bagimsizligi); bagimli istekler
  // zincirlenir, bagimsiz olanlar ayni turda cozulur.
  let sehirler;
  let istatistik;
  let bolgeler: BolgeProfili[];
  try {
    sehirler = await sehirleriGetir();
    const anahtar = sehirler[0]?.anahtar ?? "samsun";
    [istatistik, bolgeler] = await Promise.all([
      istatistikleriGetir(anahtar),
      bolgeleriGetir(anahtar),
    ]);
  } catch (hata) {
    return (
      <section className="bg-kagit bolum">
        <div className="kabuk">
          <BosDurum tip={apiDurumu(hata)} />
        </div>
      </section>
    );
  }

  const sehir = sehirler[0];
  const sehirIsim = sehir?.isim ?? "Samsun";
  const sehirAnahtar = sehir?.anahtar ?? "samsun";
  const ilceler = bolgeler.filter((b) => b.ilce_mi).map((b) => b.bolge_adi);
  const teaser = teaserBolgesi(bolgeler);
  const isaretler = haritaIsaretleriniKur(sehirAnahtar, bolgeler);
  const haritaMerkez = haritaMerkeziniBul(sehir, bolgeler, isaretler);
  const filtreKatalogu = await aramaFiltreleriniGetir(sehirAnahtar).catch(() => null);

  return (
    <>
      <BugunNeYapalimAlani
        sehir={sehirIsim}
        sehirAnahtari={sehirAnahtar}
        filtreKatalogu={filtreKatalogu}
      />
      <HaritaBolum
        sehirAnahtari={sehirAnahtar}
        sehirIsim={sehirIsim}
        isaretler={isaretler}
        merkez={haritaMerkez}
      />
      {/* 2 — Kanit. V2: tek ton kagit monotonlugunu kiran koyu murekkep bandi. */}
      <section className="doku-koyu bg-murekkep text-kagit bolum">
        <div className="kabuk">
          <Reveal className="xl:grid xl:grid-cols-12 xl:gap-6">
            <div className="mb-3 flex items-center gap-2 xl:col-span-1 xl:mb-0 xl:flex-col xl:items-start xl:gap-3 xl:pt-2">
              <LogoKaro boyut={16} dekoratif className="size-4" />
              <p className="etiket text-kagit/45">Kanıt</p>
            </div>
            <p className="yazi-govde text-kagit/85 max-w-[42rem] xl:col-span-10">
              {TANIM_CUMLESI} İlk çıkış şehri {sehirIsim}; kapsam tüm Türkiye.
            </p>
          </Reveal>
          {istatistik && istatistik.yer_sayisi > 0 ? (
            <Reveal delay={0.08}>
              <IstatistikBandi
                koyu
                className="mt-10"
                ogeler={[
                  {
                    deger: istatistik.yer_sayisi,
                    etiket: "İşaretli yer",
                    baglam: `${sehirIsim} genelinde`,
                  },
                  {
                    deger: istatistik.ilce_sayisi,
                    etiket: "İlçe",
                    baglam: "Yer verisi olan ilçeler",
                  },
                  {
                    deger: istatistik.bolge_profili_sayisi,
                    etiket: "Bölge profili",
                    baglam: "Tanıtımı hazırlanan bölgeler",
                  },
                ]}
              />
            </Reveal>
          ) : null}
          <Reveal delay={0.16}>
            <p className="text-kagit/60 mt-8 max-w-[38rem] text-sm">{GUVEN_CUMLESI}</p>
          </Reveal>
        </div>
      </section>

      {/* 3 — "Ne yapar?" uc kart, 60 ms kademe, bolum sonu mini CTA. */}
      <section className="bg-kagit bolum">
        <div className="kabuk">
          <KesilenAyrac className="mb-16" />
          <Reveal>
            <BolumBasligi
              etiket="Ne yapar?"
              baslik="Şehri üç yoldan oku"
              ozet="Keşif listesi, ilçe tanıtımları ve tek günlük Akıllı Rota aynı şehir bağlamında çalışır."
            />
          </Reveal>
          <RevealListe className="mt-12 grid gap-5 md:grid-cols-3">
            {YOLLAR.map((y) => (
              <RevealOge key={y.anahtar} className="h-full">
                <article className="kart-kabuk flex h-full flex-col">
                  <Plaka
                    kaynak={`/plaka/${y.anahtar}.webp`}
                    avifKaynak={`/plaka/${y.anahtar}.avif`}
                    oran="kart"
                    kenarli={false}
                    className="plaka-murekkep"
                  />
                  <div className="flex flex-1 flex-col p-6">
                    <h3 className="yazi-alt text-ink">{y.baslik}</h3>
                    <p className="yazi-govde text-ink/70 mt-3 flex-1">{y.metin}</p>
                    <div className="relative z-10 mt-6">
                      <Dugme href={y.href(sehirAnahtar)} varyant="bolum">
                        {y.cta}
                      </Dugme>
                    </div>
                  </div>
                  <span className="su-hatti" />
                </article>
              </RevealOge>
            ))}
          </RevealListe>
        </div>
      </section>

      {/* 4 — Sehir vitrini: koyu murekkep bandi, kart tuz adasi. */}
      <section className="doku-koyu bg-murekkep text-kagit bolum">
        <div className="kabuk">
          <Reveal>
            <BolumBasligi
              koyu
              etiket="Nereye gidilir?"
              baslik="Açık şehir"
              ozet="Yeni şehir eklemek tasarımı değiştirmez: veri gelir, işaretlenir, aynı kutulara oturur."
              aksiyon={{ href: `/sehir/${sehirAnahtar}`, etiket: "Keşfe başla" }}
            />
          </Reveal>
          <Reveal delay={0.1} className="mt-12 xl:grid xl:grid-cols-12 xl:gap-6">
            <p className="kenar-notu etiket text-kagit/45 mb-3 xl:col-span-1 xl:mb-0 xl:justify-self-end">
              1 / 81 şehir
            </p>
            <div className="min-w-0 xl:col-span-11">
              <SehirKarti
                varyant="vitrin"
                isim={sehirIsim}
                anahtar={sehirAnahtar}
                yerSayisi={istatistik?.yer_sayisi}
                ilceSayisi={istatistik?.ilce_sayisi}
                ozet={`${sehirIsim} ilk çıkış noktamız. Gezilecek yerler işaretli, ilçeler tanıtılıyor, rota tek gün için kuruluyor.`}
                plakaYerine={<IlceIndeksi ilceler={ilceler} />}
              />
              <div className="mt-6">
                <Dugme
                  href={`/sehir/${sehirAnahtar}/bolgeler`}
                  varyant="bolum"
                  className="text-kagit hover:bg-bordo-700"
                >
                  Bölgeyi tanı
                </Dugme>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* 5 — Kamusal bolge tanitimi; ic yorum/duygu turevleri tarayiciya gitmez. */}
      <section className="bg-kagit bolum">
        <div className="kabuk">
          <KesilenAyrac className="mb-16" />
          <Reveal>
            <BolumBasligi
              etiket="Bölgeyi tanı"
              baslik="Şehri ilçeleriyle oku"
              ozet="Kamusal yüzey yalnız temel tanıtım bilgisini gösterir."
            />
          </Reveal>
          <div className="mt-12 grid gap-6 lg:grid-cols-12">
            <Reveal className="lg:col-span-7">
              {teaser?.tanitim_metni ? (
                <blockquote className="bg-bordo-900 text-kagit rounded-[12px] px-6 py-6">
                  <p className="etiket text-kagit/55">{teaser.bolge_adi}</p>
                  <p className="yazi-govde text-kagit/85 mt-4">{teaser.tanitim_metni}</p>
                </blockquote>
              ) : (
                <blockquote className="bg-bordo-900 text-kagit rounded-[12px] px-6 py-6">
                  <p className="etiket text-kagit/55">Bölge tanıtımı</p>
                  <p className="yazi-govde text-kagit/85 mt-4">
                    Bölge tanıtımları hazırlanıyor. Yayınlandıkça burada ilçe ilçe temel
                    bilgi yer alacak.
                  </p>
                </blockquote>
              )}
            </Reveal>
            <Reveal delay={0.1} className="lg:col-span-5">
              <div className="h-full">
                <p className="etiket text-ink/45">Deneyim eksenleri</p>
                <ul className="mt-4">
                  {DENEYIM_EKSENLERI.map((e) => (
                    <li
                      key={e.deger}
                      className="border-bordo/12 text-ink/80 flex items-baseline justify-between gap-4 border-b py-3 text-sm"
                    >
                      <span>{e.etiket}</span>
                      <span className="text-ink/40 text-[11px] tracking-[0.24em] uppercase">
                        İlgi alanı
                      </span>
                    </li>
                  ))}
                </ul>
                <div className="mt-6">
                  <Dugme href={`/sehir/${sehirAnahtar}/bolgeler`} varyant="bolum">
                    Bölge profillerine bak
                  </Dugme>
                </div>
              </div>
            </Reveal>
          </div>
        </div>
      </section>

      {/* 6 — Doruk CTA: kanit ile ayni murekkep token; bordo logo akrabaligi. */}
      <section className="doku-koyu bg-murekkep text-kagit bolum-doruk border-bordo relative overflow-hidden border-t-2">
        <div className="kabuk relative text-center">
          <Reveal>
            <LogoKaro boyut={40} dekoratif className="mx-auto size-10" />
            <p className="etiket text-kagit/50 mt-5">Son işaret</p>
            <h2 className="yazi-bolum mt-4">Rotanı kur, şehri oku.</h2>
            <p className="yazi-govde text-kagit/75 mx-auto mt-4 max-w-lg">
              Bugün ne aradığını seç; tek günlük planını oluştur.
            </p>
            <div className="mt-8 flex justify-center">
              <Manyetik>
                <Dugme href={`/sehir/${sehirAnahtar}/rota`} varyant="birincil">
                  {CTA_BIRINCIL}
                </Dugme>
              </Manyetik>
            </div>
          </Reveal>
        </div>
      </section>
    </>
  );
}
