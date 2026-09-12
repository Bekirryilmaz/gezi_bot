"use client";

import { useEffect, useRef } from "react";
import { cn } from "cn";

export function KesilenAyrac({ className }: { className?: string }) {
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
      { threshold: 0.35 },
    );
    gozlem.observe(el);
    return () => gozlem.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      data-kesik-ayrac
      className={cn("flex items-center", className)}
      aria-hidden="true"
    >
      <span data-cizgi="sol" className="bg-bordo/12 h-px flex-1" />
      <span className="w-1.5 shrink-0" />
      <span data-cizgi="sag" className="bg-bordo/12 h-px flex-1" />
    </div>
  );
}
