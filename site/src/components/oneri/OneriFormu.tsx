"use client";

import { useCallback, useState } from "react";
import { Controller, useForm, type Resolver } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { LocateFixed } from "lucide-react";
import { TURKIYE_SEHIRLERI } from "@/data/cities";
import {
  ONERI_KATEGORILERI,
  type PlaceSuggestionCategory,
} from "@/types/placeSuggestion";
import {
  ARABA_ERISIM_SECENEKLERI,
  YOL_DURUMU_SECENEKLERI,
  oneriFormSema,
  type OneriFormSema,
} from "@/types/suggestion";
import { FotografAlani } from "@/components/oneri/FotografAlani";
import { KonumSeciciYukle } from "@/components/oneri/KonumSeciciYukle";
import { SeciciMenu } from "@/components/oneri/SeciciMenu";
import { TurnstileWidget } from "@/components/oneri/TurnstileWidget";

const TURNSTILE_KEY = process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY ?? "";
const BASARI_MESAJI = "Öneriniz incelenmek üzere ekibimize ulaştı!";
const GIRDI_SINIFI =
  "min-h-[44px] w-full max-w-full rounded-xl border border-[var(--cizgi)] bg-white px-3 py-2.5 text-ink outline-none focus:border-deniz";

type Durum = "idle" | "gonderiliyor" | "tamam" | "hata";

function ZorunluYildiz() {
  return <span className="text-red-500">*</span>;
}

function AlanHatasi({ mesaj }: { mesaj?: string }) {
  if (!mesaj) return null;
  return <p className="text-sm text-red-500">{mesaj}</p>;
}

export function OneriFormu() {
  const [turnstile, setTurnstile] = useState("");
  const [konumHatasi, setKonumHatasi] = useState<string | null>(null);
  const [durum, setDurum] = useState<Durum>("idle");
  const [mesaj, setMesaj] = useState<string | null>(null);

  const {
    register,
    control,
    handleSubmit,
    setValue,
    watch,
    reset,
    formState: { errors },
  } = useForm<OneriFormSema>({
    resolver: zodResolver(oneriFormSema) as Resolver<OneriFormSema>,
    defaultValues: {
      title: "",
      category: "",
      city: "",
      district: "",
      directions: "",
      transportation: {
        walkingDistance: "",
        roadCondition: "",
        publicTransit: "",
      },
      description: "",
      images: [],
      submitterEmail: "",
      specialTip: "",
    },
  });

  const konum = watch("coordinates");

  const mevcutKonum = useCallback(() => {
    if (!navigator.geolocation) {
      setKonumHatasi("Tarayıcın konum paylaşımını desteklemiyor.");
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setValue(
          "coordinates",
          { lat: pos.coords.latitude, lng: pos.coords.longitude },
          { shouldValidate: true, shouldDirty: true },
        );
        setKonumHatasi(null);
      },
      () => setKonumHatasi("Konum alınamadı. Haritadan pin bırakabilirsin."),
      { enableHighAccuracy: true, timeout: 12000 },
    );
  }, [setValue]);

  async function gonder(degerler: OneriFormSema, olay: React.BaseSyntheticEvent) {
    setMesaj(null);
    const formEl = olay.target as HTMLFormElement;
    const honeypot = new FormData(formEl).get("sirket_sitesi");

    if (TURNSTILE_KEY && !turnstile) {
      setDurum("hata");
      setMesaj("Doğrulamayı tamamla.");
      return;
    }

    if (!degerler.coordinates) {
      setDurum("hata");
      setMesaj("Haritadan konum seç.");
      return;
    }

    const govde = new FormData();
    govde.set("baslik", degerler.title.trim());
    govde.set("kategori", degerler.category);
    govde.set("sehir", degerler.city.trim());
    govde.set("ilce", degerler.district.trim());
    govde.set("aciklama", degerler.description.trim());
    govde.set("adres_tarifi", degerler.directions.trim());
    govde.set("araba_erisimi", degerler.transportation.carAccess);
    govde.set("yurume_mesafesi", degerler.transportation.walkingDistance.trim());
    govde.set("yol_durumu", degerler.transportation.roadCondition.trim());
    govde.set("toplu_tasima", degerler.transportation.publicTransit.trim());
    govde.set("gonderen_eposta", degerler.submitterEmail.trim());
    govde.set("enlem", String(degerler.coordinates.lat));
    govde.set("boylam", String(degerler.coordinates.lng));
    const tuyo = degerler.specialTip?.trim();
    if (tuyo) govde.set("ziyaretci_tuyosu", tuyo);
    if (turnstile) govde.set("turnstile_jetonu", turnstile);
    if (typeof honeypot === "string" && honeypot.trim()) {
      govde.set("sirket_sitesi", honeypot);
    }
    for (const dosya of degerler.images) {
      if (dosya instanceof File) govde.append("fotograflar", dosya);
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
      reset();
      setTurnstile("");
    } catch {
      setDurum("hata");
      setMesaj("Bağlantı kurulamadı. Biraz sonra tekrar dene.");
    }
  }

  return (
    <form
      noValidate
      onSubmit={handleSubmit((degerler, olay) => {
        if (olay) void gonder(degerler, olay);
      })}
      className="space-y-8 overflow-visible"
    >
      <div className="relative z-20 grid grid-cols-1 gap-6 md:grid-cols-2">
        <label className="block space-y-2">
          <span className="text-sm font-medium text-deniz">
            Mekan adı <ZorunluYildiz />
          </span>
          <input
            maxLength={200}
            className={GIRDI_SINIFI}
            placeholder="Örn. Gizli Çınaraltı"
            {...register("title")}
          />
          <AlanHatasi mesaj={errors.title?.message} />
        </label>
        <Controller
          name="category"
          control={control}
          render={({ field }) => (
            <SeciciMenu
              etiket="Kategori"
              yerTutucu="Kategori seç"
              deger={field.value}
              gerekli
              hata={errors.category?.message}
              secenekler={ONERI_KATEGORILERI}
              onSec={(id) => field.onChange(id as PlaceSuggestionCategory)}
            />
          )}
        />
      </div>

      <div className="relative z-10 grid grid-cols-1 gap-6 md:grid-cols-2">
        <Controller
          name="city"
          control={control}
          render={({ field }) => (
            <SeciciMenu
              etiket="Şehir"
              yerTutucu="Şehir seç veya yaz"
              deger={field.value}
              gerekli
              aranabilir
              hata={errors.city?.message}
              secenekler={TURKIYE_SEHIRLERI.map((s) => ({
                id: s.name,
                etiket: s.name,
              }))}
              onSec={(id) => field.onChange(id)}
            />
          )}
        />
        <label className="block space-y-2">
          <span className="text-sm font-medium text-deniz">
            İlçe <ZorunluYildiz />
          </span>
          <input
            className={GIRDI_SINIFI}
            placeholder="Atakum"
            {...register("district")}
          />
          <AlanHatasi mesaj={errors.district?.message} />
        </label>
      </div>

      <div className="relative z-0 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-sm font-medium text-deniz">
              Konum <ZorunluYildiz />
            </p>
            <p className="text-xs text-ink/55">
              Haritaya tıkla veya pini sürükle. Koordinat seçilmeden form gitmez.
            </p>
          </div>
          <button
            type="button"
            onClick={mevcutKonum}
            className="inline-flex min-h-[44px] items-center gap-1.5 rounded-full bg-yosun px-3 py-2 text-xs font-semibold text-white hover:bg-deniz"
          >
            <LocateFixed className="h-3.5 w-3.5" aria-hidden />
            Mevcut konumumu kullan
          </button>
        </div>
        <div className="relative z-0 h-[280px] w-full max-w-full overflow-hidden rounded-2xl border border-teal-100 sm:h-[360px] md:h-[450px]">
          <Controller
            name="coordinates"
            control={control}
            render={({ field }) => (
              <KonumSeciciYukle
                value={field.value ?? null}
                onChange={(k) => {
                  field.onChange(k);
                  setKonumHatasi(null);
                }}
              />
            )}
          />
        </div>
        {konum ? (
          <p className="text-xs tabular-nums text-yosun">
            Seçilen: {konum.lat.toFixed(5)}, {konum.lng.toFixed(5)}
          </p>
        ) : (
          <p className="text-xs text-ink/55">Henüz konum seçilmedi.</p>
        )}
        <AlanHatasi mesaj={errors.coordinates?.message || errors.coordinates?.lat?.message} />
        {konumHatasi ? <p className="text-sm text-red-500">{konumHatasi}</p> : null}
      </div>

      <label className="block space-y-2">
        <span className="text-sm font-medium text-deniz">
          Adres tarifi / nasıl gidilir <ZorunluYildiz />
        </span>
        <textarea
          rows={4}
          maxLength={1500}
          className={GIRDI_SINIFI}
          placeholder="Örn. Atakum sahil yolundan batıya 3 km, kırmızı tabeladan sola sap, 400 m toprak yol."
          {...register("directions")}
        />
        <AlanHatasi mesaj={errors.directions?.message} />
      </label>

      <div className="space-y-4 rounded-2xl border border-teal-100 bg-white/60 p-4 md:p-5">
        <p className="text-sm font-medium text-deniz">
          Ulaşım bilgisi <ZorunluYildiz />
        </p>
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <Controller
            name="transportation.carAccess"
            control={control}
            render={({ field }) => (
              <SeciciMenu
                etiket="Araçla ulaşım"
                yerTutucu="Durumu seç"
                deger={field.value ?? ""}
                gerekli
                hata={errors.transportation?.carAccess?.message}
                secenekler={ARABA_ERISIM_SECENEKLERI}
                onSec={(id) => field.onChange(id)}
              />
            )}
          />
          <Controller
            name="transportation.roadCondition"
            control={control}
            render={({ field }) => (
              <SeciciMenu
                etiket="Yol tipi"
                yerTutucu="Asfalt / toprak…"
                deger={field.value}
                gerekli
                hata={errors.transportation?.roadCondition?.message}
                secenekler={YOL_DURUMU_SECENEKLERI.map((s) => ({
                  id: s.id,
                  etiket: s.etiket,
                }))}
                onSec={(id) => field.onChange(id)}
              />
            )}
          />
        </div>
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <label className="block space-y-2">
            <span className="text-sm font-medium text-deniz">
              Yürüme mesafesi / süresi <ZorunluYildiz />
            </span>
            <input
              className={GIRDI_SINIFI}
              placeholder="Örn. 5 dk yürüme"
              {...register("transportation.walkingDistance")}
            />
            <AlanHatasi mesaj={errors.transportation?.walkingDistance?.message} />
          </label>
          <label className="block space-y-2">
            <span className="text-sm font-medium text-deniz">
              Toplu taşıma <ZorunluYildiz />
            </span>
            <input
              className={GIRDI_SINIFI}
              placeholder="Örn. 22 numaralı otobüs, duraktan 10 dk"
              {...register("transportation.publicTransit")}
            />
            <AlanHatasi mesaj={errors.transportation?.publicTransit?.message} />
          </label>
        </div>
      </div>

      <label className="block space-y-2">
        <span className="text-sm font-medium text-deniz">
          Hikâyesi / neden özel? <ZorunluYildiz />
        </span>
        <textarea
          maxLength={2500}
          rows={5}
          className={GIRDI_SINIFI}
          placeholder="Burayı gizli bir keşif yapan şeyi anlat."
          {...register("description")}
        />
        <AlanHatasi mesaj={errors.description?.message} />
      </label>

      <label className="block space-y-2">
        <span className="text-sm font-medium text-deniz">
          Ziyaretçi tüyosu{" "}
          <span className="rounded-full bg-kopuk px-2 py-0.5 text-xs font-normal text-ink/55">
            (İsteğe Bağlı)
          </span>
        </span>
        <textarea
          maxLength={500}
          rows={2}
          className={GIRDI_SINIFI}
          placeholder="Akşamüstü rüzgarlı olur, yol topraktır…"
          {...register("specialTip")}
        />
        <AlanHatasi mesaj={errors.specialTip?.message} />
      </label>

      <div className="space-y-2">
        <p className="text-sm font-medium text-deniz">
          Fotoğraflar <ZorunluYildiz />
        </p>
        <Controller
          name="images"
          control={control}
          render={({ field }) => (
            <FotografAlani
              dosyalar={field.value.filter((d): d is File => d instanceof File)}
              onChange={field.onChange}
              hata={errors.images?.message}
            />
          )}
        />
      </div>

      <label className="block space-y-2">
        <span className="text-sm font-medium text-deniz">
          E-posta <ZorunluYildiz />
        </span>
        <input
          type="email"
          className={GIRDI_SINIFI}
          placeholder="onay sonrası haber için"
          {...register("submitterEmail")}
        />
        <AlanHatasi mesaj={errors.submitterEmail?.message} />
      </label>

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
        className="inline-flex min-h-[44px] w-full items-center justify-center rounded-full bg-deniz px-6 py-2.5 text-sm font-semibold text-white transition hover:bg-deniz-derin disabled:opacity-60 sm:w-auto"
      >
        {durum === "gonderiliyor" ? "Gönderiliyor…" : "Öneriyi Gönder"}
      </button>
    </form>
  );
}
