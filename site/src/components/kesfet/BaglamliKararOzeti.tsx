"use client";

import { useEffect, useState } from "react";

import { kamusalYerDetayiniDegerlendir } from "@/lib/api";
import type { KamusalYerDetayi, KararBaglami } from "@/lib/types";

type SakliBaglam = { donus?: string; baglam?: KararBaglami };

const DENEYIM_ETIKETI: Record<string, string> = {
  sohbet: "sohbet",
  sohbet_uygunlugu: "sohbet",
  sessiz_ortam: "sakinlik",
  aile_uygunlugu: "aile",
  cocuk_uygunlugu: "çocuk",
  calisma_uygunlugu: "çalışma",
  manzara: "manzara",
};

function deneyimCumlesi(ilgili: string | null | undefined, yedek: string): string {
  const etiket = DENEYIM_ETIKETI[ilgili ?? ""];
  if (!etiket) return yedek;
  return `${etiket} deneyimi açısından destekleyici sinyal var.`;
}

export function BaglamliKararOzeti({
  yerId,
  ilkDetay,
}: {
  yerId: string;
  ilkDetay: KamusalYerDetayi;
}) {
  const [detay, setDetay] = useState(ilkDetay);

  useEffect(() => {
    const denetleyici = new AbortController();
    const sakli = window.sessionStorage.getItem("kesfet:aktif-baglam");
    if (!sakli) return () => denetleyici.abort();
    try {
      const veri = JSON.parse(sakli) as SakliBaglam;
      const donus = new URLSearchParams(window.location.search).get("donus");
      if (!veri.baglam || !donus || veri.donus !== donus)
        return () => denetleyici.abort();
      void kamusalYerDetayiniDegerlendir(yerId, veri.baglam, denetleyici.signal)
        .then(setDetay)
        .catch(() => undefined);
    } catch {
      /* Geçersiz oturum verisi kişisel karar üretmez. */
    }
    return () => denetleyici.abort();
  }, [yerId]);

  const karar = detay.karar_sonucu;
  const dogrulananlar = (karar?.gerekceler ?? []).filter((gerekce) =>
    ["zorunlu_kosul_dogrulandi", "amac_destekleniyor", "tercih_destekleniyor"].includes(
      gerekce.kod,
    ),
  );
  const deneyim = (karar?.gerekceler ?? []).filter(
    (gerekce) => gerekce.kod === "deneyim_sinyali_destekliyor",
  );
  const henuz = [
    ...(karar?.bilinmeyenler ?? []),
    ...(karar?.onemli_odunler ?? []).filter(
      (gerekce) => gerekce.kod === "tercih_bilinmiyor",
    ),
  ];
  return (
    <div className="space-y-10">
      <section aria-labelledby="dogrulanan-baslik">
        <h2 id="dogrulanan-baslik" className="yazi-alt text-bordo">
          Doğruladığımız
        </h2>
        {dogrulananlar.length ? (
          <ul className="text-ink/80 mt-4 grid gap-2">
            {dogrulananlar.map((gerekce) => (
              <li key={`${gerekce.kod}-${gerekce.ilgili_kosul ?? ""}`}>
                {gerekce.mesaj}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-ink/65 mt-4">
            Bu sayfa doğrudan açıldı; kişisel uygunluk iddiası kurmuyoruz. Keşfet’teki
            ziyaret bağlamın varsa değerlendirme aynı Karar Motorundan gelir.
          </p>
        )}
      </section>
      <section aria-labelledby="deneyim-baslik">
        <h2 id="deneyim-baslik" className="yazi-alt text-bordo">
          Deneyim sinyali
        </h2>
        {deneyim.length ? (
          <ul className="text-ink/80 mt-4 grid gap-2">
            {deneyim.map((gerekce) => (
              <li key={`${gerekce.kod}-${gerekce.ilgili_kosul ?? ""}`}>
                {deneyimCumlesi(gerekce.ilgili_kosul, gerekce.mesaj)}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-ink/65 mt-4">
            Bu bağlam için paylaşılabilir bir deneyim sinyali yok; bu yokluk bir puan
            değildir.
          </p>
        )}
      </section>
      <section aria-labelledby="sinir-baslik">
        <h2 id="sinir-baslik" className="yazi-alt text-bordo">
          Henüz doğrulayamadığımız
        </h2>
        {henuz.length || detay.kritik_bilinmeyenler.length ? (
          <ul className="border-deniz/15 mt-4 grid gap-2 border-l-2 pl-4">
            {henuz.map((oge) => (
              <li key={`${oge.kod}-${oge.ilgili_kosul ?? ""}`}>{oge.mesaj}</li>
            ))}
            {detay.kritik_bilinmeyenler.map((bilinmeyen) => (
              <li key={bilinmeyen}>{bilinmeyen}</li>
            ))}
          </ul>
        ) : (
          <p className="text-ink/65 mt-4">
            Bu bağlam için yayımlanmış önemli bir ödün bulunmuyor; bu, ödün olmadığı
            anlamına gelmez.
          </p>
        )}
      </section>
    </div>
  );
}
