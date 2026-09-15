"use client";

import Link from "next/link";
import { useEffect, useMemo, useReducer, useRef, useState } from "react";

import { AktifFiltreOzeti } from "@/components/arama/AktifFiltreOzeti";
import { AramaKutusu } from "@/components/arama/AramaKutusu";
import { FiltrePaneli } from "@/components/arama/FiltrePaneli";
import { apiDurumu, kesfetDegerlendir } from "@/lib/api";
import {
  aramaFiltreReducer,
  filtreleriUrlYaz,
  type AramaFiltreState,
} from "@/lib/arama-state";
import {
  kesfetCevapDurumu,
  reddiGeriAl as reddiGeriAlState,
  secenegiReddet,
} from "@/lib/kesfet-state";
import type {
  AramaFiltreDurumu,
  AramaFiltreKatalogu,
  KararBaglami,
  KesfetCevabi,
  KesfetSecenegi,
  SehirKapsami,
} from "@/lib/types";

type EkranDurumu =
  "initial" | "loading" | "success" | "empty" | "insufficient" | "unavailable" | "error";
type Props = {
  kapsam: SehirKapsami;
  filtreKatalogu: AramaFiltreKatalogu;
  ilkSorgu: string;
  ilkFiltreler: AramaFiltreDurumu;
};

function baglamAnahtari(sorgu: string, filtreler: AramaFiltreDurumu): string {
  return JSON.stringify({ sorgu: sorgu.trim(), filtreler });
}

function kosulSemalari(filtreler: AramaFiltreDurumu, katalog: AramaFiltreKatalogu) {
  const bul = (kod: string) => katalog.somut_kosullar.find((kosul) => kosul.kod === kod);
  return {
    zorunlu: filtreler.zorunluKosullar.flatMap((kod) => {
      const kosul = bul(kod);
      return kosul
        ? [
            {
              kod,
              iddia_ailesi: kosul.iddia_ailesi,
              beklenen_deger: true,
              karsilastirma: "esittir",
              kritik: true,
            },
          ]
        : [];
    }),
    tercihler: filtreler.tercihler.flatMap((kod) => {
      const kosul = bul(kod);
      return kosul
        ? [
            {
              kod,
              iddia_ailesi: kosul.iddia_ailesi,
              beklenen_deger: true,
              karsilastirma: "esittir",
              oncelik: 1,
            },
          ]
        : [];
    }),
  };
}

function BilgiSatiri({
  baslik,
  metin,
  vurgu = false,
}: {
  baslik: string;
  metin: string;
  vurgu?: boolean;
}) {
  return (
    <div
      className={
        vurgu ? "border-bordo border-l-2 pl-3" : "border-deniz/25 border-l-2 pl-3"
      }
    >
      <dt className="text-ink/50 text-xs font-semibold tracking-wide uppercase">
        {baslik}
      </dt>
      <dd className="text-ink/80 mt-1 text-sm leading-6">{metin}</dd>
    </div>
  );
}

export function KesfetKararAlani({
  kapsam,
  filtreKatalogu,
  ilkSorgu,
  ilkFiltreler,
}: Props) {
  const [sorgu, setSorgu] = useState(ilkSorgu);
  const [amac, setAmac] = useState("");
  const [filtreState, filtreEylemi] = useReducer(aramaFiltreReducer, {
    uygulanan: ilkFiltreler,
    taslak: ilkFiltreler,
  } satisfies AramaFiltreState);
  const [cevap, setCevap] = useState<KesfetCevabi | null>(null);
  const [durum, setDurum] = useState<EkranDurumu>("initial");
  const [hataMesaji, setHataMesaji] = useState("");
  const [reddedilenler, setReddedilenler] = useState<string[]>([]);
  const [geriAl, setGeriAl] = useState<{ secenek: KesfetSecenegi; sira: number } | null>(
    null,
  );
  const istek = useRef<AbortController | null>(null);
  const anahtar = useMemo(
    () => baglamAnahtari(sorgu, filtreState.uygulanan),
    [sorgu, filtreState.uygulanan],
  );

  useEffect(() => {
    const sakli = window.sessionStorage.getItem(`kesfet:${anahtar}`);
    if (!sakli) return;
    try {
      const veri = JSON.parse(sakli) as { amac?: string; reddedilenler?: string[] };
      // Oturum depolaması, ayrıntıdan geri dönüşte URL'ye yazılmayan amacı geri kurar.
      // eslint-disable-next-line react-hooks/set-state-in-effect
      if (veri.amac) setAmac(veri.amac);
      if (Array.isArray(veri.reddedilenler)) setReddedilenler(veri.reddedilenler);
    } catch {
      /* Bozuk oturum verisi karar bağlamı sayılmaz. */
    }
  }, [anahtar]);
  useEffect(() => {
    window.sessionStorage.setItem(
      `kesfet:${anahtar}`,
      JSON.stringify({ amac, reddedilenler }),
    );
  }, [anahtar, amac, reddedilenler]);
  useEffect(() => () => istek.current?.abort(), []);

  async function degerlendir({ dahaFazla = false }: { dahaFazla?: boolean } = {}) {
    if (!sorgu.trim()) {
      setDurum("initial");
      return;
    }
    istek.current?.abort();
    const denetleyici = new AbortController();
    istek.current = denetleyici;
    setDurum("loading");
    setHataMesaji("");
    const urlSorgusu = sorgu.trim().length <= 80 ? sorgu.trim() : "";
    window.history.replaceState(
      null,
      "",
      `${window.location.pathname}?${filtreleriUrlYaz(filtreState.uygulanan, urlSorgusu)}`,
    );
    const kosullar = kosulSemalari(filtreState.uygulanan, filtreKatalogu);
    const kararBaglami: KararBaglami = {
      amac: amac.trim() || null,
      cografi_baglam: {
        sehir: kapsam.sehir_ismi,
        ilce:
          filtreKatalogu.ilceler.find((ilce) => ilce.id === filtreState.uygulanan.ilce)
            ?.isim ?? null,
        alan: null,
      },
      zorunlu_kosullar: kosullar.zorunlu,
      tercihler: kosullar.tercihler,
      reddedilen_yerler: reddedilenler,
    };
    window.sessionStorage.setItem(
      "kesfet:aktif-baglam",
      JSON.stringify({ donus, baglam: kararBaglami }),
    );
    try {
      const yeni = await kesfetDegerlendir(
        {
          sorgu: sorgu.trim(),
          baglam: kararBaglami,
          arama: { ilce_id: filtreState.uygulanan.ilce, tur: filtreState.uygulanan.tur },
          haric_yerler: dahaFazla
            ? [
                ...reddedilenler,
                ...(cevap?.secenekler.map((secenek) => secenek.yer.place_id) ?? []),
              ]
            : reddedilenler,
        },
        denetleyici.signal,
      );
      if (denetleyici.signal.aborted) return;
      setCevap((eski) =>
        dahaFazla && eski
          ? { ...yeni, secenekler: [...eski.secenekler, ...yeni.secenekler] }
          : yeni,
      );
      setDurum(kesfetCevapDurumu(yeni));
    } catch (hata) {
      if (denetleyici.signal.aborted) return;
      const hataDurumu = apiDurumu(hata);
      setDurum(
        hataDurumu === "empty" || hataDurumu === "insufficient"
          ? hataDurumu
          : hataDurumu === "unavailable"
            ? "unavailable"
            : "error",
      );
      setHataMesaji(
        hata instanceof Error ? hata.message : "Keşfet değerlendirmesi tamamlanamadı.",
      );
    }
  }

  function reddet(secenek: KesfetSecenegi, sira: number) {
    const sonuc = secenegiReddet(cevap?.secenekler ?? [], reddedilenler, secenek);
    setCevap((eski) => (eski ? { ...eski, secenekler: sonuc.secenekler } : eski));
    setReddedilenler(sonuc.reddedilenler);
    setGeriAl({ secenek, sira });
  }
  function reddiGeriAl() {
    if (!geriAl) return;
    const sonuc = reddiGeriAlState(
      cevap?.secenekler ?? [],
      reddedilenler,
      geriAl.secenek,
      geriAl.sira,
    );
    setReddedilenler(sonuc.reddedilenler);
    setCevap((eski) => (eski ? { ...eski, secenekler: sonuc.secenekler } : eski));
    setGeriAl(null);
  }

  const donusSorgusu = filtreleriUrlYaz(
    filtreState.uygulanan,
    sorgu.trim().length <= 80 ? sorgu.trim() : "",
  );
  const donus = `/sehir/${kapsam.sehir_anahtari}${donusSorgusu ? `?${donusSorgusu}` : ""}`;
  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_21rem] lg:items-start">
      <section aria-labelledby="kesfet-baslik" className="space-y-6">
        <div>
          <p className="text-bordo text-sm font-semibold">Keşfet</p>
          <h1 id="kesfet-baslik" className="yazi-hero text-ink mt-2">
            Bu ziyaret için birkaç anlamlı seçenek bul
          </h1>
          <p className="yazi-govde text-ink/65 mt-3 max-w-3xl">
            Kataloğu doldurmak yerine yayımlanmış bilgilerle gerekçelendirebildiğimiz
            yerleri gösteririz.
          </p>
        </div>
        <div className="space-y-4">
          <AramaKutusu
            deger={sorgu}
            onDegerDegis={setSorgu}
            onAra={() => void degerlendir()}
            yukleniyor={durum === "loading"}
          />
          <label className="grid gap-2 text-sm font-semibold">
            Bu ziyarette ne yapmak istiyorsun?
            <input
              value={amac}
              onChange={(olay) => setAmac(olay.target.value)}
              placeholder="Örn. uzun sohbet etmek"
              className="border-deniz/20 focus-visible:ring-deniz min-h-11 rounded-2xl border bg-white px-4 text-base font-normal outline-none focus-visible:ring-2"
            />
          </label>
          <AktifFiltreOzeti filtreler={filtreState.uygulanan} katalog={filtreKatalogu} />
        </div>
        {durum === "initial" ? (
          <div
            className="border-deniz/15 bg-kopuk/35 rounded-3xl border p-6"
            role="status"
          >
            <h2 className="text-lg font-semibold">Aramayla başlayabilirsin</h2>
            <p className="text-ink/65 mt-2">
              Yer veya türü yaz; ziyaret amacın öneri ile yalnızca yer bulma arasındaki
              farkı kurar.
            </p>
          </div>
        ) : null}
        {durum === "loading" ? (
          <p role="status" className="text-ink/65 py-8">
            Bu bağlam için yayımlanmış bilgiler değerlendiriliyor…
          </p>
        ) : null}
        {durum === "unavailable" || durum === "error" ? (
          <div role="alert" className="border-bordo/20 rounded-3xl border p-6">
            <h2 className="font-semibold">Değerlendirme tamamlanamadı</h2>
            <p className="text-ink/65 mt-2">{hataMesaji}</p>
            <button
              type="button"
              onClick={() => void degerlendir()}
              className="text-bordo mt-4 min-h-11 underline"
            >
              Aynı bağlamla yeniden dene
            </button>
          </div>
        ) : null}
        {(durum === "success" || durum === "insufficient" || durum === "empty") &&
        cevap ? (
          <div aria-live="polite" className="space-y-5">
            <div>
              <h2 className="yazi-alt text-bordo">Karar özeti</h2>
              <p className="text-ink/70 mt-2">{cevap.sinirlama_nedeni}</p>
              {cevap.degerlendirilemeyen_aday_sayisi > 0 ? (
                <p className="text-ink/55 mt-1 text-sm">
                  Bazı adayları kritik bilgi eksik olduğu için doğrulanmış seçeneklere
                  katmadık.
                </p>
              ) : null}
            </div>
            {cevap.secenekler.length ? (
              <ol aria-label="Hedefli seçenekler" className="grid gap-5">
                {cevap.secenekler.map((secenek, sira) => {
                  const karar = secenek.karar_sonucu;
                  return (
                    <li
                      key={secenek.yer.place_id}
                      className="border-deniz/12 rounded-3xl border bg-white p-5 shadow-sm sm:p-6"
                    >
                      <p className="text-ink/50 text-sm">
                        {secenek.cografya.ilce_ismi ?? secenek.cografya.sehir_ismi} ·{" "}
                        {(
                          secenek.alt_kategori ??
                          secenek.ana_kategori ??
                          "mekân"
                        ).replaceAll("_", " ")}
                      </p>
                      <h3 className="text-ink mt-1 text-xl font-semibold">
                        <Link
                          href={`/yer/${secenek.yer.place_id}?donus=${encodeURIComponent(donus)}`}
                          className="decoration-deniz underline decoration-1 underline-offset-4 hover:decoration-2"
                        >
                          {secenek.yer.isim}
                        </Link>
                      </h3>
                      <dl className="mt-5 grid gap-4 sm:grid-cols-2">
                        <BilgiSatiri baslik="Neden bu?" metin={secenek.neden_bu} vurgu />
                        <BilgiSatiri baslik="Anlamlı fark" metin={secenek.anlamli_fark} />
                        <BilgiSatiri
                          baslik="Önemli ödün"
                          metin={
                            karar.onemli_odunler[0]?.mesaj ??
                            "Bu karar için yayımlanmış önemli bir ödün yok."
                          }
                        />
                        <BilgiSatiri
                          baslik="Kritik bilinmeyen"
                          metin={
                            karar.bilinmeyenler[0]?.mesaj ??
                            "Bu değerlendirmeyi durduran kritik bir bilinmeyen yok."
                          }
                        />
                      </dl>
                      <div className="mt-5 flex flex-wrap gap-4">
                        <Link
                          href={`/yer/${secenek.yer.place_id}?donus=${encodeURIComponent(donus)}`}
                          className="text-bordo min-h-11 py-2 text-sm font-semibold underline underline-offset-4"
                        >
                          Yeri ayrıntılı incele
                        </Link>
                        <button
                          type="button"
                          onClick={() => reddet(secenek, sira)}
                          className="text-ink/65 min-h-11 py-2 text-sm underline underline-offset-4"
                        >
                          Bu seçenek uymuyor
                        </button>
                      </div>
                    </li>
                  );
                })}
              </ol>
            ) : null}
            {cevap.kimlik_eslesmeleri.length ? (
              <section
                aria-labelledby="kimlik-eslesmeleri"
                className="border-deniz/12 rounded-3xl border p-5"
              >
                <h3 id="kimlik-eslesmeleri" className="font-semibold">
                  Adla bulunan yerler
                </h3>
                <p className="text-ink/60 mt-1 text-sm">
                  Bulunabilir olmaları, bu ziyaret için önerildikleri anlamına gelmez.
                </p>
                <ul className="mt-3 grid gap-2">
                  {cevap.kimlik_eslesmeleri.map((yer) => (
                    <li key={yer.place_id}>
                      <Link
                        className="text-bordo underline"
                        href={`/yer/${yer.place_id}?donus=${encodeURIComponent(donus)}`}
                      >
                        {yer.isim}
                      </Link>
                    </li>
                  ))}
                </ul>
              </section>
            ) : null}
            {geriAl ? (
              <div role="status" className="bg-kopuk rounded-2xl px-4 py-3 text-sm">
                “{geriAl.secenek.yer.isim}” yalnız bu karar bağlamında kaldırıldı.{" "}
                <button
                  type="button"
                  onClick={reddiGeriAl}
                  className="text-bordo min-h-11 px-2 font-semibold underline"
                >
                  Geri al
                </button>
              </div>
            ) : null}
            {cevap.daha_fazla_var_mi ? (
              <button
                type="button"
                onClick={() => void degerlendir({ dahaFazla: true })}
                className="border-deniz/20 min-h-11 rounded-full border px-5 font-semibold"
              >
                Kontrollü daha fazla seçenek göster
              </button>
            ) : null}
          </div>
        ) : null}
      </section>
      <aside className="space-y-5 lg:sticky lg:top-24">
        <section className="border-deniz/12 rounded-3xl border p-5">
          <h2 className="font-semibold">{kapsam.sehir_ismi} kapsamı</h2>
          <p className="text-ink/65 mt-2 text-sm leading-6">{kapsam.kapsam_aciklamasi}</p>
          {!kapsam.karar_kapsami_destekleniyor ? (
            <p className="text-bordo mt-3 text-sm">
              Bu koşulu henüz doğrulayamıyoruz; sahte claim üretmiyoruz.
            </p>
          ) : null}
        </section>
        <FiltrePaneli
          katalog={filtreKatalogu}
          state={filtreState}
          onEylem={filtreEylemi}
        />
        <button
          type="button"
          onClick={() => void degerlendir()}
          className="bg-deniz min-h-11 w-full rounded-full px-5 font-semibold text-white"
        >
          Filtreleri bu karara uygula
        </button>
      </aside>
    </div>
  );
}
