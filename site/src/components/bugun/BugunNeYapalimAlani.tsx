"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import { Dugme } from "@/components/ui/Dugme";
import { apiDurumu, bugunNeYapalimDegerlendir } from "@/lib/api";
import type {
  AramaFiltreKatalogu,
  BugunAmaci,
  BugunNeYapalimCevabi,
  KesfetSecenegi,
} from "@/lib/types";

type Durum = "initial" | "loading" | "ready" | "unavailable" | "error";
const OTURUM_ANAHTARI = "bugun-ne-yapalim:v1";

function Bilgi({ baslik, metin }: { baslik: string; metin: string }) {
  return (
    <div className="border-deniz/25 border-l-2 pl-3">
      <dt className="text-ink/50 text-xs font-semibold tracking-wide uppercase">
        {baslik}
      </dt>
      <dd className="text-ink/80 mt-1 text-sm leading-6">{metin}</dd>
    </div>
  );
}

export function BugunNeYapalimAlani({
  sehir,
  sehirAnahtari,
  filtreKatalogu,
}: {
  sehir: string;
  sehirAnahtari: string;
  filtreKatalogu: AramaFiltreKatalogu | null;
}) {
  const [metin, setMetin] = useState("");
  const [amac, setAmac] = useState<BugunAmaci | "">("");
  const [ilce, setIlce] = useState("");
  const [sure, setSure] = useState("");
  const [wifiZorunlu, setWifiZorunlu] = useState(false);
  const [sakinTercih, setSakinTercih] = useState(false);
  const [reddedilenler, setReddedilenler] = useState<string[]>([]);
  const [cevap, setCevap] = useState<BugunNeYapalimCevabi | null>(null);
  const [durum, setDurum] = useState<Durum>("initial");
  const [hataMesaji, setHataMesaji] = useState("");
  const istek = useRef<AbortController | null>(null);

  useEffect(() => {
    const sakli = window.sessionStorage.getItem(OTURUM_ANAHTARI);
    if (!sakli) return;
    try {
      const veri = JSON.parse(sakli) as {
        metin?: string;
        amac?: BugunAmaci;
        ilce?: string;
        sure?: string;
        wifiZorunlu?: boolean;
        sakinTercih?: boolean;
        reddedilenler?: string[];
        cevap?: BugunNeYapalimCevabi;
      };
      // Ayrıntıdan geri dönüşte kullanıcının karar bağlamını geri kurar.
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setMetin(veri.metin ?? "");
      setAmac(veri.amac ?? "");
      setIlce(veri.ilce ?? "");
      setSure(veri.sure ?? "");
      setWifiZorunlu(Boolean(veri.wifiZorunlu));
      setSakinTercih(Boolean(veri.sakinTercih));
      setReddedilenler(veri.reddedilenler ?? []);
      if (veri.cevap) {
        setCevap(veri.cevap);
        setDurum("ready");
      }
    } catch {
      window.sessionStorage.removeItem(OTURUM_ANAHTARI);
    }
  }, []);
  useEffect(() => () => istek.current?.abort(), []);

  function sakla(yeniCevap: BugunNeYapalimCevabi, yeniReddedilenler = reddedilenler) {
    window.sessionStorage.setItem(
      OTURUM_ANAHTARI,
      JSON.stringify({
        metin,
        amac: yeniCevap.baglam.amac || undefined,
        ilce,
        sure,
        wifiZorunlu,
        sakinTercih,
        reddedilenler: yeniReddedilenler,
        cevap: yeniCevap,
      }),
    );
  }

  async function degerlendir(seciliAmac: BugunAmaci | "" = amac) {
    istek.current?.abort();
    const denetleyici = new AbortController();
    istek.current = denetleyici;
    setDurum("loading");
    setHataMesaji("");
    try {
      const yeni = await bugunNeYapalimDegerlendir(
        {
          serbest_metin: metin.trim() || null,
          niyet: {
            sehir,
            ilce: ilce || null,
            amac: seciliAmac || null,
            sure_dakika: sure ? Number(sure) : null,
            zorunlu_kosullar: wifiZorunlu ? ["wifi"] : [],
            tercihler: sakinTercih ? ["sessiz_ortam"] : [],
          },
          haric_yerler: reddedilenler,
        },
        denetleyici.signal,
      );
      if (denetleyici.signal.aborted) return;
      setAmac(seciliAmac);
      setCevap(yeni);
      setDurum("ready");
      sakla(yeni);
    } catch (hata) {
      if (denetleyici.signal.aborted) return;
      setDurum(apiDurumu(hata) === "unavailable" ? "unavailable" : "error");
      setHataMesaji(
        hata instanceof Error ? hata.message : "Değerlendirme tamamlanamadı.",
      );
    }
  }

  function reddet(secenek: KesfetSecenegi) {
    if (!cevap?.kesfet) return;
    const yeniReddedilenler = [...new Set([...reddedilenler, secenek.yer.place_id])];
    const yeni = {
      ...cevap,
      kesfet: {
        ...cevap.kesfet,
        secenekler: cevap.kesfet.secenekler.filter(
          (aday) => aday.yer.place_id !== secenek.yer.place_id,
        ),
      },
    };
    setReddedilenler(yeniReddedilenler);
    setCevap(yeni);
    sakla(yeni, yeniReddedilenler);
  }

  const donus = "/?bugun=1#bugun-ne-yapalim";
  const kesfetParams = new URLSearchParams();
  if (cevap?.kesfet_sorgusu) kesfetParams.set("q", cevap.kesfet_sorgusu);
  if (cevap?.baglam.amac) kesfetParams.set("amac", cevap.baglam.amac);
  const cevapIlce = cevap?.kesfet?.kullanilan_baglam.ilce_id;
  if (typeof cevapIlce === "string") kesfetParams.set("ilce", cevapIlce);
  if (wifiZorunlu) kesfetParams.append("zorunlu", "wifi");
  if (sakinTercih) kesfetParams.append("tercih", "sessiz_ortam");
  return (
    <section id="bugun-ne-yapalim" className="doku-kagit bg-kagit bolum scroll-mt-20">
      <div className="kabuk grid gap-8 lg:grid-cols-[minmax(0,1fr)_22rem] lg:items-start">
        <div>
          <p className="etiket text-bordo">Bugün Ne Yapalım?</p>
          <h2 className="yazi-bolum text-ink mt-3">
            Bugünkü niyetini birkaç işarete dönüştür
          </h2>
          <p className="yazi-govde text-ink/70 mt-4 max-w-2xl">
            Kısa bir cümle yaz. Gerekiyorsa yalnız kararı değiştirecek tek şeyi sorarız;
            sonuçları mevcut Keşfet ve Karar Motoru üretir.
          </p>
          <form
            className="mt-8 space-y-5"
            onSubmit={(olay) => {
              olay.preventDefault();
              void degerlendir();
            }}
          >
            <label className="block" htmlFor="bugun-metni">
              <span className="font-semibold">Bugün için ihtiyacın</span>
              <textarea
                id="bugun-metni"
                value={metin}
                onChange={(olay) => setMetin(olay.target.value)}
                placeholder="Örn. Atakum'da arkadaşlarla 2 saat kahve içmek istiyoruz."
                rows={3}
                className="border-bordo/20 bg-tuz focus:border-bordo mt-2 w-full resize-y rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-[var(--samandira)]"
              />
            </label>
            <details className="border-deniz/15 rounded-xl border p-4">
              <summary className="min-h-11 cursor-pointer py-2 font-semibold">
                Yazarak ilerlemek istemiyorum
              </summary>
              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                <label className="grid gap-2 text-sm font-semibold">
                  Ne yapmak istiyorsun?
                  <select
                    value={amac}
                    onChange={(e) => setAmac(e.target.value as BugunAmaci | "")}
                    className="border-bordo/20 bg-tuz min-h-11 rounded-lg border px-3"
                  >
                    <option value="">Seç</option>
                    <option value="kahve_icmek">Kahve içmek</option>
                    <option value="yemek_yemek">Yemek yemek</option>
                    <option value="tarihi_kulturel_ziyaret">Tarih-kültür ziyareti</option>
                  </select>
                </label>
                <label className="grid gap-2 text-sm font-semibold">
                  İlçe / yaklaşık alan
                  <select
                    value={ilce}
                    onChange={(e) => setIlce(e.target.value)}
                    className="border-bordo/20 bg-tuz min-h-11 rounded-lg border px-3"
                  >
                    <option value="">{sehir} geneli</option>
                    {filtreKatalogu?.ilceler.map((secenek) => (
                      <option key={secenek.id} value={secenek.isim}>
                        {secenek.isim}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="grid gap-2 text-sm font-semibold">
                  Kullanılabilir süre
                  <select
                    value={sure}
                    onChange={(e) => setSure(e.target.value)}
                    className="border-bordo/20 bg-tuz min-h-11 rounded-lg border px-3"
                  >
                    <option value="">Belirtme</option>
                    <option value="60">1 saat</option>
                    <option value="120">2 saat</option>
                    <option value="180">3 saat</option>
                  </select>
                </label>
                <fieldset className="space-y-3 text-sm">
                  <legend className="font-semibold">Koşullar</legend>
                  <label className="flex min-h-11 items-center gap-3">
                    <input
                      type="checkbox"
                      checked={wifiZorunlu}
                      onChange={(e) => setWifiZorunlu(e.target.checked)}
                    />{" "}
                    Wi-Fi kesin olsun
                  </label>
                  <label className="flex min-h-11 items-center gap-3">
                    <input
                      type="checkbox"
                      checked={sakinTercih}
                      onChange={(e) => setSakinTercih(e.target.checked)}
                    />{" "}
                    Sakin ortam tercih ederim
                  </label>
                </fieldset>
              </div>
            </details>
            <Dugme type="submit" yukleniyor={durum === "loading"}>
              Bugün için seçenek bul
            </Dugme>
          </form>
        </div>
        <aside
          className="border-deniz/15 min-h-64 rounded-3xl border bg-white p-5 sm:p-6"
          aria-live="polite"
        >
          {durum === "initial" ? (
            <>
              <p className="font-semibold">Kısa ve dürüst</p>
              <p className="text-ink/65 mt-2 text-sm leading-6">
                Konum izni gerekmez. Çalışma saati doğrulanmıyorsa “şu an açık” demeyiz.
              </p>
            </>
          ) : null}
          {durum === "loading" ? (
            <p role="status">Niyetin karar bağlamına çevriliyor…</p>
          ) : null}
          {durum === "unavailable" || durum === "error" ? (
            <div role="alert">
              <p className="font-semibold">Değerlendirme tamamlanamadı</p>
              <p className="text-ink/65 mt-2 text-sm">{hataMesaji}</p>
              <button
                className="text-bordo mt-4 min-h-11 underline"
                onClick={() => void degerlendir()}
              >
                Aynı bağlamla yeniden dene
              </button>
            </div>
          ) : null}
          {durum === "ready" && cevap ? (
            <div>
              <p className="font-semibold">Anlaşılan ihtiyaç</p>
              <p className="text-ink/75 mt-2 text-sm leading-6">
                {cevap.anlasilan_ihtiyac_ozeti}
              </p>
              <p className="text-ink/55 mt-4 text-xs leading-5">
                {cevap.bugun_baglami.aciklik_aciklamasi}
              </p>
              {cevap.netlestirme ? (
                <div className="mt-5">
                  <p className="font-semibold">{cevap.netlestirme.soru}</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {cevap.netlestirme.secenekler.map((secenek) => (
                      <button
                        key={secenek.deger}
                        className="border-bordo text-bordo min-h-11 rounded-lg border px-3 text-sm font-semibold"
                        onClick={() => void degerlendir(secenek.deger)}
                      >
                        {secenek.etiket}
                      </button>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          ) : null}
        </aside>
      </div>
      {durum === "ready" && cevap?.kesfet ? (
        <div className="kabuk mt-12" aria-live="polite">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <h3 className="yazi-alt text-bordo">Bugün için hedefli seçenekler</h3>
              <p className="text-ink/65 mt-2 max-w-2xl">
                {cevap.kesfet.sinirlama_nedeni}
              </p>
              {cevap.kesfet.degerlendirilemeyen_aday_sayisi > 0 ? (
                <p className="text-ink/55 mt-2 max-w-2xl text-sm">
                  Bazı adayları kritik bilgi eksikliği nedeniyle doğrulanmış seçeneklere
                  katmadık.
                </p>
              ) : null}
            </div>
            {cevap.kesfet_sorgusu ? (
              <Link
                className="text-bordo min-h-11 py-2 font-semibold underline underline-offset-4"
                href={`/sehir/${sehirAnahtari}?${kesfetParams}`}
              >
                Aynı aramayı Keşfet’te aç
              </Link>
            ) : null}
          </div>
          {cevap.kesfet.secenekler.length ? (
            <ol
              className="mt-6 grid gap-5 md:grid-cols-2"
              aria-label="Bugün için seçenekler"
            >
              {cevap.kesfet.secenekler.map((secenek) => (
                <li
                  key={secenek.yer.place_id}
                  className="border-deniz/12 rounded-3xl border bg-white p-5 shadow-sm"
                >
                  <p className="text-ink/50 text-sm">
                    {secenek.cografya.ilce_ismi ?? secenek.cografya.sehir_ismi}
                  </p>
                  <h4 className="yazi-kart text-bordo mt-2">
                    <Link
                      href={`/yer/${secenek.yer.place_id}?donus=${encodeURIComponent(donus)}`}
                      onClick={() =>
                        window.sessionStorage.setItem(
                          "kesfet:aktif-baglam",
                          JSON.stringify({ donus, baglam: cevap.baglam }),
                        )
                      }
                      className="decoration-deniz underline underline-offset-4"
                    >
                      {secenek.yer.isim}
                    </Link>
                  </h4>
                  <dl className="mt-5 grid gap-4">
                    <Bilgi baslik="Neden bu?" metin={secenek.neden_bu} />
                    <Bilgi
                      baslik="Önemli ödün"
                      metin={
                        secenek.karar_sonucu.onemli_odunler[0]?.mesaj ??
                        "Yayımlanmış önemli bir ödün yok."
                      }
                    />
                    <Bilgi
                      baslik="Kritik bilinmeyen"
                      metin={
                        secenek.karar_sonucu.bilinmeyenler[0]?.mesaj ??
                        "Bu değerlendirmeyi durduran kritik bilinmeyen yok."
                      }
                    />
                  </dl>
                  <button
                    className="text-ink/55 mt-5 min-h-11 text-sm underline"
                    onClick={() => reddet(secenek)}
                  >
                    Bu seçeneği gösterme
                  </button>
                </li>
              ))}
            </ol>
          ) : (
            <div className="border-bordo/15 mt-6 rounded-2xl border p-5">
              <p className="font-semibold">Koşulları gevşetmedik</p>
              <p className="text-ink/65 mt-2">
                Bu bağlam için yayımlanmış ve kritik koşulları doğrulanmış seçenek yok.
              </p>
            </div>
          )}
        </div>
      ) : null}
    </section>
  );
}
