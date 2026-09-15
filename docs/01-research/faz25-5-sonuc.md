---
title: FAZ 25.5 — Rota kritik veri tamamlama sonuç raporu
version: "1.0"
status: Development doğrulaması; Akıllı Rota FAZ 26 handoff hazır
phase: FAZ 25.5
last_update: "2026-09-16"
depends:
  - "../00-product/00-urun-felsefesi.md"
  - "../00-product/03-karar-motoru.md"
  - "../00-product/04-sistem-mimarisi.md"
  - "../00-product/06-akilli-rota-motoru.md"
  - "../04-ai/06-dahili-nlp-sinyal-mimarisi.md"
  - "./faz25-2-sonuc.md"
  - "./faz25-3-sonuc.md"
  - "./faz25-4-sonuc.md"
affects:
  - "../00-product/06-akilli-rota-motoru.md"
  - "FAZ 26 Akıllı Rota motoru"
  - "Bugün Ne Yapalım"
  - "admin grouped review"
author: "Cursor"
---

# Karar

FAZ 25.5 development hattı **TAMAMLANDI**. Yeni genel data-readiness altyapısı açılmadı. Akıllı Rota motoru yazılmadı. Production DB yok. Commit/push yok. Yeni Alembic revizyonu yok; head **0016**.

Amaç yalnız rota-kritik boşlukları kapatmak ve FAZ 26 için unknown sözleşmesini sabitlemekti. Kalan eksikler limited/unknown olarak yönetilebilir.

**Bugün Ne Yapalım:** **GO** (kahve / yemek / tarih-kültür). 126 korpus 42 / 61 / 23; FAZ 25.4 ile aynı.

**Akıllı Rota:** **GO** — `rota_hazir` sayısı tek kriter değildir. Günlük MVP kahve + yemek + tarih/kültür + açık hava, unknown sözleşmesiyle güvenli aday üretebilir. Kahvaltı ve çalışma **desteklenmeyen yetenek**; tüm motoru bloke etmez.

## Pilot (değişmedi: 88)

| Ölçüm | FAZ 25.4 | FAZ 25.5 |
|---|---:|---:|
| mekan | 88 | 88 |
| canonical ilçe | 88/88 | 88/88 |
| koordinat | 88/88 | 88/88 |
| purpose coverage | 88/88 | 88/88 |
| public claim | 220 | **225** |
| public claim mekan | 65 | **66** |
| NLP aggregate mekan | 71/88 | 71/88 |
| gold | 9 | 9 |
| gold `rota_hazir` | 7 | 7 |

Amaç kotası aynı: kahve 18, yemek 18, tarih 18, açık hava 18, tatlı 12, eğlence 4, kahvaltı 0, çalışma 0.

## Çalışma saatleri

| | FAZ 25.4 | FAZ 25.5 |
|---|---:|---:|
| yayımlanmış known | 11 | **16** |
| yalnız dahili / invalid | 1 | 1 |
| unknown (yok) | 76 | 71 |
| published coverage | %12,5 | **%18,2** |

Parser `v2`: `known` / `partially_known` / `unknown` / `invalid` / `stale`. Tahmin yok. Google yorumundan saat türetilmez. Desteklenen sözdizim: `Mo-Fr 09:00-18:00`, `Sa-Su 10:00-22:00`, `24/7`, gün `off`, virgüllü aralık. PH atlanır → `partially_known`. Gece taşan / mevsim / yorum → `invalid`. `acik_iddiasi_kurulabilir` yalnız taze `known`.

Yeni 5 kayıt resmi KTB kaynağı + birinci el gözlem → inceleme → yayın (kör otomatik yayın yok):

| Mekan | Saat | Kaynak |
|---|---|---|
| Gazi Müzesi | `Mo-Su 08:30-16:30` | samsun.ktb.gov.tr TR-216752 |
| Samsun Kent Müzesi | `Mo 13:00-17:00; Tu-Su 08:00-17:00` | TR-230223 |
| Amazon Köyü | `Mo 12:00-17:00; Tu-Su 08:30-17:00` | TR-230223 |
| Bandırma Gemi-Müze | `Mo 12:00-16:45; Tu-Su 08:00-16:45` | TR-362756 |
| Canik Oyuncak Müzesi | `Tu-Sa 10:00-16:00` | TR-230223 |

Her kayıt branch/source/çekilme/parser `v2`/ham referans/timezone `Europe/Istanbul`/180 gün tazelik taşır.

Uydurulmayanlar: cami, anıt, köprü, çınar, höyük, mağara, Ambarköy (kurum saati birleştirilmedi), Arkeoloji (KTB taşınma — hizmet dışı; açık saat yayımlanmadı), Samsun Müzesi (güncel haftalık yok). Mevsimsel Bandırma yaz/kış ve TL ücret fact değil.

## Tarihi/kültürel

FAZ 25.4’te 18 mekanın `rota_hazir=0` nedeni: OSM `opening_hours` yok; identity/koordinat/amaç tam.

| | FAZ 25.4 | FAZ 25.5 |
|---|---:|---:|
| `rota_hazir` | 0 | **5** |
| `rota_sinirli` | 18 | 13 |

Reason code: 13 `calisma_saati_eksik`; 18 `ziyaret_suresi_fact_degil` (planlama tahmini fact değildir, hard block değildir). Kimlik/yayın sorunu 0.

`rota_hazir` beş resmi saatli müze. Kalan 13 `rota_sinirli` + «Gitmeden önce saatini doğrula».

## Ziyaret süresi

| Kaynak | n | Fact mi? |
|---|---:|---|
| `dogrulanmis_sure` | 0 | Evet |
| `kullanici_secimi` | 0 | Hayır |
| `planlama_tahmini` | 88 | Hayır |
| `bilinmiyor` | 0 | Hayır |

Kategori aralığı `minimum_dk` / `tipik_dk` / `maksimum_dk`. Kullanıcıya «Planlama için yaklaşık 45–75 dakika ayırdık» denir; «60 dakika sürer» denmez. Public fact değildir.

## Rota hazırlık ve unknown sözleşme

| | FAZ 25.4 | FAZ 25.5 |
|---|---:|---:|
| `rota_hazir` | 11 | **16** |
| `rota_sinirli` | 77 | **72** |
| `kesif_adayi` | 0 | 0 |
| `rota_kapali` | 0 | 0 |

`rota_hazir`: kimlik + koordinat + ilçe + amaç + yayın + yayımlanmış **known** saat. Unknown/partial/stale/invalid saat → `rota_sinirli`, hard block değil.

| Konu | Davranış |
|---|---|
| çalışma saati unknown | `limited_route` uyarı; açık iddiası yok |
| ziyaret süresi estimate | `limited_route`; public fact değil |
| geçiş unknown | `limited_route` |
| rezervasyon unknown | `limited_route` |
| geçici kapanış unknown | `limited_route`; açık varsayılmaz |
| kimlik karantina / geçersiz koordinat / pasif şube | `hard_block` |

## Senaryo A–F (motor yazılmadan aday uygunluk)

| | uygun | rota_hazir | rota_sinirli | saat known | süre tahmini | blok |
|---|---:|---:|---:|---:|---:|---:|
| A Atakum kahve+yemek | 8 | 1 | 7 | 1 | 8 | 0 |
| B Atakum kahve+sakin | 1 | 1 | 0 | 1 | 1 | 0 |
| C İlkadım tarih+yemek | 13 | 4 | 9 | 4 | 13 | 0 |
| D Samsun tarih+kahve+yemek | 54 | 10 | 44 | 10 | 54 | 0 |
| E yarım gün (aynı havuz) | 54 | 10 | 44 | 10 | 54 | 0 |
| F tam gün (aynı havuz) | 54 | 10 | 44 | 10 | 54 | 0 |

Amaç kovaları (eligible = hazir+sinirli): kahve 18 (3+15), yemek 18 (2+16), tarih 18 (5+13), açık hava 18 (4+14), tatlı 12 (1+11). B sakin tercih ince (NLP preference 1 Atakum kafe); hard block değil, sakin-zorunlu rota zayıf.

Kahvaltı/çalışma 0: MVP dışı unsupported.

## Review kuyruğu

Amaç kuyruğu bitirmek değildi. Pending **1558 → 1558**. Triyaj yeniden yazıldı: `opening_hours` + rota-kritik + pilot + güçlü kimlik önde (`calisma_saatleri` +25, pilot +40). 5 resmi saat dosyası incelenip kapatıldı; bekleyen net değişmedi.

Birinci el bu faz: **5** resmi saat observation→evidence→review→publication. Gold havuzu 9’da bırakıldı.

## 126 korpus

| | FAZ 25.4 | FAZ 25.5 |
|---|---|---|
| parse | 126/126 | 126/126 |
| ürün | success 42, insufficient 61, clarification 23 | **aynı** |
| fact / deneyim | 44 / 3 | 44 / 3 |
| duplicate / kirli isim | 0 / 0 | 0 / 0 |

Bariz yanlış öneri artışı yok.

## Canlı

- SITE `https://qk4cmqnw-3000.euw.devtunnels.ms/` HTTP 200
- API `https://qk4cmqnw-8125.euw.devtunnels.ms/docs` HTTP 200; yerel `/docs` 200
- Admin login `https://qk4cmqnw-3000.euw.devtunnels.ms/admin/login` form görünür
- Playwright: kahve 5 kart; tarih sorgusu Amazon Köyü / Gazi Müzesi / Kent Müzesi; Gazi detay **Doğruladığımız → calisma saatleri `Mo-Su 08:30-16:30`**
- Yerel API POST kahve/tarih/yemek success, n=5

## Testler

- Backend pytest: **220** geçti
- FAZ 25.5 parser/unknown/süre/senaryo/kuyruk/resmi eşleme: geçti
- Grup inceleme birinci el `site_ici` saat: geçti
- Frontend vitest: **21** geçti; `tsc --noEmit` temiz; ESLint 0 error / 2 tarihî `<img>`
- Next.js build: başarılı
- Ruff (bu faz dosyaları): temiz
- Alembic current=heads=**0016**; `alembic check` yeni upgrade yok
- `git diff --check`: whitespace hatası yok (yalnız `sehir_ayarlari.py` LF/CRLF uyarısı)

## Açık riskler

- Çalışma saati hâlâ 16/88 known; çoğunluk `rota_sinirli` uyarı ile kullanılır
- Doğrulanmış ziyaret süresi 0; planlama tahmini fact değildir
- Bağımsız saha gold yok
- Senaryo B sakin kahve ince
- Arkeoloji müzesi hizmet dışı gerçeği yayımlanmış kapanış fact’i değil
- Geçiş/ulaşım süresi yok (FAZ 26 unknown)
- Canlı tunnel POST zaman aşımı; GET ve yerel POST + Playwright doğrulandı

## FAZ 26 handoff

Akıllı Rota motoru bu belgedeki sözleşmeyi yeniden tasarlamasın.

**Desteklenen amaçlar:** `kahve_icmek`, `yemek_yemek`, `tarihi_kulturel_ziyaret`, `acik_hava`, `tatli_yemek` (ince).

**Desteklenmeyen:** `kahvalti`, `calisma`. Sessiz/sakin zorunlu tercih ince; opsiyonel uyarı.

**`rota_hazir` / `rota_sinirli`:** hazir = known yayımlanmış saat + temel kimlik/koordinat/ilçe/amaç/yayın. sinirli = aynı temel, saat unknown/partial/stale/invalid; günlük diziye girebilir.

**Opening hours unknown:** hard block değil. «Gitmeden önce saatini doğrula». Şimdi açık iddiası yok.

**Visit duration:** verified yoksa `planning_estimate` aralığı. Public fact değil.

**Hard gate:** karantina, geçersiz koordinat, pasif şube. Rezervasyon/geçici kapanış unknown → uyarı.

**MVP senaryolar:** A, C, D ve E/F (aynı günlük havuz, süre dilimi motor işi). B sakin-zorunlu olarak zayıf. Çok günlük yok.

# Sonuç

**FAZ 25.5: TAMAMLANDI**

**BUGÜN NE YAPALIM: GO**

**AKILLI ROTA: GO**
