"use client";

import { type ReactNode, useEffect, useRef } from "react";

type Ozellik = {
  children: ReactNode;
  delay?: number;
  className?: string;
};

function useBirKezGorunur(esik: number) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      el.dataset.gorunur = "1";
      return;
    }
    const gozlem = new IntersectionObserver(
      ([girdi]) => {
        if (!girdi?.isIntersecting) return;
        gozlem.disconnect();
        el.dataset.gorunur = "1";
      },
      { threshold: esik },
    );
    gozlem.observe(el);
    return () => gozlem.disconnect();
  }, [esik]);

  return ref;
}

/**
 * Kaydirma ile bir kez gorunen reveal — CSS, motion yok (Lighthouse TBT).
 */
export function Reveal({ children, delay = 0, className }: Ozellik) {
  const ref = useBirKezGorunur(0.18);
  return (
    <div
      ref={ref}
      data-reveal
      className={className}
      style={delay ? { ["--reveal-gecikme" as string]: `${delay}s` } : undefined}
    >
      {children}
    </div>
  );
}

export function RevealListe({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  const ref = useBirKezGorunur(0.12);
  return (
    <div ref={ref} data-reveal-liste className={className}>
      {children}
    </div>
  );
}

export function RevealOge({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div data-reveal-oge className={className}>
      {children}
    </div>
  );
}
