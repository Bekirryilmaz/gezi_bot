---
title: "Publication Lifecycle"
version: "1.0"
status: "uygulandi"
phase: "Dalga-1B"
last_update: "2026-09-15"
depends:
  - "../00-product/04-sistem-mimarisi.md"
  - "../04-ai/05-ai-bilgi-motoru.md"
affects:
  - "../../sunucu/yayin/"
  - "../../sunucu/veritabani/sorgular.py"
author: "Codex"
---

# Publication lifecycle

`YayinKaydi`, bir `Yer` veya `Iddia` satırının public kullanılabileceği anlamına gelen tek projection kaydıdır. Durumlar `yayinlanabilir`, `sinirli_yayinlanabilir`, `yayinlanamaz` ve `yeniden_dogrulama_gerekli`; sonuçlar reason code taşır. Liste, detay, Keşfet görünümü, rota adayı, karar, paylaşım ve cache kullanım izinleri ayrı değerlendirilir.

Canonical/şube geçerliliği, aktif claim/sürüm, kaynak hakkı, bilgi durumu, geçerlilik aralığı, withdrawal ve kullanım türü kapı girdileridir. Bilinmeyen hak izin sayılmaz. `stale` ve bilinmeyen bilgi yeniden doğrulama ister; conflicting ve withdrawn public olumlu bilgi üretemez.

Public yer listeleme, detay, istatistik ve rota adayı sorguları `sunucu/veritabani/sorgular.py` içindeki aynı yayın join'inden geçer. Yeni search/Keşfet/share/cache adapter'ları `KullanimTuru` ile bu katmana bağlanmalıdır; raw `Yer` sorgusu public kodda kullanılmaz. Detay withdrawal için `410`, diğer uygun olmayan kayıtlar için bilgi sızdırmayan `404` üretir. ETag yayın sürümüne bağlıdır.

Withdrawal destructive delete değildir. Gerekçe, zaman, aktör, kapsam ve nesne korunur. Outbox niteliğindeki `GecersizlestirmeOlayi.olay_anahtari` unique'tir. Etki bağı MVP'de `claim → yer projection → route evaluation → share/cache` zincirini taşır. Consumer aynı olayı tekrar görürse tamamlanmış olayı yeniden işlemez; bağlı public projection'lar invalid olur.

## Bağlı belgeler

- [Sistem mimarisi](../00-product/04-sistem-mimarisi.md)
- [AI Bilgi Motoru](../04-ai/05-ai-bilgi-motoru.md)

## Etkilediği belgeler

Admin runbook ve kısa ADR bu yaşam döngüsüne bağlıdır.

## Bundan sonra okunması gereken belge

[Admin auth runbook](../08-admin/admin-auth-runbook.md).
