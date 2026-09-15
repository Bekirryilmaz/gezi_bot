---
title: FAZ 25.2 — Dahili NLP ve Samsun Bilgi Temeli sonuç raporu
version: "1.0"
status: Development doğrulaması; ürün geçişi engelli
phase: FAZ 25.2
last_update: "2026-09-15"
depends:
  - "../00-product/00-urun-felsefesi.md"
  - "../00-product/01-bilgi-mimarisi.md"
  - "../00-product/02-product-language.md"
  - "../00-product/03-karar-motoru.md"
  - "../00-product/04-sistem-mimarisi.md"
  - "../04-ai/05-ai-bilgi-motoru.md"
  - "../04-ai/06-dahili-nlp-sinyal-mimarisi.md"
  - "./faz25-1-kurtarma-sonuc.md"
  - "./faz25-1-oneri-gold.md"
affects:
  - "../00-product/06-akilli-rota-motoru.md"
  - "../02-ux/07-ux-karar-akislari.md"
  - "Bugün Ne Yapalım"
  - "Karar Motoru"
  - "admin review"
author: "Cursor"
---

# Karar

FAZ 25.2 development hattı **uygulandı ve ölçülmüştür**. Google yorumları yalnız dahili aday/aggregate projection'da işlenir; kamusal DTO'ya ham metin, yazar, yorum sayısı, duygu yüzdesi veya iç skor sızmaz. Yayımlanmış yer kategorisi açık eşlemelerde amaç fact'idir; review deneyim sinyali hard PASS/FAIL üretmez. Public claim adedi değişmedi (24 kayıt / 6 mekan); otomatik yayın yoktur.

Akıllı Rota geçişi **NO-GO**. Gerekçe: amaç coverage genişlese de sıralama kalitesi düştü, aile/çocuk/çalışma/manzara/kahvaltı/tatlı için yayımlanmış fact yok, deneyim sinyali tercihte zayıf kaldı, OSM inceleme kuyruğu şişti, bağımsız saha gold'u yok, production DB'ye dokunulmadı.

## Before / after — Bugün Ne Yapalım

Aynı development DB; FAZ 25.1 ölçüleri `faz25-1-kurtarma-sonuc.md` ve `faz25-1-oneri-gold.md` kaynaklıdır.

| Ölçüm | FAZ 25.1 | FAZ 25.2 |
|---|---:|---:|
| 126 korpus parse uyumu | 126/126 | 126/126 |
| 126 ürün durumu | success 23, insufficient 80, clarification 23 | success 41, insufficient 62, clarification 23 |
| 126 fact destekli sorgu | yayımlanmış claim ile sınırlı | 44 |
| 126 deneyim destekli sorgu | 0 (karara bağlı değil) | 3 |
| 126 coverage-unknown (insufficient) | 80 | 62 |
| 30 gold ürün durumu | success 7, insufficient 18, clarification 5 | success 10, insufficient 14, clarification 6 |
| 30 gold fact / deneyim | kahve/yemek yayınlı claim | fact 12, deneyim 1 |
| Public claim / mekan | 24 / 6 | 24 / 6 (değişim 0) |
| NLP AdayGozlem | 0 | 28.803 dahili aday |
| Dahili aggregate | 0 | 1.990 (preference_eligible 568) |
| Canonical ilce_id | 26/1719 | unique eşleşme 1712; backfill yazılan 1686; atlanan 33; zero 7 |

Success artışı kategori→amaç fact'inden gelir (`kafe/kahve_uzmanlik→kahve_icmek`, yemek türleri→`yemek_yemek`, `tarihi_kulturel→tarihi_kulturel_ziyaret`). Bu, sohbet/aile/çocuk uygunluğunun doğrulandığı anlamına gelmez.

## NLP hattı (19.609 Google yorum)

Dry-run ve gerçek koşu `faz25.2-nlp-v1:samsun` ardından güven kalibrasyonu `faz25.2-nlp-v1:samsun-guven`. BERT cache hit 19.609; yeni inference 0; error 0.

- İşlenen 19.609; eşleşen 19.609; no-match 0; skipped 2.906; low-confidence 10.894
- Aday 28.794 koşu + persist sonrası 28.803
- Tür: sentiment 24.715, experience 3.321, fact 758
- Kullanım: aktif 14.058 / karantina 14.745 (karantina çoğunlukla `genel_duygu`)
- Aile (aday): genel_duygu 14.736, yemek 5.537, sessiz_ortam 2.679, fiyat_algisi 2.475, kalabaliklik 829, manzara 781, otopark 664, kahvalti 570, aile_uygunlugu 399, cocuk_uygunlugu 97, acik_alan 17, canli_muzik 6, wifi 3, calisma_uygunlugu 1
- Süre: gerçek yeniden koşu ~65 s (500'lük batch; batch 1,2–1,8 s)
- Branch audit: 1.104 Google kaynak, 1.010 şube, 62 çoklu kaynak, 0 fiziksel şube şüphesi; `branch_ambiguous` 0

Sentiment karar girdisi değildir. Unique-review tertilleri: zayıf max 1, orta max 2; güven zayıf 1.057 / orta 440 / güçlü 493. Weak/uncalibrated preference_eligible değildir ve hard kapıya girmez. Tarihsiz + tek kaynak (`source diversity=1`) kırılımda görünür. Yorumların tamamında tarih bilinmiyor.

Pilot: 50 yer, 14 kategori; kalite eşiğini geçmeyen adayla sayı doldurulmadı.

## Yapısal OSM ve ilçe

- OSM API 0.6: 854 kaynak, 843 etiket, 92 yer `ozellikler` güncellendi. `yes/no/limited/required` birbirine çevrilmedi.
- Alanlar: cuisine 59, opening_hours 36, wifi/internet_access 22, outdoor/acik_alan 13, wheelchair 4, reservation 2.
- Claim-candidate yazımı mevcut public akışı kullandı: yeni gözlem 1.805, yeni claim 1.581, yeni inceleme 1.587, hak nedeniyle 0. Otomatik yayın yok; inceleme kuyruğu şişti (operasyon riski).
- İlçe: Nominatim polygon (Overpass 504), ODbL provenance + HGM “resmî nitelik taşımaz” notu. 17/17 tam küme. ST_Covers/Contains: unique 1.712, zero 7; yalnız unique interior backfill.

## 30 gold — masa başı inceleme

Kaynak: `veri/cikti/raporlar/dahili_nlp/samsun_gold_30.json`. Parser 30/30 beklenen alan. Bu saha araştırması değildir.

Citywide kahve (1, 2, 8, 24): **success / fact**. Liste alfabetik kafe kimliği (`ALAÇAM Küçük Mucizeler`, `Adalet Cafe`, `Adana Sofrasi`, `Adress İnternet Cafe`, `Alaçatı Muhallebicisi`). FAZ 25.1'deki Günevi/Starbucks/Kollekt tepe sırayı kaybetti. `Adana Sofrasi` ve internet kafe partner kahve/sohbet için bariz alakasızlık riskidir. Sohbet yayımlanmış fact değildir.

Atakum kahve (9, 10): **insufficient / fact**, n=2 (`Günevi Atölye /Cafe`, `Kollekt`). Sayı doldurulmadı.

Aile yemek (5, 6, 25, 27): **success / fact**. Liste: `.`, `100.YIL TEKER RESTAURANT`, çift `153 Restoran`, `19 Mayıs Lokantası`. Aile uygunluğu yayımlanmamış; ürün aileyi doğrulamadan yemek kategorisiyle geçti. `.` isimli kayıt ve yinelenen 153 kimlik bariz veri hatasıdır.

Birlikte vakit / eğlence (3, 4, 7): **insufficient**. Uydurma yok.

Çalışma / sakin kafe / çocuk / manzara oturma (11–14): **insufficient**. Deneyim sinyali hard PASS üretmedi.

Fiyat / mesafe / otopark / wifi / “bu akşam” / “şimdi açık” (15–20): **clarification**. Hard wifi/otopark review'dan PASS almadı.

Tatlı / kahvaltı / müze (21–23, 28–29): **insufficient**. Kategori amaç eşlemesi bu sorguları doldurmadı.

Sakin kahve (26): **success / fact + deneyim**. Sessiz ortam preference_eligible sıralamayı kaydırdı (`Anka Cafe de Çiçek`, `Bİ DÜNYA KAHVE` vb.). Sayı/skor/kaynak adı kullanıcı metninde yok.

Aile + tarihi (30): **success / fact** (müze/anıt listesi). Tek başına “müze gezmek” (23) hâlâ insufficient; alt tür ve arama havuzu asimetrik.

Hard durum: review deneyimi hiçbir sorguyu hard FAIL/PASS ile kilitlemedi. Structured/public fact, çelişen zayıf deneyime üstün gelir (birim test).

## Karar Motoru ve sızıntı kapısı

- Amaç fact yalnız taksonomideki `ALT_KATEGORI_AMAC_ESLEMESI` ile.
- `deneyim_sinyali_destekliyor` public gerekçe kodu; sayı/yüzde yok.
- Public deny-list: ham metin, yazar, kaynak review ID, count/share, sentiment %, iç güven.
- Admin: `GET /v1/admin/dahili-sinyaller`, `POST /v1/admin/gozlemler` (RBAC/CSRF/şehir/audit). First-party gözlem `Gozlem → Iddia → IncelemeDosyasi`; `public=true` yok.
- UI: “Doğruladığımız / Deneyim sinyali / Henüz doğrulayamadığımız”.

## Performans ve kapı

- Alembic: current/heads/check `0015`; yeni autogenerate yok. Development upgrade yapıldı; sinyal verisi varken destructive downgrade çalıştırılmayacak.
- Backend pytest: 172 geçti (önceki 429/MultipleResultsFound yalıtıldı: yazma sayacı sıfırlama + izole OSM test yeri).
- Frontend: vitest 20, typecheck, lint 0 error / 2 tarihî `<img>` uyarısı, `next build` geçti.
- `git diff --check` temiz.
- NLP testleri extractor/negation/pipeline resume ile birlikte tam suite içinde.
- Canlı: SITE `https://qk4cmqnw-3000.euw.devtunnels.ms/` HTTP 200; API `https://qk4cmqnw-8125.euw.devtunnels.ms/docs` HTTP 200; yerel `127.0.0.1:8125/docs` 200. Yerel API FAZ 25.2 koduyla yeniden başlatıldı (eski süreç yemek için n=1 insufficient, yeni süreç n=5 success). Playwright MCP: partner+kahve+sohbet canlı SITE’de success, 5 kart, sohbet unknown; Adalet Cafe detayında “Doğruladığımız / Deneyim sinyali / Henüz doğrulayamadığımız”; 390px oturum restorasyonu; Swagger başlığı Şamandıra API. Detay sayfası Bugün bağlamını `kesfet:aktif-baglam` anahtarıyla aradığı için kişisel kahve fact’i “doğrudan açıldı” metnine düştü — başlıklar var, bağlam bağlanması eksik.
- Playwright: yerel `e2e/faz25-2-senaryolar.spec.ts` 1280+390 bağlı senaryolar 1 passed (1,8 dk; partner+kahve+sohbet, aile+yemek, çalışma, çocuk, sakinlik, manzara, kahvaltı, tatlı). Önceki paralel koşu anonim yazma limiti (20/dk) yüzünden 429 aldı; spec 429'da 61 sn bekler. `bugun-ne-yapalim` ve `kesfet-karar` e2e 5 passed. Yemek e2e, kategori fact sonrası 3–5 kart bekler (eski “yalnız 1 kart” beklentisi kaldırıldı).
- Korpus 126 yerel motor ~16,6 s; gold 30 ~6 s.

Production DB yok. Commit/push yok.

## Riskler

1. Kategori amaç fact şehir genelinde alfabetik kafe/restoran listesi üretir; yayınlı kaliteli şubeler tepe sırayı kaybedebilir.
2. Kirli kimlik: `.` isim, yinelenen `153 Restoran`, internet kafe / Adana Sofrası kahve önerisi.
3. OSM structured backfill 1.587 pending inceleme üretti; admin kapasitesi aşılabilir.
4. Overpass güvensiz; ilçe polygon Nominatim türevi. HGM resmî değil.
5. Tüm Google yorumları tarihsiz; temporal_unknown kalıcı.
6. `calisma_uygunlugu` aday 1; çocuk/kahvaltı/tatlı public fact yok.
7. Anonim yazma limiti e2e ve canlı formu aynı anda yorar.
8. Hero metninde “Rotanı kur” ürün CTA'sı duruyor; marka “Rotam” değil.

## Akıllı Rota GO/NO-GO

**NO-GO.** Günlük rota, konaklama ve çok günlük plan bu fazın kapsamı dışındadır. Bugün Ne Yapalım kahve/yemek/tarih amaçlarında daha çok success üretir ama sıralama ve aile/çalışma/tatlı boşlukları ürün geçişini taşımaz. Sonraki iş: kimlik temizliği, sıralamada yayınlı claim önceliği, OSM kuyruk triyajı, saha gold.

## Bu dokümanın bağlı olduğu belgeler

- [00 Ürün Felsefesi](../00-product/00-urun-felsefesi.md)
- [01 Bilgi Mimarisi](../00-product/01-bilgi-mimarisi.md)
- [02 Product Language](../00-product/02-product-language.md)
- [03 Karar Motoru](../00-product/03-karar-motoru.md)
- [04 Sistem Mimarisi](../00-product/04-sistem-mimarisi.md)
- [05 AI Bilgi Motoru](../04-ai/05-ai-bilgi-motoru.md)
- [06 Dahili NLP Sinyal Mimarisi](../04-ai/06-dahili-nlp-sinyal-mimarisi.md)
- [FAZ 25.1 kurtarma](./faz25-1-kurtarma-sonuc.md)
- [FAZ 25.1 gold](./faz25-1-oneri-gold.md)

## Bu dokümanın etkilediği belgeler

Akıllı Rota motoru referansı, UX karar akışları, admin inceleme kapasitesi, Bugün Ne Yapalım ölçümleri.

## Bundan sonra okunması gereken belge

[Dahili NLP Sinyal Mimarisi](../04-ai/06-dahili-nlp-sinyal-mimarisi.md). Planlanan saha öneri doğrulaması henüz yazılmamıştır.
