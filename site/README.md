# Site (Frontend) — ŞAMANDIRA

Next.js 16 (App Router) + Tailwind CSS. Marka: **ŞAMANDIRA**.

## Çalıştırma

API’nin ayakta olması gerekir (`http://127.0.0.1:8125` varsayılan):

```bash
# repo kökünden
.\.venv\Scripts\python.exe -m uvicorn sunucu.api.uygulama:uygulama --host 127.0.0.1 --port 8125
```

```bash
cd site
npm install
npm run dev
```

Tarayıcı: [http://localhost:3000](http://localhost:3000)

`.env.local` içinde `NEXT_PUBLIC_API_URL` API adresini gösterir.

## Sayfalar

| Yol | Açıklama |
|-----|----------|
| `/` | Ana sayfa (marka hero + CTA) |
| `/kesfet` | GIS ilçe haritası + vitrin (17 ilçe) |
| `/sehir/[anahtar]` | İlçe haritası + keşif listesi |
| `/yer/[id]` | Yer detayı (duygu özeti) |
| `/sehir/[anahtar]/bolgeler` | Şehir + ilçe bölge profilleri |
| `/sehir/[anahtar]/rota` | Hava durumu + kişisel rota sihirbazı |

## Notlar

- CORS: sunucu `API_IZINLI_ORIGINLER` ile `http://localhost:3000` izinli olmalı.
- Hava durumu: Open-Meteo (anahtar gerekmez).
- Harita: Leaflet + Carto tiles, `next/dynamic` ile `ssr: false`.
