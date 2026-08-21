# Site (Frontend) — Rotam

Next.js (App Router) + Tailwind CSS. Marka: **Rotam**.

## Çalıştırma

API’nin ayakta olması gerekir (`http://127.0.0.1:8125` varsayılan):

```bash
# repo kökünden
.\.venv_test\Scripts\python.exe -m uvicorn sunucu.api.uygulama:uygulama --host 127.0.0.1 --port 8125
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
| `/sehir/[anahtar]` | Keşif listesi (kategori filtresi) |
| `/yer/[id]` | Yer detayı (duygu özeti, örnek yorumlar) |
| `/sehir/[anahtar]/bolgeler` | Şehir + ilçe bölge profilleri |
| `/sehir/[anahtar]/rota` | Kişisel rota sihirbazı |

## Notlar

- CORS: sunucu `API_IZINLI_ORIGINLER` ile `http://localhost:3000` izinli olmalı.
- Harita görünümü henüz yok; sonraki iterasyonda eklenebilir.
