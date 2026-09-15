"use client";

import { useEffect, useState } from "react";

import { kamusalYerDetayiniDegerlendir } from "@/lib/api";
import type { KamusalYerDetayi, KararBaglami } from "@/lib/types";

type SakliBaglam = { donus?: string; baglam?: KararBaglami };

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
  return (
    <div className="space-y-10">
      <section aria-labelledby="neden-baslik">
        <h2 id="neden-baslik" className="yazi-alt text-bordo">
          Bu ziyaret için neden düşünülebilir?
        </h2>
        {karar?.gerekceler.length ? (
          <ul className="text-ink/80 mt-4 grid gap-2">
            {karar.gerekceler.map((gerekce) => (
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
      <section aria-labelledby="sinir-baslik">
        <h2 id="sinir-baslik" className="yazi-alt text-bordo">
          Önemli ödün ve bilinmeyenler
        </h2>
        {karar?.onemli_odunler.length ? (
          <ul className="mt-4 grid gap-2">
            {karar.onemli_odunler.map((oge) => (
              <li key={oge.kod}>{oge.mesaj}</li>
            ))}
          </ul>
        ) : (
          <p className="text-ink/65 mt-4">
            Bu bağlam için yayımlanmış önemli bir ödün bulunmuyor; bu, ödün olmadığı
            anlamına gelmez.
          </p>
        )}
        <ul className="border-deniz/15 mt-4 grid gap-2 border-l-2 pl-4">
          {detay.kritik_bilinmeyenler.map((bilinmeyen) => (
            <li key={bilinmeyen}>{bilinmeyen}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
