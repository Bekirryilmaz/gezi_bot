---
title: "Şamandıra — Dokümantasyon Dizini"
version: "2.0"
status: "dokumantasyon-kurali"
phase: "urun-mimarisi"
last_update: "2026-09-16"
depends:
  - "00-product/00-urun-felsefesi.md"
  - "00-product/01-bilgi-mimarisi.md"
  - "00-product/02-product-language.md"
  - "00-product/03-karar-motoru.md"
  - "00-product/04-sistem-mimarisi.md"
  - "04-ai/05-ai-bilgi-motoru.md"
  - "04-ai/06-dahili-nlp-sinyal-mimarisi.md"
  - "00-product/06-akilli-rota-motoru.md"
  - "02-ux/07-ux-karar-akislari.md"
  - "03-design/08-tasarim-ilkeleri.md"
  - "09-business/09-urun-ekosistemi.md"
  - "03-design/10-design-system.md"
  - "03-design/11-ekran-mimarisi.md"
  - "03-design/12-gorsel-tasarim-dili.md"
  - "03-design/13-bilesen-ve-etkilesim-sozlesmeleri.md"
  - "09-business/14-urun-ozellik-haritasi.md"
affects:
  - "docs altındaki bütün yeni belgeler"
author: "Codex"
---

# Şamandıra dokümantasyonu

Yeni belgelerin tek kalıcı yeri proje deposunun docs dizinidir. Kullanıcının 13 Eylül 2026 tarihli talimatına göre Documents altına belge kaydedilmez. Git'in boş klasörleri korumaması nedeniyle henüz belgesi olmayan alanlarda .gitkeep bulunur. Belgenin burada bulunması commit edildiği anlamına gelmez; commit/push için proje kuralı gereği açık kullanıcı talimatı gerekir.

## Okuma sırası ve otorite

1. [00 Ürün Felsefesi](./00-product/00-urun-felsefesi.md) — kabul edilmiş amaç ve ilkeler.
2. [01 Bilgi Mimarisi](./00-product/01-bilgi-mimarisi.md) — kabul edilmiş kullanıcı bilgi yapısı.
3. [02 Product Language](./00-product/02-product-language.md) — kabul edilmiş ortak kavramlar.
4. [03 Karar Motoru](./00-product/03-karar-motoru.md) — kabul edilmiş karar kuralları.
5. [04 Sistem Mimarisi](./00-product/04-sistem-mimarisi.md) — kabul edilmiş mimari referans; uygulanmış sistem değildir.
6. [05 AI Bilgi Motoru](./04-ai/05-ai-bilgi-motoru.md) — kullanıcının Akıllı Rota görevindeki açık beyanıyla kabul edilmiş referans. Dosyasındaki tarihsel durum ifadesi değiştirilmemiştir. Kanıt, bilgi, güven, mekân, Bir İz katkısı ve yayın sınırlarını tanımlar.
7. [06 Dahili NLP Sinyal Mimarisi](./04-ai/06-dahili-nlp-sinyal-mimarisi.md) — FAZ 25.2 uygulama sözleşmesi. Fact/experience/sentiment ayrımını, canonical sinyal ailelerini, amaç-bazlı kaynak haklarını ve otomatik yayın yasağını tanımlar.
8. [06 Akıllı Rota Motoru](./00-product/06-akilli-rota-motoru.md) — kullanıcının UX Karar Akışları görevindeki açık beyanıyla kabul edilmiş referans. Dosyasındaki tarihsel durum ifadesi değiştirilmemiştir; uygulanmış özellik anlamına gelmez. Günlük rota, düzenleme, kayıt, paylaşım ve ücretsiz/Premium sınırlarını tanımlar.
9. [07 UX Karar Akışları](./02-ux/07-ux-karar-akislari.md) — kullanıcının Tasarım İlkeleri görevindeki açık beyanıyla kabul edilmiş referans. Dosyasındaki tarihsel durum ifadesi değiştirilmemiştir; uygulanmış veya kullanıcılarla doğrulanmış olduğu anlamına gelmez. Karar akışlarını, kullanıcı kontrolünü, erişilebilirliği ve kesinti davranışlarını tanımlar.
10. [08 Tasarım İlkeleri](./03-design/08-tasarim-ilkeleri.md) — kabul edilmiş 00–07 üzerine kurulan nihai tasarım anayasası önerisi; kabul ve kullanıcı doğrulaması bekler. İstenen 36 başlığı, 10 tasarım yasasını, değerlendirme ölçütlerini, 48 maddelik öz eleştiriyi, alternatif yaklaşımları ve öz eleştiri sonrası nihai ilkeleri içerir. Kod, hero, wireframe, renk paleti veya bileşen üretmez.

11. [09 Ürün Ekosistemi](./09-business/09-urun-ekosistemi.md) — kabul edilmiş 00–08 üzerine kurulan ürün ekosistemi önerisi; kabul bekler. Mekan, kullanıcı, şehir ve bilgi yaşam döngülerini; Bir İz, kişisel hafıza, paylaşım, ücretsiz/Premium hakları ve ticari sürdürülebilirliği tanımlar. 14 Mermaid diyagramı, 48 maddelik öz eleştiri, alternatif mimariler ve nihai ilkeler içerir. Kod veya UI üretmez.

12. [10 Design System](./03-design/10-design-system.md) — kabul edilmiş 00–09 üzerine kurulan tasarım sistemi anayasası önerisi; ayrıca kabul ve doğrulama bekler. 60 ana başlık, yedi zorunlu değerlendirme başlığını taşıyan 48 bileşen sözleşmesi, 22 Mermaid diyagramı, 32 kabul senaryosu, 60 maddelik öz eleştiri, dış sistem karşılaştırmaları ve nihai ilkeler içerir. Web, mobil, tablet, admin, Premium, Akıllı Rota, AI ve Yer yüzeyleri için ortak kuralları tanımlar; kod veya UI üretmez.

13. [11 Ekran Mimarisi](./03-design/11-ekran-mimarisi.md) — kabul edilmiş 00–10 üzerine kurulan ekran mimarisi önerisi; ayrıca kabul ve kullanıcı doğrulaması bekler. Otuz ekranın her birini on beş başlıkla tanımlar; navigation, deep link, URL, web/mobil/tablet, geri dönüş, geçmiş, filtre, durum, oturum ve yetkilendirme sözleşmelerini içerir. 35 Mermaid diyagramı, 18 kullanıcı senaryosu, 70 maddelik öz eleştiri, alternatif mimariler ve nihai ilkeler bulunur. Yalnız mimari dokümantasyondur; kod, UI veya wireframe üretmez.

14. [12 Görsel Tasarım Dili](./03-design/12-gorsel-tasarim-dili.md)
15. [13 Bileşen ve Etkileşim Sözleşmeleri](./03-design/13-bilesen-ve-etkilesim-sozlesmeleri.md) — kabul edilmiş 00–12 kaynaklarının davranış karşılığı. İstenen 48 konu ve dört tamamlayıcı bölüm; her bölümde amaç, kullanıcı beklentisi, davranış kuralları, istisnalar ve kabul kriterleri vardır. B01–B48 ile E01–E30 kapsamı eşlenmiştir. 30 Mermaid diyagramı, 77 örnek senaryo, 50 öz eleştiri ve 20 maddelik nihai Interaction Contract içerir. Belge incelemeye hazırdır; kod, UI, Figma veya yeni ürün fikri değildir.

16. [14 Ürün Özellik Haritası](./09-business/14-urun-ozellik-haritasi.md) — FAZ 14 gelişim planı. 40 ana bölüm, 32 sorumluluk kaydı, 30 Mermaid diyagramı, 40 kabul senaryosu, 60 maddelik öz eleştiri ve nihai ürün yol haritası içerir. MVP/v1/v2 sırası, gerçek değere bağlı Premium, kurumsal kapsam, ticari büyüme ve yayın kapıları tanımlanır. Kabul edilmiş günlük Akıllı Rota ile ayrı kapsam kararı gerektiren çok günlük Akıllı Gezi açıkça ayrılır. Kod, UI veya uygulanmış ürün değildir.

**14 Eylül 2026 — FAZ 14 kaynak ve kapsam kaydı:** 00–12 kabul edilmiş referans kümesidir; 13, dizinde ayrıca kabulü kayıtlı olmayan tamamlayıcı davranış kaynağıdır. 14'teki sürümleme ve geliştirme sırası planlama kararıdır; çok günlük Akıllı Gezi yeni ürün genişlemesidir. Belgenin tamamlanması kapsam değişikliği, araştırma sonucu veya ürün yayını anlamına gelmez. Kaynak gövdeleri korunmuştur. Sonraki çalışma uygulama farkı, pilot kapasitesi ve doğrulama planıdır; henüz yazılmamıştır.

**14 Eylül 2026 — Bileşen ve Etkileşim Sözleşmeleri görevinin kaynak kaydı:** Kullanıcının bu görevde birlikte esas alınmasını istediği 00–12 belgeleri kabul edilmiş referans kümesidir. Kaynaklardaki tarihsel öneri etiketleri korunur; kaynakların kendi kapsamlarında koşullu bıraktıkları hizmetler bu kayıtla açılmış sayılmaz. 13 belgesinin hazırlanması ayrıca kabul, uygulama veya kullanıcı doğrulaması değildir. Sonraki uygulama incelemelerinde 10 Design System, 11 Ekran Mimarisi ve 13 birlikte okunmalıdır. UX ve erişilebilirlik doğrulama planı hâlâ planlanan çalışmadır.

**14 Eylül 2026 — Ekran Mimarisi görevinin güncel kabul kaydı:** Kullanıcının açık beyanıyla 00–10'un tamamı kabul edilmiş referanstır. Kaynak dosyalardaki ve bu dizindeki önceki öneri/kabul ifadeleri tarihsel olarak korunur; bu kayıt onların önündedir. 11 belgesinin hazırlanması ayrıca kabul, uygulama veya tamamlanmış kullanıcı araştırması anlamına gelmez. Kabul edilmiş on bir ürün belgesi ve proje kökündeki README değiştirilmemiştir. Yeni belge yalnız proje deposundadır; Documents altında dosya oluşturulmamıştır.

**14 Eylül 2026 — güncel kabul kaydı:** Design System görevindeki açık kullanıcı beyanıyla 00–09'un tamamı kabul edilmiş referanstır. Kaynak dosyalardaki ve aşağıdaki tarihsel öneri/kabul ifadeleri korunmuştur; bu güncel kayıt onların önündedir. 10 belgesinin hazırlanması onun ayrıca kabul edildiği, uygulandığı veya kullanıcılarla doğrulandığı anlamına gelmez. Kabul edilmiş on ürün belgesinin içerikleri değiştirilmemiştir.

**13 Eylül 2026 — güncel kabul kaydı:** Ürün Ekosistemi görevindeki açık kullanıcı beyanıyla 00–08'in tamamı kabul edilmiş referanstır. Yukarıdaki 08 öneri durumu ve aşağıdaki önceki görev kayıtları tarihsel olarak korunmuştur; güncel kabul kaydı bunların önündedir. 09 belgesi yeni öneridir ve ayrıca kabul bekler. Kabul edilmiş dokuz ürün belgesinin içeriği değiştirilmemiştir.
Yeni belgeler kabul edilmiş 00–10 referanslarını sessizce değiştiremez. Referansların yetki alanları farklıdır; bu sıra keyfî olarak “son dosya her şeyi ezer” anlamına gelmez. Çelişki açıkça kaydedilir ve ilgili referans için gerekçeli değişiklik gerekir. Sistem Mimarisi §0, tempo kavramı ve işletme/rota arayüz kapsamındaki gerilimleri açıklar.

## Klasör sahipliği

| Klasör | Belge kapsamı |
|---|---|
| 00-product/ | Felsefe, bilgi mimarisi, ortak dil, karar ve sistem mimarisi |
| 01-research/ | Kullanıcı araştırması, varsayım ve doğrulama kanıtları |
| 02-ux/ | Karar akışları, netleştirme, kullanıcı kontrolü |
| 03-design/ | Karar anlamını koruyan görsel/sunum ilkeleri |
| 04-ai/ | Kanıt işleme, AI değerlendirmesi ve yayın politikası |
| 05-api/ | Kanal sözleşmeleri ve entegrasyon davranışı |
| 06-frontend/ | Web ve mobil tüketici davranışı |
| 07-backend/ | Servis sahipliği, veri yaşamı ve işletim |
| 08-admin/ | İnceleme, yetki, operasyon ve geri alma |
| 09-business/ | Ürün ekosistemi, yaşam döngüleri, kullanıcı hakları, büyüme ve ticari bağımsızlık |

Her yeni belge başında title, version, status, phase, last_update, depends, affects ve author metadata alanlarını taşır. Sonunda “Bu dokümanın bağlı olduğu belgeler”, “Bu dokümanın etkilediği belgeler” ve “Bundan sonra okunması gereken belge” bulunur. Henüz yazılmamış belgeler planlanan olarak belirtilir; kırık bağlantıyla mevcutmuş gibi sunulmaz.

## Aktarım kaydı

- Ürün Felsefesi, “0-Ürün Felsefesi” görevinin nihai yanıtından aynen alındı.
- Product Language, “2-Ürün Veri Modeli” görevinin nihai yanıtından aynen alındı.
- Bilgi Mimarisi, depodaki dokumanlar/bilgi_mimarisi.md gövdesinden aynen alındı. Eski dosya mevcut bağlantılar için taşıma notu olarak bırakıldı.
- Karar Motoru, “3-Karar Motoru” görevinin Documents altındaki çıktısından aktarıldı. Gövde korunduktan sonra eski çıktı dosyası kaldırıldı.
- Dört referansa yalnız metadata, köken notu ve belge ilişkileri eklendi. Özgün gövdedeki öneri/durum ifadeleri tarihsel kayıt olarak korundu; kabul durumu kullanıcının bu görevdeki açık beyanına dayanır.
- Diğer eski plan ve teknik dosyalar bu dört referansla eşdeğer kabul edilmiş ürün belgesi değildir. Bu görev onların içeriğini veya uygulama dosyalarını değiştirmemiştir.

## Sonraki belge sırası


08 Tasarım İlkeleri, docs/03-design/08-tasarim-ilkeleri.md konumunda hazırlandı; kabul edilmiş 00–07 dosyaları değiştirilmedi. 07 UX Karar Akışları bu görevdeki açık kullanıcı beyanıyla kabul edilmiş referans olarak kaydedildi. Yeni belge tasarım kararlarının felsefesini ve sınırlarını tanımlar; UI veya uygulanmış tasarım üretmez. Sonrasında 01-research altında planlanan UX Kullanıcı Doğrulama Planı, 07 ve 08 belgelerindeki varsayımları birlikte sınamalıdır. Bilgi yayını için ayrıca 04-ai/05-kanit-guncellik-yayin-politikasi.md bağımlılığı sürer; bu planlanan dosya AI Bilgi Motoru ile aynı belge değildir. Sonraki tasarım, kanal davranışı, destek ve Premium değer çalışmaları kabul edilmiş referanslar ile bu tasarım önerisinin durumunu birlikte dikkate almalıdır. Bu kayıt araştırmanın yapıldığı, 08 belgesinin kabul edildiği veya ek özelliklerin uygulandığı anlamına gelmez.

## Bu dokümanın bağlı olduğu belgeler

- [00 Ürün Felsefesi](./00-product/00-urun-felsefesi.md)
- [01 Bilgi Mimarisi](./00-product/01-bilgi-mimarisi.md)
- [02 Product Language](./00-product/02-product-language.md)
- [03 Karar Motoru](./00-product/03-karar-motoru.md)
- [04 Sistem Mimarisi](./00-product/04-sistem-mimarisi.md)
- [05 AI Bilgi Motoru](./04-ai/05-ai-bilgi-motoru.md)
- [06 Dahili NLP Sinyal Mimarisi](./04-ai/06-dahili-nlp-sinyal-mimarisi.md)
- [06 Akıllı Rota Motoru](./00-product/06-akilli-rota-motoru.md)
- [07 UX Karar Akışları](./02-ux/07-ux-karar-akislari.md)
- [08 Tasarım İlkeleri](./03-design/08-tasarim-ilkeleri.md)
- [09 Ürün Ekosistemi](./09-business/09-urun-ekosistemi.md)
- [10 Design System](./03-design/10-design-system.md)
- [11 Ekran Mimarisi](./03-design/11-ekran-mimarisi.md)
- [12 Görsel Tasarım Dili](./03-design/12-gorsel-tasarim-dili.md)
- [13 Bileşen ve Etkileşim Sözleşmeleri](./03-design/13-bilesen-ve-etkilesim-sozlesmeleri.md)
- [14 Ürün Özellik Haritası](./09-business/14-urun-ozellik-haritasi.md)

## Bu dokümanın etkilediği belgeler

docs altındaki bütün yeni ürün ve geliştirme belgeleri; klasör sahipliği tablosundaki kapsamlar.

## Bundan sonra okunması gereken belge

[11 Ekran Mimarisi](./03-design/11-ekran-mimarisi.md) ve [10 Design System](./03-design/10-design-system.md), ilgili görev için [07 UX Karar Akışları](./02-ux/07-ux-karar-akislari.md) ve [08 Tasarım İlkeleri](./03-design/08-tasarim-ilkeleri.md) ile birlikte okunmalıdır. Sonraki yeni çalışma, 01-research altında planlanan UX ve erişilebilirlik doğrulama planıdır. İş modeli/şehir kapasitesi doğrulaması ve Kanıt, Güncellik ve Yayın Politikası bağımlılıkları sürer; bu planlanan çalışmalar henüz tamamlanmış değildir.

## Ürün Ekosistemi sonrası güncel okuma kaydı

[09 Ürün Ekosistemi](./09-business/09-urun-ekosistemi.md) tamamlanmıştır. Sonraki planlı çalışma, 01-research altında iş modeli ve şehir kapasitesi doğrulamasıdır; ücretsiz hakların maliyeti, kolaylık için ödeme isteği ve şehir bakım yükünü sınamalıdır. Önceden planlanan UX Kullanıcı Doğrulama Planı ve Kanıt, Güncellik ve Yayın Politikası bağımlılıkları sürer. Bunlar henüz yazılmış veya uygulanmış sayılmaz. Yeni belge proje docs/09-business altında oluşturulmuş; bu görevde Documents altında taşınması gereken eski referans kopyası bulunmamıştır.

## Design System sonrası güncel okuma kaydı

[10 Design System](./03-design/10-design-system.md) yalnız proje deposundaki docs/03-design altında oluşturulmuştur. Bütün istenen referanslar okunmuş; 00–09 değiştirilmemiştir. README bağlantıları ve bu dizin güncellenmiştir. Sonraki tasarım çalışmalarında sayısal başlangıç değerleri araştırma bulgusu sayılmadan, belgedeki kabul senaryolarıyla doğrulanmalıdır. Bu görev kod, ekran, commit veya push üretmemiştir; Documents altında dosya oluşturulmamıştır.

## FAZ 25.1 development kurtarma ölçümleri — 15 Eylül 2026

- [faz25-1-kurtarma-sonuc.md](./01-research/faz25-1-kurtarma-sonuc.md)
- [faz25-1-oneri-gold.md](./01-research/faz25-1-oneri-gold.md)
- [faz25-1-promotion-veri-stratejisi.md](./01-research/faz25-1-promotion-veri-stratejisi.md)

Canlı doğrulamalar ve teknik ölçümler kayıtlıdır; kaynak hakları/coğrafi veri/saha gold bağımlılıkları nedeniyle ürün geçişi NO-GO.

## FAZ 25.2 dahili NLP sinyal sözleşmesi — 15 Eylül 2026

- [06 Dahili NLP Sinyal Mimarisi](./04-ai/06-dahili-nlp-sinyal-mimarisi.md)
- [faz25-2-sonuc.md](./01-research/faz25-2-sonuc.md)

Canonical fact/experience/sentiment ayrımı, amaç-bazlı hak kapıları ve
otomatik yayın yasağı uygulama sözleşmesi olarak kaydedilmiştir.
Development NLP/aggregation/ilçe/OSM ve 126+30 ölçümleri sonuç belgesindedir.
Akıllı Rota geçişi NO-GO; production DB, commit ve push yoktur.

## FAZ 25.3 kimlik temizliği ve sıralama — 16 Eylül 2026

- [faz25-3-sonuc.md](./01-research/faz25-3-sonuc.md)

Kirli kimlik karantina, quality-first sıralama, `internet_kafe` amaç yasağı,
0015 veri korumalı downgrade ve 126+30 yeniden ölçüm kayıtlıdır.
Bugün Ne Yapalım kahve/yemek/tarih için sınırlı GO; Akıllı Rota NO-GO.
Production DB, commit ve push yoktur.

## FAZ 25.4 karar coverage ve pilot — 16 Eylül 2026

- [faz25-4-sonuc.md](./01-research/faz25-4-sonuc.md)

Samsun 88 mekanlık veriye dayalı pilot, OSM grup inceleme (kör yayın yok),
tamamlık matrisi ve iç rota hazırlık durumu kayıtlıdır. Bugün Ne Yapalım
kahve/yemek/tarih sınırlı GO; Akıllı Rota NO-GO (`rota_hazir` 11/88, tarih 0).
Production DB, commit, push ve yeni migration yoktur.
