# Site (Frontend) — Rotam

Next.js + Tailwind CSS. Faz 3 arayüzü.

## Kurulum

```bash
cd site
npm install
```

`.env.local` içinde API adresi:

```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Çalıştırma

Önce API (repo kökünden):

```bash
uvicorn sunucu.api.uygulama:uygulama --reload --host 127.0.0.1 --port 8000
```

Sonra site:

```bash
cd site
npm run dev
```

Tarayıcı: http://localhost:3000

## Sayfalar

| Yol | İçerik |
|-----|--------|
| `/` | Marka hero + giriş |
| `/sehir/[anahtar]` | Keşif listesi (kategori filtresi) |
| `/yer/[id]` | Yer detay + duygu özeti + yorumlar |
| `/sehir/[anahtar]/bolgeler` | Şehir/ilçe bölge profilleri |
| `/sehir/[anahtar]/rota` | Kişisel rota sihirbazı |

Marka adı: **Rotam**. Görsel dil: Karadeniz kıyısı (deniz yeşili / köpük / kumsal vurgusu).
