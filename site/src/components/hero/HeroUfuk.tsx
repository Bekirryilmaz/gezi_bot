"use client";

import { useEffect, useRef } from "react";
import { SCRUB_PAY_MASAUSTU, SCRUB_PAY_MOBIL } from "@/lib/hero-kapak";

/**
 * yon-v2 2.3 — prosedurel ufuk. Fotoğraf degismez.
 * rAF icinde setState yok; ref yalniz effect'te okunur.
 */
export function HeroUfuk({ className }: { className?: string }) {
  const kanvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const kanvas = kanvasRef.current;
    if (!kanvas) return;

    const azalt = window.matchMedia("(prefers-reduced-motion: reduce)");
    const baglanti = (
      navigator as Navigator & {
        connection?: { saveData?: boolean; effectiveType?: string };
      }
    ).connection;
    const agKisitli =
      Boolean(baglanti?.saveData) ||
      baglanti?.effectiveType === "2g" ||
      baglanti?.effectiveType === "3g";
    if (azalt.matches || agKisitli) return;

    const ctx = kanvas.getContext("2d", { alpha: true });
    if (!ctx) return;

    let iptal = false;
    let raf = 0;
    let ekranda = true;
    let calisiyor = false;
    let sonAn = 0;
    let fazUzak = 0;
    let fazOrta = 0;
    let fazYakin = 0;
    let isik = 0;
    let scrub = 0;

    let kutuW = 0;
    let kutuH = 0;
    let heroUst = 0;

    const olcu = () => {
      const kutu = kanvas.parentElement;
      if (!kutu) return;
      kutuW = kutu.clientWidth;
      kutuH = kutu.clientHeight;
      heroUst = kutu.getBoundingClientRect().top + window.scrollY;
      const oran = Math.min(window.devicePixelRatio || 1, 2);
      const w = Math.max(1, Math.round(kutuW * oran));
      const h = Math.max(1, Math.round(kutuH * oran));
      if (kanvas.width !== w || kanvas.height !== h) {
        kanvas.width = w;
        kanvas.height = h;
      }
    };

    const scrubOku = () => {
      const pay = window.matchMedia("(min-width: 768px)").matches
        ? SCRUB_PAY_MASAUSTU
        : SCRUB_PAY_MOBIL;
      scrub = Math.min(1, Math.max(0, (window.scrollY - heroUst) / pay));
    };

    let sonCizim = 0;
    const MIN_DT = 33;

    const dalga = (y0: number, genlik: number, faz: number, boy: number) => {
      const w = kanvas.width;
      const h = kanvas.height;
      ctx.beginPath();
      ctx.moveTo(0, h);
      ctx.lineTo(0, y0);
      const adim = Math.max(10, Math.round(w / 72));
      for (let x = 0; x <= w; x += adim) {
        const y =
          y0 +
          Math.sin(x / boy + faz) * genlik +
          Math.sin(x / (boy * 1.7) + faz * 0.65) * genlik * 0.32;
        ctx.lineTo(x, y);
      }
      ctx.lineTo(w, h);
      ctx.closePath();
    };

    const ciz = (an: number) => {
      if (iptal) return;
      if (an - sonCizim < MIN_DT) {
        if (ekranda && !document.hidden) raf = requestAnimationFrame(ciz);
        return;
      }
      sonCizim = an;
      const dt = sonAn ? Math.min(an - sonAn, 48) : 16;
      sonAn = an;

      fazUzak += dt * 0.00055;
      fazOrta += dt * 0.00088;
      fazYakin += dt * 0.00125;
      isik = (isik + dt * 0.00018) % 1;

      const w = kanvas.width;
      const h = kanvas.height;
      ctx.clearRect(0, 0, w, h);

      const ufuk = h * (0.42 + scrub * 0.04);
      const px = h / Math.max(kutuH, 1);
      const genlik = 1 + scrub * 0.25;

      const gok = ctx.createLinearGradient(0, 0, 0, ufuk);
      gok.addColorStop(0, "rgba(46, 4, 5, 0.22)");
      gok.addColorStop(1, "rgba(46, 4, 5, 0.02)");
      ctx.fillStyle = gok;
      ctx.fillRect(0, 0, w, ufuk + 8);

      dalga(ufuk + h * 0.05, 8 * px * genlik, fazUzak, w / 2.2);
      ctx.fillStyle = "rgba(46, 4, 5, 0.3)";
      ctx.fill();

      dalga(ufuk + h * 0.14, 12 * px * genlik, fazOrta, w / 1.55);
      ctx.fillStyle = "rgba(108, 0, 0, 0.24)";
      ctx.fill();

      dalga(ufuk + h * 0.26, 16 * px * genlik, fazYakin, w / 1.15);
      ctx.fillStyle = "rgba(20, 33, 38, 0.34)";
      ctx.fill();

      ctx.strokeStyle = "rgba(244, 239, 231, 0.5)";
      ctx.lineWidth = Math.max(1, h / 700);
      ctx.beginPath();
      ctx.moveTo(0, ufuk);
      ctx.lineTo(w, ufuk);
      ctx.stroke();

      const dugumler: Array<[number, number]> = [
        [0.16, 0.018],
        [0.34, -0.01],
        [0.55, 0.014],
        [0.73, -0.008],
        [0.9, 0.02],
      ];
      ctx.strokeStyle = "rgba(10, 77, 92, 0.55)";
      ctx.lineWidth = Math.max(1, h / 900);
      ctx.beginPath();
      for (let i = 0; i < dugumler.length; i++) {
        const nokta = dugumler[i];
        if (!nokta) continue;
        const x = nokta[0] * w;
        const y = ufuk + nokta[1] * h;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      for (let i = 0; i < dugumler.length; i++) {
        const nokta = dugumler[i];
        if (!nokta) continue;
        if (scrub * 1.15 + 0.4 < i / dugumler.length) continue;
        ctx.fillStyle = "rgba(251, 248, 243, 0.88)";
        ctx.beginPath();
        ctx.arc(nokta[0] * w, ufuk + nokta[1] * h, Math.max(2, h / 280), 0, Math.PI * 2);
        ctx.fill();
      }

      const bx = 0.55 * w;
      const by = ufuk + 0.014 * h;
      const nabiz = 0.55 + 0.45 * Math.sin(an / 1800);

      const parlama = ctx.createRadialGradient(bx, by, 0, bx, by, h * 0.075);
      parlama.addColorStop(0, `rgba(242, 177, 56, ${0.38 * nabiz})`);
      parlama.addColorStop(0.45, `rgba(214, 64, 44, ${0.2 * nabiz})`);
      parlama.addColorStop(1, "rgba(214, 64, 44, 0)");
      ctx.fillStyle = parlama;
      ctx.beginPath();
      ctx.arc(bx, by, h * 0.075, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = `rgba(214, 64, 44, ${0.72 + 0.28 * nabiz})`;
      ctx.beginPath();
      ctx.arc(bx, by, Math.max(3, h / 220), 0, Math.PI * 2);
      ctx.fill();

      const lx = ((isik + scrub * 0.15) % 1) * w;
      const isikG = ctx.createLinearGradient(lx - w * 0.22, 0, lx + w * 0.22, h);
      isikG.addColorStop(0, "rgba(251, 248, 243, 0)");
      isikG.addColorStop(0.5, "rgba(251, 248, 243, 0.08)");
      isikG.addColorStop(1, "rgba(251, 248, 243, 0)");
      ctx.fillStyle = isikG;
      ctx.fillRect(0, 0, w, h);

      if (ekranda && !document.hidden) {
        raf = requestAnimationFrame(ciz);
        return;
      }
      calisiyor = false;
    };

    const durdur = () => {
      cancelAnimationFrame(raf);
      calisiyor = false;
      sonAn = 0;
      sonCizim = 0;
    };

    let izinli = false;
    const izinVer = () => {
      if (izinli) return;
      izinli = true;
      baslat();
    };

    const baslat = () => {
      if (!izinli || calisiyor || iptal || !ekranda || document.hidden) return;
      const kick = () => {
        if (calisiyor || iptal || !ekranda || document.hidden) return;
        calisiyor = true;
        sonAn = 0;
        raf = requestAnimationFrame(ciz);
      };
      if ("requestIdleCallback" in window) {
        requestIdleCallback(kick, { timeout: 400 });
      } else {
        setTimeout(kick, 1);
      }
    };

    const sekme = () => {
      if (document.hidden) durdur();
      else baslat();
    };

    const tercihDegisti = (olay: MediaQueryListEvent) => {
      if (!olay.matches) return;
      iptal = true;
      durdur();
      ctx.clearRect(0, 0, kanvas.width, kanvas.height);
    };

    olcu();
    scrubOku();

    const gozlem = new IntersectionObserver(
      ([girdi]) => {
        ekranda = Boolean(girdi?.isIntersecting);
        if (ekranda) baslat();
        else durdur();
      },
      { threshold: 0 },
    );
    gozlem.observe(kanvas);

    const olcer = new ResizeObserver(olcu);
    if (kanvas.parentElement) olcer.observe(kanvas.parentElement);

    window.addEventListener("scroll", scrubOku, { passive: true });
    window.addEventListener("scroll", izinVer, { passive: true, once: true });
    document.addEventListener("visibilitychange", sekme);
    azalt.addEventListener("change", tercihDegisti);
    const gecikme = window.setTimeout(izinVer, 8000);

    return () => {
      iptal = true;
      durdur();
      gozlem.disconnect();
      olcer.disconnect();
      window.clearTimeout(gecikme);
      window.removeEventListener("scroll", scrubOku);
      window.removeEventListener("scroll", izinVer);
      document.removeEventListener("visibilitychange", sekme);
      azalt.removeEventListener("change", tercihDegisti);
    };
  }, []);

  return (
    <canvas ref={kanvasRef} className={className} data-hero-ufuk aria-hidden="true" />
  );
}
