"use client";

import { useEffect, useRef, useState } from "react";

import { aramaGetir, apiDurumu } from "@/lib/api";
import { AramaIstekYoneticisi } from "@/lib/arama-istek";
import type { AramaCevabi, AramaFiltreDurumu, VeriDurumu } from "@/lib/types";

export function useAramaSonuclari(
  q: string,
  filtreler: AramaFiltreDurumu,
  gecikmeMs = 250,
) {
  const yonetici = useRef<AramaIstekYoneticisi | null>(null);
  if (yonetici.current === null) yonetici.current = new AramaIstekYoneticisi();
  const [cevap, setCevap] = useState<AramaCevabi | null>(null);
  const [durum, setDurum] = useState<VeriDurumu>(q.trim() ? "loading" : "empty");
  const [hata, setHata] = useState<unknown>(null);
  const filtreAnahtari = JSON.stringify(filtreler);

  useEffect(() => {
    if (!q.trim()) {
      yonetici.current?.iptal();
      return;
    }
    const zamanlayici = window.setTimeout(() => {
      setDurum("loading");
      setHata(null);
      void yonetici.current
        ?.yurut((signal) => aramaGetir(q, filtreler, { signal }))
        .then((yeniCevap) => {
          if (!yeniCevap) return;
          setCevap(yeniCevap);
          setDurum(yeniCevap.sonuclar.length === 0 ? "empty" : "ready");
        })
        .catch((neden: unknown) => {
          setHata(neden);
          setDurum(apiDurumu(neden));
        });
    }, gecikmeMs);
    return () => window.clearTimeout(zamanlayici);
    // filtreAnahtari, semantik olarak ayni filtre nesnesinin gereksiz isteklerini onler.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q, filtreAnahtari, gecikmeMs]);

  useEffect(() => () => yonetici.current?.iptal(), []);
  return q.trim()
    ? { cevap, durum, hata }
    : { cevap: null, durum: "empty" as const, hata: null };
}
