"use client";

import { useCallback, useState } from "react";
import { LocateFixed } from "lucide-react";
import { TURKIYE_SEHIRLERI } from "@/data/cities";
import {
  ONERI_KATEGORILERI,
  type PlaceSuggestionCategory,
} from "@/types/placeSuggestion";
import { FotografAlani } from "@/components/oneri/FotografAlani";
import { KonumSeciciYukle } from "@/components/oneri/KonumSeciciYukle";
import { SeciciMenu } from "@/components/oneri/SeciciMenu";
import { TurnstileWidget } from "@/components/oneri/TurnstileWidget";

const TURNSTILE_KEY = process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY ?? "";
const BASARI_MESAJI = "Öneriniz incelenmek üzere ekibimize ulaştı!";

type Koordinat = { lat: number; lng: number };
type Durum = "idle" | "gonderiliyor" | "tamam" | "hata";

export function OneriFormu() {
  const [baslik, setBaslik] = useState("");
  const [kategori, setKategori] = useState<PlaceSuggestionCategory | "">("");
  const [sehir, setSehir] = useState("");
  const [ilce, setIlce] = useState("");
  const [aciklama, setAciklama] = useState("");
  const [tuyo, setTuyo] = useState("");
  const [ad, setAd] = useState("");
  const [eposta, setEposta] = useState("");
  const [konum, setKonum] = useState<Koordinat | null>(null);
  const [fotograflar, setFotograflar] = useState<File[]>([]);
  const [turnstile, setTurnstile] = useState("");
  const [konumHatasi, setKonumHatasi] = useState<string | null>(null);
  const [durum, setDurum] = useState<Durum>("idle");
  const [mesaj, setMesaj] = useState<string | null>(null);

  const mevcutKonum = useCallback(() => {
    if (!navigator.geolocation) {
      setKonumHatasi("Tarayıcın konum paylaşımını desteklemiyor.");
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setKonum({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        setKonumHatasi(null);
      },
      () => setKonumHatasi("Konum alınamadı. Haritadan pin bırakabilirsin."),
      { enableHighAccuracy: true, timeout: 12000 },
    );
  }, []);

  async function gonder(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setMesaj(null);
    const honeypot = new FormData(e.currentTarget).get("sirket_sitesi");

    if (!kategori) {
      setDurum("hata");
      setMesaj("Bir kategori seç.");
      return;
    }
    if (!konum) {
      setDurum("hata");
      setMesaj("Haritadan konum seçmeden gönderilemez.");
      return;
    }
    if (fotograflar.length < 1) {
      setDurum("hata");
      setMesaj("En az bir fotoğraf yükle.");
      return;
    }
    if (TURNSTILE_KEY && !turnstile) {
      setDurum("hata");
      setMesaj("Doğrulamayı tamamla.");
      return;
    }

    const govde = new FormData();
    govde.set("baslik", baslik.trim());
    govde.set("kategori", kategori);
    govde.set("sehir", sehir.trim());
    govde.set("ilce", ilce.trim());
    govde.set("aciklama", aciklama.trim());
    govde.set("gonderen_eposta", eposta.trim());
    govde.set("enlem", String(konum.lat));
    govde.set("boylam", String(konum.lng));
    if (ad.trim()) govde.set("gonderen_adi", ad.trim());
    if (tuyo.trim()) govde.set("ziyaretci_tuyosu", tuyo.trim());
    if (turnstile) govde.set("turnstile_jetonu", turnstile);
    if (typeof honeypot === "string" && honeypot.trim()) {
      govde.set("sirket_sitesi", honeypot);
    }
    for (const dosya of fotograflar) {
      govde.append("fotograflar", dosya);
    }

    setDurum("gonderiliyor");
    try {
      const yanit = await fetch("/api/onerim-var/gonder", {
        method: "POST",
        body: govde,
      });
      const json = (await yanit.json()) as { mesaj?: string; detail?: string };
      if (!yanit.ok) {
        setDurum("hata");
        setMesaj(json.mesaj || json.detail || "Gönderilemedi.");
        return;
      }
      setDurum("tamam");
      setMesaj(BASARI_MESAJI);
      setBaslik("");
      setKategori("");
      setSehir("");
      setIlce("");
      setAciklama("");
      setTuyo("");
      setAd("");
      setEposta("");
      setKonum(null);
      setFotograflar([]);
      setTurnstile("");
    } catch {
      setDurum("hata");
      setMesaj("Bağlantı kurulamadı. Biraz sonra tekrar dene.");
    }
  }

  return (
    <form onSubmit={gonder} className="space-y-8 overflow-visible">
      <div className="relative z-20 grid grid-cols-1 gap-6 md:grid-cols-2">
        <label className="block space-y-2">
          <span className="text-sm font-medium text-deniz">Mekan adı</span>
          <input
            required
            minLength={3}
            maxLength={200}
            value={baslik}
            onChange={(e) => setBaslik(e.target.value)}
            className="w-full rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2.5 text-ink outline-none focus:border-deniz"
            placeholder="Örn. Gizli Çınaraltı"
          />
        </label>
        <SeciciMenu
          etiket="Kategori"
          yerTutucu="Kategori seç"
          deger={kategori}
          gerekli
          secenekler={ONERI_KATEGORILERI}
          onSec={(id) => setKategori(id as PlaceSuggestionCategory)}
        />
      </div>

      <div className="relative z-10 grid grid-cols-1 gap-6 md:grid-cols-2">
        <SeciciMenu
          etiket="Şehir"
          yerTutucu="Şehir seç veya yaz"
          deger={sehir}
          gerekli
          aranabilir
          secenekler={TURKIYE_SEHIRLERI.map((s) => ({
            id: s.name,
            etiket: s.name,
          }))}
          onSec={(id) => setSehir(id)}
        />
        <label className="block space-y-2">
          <span className="text-sm font-medium text-deniz">İlçe</span>
          <input
            required
            minLength={2}
            value={ilce}
            onChange={(e) => setIlce(e.target.value)}
            className="w-full rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2.5 outline-none focus:border-deniz"
            placeholder="Atakum"
          />
        </label>
      </div>

      <div className="relative z-0 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-sm font-medium text-deniz">Konum (zorunlu)</p>
            <p className="text-xs text-ink/55">
              Haritaya tıkla veya pini sürükle. Koordinat seçilmeden form gitmez.
            </p>
          </div>
          <button
            type="button"
            onClick={mevcutKonum}
            className="inline-flex items-center gap-1.5 rounded-full bg-yosun px-3 py-1.5 text-xs font-semibold text-white hover:bg-deniz"
          >
            <LocateFixed className="h-3.5 w-3.5" aria-hidden />
            Mevcut konumumu kullan
          </button>
        </div>
        <div className="relative z-0 h-[420px] w-full overflow-hidden rounded-2xl border border-teal-100/80 md:h-[450px]">
          <KonumSeciciYukle
            value={konum}
            onChange={(k) => {
              setKonum(k);
              setKonumHatasi(null);
            }}
          />
        </div>
        {konum ? (
          <p className="text-xs tabular-nums text-yosun">
            Seçilen: {konum.lat.toFixed(5)}, {konum.lng.toFixed(5)}
          </p>
        ) : (
          <p className="text-xs text-bordo">Henüz konum seçilmedi.</p>
        )}
        {konumHatasi ? <p className="text-sm text-bordo">{konumHatasi}</p> : null}
      </div>

      <label className="block space-y-2">
        <span className="text-sm font-medium text-deniz">Hikâyesi / neden özel?</span>
        <textarea
          required
          minLength={20}
          maxLength={2500}
          rows={5}
          value={aciklama}
          onChange={(e) => setAciklama(e.target.value)}
          className="w-full rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2.5 outline-none focus:border-deniz"
          placeholder="Burayı gizli bir keşif yapan şeyi anlat."
        />
      </label>

      <label className="block space-y-2">
        <span className="text-sm font-medium text-deniz">
          Ziyaretçi tüyosu <span className="font-normal text-ink/45">(opsiyonel)</span>
        </span>
        <textarea
          maxLength={500}
          rows={2}
          value={tuyo}
          onChange={(e) => setTuyo(e.target.value)}
          className="w-full rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2.5 outline-none focus:border-deniz"
          placeholder="Akşamüstü rüzgarlı olur, yol topraktır…"
        />
      </label>

      <div className="space-y-2">
        <p className="text-sm font-medium text-deniz">Fotoğraflar</p>
        <FotografAlani dosyalar={fotograflar} onChange={setFotograflar} />
      </div>

      <div className="grid gap-8 md:grid-cols-2">
        <label className="block space-y-2">
          <span className="text-sm font-medium text-deniz">
            Adın <span className="font-normal text-ink/45">(opsiyonel)</span>
          </span>
          <input
            value={ad}
            onChange={(e) => setAd(e.target.value)}
            className="w-full rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2.5 outline-none focus:border-deniz"
          />
        </label>
        <label className="block space-y-2">
          <span className="text-sm font-medium text-deniz">E-posta</span>
          <input
            required
            type="email"
            value={eposta}
            onChange={(e) => setEposta(e.target.value)}
            className="w-full rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2.5 outline-none focus:border-deniz"
            placeholder="onay sonrası haber için"
          />
        </label>
      </div>

      <div className="hidden" aria-hidden>
        <label>
          Site
          <input type="text" name="sirket_sitesi" tabIndex={-1} autoComplete="off" />
        </label>
      </div>

      {TURNSTILE_KEY ? (
        <TurnstileWidget siteKey={TURNSTILE_KEY} onToken={setTurnstile} />
      ) : (
        <p className="text-xs text-ink/40">
          Geliştirme: Turnstile anahtarı yok, doğrulama atlanır.
        </p>
      )}

      {mesaj ? (
        <p className={`text-sm ${durum === "tamam" ? "text-yosun" : "text-bordo"}`}>{mesaj}</p>
      ) : null}

      <button
        type="submit"
        disabled={durum === "gonderiliyor"}
        className="rounded-full bg-deniz px-6 py-2.5 text-sm font-semibold text-white transition hover:bg-deniz-derin disabled:opacity-60"
      >
        {durum === "gonderiliyor" ? "Gönderiliyor…" : "Öneriyi Gönder"}
      </button>
    </form>
  );
}
