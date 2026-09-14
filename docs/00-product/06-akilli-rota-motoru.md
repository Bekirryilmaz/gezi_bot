---
title: "06 Şamandıra — Akıllı Rota Motoru"
version: "1.0"
status: "nihai-oneri-kabul-bekliyor"
phase: "urun-davranisi"
last_update: "2026-09-13"
depends:
  - "00-urun-felsefesi.md"
  - "01-bilgi-mimarisi.md"
  - "02-product-language.md"
  - "03-karar-motoru.md"
  - "04-sistem-mimarisi.md"
  - "../04-ai/05-ai-bilgi-motoru.md"
affects:
  - "02-ux: Akıllı Rota karar akışları (planlanan)"
  - "01-research: günlük karar faydası araştırması (planlanan)"
  - "03-design: rota ve paylaşım sunum ilkeleri (planlanan)"
  - "08-admin: rota bilgi düzeltme ve işletim davranışı (planlanan)"
  - "09-business: ücretsiz ve Premium kapsam değerlendirmesi (planlanan)"
author: "Codex; kabul yetkisi: proje sahibi"
---

# Şamandıra — Akıllı Rota Motoru

> **Şamandıra insanlara en iyi rotayı oluşturmaz. O gün için en doğru günü oluşturmaya yardım eder.**

“Doğru gün”, sistemin kullanıcıya biçtiği yaşam tarzı değildir. Kullanıcının o gün yapmak istediği şeyin, gerçek zamanının, bütçesinin ve açık ihtiyaçlarının birlikte karşılık bulmasıdır. Bu bazen iki ziyaret, bazen uzun bir mola, bazen de başka yere gitmemektir.

Bu belge yalnız ürün davranışını tasarlar. Kod, framework, API, veritabanı veya teknik uygulama önerisi içermez. Tasarım örnekleri kurmacadır; gerçek mekân, güncel ulaşım veya platform yeteneği iddiası değildir. Kurallar nihai öneridir; uygulanmış, araştırmayla doğrulanmış veya kullanıcı tarafından kabul edilmiş yeni referans sayılmaz. Sondaki 40 maddelik öz eleştirinin kararları ana metne işlenmiştir; ardından nihai ürün kararı verilmiştir.

## 0. Kabul edilmiş referanslar ve kapsamın sınırı

00–05 belgeleri bu görevin açık talimatıyla kabul edilmiş referanstır. 05 dosyasında önceki “kabul bekliyor” ifadesi korunmuş olsa da bu görevde kullanıcının kabul beyanı esas alınır. Altı belgenin hiçbiri değiştirilmez.

| Referans | Bağlayıcı yön | Akıllı Rota karşılığı |
|---|---|---|
| 00 §2, §5–9 | Uygunluk yükünü azalt; açık ihtiyaç ve dürüstlük öncelikli | Günün amacını koru; kullanıcıyı daha çok durağa zorlama |
| 01 §6, §11–12 | Tek Keşfet; ayrı rota, profil veya liste paylaşım portalı yok | Oluşturma, kayıt ve paylaşımı mevcut karar bağlamının durumları olarak ele al |
| 02 §3–6, §8–9 | Amaç/tercih/zorunlu koşul ayrı; tempo puanı yok; güven iddiaya ait | Zaman, yürüme, ayakta kalma ve mola somut; toplam rota puanı yok |
| 03 §10–12, §18 | Anlamlı ziyaret dizisi; toplam yük; kullanıcı kontrollü öğrenme | Varışa göre denetim, amaç koruyan değişiklik ve erken bitiş |
| 04 §4, §14, §18, §26 | Tek karar otoritesi; kanal anlamı; kesintide dürüst daralma | Durak uygunluğunu yeniden icat etme; paylaşımda aynı sınırları koru |
| 05 §27–35, §38–45 | Bir İz; kanıt/tercih ayrımı; düzeltmenin sonuca yayılması | Gözlemi ziyaret niyetinden ayır; eski kaydı yeni kanıt sayma |

### Açık gerilimler ve çözüm

**Tempo:** Kullanıcının “yavaş”, “rahat”, “yoğun” sözü anlaşılabilir; yeni tempo veya enerji puanı oluşturulmaz. §4 ve §5 bu sözleri somut sınırlarla karşılar. 02 §5 değiştirilmez.

**Kaydetme, Gezeceğim Yerler, koleksiyon ve paylaşım:** Altı belgede bunların tamamlanmış davranış tanımı bulunmuyor. Bu metin var olan uygulamayı tarif etmez; kullanıcının istediği kapsam için öneri getirir. Mevcut Keşfet/yer bağlamındaki saklama ve yeniden açma yeterlidir. Bağımsız profil, sosyal liste dizini veya rota portalı eklenmez.

**Premium:** 01 §12 mevcut mimaride ücret planları sayfasını kapsam dışı tutar. Buradaki Premium maddeleri olası değer alanlarıdır; satış, ödeme, üyelik veya yeni sayfa yayını kararı değildir. Temel karar faydası ücretsizdir. Ticari kullanım açılmadan önce fayda kanıtı ve mevcut yapı içindeki deneyim ayrıca değerlendirilir.

**Paylaşılabilir adres:** Tek rotayı salt okunur açmak, keşfedilebilir rota portalı kurmak anlamına gelmez. Alıcı mevcut Keşfet'in paylaşılmış karar durumuna gelir. Kamuya açık kullanıcı dizini, rota arama motoru ve yeni içerik ailesi oluşmaz. Ayrı bir sayfa ailesi gerekirse 01 §12 kapsamında açık değişiklik önerisi gerekir; bu belge o değişikliği yapmaz.

**Günün kapsamı:** Bir günün içindeki karar dilimi esastır; sabah başlamak veya bütün günü doldurmak gerekmez. Çok günlük tatil takvimi, konaklama organizasyonu, rezervasyon merkezi ve şehirler arası seyahat yönetimi bu tasarımın kapsamı değildir. Gece yarısını geçen kısa bir akşam aynı karar olarak sürebilir; tarih değişimi görünür kalır.

## 1. Akıllı Rota tam olarak nedir?

Akıllı Rota, **bugünkü amacı koruyan, yükü anlaşılır kılan ve koşullar değiştiğinde kullanıcıya anlamlı devam kararları sunan bir günlük karar desteğidir.**

Üç ilişkiyi birlikte değerlendirir:

- Yer ile ihtiyaç: Burada yapmak istediğimiz şeyi gerçekleştirebilir miyiz?
- Ziyaret ile ziyaret: Bu iki faaliyet bu sırayla, bu süre ve geçişle birlikte anlamlı mı?
- Plan ile gerçek gün: Geç başlarsak, yorulursak veya koşullar değişirse neyi koruyup neyi değiştirebiliriz?

Harita bu kararın konumunu açıklar. Yol tarifi seçilmiş durağa ulaşmaya yardım eder. Akıllı Rota'nın değeri ise neden gidileceğini, hangi sıranın anlamlı olduğunu, toplam yükü ve vazgeçme seçeneklerini açıklamasıdır. Bu ayrım diğer ürünlerin ne yapamadığına ilişkin iddia değildir.

Çıktı, bütün boşlukları doldurulmuş bir ajanda değildir. Kullanıcı en az şu bilgiyi anlayabilmelidir: bugün neye alan açılıyor; hangi ziyaretler bunun için gerekli; ne kadar zaman ve hareket gerekiyor; ne belirsiz; nerede durabilir veya fikrini değiştirebilir.

“Akıllı” sözcüğü gizli üstünlük puanı veya kusursuz tahmin anlamına gelmez. Daha az karar yükü, daha açık ödünler ve değişiklikte daha az yeniden düşünme anlamına gelir.

## 2. Ne zaman devreye girmeli?

Birden fazla faaliyet, birkaç yerin birlikte değerlendirilmesi veya ayrılan sürenin anlamlı kullanımı istendiğinde. “Yemekten sonra biraz yürümek istiyoruz”, “Bu üç yere bugün gidebilir miyim?” ve “İki saat içinde konuşup dinlenmek istiyoruz” uygundur.

Tek kafe araması, sırf iki yer daha eklenebilir diye rotaya dönüşmez. Kullanıcı bir yere karar verdiyse yol tarifine geçebilir. Akıllı Rota daveti görevi tamamlamasını geciktirmez.

Başlangıçta bir ana öneri gösterilir. Gerçek bir karar farkı varsa en çok iki ek gün seçeneği açılabilir: örneğin daha az yürüyüş ile daha uzun açık alan zamanı. Bu, üç sonuç doldurma kotası değildir. Yer adaylarında 01 ve 03'ün Keşfet için üç ila beş, yer alternatifleri için en çok üç sınırı korunur.

Durak sayısına başarı hedefi konmaz. Tek yer ana amacı karşılıyorsa tek yer yeterlidir. Hiçbir savunulabilir dizi bulunamıyorsa sonuç üretmemek geçerlidir.

## 3. Kullanıcı hangi yollarla başlayabilir?

Beş giriş aynı karar bağlamına ulaşır. Ayrı ürünler ve ayrı kurallar oluşturmaz.

| Giriş | Kullanıcının yaptığı | Motorun ilk karşılığı | Korunan sınır |
|---|---|---|---|
| Doğal dil | “Öğleden sonra iki saatimiz var; biraz yürüyüp uzun konuşalım.” | Anlaşılan amaç, süre ve açık koşulları kısa gösterir; yalnız belirleyici eksik sorulur | Anlaşılmayan cümle parçası kaybolmaz; sözlü tahmin zorunlu sınıra dönüşmez |
| Birkaç yer seçmek | Keşfet, yer veya kayıtlı yerlerden aday seçer | “Bu yerleri birlikte değerlendirelim” ile günün yapılabilirliğini inceler | Seçmek, her yeri mutlaka ziyaret etmek değildir; “mutlaka” ayrı seçimdir |
| İhtiyaç seçmek | Kısa yürüyüş, sohbet, yağmurdan korunma gibi bir veya birkaç amaç seçer | İhtiyaçların önceliğini gerektiğinde netleştirir; uygun diziyi önerir | “Çocukla” otomatik ihtiyaç paketi olmaz; ihtiyaçlar sonsuz etiket listesine dönüşmez |
| Hazır koleksiyon | Belirli amacı ve coğrafyası açıklanan seçkiyi başlangıç alır | Koleksiyondaki yerleri günün zamanına ve koşullarına göre yeniden değerlendirir | Koleksiyon daha önce onaylanmış bugünkü rota değildir; ticari üstünlük taşımaz |
| Tamamen boş | Amaç veya yer eklemeden boş taslak açar | Yazma, yer ekleme ve ihtiyaç seçme yollarını sunar; hiçbirini zorunlu kılmaz | Sahte kişiselleştirme ve otomatik şehir seçimi yok; boş taslak da korunabilir |

Doğal dil akışında “en iyileri gezdir” isteği evrensel en iyi listesine dönüşmez. “Bugün neye zaman ayırmak istiyorsun?” gibi kararı değiştirecek kısa netleştirme yapılır. Her istekten sonra uzun bir onay formu açılmaz; anlaşılan bağlam düzenlenebilir biçimde görünür.

Seçilmiş yerlerin tamamı aynı gün sığmıyorsa kalanlar kaybolmaz. “Bu ikisi birlikte sığıyor; üçüncüyü eklemek ana ziyareti kısaltıyor” açıklamasıyla kullanıcıya seçim verilir. Motor seçilmiş yeri habersiz çıkarmış gibi davranmaz.

### Hazır koleksiyonun niteliği

Koleksiyonun amacı, yerlerin ortak karar ilişkisi ve hangi koşullarda başlangıç olarak işe yarayacağı açıklanır. “Şehrin vazgeçilmezleri” gibi evrensel iddialar kullanılmaz. Editoryal seçki, bağımsız uygunluk kanıtı değildir. Koleksiyonun yenilenme tarihi, bütün yer bilgilerinin doğrulandığı tarih gibi sunulmaz.

Koleksiyonu açan kişi tek bir yeri de alabilir. Otomatik bütününü ekleme, tamamlanma yüzdesi ve koleksiyon bitirme ödülü yoktur. İlgili ve yeterli seçki yoksa bu giriş için içerik uydurulmaz.

## 4. Hangi bilgiler istenir?

**Başlamak ve kaydetmek için zorunlu form alanı yoktur. Bir yapılabilirlik iddiası kurmak için gereken bilgiler ise o iddianın koşuludur.** Soru sormamak, bilinmeyenleri varsayarak doldurmak anlamına gelmez.

| Bilgi | Ne zaman gerekli? | Bilinmiyorsa davranış |
|---|---|---|
| Aranacak şehir/çevre | Yeni yer önermek veya geçiş değerlendirmek için | Seçilen yerden açıksa tekrar sorulmaz; belirsizse coğrafya seçilir. Taslak kurulabilir |
| Amaç veya seçilmiş faaliyet/yer | Anlamlı dizi önermek için | Boş taslak veya kullanım amaçları açıklanmış başlangıçlar; “sana uygun” yok |
| Tarih ve başlangıç saat aralığı | Açıklık, son giriş, etkinlik veya zaman bağımlı uygunluk için | Tarihsiz fikir taslağı; belirli saatte yapılabilirlik sözü verilmez |
| Toplam süre veya zorunlu bitiş | “Bu zamana sığar” sonucu için | Kalış/geçiş yükü biliniyorsa anlatılır; günün sınırsız olduğu varsayılmaz |
| Başlangıç noktası | İlk ulaşım ve kapıdan kapıya toplam için | İlk duraktan başlayan kapsam açıkça belirtilir |
| Bitiş noktası/dönüş | Dönüş istenmişse veya varılması gereken yer varsa | Dönüş dahil edilmez; “dönüş hariç” görünür. Başlangıca dönüş varsayılmaz |
| Ulaşım biçimi | Bağlantı ve hareket yükü için | Kısa mesafeden yürüme kararı çıkarılmaz; ilgili seçim istenir |
| Bütçe ve kapsamı | Bütçe uyumu veya kesin üst sınır için | Bütçe uyumu iddia edilmez; bilinen zorunlu giderler yine gösterilir |
| Kişi sayısı | Toplam ücret, kapasite veya grup koşulu için | Kişi başı ve grup toplamı karıştırılmaz; gerekiyorsa sorulur |
| Zorunlu ihtiyaçlar | Kullanıcı belirttiğinde tüm dizi için | Bilinmeyen koşul karşılandı sayılmaz; kullanıcıya sağlık/kimlik anketi yapılmaz |
| Mutlaka ziyaret edilecek yer/saat | Kullanıcı sabitlediyse | Seçilen aday otomatik zorunlu durak sayılmaz |
| Kalış ve hareket tercihleri | Alternatifleri anlamlı biçimde ayırıyorsa | Gerekçeli, değiştirilebilir öneri verilir; kişilik çıkarılmaz |
| Rezervasyon veya bilet durumu | Kullanım için gerekiyorsa | “Gerekli, tamamlandığı bilinmiyor” denir; işlem yapılmış varsayılmaz |

Bütçede kişi başı/toplam, para birimi ve ulaşımın dahil olup olmadığı yalnız sonucu etkiliyorsa netleştirilir. “Ucuz” tercih, “toplam en fazla 800 TL” zorunlu sınırdır. Kullanıcı açıkça kişi başı sınır söylediyse yeniden sormaya gerek yoktur.

Başlangıç için tam ev adresi gerekmez; buluşma noktası veya seçilmiş kamusal nokta yeterli olabilir. Daha kaba bir konumla doğru toplam çıkarılamıyorsa kapsam daralır. Konum izni, üyelik, telefon ve e-posta temel rota yardımının koşulu değildir.

### İsteğe bağlı bilgiler

Manzara, daha az ses, açık/kapalı alan tercihi, yeni yer deneme isteği, daha uzun oturma, kaç kez yer değiştirmek istediği, özel bir buluşma noktası, “bu sefer hatırlanan tercihlerimi kullanma” ve özel notlar. Her biri sonucunu değiştirebildiği yerde sunulur; tek seferde soru listesine dönüştürülmez.

### Hiç sorulmaması gerekenler

Karar için gereksiz tam kimlik, gelir/meslek/sosyal sınıf, ilişki durumu, arkadaş adları, çocukların tam doğum tarihi, teşhis veya sağlık raporu, sürekli konum geçmişi, rehber ve sosyal hesap erişimi. “Basamaksız yol gerekli mi?” işlevsel ihtiyaçtır; “hangi engelin var?” gerekli değildir. Yaşa bağlı bilet/kullanım koşulu varsa yalnız ilgili yaş aralığı sorulabilir.

Kullanıcının kendi ifadesinden gerekli koşul ayrılır; hassas ayrıntı kalıcı profile veya paylaşım metnine otomatik taşınmaz. Mekân bilgisi açığı kullanıcıya uzun araştırma ödevi olarak yüklenmez.

### Soru sırası

Önce sonucu bütünüyle değiştiren eksik belirlenir. Bir kısa soru sorulur; cevap yeni zorunlu soruyu doğuruyorsa neden gerektiği açıklanır. Kullanıcı yanıtlamak istemezse hangi kapsamda devam edilebildiği söylenir. Soru sayısını yapay biçimde azaltmak için kritik varsayım gizlenmez; her alanı öğrenmek için de soru sorulmaz.

## 5. Motor nasıl düşünmeli?

Sıra “önce en kısa yol, sonra güzel yerler” değildir. 03 §10.4 korunur: **zorunlu koşullar → ana amaç → zaman ve toplam yükün yapılabilirliği → anlamlı tamamlayıcılık → benzer uygunlukta daha az gereksiz yol ve çaba.**

Zaman veya mesafe kullanıcı tarafından üst sınır yapılmışsa ilk aşamadaki zorunlu koşuldur. Bunların tercih olduğu durumda ise ana amacı otomatik geçersiz kılamaz. Aşamalar birbirinden kopuk tek seferlik işlem değildir; sıra değişince varış ve uygunluk yeniden kontrol edilir.

| Adım | Karar sorusu | Sonuç |
|---|---|---|
| 1. Söyleneni ayır | Amaç, tercih, zorunlu koşul ve sabit ziyaret ne? | Anlaşılan gün; çelişen veya anlaşılmayan ifade görünür |
| 2. Bilinebilirliği kontrol et | Bu yerleri ve gerekli koşulları yeterince biliyor muyuz? | Bilgi eksiği ile bilinen engel ayrılır |
| 3. Zorunlu sınırları koru | Her gerekli durak, geçiş, bitiş ve grup koşulu karşılanıyor mu? | Karşılanmayan/bilinmeyen koşulla olumlu tam rota çıkmaz |
| 4. Ana amacı yerleştir | Günün bu kullanıcı için asıl değeri nerede gerçekleşiyor? | Öncelikli faaliyet için anlamlı kalış korunur |
| 5. Bütün gün yükünü denetle | İlk yol, geçiş, bekleme, ziyaret, mola ve dönüş birlikte sığıyor mu? | Gereken toplamlar, kapsam ve belirsizlik açık |
| 6. Sırayı ve tamamlayıcıları seç | Hangi sıra amacı ve kullanılabilir saatleri destekliyor? | Her durağın işi ve sıradaki nedeni var |
| 7. Kırılganlığı değerlendir | Tek bir gecikme veya ortak olay planı bütünüyle bozuyor mu? | Gerekli yerde daha sade plan veya farklı riske dayanan alternatif |
| 8. Anlamlı ödünleri karşılaştır | Daha az yürüyüş mü, daha uzun sohbet mi; kullanıcının önceliği ne? | Genel kalite puanı yerine somut fark |
| 9. Açıkla ve kullanıcıya bırak | Neden, hangi ödün, hangi bilinmeyen ve hangi değişiklik yolu? | Düzenlenebilir öneri |
| 10. Değişiklikte yeniden denetle | Yeni sıra/yer/saat kalan günü etkiliyor mu? | Eski olumlu hüküm otomatik korunmaz |

### Süre, mesafe ve “tempo”

Süre; ulaşım, bekleme, anlamlı kalış, yerleşme/geçiş, mola ve istenen dönüş olarak ele alınır. Aynı kıyı yürüyüşü hem faaliyet hem geçişse bir kez sayılır; iki amaca hizmet ettiği anlatılabilir.

Mesafe tek başına efor değildir. Eğim, yüzey, merdiven, aktarma, oturma olanağı ve kesintisiz ayakta kalma ilgiliyse değerlendirilir. Araç seçildiğinde park etme ve son yaklaşım biliniyorsa toplamın parçasıdır; araçtan indiği anda girişte olacağı varsayılmaz.

“Rahat olsun” talebi için sonuç üzerinde fark yaratan somut soru sorulur: “Daha az yürümek mi, daha az yer değiştirmek mi?” Kullanıcı “ikisi de” diyebilir. Ürün bunları bir tempo skalasında eritmez. Bir genel “rahat” seçeneği sunulacaksa değiştirdiği yürüyüş, durak değişimi ve mola tercihleri görünür olmalıdır.

Anlamlı kalış süresi mekânın ve faaliyetin dayanağına bağlıdır. Kullanıcı sırf üç durak sığsın diye bir müze ziyaretini anlamsız birkaç dakikaya sıkıştıramazmış gibi engellenmez; ancak ürün bunun amaç için yeterli olduğunu söylemez. Durak sayısını azaltmak daha iyi bir öneri olabilir.

### Belirsiz toplamlar ve esneklik

İyi ihtimallerin toplamı “yetişirsin” sonucuna dönüşmez. Kuyruk, yağış veya aynı ulaşım aksı birkaç parçayı birlikte etkileyebilir. Kararın sağlamlığı bu ortak etkilere göre değerlendirilir; keyfî bir yüzde veya her rotaya sabit dakika eklenmez.

Kullanıcının serbest bırakmak istediği süre, gözleme dayanan gecikme payından ayrıdır. “20 dakikayı boş bırakalım” bir kullanıcı tercihidir; “gecikmeler en fazla 20 dakika olur” tahmini değildir. Her ikisi de zorunlu zaman sınırında yer kaplar.

Bütçenin kapsamı bütün gün boyunca aynı tutulur. Bilinen üst tahmin sınırı aşıyorsa uyum iddia edilmez. Gerekli ücret bilinmiyorsa ücretsiz sayılmaz. Sınırsız veya tercihe bağlı tüketim için kesin toplam üretilemez.

## 6. Kullanıcı hangi kararları değiştirebilmeli?

Kullanıcı amacı, önceliği, tarih/saat/süreyi, coğrafyayı, başlangıcı/bitişi, ulaşımı, bütçeyi, zorunlu koşulu, kalış süresini, molayı, durakları ve sırayı değiştirebilir. Kullanıcı istediğinde bütün öneriyi reddedebilir.

Üç sabitleme birbirinden ayrılır:

- **Bu yer mutlaka olsun:** Yerin varlığı korunur; saati ve sırası ayrıca sabit değilse değişebilir.
- **Bu saatte burada olmalıyım:** Saat/buluşma koşulu korunur; uygun sıra buna göre aranır.
- **Bu sırayı koru:** Göreli sıra korunur; yer varlığına ilişkin başka seçimler ayrıca görünürdür.

Bir seçim diğer kilitleri gizlice açmaz. Motorun eklediği tamamlayıcı duraklar kullanıcı sabitlemedikçe zorunlu olmaz. Zorunlu koşulu tercihe çevirmek kullanıcı eylemidir; öneriyi kabul etmek veya uyarıyı kapatmak bu değişiklik sayılmaz.

Kullanıcı bilinen uyuşmazlığa rağmen yeri taslakta tutabilir. Taslak “senin seçimin” olarak kalır; Şamandıra bunu uyumlu veya yapılabilir öneri diye sunmaz. Kullanıcı ısrar etti diye yer bilgisi değişmez.

## 7. Motor hangi kararları otomatik vermeli?

Oluşturma isteği, belirtilmiş sınırlar içinde ilk öneriyi kurmaya yeterlidir. Her durak için ayrı onay penceresi açılmaz.

| Otomatik verebilir | Açıklama veya kullanıcı seçimi gerektirir |
|---|---|
| Kimliği kesin aynı yerin yanlışlıkla çift eklenmesini belirtmek; ikinciyi öneriden ayırmak | Bilinçli ikinci ziyaret veya farklı şubeyi silmek |
| Sabitlenmemiş adaylar için ilk sıra ve gerekçeli kalış önermek | Kullanıcının koruduğu sıra, saat veya durağı değiştirmek |
| Amaca katkısı olmayan otomatik tamamlayıcıyı hiç eklememek | Seçilmiş bir yeri habersiz çıkarmak |
| Düzenleme sonrası toplamları ve varış koşullarını yeniden değerlendirmek | Bütçe, bitiş, ulaşım veya coğrafyayı genişletmek |
| Eski uygunluk iddiasını yeni engel nedeniyle durdurmak | Engel karşısında kullanıcı adına yeni amaç seçmek |
| Aynı amaca ve sınırlara uyan az sayıda alternatif bulmak | Harcama, bilet alma, rezervasyon ve dış paylaşım yapmak |
| Küçük bilgi değişimlerini ilgili açıklamaya yansıtmak | Kullanıcının sürmekte olan gününü sessizce yeniden düzenlemek |

Kullanıcı “kalanını yeniden düzenle” derse mevcut sınırlar içinde yeni sıra ve sabitlenmemiş tamamlayıcılar önerilebilir. Tek bir değişiklik karşılığı bütün günün rastgele yenilenmesi uygun değildir. Kabul edilen değişiklik kısa fark özetiyle görünür olur; geri alınabilir.

## 8. Rota nedenlerini nasıl açıklamalı?

Gerekçe üç düzeyde çalışır:

1. **Günün bütünü:** “Sohbete daha çok zaman ayırmak için iki ziyaret önerdik; son durak dönüş noktasına yakın.”
2. **Durağın rolü:** “Burada kısa yürüyüş isteğin karşılanıyor. Uzatmak sonraki oturma süresini azaltır.”
3. **Sıranın ve değişikliğin nedeni:** “Müzeyi öne aldık; son giriş saati sonraya bırakmayı zorlaştırıyor.”

Her gerekçe gerçek dayanakla üretilir. “Sana özel hesapladık” açıklama değildir. “Başka sırayla ne değişir?” sorusu somut süre, erişim veya amaç farkıyla cevaplanır. İç puanlar, teknik ağırlıklar, ham yorum ve ara muhakeme gösterilmez.

İlk anlatım; ana neden, önemli ödün ve gerekli bilinmeyeni birlikte taşır. Ayrıntı isteğe bağlı açılabilir. Kritik engel olumlu başlığın altında gizlenmez. “Neden bunu eklemedin?” yanıtı yalnız gerçekten belirleyici gerekçeyi anlatır; kullanıcının bütçesini veya zevkini yargılamaz.

## 9. Belirsizlik nasıl gösterilmeli?

Güven bütün rotaya verilen bir yıldız veya yüzde değildir. Durak, geçiş, saat ve maliyet hakkındaki gerekli iddiaların sınırları ayrı kalır. Kullanıcı bu ayrımları iç değerlendirme etiketlerini ezberlemeden anlayabilmelidir.

| Durum | Kullanıcıya anlamı | Devam |
|---|---|---|
| Dayanaklı tahmin | “Bu geçiş yaklaşık 15–25 dakika; varış trafik koşullarına bağlı.” | Aralığın toplam ve bitişe etkisi görülür |
| Bilinen koşula bağlılık | “Bu ziyaret için önceden rezervasyon gerekiyor.” | İşlem tamamlanmadan yer ayrılmış sayılmaz |
| Kritik bilinmeyen | “Kullanacağın geçişte basamaksız erişimi doğrulayamıyoruz.” | Bütün rota için erişim uyumu verilmez; bilinen başka bağlantı aranır |
| Çözülemeyen çelişki | “Bu tarih için ziyaret saatleri netleşmedi.” | Saat uydurulmaz; ilgili ziyaret değerlendirilemeyebilir |
| Eskimiş bilgi | “Kayıttaki ücret bu ziyaret için güncel değil.” | Eski rakam zorunlu bütçeyi geçiremez |
| Bilinen engel | “Bu sırada ikinci durağın son girişine yetişilemiyor.” | Sıra, süre veya yer değişikliği açık seçenek olur |
| Kapsam eksikliği | “Bu şehirde bu koşulları karşılayan bir dizi için yeterli bilgimiz yok.” | Taslak ve bilinen yerler korunur |
| Geçici kesinti | “Geçiş sürelerini şu anda değerlendiremiyoruz.” | Eski süre yeni/canlı sonuç gibi kullanılmaz |

“Koşula bağlı” bilinmeyen zorunlu koşul için kaçış etiketi değildir. Bilinen bir rezervasyon gereği ile rezervasyonun gerekip gerekmediğinin bilinmemesi farklıdır.

Tek bir kritik eksik bütün gün hakkında genel “güvensiz” hükmü üretmez. Hangi kısmın artık savunulamadığı belirtilir; bağımsız bilinen kısım kullanılabilir. Buna karşılık gerekli bağlantı eksikse olumlu tam gün vaadi sürmez.

Paylaşılan kısa metin, sesli anlatım ve harita aynı belirsizliği taşır. Renk tek başına durum anlatmaz. Bilginin son kontrol zamanı yalnız ilgili iddiaya bağlanır; rota kaydetme zamanı doğrulama tarihi değildir.

## 10. Kullanıcı rotayı nasıl düzenlemeli?

Düzenleme, yeni bir başlangıç formu doldurmak olmamalıdır. Doğal dil ve doğrudan eylemler aynı sonucu verir: “Son yeri çıkar”, “Burada daha uzun kalalım”, “Daha az yürüyelim”, “İlk iki yer aynı kalsın”.

Her değişiklik şu döngüyü izler: **niyeti al → etkisini değerlendir → değişeni ve korunamayanı göster → sonucu sürdür veya geri al.**

Kullanıcının açıkça istediği basit değişiklik uygulanır; ayrıca onay istemek zorunlu değildir. Fakat değişiklik başka bir koşuldan vazgeçmeyi gerektiriyorsa o ek karar kullanıcıya bırakılır. Motor doğrudan istenen değişiklik bahanesiyle yeni ödün kabul edemez.

Örnek: Bir durak çıkarılır; boşalan 40 dakika otomatik yeni yere doldurulmaz. Kullanıcı mevcut ziyareti uzatabilir, serbest bırakabilir veya alternatif isteyebilir. Ana amacı taşıyan durağın çıkarılması halinde “Bu değişiklikten sonra sohbet için bir durak kalmıyor” denir; yeni amaç uydurulmaz.

Liste üzerinde düzenlemek, harita kullanmadan da mümkün olmalıdır. Klavye ve yardımcı teknolojilerle ekleme, çıkarma, sıra değiştirme ve geri alma tamamlanabilir. Yeniden değerlendirme sürerken hangi değişikliğin beklediği görünür; daha eski sonuç yeni seçimi geri alamaz.

## 11. Durak sırası değiştirilebilir mi?

Evet. Sürükleme tek yöntem olamaz; “öne al”, “sona al” veya “şundan sonra” karşılığı bulunur. Yeni sıranın varış, son giriş, kalış, bütçe, dönüş ve gerekli erişim üzerindeki etkisi birlikte değerlendirilir.

Sıra değişimi bilinen engel yaratıyorsa kullanıcı seçimi taslakta korunabilir, fakat yapılabilir rota hükmü kaldırılır. Motor otomatik eski sıraya sıçramaz. “Bu sırayı tut” ve “uygun sırayı göster” birbirinden ayrılır.

Zamanı sabit bir ziyaret taşınırken o saat sessizce değişmez. Kullanıcı sırayı koruyabilir, saati ayrıca değiştirebilir veya durağı çıkarabilir. Tamamlandığı kullanıcı tarafından belirtilen ziyaretler geçmişteki yerini korur; kalanlar düzenlenir.

## 12. Yer eklenip çıkarılabilir mi?

Evet. Keşfet'ten, yer sayfasından, Gezeceğim Yerler'den veya doğal dille eklenebilir. Eklenince bütün günün yükü değişir; yalnız yeni yerin uygunluğu kontrol edilmez.

“Yerine başka seçenek” aynı rolü ve zorunlu koşulları koruyan alternatif arar. “Yeni bir şey ekle” farklı amaç eklemek olabilir; motor bu iki isteği karıştırmaz. Aynı bağlamda reddedilmiş yer, kullanıcı geri almadıkça farklı sıfatlarla dönmez.

Bilgisi yetersiz bir yer kullanıcının kişisel taslak notu olarak kalabilir. Yer kimliği doğrulanmıyorsa resmî yer kartı, harita noktası veya öneri üretilmez. Özel not kendiliğinden kamusal yer kaydına dönüşmez; yer bildirimi ayrı ve isteğe bağlıdır.

Bir durağı rotadan çıkarmak kayıtlı yer listesinden silmez. Son durağı çıkarmak boş taslağa döner; kullanıcı hata yapmış sayılmaz. Motor tek yer kaldığında sırf “rota” adını hak etmek için başka yer eklemez.

## 13. Gün başladıktan sonra ne olur?

Başlatmak zorunlu takip veya konum izni değildir. Kullanıcı isterse “Şimdi başlayacağım”, “Buradaydım”, “Bu durağı atla”, “Burada kalacağım” veya “Günü bitir” diyebilir. Yol tarifine geçiş, varış veya ziyaret tamamlandı anlamına gelmez.

Geç kalma, yeni kapanma, kullanıcı yorgunluğu, bütçe değişikliği veya anlamlı hava/ulaşım değişimi kalan bölümün yeniden değerlendirilmesini gerektirebilir. Ürün yalnız erişebildiği güncellemeleri kullanır; sürekli canlı izleme vaadi vermez.

Öncelik: tamamlanmış ziyaretleri koru; kalan ana amacı ve zorunlu koşulları koru; gereksiz tamamlayıcıları azaltmayı öner; aynı rolü karşılayan başka seçenek ara; hâlâ mümkün değilse amacı karşılayamadığını söyle. Erişim veya bitiş şartı “günü kurtarmak” gerekçesiyle silinmez.

Her küçük tahmin dalgalanmasında öneri değiştirilmez. Değişiklik yapılabilirliği, ana amacı veya anlamlı yükü etkiliyorsa kısa açıklama gösterilir. Bildirim ancak izinli kapsamda ve ilgili etkin karar için yapılır; kapanmış geçmiş günler sürekli uyarı üretmez.

Erken bitiş memnuniyetsizlik veya başarısız tamamlama değildir. “Bugün bu kadar” geçerli çıkıştır. Geri bildirim vermeden ayrılabilir; kalan yerler otomatik gidilmedi/istenmiyor kaydına dönüşmez.

## 14. Şehir değiştirince ne olmalı?

**Keşfet'te başka şehre bakmak ile rotanın şehrini değiştirmek farklı eylemdir.** Gezinti, açık veya kaydedilmiş rotayı yeniden yazmaz. Şehir başlığı her zaman görünürdür.

“Bu günü başka şehir için düşün” seçimi yeni taslak oluşturur; önceki taslak korunur. Kullanıcının açıkça taşımak istediği amaç ve tercihler başlangıç olabilir. Eski yerler, başlangıç/bitiş, rezervasyonlar, geçişler ve yerel maliyetler aktarılmış sayılmaz. Tarih, saat ve grup koşulları da yeni bağlamdaki geçerliliği görünür biçimde gözden geçirilir; hiçbir zorunlu koşul sessizce kaldırılmaz.

Eski şehrin sabitlenmiş yeri yeni şehirde eşdeğer isimli bir yerle değiştirilmez. “Bu ziyaret eski şehirde; yeni gün taslağına taşınmadı” denir. Eski rotaya dönüş mümkündür.

Farklı şehirlerden yerler aynı taslağa eklenirse şehirler arası geçişin bu günlük kapsamda desteklenmediği açıklanır. Kullanıcıdan günleri/şehir bağlamlarını ayırması istenebilir; otomatik çok günlük seyahat planı yaratılmaz. Şehir değişikliği, kapsanmayan şehirde sahte rota üretme gerekçesi olmaz.

## 15. Rota kaydedilebilir mi?

Evet. Kaydedilen şey yalnız sıralı yer listesi değil, **seçilmiş günün amacı, kullanıcının kararları, kapsamı ve o sırada bilinen önemli sınırlarıdır**. Gereksiz hassas serbest metin ve konum geçmişi otomatik kalıcılaştırılmaz.

Boş, tarihsiz, kısmi ve uyuşmazlık içeren taslaklar da kaydedilebilir. Kaydetmek onaylanmış yapılabilirlik, rezervasyon, ziyaret veya beğeni değildir. “Kaydedildi” yalnız kaydın gerçekten tamamlandığında gösterilir; başarısızsa taslak görünür kalır ve yeniden deneme yolu vardır.

Hesapsız kullanıcı bulunduğu cihazdaki kayda yeniden ulaşabilir; cihaz verisi silinirse veya cihaz değişirse korunma garantisi verilmez. Bu sınır kayıt anında anlaşılır olur. Cihazlar arası devam ayrı, isteğe bağlı bir kolaylıktır; ilk kararın önüne hesap duvarı koymaz.

| Yaşam durumu | Anlamı | Yeniden kullanım |
|---|---|---|
| Boş/tarihsiz taslak | Henüz ziyaret koşulları kurulmadı | Eksik bağlam görünür biçimde tamamlanır |
| Değerlendirilmiş öneri | Belirli kapsamda dayanaklı sonuç var | Yeni tarih/saat ve değişen bilgiler tekrar değerlendirilir |
| Kullanıcıca düzenlenmiş taslak | Seçim değişti; uyuşmazlık bulunabilir | Kaydetmek uyuşmazlığı temizlemez |
| Sürmekte olan gün | Kullanıcı devam etmek istediğini belirtti | Kalan bölüm güncel bilgiyle değerlendirilir |
| Bitirilmiş/ertelenmiş gün | Kullanıcı günü sonlandırdı veya erteledi | Başarı puanı yok; yeni tarih yeni değerlendirme |
| Silinmiş kayıt | Kullanıcı artık saklamak istemiyor | Aktif paylaşım da kapanır; dış kopyaların sınırı açıklanır |

Bunlar zorunlu kullanıcı rozetleri veya yeni uygunluk sınıfları değildir. Kayıt yaşamı, 02–03'teki uygunluk anlamlarının yerine geçmez.

Yeniden açıldığında “Kayıtlı taslak” ile “bugün için yeniden değerlendirilmiş öneri” ayrılır. Eski yerleri otomatik değiştirmek yerine değişen bilgi ve önerilen fark gösterilir. Kullanıcı “aynı fikri başka gün kullan” diyebilir; geçmiş ziyaret kaydı yeni güne taşınmaz.

Silme, çoğaltma, ad değiştirme ve yeniden açma mevcut karar alanından yapılır. Yanlışlıkla silmeye geri alma yolu bulunur. Geri alma eski kapanma bilgisini veya geçersizleşmiş paylaşımı otomatik diriltmez; paylaşım yeniden açılacaksa açık seçim gerekir.

## 16. Gezeceğim Yerler ile ilişkisi nedir?

Bu belgede önerilen anlam: **Gezeceğim Yerler, daha sonra değerlendirmek üzere tutulan yer niyetleridir; Akıllı Rota belirli bir güne ilişkin karardır.** Listenin adı ziyaret taahhüdü değildir.

| Eylem | Gezeceğim Yerler etkisi | Rota etkisi |
|---|---|---|
| Bir yeri kaydet | Sonra bakılacak niyet oluşur | Otomatik rota oluşmaz |
| Listeden birkaç yer seç | Liste korunur | Birlikte değerlendirme başlar; seçilenler otomatik zorunlu olmaz |
| Bir yeri rotaya ekle | Otomatik liste kaydı gerekmez; ayrı seçim sunulabilir | Günün bir adayı/durağı olur |
| Rotadan çıkar | Listeden silinmez | İlgili günün dizisinden çıkar |
| Listeden sil | Kişisel niyet kaldırılır | Mevcut rotadan habersiz silinmez |
| “Buradaydım” de | İstenirse ayrıca ziyaret edildi olarak işaretlenebilir | Bu günün geçmişi kullanıcı beyanıyla belirlenir |
| Rota kaydet/paylaş | Liste bütünü saklanmış/paylaşılmış sayılmaz | Yalnız seçilmiş kayıt ve paylaşım kapsamı etkilenir |

Liste tarihsiz, şehirler arası ve sırasız olabilir. Aynı yer farklı günlerde yeniden düşünülebilir. Ziyaret edilen yer otomatik silinmez veya “tamamlanması gereken” sayaç yaratmaz. Listede çok bekleyen yer hakkında hatırlatma baskısı kurulmaz.

Listeye alınmış olmak, motorun uygunluk ölçütüne bonus sağlamaz. Açık “bu yer mutlaka olsun” seçimi ise günün koşuludur; yine ziyaret edilebilirliği kanıtlamaz. Kapanmış yerin niyeti korunabilir, güncel engel yanında görünür; gizlice benzeriyle değiştirilmez.

## 17. Ücretsiz kullanıcı ne yapabilir?

Ücretsiz kullanıcı, ürünün temel sözünü baştan sona karşılayan bir gün oluşturabilmelidir:

- Beş giriş yoluyla başlamak; hesap ve konum izni olmadan karar desteği almak.
- Amaç, bütçe, süre, erişim ve grup koşullarını belirtmek.
- Gerekçeyi, ödünü, bilinmeyeni ve anlamlı alternatif farkını görmek.
- Yer eklemek/çıkarmak; sıra, kalış, mola ve sınırları değiştirmek; geri almak.
- Temel yeniden değerlendirme, yeni engel açıklaması ve günü erken bitirme.
- Kişisel taslağı kaydetmek, yeniden açmak, çoğaltmak, silmek ve Gezeceğim Yerler ile çalışmak.
- Temel link, WhatsApp metni, Story görseli ve QR paylaşımını hazırlamak; erişimi kapatmak.
- Paylaşılan rotayı hesap açmadan okumak ve kendi bağlamıyla değerlendirmek.
- Bilgi hatasını bildirmek; Bir İz katkısını atlamak veya vermek.

Erişim koşulunun denetlenmesi, bütçe üst sınırı, önemli belirsizlik, kritik güncelleme, silme ve paylaşımı kapatma hiçbir zaman ücretli güvenlik katmanı olamaz. Aynı bağlam ve dayanak için Premium daha doğru, ücretsiz daha gevşek karar üretmez.

Bu aşamada ücret, sayısal rota kotası ve kullanım limiti uydurulmaz. İleride sürdürülebilir kullanım sınırı gerekirse oluşturmadan önce açık olur; mevcut günün okunması, düzenlenmesi ve kritik düzeltmesi yarıda ödeme istemine dönüşmez. Ticari karar ayrıca doğrulanmalıdır.

## 18. Premium özellikler neler olabilir?

Premium, **daha doğru öneri satın almak** değil, tekrarlanan düzenleme ve birlikte çalışma yükünü azaltmak üzerinden değerlendirilir.

| Olası özellik | Kullanıcı değeri | Felsefeyle uyum ve sınır |
|---|---|---|
| İsteğe bağlı cihazlar arası devam | Aynı taslağı yeniden kurmaz | Veri kontrolü ve temel hesapsız kullanım korunur |
| Kullanıcının seçtiği gün şablonları | Tekrarlanan sınırları tekrar yazmaz | Bugünkü ihtiyaç üstün; gizli profil yok |
| Birkaç senaryoyu yan yana değerlendirme | “Yağmur olursa / daha geç çıkarsak” karar yükünü azaltır | Ücretsiz kullanıcı tek değişikliği yapıp temel yeniden değerlendirme alabilir |
| Davetli ortak öneri toplama | Gruptaki tercih farkını ayrı mesajlardan birleştirmez | Çoğunluk zorunlu koşulu ezemez; alıcı okumak için ödeme yapmaz |
| Geniş düzenleme geçmişi | Önceki kararların neden değiştiğini hatırlar | Temel geri alma ücretsiz; eski bilgi yeni garanti olmaz |
| Paylaşım görünümünü kişiselleştirme | Farklı sunum tercihini karşılar | Kritik sınır, atıf ve güncellik bilgisi tasarımdan çıkarılamaz |

Bu adayların hiçbiri gelir vaadi veya otomatik yayın kapsamı değildir. Ayrı ücret planı/profil sayfası için 01'in değiştirilmesi gerekiyorsa bunun kararı ayrıca verilir. Öncelik kullanıcı araştırmasında tekrar eden çabanın gösterilmesidir.

İlk ticari aday olarak cihazlar arası devam ve açıkça kaydedilen şablonlar değerlendirilebilir. Ortak çalışma, yetki ve grup gizliliği nedeniyle daha sonra sınanır. Sadece güzel görünüm için bilgi kalitesini ayırmak veya az bütçeli kullanıcıyı eksik günle bırakmak kabul edilmez.

Premium bittiğinde mevcut kayıtlar okunabilir, dışa paylaşılabilir ve silinebilir kalır. Temel değişiklik ve kritik yeniden değerlendirme sürer; ileri kolaylıklar yeni kullanımda durabilir. Bir grubun sahibinin aboneliği bitti diye grup elindeki gün bilgisinden mahrum bırakılmaz.

## 19. Paylaşım sistemi nasıl çalışmalı?

Paylaşımın amacı “bu kararı birlikte anlayalım”dır. Beğeni, takipçi, viral rota, kamuya açık profil ve genel sıralama üretmez.

Varsayılan rota özeldir. Kullanıcı paylaşımı başlatır; paylaşılacak içeriğin önizlemesini görür ve kendisi gönderir/yayınlar. “Paylaş” eylemi rehbere erişim veya bütün arkadaşlara mesaj yetkisi vermez.

Varsayılan içerik: nötr rota başlığı, şehir, kullanıcının paylaşmayı seçtiği duraklar, amaç/rolün paylaşılabilir anlatımı, süre kapsamı, önemli koşullar, bilgi sınırları ve ilgili kayıt tarihi. Tam ev/otel başlangıcı, gerçek zamanlı konum, grup üyeleri, sağlık gerekçesi, özel not, kişisel bütçe ve rezervasyon ayrıntıları varsayılan dışarıda kalır. Başlık da hassas bilgi açısından önizlenir.

Bir erişim koşulunu özel kimlik açıklamadan taşımak mümkündür: “Bu geçişin basamaksız olduğu doğrulanmadı.” Gizlilik için kritik koşul metinden çıkarılacaksa onu gerektiren olumlu uygunluk iddiası da çıkarılır. Paylaşılan içerik daha genel bir taslak olabilir; gizleme, doğrulanmış rota görüntüsü yaratamaz.

### Paylaşımın üç ayrı hali

**Özel çalışma kopyası:** Sahibinin bütün kararlarının bulunduğu taslak. Paylaşım değişikliği bunu kendiliğinden herkese açmaz.

**Paylaşılan görünüm:** Sahibinin açıkça paylaştığı son seçim. Varsayılan salt okunurdur. Sahibinin her özel düzenlemesi otomatik yayına gitmez; “paylaşılan sürümü güncelle” ile yeni seçim yayımlanır. İki sürüm farklıysa sahibi bunu görür.

**Alıcının kopyası:** “Kendi günüm için değerlendir” ile oluşan bağımsız taslak. Kopyalamak orijinali değiştirmez; eski sahibin özel tercihleri ve zorunlu koşulları alıcının kişiliği sayılmaz.

Bilgi düzeltmesi ile sahibin plan değişikliği ayrılır. Paylaşılan seçim aynı kalsa bile doğrulanmış kapanma veya geri çekilmiş iddia açık linkte eski olumlu güvence olarak sürmez. “Planın seçimi değişmedi; ikinci yerin ziyaret bilgisi değişti” denebilir. Uygun yeni yer seçmek ise sahibin/alıcı kopyasının kararıdır.

### Erişim ve kontrol

Linki bilenlerin açabildiği paylaşım varsayılanı açıkça anlatılır; “yalnız arkadaşların görebilir” denmez. Böyle bir link yeniden iletilebilir. İsteğe bağlı süre sonu ve istediği an kapatma temel kontroldür. Kapatma Şamandıra'daki yeni açılışları engeller; indirilmiş görseli, kopyalanmış metni veya dış platform önizlemesini geri silemez.

Hesapsız paylaşımda yönetme/kapatma erişimini kaybetme sınırı baştan açıklanır. Yönetim erişimi alıcının salt okuma linkinden ayrıdır; bunu kaybeden kişiye kesin geri alma sözü verilmez. Mevcut destek yolu bulunur.

Davetli ortak çalışma ileride açılırsa okuma, öneri verme ve düzenleme yetkileri ayrı olur. Varsayılan alıcı düzenleyemez. Öneri doğrudan plana uygulanmaz; sorumlu kişi değişikliği kabul eder. Başkasının zorunlu koşulunu kaldırmak o kişinin açık kararını gerektirir. Ortak zorunlu koşulun sahibinin kimliği gereksiz yere açıklanmaz. Çatışan düzenlemeler sessizce birbirini ezmez; son ortak seçim açıkça belirlenir.

## 20. Instagram Story, WhatsApp, link ve QR nasıl davranmalı?

Aşağıdakiler Şamandıra'nın çıktı davranışıdır; dış platformların güncel paylaşım yetenekleri, otomatik yayın izni veya belirli dosya ölçüsü hakkında iddia değildir. Doğrudan aktarım mümkün değilse görseli kaydetme veya metin/linki kopyalama yolu sunulur.

| Kanal | Çıktının işi | İçerik ve sınır | Alıcının devamı |
|---|---|---|---|
| Instagram Story | Gün fikrini kısa görselle anlatmak | Şehir, paylaşılabilir başlık, durak rolleri, kapsamlı süre, gerekli önemli uyarı ve oluşturulma/değerlendirme bağlamı. Canlı navigasyon gibi çizim yok | Varsa eklenen link veya QR ile güncel paylaşılan görünüme geçer; uygulama/hesap zorunlu değil |
| WhatsApp | Birlikte kararı konuşabilmek | Okunabilir kısa metin, sıralı duraklar, süre/dönüş kapsamı, önemli koşul ve link. Kişisel başlangıç veya sağlık notu yok | Linki açabilir ya da yalnız metinden temel kararı anlayabilir |
| Link | Kararın ayrıntısını ve güncel bilgi sınırını açmak | Salt okunur, indekslenmesi amaçlanmayan paylaşım. Gizli bilgiyi önizleme başlığına koymaz | Mevcut Keşfet bağlamında okur; kendi koşullarıyla yeni taslak oluşturur |
| QR | Aynı linke basılı/görsel erişim sağlamak | Özel not veya ham konum yüklemez; yanında açıklama ve okunabilir alternatif bağlantı bulunur | Tarama yalnız açar; ziyaret, onay veya düzenleme sayılmaz |

### Story'nin davranışı

Estetik uğruna bütün durakları küçük ve okunamaz yazmak yerine özet kapsam seçilir. Eksik durak sayısı açıkça belirtilir; özet tam rota gibi gösterilmez. Kritik sınır tek görsele sığmıyorsa daha kısa anlatım, ek görsel veya yalnız “taslak” sunumu kullanılır. “Ayrıntı linkte” sözü mevcut olumlu iddianın kritik eksiğini gizleme izni değildir.

Görsel sabittir: sonradan değişemez ve gelecekteki açıklığı doğrulamaz. “Gün fikri — ziyaret koşullarını yeniden kontrol et” gibi anlamlı tarih/kapsam notu taşır. Kullanıcı görseli Story'ye kendisi yerleştirir; dış uygulamaya geçiş “yayınlandı” diye raporlanmaz.

### WhatsApp'ın davranışı

Metin, görsel olmadan da anlaşılır olmalıdır. Örnek kurmacadır: “Kısa yürüyüş + uzun sohbet. İlk duraktan itibaren yaklaşık iki saat; dönüş dahil değil. İkinci durakta rezervasyon gerekiyor. Güncel taslak: [paylaşım bağlantısı].” Bu metin ancak ilgili tahmin destekleniyorsa kullanılır.

Alıcı ve gönderme eylemi kullanıcıya aittir. Mesajın kopyalanması, taslağın hazırlanması veya dış uygulamanın açılması gönderim/teslim/okundu kanıtı değildir. Mesaj önizlemesi eski kalabilir; güncel ayrıntı linkte yeniden değerlendirilir. Önizleme varsayılan olarak nötr ve az bilgi taşır.

### Linkin davranışı

Açılışta şehri, bu taslağın hangi gün/kapsam için düşünüldüğünü ve güncel değerlendirme durumunu anlatır. Tarih geçmişse bugüne otomatik taşınmaz. “Ben de kullanacağım” seçimi, alıcının tarih, süre, başlangıç ve gerekli koşullarını kurar; kişisel uygunluk yeniden değerlendirilir.

Süresi bitmiş, kapatılmış, silinmiş veya geçici olarak açılamayan paylaşım farklı anlamlarla anlatılır. Kapatılmış linke eski olumlu rota özeti gösterilmez. Linkin açılması sahibine alıcının konumunu veya kimliğini otomatik bildirmez.

### QR'ın davranışı

QR ile link aynı erişim ve sona erme kurallarını taşır. QR çıktısı alındıktan sonra paylaşım kapatılırsa tarama kapatılmış duruma ulaşır. QR'ın görsel varlığı bilgi güncelliğini veya yayıncının resmî yetkisini kanıtlamaz.

Telefonundaki görseli aynı telefonla tarayamayan kullanıcı için tıklanabilir/kopyalanabilir yol korunur. Basılı kullanımda okunabilir açıklama ve bağlantı alternatifi vardır. Erişim kodu, alıcıya düzenleme yetkisi taşımaz.

## 21. Şamandıra bu rotalardan ne öğrenebilir?

Üç ayrı öğrenme alanı korunur: kişisel karar desteği, yer/geçiş bilgisi ve ürün davranışının kalitesi. Birindeki işaret diğerinde otomatik gerçek olmaz.

| İşaret | Öğrenilebilecek | Öğrenilemeyecek |
|---|---|---|
| “Bu gün için daha az yürümek istiyorum” | Bu bağlamın açık önceliği | Kalıcı sağlık veya kişilik profili |
| “Bu tercihi hatırla” | Kullanıcının görebildiği, değiştirebildiği tercih | Diğer grup üyelerinin aynı tercihi |
| Durağı çıkarma | Bu dizide istenmediği; neden söylendiyse o neden | Mekânın kötü veya hiç istenmeyecek olduğu |
| Uzun kalma beyanı | Kullanıcının bildirdiği gerçekleşen kalış | Memnuniyet; diğer ziyaretçiler için olağan süre |
| Yol tarifi, kaydetme veya paylaşma | Niyet/ilgi | Gerçek ziyaret, doluluk veya beğeni |
| “Gittiğimde kapalıydı” | Zaman/yer kapsamıyla bilgi inceleme tetiki | Tek beyanla bütün dönemde kalıcı kapanma |
| Günü erken bitirme | Devam edilmediği | Tasarım başarısızlığı veya yorgunluk nedeni |
| Paylaşım kopyaları | Bir gün fikrine ilgi | Bağımsız ziyaret ve kanıt çoğalması |
| Hiç geri bildirim yok | Sonucun bilinmediği | Sessiz onay veya memnuniyet |

İsteğe bağlı deneyim sorusu “Bugün yapmak istediğine zaman kaldı mı?” olabilir. Bu günün faydasını araştırır; mekân gerçeği üretmez. Belirli yer koşulu için 05'teki Bir İz, örneğin “Oturmak için bekledin mi?” ile ayrı somut gözlem alır. Aynı katkı iki bağımsız kanıt sayılmaz; planlanan saat gerçek ziyaret saati yerine geçmez.

Hatırlanan tercihler görünür, düzeltilebilir, silinebilir ve o gün için kapatılabilir. Grup seçimi hesap sahibinin kalıcı geçmişine yazılmaz. Konum izi, birlikte görülme, hassas kimlik veya gelir çıkarımı yapılmaz. Yeni katkı veya rota kullanımı otomatik model eğitimi/pazarlama izni değildir.

Ürün; nerede fazla soru sorduğunu, hangi geçişleri yanlış değerlendirdiğini, nedenlerin anlaşılıp anlaşılmadığını, benzer önerilerin yük yarattığını ve hangi ihtiyaçlarda gereksiz sustuğunu öğrenebilir. Kendi önerdiği yerleri tekrar seçilmiş görmesi doğruluk kanıtı değildir; gösterim sırası, gösterilmeyen seçenekler ve gönüllü yanıt yanlılığı araştırmada dikkate alınır.

## 22. Asla yapılmayacak şeyler

1. Herkes için en iyi rota veya kusursuz gün ilan etmek.
2. Tek yer ihtiyacını zorunlu çok duraklı geziye büyütmek.
3. Durak sayısı, rota tamamlama veya mesafeyi başarı yarışı yapmak.
4. Zorunlu koşulu başka avantajlarla telafi etmek.
5. Bilinmeyen erişim, ücret veya açıklığı olumlu saymak.
6. Kullanıcının bütçe, bitiş, ulaşım veya coğrafyasını habersiz genişletmek.
7. Kullanıcının amacını, sabitlediği durağı veya reddini gizlice değiştirmek.
8. Mekânlara veya rotaya genel tempo, enerji, güven ve uygunluk puanı vermek.
9. Kuş uçuşu yakınlıktan yürünebilirlik veya erişilebilirlik üretmek.
10. Ortalama sürelerle yetişme garantisi vermek.
11. Aynı olaya bağlı iki yedeği bağımsız çözüm göstermek.
12. Rezervasyon gerekmesini rezervasyon yapılmış gibi anlatmak.
13. Kullanıcı adına izinsiz harcama, rezervasyon, gönderim veya yayın yapmak.
14. Ödeme, ortaklık veya popülerliği uygunluk avantajına çevirmek.
15. Kritik bilgi, temel düzeltme veya kullanıcı kontrolünü Premium'a kilitlemek.
16. Ham yorum, yorumcu, yıldız, konu puanı veya yeniden yazılmış yorum yayımlamak.
17. Özel rota, başlangıç, grup koşulu veya notları otomatik paylaşmak.
18. Paylaşım açılmasını ziyaret ya da kopyaları bağımsız kanıt saymak.
19. Sabit görselin güncellendiğini veya dış kopyaların uzaktan silinebildiğini vaat etmek.
20. Erken bitişi suçluluk, eksik rozet veya ısrarlı hatırlatmayla cezalandırmak.
21. Sürekli takip ve gereksiz kişisel veriyle temel karar hizmetini şartlandırmak.
22. Kullanıcının geçmişinden bugünkü açık isteğin önüne geçen kimlik çıkarmak.
23. Bilinmeyen kapsamı, kesintiyi ve gerçek eşleşme yokluğunu tek “sonuç yok” mesajına çevirmek.
24. Uydurulmuş mekân, bağlantı, saat veya güvenceyle boşluk doldurmak.
25. Kaydetme tarihini yer bilgisinin doğrulama tarihi olarak sunmak.
26. Çok günlük seyahat, sosyal portal veya rezervasyon ürününü bu metinle sessizce kapsam içine almak.

## 23. Ürünü güçlendiren ek fikirler

Aşağıdakiler yeni üst kavram veya yeni sayfa ailesi değildir. Mevcut amaç, tercih, zorunlu koşul ve karar özeti dilinin etkileşim önerileridir. Her biri yararını kanıtlayamazsa daraltılır veya kaldırılır.

| Fikir | Somut davranış | Ürün Felsefesi ile neden çelişmez? | Doğrulama / kaldırma nedeni |
|---|---|---|---|
| “Bugün neye mutlaka zaman kalsın?” | Birden çok amaç çatışınca ana faaliyeti seçtirir | 00 ilke 1–3: karar anını ve açık ihtiyacı belirler | Zaten açık amacı tekrar soruyorsa kaldır |
| “Burada kalabiliriz” | Yeni yere geçmeden mevcut yerde sürdürmenin sonucunu gösterir | 00 ilke 19–20: gerçek hayat faydası; daha çok tüketim hedefi yok | Her durakta gereksiz öneri gürültüsü oluyorsa yalnız istekle göster |
| “Bir durak eksilt” | Çıkarılabilecek tamamlayıcıyı ve kazanılacak alanı gerekçeler | 00 ilke 4, 6: karar yükünü azaltır, nedeni açıklar | Ana amacı/sabitleri aşındırıyorsa öneriyi durdur |
| “Bir kısmını boş bırak” | Kullanıcının belirlediği süreyi yeni faaliyetlerle doldurmaz | 00 §5 özerklik: zaman kullanıcıya ait | Esneklik, gecikme garantisi sanılıyorsa dilini değiştir |
| “Aynı amacı başka koşulda sürdür” | Yağmur, geç çıkış veya yorgunlukta aynı rol için seçenek sunar | 00 ilke 9, 12: değişken koşulu ve zorunlu sınırı korur | Aynı ortak riski taşıyorsa alternatif deme |
| “Ne değişti?” | Düzenlemenin süre, maliyet, amaç ve bilinmeyene etkisini kısa verir | 00 ilke 6–8: gerekçe ve sınır görünür | Her küçük değişikliği uzun rapora çeviriyorsa sadeleştir |
| “Birlikte uyamadığımız koşul” | Grup çatışmasını kişiyi hedef göstermeden anlatır | 00 ilke 11–12: ortak karar; zorunlu koşul çoğunlukta erimez | Kişisel bilgiyi ifşa ediyorsa kapsamı daralt |
| “Bugün için yeniden bak” | Eski taslağı güncel tarih ve bilgiyle tekrar değerlendirir | 00 ilke 8–9: eski bilgi güncel olgu değildir | Eski taslağı habersiz değiştiriyorsa akışı düzelt |

Özgün değer yeni bir isim koymakta değildir. **Günün ana amacını korurken gereksiz durakları azaltabilmek ve kullanıcıya neyi koruyup neyi bırakabileceğini anlatmakta** birikir. Bu bir rekabet üstünlüğü kanıtı değildir; gerçek karar faydasıyla sınanmalıdır.

## 24. Operasyon nasıl davranmalı?

Bu bölüm teknik sistem tasarımı değil, ürün sorumluluğudur. Bilgi Motoru neyin bilinebildiğini; Karar Motoru yerin bu ihtiyaca uygunluğunu; Akıllı Rota ziyaretlerin ve geçişlerin birlikte anlamını belirler. Rota üretmek yeni yer olgusu uydurma yetkisi değildir.

| Sorumlu | Sahiplendiği karar | Kritik durumda davranış |
|---|---|---|
| Ürün sorumlusu | Amacın korunması, kontrol, kapsam ve ticari sınırlar | Felsefeye aykırı davranışı daraltır; ilgi gördü diye sürdürmez |
| Bilgi kalitesi sorumlusu | İddia yeterliliği, güncellik, çelişki ve ilgili doğrulama | Etkilenen olumlu güvenceyi durdurur; kanıtsız yeni hüküm yayımlamaz |
| Rota deneyimi sorumlusu | Toplam yük, sıra, değişiklik ve gerekçenin tutarlılığı | Bilinen durakları geçersiz toplam halinde önermeyi engeller |
| Destek/inceleme sorumlusu | Somut hata bildirimi ve etkilenen kararın ele alınması | Kullanıcıyı yorum yazmaya zorlamadan ilgili sorunu kabul eder |
| Değerlendirme sorumlusu | Fayda, yanlış olumlu, gereksiz susma ve kapsam ölçümü | Olumlu örnekleri seçerek başarı ilan etmez |

Bir yer kapanır, taşınır veya erişim iddiası geri çekilirse etkilenen yeni öneriler, açık/kayıtlı rota tekrar kullanımları ve link görünümü yeniden değerlendirilir. Tamamlanmış ziyaret yeniden yazılmaz. Dışarı aktarılmış metin/görsele ulaşılamama sınırı korunur; mümkün olmayan geri çekme tamamlandı sayılmaz.

İşletme saat ve koşul bildirir; kullanıcının rotasına doğrudan durak ekleyemez. Editör kendi favorisini dayatamaz. Ticari ilişki bilgi incelemesinde ayrıcalık veya daha hızlı uygunluk sağlamaz.

Kesintide kullanıcı seçimi görünür kalır. Doğal dil anlama çalışmıyorsa açık yer/ihtiyaç seçimleri kullanılabilir. Güncel geçerlilik denetlenemiyorsa etkilenen olumlu uygunluk durur. Kaydedilmiş tarihli temel bilgi okunabilir; yeni canlı durum veya güncel yapılabilirlik iddia edilmez. Yeniden bağlantıda kullanıcı düzenlemeleri korunarak bilgi yenilenir.

Karmaşık dizi makul bekleyişte kurulamıyorsa sonu gelmeyen üretim gösterilmez; desteklenen daha sade seçenek veya somut sınır verilir. Keyfî bir süre eşiği bu belgede icat edilmez. Kullanıcı beklemeyi bırakabilir; taslağını kaybetmez.

## 25. Uçtan uca kurmaca gün örneği

İstek: “İki saatimiz var. Kısa yürüyüşten sonra uzun konuşalım. Başlangıca dönelim; toplam yürüyüş 35 dakikayı geçmesin.”

Amaçlar kısa yürüyüş ve uzun sohbettir; ikincisi açık önceliklidir. İki saat, başlangıca dönüş ve en fazla 35 dakika yürüyüş zorunlu sınırdır. Şehir, başlangıç, ziyaret günü/saati ve gerekli yer/geçiş bilgilerinin yeterince bilindiği varsayılmıştır. Bütçe belirtilmediği için bütçeye uyum sözü yoktur.

| Parça | Amaç / yük | Dayanaklı olduğu varsayılan süre |
|---|---|---|
| Başlangıçtan kıyıya | Yürüyüşe erişim | 5 dakika |
| Kıyıda yürüyüş | Açık ilk amaç | 15 dakika |
| Oturma alanına geçiş | Sohbete bağlantı | 5 dakika |
| Oturarak sohbet | Ana amaç | 55–65 dakika |
| Başlangıca dönüş | Bitiş koşulu | 5–10 dakika |
| Yerleşme ve küçük gecikme payı | İlgili koşullar için desteklendiği varsayılmış yük | 10–15 dakika |

Toplam 95–115 dakika; yürüyüş 30–35 dakikadır. Aralıklar garanti değildir. Bu örnekte gerekli ortak risklerin ayrıca incelendiği varsayılır; gerçek kullanımda pay için dayanak yoksa rakam uydurulmaz.

Öneri: “Kısa yürüyüşten sonra sohbet için daha uzun bir bölüm bıraktık. Dönüş dahil yaklaşık 95–115 dakika; toplam yürüyüş 30–35 dakika. Ek durak önermedik, çünkü sohbet süresini azaltıyor.”

Kullanıcı “yürüyüşü sona al” derse yeni varış saatlerinde oturma koşulu tekrar değerlendirilir. “Burada yarım saat fazla kalalım” derse bitişe etkisi gösterilir; dönüş veya toplam süre sınırı kendiliğinden silinmez.

Kullanıcı 25 dakika geç çıkıp bitişi değiştiremezse kalan süre 95 dakikadır. Önceki aralığın üst tarafı artık sığmaz; “yine de yetişirsin” denmez. Yürüyüşü kısaltmak, bilinen daha yakın oturma seçeneği veya tek yerde sohbet açıklanabilir alternatiflerdir. Yürüyüş açık amaç olduğu için kaldırılması kullanıcı kararıdır.

Oturma alanı yalnız açık terastaysa yağmurda sohbetin korunacağı söylenmez. Yedek de açık terasa bağlıysa gerçek hava alternatifi değildir. Uygun kapalı seçenek bilinmiyorsa bu sınır açık kalır.

Kullanıcı oturma yerinde kalmayı seçip kalan plandan vazgeçebilir. Gezi eksik sayılmaz. Sonradan “konuşmaya zaman kaldı” demesi günün faydasına işarettir; bütün yer koşullarını doğrulayan kanıt değildir.

## 26. Yayın öncesi doğrulama ve başarı ölçüsü

Bu tasarım uygulama veya saha doğrulaması yapıldığını iddia etmez. İlk kapsam, yeterli yer ve bağlantı bilgisinin bulunduğu sınırlı coğrafya/amaçlarda sınanır. Tek yer kararının doğruluğu kurulmadan karmaşık günlere genişlenmez.

| Ölçü | Ne aranır? | Hangi yanlış teşvikten kaçınılır? |
|---|---|---|
| Karar çabası | Anlamlı sonuca varmak için soru, düzenleme ve tekrar düşünme yükü | Üründe geçirilen süreyi artırmak |
| Amaç karşılığı | Gönüllü ve gerçekten yaşanmış deneyimde ana amaca zaman kalması | Bütün durakların tamamlanmasını başarı saymak |
| Koşul doğruluğu | Karşılandı denilen zorunlu sınırların bağımsız incelemesi | Çok sayıda doğru adresle kritik hatayı gizlemek |
| Açıklamayı anlama | Kullanıcı neden, ödün ve bilinmeyeni doğru anlatabiliyor mu? | Metni beğenmesini yeterli saymak |
| Süre ve maliyet kapsamı | Tahminin hangi parçaları içerdiği ve gerçekleşmeyle farkı | Dönüş/bekleme hariç toplamı tam süre diye vermek |
| Değişiklik yükü | Bir yer/saat değişince kaç eski kararın yeniden kurulması gerekiyor? | Her düzenlemeyi yeni öneri sayarak kullanım şişirmek |
| Gereksiz susma | Yeterli dayanak varken kaç faydalı karar kaçırılıyor? | Hiç önermeyerek hatasız görünmek |
| Paylaşım bütünlüğü | Alıcı hangi bağlamı, güncelliği ve sınırı anlıyor? | Gönderim ve açılmayı gerçek fayda sanmak |
| Kapsam | Amaç, şehir, ulaşım ve ihtiyaçlara göre bilgi açıkları | Az veriyi yer kalitesi eksisi saymak |
| Düzeltme tamamlanması | Eski olumlu hükmün kontrol edilebilir bütün kullanımlardan kalkması | Yalnız kaynak güncellemesini tamamlandı saymak |

Sayısal başarı ve işletim eşikleri araştırma planında yayından önce belirlenir; bu metin ölçülmüş oran uydurmaz. Yanıt vermeyenler mutlu veya mutsuz sayılmaz. Gönüllü geribildirimin yanlılığı bağımsız inceleme ve kullanım gözlemiyle birlikte ele alınır.

### Davranış kabul senaryoları

1. Konum izni verilmediğinde elle başlangıç seçilerek devam edilebilir.
2. Tarih bilinmiyorsa taslak kaydedilebilir; bugünkü açıklık sözü verilmez.
3. İlk veya dönüş yolu bilinmiyorsa kapıdan kapıya toplam iddia edilmez.
4. İki durak tek tek açık ama ikinciye son girişten sonra varılıyorsa dizi önerilmez.
5. Bütçenin üst tahmini sınırı aşıyorsa uyum verilmez.
6. Kullanılan geçişte zorunlu erişim bilinmiyorsa diğer durakların bilgisi bunu telafi etmez.
7. Sıra değişince saat, geçiş ve amaç birlikte yeniden değerlendirilir.
8. Durak silinince boşluk yeni durakla otomatik doldurulmaz.
9. Kullanıcı seçilmiş uyumsuz yeri taslakta tutabilir; olumlu uygunluk etiketi oluşmaz.
10. Keşfet'te şehir değiştirmek mevcut rotayı bozmaz.
11. Yeni şehir taslağı eski rezervasyonu veya sabit yeri taşınmış saymaz.
12. Kaydedilmiş eski rota yeniden açılınca güncel koşullar ayrı değerlendirilir.
13. Aynı yağışa bağlı yedekler bağımsız çözüm diye sunulmaz.
14. Ücretsiz kullanıcı aynı zorunlu kontrolleri ve kritik değişikliği görür.
15. Paylaşılan rota sahibinin özel düzenlemesi açık paylaşım güncellemesi olmadan yayımlanmaz.
16. Yeni kapanma bilgisi, paylaşılan seçimi değiştirmeden eski olumlu hükmü durdurur.
17. Story'de kritik sınır sığmıyorsa olumlu anlatı daraltılır.
18. Link kapatılınca QR yeni açılışta aynı kapatılmış duruma gelir.
19. Alıcı kopyası sahibinin özel koşullarını kendi tercihi olarak öğrenmez.
20. Kullanıcı erken bitirince tamamlama baskısı ve otomatik memnuniyetsizlik kaydı oluşmaz.
21. Grup tercihi bir kişinin zorunlu erişim koşulunu çoğunlukla kaldıramaz.
22. Bağlantı kesilince tarihli kayıt okunabilir; yeni güncel yapılabilirlik üretilmez.
23. Katkıdaki gerçek ziyaret saati bilinmiyorsa planlanan saat yerine konmaz.
24. Geri alma kullanıcı seçimini geri getirir; yeni kapanmayı veya kapatılmış paylaşımı geri getirmez.

Kritik yanlış olumlu koşul, sistematik amaç kaybı, özel bilgi ifşası veya sınırları taşımayan paylaşım saptanırsa ilgili yetenek/kapsam daraltılır. Yeniden açılışta düzeltilmiş davranış ve bağımsız doğrulama aranır. Fayda sağlamayan bir ek fikir, ilgi çekse bile kaldırılabilir.

## 27. Öz eleştiri — 40 itiraz ve nihai düzeltme

Bu riskler yalnız kötü uygulama ihtimali değildir; bazıları seçilen yaklaşımın doğrudan maliyetidir. Aşağıdaki kararlar nihai metne işlenmiştir. Araştırma gerektiren kalan belirsizlikler kapanmış sayılmaz.

| No | Kendi önerime itiraz | Somut risk / alternatif | Nihai düzeltme ve sınama |
|---|---|---|---|
| 1 | “Doğru gün” paternalist bir vaat olabilir | Sistem kullanıcının nasıl yaşaması gerektiğine karar verir | §1: doğruluğu kullanıcının açık amacı tanımlar; memnuniyet garantisi yok |
| 2 | Yeni ürün adı sıradan planlayıcıyı gizleyebilir | Uzun ajanda ve durak doldurma geri gelir | §1–2: tek yer, boş zaman ve erken bitiş eşdeğer geçerli sonuçlar |
| 3 | Ana amaç seçimi gereksiz soru olabilir | İstekte zaten açık olan şey yeniden sorulur | §4: yalnız kararı değiştiren belirsizlik sorulur; tekrar yükü ölçülür |
| 4 | Boş başlangıç kullanıcıyı yalnız bırakabilir | Form istememek hiçbir yardım sunmamaya dönüşür | §3: yazma, yer ve ihtiyaç girişleri görünür; otomatik amaç atama yok |
| 5 | Doğal dil yanlış zorunlu koşul çıkarabilir | “Ucuz” kesin bütçe olur veya “şart” silinir | §4: anlaşılan koşullar görünür ve düzeltilebilir; belirleyici belirsizlik netleştirilir |
| 6 | Seçilmiş yer ile sabit yer farkı anlaşılmayabilir | Kullanıcı motorun seçimini sildiğini düşünür | §3, §6: aday seçimi ve “mutlaka” ayrı; sığmayan seçilmişler kaybolmaz |
| 7 | Çok sayıda sabitleme öğrenme yükü yaratır | Kullanıcı her durağa üç kilit koymak zorunda kalır | §6: yalnız ihtiyaç halinde yer/saat/sıra ayrımı; varsayılan zorunlu kilit yok |
| 8 | Sabitler planı imkânsızlaştırabilir | Motor sürekli başarısız görünür | §6: uyuşmazlık açıklanır, kullanıcı taslağı saklayabilir; otomatik gevşetme yok |
| 9 | Ana amaç ölçülemez kadar soyut kalabilir | “Keyif” adına rastgele seçimler yapılır | §4–5: yalnız somut karşılığı ve dayanağı olan uygunluk; diğer kısmı bilinmiyor |
| 10 | “Tempo yok” kullanıcı dilini kurutabilir | Rahat gün isteyen kişi teknik sorularla karşılaşır | §5: günlük dil korunur, sadece kararı değiştiren somut ayrım sorulur |
| 11 | Çok temkinli süreler günün değerini azaltabilir | Gereksiz geniş aralıklar bütün dizileri eler | §5, §26: gerçek aralık ve gereksiz susma birlikte sınanır; keyfî pay yok |
| 12 | Küçük gecikmeler birlikte büyük hata yaratabilir | Bağımsız sanılan süreler aynı trafikle uzar | §5: ortak risk değerlendirmesi; yalnız iyi ihtimallerle yetişme yok |
| 13 | Serbest zaman ile gecikme payı karışabilir | Kullanıcı boş zamanı garanti rezerv sanır | §5: kullanıcı tercihi ve dayanaklı tahmin ayrı anlatılır |
| 14 | Eksik fiyat bütçe kararı desteğini kısıtlar | Kullanıcı uygun sonuç bulamaz | §4–5: kapsamlı bilinen giderler; veri açığı bütçe uyumu diye örtülmez |
| 15 | Yer erişimi geçiş erişimine kefil olabilir | Basamaksız iki yer arasında merdivenli yol vardır | §5, §9: zincirin gereken bütün parçaları ayrı değerlendirilir |
| 16 | Çok alternatif yeniden karar yorgunluğu yaratır | Kullanıcı üç ayrı günü baştan karşılaştırır | §2: bir ana öneri; yalnız anlamlı fark varsa ek seçenek |
| 17 | Az alternatif kullanıcıyı dar alana kapatabilir | Motorun ilk seçimine bağımlılık doğar | §8–12: neden, değiştirme, ret ve açık alternatif isteme yolları korunur |
| 18 | Düzenleme her seferinde bütün günü oynatabilir | Kullanıcı yaptığı işi kaybeder | §7, §10: istenen değişiklikle sınırlı etki; fark özeti ve geri alma |
| 19 | Uyarılı taslak örtük onay sanılabilir | Kullanıcı uyumsuz rotayı yapılabilir kabul eder | §9, §15: kayıt yaşamı ve uygunluk ayrılır; olumlu tam rota hükmü verilmez |
| 20 | Sürekli yeniden değerlendirme dikkat tüketebilir | Gezi bildirim yönetimine dönüşür | §13: anlamlı değişiklik ve izinli etkin karar sınırı |
| 21 | Şehir kopyalama eski koşulları yanlış taşıyabilir | Başlangıç, rezervasyon veya tarih yanlış kalır | §14: yeni taslak; yerel bağlam taşınmış sayılmaz, eski kayıt korunur |
| 22 | Şehirler arası sınır bazı günlük gezileri dışlar | Yakın komşu şehir kullanıcıya doğal gelebilir | §14: bu sürümde sınır açık; fayda ve bağlantı kanıtıyla ayrı kapsam değerlendirmesi gerekir |
| 23 | Gezeceğim Yerler ikinci planlayıcıya dönüşebilir | Liste tamamlama baskısı ve ayrı portal oluşur | §16: tarihsiz niyet; rota ile bağımsız değişiklik; yeni sayfa ailesi yok |
| 24 | Hesapsız kayıt kaybolabilir | Cihaz verisi temizlendiğinde emek gider | §15: sınır kayıt anında açık; hesap ilk kararın zorunlu adımı yapılmaz |
| 25 | Kayıtlı rota güvenin dondurulması sanılabilir | Aylar önceki fiyat/açıklık güncel kabul edilir | §15: yeniden kullanım yeni değerlendirme; kaydetme doğrulama değil |
| 26 | Paylaşılacak amaç özel bilgi verebilir | Sağlık/ilişki çağrışımı başlıktan sızar | §19: başlık dahil önizleme; varsayılan nötr metin ve asgari içerik |
| 27 | Gizlilik için uyarı silmek yanıltabilir | Erişim eksikliği gizlenirken olumlu rota kalır | §19: koşul kişisiz anlatılır; gerekirse olumlu hüküm de daraltılır |
| 28 | Salt okunur link güvenli özel grup sanılabilir | Link başkasına iletilir | §19: linki bilenlerin erişimi açıkça anlatılır; davetli erişim ayrı yetenek |
| 29 | Hesapsız paylaşım yönetimi kaybolabilir | Sahip linki kapatamaz | §19: yönetim erişimi sınırı baştan açıklanır; kesin geri çekme vaadi yok |
| 30 | Canlı link ile sabit görsel çelişebilir | Alıcı eski Story'ye göre yola çıkar | §20: sabit çıktı tarihli taslaktır; güncel bilgi linkte; uzaktan silme vaadi yok |
| 31 | Paylaşılan sürümü güncellemek zahmetli olabilir | Sahip değişikliği yayınlamayı unutur | §19: özel/paylaşılan farkı görünür; yalnız bilgi düzeltmeleri kendiliğinden yansır |
| 32 | QR erişilebilir tek yol olmayabilir | Aynı telefonla tarama veya görme güçlüğü | §20: metin ve tıklanabilir/kopyalanabilir bağlantı alternatifi |
| 33 | Ortak çalışma grup baskısı yaratabilir | Çoğunluk bir kişinin koşulunu kaldırır | §19: zorunlu koşul sahibi karar verir; ortak çözüm yoksa uyuşmazlık açıklanır |
| 34 | Premium ücretsiz deneyimi kasıtlı kötüleştirebilir | Kritik düzeltme veya temel alternatif ücretli olur | §17–18: aynı doğruluk ve kontrol; ticari ayrım yalnız ilave kolaylık |
| 35 | Premium adayları yeterince değerli olmayabilir | Kullanıcı ödemez; temel ürün gereksiz genişler | §18: gelir garantisi yok; tekrarlanan gerçek çaba kanıtlanmadan satış kapsamı açılmaz |
| 36 | Erken bitişi başarı saymak hata gizleyebilir | Kötü deneyimden vazgeçiş olumlu raporlanır | §13, §21: erken bitiş nötr; neden isteğe bağlı öğrenilir, otomatik başarı yok |
| 37 | Katkı soruları geziyi kesintiye uğratabilir | Her durakta gözlem borcu yaratılır | §21: ayrı, isteğe bağlı Bir İz; atlama/kapama ve sorusuz çıkış |
| 38 | Öğrenme kendi önerilerini doğrulayabilir | Gösterilen yer seçilir, sonra hep üstün önerilir | §21, §26: niyet/ziyaret/kanıt ayrımı; bağımsız inceleme ve kapsam araştırması |
| 39 | Operasyon maliyeti kapsamı boğabilir | Çok şehirde eski bağlantı ve koşullar birikir | §24–26: az coğrafya/amaçla aç; kritik kontrolü azaltmak yerine kapsamı daralt |
| 40 | Tasarım ayrıntısı yeni bir ürün bürokrasisi yaratabilir | Her küçük karar için uzun kontrol akışı olur | §4, §10, §23: kullanıcı yalnız kararı değiştiren bilgi görür; faydasız etkileşim kaldırılır |

## 28. Öz eleştiri sonrası nihai sürüm — savunulan ürün kararı

**Akıllı Rota, mevcut Keşfet ve yer bağlamı içinde çalışan; kullanıcının bugünkü amacını, telafi edilemeyen sınırlarını ve değiştirilebilir ziyaret dizisini birlikte ele alan karar yeteneğidir.**

Nihai sürümün davranışı şöyledir:

1. Kullanıcı doğal dil, birkaç yer, ihtiyaç, koleksiyon veya boş taslakla başlar. İlk karar için hesap ve konum izni zorunlu değildir.
2. Motor yalnız sonucu değiştiren soruyu sorar. Eksik bağlamı doldurmuş gibi yapmaz; taslak ile yapılabilirlik iddiasını ayırır.
3. Zorunlu koşullar, ana amaç, toplam yapılabilirlik, tamamlayıcılık ve gereksiz yük sırası korunur. Tempo veya genel rota puanı üretilmez.
4. Her durağın işi vardır; tek yer ve boş bırakılan zaman geçerlidir. Ana amaca katkı vermeyen durak eklenmez.
5. Kullanıcı yer, sıra, saat, kalış, amaç ve sınırları değiştirebilir. Motor etkisini açıklar; ek bir ödünü kullanıcı adına kabul etmez.
6. Öneri nedenini, önemli ödününü ve gerekli bilinmeyenini birlikte taşır. Bilinmeyen zorunlu koşul, uyarı eklenerek karşılanmış sayılmaz.
7. Gün değişince kalan bölüm değerlendirilir; tamamlanmış ziyaretler ve kullanıcı kararları korunur. Erken bitiş nötr ve meşru sonuçtur.
8. Rota kaydedilir; Gezeceğim Yerler'den farklı bir günlük karar olarak yaşar. Yeniden kullanımda bilgi ve bağlam yeniden değerlendirilir.
9. Ücretsiz kullanım temel sözü bütünüyle karşılar. Premium yalnız doğrulanacak ilave kolaylıklar sunabilir; doğruluk, kritik bilgi ve kontrol satılmaz.
10. Paylaşım kullanıcının açık seçimidir. Özel kopya, paylaşılan seçim ve alıcının kendi taslağı ayrıdır. Bütün kanallarda bilgi sınırı korunur.
11. Rotalar kullanıcı gözetimine değil; daha iyi soru, daha doğru toplam yük, daha anlaşılır gerekçe ve daha iyi bilgi düzeltmesine katkı sağlar.
12. İlk yayın dar ve doğrulanabilir kapsamda başlar. Amaç kaybı, kritik yanlış olumlu, özel bilgi ifşası veya faydasız karmaşıklıkta yetenek daraltılır.

Nihai seçim, bütün günü tamamlatan program yerine **kullanıcının önem verdiği şeye zaman ayırmasını ve gün değiştiğinde daha az uğraşarak karar vermesini** destekler. Belgenin başarısı kapsamının büyüklüğüyle değil, gerçek bir günde bu yükü azaltıp azaltmadığıyla değerlendirilecektir.

## Bu dokümanın bağlı olduğu belgeler

- [00 Ürün Felsefesi](./00-urun-felsefesi.md)
- [01 Bilgi Mimarisi](./01-bilgi-mimarisi.md)
- [02 Product Language](./02-product-language.md)
- [03 Karar Motoru](./03-karar-motoru.md)
- [04 Sistem Mimarisi](./04-sistem-mimarisi.md)
- [05 AI Bilgi Motoru](../04-ai/05-ai-bilgi-motoru.md)

## Bu dokümanın etkilediği belgeler

Aşağıdaki çalışmalar **planlanandır; bu görevde oluşturulmuş değildir**:

- 02-ux altında Akıllı Rota oluşturma, düzenleme, paylaşım ve geri alma davranışları.
- 01-research altında günün amacı, karar yükü, belirsizliği anlama ve ücretsiz/Premium değer araştırması.
- 03-design altında kısa anlatım, erişilebilir düzenleme ve paylaşımda anlam koruma ilkeleri.
- 08-admin altında rota etkileyen bilgi düzeltmesi, inceleme ve kullanıcıya açıklama politikası.
- 09-business altında Premium fayda, temel ücretsiz haklar ve ticari bağımsızlık değerlendirmesi.
- 04-ai altında planlanan Kanıt, Güncellik ve Yayın Politikası: durak ve geçiş kararlarının gerekli bilgi kapsamı.

Bu ilişkiler kabul edilmiş 00–05 belgelerini değiştirmez ve yeni teknik kapsam açmaz.

## Bundan sonra okunması gereken belge

**Akıllı Rota — Karar Akışları ve Kullanıcı Doğrulama Planı**; 02-ux altında planlanmaktadır, henüz mevcut değildir. Bu belgedeki davranışları gerçek kullanıcı senaryolarıyla sınamalı; özellikle soru yükü, sıra değişimi, kritik bilinmeyen, şehir değişimi ve paylaşım gizliliğinin anlaşılıp anlaşılmadığını incelemelidir. Yeni bir sayfa ailesi veya uygulama tercihi varsaymamalıdır.

Ayrıca 04 ve 05'in öngördüğü **05 Kanıt, Güncellik ve Yayın Politikası** çalışmasının planlanan konumu docs/04-ai/05-kanit-guncellik-yayin-politikasi.md olarak korunur; bu rota belgesi onun ölçülmüş eşiklerini tamamlamış sayılmaz. Belge sırası için [Dokümantasyon dizini](../README.md).
