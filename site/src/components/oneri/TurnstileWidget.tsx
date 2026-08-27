"use client";

import { useEffect, useRef } from "react";

type Props = {
  siteKey: string;
  onToken: (jeton: string) => void;
};

type TurnstileApi = {
  render: (
    el: HTMLElement,
    opts: { sitekey: string; callback: (t: string) => void; theme?: string },
  ) => string;
  remove: (id: string) => void;
};

declare global {
  interface Window {
    turnstile?: TurnstileApi;
  }
}

export function TurnstileWidget({ siteKey, onToken }: Props) {
  const kutuRef = useRef<HTMLDivElement>(null);
  const widgetId = useRef<string | null>(null);
  const onTokenRef = useRef(onToken);

  useEffect(() => {
    onTokenRef.current = onToken;
  }, [onToken]);

  useEffect(() => {
    let iptal = false;

    function yukle() {
      const kutu = kutuRef.current;
      const api = window.turnstile;
      if (!kutu || !api || iptal || widgetId.current) return;
      widgetId.current = api.render(kutu, {
        sitekey: siteKey,
        theme: "light",
        callback: (jeton) => onTokenRef.current(jeton),
      });
    }

    if (window.turnstile) {
      yukle();
      return () => {
        iptal = true;
        if (widgetId.current && window.turnstile) {
          window.turnstile.remove(widgetId.current);
        }
      };
    }

    const mevcut = document.querySelector<HTMLScriptElement>(
      "script[data-turnstile]",
    );
    if (mevcut) {
      mevcut.addEventListener("load", yukle);
      return () => {
        iptal = true;
        mevcut.removeEventListener("load", yukle);
      };
    }

    const script = document.createElement("script");
    script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    script.async = true;
    script.dataset.turnstile = "1";
    script.addEventListener("load", yukle);
    document.body.appendChild(script);
    return () => {
      iptal = true;
      script.removeEventListener("load", yukle);
      if (widgetId.current && window.turnstile) {
        window.turnstile.remove(widgetId.current);
      }
    };
  }, [siteKey]);

  return <div ref={kutuRef} className="min-h-[65px]" />;
}
