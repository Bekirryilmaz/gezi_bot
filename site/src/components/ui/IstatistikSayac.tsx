"use client";

import { useEffect, useRef } from "react";

/**
 * yon.md 3.8 / 4.3: tek sefer, 900 ms, tabular.
 * Sayaci DOM'da yazar (5.15) — 60 setState yok.
 * Indirgenmis harekette son deger dogrudan (ilk render).
 */
export function IstatistikSayac({ deger }: { deger: number }) {
  const kok = useRef<HTMLSpanElement>(null);
  const sabit = useRef<HTMLSpanElement>(null);
  const canli = useRef<HTMLSpanElement>(null);
  const metin = deger.toLocaleString("tr-TR");

  useEffect(() => {
    const el = kok.current;
    const hedef = sabit.current;
    const overlay = canli.current;
    if (!el || !hedef || !overlay) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      return;
    }

    let iptal = false;
    let kare = 0;
    let basladi = false;

    const baslat = () => {
      if (basladi || iptal) return;
      basladi = true;
      hedef.classList.add("invisible");
      overlay.removeAttribute("hidden");
      const bas = performance.now();
      const sure = 900;
      const adim = (t: number) => {
        if (iptal) return;
        const p = Math.min(1, (t - bas) / sure);
        const ease = 1 - (1 - p) ** 3;
        overlay.textContent = Math.round(deger * ease).toLocaleString("tr-TR");
        if (p < 1) {
          kare = requestAnimationFrame(adim);
          return;
        }
        hedef.classList.remove("invisible");
        overlay.setAttribute("hidden", "");
      };
      kare = requestAnimationFrame(adim);
    };

    const gozlem = new IntersectionObserver(
      ([girdi]) => {
        if (!girdi?.isIntersecting) return;
        gozlem.disconnect();
        baslat();
      },
      { threshold: 0.15 },
    );
    gozlem.observe(el);
    return () => {
      iptal = true;
      cancelAnimationFrame(kare);
      gozlem.disconnect();
    };
  }, [deger]);

  return (
    <span ref={kok} className="relative inline-block tabular-nums">
      <span ref={sabit}>{metin}</span>
      <span
        ref={canli}
        className="absolute inset-0 motion-reduce:hidden"
        aria-hidden="true"
        hidden
      />
    </span>
  );
}
