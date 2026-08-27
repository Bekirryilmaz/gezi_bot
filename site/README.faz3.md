# Site (Frontend) — ŞAMANDIRA

Next.js 16 + Tailwind CSS. Görsel dil: Karadeniz kıyısı (deniz / köpük)
ve koyu bordo kontrast.

## Kurulum

```bash
cd site
npm install
```

`.env.local` içinde API adresi:

```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8125
```

## Çalıştırma

Önce API (repo kökünden), sonra `npm run dev`. Tarayıcı: http://localhost:3000

## Sayfalar

| Yol | İçerik |
|-----|--------|
| `/` | Marka hero + giriş |
| `/kesfet` | İnteraktif ilçe haritası ve vitrin |
| `/sehir/[anahtar]` | Harita + keşif listesi |
| `/yer/[id]` | Yer detay + duygu özeti |
| `/sehir/[anahtar]/bolgeler` | Şehir/ilçe bölge profilleri |
| `/sehir/[anahtar]/rota` | Hava durumu + rota sihirbazı |

Marka adı: **ŞAMANDIRA**.
