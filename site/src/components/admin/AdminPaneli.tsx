"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import {
  AdminApiHatasi,
  adminGorunumu,
  adminIstek,
  eylemHazirMi,
  kritikEylemMi,
  type AdminGorunumDurumu,
  type AdminKimlik,
  type AuditOlayi,
  type Birlestirme,
  type ClaimInceleme,
  type ClaimOzet,
  type EslemeAdayi,
  type IncelemeDosyasi,
} from "@/lib/admin-api";

type Sekme = "kuyruk" | "kimlik" | "claim" | "audit";

function EylemFormu({
  eylem,
  nesneTuru,
  nesneId,
  payload = {},
  tamamlandi,
}: {
  eylem: string;
  nesneTuru: string;
  nesneId: string;
  payload?: Record<string, unknown>;
  tamamlandi: () => void;
}) {
  const [gerekce, setGerekce] = useState("");
  const [onay, setOnay] = useState(false);
  const [hata, setHata] = useState("");
  const [bekliyor, setBekliyor] = useState(false);
  const kritik = kritikEylemMi(eylem);
  async function gonder(event: FormEvent) {
    event.preventDefault();
    if (!eylemHazirMi(eylem, gerekce, onay)) return;
    setBekliyor(true);
    setHata("");
    try {
      await adminIstek("/incelemeler", {
        method: "POST",
        body: JSON.stringify({
          eylem,
          nesne_turu: nesneTuru,
          nesne_id: nesneId,
          gerekce,
          payload,
        }),
      });
      setGerekce("");
      setOnay(false);
      tamamlandi();
    } catch (error) {
      setHata(error instanceof Error ? error.message : "İşlem tamamlanamadı.");
    } finally {
      setBekliyor(false);
    }
  }
  return (
    <form onSubmit={gonder} className="border-bordo/10 mt-3 grid gap-3 border-t pt-3">
      <label className="grid gap-1 text-xs font-medium">
        Gerekçe
        <textarea
          value={gerekce}
          onChange={(e) => setGerekce(e.target.value)}
          minLength={8}
          required
          rows={2}
          className="border-bordo/20 rounded border p-2 text-sm"
        />
      </label>
      {kritik && (
        <label className="flex items-start gap-2 text-xs">
          <input
            type="checkbox"
            checked={onay}
            onChange={(e) => setOnay(e.target.checked)}
            className="mt-0.5"
          />
          <span>
            Kamusal etkiyi inceledim; bu işlem ikinci bir kişi tarafından ayrıca
            onaylanacaktır.
          </span>
        </label>
      )}
      {hata && (
        <p role="alert" className="text-xs text-red-700">
          {hata}
        </p>
      )}
      <button
        disabled={bekliyor || !eylemHazirMi(eylem, gerekce, onay)}
        className="bg-bordo w-fit rounded px-3 py-2 text-xs font-semibold text-white disabled:opacity-40"
      >
        {bekliyor ? "İşleniyor…" : eylem.replaceAll("_", " ")}
      </button>
    </form>
  );
}

export function AdminPaneli() {
  const router = useRouter();
  const [durum, setDurum] = useState<AdminGorunumDurumu>("yukleniyor");
  const [kimlik, setKimlik] = useState<AdminKimlik | null>(null);
  const [kuyruk, setKuyruk] = useState<IncelemeDosyasi[]>([]);
  const [adaylar, setAdaylar] = useState<EslemeAdayi[]>([]);
  const [birlestirmeler, setBirlestirmeler] = useState<Birlestirme[]>([]);
  const [claimler, setClaimler] = useState<ClaimOzet[]>([]);
  const [audit, setAudit] = useState<AuditOlayi[]>([]);
  const [claim, setClaim] = useState<ClaimInceleme | null>(null);
  const [hata, setHata] = useState("");
  const [sekme, setSekme] = useState<Sekme>("kuyruk");

  const yenile = useCallback(async () => {
    try {
      const ben = await adminIstek<AdminKimlik>("/me");
      setKimlik(ben);
      const [yeniKuyruk, yeniAdaylar, yeniBirlestirmeler, yeniClaimler] =
        await Promise.all([
          adminIstek<IncelemeDosyasi[]>("/kuyruk"),
          adminIstek<EslemeAdayi[]>("/kimlik/esleme-adaylari"),
          adminIstek<Birlestirme[]>("/kimlik/birlestirmeler"),
          adminIstek<ClaimOzet[]>("/claimler"),
        ]);
      setKuyruk(yeniKuyruk);
      setAdaylar(yeniAdaylar);
      setBirlestirmeler(yeniBirlestirmeler);
      setClaimler(yeniClaimler);
      if (ben.yetkiler.includes("audit_gor"))
        setAudit(await adminIstek<AuditOlayi[]>("/audit"));
      setDurum("hazir");
    } catch (error) {
      if (error instanceof AdminApiHatasi && error.durum === 401) {
        setDurum("yetkisiz");
        router.replace("/admin/login");
      } else {
        setDurum("hata");
        setHata(error instanceof Error ? error.message : "Admin verisi yüklenemedi.");
      }
    }
  }, [router]);

  useEffect(() => {
    const zamanlayici = window.setTimeout(() => void yenile(), 0);
    return () => window.clearTimeout(zamanlayici);
  }, [yenile]);
  const gorunum = adminGorunumu(durum, kuyruk);
  if (gorunum === "loading" || gorunum === "login_redirect")
    return (
      <p role="status" className="p-8">
        Admin oturumu doğrulanıyor…
      </p>
    );
  if (gorunum === "error")
    return (
      <div className="p-8">
        <p role="alert">{hata}</p>
        <button
          onClick={() => void yenile()}
          className="bg-bordo mt-4 rounded px-4 py-2 text-white"
        >
          Tekrar dene
        </button>
      </div>
    );

  async function claimAra(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setHata("");
    const id = String(new FormData(event.currentTarget).get("claim_id") || "");
    try {
      setClaim(await adminIstek<ClaimInceleme>(`/claimler/${encodeURIComponent(id)}`));
    } catch (error) {
      setHata(error instanceof Error ? error.message : "Claim yüklenemedi.");
    }
  }

  async function ikinciOnay(dosya: IncelemeDosyasi, gerekce: string) {
    await adminIstek(`/incelemeler/${dosya.id}/ikinci-onay`, {
      method: "POST",
      body: JSON.stringify({ gerekce, beklenen_surum: dosya.surum }),
    });
    await yenile();
  }

  return (
    <div className="bg-sis min-h-screen">
      <header className="border-bordo/15 bg-murekkep text-kagit border-b">
        <div className="kabuk flex flex-wrap items-center justify-between gap-3 py-5">
          <div>
            <p className="etiket text-signal">Şamandıra operasyon</p>
            <h1 className="mt-1 text-xl font-semibold">Yayın ve düzeltme masası</h1>
          </div>
          <p className="text-sm">{kimlik?.gorunen_ad}</p>
        </div>
      </header>
      <main className="kabuk py-6 sm:py-10">
        <nav aria-label="Admin bölümleri" className="mb-6 flex gap-2 overflow-x-auto">
          {(["kuyruk", "kimlik", "claim", "audit"] as Sekme[])
            .filter((s) => s !== "audit" || kimlik?.yetkiler.includes("audit_gor"))
            .map((s) => (
              <button
                key={s}
                onClick={() => setSekme(s)}
                aria-pressed={sekme === s}
                className="border-bordo/20 aria-pressed:bg-bordo rounded-full border px-4 py-2 text-sm aria-pressed:text-white"
              >
                {s}
              </button>
            ))}
        </nav>
        {hata && (
          <p role="alert" className="mb-4 rounded bg-red-50 p-3 text-red-800">
            {hata}
          </p>
        )}
        {sekme === "kuyruk" && (
          <section>
            <h2 className="yazi-alt">İnceleme kuyruğu</h2>
            <div className="mt-4 grid gap-4">
              {kuyruk.length === 0 && <p>Bekleyen dosya yok.</p>}
              {kuyruk.map((dosya) => (
                <article
                  key={dosya.id}
                  className="border-bordo/15 rounded-lg border bg-white p-4"
                >
                  <div className="flex flex-wrap justify-between gap-2">
                    <strong>{dosya.onerilen_eylem}</strong>
                    <span className="text-xs uppercase">
                      {dosya.risk_sinifi} · {dosya.durum}
                    </span>
                  </div>
                  <p className="mt-2 text-sm break-all">
                    {dosya.nesne_turu}: {dosya.nesne_id}
                  </p>
                  {dosya.durum === "ikinci_inceleme_bekliyor" &&
                    kimlik?.yetkiler.includes("ikinci_incele") && (
                      <IkinciOnayFormu onayla={(g) => ikinciOnay(dosya, g)} />
                    )}
                </article>
              ))}
            </div>
          </section>
        )}
        {sekme === "kimlik" && (
          <section>
            <h2 className="yazi-alt">Kimlik eşleme adayları</h2>
            <div className="mt-4 grid gap-4 md:grid-cols-2">
              {adaylar.map((aday) => (
                <article
                  key={aday.id}
                  className="border-bordo/15 rounded-lg border bg-white p-4"
                >
                  <strong>Güven: %{Math.round(aday.confidence * 100)}</strong>
                  <p className="mt-2 text-xs break-all">
                    Sol: {aday.sol_sube_id}
                    <br />
                    Sağ: {aday.sag_sube_id}
                  </p>
                  <details className="mt-2 text-xs">
                    <summary>Belirsizlik</summary>
                    <pre className="mt-2 overflow-auto">
                      {JSON.stringify(aday.belirsizlik, null, 2)}
                    </pre>
                  </details>
                  <EylemFormu
                    eylem="esleme_reddet"
                    nesneTuru="esleme_adayi"
                    nesneId={aday.id}
                    tamamlandi={() => void yenile()}
                  />
                  <EylemFormu
                    eylem="canonical_merge"
                    nesneTuru="esleme_adayi"
                    nesneId={aday.id}
                    payload={{ hedef_sube_id: aday.sol_sube_id }}
                    tamamlandi={() => void yenile()}
                  />
                </article>
              ))}
            </div>
            <h3 className="yazi-kart mt-8">Aktif birleşmeler / split</h3>
            <div className="mt-3 grid gap-4 md:grid-cols-2">
              {birlestirmeler.map((kayit) => (
                <article
                  key={kayit.id}
                  className="border-bordo/15 rounded-lg border bg-white p-4"
                >
                  <p className="text-xs break-all">
                    Kaynak: {kayit.kaynak_sube_id}
                    <br />
                    Hedef: {kayit.hedef_sube_id}
                  </p>
                  <EylemFormu
                    eylem="split"
                    nesneTuru="sube"
                    nesneId={kayit.kaynak_sube_id}
                    payload={{ birlesme_id: kayit.id }}
                    tamamlandi={() => void yenile()}
                  />
                </article>
              ))}
            </div>
          </section>
        )}
        {sekme === "claim" && (
          <section>
            <h2 className="yazi-alt">Claim inceleme</h2>
            <div className="mt-4 flex gap-2 overflow-x-auto pb-2">
              {claimler.map((c) => (
                <button
                  key={c.id}
                  onClick={async () => {
                    setClaim(await adminIstek<ClaimInceleme>(`/claimler/${c.id}`));
                  }}
                  className="border-bordo/15 min-w-48 rounded border bg-white p-3 text-left text-xs"
                >
                  <strong className="block">{c.aile}</strong>
                  <span className="mt-1 block break-all">{c.id}</span>
                </button>
              ))}
            </div>
            <form onSubmit={claimAra} className="mt-4 flex max-w-xl gap-2">
              <label className="sr-only" htmlFor="claim_id">
                Claim ID
              </label>
              <input
                id="claim_id"
                name="claim_id"
                required
                placeholder="Claim UUID"
                className="border-bordo/20 min-w-0 flex-1 rounded border bg-white px-3 py-2"
              />
              <button className="bg-bordo rounded px-4 py-2 text-white">Getir</button>
            </form>
            {claim && (
              <article className="border-bordo/15 mt-5 rounded-lg border bg-white p-5">
                <div className="flex flex-wrap justify-between gap-2">
                  <h3 className="font-semibold">{claim.aile}</h3>
                  <span className="bg-kopuk rounded px-2 py-1 text-xs">
                    {claim.yayin_onizleme.durum}
                  </span>
                </div>
                <p className="mt-2 text-sm">
                  Nedenler: {claim.yayin_onizleme.neden_kodlari.join(", ") || "yok"}
                </p>
                <p className="mt-2 text-sm">
                  Etkilenen alanlar:{" "}
                  {claim.yayin_onizleme.etkilenen_public_alanlar.join(", ")}
                </p>
                <div className="bg-sis mt-3 grid gap-2 rounded p-3 text-xs">
                  <div>
                    <strong>Kapsam</strong>
                    <pre className="mt-1 overflow-auto whitespace-pre-wrap">
                      {JSON.stringify(claim.kapsam, null, 2)}
                    </pre>
                  </div>
                  <div>
                    <strong>Aktif sürüm</strong>
                    <pre className="mt-1 overflow-auto whitespace-pre-wrap">
                      {JSON.stringify(claim.surum, null, 2)}
                    </pre>
                  </div>
                </div>
                <div className="mt-4 grid gap-4 md:grid-cols-2">
                  <KanitListesi
                    baslik="Destekleyen kanıt"
                    kanitlar={claim.supporting_evidence}
                  />
                  <KanitListesi baslik="Karşı kanıt" kanitlar={claim.counter_evidence} />
                </div>
                <div className="mt-4 grid gap-3 md:grid-cols-2">
                  <EylemFormu
                    eylem="claim_approve"
                    nesneTuru="claim"
                    nesneId={claim.id}
                    tamamlandi={() => void yenile()}
                  />
                  <EylemFormu
                    eylem="claim_limit"
                    nesneTuru="claim"
                    nesneId={claim.id}
                    tamamlandi={() => void yenile()}
                  />
                  <EylemFormu
                    eylem="claim_stale"
                    nesneTuru="claim"
                    nesneId={claim.id}
                    tamamlandi={() => void yenile()}
                  />
                  <EylemFormu
                    eylem="claim_reject"
                    nesneTuru="claim"
                    nesneId={claim.id}
                    tamamlandi={() => void yenile()}
                  />
                  <EylemFormu
                    eylem="withdraw"
                    nesneTuru="claim"
                    nesneId={claim.id}
                    tamamlandi={() => void yenile()}
                  />
                </div>
              </article>
            )}
          </section>
        )}
        {sekme === "audit" && (
          <section>
            <h2 className="yazi-alt">Append-only audit</h2>
            <div className="border-bordo/15 mt-4 overflow-x-auto rounded-lg border bg-white">
              <table className="w-full min-w-[760px] text-left text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="p-3">Zaman</th>
                    <th className="p-3">Eylem</th>
                    <th className="p-3">Nesne</th>
                    <th className="p-3">Gerekçe</th>
                    <th className="p-3">İstek</th>
                  </tr>
                </thead>
                <tbody>
                  {audit.map((olay) => (
                    <tr key={olay.id} className="border-b last:border-0">
                      <td className="p-3">
                        {new Date(olay.olusturulma_zamani).toLocaleString("tr-TR")}
                      </td>
                      <td className="p-3">{olay.eylem}</td>
                      <td className="p-3 break-all">
                        {olay.nesne_turu}:{olay.nesne_id}
                      </td>
                      <td className="p-3">{olay.gerekce}</td>
                      <td className="p-3 text-xs break-all">{olay.istek_id}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

function KanitListesi({
  baslik,
  kanitlar,
}: {
  baslik: string;
  kanitlar: Array<Record<string, unknown>>;
}) {
  return (
    <div>
      <h4 className="font-semibold">{baslik}</h4>
      {kanitlar.length === 0 ? (
        <p className="text-ink/60 mt-2 text-sm">Kayıt yok.</p>
      ) : (
        <ul className="mt-2 grid gap-2">
          {kanitlar.map((k, i) => (
            <li key={String(k.id || i)} className="bg-sis rounded p-3 text-xs">
              <strong>{String(k.kaynak || "kaynak")}</strong>
              <pre className="mt-1 overflow-auto whitespace-pre-wrap">
                {JSON.stringify(k.icerik_ozeti, null, 2)}
              </pre>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function IkinciOnayFormu({ onayla }: { onayla: (gerekce: string) => Promise<void> }) {
  const [gerekce, setGerekce] = useState("");
  const [onay, setOnay] = useState(false);
  const [hata, setHata] = useState("");
  return (
    <form
      className="mt-3 grid gap-2 border-t pt-3"
      onSubmit={async (e) => {
        e.preventDefault();
        try {
          await onayla(gerekce);
        } catch (error) {
          setHata(error instanceof Error ? error.message : "Onay başarısız.");
        }
      }}
    >
      <label className="grid gap-1 text-xs">
        Bağımsız inceleme gerekçesi
        <textarea
          value={gerekce}
          onChange={(e) => setGerekce(e.target.value)}
          minLength={8}
          required
          className="rounded border p-2"
        />
      </label>
      <label className="flex gap-2 text-xs">
        <input
          type="checkbox"
          checked={onay}
          onChange={(e) => setOnay(e.target.checked)}
        />
        Etkiyi ve önceki aktörü kontrol ettim.
      </label>
      {hata && (
        <p role="alert" className="text-xs text-red-700">
          {hata}
        </p>
      )}
      <button
        disabled={!onay || gerekce.trim().length < 8}
        className="bg-samandira w-fit rounded px-3 py-2 text-xs font-semibold text-white disabled:opacity-40"
      >
        İkinci onayı ver
      </button>
    </form>
  );
}
