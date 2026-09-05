# Site — Şamandıra

Next.js 16 (App Router) + React 19 + Tailwind 4. Marka: **Şamandıra**
(Alegre Group). Fontlar: Sora + Fraunces. Tema tokenları: `deniz` / `kopuk` /
`kumsal` / `gunes`.

API ayakta olmadan keşif ve rota çalışmaz. Çalıştırma kaynağı: repo kökündeki
[`calis.txt`](../calis.txt).

## Çalıştırma

1. PostgreSQL (`C:\PostgreSQL`) ve aktarılmış Samsun verisi
2. API — repo kökünden, port **8125**:

```text
.\.venv_test\Scripts\python.exe -m uvicorn sunucu.api.uygulama:uygulama --host 127.0.0.1 --port 8125
```

3. Site — port **3000**:

```text
cd site
npm install
npm run dev -- --port 3000
```

Tarayıcı: http://localhost:3000

`site/.env.local` (git’te yok; bir kez oluştur):

```text
NEXT_PUBLIC_API_URL=http://127.0.0.1:8125
```

`next.config.ts` tarayıcı isteklerini `/backend/:path*` → FastAPI’ye rewrite
eder. Sunucu bileşenleri `NEXT_PUBLIC_API_URL` ile doğrudan 8125’e gider
(`site/src/lib/api.ts`).

CORS: API tarafında `API_IZINLI_ORIGINLER` varsayılanı `http://localhost:3000`.

## Sayfalar (şu an)

| Yol | Açıklama |
|-----|----------|
| `/` | Hero + Keşfet / Bölgeler / Rota |
| `/sehir/[anahtar]` | Keşif listesi, kategori chip (konaklama yok) |
| `/yer/[id]` | Tanıtım + duygu özeti + yan bilgiler (UUID) |
| `/sehir/[anahtar]/bolgeler` | Şehir + ilçe profilleri |
| `/sehir/[anahtar]/rota` | Rota sihirbazı |

Sihirbaz: senaryo → tercihler (gün 1–5, 6 eksen, ucuz/sakin) → (senaryo 2 ise)
alternatifler → sonuç. Site Senaryo 2’de
`POST /rotalar/olustur-alternatifler` ve
`POST /rotalar/{id}/konaklama-bolgesi-oner` kullanır.

Hedef URL’ler (`/yer/{sehir}/{slug}`, `/sehir/.../gezilecek-yerler`, ilçe
sayfası, `/rehber/{slug}`) plan’da; bu kodda henüz yok.

## Kod haritası

| Dosya | Rol |
|---|---|
| `src/lib/api.ts` | Tek HTTP sarmalayıcı — bileşen içine ham `fetch` yazma |
| `src/lib/types.ts` | Python `semalar.py` ile hizalı tipler |
| `src/lib/sabitler.ts` | Site sabitleri |
| `src/components/RotaSihirbazi.tsx` | Rota akışı |
| `src/app/layout.tsx` | Kök layout + metadata |
| `next.config.ts` | `/backend` rewrite |

## Notlar

- Ham yorum metni / yorumcu adı render edilmez.
- Site içi harita yok.
- Keşif listesi API `limit`/`offset`/`toplam_sayi` döner; “daha fazla yükle” UI yok.
- `robots.txt` / `sitemap.xml` / sayfa başına JSON-LD henüz yok (T-06).
- Prod yayın `next build && next start` ile olacak; şu an yerel `npm run dev`.
- Bu Next.js sürümü eğitim verisinden farklı olabilir: `site/AGENTS.md` ve
  `node_modules/next/dist/docs/`.
