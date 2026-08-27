# ŞAMANDIRA

Samsun ile başlayıp Karadeniz’e büyüyecek, kişiselleştirilmiş rota
algoritmasına sahip gezi/keşif platformu. Marka adı **ŞAMANDIRA**
(küçük harfle `samandira`).

Yerel MVP ayaktadır: FastAPI + PostgreSQL/PostGIS API ve Next.js 16 /
Tailwind arayüzü birlikte çalışır. Keşif haritası, ilçe vitrini, hava
durumu widget’ı ve rota sihirbazı sitede canlıdır. Canlıya alma
(nginx/SSL) henüz yapılmamıştır.

## Mimari

Üç katman birbirinden bağımsız geliştirilebilir:

- **`veri/`** — Toplama, eşleme, duygu analizi, kalite kontrolü (Python).
  Çıktı: temiz JSONL.
- **`sunucu/`** — SQLAlchemy + Alembic, JSONL aktarımı, FastAPI, rota
  motoru. PostgreSQL + PostGIS. Detay: `sunucu/README.md`.
- **`site/`** — Next.js 16 (App Router) + TypeScript + Tailwind.
  Marka: ŞAMANDIRA. Sayfalar: ana sayfa, `/kesfet` (ilçe haritası),
  yer listesi/detay, bölgeler, rota (hava durumu + sihirbaz).

Ayrıca:

- **`ortak/`** — Kategori taksonomisi sabitleri (`sabitler.py`).
- **`dokumanlar/`** — Taksonomi ve veri sözlüğü.
- **`altyapi/`** — Docker Compose (yerel PostGIS) ve ileride dağıtım.

```
gezi_bot/
  ortak/
  veri/           toplayicilar, esleme, duygu_analizi, kalite_kontrol
  sunucu/         api, veritabani, rota_motoru
  site/           Next.js 16 arayüzü (ŞAMANDIRA)
  dokumanlar/
  altyapi/
```

## Kod Yazım Kuralı

Fonksiyon, değişken ve sınıf isimleri **Türkçe ama Türkçe karaktersiz**
yazılır. Örnek: `isletme_verisi`, `duygu_skoru`, `rota_olustur`. Yorum
ve dokümantasyon Türkçe’dir.

## Kurulum (geliştirme)

### 1. Veritabanı

Docker ile:

```bash
cd altyapi
docker compose up -d
```

`localhost:5432` üzerinde `gezi_veritabani` açılır. Yerel PostgreSQL +
PostGIS de kullanılabilir (`calis.txt`).

### 2. Veri katmanı (`veri/`)

```bash
cd veri
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

Toplayıcı örnekleri: `veri/README.md`.

### 3. Sunucu (`sunucu/`)

```bash
cd sunucu
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
```

Repo kökünden veri aktarımı ve API:

```bash
python -m sunucu.veritabani.aktarim.calistir --sehir samsun
uvicorn sunucu.api.uygulama:uygulama --reload --host 127.0.0.1 --port 8125
```

Swagger: `http://127.0.0.1:8125/docs`

### 4. Site (`site/`)

```bash
cd site
npm install
npm run dev
```

Tarayıcı: `http://localhost:3000`  
`site/.env.local`: `NEXT_PUBLIC_API_URL=http://127.0.0.1:8125`

## Ortam Değişkenleri

Her alt projenin `.env.example` dosyası vardır. Gerçek `.env` git’e
girmez.

## Şu anki durum

Veri pipeline’ı, FastAPI + PostGIS ve ŞAMANDIRA arayüzü yerel MVP olarak
birlikte çalışır. Samsun odaklıdır; ikinci şehir ve üretim dağıtımı
sonraki iştir.
