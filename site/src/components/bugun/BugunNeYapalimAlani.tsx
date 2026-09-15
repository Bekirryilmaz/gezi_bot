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
const OTURUM_ANAHTARI = "bugun-ne-yapalim:v2";
const IHTIYAC_ETIKETLERI: Record<string, string> = {
  partner: "Partnerinle vakit geçirmek",
  aile: "Ailenle vakit geçirmek",
  arkadaslar: "Arkadaşlarınla vakit geçirmek",
  cocuklar: "Çocuklarla vakit geçirmek",
  yalniz: "Tek başına vakit geçirmek",
  kahve_icmek: "Kahve içmek",
  yemek_yemek: "Yemek yemek",
  tatli_yemek: "Tatlı yemek",
  kahvalti_yapmak: "Kahvaltı yapmak",
  eglence: "Eğlenmek",
  gezme: "Gezmek",
  tarihi_kulturel_ziyaret: "Tarih ve kültür gezisi",
  acik_hava: "Açık havada vakit geçirmek",
  calisma: "Çalışmak",
  birlikte_vakit: "Birlikte vakit geçirmek",
  aileyle_vakit: "Ailece vakit geçirmek",
  cocukla_aktivite: "Çocuklarla bir şey yapmak",
  sohbet: "Sohbet etmek",
  oturmak: "Oturmak",
  dolasmak: "Dolaşmak",
  canli_muzik: "Canlı müzik",
};

const KOSUL_ETIKETLERI: Record<string, string> = {
  wifi: "Wi-Fi",
  otopark: "Otopark",
  sessiz_ortam: "Sessiz ortam",
  uygun_fiyat: "Uygun fiyat",
  yakinda: "Yakın bir yer",
  manzara: "Manzara",
  calisma_uygunlugu: "Laptopla çalışmaya uygunluk",
  muze_turu: "Müze ziyareti",
  tekerlekli_sandalye_erisimi: "Tekerlekli sandalye erişimi",
  basamaksiz_giris: "Basamaksız giriş",
  ucretsiz: "Ücretsiz olması",
};

function bilinmeyenMetni(secenek: KesfetSecenegi, cevap: BugunNeYapalimCevabi) {
  const dogrulanan = new Set(
    secenek.karar_sonucu.gerekceler
      .filter((g) => ["tercih_destekleniyor", "zorunlu_kosul_dogrulandi"].includes(g.kod))
      .map((g) => KOSUL_ETIKETLERI[g.ilgili_kosul ?? ""]),
  );
  const bilinmeyenler = [
    ...cevap.dogrulanamayan_ihtiyaclar,
    ...[...secenek.karar_sonucu.bilinmeyenler, ...secenek.karar_sonucu.onemli_odunler]
      .filter((g) => /bilinmiyor|celiskili|eskimis|geri_cekilmis/.test(g.kod))
      .map((g) => KOSUL_ETIKETLERI[g.ilgili_kosul ?? ""] ?? g.mesaj),
  ];
  return (
    [...new Set(bilinmeyenler)].filter((b) => !dogrulanan.has(b)).join("; ") ||
    "İsteğinle ilgili ek bir belirsizlik belirlemedik."
  );
}

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
  const [oturumHazir, setOturumHazir] = useState(false);
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
  const metinAlani = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    // Oturum yuklenmeden SSR alanina yazilan yeni metin eski kayitla ezilmesin.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setOturumHazir(true);
    const sakli = window.sessionStorage.getItem(OTURUM_ANAHTARI);
    if (!sakli) return;
    try {
      const veri = JSON.parse(sakli) as {
        metin?: string;
        amac?: BugunAmaci;
        amacKaynagi?: "kullanici";
        ilce?: string;
        sure?: string;
        wifiZorunlu?: boolean;
        sakinTercih?: boolean;
        reddedilenler?: string[];
        cevap?: BugunNeYapalimCevabi;
      };
      // Ayrıntıdan geri dönüşte kullanıcının karar bağlamını geri kurar.
      setMetin(veri.metin ?? "");
      setAmac(veri.amacKaynagi === "kullanici" ? (veri.amac ?? "") : "");
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

  function sakla(
    yeniCevap: BugunNeYapalimCevabi,
    yeniReddedilenler = reddedilenler,
    kullaniciAmaci: BugunAmaci | "" = amac,
  ) {
    window.sessionStorage.setItem(
      OTURUM_ANAHTARI,
      JSON.stringify({
        metin,
        amac: kullaniciAmaci || undefined,
        amacKaynagi: "kullanici",
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
    const zamanAsimi = window.setTimeout(() => {
      if (istek.current !== denetleyici) return;
      setDurum("unavailable");
      setHataMesaji(
        "Değerlendirme beklenenden uzun sürdü. Biraz sonra yeniden deneyebilirsin.",
      );
      denetleyici.abort("timeout");
    }, 15_000);
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
      sakla(yeni, reddedilenler, seciliAmac);
    } catch (hata) {
      if (denetleyici.signal.aborted) return;
      setDurum(apiDurumu(hata) === "unavailable" ? "unavailable" : "error");
      setHataMesaji(
        hata instanceof Error ? hata.message : "Değerlendirme tamamlanamadı.",
      );
    } finally {
      window.clearTimeout(zamanAsimi);
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
  const anlasilanMaddeler = cevap?.anlasilan_ihtiyac
    ? [
        cevap.anlasilan_ihtiyac.kisi_baglami,
        cevap.anlasilan_ihtiyac.ana_amac,
        ...cevap.anlasilan_ihtiyac.alt_amaclar,
        ...cevap.anlasilan_ihtiyac.aktiviteler,
      ]
        .filter((deger): deger is string => Boolean(deger))
        .filter((deger, sira, tum) => tum.indexOf(deger) === sira)
        .map((deger) => IHTIYAC_ETIKETLERI[deger] ?? deger.replaceAll("_", " "))
        .concat(
          cevap.anlasilan_ihtiyac.zorunlu_kosullar.map(
            (kod) => `${KOSUL_ETIKETLERI[kod] ?? kod.replaceAll("_", " ")} kesin olsun`,
          ),
          cevap.anlasilan_ihtiyac.tercihler.map(
            (kod) => `Mümkünse ${KOSUL_ETIKETLERI[kod] ?? kod.replaceAll("_", " ")}`,
          ),
        )
    : [];
  return (
    <section id="bugun-ne-yapalim" className="doku-kagit bg-kagit bolum scroll-mt-20">
      <div className="kabuk grid gap-8 lg:grid-cols-[minmax(0,1fr)_22rem] lg:items-start">
        <div>
          <p className="etiket text-bordo">Bugün Ne Yapalım?</p>
          <h2 className="yazi-bolum text-ink mt-3">Bugün ne yapmak istiyorsun?</h2>
          <p className="yazi-govde text-ink/70 mt-4 max-w-2xl">
            Aklındaki planı günlük konuştuğun gibi yaz. Bildiğimiz kısmı kullanır,
            bilmediğimizi açıkça söyleriz.
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
                ref={metinAlani}
                id="bugun-metni"
                value={metin}
                disabled={!oturumHazir}
                onChange={(olay) => {
                  istek.current?.abort();
                  setMetin(olay.target.value);
                  setAmac("");
                  setCevap(null);
                  setDurum("initial");
                }}
                placeholder="Sevgilimle kahve içip sohbet edeceğiz"
                rows={3}
                className="border-bordo/20 bg-tuz focus:border-bordo mt-2 w-full resize-y rounded-xl border px-4 py-3 outline-none focus:ring-2 focus:ring-[var(--samandira)]"
              />
            </label>
            <p className="text-ink/60 text-sm leading-6">
              {oturumHazir
                ? "Örneğin: “Ailemi yemeğe götüreceğim” veya “Çalışmalık sakin bir kafe”."
                : "Giriş alanı hazırlanıyor… Birazdan planını yazabilirsin."}
            </p>
            <details className="border-deniz/15 rounded-xl border p-4">
              <summary className="min-h-11 cursor-pointer py-2 font-semibold">
                Seçenekleri daralt
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
                    <option value="tatli_yemek">Tatlı yemek</option>
                    <option value="kahvalti_yapmak">Kahvaltı yapmak</option>
                    <option value="eglence">Eğlenmek</option>
                    <option value="gezme">Gezmek</option>
                    <option value="calisma">Çalışmak</option>
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
            <Dugme type="submit" disabled={!oturumHazir} yukleniyor={durum === "loading"}>
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
            <p role="status">Planına uygun seçeneklere bakıyoruz…</p>
          ) : null}
          {durum === "unavailable" || durum === "error" ? (
            <div role="alert">
              <p className="font-semibold">Değerlendirme tamamlanamadı</p>
              <p className="text-ink/65 mt-2 text-sm">{hataMesaji}</p>
              <button
                className="text-bordo mt-4 min-h-11 underline"
                onClick={() => void degerlendir()}
              >
                Yeniden dene
              </button>
            </div>
          ) : null}
          {durum === "ready" && cevap ? (
            <div>
              <div className="flex items-center justify-between gap-3">
                <p className="font-semibold">Şunu anladım:</p>
                <button
                  type="button"
                  className="text-bordo min-h-11 text-sm underline"
                  onClick={() => metinAlani.current?.focus()}
                >
                  Düzelt
                </button>
              </div>
              {anlasilanMaddeler.length ? (
                <ul className="text-ink/75 mt-2 list-disc space-y-1 pl-5 text-sm leading-6">
                  {anlasilanMaddeler.map((madde) => (
                    <li key={madde}>{madde}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-ink/75 mt-2 text-sm leading-6">
                  {cevap.anlasilan_ihtiyac_ozeti}
                </p>
              )}
              <p className="text-ink/70 mt-4 text-sm leading-6">
                {cevap.durum_aciklamasi}
              </p>
              {cevap.dogrulanamayan_ihtiyaclar?.length ? (
                <div className="border-bordo/15 mt-4 rounded-xl border p-3">
                  <p className="text-sm font-semibold">
                    Henüz doğrulayamadığımız noktalar
                  </p>
                  <ul className="text-ink/65 mt-2 list-disc pl-5 text-sm leading-6">
                    {cevap.dogrulanamayan_ihtiyaclar.map((ihtiyac) => (
                      <li key={ihtiyac}>{ihtiyac}</li>
                    ))}
                  </ul>
                </div>
              ) : null}
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
                  Bazı yerleri, isteğine uygun olup olmadığını henüz bilmediğimiz için
                  gösteremedik.
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
                      baslik="Bilmen gereken"
                      metin={
                        secenek.karar_sonucu.onemli_odunler[0]?.mesaj ??
                        "Bu seçenek için ek bir uyarımız yok."
                      }
                    />
                    <Bilgi
                      baslik="Henüz bilmiyoruz"
                      metin={bilinmeyenMetni(secenek, cevap)}
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
              <p className="font-semibold">İsteğini olduğu gibi koruduk</p>
              <p className="text-ink/65 mt-2">
                İsteğini karşıladığını doğrulayabildiğimiz bir yer henüz yok.
              </p>
            </div>
          )}
        </div>
      ) : null}
    </section>
  );
}
