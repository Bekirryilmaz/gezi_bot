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
| `/yer/[id]` | Allow-list tanıtım + olgusal yan bilgiler (UUID) |
| `/sehir/[anahtar]/bolgeler` | Şehir + ilçe tanıtımları |
| `/sehir/[anahtar]/rota` | Tek günlük Akıllı Rota |
| `/admin/login` | İç ekip girişi (tüketici hesabı değildir) |
| `/admin` | Yetkili inceleme, yayın, withdrawal ve audit masası |

Sihirbaz yalnız günlük tercihleri alır ve `POST /v1/gunluk-planlar` çağırır.
Gün sayısı, konaklama ve çok günlük alternatif seçimi public akışta yoktur.
Loading, empty, insufficient, unavailable ve error durumları ayrı gösterilir.

Hedef URL’ler (`/yer/{sehir}/{slug}`, `/sehir/.../gezilecek-yerler`, ilçe
sayfası, `/rehber/{slug}`) plan’da; bu kodda henüz yok.

## Kod haritası

| Dosya | Rol |
|---|---|
| `src/lib/api.ts` | Tek HTTP sarmalayıcı — bileşen içine ham `fetch` yazma |
| `src/lib/types.ts` | Python `semalar.py` ile hizalı tipler |
| `src/lib/sabitler.ts` | Site sabitleri |
| `src/components/GunlukRotaSihirbazi.tsx` | Public tek günlük rota akışı |
| `src/app/layout.tsx` | Kök layout + metadata |
| `next.config.ts` | `/backend` rewrite |

## Notlar

- Ham yorum/yazar, örnek ifade, duygu/puan, yorum hacmi ve iç skor render edilmez.
- Site içi harita yok.
- Keşif listesi API `limit`/`offset`/`toplam_sayi` döner; “daha fazla yükle” UI yok.
- `robots.txt` / `sitemap.xml` / sayfa başına JSON-LD henüz yok (T-06).
- Prod yayın `next build && next start` ile olacak; şu an yerel `npm run dev`.
- Bu Next.js sürümü eğitim verisinden farklı olabilir: `site/AGENTS.md` ve
  `node_modules/next/dist/docs/`.
