---
title: FAZ 25.4 — Karar coverage ve pilot mekan kalitesi sonuç raporu
version: "1.0"
status: Development doğrulaması; Akıllı Rota geçişi engelli
phase: FAZ 25.4
last_update: "2026-09-16"
depends:
  - "../00-product/00-urun-felsefesi.md"
  - "../00-product/03-karar-motoru.md"
  - "../00-product/04-sistem-mimarisi.md"
  - "../00-product/06-akilli-rota-motoru.md"
  - "../04-ai/06-dahili-nlp-sinyal-mimarisi.md"
  - "./faz25-2-sonuc.md"
  - "./faz25-3-sonuc.md"
  - "../09-business/14-urun-ozellik-haritasi.md"
  - "../05-engineering/15-uygulama-fark-analizi-ve-mvp-uygulama-plani.md"
affects:
  - "../00-product/06-akilli-rota-motoru.md"
  - "admin grouped review"
  - "Bugün Ne Yapalım"
  - "pilot coverage"
author: "Cursor"
---

# Karar

FAZ 25.4 development hattı **TAMAMLANDI**. Samsun için veriye dayalı 88 mekanlık pilot havuz, OSM düşük risk grup inceleme (kör otomatik yayın yok), tamamlık matrisi ve iç rota hazırlık **durumu** kuruldu. Akıllı Rota motoru yazılmadı. Production DB yok. Commit/push yok. Yeni Alembic revizyonu yok; head **0016**.

**Bugün Ne Yapalım:** sınırlı **GO** (kahve / yemek / tarih-kültür). FAZ 25.3 kalite korunur; 126 success 41→42.

**Akıllı Rota:** **NO-GO.** `rota_hazir` 11/88; tarihi/kültürel 0; kahvaltı ve çalışma kovaları veri yetersiz diye havuza alınmadı; yayımlanmış çalışma saati %12,5.

## Pilot seçim mantığı

1719 kaydın tamamı doldurulmadı. Adaylar aktif şube + öneriye uygun kimlik + geçerli koordinat + geçerli isim; `internet_kafe` ve konaklama atlanır. Puan: kimlik sınıfı, ilçe, OSM yapısal aile, NLP preference, public claim, OSM saat. Amaç kotası 18, ilçe kotası 24, havuz 50–150. Zayıf kova (4'ten az ve puan 120 altı) doldurulmaz.

Çıkan havuz **88**. Keyfi 100'e tamamlanmadı.

Gold: yalnız `güclü`/`dogrulanmis` ve OSM yapısal aile (`calisma_saatleri`, `wifi`, `acik_alan`, `otopark`, `rezervasyon`). Sayı için yer_turu-only doldurma yok. **9** gold; 7’si `rota_hazir`.

## Kategori / ilçe dağılımı

| Amaç | n | Not |
|---|---:|---|
| kahve_icmek | 18 | kota |
| yemek_yemek | 18 | kota |
| tarihi_kulturel_ziyaret | 18 | kota |
| acik_hava | 18 | kota |
| tatli_yemek | 12 | yeterli kova |
| eglence | 4 | ince; saklanmadı çünkü ≥4 ve yüksek puanlı aday var |
| kahvalti | 0 | NLP/etiket kova 3'ten az; saklandı |
| calisma | 0 | `calisma_uygunlugu` preference yok; saklandı |

İlçe: İlkadım 24 (kota), Atakum 21, Canik 8, Çarşamba 6, Bafra 5, Havza 5, Kavak 4, diğerleri 1–3. 15 canonical ilçe. Kimlik: güclü 78, kullanılabilir 10, karantina 0.

Koordinat ve `ilce_id` 88/88 `biliniyor`.

## Public fact / opening_hours / route-critical

Grup inceleme öncesi public claim 5 mekan / 24 iddia (25.3). Sonrası 65 mekan / 220 iddia (şehir; pilotda public_claim 63).

Pilot matris (88):

| Kolon | biliniyor | yalniz_dahili | bilinmiyor |
|---|---:|---:|---:|
| kimlik / ilçe / koordinat / amaç | 88 | 0 | 0 |
| calisma_saatleri | 11 | 1 | 76 |
| wifi | 6 | 0 | 82 |
| acik_alan | 4 | 3 | 81 |
| otopark | 0 | 31 | 57 |
| erisilebilirlik / aile / çocuk / çalışma / sessizlik | 0 | 0 | 88 |
| manzara | 0 | 13 | 75 |
| fiyat | 0 | 40 | 48 |
| ziyaret_suresi | 0 | 0 | 88 (sezgisel fact değil) |

Çalışma saati: OSM parse + sözdizimi; gece taşan / PH / yorum **tahmin edilmez**. 11 geçerli saat yayımlanıp normalize + `zaman_kapsami=haftalik` yazıldı. 1 OSM saat invalid → `yalniz_dahili`.

## Internal NLP (pilot 88)

71 mekanda en az bir aggregate. Preference-eligible: sessizlik 24, otopark 16, kalabalık 14, aile 12, fiyat 6, manzara 5, çocuk 5, açık alan 1. `calisma_uygunlugu` ve `kahvalti` 0. Güçlü sessizlik 31 / orta 14 / zayıf 14 / yok 29. Kamusal skor yok.

## Rota hazırlık durumu (skor değil)

| Durum | n | Anlam |
|---|---:|---|
| rota_hazir | 11 | kimlik+koordinat+ilçe+amaç+yayın uygun; yayımlanmış geçerli saat |
| rota_sinirli | 77 | temel uygun; saat unknown veya yalnız dahili |
| kesif_adayi | 0 | |
| rota_kapali | 0 | karantina bu havuzda yok |

Reason code `kirilim` içinde; `kamusal_skor: false`.

Simülasyon (motor yok): kahve 3 hazır, yemek 2, tatlı 1, açık hava 4, eğlence 1, **tarih 0**. Atakum 6 hazır / 21; İlkadım 4 / 24. Kahve+yemek+tarih senaryosu: 5 hazır, 49 sınırlı.

## Review kuyruğu

| | FAZ 25.3 | 25.4 başı | 25.4 sonrası |
|---|---:|---:|---:|
| bekleyen | 1772 | 1754 | 1558 |
| dusuk_risk | 1223 | 1223 | 1029 |
| yuksek_risk | 528 | 528 | 528 |
| orta_risk | 3 | 3→1 | 1 |

Pilot grup inceleme: 196 onay, 8 yayın kapısı hatası, 0 kör otomatik yayın. Tekerlekli sandalye ve `amac_destegi` grup dışı. Aile kırılımı: saat 11, wifi 6, açık alan 4, yer_turu 62, telefon 31, web 26, adres 56.

## First-party / gold

Admin gözlem formu doğrudan yayınlamaz; eksik aileler pilot sekmesinden forma taşınır. Sahada uydurma wifi/sessizlik yazılmadı.

First-party kontrollü gold = OSM yapısal + insan grup incelemesi: **9 mekan** (Günevi, Pablo Artisan, Yemen Kahvesi, Peçko, Chocolabs, Çarşı Restoran, Yeşiloğlu Çakallı, Paribu Cineverse, İnci Plajı). 7 `rota_hazir`. 20–40’a kötü kayıt basılmadı.

## 126 / 30 regresyon

Aynı development DB; motor yeniden ölçüldü.

| Ölçüm | FAZ 25.3 | FAZ 25.4 |
|---|---|---|
| 126 parse | 126/126 | 126/126 |
| 126 ürün | success 41, insufficient 62, clarification 23 | **success 42**, insufficient 61, clarification 23 |
| 126 fact / deneyim | 44 / 3 | 44 / 3 |
| duplicate / kirli isim | 0 / 0 | 0 / 0 |
| benzersiz önerilen yer | (25.3 iz) | 18 |
| published claim / mekan | 24 / 6 | 220 / 65 |
| 30 gold ürün | success 10, insufficient 14, clarification 6 | **aynı 10 / 14 / 6** |
| 30 fact / deneyim | 12 / 1 | 12 / 1 |

Bariz yanlış tepe: kahve citywide hâlâ **Günevi Atölye /Cafe**; yemek **Samsun Çarşı Restoran**; tarih (30) Amazon Köyü / Gazi Müzesi / Kent Müzesi. `.` ve internet kafe sızıntısı 0. Aile/çalışma/çocuk/tatlı/kahvaltı/wifi hard hâlâ insufficient veya clarification — coverage bu sorguları “success”e çevirmedi (beklenen).

## Akıllı Rota GO eşiği (veriden)

Uydurma kota yok. Bu dağılımla GO için asgari savunulabilir çizgi:

1. Çekirdek amaçlarda (kahve, yemek, **tarihi/kültürel**) her birinde ≥ birkaç `rota_hazir` (saat yayımlı).
2. Atakum ve İlkadım’da her çekirdek amaç için en az bir `rota_hazir`.
3. `rota_hazir` / `rota_sinirli` ayrımı korunur; saat unknown durak `rota_hazir` sayılmaz.
4. Kimlik karantina sızıntısı 0; 126/30 kalite 25.3’ten gerilemez.
5. Kahvaltı/çalışma ancak veri kovası oluşursa dahil.

Bugünkü gerçek: (1) tarih 0, (2) İlkadım tarih 0, (3) 11/88 hazır, (4) kalite korunur, (5) kova yok. **NO-GO.**

## Canlı

Yerel API 8125 FAZ 25.4 koduyla; site 3000. Devtunnel: SITE `https://qk4cmqnw-3000.euw.devtunnels.ms/` · API `https://qk4cmqnw-8125.euw.devtunnels.ms/`.

Doğrulama (16 Eylül 2026):

- Yerel ana sayfa `#bugun-ne-yapalim`: partner+kahve → Günevi; aile+yemek 390px → Samsun Çarşı Restoran; detay + bağlama dönüş.
- Keşfet `q=kafe`: Günevi, kahve gerekçesi. Rota planlayıcı formu duruyor (motor bu fazda yok).
- Admin `/admin` → `/admin/login` (e-posta/parola). Operasyon kullanıcısının parolası saklanmadı; paneli oturum açmadan smoke edilemedi. Canlı `/admin` oturum doğrulamasında takıldı (tunnel API yavaş/timeout); yerel login formu göründü.
- Canlı SITE HTTP 200; kahve sorgusu success, 5 kart, tepe Günevi. Canlı API `/docs` 200; `POST /v1/bugun-ne-yapalim` success. İkinci doğrudan tunnel POST zaman aşımı (yavaş/limit); SITE proxy yolu çalıştı.
- Playwright e2e: `bugun-ne-yapalim` + `faz25-2-senaryolar` 5/5.

## Riskler

1. `rota_hazir` yalnız OSM saat sözdizimi geçen 11 yer; resmi işletme saati adaptörü yok.
2. `yer_turu`/telefon/adres grup yayını public claim sayısını şişirir; gold bu yüzden yapısal OSM ile daraltıldı.
3. Otopark NLP `yalniz_dahili`; public fact değil.
4. Ziyaret süresi yalnız kategori sezgiseli (planner yedegi, `fact_mi=false`).
5. 8 grup kayıt yayın kapısında kaldı (telefon/web/adres).
6. Bağımsız saha gold yok.
7. Hero “Rotanı kur” bu fazda dokunulmadı.

## GO / NO-GO

**FAZ 25.4 TAMAMLANDI.**

**Bugün Ne Yapalım — sınırlı GO.** Kahve/yemek/tarih; 25.3 sıralama bozulmadı.

**Akıllı Rota — NO-GO.** Pilot zenginleşti ama günlük dizi için saat+amaç+ilçe birlikte `rota_hazir` değil.

## Bu dokümanın bağlı olduğu belgeler

- [03 Karar Motoru](../00-product/03-karar-motoru.md)
- [04 Sistem Mimarisi](../00-product/04-sistem-mimarisi.md)
- [06 Akıllı Rota Motoru](../00-product/06-akilli-rota-motoru.md)
- [FAZ 25.3 sonuç](./faz25-3-sonuc.md)

## Bu dokümanın etkilediği belgeler

Akıllı Rota geçiş kararı, admin inceleme kapasitesi, Bugün Ne Yapalım coverage.

## Bundan sonra okunması gereken belge

[06 Akıllı Rota Motoru](../00-product/06-akilli-rota-motoru.md) — uygulanmış özellik değildir. Resmi saat kaynağı ve tarih `rota_hazir` boşluğu kapanmadan motor yazılmamalıdır.
