"use client";

import { useEffect, useRef, useState } from "react";

export function IstatistikSayac({ deger }: { deger: number }) {
  const [goster, setGoster] = useState(0);
  const kok = useRef<HTMLSpanElement>(null);
  const metin = deger.toLocaleString("tr-TR");

  useEffect(() => {
    const el = kok.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      return;
    }

    let iptal = false;
    let kare = 0;
    let basladi = false;

    const baslat = () => {
      if (basladi || iptal) return;
      basladi = true;
      const bas = performance.now();
      const sure = 900;
      const adim = (t: number) => {
        if (iptal) return;
        const p = Math.min(1, (t - bas) / sure);
        const ease = 1 - (1 - p) ** 3;
        setGoster(Math.round(deger * ease));
        if (p < 1) kare = requestAnimationFrame(adim);
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

  const canli = goster > 0;

  return (
    <span ref={kok} className="relative inline-block tabular-nums">
      <span className={canli ? "invisible" : undefined}>{metin}</span>
      {canli ? (
        <span className="absolute inset-0 motion-reduce:hidden" aria-hidden="true">
          {goster.toLocaleString("tr-TR")}
        </span>
      ) : null}
    </span>
  );
}
