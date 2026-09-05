# Proje Brifi (orijinal metin, Rotam dönemi)
> Bu dosya projenin çıkış brifidir ve **değişmez tarihî belgedir**. Güncel gerçek ve kararlar için `plan/00_brief_eki.md` okunur; çelişkide **00_brief_eki kazanır**. Marka artık **Şamandıra**'dır (brif içindeki "Rotam" ifadeleri tarihîdir).

Rotam — başka bir yapay zeka için proje brifi
Sen bir ürün/planlama asistanısın. Bu brifi oku. Kullanıcı seninle konuşup işleri netleştirecek; sen de Cursor'daki ajan için kısa, uygulanabilir talimat yazacaksın. Kodu sen yazmıyorsun; Cursor ajanı yazıyor.

Kritik: README.md, sunucu/README.md, sunucu/api/README.md "Faz 3 boş / site yok / sadece Swagger" diyor. Bu yanlış. Site yazılmış. Gerçek durum bu briftedir.

1. Ürün nedir?
Marka: Rotam
Repo: gezi_bot
Yol: C:\Users\ebube\OneDrive\Desktop\buyuk_gezi_projesi\gezi_bot
Dal: main (origin/main ile aynı). Son commit: f1c87c0 — "rota algoritması güncellemesi" (25 Ağustos 2026).

Samsun ile başlayan, Karadeniz'e sonra Türkiye'ye büyüyecek kişiselleştirilmiş gezi / keşif platformu. Kullanıcıya üç şey sunar:

Keşif — şehirdeki yerleri (müze, plaj, kafe…; konaklama vitrinde gizlenir) listele, filtrele, detay oku
Bölgeler — şehir + ilçe tanıtımı ve yorumlardan çıkan duygu özeti
Rota — ilgi ağırlıklarına göre gün gün plan; konaklama belli veya değil
İlk şehir: Samsun (plaka 55, Karadeniz). Başka şehir kodda yok; eklemek için veri/ortak/sehir_ayarlari.py yeter, toplayıcı kodu değişmez.

2. Şu an gerçek durum (2026-09-05)
Katman	Durum
Veri toplama + eşleme + duygu + profil + tanıtım
Yazılmış, Samsun ile çalıştırılmış
PostgreSQL + PostGIS + Alembic (0001–0004)
Hazır
JSONL → DB aktarım
Hazır, idempotent
FastAPI + rota motoru
Hazır, uçtan uca test edilmiş
Next.js site (Rotam)
Yazılmış ve yerel çalışıyor
Harita (site içi)
Yok (yer detayında "Google Maps'te aç" linki var)
Kullanıcı hesabı / giriş
Yok
Ödeme / rezervasyon
Yok
Admin paneli
Yok
Canlıya alma (Docker app + nginx + Oracle)
Yok; altyapi/ sadece DB compose
İkinci şehir
Yok
TripAdvisor / Booking toplayıcı
Kod var, varsayılan kapalı (engel)
Sabit/küratör rotalar
Tablo + API var, içerik büyük ihtimalle boş
Fotoğraflar
Şema var, pratikte zayıf
Yerel makine: Docker yok. PostgreSQL yerelde: C:\PostgreSQL. API port 8125, site 3000. Python venv: repo kökünde .venv_test.

Çalıştırma: repo kökündeki calis.txt güncel kaynak. Kök README'deki "port 8000 / site boş" bilgisine uyma.

3. Mimari
Üç bağımsız parça + ince ortak katman:

veri/          Python  — scraping, eşleme, duygu, kalite. Çıktı: JSONL
sunucu/        Python  — PostgreSQL aktarım + FastAPI + rota motoru
site/          Next.js 16 + React 19 + Tailwind 4 — kullanıcı arayüzü
ortak/         Sadece taksonomi sabitleri (veri + sunucu paylaşır)
dokumanlar/    Türkçe sözlük / taksonomi (kod yazmayan da okusun diye)
altyapi/       docker-compose: yalnızca PostGIS (bu makinede kullanılmıyor)
Akış:

Kaynaklar (OSM, Google, Ekşi…)
  → veri/cikti/ham/*.jsonl
  → eşleme → birlesik_yerler
  → duygu → yorumlar
  → yer/bölge profili + tanıtım
  → python -m sunucu.veritabani.aktarim.calistir --sehir samsun
  → PostgreSQL
  → FastAPI (8125)
  → Next.js (/backend vekili ile)
veri/cikti/ git'te yok (büyük dosyalar). Veri bu makinede yerel duruyor; yeni klonla site boş DB ile açılır.

4. Sert kurallar (ajan bunları bozmasın)
İsimler Türkçe, Türkçe karaktersiz: isletme_verisi, duygu_skoru, rota_olustur. Yorumlar ve dokümanlar Türkçe.
Yeni özellik sırası: önce dokumanlar/kategori_taksonomisi.md (gerekirse veri_sozlugu.md) → sonra ortak/sabitler.py → sonra kod. Taksonomi ile kod sapmasın.
Kara kutu yok. "Neden bu skor?" her zaman kirilim ile cevaplanmalı. Konu/profil çıkarımı anahtar kelime + izlenebilir ornek_ifadeler / gecen_ifade. Anlatım metinleri şablon + sabit tohum; LLM yok. Genel duygu skoru tek istisna: Türkçe BERT (incidelen/bert-base-turkish-sentiment-analysis-128k-cased).
Şehir bağımsız. Yeni şehir = SEHIRLER sözlüğüne SehirAyari. Toplayıcı/API/rota kodu şehir adına bağlanmasın.
Katmanları karıştırma. Scraping değişikliği siteyi kırmasın. ortak/ bilerek küçük.
JSONB esnek alanlar: ozellikler, aktiviteler, deneyim_puanlari, konu_duygulari, yer_profili. Yeni etiket için kolon/migration açma; taksonomi + sabit ekle.
Commit / push kullanıcı açıkça istemeden yapılmaz.
5. Taksonomi (ortak dil)
ortak/sabitler.py ↔ dokumanlar/kategori_taksonomisi.md

Ana kategoriler: gezilecek_yer | konaklama | yeme_icme

Özellikler (JSONB): alkol_servisi, ogrenci_dostu, fiyat_seviyesi (1–4), ortalama_ziyaret_suresi_dk, …
Özel etiketler: sehrin_klasigi (+15 skor), sponsorlu_mekan (+30), kahvalti_verir (sabah slotu)

Deneyim eksenleri (0–100, rota skoru):
tarihi_kulturel_puani, eglence_puani, doga_macera_puani, gastronomi_puani, gece_hayati_puani, rahatlatici_sakin_puani
Yorum yoksa alt kategori varsayılanı kullanılır.

Yer profili (yorumlardan, BERT/LLM yok): fiyat_algisi, ulasim_kolayligi, kalabalik_zamanlar, ziyaretci_profili
fiyat_seviyesi (kaynak, objektif) ≠ fiyat_algisi (ziyaretçi algısı).

İki metin türü karışmasın:

tanitim_metni — Wikipedia / Google hakkında / OSM / şablon (nesnel)
duygu_ozeti — yorumlardan şablon anlatım (öznel)
6. Veri katmanı (veri/)
Komutlar repo kökünden.

Toplayıcılar
Dosya	Kaynak	Not
osm_toplayici.py
Overpass API
Hızlı, ücretsiz
google_maps_toplayici.py
Playwright
Ana yer kataloğu; yorumlar bazen boş ("sınırlı görünüm")
eksi_sozluk_toplayici.py
requests + BS
Ana Türkçe yorum + bölge profili kaynağı
tripadvisor_toplayici.py
Playwright
DataDome; varsayılan atla
booking_toplayici.py
Playwright
TR IP yasal engel; varsayılan atla
Orkestratör: python -m veri.toplayicilar.tum_kaynaklari_calistir --sehir samsun
Google takılırsa: nobetci_calistir.py (durgunlukta süreci öldürüp --devam-et).
Kesinti dayanıklı: aynı çıktı dosyası varsa kaldığı yerden. Engel tespit edilirse nazikçe durur.

Sonrası
python -m veri.esleme.eslestirici --sehir samsun
python -m veri.duygu_analizi.pipeline_calistir --sehir samsun
python -m veri.duygu_analizi.profil_pipeline_calistir --sehir samsun
python -m veri.duygu_analizi.bolge_profili_pipeline_calistir --sehir samsun
python -m veri.duygu_analizi.tanitim_pipeline_calistir --sehir samsun
python -m veri.kalite_kontrol.rapor_olustur --sehir samsun
Eşleme: kategori + mesafe + bulanık isim (rapidfuzz) → BirlesikYer.
Kalite raporu veriyi değiştirmez, işaret eder.

Ekşi yorumları bölgeye bağlıdır. yer_ismi_tespiti.py metinde bilinen yer adı görürse o yere de bağlar (fırsatçı, izlenebilir).

7. Veritabanı
PostgreSQL + PostGIS. Bağlantı: sunucu/.env → VERITABANI_URL
Varsayılan: postgresql+psycopg://gezi_kullanici:gezi_sifre@localhost:5432/gezi_veritabani

Tablolar (sunucu/veritabani/modeller.py):
sehirler, yerler, yer_kaynaklari, konaklama_detaylari, yorumlar, bolge_profilleri, sabit_rotalar, kullanici_rotalari

ID'ler UUID metin. yerler.konum = Geography POINT 4326 (GiST).
Migrasyonlar: 0001_ilk_sema → 0002_yer_profili → 0003_bolge_profili → 0004_tanitim_metni

Aktarım: python -m sunucu.veritabani.aktarim.calistir --sehir samsun
Sıra: şehir → yerler → yorumlar → yer profilleri → bölge profilleri → tanıtımlar. Tekrar çalıştırılabilir.

8. API (FastAPI)
Giriş: sunucu/api/uygulama.py
Swagger: http://127.0.0.1:8125/docs
CORS: API_IZINLI_ORIGINLER (varsayılan localhost:3000)
Site tarayıcıda /backend/* → Next rewrite → FastAPI (CORS'u azaltır). SSR doğrudan NEXT_PUBLIC_API_URL (8125).

Metod	Yol	Ne işe yarar
GET
/sehirler
Aktif şehirler
GET
/sehirler/{anahtar}/yerler
Liste. Varsayılan sadece_kesif=true
GET
/sehirler/{anahtar}/bolgeler
Şehir + ilçe profilleri
GET
/yerler/{id}
Detay + profil + örnek yorum (olumlu+olumsuz karışık)
POST
/rotalar/olustur
Tek rota (Senaryo 1 veya eski Senaryo 2)
POST
/rotalar/olustur-alternatifler
2–3 alternatif, otel dayatma yok
POST
/rotalar/{id}/konaklama-bolgesi-oner
Seçilen rotaya bölge önerisi
GET
/rotalar/{id}
Kayıtlı rota (paylaşılabilir)
GET
/sabit-rotalar
Elle küratör rotalar
Keşif vitrini (sadece_kesif=true, site bunu kullanır): konaklama gizlenir; yeme-içme yalnızca sehrin_klasigi / sponsorlu_mekan / kahvalti_verir veya duygu ≥ 80/100 (skor >= 0.6). Gezilecek yer serbest. Rota motoru sadece_kesif=false ile kısıtsız çeker.

Şema ayrı: sunucu/api/semalar.py (dışarı) ≠ modeller.py (saklama).

9. Rota motoru
Kütüphanesiz, deterministik. Test: pytest sunucu/rota_motoru/testler/ -v

Zincir: skorlama → açısal kümeleme (bearing, k-means yok) → günlük slot dizimi (TSP yedek; siralama.py duruyor ama üretim slot kullanıyor).

Gün şablonu (4 slot):

Sabah: gezilecek veya kahvalti_verir
Öğle: yeme-içme, ≤ 20 km
İkindi: gezilecek veya kafe/kahve
Akşam: yeme-içme
gece dilimi taksonomide var, günlük şablonda yok.

Maliyet = yol + ziyaret + bekleme_payi_dk (yeme 30, gezi 15, konaklama 20).
Yarıçap 40 km. Şehir içi hız 30 km/sa, gün 8 saat — kaba sabitler.

Skor bileşenleri (hepsi kirilim'de): deneyim ekseni eşleşmesi, aktivite +15, ucuz tercih (profil fiyat_algisi × güven), sakin tercih (kalabalık zaman cezası), kaynak puanı ×2, sponsor +30, klasik +15. Yol süresi ziyaretin 1.5 katını aşarsa skor yarıya iner. Zorunlu durak = 1000 (her zaman üstte).

Senaryo 1 — konaklama belli: konaklama_yer_id veya enlem/boylam veya konaklama_bolge_adi (ilçe merkezi sehir_ayarlari.ilce_merkezleri).

Senaryo 2 — belli değil (yeni akış, sitenin kullandığı):

POST /rotalar/olustur-alternatifler → "Dengeli keşif" / "Tarih & kültür" / "Doğa & manzara"
Kullanıcı birini seçer
POST /rotalar/{id}/konaklama-bolgesi-oner → baskın ilçe + gerekçe + örnek tesisler (otel zorunlu değil)
Eski POST /rotalar/olustur konaklama yoksa hâlâ otel önerir (geriye uyumluluk).

Sonuç kullanici_rotalari'na yazılır; commit API'dedir.

10. Site (site/)
Next.js 16 App Router, Tailwind 4, fontlar Sora + Fraunces. Dil: Karadeniz kıyısı (deniz yeşili, köpük, kumsal / deniz, yosun, gunes).

Yol	Sayfa
/
Hero + Keşfet / Bölgeler / Rota
/sehir/[anahtar]
Keşif listesi, kategori chip (konaklama yok)
/yer/[id]
Tanıtım + duygu özeti + yan bilgiler
/sehir/[anahtar]/bolgeler
İlçe/şehir profilleri
/sehir/[anahtar]/rota
RotaSihirbazi
Sihirbaz adımları: senaryo → tercihler (gün 1–5, 6 eksen slider, ucuz/sakin) → (senaryo 2 ise) alternatifler → sonuç.

API sarmalayıcı: site/src/lib/api.ts
Tipler: site/src/lib/types.ts (Python şemalarıyla hizalı tutulmalı)

.env.local: NEXT_PUBLIC_API_URL=http://127.0.0.1:8125

11. Yerel çalıştırma (bu makine)
# PostgreSQL
C:\PostgreSQL\bin\pg_ctl.exe status -D C:\PostgreSQL\data
# API — repo kökü
.\.venv_test\Scripts\python.exe -m uvicorn sunucu.api.uygulama:uygulama --host 127.0.0.1 --port 8125
# Site
cd site
npm run dev -- --port 3000
Site: http://localhost:3000
API: http://127.0.0.1:8125/docs

İlk kurulum (bir kez): alembic upgrade head + aktarım --sehir samsun.

12. Bilinen boşluklar / tuzaklar
Kök ve sunucu README'leri eski; brife ve calis.txt / site/README.md'ye güven.
dokumanlar/kategori_taksonomisi.md §6 "rota profili henüz uygulanmadı" diyor — kısmen yanlış: ucuz/sakin skorlamada duruyor; ziyaretçi profili / aile henüz yok.
Keşif listesi ilk ~60 kayıt; sayfalama UI yok.
Site içi harita yok.
sehrin_klasigi / sponsorlu_mekan kodda var, veride dolu olmayabilir → yeme-içme vitrini zayıf kalabilir.
TripAdvisor/Booking pratikte yok.
Google yorumları eksik kalabilir; duygu ağırlığı Ekşi'de.
Deneyim puanları çoğu yerde kategori varsayılanı, yere özel değil → 40 km filtresi şart.
Gece hayatı slotu yok.
Aktivite seçici sitede yok (API'de var).
Zorunlu durak UI yok.
Auth, admin, deploy, ikinci şehir yok.
site/AGENTS.md: bu Next.js sürümü eğitim verisinden farklı olabilir; site/node_modules/next/dist/docs/ oku.
UI değişince tarayıcıda akışı dene; tek ekran görüntüsü yetmez.
13. Önemli dosya haritası
ortak/sabitler.py
ortak/cografya_araclari.py
dokumanlar/kategori_taksonomisi.md
dokumanlar/veri_sozlugu.md
calis.txt
veri/ortak/sehir_ayarlari.py          # tek şehir kayıt yeri
veri/toplayicilar/*
veri/esleme/eslestirici.py
veri/duygu_analizi/{model,konu_analizi,pipeline_calistir,profil_*,bolge_*,tanitim_*,anlatim_uretici}.py
veri/kalite_kontrol/rapor_olustur.py
sunucu/veritabani/modeller.py
sunucu/veritabani/sorgular.py         # keşif vitrini burada
sunucu/veritabani/aktarim/calistir.py
sunucu/api/{uygulama,semalar,yerler_router,rotalar_router}.py
sunucu/rota_motoru/{skorlama,kumeleme,zaman_butcesi,rota_olusturucu,rota_anlatim,veri_tipleri}.py
site/src/app/page.tsx
site/src/app/sehir/[anahtar]/{page,rota/page,bolgeler/page}.tsx
site/src/app/yer/[id]/page.tsx
site/src/components/RotaSihirbazi.tsx
site/src/lib/{api,types,sabitler}.ts
site/next.config.ts                   # /backend rewrite

14. Cursor ajanına nasıl talimat yazacaksın?
Her görevde şunları ver:

Amaç (kullanıcı ne görecek / ne değişecek)
Dokunulacak katman (veri / sunucu / site / ortak+doküman)
İlgili dosyalar (yukarıdaki haritadan)
Yapılmayacaklar (kapsam dışı)
Doğrulama: UI ise tarayıcıda akış; API ise hangi uç; rota ise skor kırılımı bozulmasın
Taksonomi değişiyorsa önce doküman + ortak/sabitler.py
Örnek talimat:

site/src/app/sehir/[anahtar]/page.tsx keşif listesine "daha fazla yükle" ekle. GET /sehirler/{anahtar}/yerler zaten limit/offset/toplam_sayi dönüyor (site/src/lib/api.ts, sunucu/api/yerler_router.py). Rota motoruna, taksonomiye ve keşif filtresine dokunma. Bitince /sehir/samsun üzerinde ikinci sayfanın geldiğini tarayıcıda doğrula.

Kötü talimat: "siteyi geliştir", "harita ekle her şeyiyle", "README'ye göre Faz 3'ü başlat".

15. Kullanıcı bu sohbeti nasıl kullanacak?
Kullanıcı seninle konuşur (öncelik, UX, neyin sırası). Sen netleştirir, sonra tek bir kopyalanabilir Cursor talimatı üretirsin. Kullanıcı onu bu Cursor sohbetine yapıştırır.

Şüphede kodu uydurma; "Cursor ajana X dosyasına baktır" de. README ile çelişirse bu brifi tut.
