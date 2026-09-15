export class AramaIstekYoneticisi {
  private sira = 0;
  private denetleyici: AbortController | null = null;

  async yurut<T>(istek: (signal: AbortSignal) => Promise<T>): Promise<T | undefined> {
    this.denetleyici?.abort();
    const sira = ++this.sira;
    const denetleyici = new AbortController();
    this.denetleyici = denetleyici;
    try {
      const sonuc = await istek(denetleyici.signal);
      return sira === this.sira && !denetleyici.signal.aborted ? sonuc : undefined;
    } catch (hata) {
      if (
        denetleyici.signal.aborted ||
        (hata instanceof DOMException && hata.name === "AbortError")
      ) {
        return undefined;
      }
      throw hata;
    }
  }

  iptal(): void {
    this.sira += 1;
    this.denetleyici?.abort();
    this.denetleyici = null;
  }
}
