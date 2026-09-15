---
title: FAZ 25.1 — 30 sorguluk bağımsız öneri masa başı gold incelemesi
version: 1.0
status: Development doğrulaması; ürün geçişi engelli
phase: FAZ 25.1
last_update: 2026-09-15
depends: [00-urun-felsefesi, 01-bilgi-mimarisi, 02-product-language, 03-karar-motoru, 04-sistem-mimarisi]
affects: [Bugün Ne Yapalım, NLP, admin review, Akıllı Rota]
author: Codex
---

# 30 sorguluk öneri incelemesi

Bu rapor parser beklenen alanları testinden ayrıdır. İnceleme ölçütü kullanıcı cümlesindeki gerçek amaç, zorunlu koşullar, ziyaret bağlamı ve çoklu planın karşılanmasıdır. Gerçek canlı API yanıtları aşağıdadır; otomatik “öneri iyi” etiketi verilmemiştir. Masa başı insan ölçütleriyle Codex incelemesi yapılmıştır; bağımsız saha değerlendiricisi, işletme ziyareti veya kullanıcı araştırması yapılmış gibi sunulmaz. Yayınlı claim desteği mekanın bugün gerçekte uygun olduğunu kanıtlamaz.

Normal success bile yalnız doğrulanabilen ihtiyaç parçası için olabilir. Dağılım gerçek son yanıtlar üzerinden aşağıda hesaplanır.

Son ölçüm: `{'success': 7, 'insufficient': 18, 'clarification': 5}`.

## 1. sevgilimle kahve içicem ve sohbet edicez

Corpus sıra: 1; canlı durum: **success**.

Parse edilen ihtiyaç: {"kisi_baglami": "partner", "ana_amac": "kahve_icmek", "alt_amaclar": [], "aktiviteler": ["sohbet"], "ziyaret_baglamlari": ["birlikte_vakit"], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": ["sohbet_uygunlugu"]}

- **Günevi Atölye /Cafe**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Starbucks**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Kollekt**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.

Bilinmeyenler: sohbet için uygunluk; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Kahve kısmı kategoriyle uyumlu. Sohbet ortamı doğrulanmadığı için tam ihtiyaç karşılanmış kabul edilemez. Partnerden romantik ortam çıkarılmaması doğru. Starbucks şube adı ve ilçesi eksik; kimlik insan kontrolü gerektirir.

## 2. sevgilimle kahve içip oturacağız

Corpus sıra: 2; canlı durum: **success**.

Parse edilen ihtiyaç: {"kisi_baglami": "partner", "ana_amac": "kahve_icmek", "alt_amaclar": ["birlikte_vakit"], "aktiviteler": ["oturmak"], "ziyaret_baglamlari": ["birlikte_vakit"], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": []}

- **Günevi Atölye /Cafe**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Starbucks**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Kollekt**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.

Bilinmeyenler: Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Kahve ve aynı yerde oturma bir ziyaret olarak değerlendirilmeli. Oturma ifadesi ikinci rota durağı değildir. Kahve seçenekleri ilgili; oturma kapasitesi ve partner bağlamına uygunluk sahada doğrulanmadı.

## 3. sevgilimle takılıcaz

Corpus sıra: 3; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": "partner", "ana_amac": "birlikte_vakit", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": ["birlikte_vakit"], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": ["birlikte_vakit"]}

Önerilen mekan: yok.

Bilinmeyenler: birlikte vakit geçirmek; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Takılmak kahve veya romantik ortam anlamına gelmez. Amaç anlaşılmış olsa da birlikte vakit kullanımını destekleyen veri yok. Öneri yapılmaması güvenli; ürün ihtiyacı cevapsız.

## 4. sevgilimle eğlenicez

Corpus sıra: 4; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": "partner", "ana_amac": "eglence", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": ["birlikte_vakit"], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": ["eglence"]}

Önerilen mekan: yok.

Bilinmeyenler: eğlenmek; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Eğlenmek kahveyle doldurulmadı. Eğlence türü/işletme güncel programı yok; sonuçsuz kalma ürün açığı.

## 5. ailemi yemeğe götürcem

Corpus sıra: 5; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": "aile", "ana_amac": "yemek_yemek", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": ["birlikte_vakit"], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": ["aile_uygunlugu"]}

- **Crakers Pizza**: Yemek yemek için uygunluğunu doğrulayabildik. Gerçek veri desteği: yemek_yemek.

Bilinmeyenler: aileyle kullanım; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Pizza yemeğe ilgili ama aileyi yemeğe götürme talebine seçenek tek ve dar. Aile/grup uygunluğu bilinmiyor; yemek desteği tam aile deneyimi doğrulaması değildir.

## 6. ailecek yemek yiyebileceğimiz bir yer

Corpus sıra: 6; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": "aile", "ana_amac": "yemek_yemek", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": ["birlikte_vakit"], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": ["aile_uygunlugu"]}

- **Crakers Pizza**: Yemek yemek için uygunluğunu doğrulayabildik. Gerçek veri desteği: yemek_yemek.

Bilinmeyenler: aileyle kullanım; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Aile yemeği için Crakers Pizza kategori olarak ilgili. Aileye uygunluk açık bilinmeyen; alternatif yemek türü/oturma kapasitesi yok.

## 7. arkadaşlarla kahve içip sohbet edeceğiz

Corpus sıra: 8; canlı durum: **success**.

Parse edilen ihtiyaç: {"kisi_baglami": "arkadaslar", "ana_amac": "kahve_icmek", "alt_amaclar": [], "aktiviteler": ["sohbet"], "ziyaret_baglamlari": ["birlikte_vakit"], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": ["sohbet_uygunlugu"]}

- **Günevi Atölye /Cafe**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Starbucks**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Kollekt**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.

Bilinmeyenler: sohbet için uygunluk; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Arkadaşlarla kahve kısmı destekleniyor; sohbet, grup kapasitesi ve ses düzeyi bilinmiyor. Genel kahve önerisi kısmi karşılık.

## 8. Atakum'da kahve içelim

Corpus sıra: 9; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "kahve_icmek", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": "Atakum", "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": []}

- **Günevi Atölye /Cafe**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Kollekt**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.

Bilinmeyenler: Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Atakum canonical filtresiyle iki ilgili kafe. Starbucks ilçesi bilinmediği için Atakum diye gösterilmedi. Coğrafi doğruluk mevcut canonical ilişkiyle sınırlı; polygon doğrulaması yapılmadı.

## 9. laptop açıp çalışacağım

Corpus sıra: 11; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "calisma", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": ["calisma_uygunlugu"], "desteklenmeyen_istekler": ["calisma_uygunlugu", "calisma"]}

Önerilen mekan: yok.

Bilinmeyenler: çalışma / laptop uygunluğu; çalışmak; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Laptop işi için priz, internet, masa ve çalışma süresi gereksinimi önemli. Kafe etiketi bunları kanıtlamaz. Sonuçsuzluk veri kaynaklı.

## 10. çalışmalık sakin bir kafe

Corpus sıra: 12; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "calisma", "alt_amaclar": ["kahve_icmek"], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": ["sessiz_ortam", "calisma_uygunlugu"], "desteklenmeyen_istekler": ["calisma_uygunlugu", "calisma"]}

Önerilen mekan: yok.

Bilinmeyenler: çalışma / laptop uygunluğu; çalışmak; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Çalışma ve sakinlik birlikte isteniyor; iki ihtiyaç da doğrulanmamış. Kafe sözcüğü ayrı bir kahve molası/rota planı sayılmamalı. Yanlış olumlu öneriden kaçınıldı.

## 11. çocuklarla gidebileceğimiz yer

Corpus sıra: 13; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": "cocuklar", "ana_amac": "cocukla_aktivite", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": ["cocuk_uygunlugu"], "desteklenmeyen_istekler": ["cocuk_uygunlugu", "cocukla_aktivite"]}

Önerilen mekan: yok.

Bilinmeyenler: çocuklarla kullanım; çocuklarla bir şey yapmak; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Çocuk yaşı/aktivite türü ve güvenlik bilinmiyor. Genel aile/çocuk uygunluğu kanıtı olmadan öneri üretilmedi; veri eksikliği büyük.

## 12. manzaralı bir yerde oturalım

Corpus sıra: 14; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "birlikte_vakit", "alt_amaclar": [], "aktiviteler": ["oturmak"], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": ["manzara"], "desteklenmeyen_istekler": ["manzara", "birlikte_vakit"]}

Önerilen mekan: yok.

Bilinmeyenler: manzara; birlikte vakit geçirmek; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Manzara ve oturma desteği yok. Mekanın koordinatı veya olumlu sentiment manzara kanıtı değildir.

## 13. çok pahalı olmasın

Corpus sıra: 15; canlı durum: **clarification**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": null, "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": ["uygun_fiyat"], "desteklenmeyen_istekler": ["uygun_fiyat"]}

Önerilen mekan: yok.

Bilinmeyenler: fiyat düzeyi; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Bütçe tercihi anlaşılmış, ziyaret amacı eksik. Tek amaç sorusu makul; fiyatı uydurarak öneri yapılmıyor.

## 14. arabamız yok uzak olmasın

Corpus sıra: 16; canlı durum: **clarification**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": null, "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": "araçsız", "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": ["yakinda"], "desteklenmeyen_istekler": ["yakinda"]}

Önerilen mekan: yok.

Bilinmeyenler: yakınlık; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Arabasız/yakınlık anlaşılmış; amaç ve başlangıç noktası gerekir. İlk amaç sorusu sonucu değiştirebilir; yalnız amaç yanıtı ulaşım mesafesini doğrulamayacaktır.

## 15. wifi kesin olsun

Corpus sıra: 18; canlı durum: **clarification**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": null, "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": ["wifi"], "tercihler": [], "desteklenmeyen_istekler": []}

Önerilen mekan: yok.

Bilinmeyenler: Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Wi-Fi zorunlu koşulu korunmuş, amaç eksik olduğu için bir amaç sorusu var. Açık Wi-Fi bilinmeyeni ancak aday değerlendirmesinden sonra güvenle söylenebilir.

## 16. bu akşam nereye gidelim

Corpus sıra: 19; canlı durum: **clarification**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": null, "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bu akşam", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": []}

Önerilen mekan: yok.

Bilinmeyenler: Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Akşam zamanı korunmuş, aktivite amaçsız. Tek netleştirme makul. Yanıt sonrası güncel saatler yine bilinmeyen kalacak.

## 17. şimdi açık bir yer

Corpus sıra: 20; canlı durum: **clarification**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": null, "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "şimdi", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": []}

Önerilen mekan: yok.

Bilinmeyenler: Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Şimdi/açıklık isteği anlaşılmış. Amaç sorusu var; çalışma saatleri doğrulanmadığı için açık diye iddia yok.

## 18. tatlı yiyelim

Corpus sıra: 21; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "tatli_yemek", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": ["tatli_yemek"]}

Önerilen mekan: yok.

Bilinmeyenler: tatlı yemek; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Tatlı amacı doğru, yalnız yemek/kafe etiketinden tatlı varlığı çıkarılmadı. Tatlı ürün/menu verisi eksik.

## 19. kahvaltıya gidelim

Corpus sıra: 22; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "kahvalti_yapmak", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": ["kahvalti_yapmak"]}

Önerilen mekan: yok.

Bilinmeyenler: kahvaltı yapmak; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Kahvaltı ihtiyacı sıradan restoranla karşılanmış sayılmadı. Güncel kahvaltı menüsü ve servis saatleri yok.

## 20. müze gezmek istiyorum

Corpus sıra: 23; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "tarihi_kulturel_ziyaret", "alt_amaclar": ["gezme"], "aktiviteler": ["dolasmak"], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": ["muze_turu"], "tercihler": [], "desteklenmeyen_istekler": ["muze_turu"]}

Önerilen mekan: yok.

Bilinmeyenler: müze olarak ziyaret edilebilmesi; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: İlk incelemede genel tarih sonucu Tekkeköy Mağaraları müze isteğine bariz alt tür uyumsuzluğu oluşturuyordu. Düzeltme sonrası doğrulanmış müze türü olmadan sonuç yok. Bandırma adında müze geçmesi tek başına yayınlı alt tür claim kanıtı sayılmadı.

## 21. tarihi yer gezip sonra kahve içelim

Corpus sıra: 24; canlı durum: **success**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "kahve_icmek", "alt_amaclar": ["tarihi_kulturel_ziyaret", "gezme"], "aktiviteler": ["dolasmak"], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": []}

- **Günevi Atölye /Cafe**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Starbucks**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Kollekt**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.

Bilinmeyenler: Birden fazla etkinliğin aynı planda birleştirilmesi; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Yalnız kahve mekanları öneriliyor; tarihi ziyaret ayağı desteklenmiş değildir. Çoklu plan bilinmeyeni var. Bu yanıt tamamlanmış gezi planı sayılamaz; bariz eksik ihtiyaç mevcut.

## 22. biraz dolaşıp sonra yemek yiyelim

Corpus sıra: 25; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "yemek_yemek", "alt_amaclar": ["gezme"], "aktiviteler": ["dolasmak"], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": []}

- **Crakers Pizza**: Yemek yemek için uygunluğunu doğrulayabildik. Gerçek veri desteği: yemek_yemek.

Bilinmeyenler: Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Yemek ayağına tek pizza yeri ilgili; dolaşma ayağı ve iki durağın ulaşımı eksik. Tam plan başarısı sayılamaz.

## 23. eşimle sakin sakin kahve içelim

Corpus sıra: 26; canlı durum: **success**.

Parse edilen ihtiyaç: {"kisi_baglami": "partner", "ana_amac": "kahve_icmek", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": ["birlikte_vakit"], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": ["sessiz_ortam"], "desteklenmeyen_istekler": []}

- **Günevi Atölye /Cafe**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Starbucks**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Kollekt**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.

Bilinmeyenler: Sessiz ortam; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Sakinlik açık tercih olarak korunmuş ve bilinmeyen gösterilmiş. Kahve ilgisi var; ses düzeyi doğrulanmadığından tam karşılık yok.

## 24. aileyle tarihi bir yer gezelim

Corpus sıra: 30; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": "aile", "ana_amac": "tarihi_kulturel_ziyaret", "alt_amaclar": ["gezme"], "aktiviteler": ["dolasmak"], "ziyaret_baglamlari": ["birlikte_vakit"], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": ["aile_uygunlugu"]}

- **Bandırma Gemi-Müze ve Millî Mücadele Açık Hava Müzesi**: Tarih ve kültür gezisi için uygunluğunu doğrulayabildik. Gerçek veri desteği: tarihi_kulturel_ziyaret.
- **Tekkeköy Mağaraları**: Tarih ve kültür gezisi için uygunluğunu doğrulayabildik. Gerçek veri desteği: tarihi_kulturel_ziyaret.

Bilinmeyenler: aileyle kullanım; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: İki geniş tarih/kültür seçeneği ilgili olabilir. Aile uygunluğu, yaşa uygun anlatım, erişim ve süre bilinmiyor. Yer türü doğrulaması bu sorguda müze kadar dar değildir.

## 25. wi-fi mutlaka olsun kahve içeceğim

Corpus sıra: 66; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "kahve_icmek", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": ["wifi"], "tercihler": [], "desteklenmeyen_istekler": []}

- **Kollekt**: Kahve içmek için uygunluğunu doğrulayabildik. Wi-Fi isteğini de karşılıyor. Gerçek veri desteği: wifi, kahve_icmek.
- **Starbucks**: Kahve içmek için uygunluğunu doğrulayabildik. Wi-Fi isteğini de karşılıyor. Gerçek veri desteği: wifi, kahve_icmek.

Bilinmeyenler: Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Kollekt ve Starbucks için yayınlı Wi-Fi desteği var; zorunlu Wi-Fi koşulu yok sayılmadı. İnternetin güncel çalışması/performansı sahada doğrulanmış değil; iki sonuç sebebiyle insufficient.

## 26. internet şart laptop açacağım

Corpus sıra: 67; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "calisma", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": ["wifi"], "tercihler": ["calisma_uygunlugu"], "desteklenmeyen_istekler": ["calisma_uygunlugu", "calisma"]}

Önerilen mekan: yok.

Bilinmeyenler: çalışma / laptop uygunluğu; çalışmak; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Wi-Fi tek başına laptopla çalışma uygunluğunu kanıtlamaz. İş amacı için sonuç yok; çalışma alanı/priz/politika bilgisi gerekir.

## 27. otopark şart yemek

Corpus sıra: 70; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "yemek_yemek", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": ["otopark"], "tercihler": [], "desteklenmeyen_istekler": []}

Önerilen mekan: yok.

Bilinmeyenler: Otopark; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: İlk gold taramada empty çıktı; otopark kanıtı bilinmeyen adaylarla gerçek boş havuz ayrımı yanlıştı. Düzeltme sonrası insufficient ve açık Otopark bilinmeyeni; otopark varmış gibi yemek önerisi yok.

## 28. sakin kahveci

Corpus sıra: 74; canlı durum: **success**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "kahve_icmek", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": ["sessiz_ortam"], "desteklenmeyen_istekler": []}

- **Günevi Atölye /Cafe**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Starbucks**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Kollekt**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.

Bilinmeyenler: Sessiz ortam; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Kahve ilgili; sakinlik bilinmeyen. İsim veya sentiment sakin ortam kanıtı değildir. success etiketi tam sessizlik doğrulaması sayılmamalı.

## 29. şimdi kahve içelim

Corpus sıra: 91; canlı durum: **success**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "kahve_icmek", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "şimdi", "ulasim": null, "butce_ust_siniri": null, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": []}

- **Günevi Atölye /Cafe**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Starbucks**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.
- **Kollekt**: Kahve içmek için uygunluğunu doğrulayabildik. Gerçek veri desteği: kahve_icmek.

Bilinmeyenler: Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: Kahve seçenekleri ilgili, fakat şimdi açık oldukları doğrulanamıyor. API bugun_baglami ve UI açıklaması bunu söylüyor; açık venue başarısı sayılamaz.

## 30. en fazla 500 tl yemek

Corpus sıra: 99; canlı durum: **insufficient**.

Parse edilen ihtiyaç: {"kisi_baglami": null, "ana_amac": "yemek_yemek", "alt_amaclar": [], "aktiviteler": [], "ziyaret_baglamlari": [], "sehir": "Samsun", "ilce": null, "zaman": "bugün", "ulasim": null, "butce_ust_siniri": 500.0, "zorunlu_kosullar": [], "tercihler": [], "desteklenmeyen_istekler": []}

Önerilen mekan: yok.

Bilinmeyenler: Güncel fiyatın bütçe sınırını karşılaması; Güncel çalışma saatlerini doğrulayamadığımız için şu an açık olduğunu söyleyemiyoruz.

İnceleme / bariz alakasızlık / eksik ihtiyaç: 500 TL sayısal sınır korunmuş. Güncel fiyat yok; öneri yok. Düzeltmeyle bütçeyi karşılama açık bilinmeyen alanına da eklendi.


## Belge ilişkileri

Bağlı belgeler: docs/00-product/00-urun-felsefesi.md, 01-bilgi-mimarisi.md, 02-product-language.md, 03-karar-motoru.md, 04-sistem-mimarisi.md.

Etkilediği belgeler: docs/04-ai/05-ai-bilgi-motoru.md, docs/00-product/06-akilli-rota-motoru.md, docs/02-ux/07-ux-karar-akislari.md.

Bundan sonra okunacak belge: bu ölçümle birlikte faz25-1-oneri-gold.md ve faz25-1-promotion-veri-stratejisi.md. Sahada bağımsız öneri doğrulama planı planlanmıştır; gerçekleştirilmiş sayılmaz.
