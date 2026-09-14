"use client";

import Link from "next/link";
import { useState } from "react";
import { Dugme } from "@/components/ui/Dugme";
import { BosDurum } from "@/components/ui/BosDurum";
import { Spinner } from "@/components/ui/Spinner";
import { apiDurumu, gunlukPlanOlustur, veriDurumuBelirle } from "@/lib/api";
import { HATA_PUSULA } from "@/lib/marka";
import { DENEYIM_EKSENLERI, altKategoriEtiketi } from "@/lib/sabitler";
import type { GunlukPlanCevap } from "@/lib/types";

type Props = {
  sehirAnahtari: string;
  sehirIsim: string;
};

function GunlukPlan({ plan }: { plan: GunlukPlanCevap }) {
  return (
    <div className="space-y-8">
      {plan.rota_tavsiyesi ? (
        <p className="border-bordo/12 text-ink/80 bg-tuz rounded-[12px] border p-5 text-sm leading-relaxed">
          {plan.rota_tavsiyesi}
        </p>
      ) : null}
      <section>
        <h3 className="font-display text-bordo text-2xl">Bugünün planı</h3>
        <p className="text-ink/50 mt-1 text-sm">
          {(plan.toplam_mesafe_metre / 1000).toFixed(1)} km · yaklaşık{" "}
          {plan.toplam_sure_dakikasi} dk
        </p>
        <ol className="mt-4 space-y-3">
          {plan.duraklar.map((durak) => (
            <li key={`${durak.yer.id}-${durak.sira}`}>
              <Link
                href={`/yer/${durak.yer.id}`}
                className="group border-bordo/12 focus-visible:ring-samandira flex cursor-pointer gap-3 border-b pb-3 focus-visible:ring-2 focus-visible:outline-none"
              >
                <span className="font-display text-yosun text-xl">{durak.sira}</span>
                <span>
                  <span className="text-ink group-hover:text-bordo block font-medium">
                    {durak.yer.isim}
                  </span>
                  <span className="text-ink/50 text-sm">
                    {altKategoriEtiketi(durak.yer.alt_kategori)} · yaklaşık{" "}
                    {durak.tahmini_ziyaret_suresi_dk} dk
                  </span>
                </span>
              </Link>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}

export function GunlukRotaSihirbazi({ sehirAnahtari, sehirIsim }: Props) {
  const [eksenler, setEksenler] = useState<Record<string, number>>({
    tarihi_kulturel_puani: 0.7,
    gastronomi_puani: 0.6,
    doga_macera_puani: 0.5,
  });
  const [ucuz, setUcuz] = useState(false);
  const [sakin, setSakin] = useState(false);
  const [plan, setPlan] = useState<GunlukPlanCevap | null>(null);
  const [hata, setHata] = useState<unknown>(null);
  const [bekliyor, setBekliyor] = useState(false);

  function eksenDegistir(eksen: string, deger: number) {
    setEksenler((onceki) => ({ ...onceki, [eksen]: deger }));
  }

  async function planOlustur() {
    setHata(null);
    setBekliyor(true);
    try {
      const sonuc = await gunlukPlanOlustur({
        sehir_anahtari: sehirAnahtari,
        tercihler: {
          ilgi_agirliklari: eksenler,
          ucuz_tercih_et: ucuz,
          sakin_tercih_et: sakin,
        },
      });
      setPlan(sonuc);
    } catch (yakalanan) {
      setHata(yakalanan);
    } finally {
      setBekliyor(false);
    }
  }

  const durum = veriDurumuBelirle({
    yukleniyor: bekliyor && !plan,
    hata,
    ogeSayisi: plan?.duraklar.length,
  });

  return (
    <div className="grid gap-12 lg:grid-cols-[1fr_1.2fr]">
      <form
        className="space-y-8"
        onSubmit={(olay) => {
          olay.preventDefault();
          void planOlustur();
        }}
      >
        <div className="border-bordo/12 bg-tuz rounded-[12px] border p-5">
          <p className="etiket text-ink/45">Tek günlük Akıllı Rota</p>
          <p className="text-ink/75 mt-2 text-sm">
            {sehirIsim} için bugünün ilgi alanlarını seç. Bu akış konaklama veya çok
            günlük gezi planı üretmez.
          </p>
        </div>

        <div>
          <p className="text-ink/50 text-sm">İlgi alanların</p>
          <div className="mt-3 space-y-4">
            {DENEYIM_EKSENLERI.map((eksen) => (
              <label key={eksen.deger} className="block">
                <span className="flex justify-between text-sm">
                  <span>{eksen.etiket}</span>
                  <span className="text-ink/45 tabular-nums">
                    {Math.round((eksenler[eksen.deger] ?? 0) * 100)}%
                  </span>
                </span>
                <input
                  type="range"
                  min={0}
                  max={1}
                  step={0.1}
                  value={eksenler[eksen.deger] ?? 0}
                  onChange={(olay) =>
                    eksenDegistir(eksen.deger, Number(olay.target.value))
                  }
                  className="accent-yosun mt-1 w-full"
                />
              </label>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap gap-4 text-sm">
          <label className="flex min-h-11 cursor-pointer items-center gap-2">
            <input
              type="checkbox"
              checked={ucuz}
              onChange={(olay) => setUcuz(olay.target.checked)}
              className="accent-yosun"
            />
            Bütçe dostu tercih et
          </label>
          <label className="flex min-h-11 cursor-pointer items-center gap-2">
            <input
              type="checkbox"
              checked={sakin}
              onChange={(olay) => setSakin(olay.target.checked)}
              className="accent-yosun"
            />
            Kalabalıktan uzak dur
          </label>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <Dugme
            varyant="birincil"
            type="submit"
            disabled={bekliyor}
            yukleniyor={bekliyor}
          >
            {bekliyor ? "Hazırlanıyor…" : "Bugünün rotasını oluştur"}
          </Dugme>
          {bekliyor ? <Spinner className="text-bordo" /> : null}
        </div>
        {hata ? (
          <p className="text-samandira-koyu text-sm" role="alert">
            {hata instanceof Error ? hata.message : HATA_PUSULA}
          </p>
        ) : null}
      </form>

      <div aria-live="polite">
        {durum === "loading" ? (
          <BosDurum tip="loading" />
        ) : hata ? (
          <BosDurum tip={apiDurumu(hata)} ctalar={[]} />
        ) : plan ? (
          plan.duraklar.length === 0 ? (
            <BosDurum tip="empty" baslik="Bugün için durak bulunamadı" />
          ) : null
        ) : (
          <BosDurum
            tip="empty"
            baslik="Plan henüz yok"
            metin="Tercihlerini seçtiğinde tek günlük plan burada görünecek."
            ctalar={[]}
          />
        )}
        {plan && plan.duraklar.length > 0 ? (
          <div className={hata ? "mt-6 opacity-80" : undefined}>
            <GunlukPlan plan={plan} />
          </div>
        ) : null}
      </div>
    </div>
  );
}
