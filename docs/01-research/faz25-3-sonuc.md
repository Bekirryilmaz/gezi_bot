---
title: FAZ 25.3 — Kimlik temizliği ve öneri sıralama kalitesi sonuç raporu
version: "1.0"
status: Development doğrulaması; Akıllı Rota geçişi engelli
phase: FAZ 25.3
last_update: "2026-09-16"
depends:
  - "../00-product/00-urun-felsefesi.md"
  - "../00-product/01-bilgi-mimarisi.md"
  - "../00-product/02-product-language.md"
  - "../00-product/03-karar-motoru.md"
  - "../00-product/04-sistem-mimarisi.md"
  - "../04-ai/06-dahili-nlp-sinyal-mimarisi.md"
  - "./faz25-2-sonuc.md"
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

FAZ 25.3 development hattı **TAMAMLANDI**. Kirli kimlik karantinaya alındı, aynı normalize isim tepe listede tek kaldı, kategori→amaç yalnız `direct_purpose_fact` ile amaç üretir, sıralama kalite/fact/deneyim önceliklidir, OSM kuyruğu triyajlandı, 0015 veri korumalı downgrade fail-closed çalışır. Production DB yok. Commit/push yok. Mekan adına gömülü kural yok.

**Bugün Ne Yapalım:** sınırlı **GO** (kahve / yemek / tarih-kültür; sıralama 25.2 alfabetik sapmasından kurtuldu). Genel günlük ihtiyaç ürünü **değil**.

**Akıllı Rota:** **NO-GO**.

## Before / after

Aynı development DB. 25.1/25.2 ölçüleri `faz25-1-kurtarma-sonuc.md` ve `faz25-2-sonuc.md` kaynaklıdır.

| Ölçüm | FAZ 25.2 | FAZ 25.3 |
|---|---:|---:|
| 126 korpus parse uyumu | 126/126 | 126/126 |
| 126 ürün durumu | success 41, insufficient 62, clarification 23 | success 41, insufficient 62, clarification 23 |
| 126 fact destekli sorgu | 44 | 44 |
| 126 deneyim destekli sorgu | 3 | 3 |
| 126 duplicate öneri | ölçülmedi | 0 |
| 126 kirli isim sızıntısı | `.` yemek listesinde | 0 |
| 30 gold ürün durumu | success 10, insufficient 14, clarification 6 | success 10, insufficient 14, clarification 6 |
| 30 gold fact / deneyim | 12 / 1 | 12 / 1 |
| Public claim / mekan | 24 / 6 | 24 / 6 (değişim 0) |
| Kimlik sınıfları (aktif şube) | yok | güclü 179, kullanılabilir 1522, şüpheli 10, karantina 8 |
| `internet_kafe` kayıt | 0 (kafe altında) | 4 |
| İnceleme kuyruğu triyaj | yok | düşük 1223, yüksek 528, orta 3, boş 108; bekleyen 1772 |
| Alembic head | 0015 | 0016 |

Coverage sayıları aynı kaldı; değişen şey **kimin tepe sıraya geldiği**. Success hâlâ kategori→amaç fact'inden gelir. Aile/çalışma/tatlı/kahvaltı yayımlanmış fact olmadığı için insufficient durur.

## 0015 downgrade güvenliği

Üç `test_0015_downgrade_veri_varken_sessizce_tablo_silmez` parametresi (`dahili_gozlem_adaylari`, `dahili_sinyal_ozetleri`, `ilce_sinirlari`) geçti. Testler atlanmadı, xfail edilmedi, assertion gevşetilmedi.

Kök neden: Alembic varsayılanı çok revizyonu tek işlemde sarar. Head 0016 iken `downgrade 0014`, önce 0016'yı geri alır sonra 0015 veri koruması `RuntimeError` üretir; tek işlem rollback olunca `alembic_version` 0016'da kalır ve test `0015 in current` beklerken başarısız olur.

Uygulama:

- `env.py` online: `transaction_per_migration=True`. 0016 kendi işleminde biter; 0015 fail-closed kalır; sürüm 0015'te durur.
- `0015.downgrade`: DROP'tan önce ve `LOCK TABLE ... ACCESS EXCLUSIVE` sonrasında `EXISTS` kontrolü. Veri varsa `RuntimeError("0015 downgrade veri kaybina yol acar; yeni tablolar bosaltilmali: …")`. Kısmi silme yok.

Doğrulama:

1. Tek kullanımlık test DB: 0015 upgrade, tabloya test satırı, downgrade 0014 → returncode ≠ 0, hata metninde tablo adı, `count(*) >= 1`, üç tablo `to_regclass` dolu, current 0015.
2. Boş tek kullanımlık DB: head upgrade → 0014 downgrade → head upgrade başarılı.
3. Development DB: destructive downgrade **çalıştırılmadı**. `alembic current/heads` = `0016 (head)`; `alembic check` yeni upgrade yok; `sema_baseline` uyumlu.

## Kimlik ve taksonomi

- Geçersiz isim (`.` ve tek karakter) `karantina`; öneri havuzuna girmez.
- Aynı normalize isim `oneri_listesini_sec` içinde bir kez.
- Uzak aynı isim otomatik birleşmez (`AYRI_TUT`); FAZ 17 `eslemeyi_degerlendir` aynı kaynak için yeni eşlemeyi reddeder. Otomatik birleştirme 0; insan incelemesi çift 2.
- `internet_kafe` kahve amacı üretmez (`NO_PURPOSE_INFERENCE`).
- Kaynak etiketi `dondurma`/`pastane` kafe kimliğini `tatli_pastane` yapar; kahve havuzundan çıkar. Mekan adına özel kural yok.
- `Adana Sofrasi` hâlâ `kafe` + `kullanilabilir`; tepe sırayı `güclü` kimlikler alır.

## Sıralama

Anahtar (küçük önce, eksi alanlar büyük önce): kimlik sınıfı → yayın → amaç seviyesi → public fact → güçlü deneyim → deneyim destek → ilçe uyumu → bilinmeyen yükü → tamamlık → normalize isim → canonical id.

Zengin aday (public fact, deneyim veya güçlü kimlik) varken kategori-only doldurma yok. Alfabe son tie-break.

Citywide kahve (gold 1, 2, 8, 24): **Günevi Atölye /Cafe**, Cafe Pi, Doğu Kafe, Door Coffee & Kitchen Havza, Glutensiz Kafe. 25.2 alfabetik `ALAÇAM Küçük Mucizeler` / internet kafe / `Adana Sofrasi` tepe sırayı kaybetti.

Atakum kahve (9, 10): Günevi + Kollekt; n=2, zayıf doldurma yok.

Aile yemek (5, 6, 25, 27): `.` yok; `153 Restoran` bir kez.

Sakin kahve (26): fact + deneyim; Günevi önce.

Artık risk: şehir genelinde `güclü` kimlikli Havza kafeleri merkez ilçelerin önüne gelebilir. İlçe belirtilince `ilce_uyumu` geriye iter; citywide coğrafi yoğunluk cezası yok.

## 30 gold — masa başı

Kaynak: `veri/cikti/raporlar/dahili_nlp/samsun_gold_30.json`. Parser 30/30. Saha araştırması değildir.

| Küme | Durum | Not |
|---|---|---|
| Citywide kahve 1,2,8,24 | success / fact | Günevi önce; sohbet unknown |
| Atakum kahve 9,10 | insufficient / fact | n=2 doldurulmadı |
| Birlikte vakit / eğlence 3,4,7 | insufficient | uydurma yok |
| Aile yemek 5,6,25,27 | success / fact | aile uygunluğu yayımlanmamış |
| Çalışma / çocuk / manzara 11–14 | insufficient | deneyim hard PASS değil |
| Fiyat / mesafe / otopark / wifi / açık 15–20 | clarification | review hard kapı değil |
| Tatlı / kahvaltı / müze 21–23,28–29 | insufficient | fact yok |
| Sakin kahve 26 | success / fact+deneyim | |
| Aile + tarihi 30 | success / fact | müze/anıt |

## Kuyruk

`inceleme_kuyrugunu_triyaj_et`: düşük/yüksek/orta. Admin listesi `oncelik_puani` azalan. Otomatik yayın yok. 108 dosyanın `triyaj_sinifi` boş (kimlik inceleme dosyaları triyaj koşusundan sonra); operasyon borcu duruyor.

## Canlı SITE / API

Yerel API FAZ 25.3 koduyla yeniden başlatıldı (`127.0.0.1:8125`). Site `localhost:3000` (önceki dev süreci; `/backend` vekili).

- `GET /docs`, `GET /openapi.json`: 200. Swagger başlığı Şamandıra API.
- `POST /v1/bugun-ne-yapalim` partner+kahve+sohbet: 200, 0,31 s, success, Günevi önce. Yemek 0,46 s. Çalışma insufficient 0,01 s. Public JSON'da `kimlik_kalite`, `oncelik_puani`, `triyaj`, sentiment, yorum sayısı, Rotam yok.
- Playwright MCP masaüstü: form → 5 kart → Günevi detay. Başlıklar Doğruladığımız / Deneyim sinyali / Henüz doğrulayamadığımız. Bağlam bağlandı (`Yer belirtilen amaci destekliyor.`).
- Keşfet `q=kafe`: aynı tepe küme.
- 390px: oturum restorasyonu; Günevi önce; sohbet unknown görünür.

## Test ve kapı

- Migration safety + FAZ 25.3 hedefli: 65 geçti (önceki 0015 üçlüsü dahil).
- Backend pytest: 186 geçti.
- Frontend vitest: 20 geçti. `tsc --noEmit` temiz. ESLint 0 error / 2 tarihî `<img>`.
- `git diff --check` temiz (EOF boş satır `test_kesfet_db.py` düzeltildi).
- Development: current/heads/check/baseline 0016; destructive 0015 downgrade yok.

Korpus 126 yerel motor ~10 s; gold 30 ~3,4 s.

## Riskler

1. Citywide kahvede uzak ilçe `güclü` kimlikler tepeye çıkabilir.
2. `Adana Sofrasi` hâlâ kafe; sıralama düşürür, kategori düzeltmez (isim kuralı yok).
3. Bekleyen inceleme 1772; 108 triyajsız kimlik dosyası.
4. Aile/çalışma/tatlı/kahvaltı public fact yok; coverage 25.2 ile aynı.
5. `unknown_sorgu` korpus metriği 0; sohbet bilinmeyeni kart/özet metninde durur.
6. Hero CTA hâlâ “Rotanı kur”; marka Rotam değil.
7. Bağımsız saha gold yok.

## GO / NO-GO

**FAZ 25.3 TAMAMLANDI.**

**Bugün Ne Yapalım — sınırlı GO.** Kahve/yemek/tarih amaçlarında sıralama insan beklentisine 25.2'den yakın; kirli isim ve internet kafe tepe listeden çıktı. Genel ihtiyaç (aile doğrulaması, çalışma, tatlı, kahvaltı, sohbet fact) karşılanmıyor.

**Akıllı Rota — NO-GO.** Günlük çok duraklı plan, konaklama ve güncel saat/ulaşım bu fazın dışında; saha gold yok.

## Bu dokümanın bağlı olduğu belgeler

- [00 Ürün Felsefesi](../00-product/00-urun-felsefesi.md)
- [01 Bilgi Mimarisi](../00-product/01-bilgi-mimarisi.md)
- [02 Product Language](../00-product/02-product-language.md)
- [03 Karar Motoru](../00-product/03-karar-motoru.md)
- [04 Sistem Mimarisi](../00-product/04-sistem-mimarisi.md)
- [06 Dahili NLP Sinyal Mimarisi](../04-ai/06-dahili-nlp-sinyal-mimarisi.md)
- [FAZ 25.2 sonuç](./faz25-2-sonuc.md)
- [FAZ 25.1 gold](./faz25-1-oneri-gold.md)

## Bu dokümanın etkilediği belgeler

Akıllı Rota motoru referansı, UX karar akışları, admin inceleme kapasitesi, Bugün Ne Yapalım ölçümleri.

## Bundan sonra okunması gereken belge

[Dahili NLP Sinyal Mimarisi](../04-ai/06-dahili-nlp-sinyal-mimarisi.md). Planlanan saha öneri doğrulaması henüz yazılmamıştır.
