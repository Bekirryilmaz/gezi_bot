# Sunucu katmanı

Üç parça: veritabanı şeması + JSONL aktarımı (`veritabani/`), REST API
(`api/`), kişiselleştirilmiş rota motoru (`rota_motoru/`). `veri/` katmanının
JSONL çıktısını PostgreSQL’e yazar; `site/` (Next.js, port 3000) bu API’yi
tüketir.

```
veri/cikti/islenmis/*.jsonl
        → veritabani/aktarim/
        → PostgreSQL + PostGIS
        → api/  ↔  rota_motoru/
        → site/  (SSR: 8125, tarayıcı: /backend rewrite)
```

Yerel çalıştırma: repo kökündeki [`calis.txt`](../calis.txt). Bu makinede
Docker yok; PostgreSQL `C:\PostgreSQL`. Ortak venv: repo kökünde `.venv_test`.
API portu **8125** (8000 değil).

## Kurulum

Komutları **repo kökünden** çalıştır (`ortak.*`, `veri.*`, `sunucu.*`). Alembic
istisnası: `sunucu/` içinden.

```text
.\.venv_test\Scripts\python.exe -m pip install -r sunucu\requirements.txt
copy sunucu\.env.example sunucu\.env
```

`VERITABANI_URL` varsayılanı:

```text
postgresql+psycopg://gezi_kullanici:gezi_sifre@localhost:5432/gezi_veritabani
```

Şema (Alembic `0001_ilk_sema` … `0004_tanitim_metni`):

```text
cd sunucu
..\.venv_test\Scripts\python.exe -m alembic upgrade head
```

Mevcut bir veritabanında `upgrade` çalıştırmadan baseline denetimi:

```text
cd sunucu
..\.venv_test\Scripts\python.exe -m alembic current
..\.venv_test\Scripts\python.exe -m alembic heads
..\.venv_test\Scripts\python.exe -m alembic history
cd ..
.\.venv_test\Scripts\python.exe -m sunucu.veritabani.sema_baseline
```

Denetim Alembic revizyonunu, PostGIS'i, tablo/kolon ve kritik indeksleri
salt-okunur karşılaştırır; drift durumunda kod `1`, erişim yoksa `2` döner.
Gerçek ortamda migration öncesi PostgreSQL yedeği alınır ve geri yükleme
ayrı bir kopyada denenir; bu denetim otomatik `upgrade`, `downgrade` veya
tablo/indeks silme çalıştırmaz.

Yerel Postgres yoksa (başka makine): PostGIS 14+ ve şu SQL yeter. `altyapi/`
içindeki compose yalnız opsiyonel yedek yoldur; bu geliştirme makinesinde
kullanılmaz.

```sql
CREATE ROLE gezi_kullanici LOGIN PASSWORD 'gezi_sifre';
CREATE DATABASE gezi_veritabani OWNER gezi_kullanici;
\c gezi_veritabani
CREATE EXTENSION postgis;
```

## Veri aktarımı

API’nin gerçek veriyle dolması için:

```text
.\.venv_test\Scripts\python.exe -m sunucu.veritabani.aktarim.calistir --sehir samsun
```

Önkoşul: `veri/` hattında eşleme + duygu + profil (+ bölge + tanıtım)
JSONL’leri üretilmiş olmalı. Aktarım sırası:

1. `Sehir` — `veri/ortak/sehir_ayarlari.py::SEHIRLER` üzerinden upsert
2. Yerler + `YerKaynak` (`yer_aktar.py`)
3. Yorumlar + `duygu_skoru_ortalama` (`yorum_aktar.py`)
4. `yer_profili` / `duygu_ozeti` (`profil_aktar.py`)
5. Bölge profilleri (`bolge_profil_aktar.py`)
6. Tanıtım metinleri (`tanitim_aktar.py`)

İdempotenttir: aynı yer/yorum tekrar eklenmez. Konsola eklenen/güncellenen
sayılar basılır.

## API

```text
.\.venv_test\Scripts\python.exe -m uvicorn sunucu.api.uygulama:uygulama --host 127.0.0.1 --port 8125
```

Swagger: http://127.0.0.1:8125/docs

Site tarayıcıda `/backend/*` → Next rewrite → bu süreç. CORS:
`API_IZINLI_ORIGINLER` (varsayılan `http://localhost:3000`). Uç nokta tablosu:
[`api/README.md`](api/README.md).

## Rota motoru

Kütüphanesiz, deterministik. Zincir: skorlama → açısal kümeleme → günlük
slot dizimi. Her skor `kirilim` taşır. Ayrıntı: [`rota_motoru/README.md`](rota_motoru/README.md).

```text
.\.venv_test\Scripts\python.exe -m pytest
```

Kamusal MVP akışı yalnız `POST /v1/gunluk-planlar` kullanır. Çok günlük ve
konaklama devam yazmaları `410 Gone` ile kapalıdır; tarihsel tablolar ve
salt-okunur kayıt uçları veri kaybı olmadan korunur.

## Klasör yapısı

```
sunucu/
  veritabani/
    modeller.py            SQLAlchemy (Sehir, Yer, Yorum, BolgeProfili, …)
    baglanti.py
    sorgular.py            Keşif vitrini filtresi burada
    sema_baseline.py       Salt-okunur migration/model drift denetimi
    migrasyonlar/          Alembic 0001–0004
    aktarim/               JSONL → PostgreSQL
  api/
    uygulama.py            FastAPI giriş
    altyapi.py             Request ID, JSON log, tipli hata ve write limiti
    semalar.py             Dışarıya açık Pydantic (modeller.py değil)
    yerler_router.py
    rotalar_router.py
  rota_motoru/
    veri_tipleri.py
    skorlama.py
    zaman_butcesi.py
    kumeleme.py
    siralama.py            TSP yedek; üretim slot kullanır
    rota_olusturucu.py
    rota_anlatim.py
    testler/
```

JSONB esnek alanlar (`ozellikler`, `aktiviteler`, `deneyim_puanlari`,
`konu_duygulari`, `yer_profili`) dururken yeni kolon açma; etiket =
taksonomi + `ortak/sabitler.py`.
