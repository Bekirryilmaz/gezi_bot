# Şamandıra

Karadeniz kıyısından başlayan kişiselleştirilmiş gezi / keşif platformu.
Marka: **Şamandıra** (Alegre Group). Repo adı henüz `gezi_bot` (GitHub’da
`samandira` olacak). Canonical: `https://şamandıra.com`.

İlk şehir: **Samsun**. Tarihsel yerel uygulamanın üç ana alanı:

- **Keşif** — şehirdeki yerleri listele, filtrele, detay oku (konaklama vitrinde gizlenir)
- **Bölgeler** — şehir + ilçe tanıtımı ve ziyaretçi yorumlarından derlenen duygu özeti
- **Rota** — ilgi ağırlıklarına göre gün gün plan; konaklama belli veya değil

Yerel çalıştırma kaynağı: [`calis.txt`](calis.txt). Güncel kabul edilmiş ürün
referansları ve kabul kayıtları: [dokümantasyon dizini](docs/README.md).
Geliştirme sırası, MVP/v1/v2 ve ticari büyüme:
[14 Ürün Özellik Haritası](docs/09-business/14-urun-ozellik-haritasi.md).
`plan/00_brief_eki.md` ve `plan/BRIF.md` tarihsel planlardır; kabul edilmiş
ürün referanslarının önüne geçmezler.

Bu README'deki gün gün rota, konaklama bağlamı, duygu skoru ve diğer teknik
anlatımlar mevcut uygulama geçmişidir; hedef kapsamın kabulü değildir.
Kabul edilmiş Akıllı Rota günlük planla sınırlıdır. Çok günlük **Akıllı Gezi**,
FAZ 14'te ayrı kapsam kararı bekleyen genişleme olarak değerlendirilmiştir.
Aşağıdaki hazır/çalışıyor beyanları bu dokümantasyon görevinde yeniden test
edilmemiştir; hedef davranışla uyum için uygulama farkı incelemesi gerekir.

## Şu anki durum

| Parça | Durum |
|---|---|
| Veri toplama + eşleme + duygu + profil + tanıtım | Yazılmış, Samsun ile çalıştırılmış |
| PostgreSQL + PostGIS + Alembic (`0001`–`0004`) | Hazır (bu makinede Docker yok; yerel `C:\PostgreSQL`) |
| JSONL → DB aktarım | Hazır, idempotent |
| FastAPI + rota motoru | Hazır, uçtan uca test edilmiş — port **8125** |
| Next.js site | Yazılmış ve yerel çalışıyor — port **3000** |
| Harita (site içi) | Yok (yer detayında dış harita linki var) |
| Kullanıcı hesabı / ödeme / admin / canlı yayın | Yok |
| İkinci şehir | Yok (`veri/ortak/sehir_ayarlari.py` yeter) |

DB’de Samsun için yer kataloğu dolu (~1.700 kayıt). Keşif vitrini varsayılan
limit ile ilk sayfayı gösterir; sayfalama UI’si henüz yok.

## Mimari

Üç bağımsız katman + ince ortak dil:

```
Kaynaklar (OSM, Google, Ekşi, …)
  → veri/cikti/ham/*.jsonl
  → eşleme → birlesik_yerler
  → duygu → yorumlar
  → yer/bölge profili + tanıtım
  → python -m sunucu.veritabani.aktarim.calistir --sehir samsun
  → PostgreSQL
  → FastAPI (8125)
  → Next.js (tarayıcı /backend/* vekili; SSR doğrudan 8125)
```

| Klasör | Dil | Ne işe yarar |
|---|---|---|
| `veri/` | Python | Scraping, eşleme, duygu, kalite. Çıktı: JSONL (`veri/cikti/` git’te yok) |
| `sunucu/` | Python | PostgreSQL aktarım + FastAPI + rota motoru |
| `site/` | Next.js 16 + React 19 + Tailwind 4 | Kullanıcı arayüzü |
| `ortak/` | Python | Yalnız taksonomi sabitleri (`veri` + `sunucu` paylaşır) |
| `dokumanlar/` | Markdown | Taksonomi + veri sözlüğü |
| `plan/` | Markdown | Brif, SEO, marka, deploy, görev paketleri (T-00…) |
| `altyapi/` | Docker Compose | Yalnız PostGIS; **bu makinede kullanılmıyor** |

Katman kuralı: site sunucu kodunu import etmez (yalnız HTTP). Yeni şehir =
`veri/ortak/sehir_ayarlari.py` içine `SehirAyari`; toplayıcı/API/rota koduna
şehir adı gömülmez.

## Kod yazım kuralı

Fonksiyon, değişken, sınıf, commit ve doküman tanımlayıcıları **Türkçe,
Türkçe karaktersiz**: `isletme_verisi`, `duygu_skoru`, `rota_olustur`.
Kullanıcıya görünen metinde marka **Şamandıra** (eski “Rotam” yok).

Yeni özellik sırası: `dokumanlar/kategori_taksonomisi.md` → `ortak/sabitler.py`
→ kod. Kara kutu yok: her skor `kirilim` ile açıklanır. Anlatım metinleri
şablon + sabit tohum (LLM yok). Tek istisna: genel duygu skoru — Türkçe BERT.

## Yerel kurulum

Bu makine: PostgreSQL `C:\PostgreSQL`, ortak venv repo kökünde `.venv_test`,
API **8125**, site **3000**. Komutların çoğu **repo kökünden** çalışır.

### 1. PostgreSQL

```text
C:\PostgreSQL\bin\pg_ctl.exe status -D C:\PostgreSQL\data
```

Gerekirse başlat:

```text
C:\PostgreSQL\bin\pg_ctl.exe start -D C:\PostgreSQL\data -l C:\PostgreSQL\data\startup.log -w
```

Bağlantı (`sunucu/.env` veya varsayılan):

```text
postgresql+psycopg://gezi_kullanici:gezi_sifre@localhost:5432/gezi_veritabani
```

`sunucu/.env` yoksa: `copy sunucu\.env.example sunucu\.env`

### 2. Python venv (bir kez)

```text
python -m venv .venv_test
.\.venv_test\Scripts\python.exe -m pip install -r sunucu\requirements.txt
.\.venv_test\Scripts\python.exe -m pip install -r veri\requirements.txt
.\.venv_test\Scripts\python.exe -m playwright install chromium
```

Toplayıcılar Playwright Chromium ister; API/rota yalnız `sunucu/requirements.txt`
ile de ayağa kalkar.

### 3. Şema + aktarım (bir kez / şema değişince)

```text
cd sunucu
..\.venv_test\Scripts\python.exe -m alembic upgrade head
```

Sonra repo kökünden:

```text
.\.venv_test\Scripts\python.exe -m sunucu.veritabani.aktarim.calistir --sehir samsun
```

Aktarım idempotenttir. Sıra: şehir → yerler → yorumlar → yer profilleri →
bölge profilleri → tanıtımlar.

### 4. API + site

```text
.\.venv_test\Scripts\python.exe -m uvicorn sunucu.api.uygulama:uygulama --host 127.0.0.1 --port 8125
```

Başka terminalde:

```text
cd site
npm install
npm run dev -- --port 3000
```

`site/.env.local`:

```text
NEXT_PUBLIC_API_URL=http://127.0.0.1:8125
```

- Site: http://localhost:3000
- API / Swagger: http://127.0.0.1:8125/docs
- CORS: `API_IZINLI_ORIGINLER` (varsayılan `localhost:3000`). Tarayıcı
  `/backend/*` → Next rewrite → FastAPI.

## Veri hattı (toplayıcı → site)

Hepsi repo kökünden, `.venv_test` ile. `--sehir` anahtarı
`veri/ortak/sehir_ayarlari.py` içindeki kayıttır.

```text
.\.venv_test\Scripts\python.exe -m veri.toplayicilar.tum_kaynaklari_calistir --sehir samsun
.\.venv_test\Scripts\python.exe -m veri.esleme.eslestirici --sehir samsun
.\.venv_test\Scripts\python.exe -m veri.duygu_analizi.pipeline_calistir --sehir samsun
.\.venv_test\Scripts\python.exe -m veri.duygu_analizi.profil_pipeline_calistir --sehir samsun
.\.venv_test\Scripts\python.exe -m veri.duygu_analizi.bolge_profili_pipeline_calistir --sehir samsun
.\.venv_test\Scripts\python.exe -m veri.duygu_analizi.tanitim_pipeline_calistir --sehir samsun
.\.venv_test\Scripts\python.exe -m veri.kalite_kontrol.rapor_olustur --sehir samsun
.\.venv_test\Scripts\python.exe -m sunucu.veritabani.aktarim.calistir --sehir samsun
```

TripAdvisor ve Booking varsayılan kapalı (engel). Google takılırsa:
`veri.toplayicilar.nobetci_calistir`. Detay: `veri/README.md`.

## API uçları (9 genel)

| Metod | Yol | Ne işe yarar |
|---|---|---|
| GET | `/sehirler` | Aktif şehirler |
| GET | `/sehirler/{anahtar}/yerler` | Liste. Varsayılan `sadece_kesif=true` |
| GET | `/sehirler/{anahtar}/bolgeler` | Şehir + ilçe profilleri |
| GET | `/yerler/{id}` | Detay + profil + örnek ifade (ham yorum metni yok) |
| POST | `/rotalar/olustur` | Tek rota (Senaryo 1 veya eski Senaryo 2) |
| POST | `/rotalar/olustur-alternatifler` | 2–3 alternatif; otel dayatma yok |
| POST | `/rotalar/{id}/konaklama-bolgesi-oner` | Seçilen rotaya bölge önerisi |
| GET | `/rotalar/{id}` | Kayıtlı rota (paylaşılabilir) |
| GET | `/sabit-rotalar` | Elle küratör rotalar |

Keşif vitrini (`sadece_kesif=true`): konaklama gizlenir; yeme-içme yalnızca
`sehrin_klasigi` / `sponsorlu_mekan` / `kahvalti_verir` veya duygu ≥ 80/100.
Rota motoru `sadece_kesif=false` ile kısıtsız çeker.

## Site sayfaları (şu an)

| Yol | Sayfa |
|---|---|
| `/` | Hero + Keşfet / Bölgeler / Rota |
| `/sehir/[anahtar]` | Keşif listesi (konaklama chip’i yok) |
| `/yer/[id]` | Tanıtım + duygu özeti + yan bilgiler (UUID; slug T-05) |
| `/sehir/[anahtar]/bolgeler` | İlçe/şehir profilleri |
| `/sehir/[anahtar]/rota` | Rota sihirbazı |

Hedef URL’ler (`/yer/{sehir}/{slug}`, ilçe sayfası, `/rehber/{slug}`)
`plan/00_brief_eki.md` §5 ve `plan/02_seo_mimarisi.md` içinde; henüz yok.

Rota testleri:

```text
.\.venv_test\Scripts\python.exe -m pytest sunucu/rota_motoru/testler/ -v
```

## Doküman haritası

[12 Görsel Tasarım Dili](docs/03-design/12-gorsel-tasarim-dili.md)

[13 Bileşen ve Etkileşim Sözleşmeleri](docs/03-design/13-bilesen-ve-etkilesim-sozlesmeleri.md) — kabul edilmiş 00–12 referanslarına bağlı davranış belgesi; 52 ana bölüm, 30 Mermaid diyagramı, 77 örnek senaryo, 50 maddelik öz eleştiri ve nihai Interaction Contract. Dokümantasyon olarak hazır; uygulama veya yeni sözleşmenin ayrıca kabul edildiği anlamına gelmez.

**14 Eylül 2026 — Design System güncellemesi:** Kullanıcının açık beyanıyla 00–09 belgelerinin tamamı kabul edilmiş referanstır; aşağıdaki eski durum kayıtları tarihsel olarak korunur. Yeni [10 Design System](docs/03-design/10-design-system.md), 60 ana başlık, 48 bileşen sözleşmesi, 22 Mermaid diyagramı, 32 kabul senaryosu ve 60 maddelik öz eleştiriyle bütün kanalların tasarım anayasası önerisini tanımlar. Referansların içerikleri değiştirilmemiştir. Yeni belge ayrıca kabul ve doğrulama bekler; kod, ekran veya tamamlanmış kullanıcı araştırması değildir.

**13 Eylül 2026 — Ürün Ekosistemi güncellemesi:** Bu görevde 00–08 belgelerinin tamamı kabul edilmiş referans olarak alınmıştır; aşağıdaki önceki kabul/durum ifadeleri tarihsel kayıttır. Yeni [09 Ürün Ekosistemi](docs/09-business/09-urun-ekosistemi.md), bu referansları değiştirmeden yaşam döngülerini, kişisel kayıt ve paylaşımı, ücretsiz/Premium sınırlarını, ticari modelleri ve uzun vadeli büyümeyi tanımlar. 14 Mermaid diyagramı, 48 maddelik öz eleştiri ve alternatif mimari değerlendirmesi içerir. Yeni belge kabul bekleyen ürün mimarisi önerisidir; uygulanmış özellik veya tamamlanmış araştırma değildir.

Kabul edilmiş 00–07 ürün ve UX referansları ile yeni tasarım belgesi için [dokümantasyon dizini](docs/README.md) kullanılır. [08 Tasarım İlkeleri](docs/03-design/08-tasarim-ilkeleri.md), bu referansların üzerine kurulan nihai tasarım anayasası önerisidir; kabul, uygulama veya tamamlanmış kullanıcı araştırması anlamına gelmez. 07 UX Karar Akışları kullanıcının Tasarım İlkeleri görevindeki açık beyanıyla kabul edilmiş referanstır. Ürün kararlarında kabul edilmiş referanslar aşağıdaki tarihsel planların önündedir.

| Dosya | İçerik |
|---|---|
| `calis.txt` | Bu makinede çalıştırma (port, venv, PostgreSQL) |
| `dokumanlar/kategori_taksonomisi.md` | Kategori / özellik / deneyim eksenleri |
| `dokumanlar/veri_sozlugu.md` | Alan adları sözlüğü |
| `plan/BRIF.md` | Orijinal brif (değişmez tarihî belge) |
| `plan/00_brief_eki.md` | Güncel kararlar + durum |
| `plan/01_urun_analizi_ve_strateji.md` | Pazar, yol haritası, KPI |
| `plan/02_seo_mimarisi.md` | URL, metadata, JSON-LD |
| `plan/03_cursor_araclari_kurulumu.md` | Cursor rules / MCP / kalite kapıları |
| `plan/04_marka_ve_tema.md` | Logo, palet, ses tonu |
| `plan/05_deployment_oracle.md` | Canlıya alma (henüz uygulanmadı) |
| `plan/06_mobil_ve_harita.md` | Harita + PWA (henüz yok) |
| `plan/07_cursor_talimatlari.md` | T-00 … T-15 görev paketleri |
| `veri/README.md` | Toplayıcı ayrıntıları |
| `sunucu/README.md` | Aktarım, API, rota motoru |
| `sunucu/api/README.md` | Uç nokta sözleşmesi |
| `site/README.md` | Next.js çalıştırma ve sayfalar |

## Bilinen boşluklar

Site içi harita, auth, admin, prod yayın, ikinci şehir, keşif sayfalama UI,
yer slug’ı, robots/sitemap/JSON-LD yok. Ham yorum metni ve yorumcu adı
sitede gösterilmez. OSM atfı footer’da kalır (ODbL).
