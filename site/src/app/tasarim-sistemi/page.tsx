import type { Metadata } from "next";
import { BolgeKarti } from "@/components/ui/BolgeKarti";
import { BolumBasligi } from "@/components/ui/BolumBasligi";
import { BosDurum } from "@/components/ui/BosDurum";
import { Dugme } from "@/components/ui/Dugme";
import { DuyguOzeti } from "@/components/ui/DuyguOzeti";
import { FiltreCip } from "@/components/ui/FiltreCip";
import { FiltreSatiri } from "@/components/ui/FiltreSatiri";
import { ListeIskel, MetinIskel, PlakaIskel, YerKartiIskel } from "@/components/ui/Iskel";
import { IstatistikBandi } from "@/components/ui/IstatistikBandi";
import { KesilenAyrac } from "@/components/ui/KesilenAyrac";
import { Markir } from "@/components/ui/Markir";
import { Plaka } from "@/components/ui/Plaka";
import { RehberKarti } from "@/components/ui/RehberKarti";
import { RotaKarti } from "@/components/ui/RotaKarti";
import { Rozet } from "@/components/ui/Rozet";
import { SehirKarti } from "@/components/ui/SehirKarti";
import { SkorKirilim } from "@/components/ui/SkorKirilim";
import { YataySerit, YataySeritOge } from "@/components/ui/YataySerit";
import { YerKarti } from "@/components/ui/YerKarti";
import { KelimeKilidi } from "@/components/marka/KelimeKilidi";
import { LogoKaro } from "@/components/marka/LogoKaro";
import { Reveal } from "@/components/hareket/Reveal";
import type { YerOzet } from "@/lib/types";

export const metadata: Metadata = {
  title: "Tasarım sistemi",
  description: "Şamandıra bileşen kütüphanesi — mürekkep ve tuz sözleşmesi.",
  robots: { index: false, follow: false },
};

const ORNEK_YER: YerOzet = {
  id: "ornek",
  isim: "Örnek iskele ve uzun bir yer adı iki satıra sığsın",
  ana_kategori: "gezilecek_yer",
  alt_kategori: "doga_manzara",
  ilce: "Sahil",
  enlem: 41.3,
  boylam: 36.3,
  kapak_fotografi_url: null,
  ticari_bildirim: null,
};

const ORNEK_FOTOLU: YerOzet = {
  ...ORNEK_YER,
  id: "ornek-foto",
  isim: "Vitrin plakası (örnek medya, yer fotoğrafı değil)",
  kapak_fotografi_url: "/og-default.png",
};

const RENKLER = [
  ["bordo-950", "#2E0405"],
  ["bordo-900", "#4A0708"],
  ["bordo", "#6C0000"],
  ["bordo-700", "#8E1710"],
  ["samandira", "#D6402C"],
  ["samandira-koyu", "#A92E1E"],
  ["tuz", "#FBF8F3"],
  ["kagit", "#F4EFE7"],
  ["kagit-koyu", "#EBE3D6"],
  ["ink", "#142126"],
  ["deniz", "#0A4D5C"],
  ["signal", "#F2B138"],
] as const;

const KONTRAST = [
  ["#FFFFFF / bordo", "12,8:1", "AAA — koyu yüzeyde her boy"],
  ["ink / kagit", "12,5:1", "gövde metni"],
  ["bordo / kagit", "11,2:1", "başlık mürekkebi"],
  ["#FFFFFF / samandira", "4,53:1", "buton ≥16 px ve ≥600"],
  ["samandira / kagit", "3,96:1", "metin yasak; ikon/kenarlık"],
  ["#FFFFFF / bordo-700", "9,2:1", "koyu zeminde ikincil"],
] as const;

function VitrinBaslik({ children }: { children: string }) {
  return <h2 className="yazi-alt text-bordo">{children}</h2>;
}

export default function TasarimSistemiSayfasi() {
  return (
    <main className="bg-kagit pt-28 pb-24">
      <div className="kabuk space-y-24">
        <Reveal>
          <BolumBasligi
            etiket="Kütüphane"
            baslik="Tasarım sistemi"
            ozet="yon.md P2+P3: tokenlar, plaka, kart ailesi, boş durumlar ve iskeletler. Sayfa noindex."
          />
        </Reveal>

        <section>
          <VitrinBaslik>Palet</VitrinBaslik>
          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4 md:grid-cols-6">
            {RENKLER.map(([ad, hex]) => (
              <div
                key={ad}
                className="border-bordo/12 overflow-hidden rounded-[12px] border"
              >
                <div className="h-16" style={{ background: hex }} />
                <p className="text-ink/60 px-2 py-2 text-[11px]">
                  {ad}
                  <span className="mt-0.5 block font-mono text-[10px] tabular-nums">
                    {hex}
                  </span>
                </p>
              </div>
            ))}
          </div>
          <ul className="mt-8 space-y-2 text-sm">
            {KONTRAST.map(([cift, oran, karar]) => (
              <li key={cift} className="flex flex-wrap gap-x-3 gap-y-1">
                <span className="text-ink/80 min-w-48 font-medium">{cift}</span>
                <span className="tabular-nums">{oran}</span>
                <span className="text-ink/55">{karar}</span>
              </li>
            ))}
          </ul>
        </section>

        <section>
          <VitrinBaslik>Tipografi</VitrinBaslik>
          <div className="mt-6 space-y-4">
            <p className="yazi-kapak text-bordo">Kapak 44→100</p>
            <p className="yazi-bolum text-bordo">Bölüm 30→54</p>
            <p className="yazi-alt text-bordo">Alt bölüm 22→30</p>
            <p className="yazi-kart text-bordo">Kart başlığı Sora 600</p>
            <p className="yazi-govde max-w-[42rem]">
              Gövde 16→17 / 1,62 — ölçü 62–68 karakter. Tırnak “ ” ve üç nokta ….
            </p>
            <p className="etiket text-ink/55">Etiket katı · 11px · 0,24em</p>
            <p className="yazi-sayi text-bordo">1.719</p>
          </div>
        </section>

        <section>
          <VitrinBaslik>Karo kilidi</VitrinBaslik>
          <div className="mt-8 flex flex-wrap items-end gap-8">
            {([16, 24, 28, 32, 40] as const).map((b) => (
              <div key={b} className="text-center">
                <LogoKaro boyut={b} />
                <p className="text-ink/45 mt-2 text-[11px] tabular-nums">{b}px</p>
              </div>
            ))}
            <KelimeKilidi boyut={32} yaziSinif="text-[28px] text-ink" />
          </div>
        </section>

        <section>
          <VitrinBaslik>Plaka</VitrinBaslik>
          <p className="yazi-indeks text-ink/60 mt-2 max-w-xl">
            Aynı oran, fotoğraflı veya tipografik. Izgara adımı değişmez — CLS 0.
          </p>
          <div className="mt-8 grid gap-5 md:grid-cols-2">
            <div>
              <p className="etiket text-ink/55 mb-3">Fotoğrafsız</p>
              <Plaka
                oran="kart"
                kategori="gezilecek_yer"
                etiket={<span className="etiket">Sahil</span>}
              />
            </div>
            <div>
              <p className="etiket text-ink/55 mb-3">Örnek medya</p>
              <Plaka
                oran="kart"
                kaynak="/og-default.png"
                alt=""
                etiket={<span className="etiket">Vitrin</span>}
                rozet={<Rozet tur="skor">4.6</Rozet>}
              />
            </div>
          </div>
        </section>

        <section>
          <VitrinBaslik>Dugme</VitrinBaslik>
          <div className="mt-6 flex flex-wrap items-center gap-3">
            <Dugme href="/tasarim-sistemi" varyant="birincil">
              Rotanı kur
            </Dugme>
            <Dugme href="/tasarim-sistemi" varyant="ikincil">
              Keşfe başla
            </Dugme>
            <Dugme href="/tasarim-sistemi" varyant="hayalet">
              Bölgeyi tanı
            </Dugme>
            <Dugme href="/tasarim-sistemi" varyant="metin">
              Skor kırılımı
            </Dugme>
            <Dugme href="/tasarim-sistemi" varyant="bolum">
              Tümünü gör
            </Dugme>
            <Dugme varyant="birincil" yukleniyor disabled>
              Hazırlanıyor…
            </Dugme>
          </div>
        </section>

        <section>
          <VitrinBaslik>Rozet</VitrinBaslik>
          <div className="mt-6 flex flex-wrap gap-2">
            <Rozet tur="sponsorlu">Sponsorlu</Rozet>
            <Rozet tur="klasik">Şehrin Klasiği</Rozet>
            <Rozet tur="kategori">Müze</Rozet>
            <Rozet tur="skor">4.6</Rozet>
            <Rozet tur="durum">Hazırlanıyor</Rozet>
          </div>
        </section>

        <section>
          <VitrinBaslik>İstatistik ve veri</VitrinBaslik>
          <IstatistikBandi
            className="mt-6"
            ogeler={[
              { deger: 1719, etiket: "İşaretli yer" },
              { deger: 1, etiket: "Açık şehir", baglam: "Samsun'da başladık" },
              { deger: 6, etiket: "Deneyim ekseni" },
            ]}
          />
          <DuyguOzeti
            className="mt-10"
            etiket="Olumlu"
            metin="İskele sessiz, çay demli, ufuk açık — kısa molalık bir durak."
          />
          <div className="mt-8 max-w-sm">
            <SkorKirilim
              kirilim={{
                tarihi_kulturel_puani: 4.2,
                gastronomi_puani: 3.1,
                doga_macera_puani: 4.8,
              }}
            />
          </div>
        </section>

        <section>
          <VitrinBaslik>Filtre</VitrinBaslik>
          <FiltreSatiri className="mt-6">
            <FiltreCip href="/tasarim-sistemi" aktif sayi={12}>
              Tümü
            </FiltreCip>
            <FiltreCip href="/tasarim-sistemi" aktif={false} sayi={4}>
              Doğa
            </FiltreCip>
            <FiltreCip href="/tasarim-sistemi" aktif={false} sayi={0}>
              Gece
            </FiltreCip>
          </FiltreSatiri>
        </section>

        <section>
          <VitrinBaslik>Kart ailesi</VitrinBaslik>
          <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            <YerKarti yer={ORNEK_YER} />
            <YerKarti yer={ORNEK_FOTOLU} sponsorlu klasik />
            <YerKartiIskel />
          </div>
          <p className="yazi-indeks text-ink/55 mt-3">
            Üçüncü sütun iskelet — aynı oran ve kart yüksekliği.
          </p>
          <div className="mt-10">
            <SehirKarti
              varyant="vitrin"
              isim="Örnek şehir"
              anahtar="samsun"
              yerSayisi={1719}
              ilceSayisi={15}
              ozet="Tek şehirde vitrin: tam genişlik plaka, sayı satırı gerçek veriden."
            />
          </div>
          <div className="mt-8 grid gap-5 md:grid-cols-2">
            <SehirKarti
              varyant="izgara"
              isim="Izgara"
              anahtar="samsun"
              yerSayisi={80}
              ozet="2–3 şehirde ızgara varyantı."
            />
            <SehirKarti
              varyant="serit"
              isim="Şerit"
              anahtar="samsun"
              yerSayisi={12}
              ozet="4+ şehirde yatay şerit."
            />
          </div>
          <div className="mt-8 grid gap-5 md:grid-cols-3">
            <BolgeKarti
              ad="Atakum"
              ozet="Sahil bandı sakin, akşam yürüyüşü için uygun."
              yerSayisi={120}
              href="/sehir/samsun/bolgeler"
            />
            <RehberKarti
              href="/tasarim-sistemi"
              baslik="Nasıl rota kurulur"
              ozet="Tercihlerini söyle, kırılımı oku, gün gün planı al."
              okumaDk={6}
              tarih="2026-09-05"
            />
            <RotaKarti
              gunSayisi={3}
              duraklar={["İskele", "Müze", "Çarşı", "Sahil"]}
              eksen="Doğa & macera"
              href="/sehir/samsun/rota"
            />
          </div>
        </section>

        <section>
          <VitrinBaslik>Yatay şerit</VitrinBaslik>
          <YataySerit className="mt-6">
            {["Bir", "İki", "Üç", "Dört"].map((ad) => (
              <YataySeritOge key={ad}>
                <SehirKarti
                  varyant="serit"
                  isim={ad}
                  anahtar="samsun"
                  yerSayisi={10}
                  ozet="Kullanıcı kontrollü şerit; marquee yok."
                />
              </YataySeritOge>
            ))}
          </YataySerit>
        </section>

        <section>
          <VitrinBaslik>Boş durumlar</VitrinBaslik>
          <div className="mt-8 grid gap-5 md:grid-cols-2">
            <BosDurum
              tip="filtre"
              cta={{ href: "/tasarim-sistemi", etiket: "Filtreleri temizle" }}
            />
            <BosDurum tip="veri" />
            <BosDurum tip="hata" />
            <BosDurum tip="404" />
            <BosDurum tip="hazirlaniyor" />
          </div>
        </section>

        <section>
          <VitrinBaslik>İskeletler</VitrinBaslik>
          <div className="mt-8 grid gap-5 md:grid-cols-3">
            <YerKartiIskel />
            <div className="space-y-4">
              <PlakaIskel oran="kart" />
              <MetinIskel />
            </div>
            <ListeIskel />
          </div>
        </section>

        <section>
          <VitrinBaslik>Markır ve ayraç</VitrinBaslik>
          <div className="mt-6 flex items-center gap-6">
            <Markir className="text-samandira" boyut={24} />
            <Markir className="text-bordo" boyut={16} />
          </div>
          <KesilenAyrac className="mt-8" />
        </section>
      </div>
    </main>
  );
}
