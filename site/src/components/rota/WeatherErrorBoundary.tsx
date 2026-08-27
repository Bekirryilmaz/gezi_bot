"use client";

import { Component, type ErrorInfo, type ReactNode } from "react";

type Props = {
  children: ReactNode;
};

type State = {
  hata: Error | null;
};

export class WeatherErrorBoundary extends Component<Props, State> {
  state: State = { hata: null };

  static getDerivedStateFromError(hata: Error): State {
    return { hata };
  }

  componentDidCatch(hata: Error, bilgi: ErrorInfo) {
    console.error("Hava durumu bileşeni hata verdi:", hata, bilgi);
  }

  render() {
    if (this.state.hata) {
      return (
        <div
          role="alert"
          className="rounded-2xl border border-bordo/20 bg-white/70 px-5 py-4 text-sm text-ink/70"
        >
          Hava durumu şu an gösterilemiyor. Rotanı yine de kurabilirsin.
        </div>
      );
    }
    return this.props.children;
  }
}
