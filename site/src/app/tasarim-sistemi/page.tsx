import type { Metadata } from "next";
import { BolumBasligi } from "@/components/ui/BolumBasligi";
import { BosDurum } from "@/components/ui/BosDurum";
import { Dugme } from "@/components/ui/Dugme";
import { DuyguOzeti } from "@/components/ui/DuyguOzeti";
import { FiltreCip } from "@/components/ui/FiltreCip";
import { IstatistikBandi } from "@/components/ui/IstatistikBandi";
import { RehberKarti } from "@/components/ui/RehberKarti";
import { Rozet } from "@/components/ui/Rozet";
import { SehirKarti } from "@/components/ui/SehirKarti";
import { SkorKirilim } from "@/components/ui/SkorKirilim";
import { YerKarti } from "@/components/ui/YerKarti";
import { KelimeKilidi } from "@/components/marka/KelimeKilidi";
import { LogoKaro } from "@/components/marka/LogoKaro";
import { Reveal, RevealListe, RevealOge } from "@/components/hareket/Reveal";
import type { YerOzet } from "@/lib/types";

export const metadata: Metadata = {
  title: "Tasarım sistemi",
  description: "Şamandıra bileşen kütüphanesi — üretim vitrini.",
  robots: { index: false, follow: false },
};

const ORNEK_YER: YerOzet = {
  id: "ornek",
  isim: "Örnek iskele",
  ana_kategori: "gezilecek_yer",
  alt_kategori: "doga_manzara",
  ilce: "Sahil",
  enlem: 41.3,
  boylam: 36.3,
  kaynakta_puan_ortalamasi: 4.6,
  duygu_skoru_ortalama: 0.82,
  kapak_fotografi_url: null,
};

const RENKLER = [
  ["bordo", "#6C0000"],
  ["samandira", "#D6402C"],
  ["kagit", "#F4EFE7"],
  ["tuz", "#FBF8F3"],
  ["ink", "#142126"],
  ["deniz", "#0A4D5C"],
  ["signal", "#F2B138"],
] as const;

export default function TasarimSistemiSayfasi() {
  return (
    <main className="bg-kagit px-5 pt-28 pb-24 md:px-8">
      <div className="mx-auto max-w-6xl space-y-24">
        <Reveal>
          <BolumBasligi
            etiket="Kütüphane"
            baslik="Tasarım sistemi"
            ozet="Tokenlar, karo kilidi ve üretim bileşenleri. Bu sayfa noindex; her yeni yüzey buradan türer."
          />
        </Reveal>

        <section>
          <h2 className="font-display text-deniz-derin text-3xl tracking-[-0.02em]">
            Renk
          </h2>
          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4 md:grid-cols-7">
            {RENKLER.map(([ad, hex]) => (
              <div key={ad} className="border-deniz/10 overflow-hidden rounded-xl border">
                <div className="h-16" style={{ background: hex }} />
                <p className="text-ink/60 px-2 py-2 text-[11px] tracking-wide">
                  {ad}
                  <span className="mt-0.5 block font-mono text-[10px]">{hex}</span>
                </p>
              </div>
            ))}
          </div>
        </section>

        <section>
          <h2 className="font-display text-deniz-derin text-3xl tracking-[-0.02em]">
            Karo
          </h2>
          <p className="text-ink/65 mt-2 max-w-xl text-sm">
            Kullanıcı illüstrasyonu birebir; işaret min 16px; kelime kilidi min 24px.
          </p>
          <div className="mt-8 flex flex-wrap items-end gap-8">
            {([16, 24, 32, 48] as const).map((b) => (
              <div key={b} className="text-center">
                <LogoKaro boyut={b} />
                <p className="text-ink/45 mt-2 text-[11px] tabular-nums">{b}px</p>
              </div>
            ))}
            <KelimeKilidi boyut={32} yaziSinif="text-[28px] text-ink" />
          </div>
        </section>

        <section>
          <h2 className="font-display text-deniz-derin text-3xl tracking-[-0.02em]">
            Dugme ve rozet
          </h2>
          <div className="mt-6 flex flex-wrap gap-3">
            <Dugme href="/tasarim-sistemi" varyant="birincil">
              Rotanı kur
            </Dugme>
            <Dugme href="/tasarim-sistemi" varyant="ikincil">
              Keşfe başla
            </Dugme>
            <Dugme href="/tasarim-sistemi" varyant="hayalet">
              İncele
            </Dugme>
          </div>
          <div className="mt-6 flex flex-wrap gap-2">
            <Rozet>Deniz</Rozet>
            <Rozet ton="samandira">Vurgu</Rozet>
            <Rozet ton="signal">Sponsorlu</Rozet>
            <Rozet ton="yosun">Olumlu</Rozet>
            <Rozet ton="sis">Nötr</Rozet>
          </div>
        </section>

        <section>
          <h2 className="font-display text-deniz-derin text-3xl tracking-[-0.02em]">
            Istatistik ve duygu
          </h2>
          <IstatistikBandi
            className="mt-6"
            ogeler={[
              { deger: "1.719", etiket: "İşaretli yer" },
              { deger: "1", etiket: "Açık şehir" },
              { deger: "6", etiket: "Deneyim ekseni" },
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
          <h2 className="font-display text-deniz-derin text-3xl tracking-[-0.02em]">
            Kart ailesi
          </h2>
          <div className="mt-4 flex flex-wrap gap-2">
            <FiltreCip href="/tasarim-sistemi" aktif sayi={12}>
              Tümü
            </FiltreCip>
            <FiltreCip href="/tasarim-sistemi" aktif={false}>
              Doğa
            </FiltreCip>
          </div>
          <RevealListe className="mt-8 grid gap-5 md:grid-cols-3">
            <RevealOge>
              <YerKarti yer={ORNEK_YER} />
            </RevealOge>
            <RevealOge>
              <SehirKarti
                isim="Örnek şehir"
                anahtar="samsun"
                yerSayisi={12}
                ozet="Veri gelince işaretlenir; tasarım şehir adına kilitli değil."
              />
            </RevealOge>
            <RevealOge>
              <RehberKarti
                href="/tasarim-sistemi"
                baslik="Nasıl rota kurulur"
                ozet="Tercihlerini söyle, kırılımı oku, gün gün planı al."
              />
            </RevealOge>
          </RevealListe>
          <BosDurum
            className="mt-10"
            cta={{ href: "/tasarim-sistemi", etiket: "Filtreleri sıfırla" }}
          />
        </section>

        <section>
          <h2 className="font-display text-deniz-derin text-3xl tracking-[-0.02em]">
            Hareket
          </h2>
          <p className="text-ink/65 mt-2 max-w-xl text-sm">
            Reveal kaydırmada bir kez. prefers-reduced-motion açıkken transform kapanır,
            içerik son halinde kalır.
          </p>
          <div className="mt-8 flex items-center gap-6">
            <div className="border-deniz/10 bg-kagit rounded-xl border px-6 py-8">
              Kart yüzeyi
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
