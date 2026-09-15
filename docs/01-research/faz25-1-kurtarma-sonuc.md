---
title: FAZ 25.1 — Kurtarma ve son development doğrulama raporu
version: 1.0
status: Development doğrulaması; ürün geçişi engelli
phase: FAZ 25.1
last_update: 2026-09-15
depends: [00-urun-felsefesi, 01-bilgi-mimarisi, 02-product-language, 03-karar-motoru, 04-sistem-mimarisi]
affects: [Bugün Ne Yapalım, NLP, admin review, Akıllı Rota]
author: Codex
---

# Karar

FAZ 25.1 ürün açısından **tamamlandı sayılmadı**. Canlı doğrulama ve teknik ölçüm katmanları tamamlandı; gerçek Google yorum aggregation/promotion haklar nedeniyle çalıştırılmadı, güvenilir resmi polygon olmadan ilçe backfill yapılmadı, bağımsız saha öneri gold'u yok. Bugün Ne Yapalım sınırlı doğrulanmış kahve/yemek/tarih amacıyla çalışıyor; genel kullanıcı ihtiyaçlarını yeterince karşılamıyor. Akıllı Rota geçişi NO-GO.

## Kurtarılan repo

Gerçek path C:/dev/buyuk_gezi_projesi/gezi_bot; branch main. Başlangıçta 15 tracked unstaged değişiklik ve önceki intent/corpus/black-box dosyaları vardı. Staged boştu. Önceki işler korunarak hedefli değişikliklerle devam edildi. Reset, stash, commit, push ve production işlemi yok. Migration eklenmedi; public claim adedi değişmedi.

## Canlı doğrulama

SITE https://qk4cmqnw-3000.euw.devtunnels.ms/; API https://qk4cmqnw-8125.euw.devtunnels.ms/; /docs ve OpenAPI final smoke HTTP 200. plan/00_brief_eki.md ve plan/01_urun_analizi_ve_strateji.md aynı qk4cmqnw tunnel adreslerini içeriyor. site/.env.local/next.config.ts backend rewrite için127.0.0.1:8125 kullanıyor; bu server-side development hedefidir, browser canlı /backend üzerinden çağırır. SITE testi gerçek /backend proxy çağrısı, API corpus testi doğrudan gerçek devtunnel POST kullandı.

126 sorgu final HTTP 200; durumlar `{'success': 23, 'insufficient': 80, 'clarification': 23}`. Tanımlı public intent beklenti uyumu 126/126. 44 sorguda mekan var, 82 sorguda yok; seçili sayılar `{3: 23, 0: 82, 1: 17, 2: 4}`. Bunlar gerçek ihtiyaç tam karşılanma skoru değildir. Public DTO kontrolünde ham yorum/evidence, parser/full stage trace, sentiment ve aggregate metrik anahtarı yok. Standart opaque trace_reference private trace içeriği değildir.

İlk 126 taramada 124 HTTP 200 ve 2 exhausted transport timeout (sıra 16,81) vardı; toplam 59 timeout denemesi kaydedildi. İki sorgu recovery'de 200 verdi. İlk denemeler saklandı; 'ilk seferde sıfır hata' iddiası yok. Devtunnel/transport dalgalanması gerçek kullanıcı deneyiminde retry gerektiriyor. Backend response süreleri tek başına tunnel uçtan uca gecikmesini açıklamaz; kesin ağ kök nedeni kanıtlanmadı. Final local/live intent-state farkları: yok. İlk run eski kod parçalarıyla karşılaştırılmamalı; etkilenen gold/outcome sorguları son kodla tekrarlandı.

İlk SITE koşusunda21 zorunlu ifade ×1280 ve390px =42 gerçek akış geçti;29 akış ilk,13 akış ikinci denemede yanıt aldı. Session/hydration düzeltmesinden sonra sıkı test her istekte textarea ile gerçek POST gövdesini eşleştirdi:21 desktop assertion tamamlandı ve21 mobil assertion ayrı Playwright koşusunda geçti. Birleşik sıkı koşunun desktop kısmından sonra ilk mobil screenshot font beklemesinde runner timeout verdi; uygulama assertion hatası değildi ve ayrı mobil koşu bunu kapattı. Son mobil durumları `{'success': 3, 'insufficient': 12, 'clarification': 6}`, deneme dağılımı `{1: 18, 3: 3}`. Timeout UI unavailable olarak ayrıldı. /docs gerçek Swagger UI'da endpoint açma/Try it out akışı geçti. Ekranlar ve metinlerle masa başı UX kontrolü yapıldı; gerçek yeni kullanıcı araştırması değil.

UI düzeltmeleri: örnekli tek giriş, ikincil daraltma, doğal anlaşılmış ihtiyaç/koşul etiketleri, somut kart nedeni, bilinmeyenlerin birlikte gösterimi, sessizlik/sohbet/romantik unsupported inference engeli, session restore/new text sırasında eski inferred amaç override düzeltmesi. Mobil scroll header zemini opaklaştırıldı. Müze isteğine genel tarihi mekan önerilmesi engellendi; aynı ziyarette oturmak/kafe bağlamı çok duraklı plan uyarısı sayılmadı. Budget unknown ve otopark unknown/empty ayrımı düzeltildi. Az adayda 2–4 sayısını doldurmak için zayıf mekan eklenmedi.

Ek canlı API smoke: {'empty': 1, 'insufficient': 1}; Yakakent'te kahve gerçek geography-empty döndü, unknown otopark ise insufficient. SITE dahil farklı gerçek canlı ifadeler: 130; corpus126dışında2doğrudanAPI smoke var. Tüm seçili cevapların farklı mekan sayısı: 6. Trace aşama grupları: {'searched_success': 23, 'pre_search_capability_or_family_insufficient': 58, 'searched_insufficient': 22, 'clarification': 23}.

## Veriler ve publication

1719 mekan,1958 kaynak bağlantısı,19609 Google Maps yorum. Gozlem212, mevcut claim/candidate212, pending167, review dosyası/kuyruğu bulunan mekan68; bu68 yeni aggregate gate geçişi sayısı değildir. Önceki19 mekan/41 observation/41 candidate pilot korunmuş. Yeni NLP AdayGozlem0; yeni claim candidate0; aggregate promotion eligible0; public claim24/6mekan, değişim0. Auto-publish yok.

## Full trace

Development/test Session.info ve internal uvicorn log: parsed_intent, search_candidate_count, geographic_filtered_count, publication_eligible_count, decision_evaluated_count, hard_constraint_rejected_count, unknown_critical_count, selected_count, final_state. Production instrumentation kapalı; public DTO'ya eklenmedi. Erken clarification/capability çıkışında0, çalıştırılmamış aşamadır. unknown critical sayacı aday sayısıdır; kullanıcı bilinmeyen aile adedi değildir. Search publication count ile karar değerlendirme stage aynı kavram değildir.

Kahve+sohbet örneği:199search,199geographic,199search publication,199decision,196unknowncritical,3selected,success. Family dinner827candidate/823unknown/1selectedinsufficient. Claim coverage düşükken arama identity havuzu büyük olabilir; parser başarısı veri yeterliliğini göstermez.

## Family coverage

Payda1719. Unknown pending/stale/conflict'i içerir; son üç kolon diagnostic overlay, toplamaya uygun partition değil. Purpose listesinde olmayan değer known false sayılmaz.

| Aile | Known true/value | Known false | Unknown | Stale | Conflicting | Review pending |
|---|---:|---:|---:|---:|---:|---:|
| amac_destegi | 6 | 0 | 1713 | 1 | 0 | 68 |
| wifi | 2 | 0 | 1717 | 1 | 0 | 7 |
| otopark | 0 | 0 | 1719 | 0 | 0 | 0 |
| sessiz_ortam | 0 | 0 | 1719 | 0 | 0 | 0 |
| sohbet_uygunlugu | 0 | 0 | 1719 | 0 | 0 | 0 |
| aile_uygunlugu | 0 | 0 | 1719 | 0 | 0 | 0 |
| cocuk_uygunlugu | 0 | 0 | 1719 | 0 | 0 | 0 |
| calisma_uygunlugu | 0 | 0 | 1719 | 0 | 0 | 0 |
| manzara | 0 | 0 | 1719 | 0 | 0 | 0 |
| uygun_fiyat | 0 | 0 | 1719 | 0 | 0 | 0 |
| fiyat | 0 | 0 | 1719 | 0 | 0 | 0 |
| calisma_saati | 0 | 0 | 1719 | 0 | 0 | 0 |
| acik_alan | 0 | 0 | 1719 | 0 | 0 | 0 |
| acik_hava | 0 | 0 | 1719 | 0 | 0 | 0 |
| canli_muzik | 0 | 0 | 1719 | 0 | 0 | 0 |
| tekerlekli_sandalye_erisimi | 0 | 0 | 1719 | 0 | 0 | 1 |
| ziyaret_suresi | 0 | 0 | 1719 | 0 | 0 | 0 |
| ulasim | 0 | 0 | 1719 | 0 | 0 | 0 |

Amaç desteği: kahve3, yemek1, tarih/kültür2; tatlı, kahvaltı, eğlence, çalışma, birlikte vakit, çocuk aktivitesi0.

Ürünü kilitleyen aile sırası: (1) amaç/çalışma-eğlence-tatlı-kahvaltı desteği, (2) sohbet/sessizlik/çalışma/aile-çocuk uygunluğu, (3) güncel fiyat-saat/ulasim/yakınlık ve canonical district, (4) hard Wi-Fi/otopark ve manzara. Bu ürün önem sırasıdır, bağımsız pazar talebi ölçümü değildir. Corpus'ta görülen somut unknown frekansı: '+json.dumps(dict(unknown_freq.most_common()),ensure_ascii=False)+'

## Aggregation, rights ve canonical sonuç

209 izinli metadata aggregate grubu üretildi; dağılım ve fail-closed promotion config ayrı dosyalarda. Gerçek Google yorum→AdayGozlem yolu hak bilinmediği için kapalı. Negation/counter testleri sakin değil, çok gürültülü, otopark yok, wifi yok/çekmiyor, çocukla gidilmez, manzarası yok, açık alan yok, çok pahalı ve çalışmaya uygun değil ifadelerinde olumlu keyword/sentiment çıkarımı yapılmadığını doğruladı.

Canonical ilce_id26/1719;1693eksik.1692upstream metin yok, bir“merkez” çözümsüz. Koordinat1719. Verified resmi polygon alınamadı; backfill0. Yeni missing text mevcut canonical ilişkiyi artık silmez. Hak/retention/public sonucu ve kaynak stratejisi ayrıntıları promotion-veri-stratejisi belgesindedir.

## Gold ve riskler

30-query raporu gerçek venue/neden/support/unknown ve her sorguya masa başı değerlendirme içerir. Aile için pizza tek seçenek; çalışma/tatlı/kahvaltı/eğlence sonuçsuz; sohbet/sakinlik bilinmeyen; çok duraklı istekler tam plan değil. Müze alt tür alakasızlığı ve otopark empty ayrımı düzeltildi. Success tam semantik ihtiyaç desteği garantisi değildir. Starbucks branch adı/ilçesi; yayınlı Wi-Fi freshness; source-derived legacy profil hakları; tunnel timeout; canonical coğrafya; bağımsız saha gold eksikleri açık riskler.

## Son doğrulama

Alembic current0014(head), heads0014, check yeni upgrade işlemi yok. Baseline uyumlu, PostGIS3.6.2, canonical source bindings1958/null-orphan0. Backend/NLP son kodla148test geçti. Targeted30test ve yeni modülrufflint geçti. Frontend19test, typecheck,lint0error/2eskiimgwarning, productionbuild geçti. Local linked-flow Playwright6test geçti; ilk canlı42 ve Swagger1test geçti, son canlı12tekrar ve outcome8tekrar ayrı. Sıkı desktop21 assertion tamamlandı; birleşik runner mobil screenshot font timeout'u nedeniyle fail kaydetti, ardından ayrı sıkı390px21 koşusu geçti. API126,30gold, finalSITE/API/docs/OpenAPI smoke ve gitdiffcheck kayıtlı. Starlettehttpx deprecation uyarısı var.

## Değişiklik dosyaları

Aşağıdaki liste başlangıçtan kalan işler ve bu turun değişikliklerini birlikte gösterir; önceki15dosya bu tur sıfırdan üretilmedi.

- docs/01-research/faz25-1-kurtarma-sonuc.md
- docs/01-research/faz25-1-oneri-gold.md
- docs/01-research/faz25-1-promotion-veri-stratejisi.md
- docs/README.md
- site/e2e/bugun-korpus-blackbox.spec.ts
- site/e2e/bugun-ne-yapalim.spec.ts
- site/e2e/docs-live.spec.ts
- site/e2e/faz25-live-site.spec.ts
- site/src/app/globals.css
- site/src/components/admin/AdminPaneli.tsx
- site/src/components/bugun/BugunNeYapalimAlani.test.tsx
- site/src/components/bugun/BugunNeYapalimAlani.tsx
- site/src/components/hero/ScrollHero.tsx
- site/src/lib/admin-api.ts
- site/src/lib/types.ts
- sunucu/admin/router.py
- sunucu/admin/semalar.py
- sunucu/arama/servis.py
- sunucu/bilgi/aggregation.py
- sunucu/bilgi/faz25_data_audit.py
- sunucu/bilgi/pilot_claimleri.py
- sunucu/bilgi/testler/test_faz25_data.py
- sunucu/bilgi/testler/test_pilot_claim_pipeline.py
- sunucu/bugun_ne_yapalim/gelistirme_izi.py
- sunucu/bugun_ne_yapalim/intent.py
- sunucu/bugun_ne_yapalim/korpus_raporu.py
- sunucu/bugun_ne_yapalim/semalar.py
- sunucu/bugun_ne_yapalim/servis.py
- sunucu/bugun_ne_yapalim/testler/intent_korpusu.json
- sunucu/bugun_ne_yapalim/testler/test_bugun_ne_yapalim.py
- sunucu/bugun_ne_yapalim/testler/test_intent_korpusu.py
- sunucu/kesfet/servis.py
- sunucu/veritabani/aktarim/yer_aktar.py
- veri/cikti/raporlar/faz25_1_data_coverage_aggregation.json
- veri/cikti/raporlar/faz25_1_intent_trace.json
- veri/cikti/raporlar/faz25_1_promotion_config.json
- veri/duygu_analizi/gozlem_adayi.py
- veri/duygu_analizi/pipeline_calistir.py
- veri/duygu_analizi/testler/test_gozlem_adayi.py
- veri/ortak/veri_yukleyiciler.py

Bu turun ana ilaveleri: aggregation/data audit/rights filter/private trace; search/kesfet counters; import canonical koruma; UI session/hydration/explicit-amac/unknown/neden/menü düzeltmeleri; live SITE/docs testleri ve raporlar.

## Belge ilişkileri

Bağlı belgeler: docs/00-product/00-urun-felsefesi.md, 01-bilgi-mimarisi.md, 02-product-language.md, 03-karar-motoru.md, 04-sistem-mimarisi.md.

Etkilediği belgeler: docs/04-ai/05-ai-bilgi-motoru.md, docs/00-product/06-akilli-rota-motoru.md, docs/02-ux/07-ux-karar-akislari.md.

Bundan sonra okunacak belge: bu ölçümle birlikte faz25-1-oneri-gold.md ve faz25-1-promotion-veri-stratejisi.md. Sahada bağımsız öneri doğrulama planı planlanmıştır; gerçekleştirilmiş sayılmaz.
