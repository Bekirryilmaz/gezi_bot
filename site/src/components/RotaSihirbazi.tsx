"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { konaklamaBolgesiOner, rotaAlternatifleriOlustur, rotaOlustur } from "@/lib/api";
import { HATA_PUSULA } from "@/lib/marka";
import { DENEYIM_EKSENLERI, altKategoriEtiketi } from "@/lib/sabitler";
import type { BolgeProfili, RotaCevap } from "@/lib/types";
import { Dugme } from "@/components/ui/Dugme";
import { BosDurum } from "@/components/ui/BosDurum";
import { Spinner } from "@/components/ui/Spinner";

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
        <p className="border-bordo/12 text-ink/80 bg-tuz rounded-[12px] border p-5 text-sm leading-relaxed">
          {rota.rota_tavsiyesi}
        </p>
      )}
      {rota.konaklama_bolgesi_onerisi && (
        <div className="border-bordo/12 bg-tuz rounded-[12px] border p-5">
          <p className="text-ink/50 text-sm">Önerilen konaklama bölgesi</p>
          <p className="font-display text-bordo mt-1 text-2xl">
            {rota.konaklama_bolgesi_onerisi.bolge_adi}
          </p>
          {rota.konaklama_bolgesi_onerisi.gerekce && (
            <p className="text-ink/70 mt-2 text-sm">
              {rota.konaklama_bolgesi_onerisi.gerekce}
            </p>
          )}
          {rota.konaklama_bolgesi_onerisi.ornek_konaklamalar?.length > 0 && (
            <ul className="text-ink/60 mt-4 space-y-1 text-sm">
              <li className="text-ink/40">Bu bölgede örnek tesisler (zorunlu değil):</li>
              {rota.konaklama_bolgesi_onerisi.ornek_konaklamalar.slice(0, 3).map((k) => (
                <li key={k.id}>
                  <Link
                    href={`/yer/${k.id}`}
                    className="text-bordo decoration-deniz underline-offset-4 hover:underline hover:decoration-2"
                  >
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
          <h3 className="font-display text-bordo text-2xl">{gun.gun_no}. gün</h3>
          <p className="text-ink/50 mt-1 text-sm">
            {(gun.toplam_mesafe_metre / 1000).toFixed(1)} km · ~{gun.toplam_sure_dakikasi}{" "}
            dk
          </p>
          <ol className="mt-4 space-y-3">
            {gun.duraklar.map((durak) => (
              <li key={`${gun.gun_no}-${durak.sira}`}>
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
  const [bekliyor, setBekliyor] = useState(false);

  const bolgeSecenekleri = useMemo(() => {
    const adlar = new Set<string>();
    for (const b of bolgeler) {
      if (b.bolge_adi) adlar.add(b.bolge_adi);
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

  async function senaryo1Olustur() {
    setHata(null);
    const talep = {
      ...tercihGovdesi(),
      konaklama_yer_id: baslangicKonaklamaYerId || undefined,
      konaklama_bolge_adi: !baslangicKonaklamaYerId && bolgeAdi ? bolgeAdi : undefined,
    };
    if (!talep.konaklama_yer_id && !talep.konaklama_bolge_adi) {
      setHata("Konaklama bölgesi seç.");
      return;
    }
    setBekliyor(true);
    try {
      const sonuc = await rotaOlustur(talep);
      setRota(sonuc);
      setAdim("sonuc");
    } catch (err) {
      setRota(null);
      setHata(err instanceof Error ? err.message : HATA_PUSULA);
    } finally {
      setBekliyor(false);
    }
  }

  async function senaryo2Alternatifler() {
    setHata(null);
    setBekliyor(true);
    try {
      const cevap = await rotaAlternatifleriOlustur({
        ...tercihGovdesi(),
        alternatif_sayisi: 3,
      });
      setAlternatifler(cevap.alternatifler);
      setAdim("alternatifler");
    } catch (err) {
      setAlternatifler([]);
      setHata(err instanceof Error ? err.message : HATA_PUSULA);
    } finally {
      setBekliyor(false);
    }
  }

  async function alternatifSec(secilen: RotaCevap) {
    setHata(null);
    setBekliyor(true);
    try {
      const zengin = await konaklamaBolgesiOner(secilen.id);
      setRota(zengin);
      setAdim("sonuc");
    } catch (err) {
      setRota(secilen);
      setAdim("sonuc");
      setHata(err instanceof Error ? err.message : "Bölge önerisi alınamadı");
    } finally {
      setBekliyor(false);
    }
  }

  return (
    <div className="grid gap-12 lg:grid-cols-[1fr_1.2fr]">
      <div className="space-y-8">
        {adim === "senaryo" && (
          <div className="space-y-4">
            <p className="text-ink/50 text-sm">Nasıl başlamak istersin?</p>
            <button
              type="button"
              onClick={() => {
                setSenaryo("bolge_belli");
                setAdim("tercihler");
              }}
              className="border-bordo/12 hover:border-bordo/40 focus-visible:ring-samandira bg-tuz block w-full cursor-pointer rounded-[12px] border px-5 py-4 text-left transition-[border-color,background-color] duration-[var(--sure-hizli)] focus-visible:ring-2 focus-visible:outline-none"
            >
              <span className="font-display text-bordo text-xl">
                Konaklama bölgem belli
              </span>
              <span className="text-ink/60 mt-1 block text-sm">
                İlçe veya bölge seç; rota o merkez etrafında kurulsun.
              </span>
            </button>
            <button
              type="button"
              onClick={() => {
                setSenaryo("bolge_degil");
                setAdim("tercihler");
              }}
              className="border-bordo/12 hover:border-bordo/40 focus-visible:ring-samandira bg-tuz block w-full cursor-pointer rounded-[12px] border px-5 py-4 text-left transition-[border-color,background-color] duration-[var(--sure-hizli)] focus-visible:ring-2 focus-visible:outline-none"
            >
              <span className="font-display text-bordo text-xl">
                Henüz karar vermedim
              </span>
              <span className="text-ink/60 mt-1 block text-sm">
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
                <label className="text-ink/50 text-sm">Konaklama bölgesi</label>
                <select
                  value={bolgeAdi}
                  onChange={(e) => setBolgeAdi(e.target.value)}
                  className="border-bordo/12 bg-tuz mt-2 min-h-11 w-full cursor-pointer rounded-[8px] border px-3 py-2 text-sm"
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
              <p className="text-ink/60 text-sm">
                Konaklama üssü olarak seçtiğin yer kullanılacak.
              </p>
            )}

            <div>
              <label className="text-ink/50 text-sm">Kaç gün?</label>
              <div className="mt-2 flex flex-wrap gap-2">
                {[1, 2, 3, 4, 5].map((g) => (
                  <button
                    key={g}
                    type="button"
                    onClick={() => setGunSayisi(g)}
                    className={`focus-visible:ring-samandira inline-flex size-11 cursor-pointer items-center justify-center rounded-[8px] text-base font-medium transition-[background-color,color] duration-[var(--sure-hizli)] focus-visible:ring-2 focus-visible:outline-none ${
                      gunSayisi === g
                        ? "bg-samandira text-base font-semibold text-white"
                        : "text-ink hover:bg-kagit-koyu border-bordo/12 bg-tuz border"
                    }`}
                  >
                    {g}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <p className="text-ink/50 text-sm">İlgi alanların</p>
              <div className="mt-3 space-y-4">
                {DENEYIM_EKSENLERI.map((eksen) => (
                  <label key={eksen.deger} className="block">
                    <span className="flex justify-between text-sm">
                      <span>{eksen.etiket}</span>
                      <span className="text-ink/45 tabular-nums">
                        {Math.round((eksikler[eksen.deger] ?? 0) * 100)}%
                      </span>
                    </span>
                    <input
                      type="range"
                      min={0}
                      max={1}
                      step={0.1}
                      value={eksikler[eksen.deger] ?? 0}
                      onChange={(e) => eksenDegistir(eksen.deger, Number(e.target.value))}
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
                  onChange={(e) => setUcuz(e.target.checked)}
                  className="accent-yosun"
                />
                Bütçe dostu tercih et
              </label>
              <label className="flex min-h-11 cursor-pointer items-center gap-2">
                <input
                  type="checkbox"
                  checked={sakin}
                  onChange={(e) => setSakin(e.target.checked)}
                  className="accent-yosun"
                />
                Kalabalıktan uzak dur
              </label>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <Dugme varyant="hayalet" onClick={() => setAdim("senaryo")}>
                Geri
              </Dugme>
              <Dugme
                varyant="birincil"
                type="submit"
                disabled={bekliyor}
                yukleniyor={bekliyor}
              >
                {bekliyor
                  ? "Hazırlanıyor…"
                  : senaryo === "bolge_belli"
                    ? `${sehirIsim} rotasını oluştur`
                    : "Alternatif rotaları göster"}
              </Dugme>
              {bekliyor ? <Spinner className="text-bordo" /> : null}
            </div>
            {hata && (
              <p className="text-samandira-koyu text-sm whitespace-pre-wrap">{hata}</p>
            )}
          </form>
        )}

        {adim === "alternatifler" && (
          <div className="space-y-4">
            <p className="text-ink/50 text-sm">
              Bir rota seç; ardından konaklama bölgesi önerilecek.
            </p>
            {alternatifler.map((alt, i) => (
              <button
                key={alt.id}
                type="button"
                disabled={bekliyor}
                onClick={() => alternatifSec(alt)}
                className="border-bordo/12 hover:border-bordo/40 focus-visible:ring-samandira bg-tuz block w-full cursor-pointer rounded-[12px] border px-5 py-4 text-left transition-[border-color,background-color] duration-[var(--sure-hizli)] focus-visible:ring-2 focus-visible:outline-none disabled:opacity-60"
              >
                <span className="font-display text-bordo text-xl">
                  {alt.alternatif_etiketi ?? `Alternatif ${i + 1}`}
                </span>
                <span className="text-ink/60 mt-1 block text-sm">
                  {alt.gunler.length} gün ·{" "}
                  {alt.gunler.reduce((a, g) => a + g.duraklar.length, 0)} durak ·{" "}
                  {(
                    alt.gunler.reduce((a, g) => a + g.toplam_mesafe_metre, 0) / 1000
                  ).toFixed(0)}{" "}
                  km
                </span>
              </button>
            ))}
            <Dugme varyant="hayalet" onClick={() => setAdim("tercihler")}>
              Geri
            </Dugme>
            {hata && (
              <p className="text-samandira-koyu text-sm whitespace-pre-wrap">{hata}</p>
            )}
          </div>
        )}

        {adim === "sonuc" && (
          <Dugme
            varyant="hayalet"
            onClick={() => {
              setRota(null);
              setAlternatifler([]);
              setAdim("senaryo");
            }}
          >
            Yeni rota
          </Dugme>
        )}
      </div>

      <div>
        {!rota && adim !== "alternatifler" ? (
          <BosDurum
            tip="hazirlaniyor"
            baslik="Plan henüz yok"
            metin="Senaryonu ve tercihlerini seçtiğinde gün gün rota burada belirecek."
            ctalar={[]}
          />
        ) : adim === "alternatifler" && !rota ? (
          <div className="space-y-8">
            {alternatifler.map((alt) => (
              <div key={alt.id} className="opacity-80">
                <p className="text-ink/45 mb-3 text-sm">
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
