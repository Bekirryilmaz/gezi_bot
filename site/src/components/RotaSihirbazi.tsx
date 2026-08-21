"use client";

import Link from "next/link";
import { useMemo, useState, useTransition } from "react";
import {
  konaklamaBolgesiOner,
  rotaAlternatifleriOlustur,
  rotaOlustur,
} from "@/lib/api";
import { DENEYIM_EKSENLERI, altKategoriEtiketi } from "@/lib/sabitler";
import type { BolgeProfili, RotaCevap } from "@/lib/types";

type Senaryo = "bolge_belli" | "bolge_degil";
type Adim = "senaryo" | "tercihler" | "alternatifler" | "sonuc";

type Props = {
  sehirAnahtari: string;
  sehirIsim: string;
  baslangicKonaklamaYerId?: string | null;
  baslangicKonaklamaBolge?: string | null;
  bolgeler: BolgeProfili[];
};

function RotaGunleri({ rota }: { rota: RotaCevap }) {
  return (
    <div className="space-y-10">
      {rota.rota_tavsiyesi && (
        <p className="rounded-2xl bg-white/70 p-5 text-sm leading-relaxed text-ink/80">
          {rota.rota_tavsiyesi}
        </p>
      )}
      {rota.konaklama_bolgesi_onerisi && (
        <div className="rounded-2xl bg-white/70 p-5">
          <p className="text-sm text-ink/50">Önerilen konaklama bölgesi</p>
          <p className="mt-1 font-display text-2xl text-deniz">
            {rota.konaklama_bolgesi_onerisi.bolge_adi}
          </p>
          {rota.konaklama_bolgesi_onerisi.gerekce && (
            <p className="mt-2 text-sm text-ink/70">
              {rota.konaklama_bolgesi_onerisi.gerekce}
            </p>
          )}
          {rota.konaklama_bolgesi_onerisi.ornek_konaklamalar?.length > 0 && (
            <ul className="mt-4 space-y-1 text-sm text-ink/60">
              <li className="text-ink/40">Bu bölgede örnek tesisler (zorunlu değil):</li>
              {rota.konaklama_bolgesi_onerisi.ornek_konaklamalar.slice(0, 3).map((k) => (
                <li key={k.id}>
                  <Link href={`/yer/${k.id}`} className="hover:text-deniz hover:underline">
                    {k.isim}
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
      {rota.gunler.map((gun) => (
        <section key={gun.gun_no}>
          <h3 className="font-display text-2xl text-deniz">{gun.gun_no}. gün</h3>
          <p className="mt-1 text-sm text-ink/50">
            {(gun.toplam_mesafe_metre / 1000).toFixed(1)} km · ~{gun.toplam_sure_dakikasi} dk
          </p>
          <ol className="mt-4 space-y-3">
            {gun.duraklar.map((durak) => (
              <li key={`${gun.gun_no}-${durak.sira}`}>
                <Link
                  href={`/yer/${durak.yer.id}`}
                  className="group flex gap-3 border-b border-[var(--cizgi)] pb-3"
                >
                  <span className="font-display text-xl text-yosun">{durak.sira}</span>
                  <span>
                    <span className="block font-medium text-ink group-hover:text-deniz">
                      {durak.yer.isim}
                    </span>
                    <span className="text-sm text-ink/50">
                      {altKategoriEtiketi(durak.yer.alt_kategori)} · ~
                      {durak.tahmini_ziyaret_suresi_dk} dk
                    </span>
                  </span>
                </Link>
              </li>
            ))}
          </ol>
        </section>
      ))}
    </div>
  );
}

export function RotaSihirbazi({
  sehirAnahtari,
  sehirIsim,
  baslangicKonaklamaYerId = null,
  baslangicKonaklamaBolge = null,
  bolgeler,
}: Props) {
  const baslangicSenaryo: Senaryo =
    baslangicKonaklamaYerId || baslangicKonaklamaBolge ? "bolge_belli" : "bolge_degil";
  const [adim, setAdim] = useState<Adim>(
    baslangicSenaryo === "bolge_belli" ? "tercihler" : "senaryo",
  );
  const [senaryo, setSenaryo] = useState<Senaryo>(baslangicSenaryo);
  const [bolgeAdi, setBolgeAdi] = useState(baslangicKonaklamaBolge ?? "");
  const [gunSayisi, setGunSayisi] = useState(2);
  const [eksikler, setEksenler] = useState<Record<string, number>>({
    tarihi_kulturel_puani: 0.7,
    gastronomi_puani: 0.6,
    doga_macera_puani: 0.5,
  });
  const [ucuz, setUcuz] = useState(false);
  const [sakin, setSakin] = useState(false);
  const [alternatifler, setAlternatifler] = useState<RotaCevap[]>([]);
  const [rota, setRota] = useState<RotaCevap | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [bekliyor, startTransition] = useTransition();

  const bolgeSecenekleri = useMemo(() => {
    const adlar = new Set<string>();
    for (const b of bolgeler) {
      if (b.bolge_adi) adlar.add(b.bolge_adi);
    }
    // Bilinen ilçeler (API boşsa bile)
    for (const adi of [
      "Atakum",
      "İlkadım",
      "Canik",
      "Tekkeköy",
      "Bafra",
      "Çarşamba",
    ]) {
      adlar.add(adi);
    }
    return Array.from(adlar).sort((a, b) => a.localeCompare(b, "tr"));
  }, [bolgeler]);

  function eksenDegistir(eksen: string, deger: number) {
    setEksenler((onceki) => ({ ...onceki, [eksen]: deger }));
  }

  function tercihGovdesi() {
    return {
      sehir_anahtari: sehirAnahtari,
      gun_sayisi: gunSayisi,
      tercihler: {
        ilgi_agirliklari: eksikler,
        ucuz_tercih_et: ucuz,
        sakin_tercih_et: sakin,
      },
    };
  }

  function senaryo1Olustur() {
    setHata(null);
    startTransition(async () => {
      try {
        const talep = {
          ...tercihGovdesi(),
          konaklama_yer_id: baslangicKonaklamaYerId || undefined,
          konaklama_bolge_adi:
            !baslangicKonaklamaYerId && bolgeAdi ? bolgeAdi : undefined,
        };
        if (!talep.konaklama_yer_id && !talep.konaklama_bolge_adi) {
          setHata("Konaklama bölgesi seç.");
          return;
        }
        const sonuc = await rotaOlustur(talep);
        setRota(sonuc);
        setAdim("sonuc");
      } catch (err) {
        setRota(null);
        setHata(err instanceof Error ? err.message : "Rota oluşturulamadı");
      }
    });
  }

  function senaryo2Alternatifler() {
    setHata(null);
    startTransition(async () => {
      try {
        const cevap = await rotaAlternatifleriOlustur({
          ...tercihGovdesi(),
          alternatif_sayisi: 3,
        });
        setAlternatifler(cevap.alternatifler);
        setAdim("alternatifler");
      } catch (err) {
        setAlternatifler([]);
        setHata(err instanceof Error ? err.message : "Alternatifler üretilemedi");
      }
    });
  }

  function alternatifSec(secilen: RotaCevap) {
    setHata(null);
    startTransition(async () => {
      try {
        const zengin = await konaklamaBolgesiOner(secilen.id);
        setRota(zengin);
        setAdim("sonuc");
      } catch (err) {
        setRota(secilen);
        setAdim("sonuc");
        setHata(err instanceof Error ? err.message : "Bölge önerisi alınamadı");
      }
    });
  }

  return (
    <div className="grid gap-12 lg:grid-cols-[1fr_1.2fr]">
      <div className="space-y-8">
        {adim === "senaryo" && (
          <div className="space-y-4">
            <p className="text-sm text-ink/50">Nasıl başlamak istersin?</p>
            <button
              type="button"
              onClick={() => {
                setSenaryo("bolge_belli");
                setAdim("tercihler");
              }}
              className="block w-full rounded-2xl bg-white/70 px-5 py-4 text-left transition hover:bg-white"
            >
              <span className="font-display text-xl text-deniz">Konaklama bölgem belli</span>
              <span className="mt-1 block text-sm text-ink/60">
                İlçe veya bölge seç; rota o merkez etrafında kurulsun.
              </span>
            </button>
            <button
              type="button"
              onClick={() => {
                setSenaryo("bolge_degil");
                setAdim("tercihler");
              }}
              className="block w-full rounded-2xl bg-white/70 px-5 py-4 text-left transition hover:bg-white"
            >
              <span className="font-display text-xl text-deniz">Henüz karar vermedim</span>
              <span className="mt-1 block text-sm text-ink/60">
                2–3 alternatif rota gör; sonra konaklama bölgesi önerilsin.
              </span>
            </button>
          </div>
        )}

        {adim === "tercihler" && (
          <form
            className="space-y-8"
            onSubmit={(e) => {
              e.preventDefault();
              if (senaryo === "bolge_belli") senaryo1Olustur();
              else senaryo2Alternatifler();
            }}
          >
            {senaryo === "bolge_belli" && !baslangicKonaklamaYerId && (
              <div>
                <label className="text-sm text-ink/50">Konaklama bölgesi</label>
                <select
                  value={bolgeAdi}
                  onChange={(e) => setBolgeAdi(e.target.value)}
                  className="mt-2 w-full rounded-xl border border-[var(--cizgi)] bg-white/80 px-3 py-2 text-sm"
                  required
                >
                  <option value="">Seç…</option>
                  {bolgeSecenekleri.map((adi) => (
                    <option key={adi} value={adi}>
                      {adi}
                    </option>
                  ))}
                </select>
              </div>
            )}
            {baslangicKonaklamaYerId && (
              <p className="text-sm text-ink/60">
                Konaklama üssü olarak seçtiğin yer kullanılacak.
              </p>
            )}

            <div>
              <label className="text-sm text-ink/50">Kaç gün?</label>
              <div className="mt-2 flex flex-wrap gap-2">
                {[1, 2, 3, 4, 5].map((g) => (
                  <button
                    key={g}
                    type="button"
                    onClick={() => setGunSayisi(g)}
                    className={`h-10 w-10 rounded-full text-sm font-medium transition ${
                      gunSayisi === g
                        ? "bg-deniz text-white"
                        : "bg-white/70 text-ink hover:bg-white"
                    }`}
                  >
                    {g}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <p className="text-sm text-ink/50">İlgi alanların</p>
              <div className="mt-3 space-y-4">
                {DENEYIM_EKSENLERI.map((eksen) => (
                  <label key={eksen.deger} className="block">
                    <span className="flex justify-between text-sm">
                      <span>{eksen.etiket}</span>
                      <span className="tabular-nums text-ink/45">
                        {Math.round((eksikler[eksen.deger] ?? 0) * 100)}%
                      </span>
                    </span>
                    <input
                      type="range"
                      min={0}
                      max={1}
                      step={0.1}
                      value={eksikler[eksen.deger] ?? 0}
                      onChange={(e) =>
                        eksenDegistir(eksen.deger, Number(e.target.value))
                      }
                      className="mt-1 w-full accent-yosun"
                    />
                  </label>
                ))}
              </div>
            </div>

            <div className="flex flex-wrap gap-4 text-sm">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={ucuz}
                  onChange={(e) => setUcuz(e.target.checked)}
                  className="accent-yosun"
                />
                Bütçe dostu tercih et
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={sakin}
                  onChange={(e) => setSakin(e.target.checked)}
                  className="accent-yosun"
                />
                Kalabalıktan uzak dur
              </label>
            </div>

            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() => setAdim("senaryo")}
                className="rounded-full bg-white/70 px-5 py-3 text-sm text-ink/70"
              >
                Geri
              </button>
              <button
                type="submit"
                disabled={bekliyor}
                className="rounded-full bg-gunes px-6 py-3 text-sm font-semibold text-deniz-derin transition hover:brightness-105 disabled:opacity-60"
              >
                {bekliyor
                  ? "Hazırlanıyor…"
                  : senaryo === "bolge_belli"
                    ? `${sehirIsim} rotamı oluştur`
                    : "Alternatif rotaları göster"}
              </button>
            </div>
            {hata && (
              <p className="text-sm text-red-700/90 whitespace-pre-wrap">{hata}</p>
            )}
          </form>
        )}

        {adim === "alternatifler" && (
          <div className="space-y-4">
            <p className="text-sm text-ink/50">Bir rota seç; ardından konaklama bölgesi önerilecek.</p>
            {alternatifler.map((alt, i) => (
              <button
                key={alt.id}
                type="button"
                disabled={bekliyor}
                onClick={() => alternatifSec(alt)}
                className="block w-full rounded-2xl bg-white/70 px-5 py-4 text-left transition hover:bg-white disabled:opacity-60"
              >
                <span className="font-display text-xl text-deniz">
                  {alt.alternatif_etiketi ?? `Alternatif ${i + 1}`}
                </span>
                <span className="mt-1 block text-sm text-ink/60">
                  {alt.gunler.length} gün ·{" "}
                  {alt.gunler.reduce((a, g) => a + g.duraklar.length, 0)} durak ·{" "}
                  {(
                    alt.gunler.reduce((a, g) => a + g.toplam_mesafe_metre, 0) / 1000
                  ).toFixed(0)}{" "}
                  km
                </span>
              </button>
            ))}
            <button
              type="button"
              onClick={() => setAdim("tercihler")}
              className="rounded-full bg-white/70 px-5 py-3 text-sm text-ink/70"
            >
              Geri
            </button>
            {hata && (
              <p className="text-sm text-red-700/90 whitespace-pre-wrap">{hata}</p>
            )}
          </div>
        )}

        {adim === "sonuc" && (
          <button
            type="button"
            onClick={() => {
              setRota(null);
              setAlternatifler([]);
              setAdim("senaryo");
            }}
            className="rounded-full bg-white/70 px-5 py-3 text-sm text-ink/70"
          >
            Yeni rota
          </button>
        )}
      </div>

      <div>
        {!rota && adim !== "alternatifler" ? (
          <p className="text-ink/50">
            Senaryonu ve tercihlerini seçtiğinde plan burada belirecek.
          </p>
        ) : adim === "alternatifler" && !rota ? (
          <div className="space-y-8">
            {alternatifler.map((alt) => (
              <div key={alt.id} className="opacity-80">
                <p className="mb-3 text-sm text-ink/45">
                  {alt.alternatif_etiketi ?? "Önizleme"}
                </p>
                <RotaGunleri rota={alt} />
              </div>
            ))}
          </div>
        ) : rota ? (
          <RotaGunleri rota={rota} />
        ) : null}
      </div>
    </div>
  );
}
