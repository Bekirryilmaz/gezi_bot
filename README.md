# Samsun Gezi Platformu

Samsun ile başlayıp Karadeniz bölgesine büyüyecek, Türkiye'ye özel, kişiselleştirilmiş
rota algoritmasına sahip bir gezi/keşif platformu. Detaylı yol haritası için
`.cursor/plans/` altındaki plan dosyasına bakabilirsin.

## Proje Neden Bu Şekilde Bölündü

Proje üç ana, birbirinden bağımsız çalışabilen parçaya ayrılmıştır. Amaç, veri
toplama tarafında yapılan bir değişikliğin site tarafını etkilememesi, ikisinin
ayrı ayrı geliştirilip test edilebilmesidir:

- **`veri/`** — Veri toplama (scraping), kaynaklar arası eşleştirme, duygu analizi
  ve veri kalite kontrolü. Tamamen Python. Çıktısı: temiz, standart formatlı veri.
- **`sunucu/`** — Veritabanı şeması + veri aktarımı, REST API ve kişiselleştirilmiş
  rota üretme algoritması. Tamamen Python (FastAPI). `veri/` katmanının ürettiği
  veriyi PostgreSQL'e aktarır, siteye API olarak sunar. Detaylar için `sunucu/README.md`.
- **`site/`** — Kullanıcının göreceği web sitesi (ileride Next.js ile yazılacak,
  Faz 3'te doldurulacak). Şu an sadece yer tutucu.

Ayrıca:

- **`ortak/`** — Sadece `veri/` ve `sunucu/` arasında paylaşılan kategori
  taksonomisi sabitleri (`sabitler.py`). Bilerek çok küçük tutulur; nadiren
  değişir, bu yüzden iki tarafın da bağlı olması çakışma riski yaratmaz.
- **`dokumanlar/`** — Kategori taksonomisi, veri sözlüğü gibi Türkçe, herkesin
  (özellikle kod yazmayanların da) anlayabileceği açıklayıcı dokümanlar.
- **`altyapi/`** — Docker Compose, veritabanı ve dağıtım (deployment) ile ilgili
  dosyalar.

## Kod Yazım Kuralı

Bu projede fonksiyon, değişken ve sınıf isimleri **Türkçe ama Türkçe karaktersiz**
yazılır. Örnek: `isletme_verisi`, `duygu_skoru`, `rota_olustur`. Yorum satırları ve
dokümantasyon tamamen Türkçe'dir. Amaç, projenin veri kalitesini kontrol eden,
kod yazmayan biri tarafından bile büyük ölçüde anlaşılabilir olmasıdır.

## Klasör Yapısı

```
gezi_bot/
  ortak/                    Sadece kategori taksonomisi sabitleri (veri ve sunucu arasinda paylasilir)
  veri/                     Veri toplama, temizleme, duygu analizi (Python)
    ortak/                  Toplayicilara ozel veri semalari (Pydantic modelleri)
    toplayicilar/           Kaynak basina bir dosya (osm, google, eksi sozluk, tripadvisor)
    esleme/                 Kaynaklar arasi tekillestirme (deduplication)
    duygu_analizi/          Sentiment + konu (aspect) analizi pipeline'i
    kalite_kontrol/         Turkce veri kalite raporlari
    cikti/                  Ham ve islenmis veri ciktilari (git'e girmez, buyuk dosyalar)
  sunucu/                   FastAPI backend + rota algoritmasi (Python)
    api/                    REST uc noktalari (yer listeleme/detay, rota olusturma)
    veritabani/             SQLAlchemy modelleri + Alembic migration + JSONL aktarim katmani
    rota_motoru/            Rota algoritmasi (skorlama -> kumeleme -> siralama -> orkestrator)
  site/                     Next.js frontend (Faz 3)
  dokumanlar/               Kategori taksonomisi, veri sozlugu, mimari notlari
  altyapi/                  Docker Compose, veritabani, dagitim betikleri
```

## Kurulum (Geliştirme Ortamı)

### 1. Veritabanı (yerel geliştirme için)

Yerel bilgisayarında PostgreSQL + PostGIS'i Docker ile ayağa kaldırmak için:

```bash
cd altyapi
docker compose up -d
```

Bu, `localhost:5432` üzerinde `gezi_veritabani` adında bir veritabanı açar
(kullanıcı adı/şifre için `altyapi/docker-compose.yml` içine bak).

### 2. Veri katmanı (`veri/`)

```bash
cd veri
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac (Oracle sunucu)
pip install -r requirements.txt
playwright install chromium     # Google Maps ve TripAdvisor toplayicilari icin gerekli
```

Toplayıcıları çalıştırma örnekleri `veri/README.md` içinde anlatılıyor.

### 3. Sunucu (`sunucu/`)

```bash
cd sunucu
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env          # Windows, DB baglanti bilgisini duzenle
alembic upgrade head            # Veritabani semasini olustur
```

Sonra (repo kökünden), önce veriyi aktar, sonra API'yi başlat:

```bash
python -m sunucu.veritabani.aktarim.calistir --sehir samsun
uvicorn sunucu.api.uygulama:uygulama --reload
```

`http://127.0.0.1:8000/docs` adresinden Swagger arayüzüyle tüm uç noktaları
deneyebilirsin. Detaylar için `sunucu/README.md`, `sunucu/api/README.md` ve
`sunucu/rota_motoru/README.md`.

## Ortam Değişkenleri

Her alt proje kendi `.env.example` dosyasını içerir. Gerçek `.env` dosyaları asla
git'e eklenmez (bkz. `.gitignore`).

## Şu Anki Durum

Faz 1 (veri toplama + duygu analizi) ve Faz 2 (veri aktarımı + sunucu API +
rota algoritması) tamamlandı, Samsun verisiyle uçtan uca test edildi. Faz 3
(Next.js sitesi + canlıya alma) için klasörler hazır ama içerik henüz
doldurulmadı.
