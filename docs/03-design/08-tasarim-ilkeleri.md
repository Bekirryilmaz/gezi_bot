---
title: "08 Şamandıra — Tasarım İlkeleri"
version: "1.0"
status: "nihai-tasarim-ilkeleri-onerisi-kabul-bekliyor"
phase: "tasarim-felsefesi"
last_update: "2026-09-13"
depends:
  - "../00-product/00-urun-felsefesi.md"
  - "../00-product/01-bilgi-mimarisi.md"
  - "../00-product/02-product-language.md"
  - "../00-product/03-karar-motoru.md"
  - "../00-product/04-sistem-mimarisi.md"
  - "../04-ai/05-ai-bilgi-motoru.md"
  - "../00-product/06-akilli-rota-motoru.md"
  - "../02-ux/07-ux-karar-akislari.md"
affects:
  - "01-research: UX Kullanıcı Doğrulama Planı (planlanan)"
  - "03-design: sonraki tasarım kararları ve içerik sunumu çalışmaları (planlanan)"
  - "06-frontend: web ve mobil davranış belgeleri (planlanan)"
  - "08-admin: bilgi düzeltme ve destek deneyimi (planlanan)"
  - "09-business: Premium değer ve davet politikası (planlanan)"
author: "Codex; kabul yetkisi: proje sahibi"
---

# Şamandıra — Tasarım İlkeleri

> **İnsanlara en iyi yeri göstermeye çalışmaz.  
> Kendileri için doğru olan yeri  
> en kısa yoldan bulmalarını sağlar.**

Bu cümle tasarımın değişmez görevidir. Buradaki en kısa yol, yalnız tıklama veya saniye sayısı değildir. Kullanıcının kendini anlatma, bilgiyi anlama, alternatifleri karşılaştırma, belirsizliği değerlendirme ve yanlış seçimden dönme çabasının toplamıdır. Önemli bir koşulu saklayan kısa yol, ürünün amacını karşılamaz.

**Şamandıra'nın tasarım felsefesi: Karar için gerekli açıklığı, yerin gerçek karakterini ve kullanıcının iradesini aynı deneyimde korumak.** Tasarım, doğru sorunun anlaşılmasını ve yeterli cevaptan sonra durabilmeyi sağlamalıdır. Bir yere gitmek kadar o yeri seçmemek de bilinçli bir karar olabilir.

Bu belge tasarım kararlarının anayasasıdır. Kod, hero, ekran düzeni, wireframe, renk paleti, bileşen veya Figma tarifi içermez. Kart, liste, ikon ve harita bölümleri onların biçimini değil taşıması gereken anlamı tanımlar. Sayısal boyut, süre, hareket eğrisi veya görsel stil reçetesi vermez.

§1–36 istenen konuları sırasıyla cevaplar. §37 değerlendirme yöntemini; §38 kırk sekiz maddelik öz eleştiriyi; §39 alternatif yaklaşımlar ve tercih gerekçesini; §40 öz eleştiri sonrası nihai ilkeleri içerir. Nihai kararlar ana metne işlenmiştir. Duygu hedefleri ve etkililik beklentileri araştırma hipotezidir; kullanıcılarla doğrulanmış sonuç değildir. Bu yeni belgenin hazırlanması, kullanıcı tarafından kabul edildiği veya tasarımın uygulandığı anlamına gelmez.

## 0. Referans otoritesi ve tasarımın yetki sınırı

Kullanıcının 13 Eylül 2026 tarihli bu görevdeki açık beyanıyla **00–07 belgelerinin tamamı kabul edilmiş referanstır**. Özellikle 05, 06 ve 07 dosyalarındaki tarihsel öneri/kabul ifadeleri değiştirilmez. Tasarım ilkeleri bu sekiz belgenin üzerine kurulur; daha yeni belge olmak ürün kapsamını, kavramları veya karar kurallarını değiştirme yetkisi vermez.

| Kabul edilmiş referans | Tasarıma getirdiği bağlayıcı sınır | Bu belgedeki açılım |
|---|---|---|
| [00 Ürün Felsefesi](../00-product/00-urun-felsefesi.md), §2, §5–9 | Uygunluk yükü azalır; dürüstlük hızdan, açık ihtiyaç varsayımdan, güven ticari kazançtan önce gelir | §1–6, §27–29, §36–40 |
| [01 Bilgi Mimarisi](../00-product/01-bilgi-mimarisi.md), §2, §6–7, §9–12 | Tek Keşfet, kendi başına anlamlı Yer, sınırlı ilk seçki, yardımcı harita; yeni portal yok | §8–15, §18, §24 |
| [02 Product Language](../00-product/02-product-language.md), §3–6, §8–14 | Amaç/tercih/zorunlu koşul; ödün/engel; olgu/çıkarım/bilinmeyen ayrımları korunur | §9, §11, §14–17, §19, §28 |
| [03 Karar Motoru](../00-product/03-karar-motoru.md), §2, §5–9, §15, §18 | Zorunlu koşul telafi edilemez; gerekçe gerçek karardan doğar; alternatif anlamlı fark taşır | §8–12, §15, §24, §29 |
| [04 Sistem Mimarisi](../00-product/04-sistem-mimarisi.md), §0, §4, §14–18, §25 | Sunum ikinci karar otoritesi değildir; aynı anlam bütün kanallarda korunur; kesintide dürüst daralma | §9–10, §18, §21–26, §37 |
| [05 AI Bilgi Motoru](../04-ai/05-ai-bilgi-motoru.md), §11–18, §23–29, §33–35, §38–43 | Güven iddiaya aittir; bilgi yaşamı görünür sonuç taşır; Bir İz kayıt/yayın ayrımını korur | §16–17, §19, §23–26, §28 |
| [06 Akıllı Rota Motoru](../00-product/06-akilli-rota-motoru.md), §1–20, §26, §28 | Günün amacı ve toplam yük; düzenleme, boş zaman, ücretsiz temel fayda ve paylaşım sınırları | §3–4, §7, §10–13, §18, §22, §26–27 |
| [07 UX Karar Akışları](../02-ux/07-ux-karar-akislari.md), §0, §14–18, §21–30, §34 | Doğrudan başlangıç, korunmuş bağlam, gerçek işlem sonucu, erişilebilirlik ve baskısız çıkış | Bütün sunum ilkeleri; özellikle §2, §10, §21–27 |

### 0.1. Önceki belgelerdeki gerilimler nasıl korunuyor?

- **Tempo:** Bilgi Mimarisi'nin yer anlatısındaki sözcük, Product Language §5 ve Sistem Mimarisi §0 doğrultusunda yeni bir eksene dönüşmez. Bu belgede okumanın ritmi tasarım anlatımıdır; mekânın tempo veya enerji puanı değildir.
- **Rota ve kayıtlar:** 06 ve 07'nin görev durumları mevcut Keşfet/Yer bağlamında kalır. Tasarım bunları rota portalı, sosyal profil, yeni ana menü veya bağımsız harita merkezine genişletemez.
- **Premium:** Özenli deneyim bütün kullanıcıların hakkıdır. Ücretli Premium'un 06 §18'deki kolaylıkları adaydır. Bu belge fiyat, kota, satış sayfası, ödeme akışı veya yayımlanmış özellik ilan etmez.
- **Şeffaflık:** Dayanak anlamı, kapsam, ilgili güncellik ve düzeltme yolu açıklanır. Ham yorum, yorumcu, iç skor ve kaynak platform dökümü gösterilmez; gerekli veri/hizmet atıfları korunur.
- **Taslak ve öneri:** Kullanıcı uyumsuz veya eksik taslak saklayabilir. Taslağın görsel bütünlüğü yapılabilirlik onayı veremez.
- **Yeni belgenin etkisi:** Sonraki tasarım çalışmalarını yönlendirir. Kabul edilmiş sekiz belgeye geriye dönük değişiklik yapmaz. Çözülemeyen bir çatışma ilgili maddeyle kaydedilir; görsel tercih adına sessizce aşılmaz.

### 0.2. İlke çatıştığında karar sırası

Önce mevcut referanslara uygunluk, kritik doğruluk ve açık zorunlu koşullar korunur. Ardından kullanıcı iradesi ve eşdeğer erişim; sonra kararın anlaşılabilirliği ve bağlam sürekliliği; sonra çaba ve bekleme yükü; bunların içinde karakter ve estetik değerlendirilir. Ticari hedef bu sınırları aşamaz.

Bu sıra erişilebilirliği sonraya bırakma gerekçesi değildir. Doğru bilgi kullanıcı tarafından algılanamıyorsa aktarılmış sayılmaz. Bir önerinin kritik sınırı mevcut sunumda anlatılamıyorsa sunum genişler veya olumlu iddia daralır. Sınır silinmez.

## 1. Şamandıra'nın tasarım felsefesi nedir?

**Tasarım, seçimin nedenini ve bedelini görünür kılan sakin bir rehberliktir.** Kullanıcıya hangi hayatı beğenmesi gerektiğini söylemez. O anki amacını somut yer bilgisiyle ilişkilendirir; karar verebileceği kadar açıklık oluşturur.

Felsefenin üç niteliği vardır. Açıklık, seçenekleri ayıran farkları anlaşılır kılar. Özen, küçük bir ihtiyaca da ciddi ve tutarlı karşılık verir. Karakter, gerçek yerlerin ve yerel yaşamın ayırt edici özelliklerini korur. Bunlardan biri diğerinin eksikliğini kapatamaz: güzel anlatım yanlış bilgiyi, kusursuz düzen de anlamsız öneriyi iyileştirmez.

Şamandıra'nın kendine özgülüğü, başka ürünlerin görsel işaretlerinin karışımından doğmaz. Aynı niyetin aramada, gerekçede, haritada, kayıtta ve çıkışta korunmasından doğar. Kullanıcı ürünü “bana seçim yaptırdı” diye hatırlamalıdır.

**Karar sınaması:** Tasarım tercihi hangi belirsizliği azaltıyor? Hangi gerçek farkı görünür kılıyor? Kullanıcının reddetme veya düzeltme hakkını nasıl koruyor? Bunlara cevap vermeyen tercih, estetik beğeniyle bağlayıcı hale gelemez.

## 2. Kullanıcı ilk baktığında ne hissetmeli?

**“Burada başlayabilirim; kendimi uzun uzun hazırlamam gerekmiyor.”** İlk temas yön bulma rahatlığı yaratmalıdır. Kullanıcı ürünün ne işe yaradığını, kendi niyetiyle nasıl başlayacağını ve kapsamın nerede bittiğini anlayabilmelidir.

Bu rahatlık, kullanıcıyı zaten tanıyormuş gibi konuşarak kurulmaz. İhtiyaç bilinmiyorsa kişisel isabet iddiası yoktur. Yer adıyla gelen kişi doğrudan o yere; ihtiyaçla gelen kişi anlaşılır seçim alanına erişir. Herkes aynı tanıtım sırasından geçirilmez. Hesap, konum ve bildirim izni ilk faydanın önüne konmaz.

İlk izlenimin insani tarafı “ne istediğini bilmemen de normal” duygusudur. Kararsız kişiye anlamı açık başlangıçlar sunulur; onu karakter testine sokan etiketler sunulmaz. Kapsam küçükse büyük bir hizmet alanı görüntüsü yaratılmaz.

**Sınama:** İlk kez gelen kişi, açıklama yardımı almadan nereden başlayacağını ve ne tür yardım alacağını kendi sözleriyle anlatabiliyor mu? Duygu hedefi, hızlı geçiş veya güzel görünüm puanıyla doğrulanmış sayılmaz.

## 3. Siteden ayrılırken ne hissetmeli?

**“Seçimimi anlayarak yaptım; şimdi kendi günüme dönebilirim.”** Bir yeri seçtiyse nedenini ve önemli koşulunu; seçmediyse hangi nedenle vazgeçtiğini bilmelidir. Yeterli bilgi yoksa belirsizliğin nerede kaldığını anlamalıdır.

Kullanıcı bütün olasılıkları tüketmiş olmak zorunda değildir. Makul bir kararın ardından başka yer kaçırdığı duygusu üretilmez. Çıkış yeni öneriler, zorunlu değerlendirme, katkı borcu veya Premium davetiyle uzatılmaz. Daha sonra dönmek isteyen kişi kaydın gerçekten nerede ve hangi sınırla saklandığını bilir.

Bir günlük rotanın erken bitmesi tasarım açısından meşru, ölçüm açısından nötr sonuçtur. Kullanıcı memnun kaldığı için de sorun yaşadığı için de ayrılabilir. Kısa oturum otomatik başarı; uzun oturum otomatik başarısızlık değildir. Ayrılmanın anlamı davranış ve gönüllü deneyim karşılığıyla değerlendirilir.

**Sınama:** Kullanıcı kararını gerekçelendirebiliyor, kayıt/çıkış sonucunu anlayabiliyor ve zorlanmadan ayrılabiliyor mu? Kendini kararını savunmak ya da bir programı tamamlamak zorunda hissediyorsa tasarım amacından uzaklaşmıştır.

## 4. Premium hissi nasıl oluşmalı?

**Premium his, kullanıcının zamanına ve muhakemesine gösterilen özenin toplamıdır.** Pahalı yerleri yüceltmek, ayrıcalık duygusu satmak veya ihtişamlı yüzeyler kurmak değildir. Ücretsiz bir yürüyüşü seçen kişi de aynı ciddiyetle karşılanır.

Özen; isabetli sözcükte, tutarlı hiyerarşide, yerinde ayrıntıda, temiz geri dönüşte ve dürüst işlem sonucunda hissedilir. Kullanıcı tekrar anlatmak zorunda kalmaz; gereksiz mesajla bölünmez; bir hatada terk edilmez. Ortamın karakteri iyi seçilmiş gerçek içerikten gelir. Kalite, ilk görüntü kadar yavaş bağlantıda ve bilinmeyen bilgi karşısında da sürmelidir.

“Premium his” deneyim standardıdır; **Premium** ise ancak doğrulanıp açılan ilave kolaylıkların ticari kapsamı olabilir. Daha doğru bilgi, erişilebilir kullanım, önemli uyarı ve temel kontrol ücretli ayrıcalık değildir. Ücretsiz deneyimi kasıtlı biçimde yorarak ücretli sürümü değerli gösterme kabul edilmez.

**Sınama:** Marka işaretleri ve etkileyici medya çıkarıldığında deneyim hâlâ özenli mi? Hata düzeltme, geri alma ve gerçek bilgi sınırı da ilk izlenim kadar iyi mi? Cevap hayırsa premium hissi yüzeyseldir.

## 5. Şamandıra neden minimal olmalı?

Kullanıcı bir yer seçmek için yeni bir yazılımın mantığını öğrenmek zorunda kalmamalıdır. Her gereksiz eylem, tekrar ve bağımsız bölüm, kararın asıl sorusuyla yarışır. Minimal yaklaşım bu rekabeti azaltır.

Azaltmanın hedefi önce tekrarlanan anlam, ilgisiz teklif, gereksiz geçiş, kanıtsız sıfat ve birbirine benzeyen seçenektir. Kararı taşımayan bilgi öne çıkmaz. Arama ile Keşfet'in tek alan olması ve haritanın yardımcı rolü bu yaklaşımın yapısal karşılığıdır.

Minimal olmak tek eyleme mecbur bırakmak değildir. Kullanıcının “düzelt”, “vazgeç”, “daha fazlasına bak” gibi hakları korunur. Çaba yalnız ekranda görünen şeylerden oluşmaz; görünmeyeni aramak da çabadır.

**Sınama:** Bir şey kaldırıldığında aynı karar daha az açıklamayla verilebiliyor mu? Kullanıcı kaldırılan kontrolü arıyor, bilgiyi hatırlamaya çalışıyor veya geri dönmek zorunda kalıyorsa sadeleşme gerçekleşmemiştir. Yalnız daha boş bir görünüm elde edilmiştir.

## 6. Neden tamamen minimal olmamalı?

**Eksiltmenin sınırı, anlam ve seçim hakkının kaybolduğu yerdir.** Çok kısa anlatım; koşulu, ödünü, yerin karakterini ve karşılaştırma farkını silebilir. Kullanıcıya güzel bir fotoğraf ile tek eylem bırakmak uygunluğu değerlendirme yükünü ona geri verir.

Şamandıra yeterli zenginlik taşımalıdır: gerçek ortamı anlamaya yarayan içerik, karar açısından gerekli derinlik, anlaşılır alternatifler ve bilgi sınırları. İlgili gerekçenin yanında kalması gereken bir bilinmeyen, “ayrıntı” adına geri çekilmez. Kararın önemi arttıkça açıklamanın derinleşmesi normaldir.

Yerlerin aynı sözlerle anlatılması da aşırı minimalizmdir. Kıyıda oturmak ile kapalı salonda konuşmak arasındaki gerçek fark korunmalıdır. Ancak zenginlik uzun tarihçe veya dekoratif medya zorunluluğu oluşturmaz; içeriğin işlevi gösterilebilir olmalıdır.

**Sınama:** Kullanıcı iki seçeneğin farkını ve seçtiği yerin kendisine uymayabileceği koşulu anlatabiliyor mu? Anlatamıyorsa daha fazla sadeleştirmek yerine doğru ayrıntıyı geri getirmek gerekir. Hedef en az içerik değil, karar için yeterli içeriktir.

## 7. Boşluk kullanımı

Boşluk, bilgilerin ilişkisini ve okumanın sırasını anlaşılır kılar. Aynı karara ait gerekçe ile önemli koşul birbirinden kopmamalı; farklı kararların sınırı anlaşılmalıdır. Boşluk bu ilişkiyi desteklediği ölçüde değerlidir.

Ferah görünmek adına kullanıcının birbirine bağlı iki bilgiyi uzak yerlerden toplaması istenmez. Aynı biçimde karşılaştırılabilir seçenekleri gereğinden fazla ayırmak hafıza yükünü artırabilir. Dar ekran, metin büyütme ve farklı dil uzunluklarında ilişki korunur; boşluk oranı kutsallaştırılmaz.

Boş alan her zaman doldurulacak kapasite değildir. Yeterli seçenek yoksa yeni öneri eklenmez. Günlük rotada boş bırakılan zaman da aynı saygıyla ele alınır; kullanıcının zamanı sistemin dolduracağı bir envanter değildir. Ancak sayfa boşluğu ile planın boş zamanı ayrı kavramlardır.

**Sınama:** Kullanıcı hangi bilgilerin birlikte okunacağını doğru anlıyor mu? Bilgiler arasında gidip gelmesi artıyorsa boşluk azaltılabilir; metinleri birbirine karıştırıyorsa artırılabilir. Ölçüt dekoratif ferahlık değil, anlamın okunabilirliğidir.

## 8. Bilgi yoğunluğu

Bilgi yoğunluğu alan başına sözcük sayısıyla yönetilmez. **Aynı anda çözülmesi gereken farklı soru sayısı ve karşılaştırma yüküyle** yönetilir. Uzun ama tutarlı açıklama, kısa fakat belirsiz işaret yığınından daha kolay anlaşılabilir.

İlk okuma; yer kimliği, bu bağlamdaki gerekçe, önemli ödün ve gerekli bilgi sınırını taşır. İsteğe bağlı derinlik bunların dayanağını ve pratik ayrıntıları açar. İç analiz, ham yorum ve teknik skorlar derinlik katmanı adıyla ürüne sokulmaz.

Keşfet'in ilk kümesindeki 3–5 hedefi, Yer'deki en çok 3 alternatif ve rotadaki bir ana, gerekirse en çok 2 ek seçenek 01, 06 ve 07'den gelir. Bunlar bütün kullanım alanlarına taşınacak yeni bir “az seçenek yasası” veya sayı doldurma görevi değildir. Daha fazla sonuç açık kullanıcı isteğiyle erişilebilir kalır.

**Sınama:** Kullanıcı gerekçe, ödün ve bilinmeyeni karıştırmadan aktarabiliyor mu? Gerekli açıklama sığmıyorsa önce tekrar ve ikincil olumlu anlatım azalır. Kritik koşul küçülmez veya kaybolmaz. Büyük ekran da öneri sayısını artırma izni vermez.

## 9. Hiyerarşi

Hiyerarşi, tasarımcının neyi etkileyici bulduğunu değil **bu kullanıcının kararını neyin değiştirdiğini** gösterir. Bilinen kapanma veya açık zorunlu koşulu bozan engel, çekici özelliklerin gerisine konamaz. Bilgi Mimarisi'nin kimlikten gerekçe/ödüne, pratik koşullardan gitme bilgisine uzanan sırası korunur.

Bağlam belirli ayrıntının önemini değiştirebilir. Basamaksız erişim şartsa ilgili yol bilgisi ana karar bilgisidir. Bu, her yeni sorguda yer kimliğinin ve bütün okuma düzeninin yer değiştirmesini gerektirmez. Sabit anlam iskeleti içinde vurgu güncel ihtiyaca bağlanır.

İddia ile onu sınırlayan saat, bölüm veya belirsizlik aynı yorumlama anında erişilebilir olmalıdır. Olumlu anlatımın güçlü, sınırın okunamayacak kadar silik olması doğruluk ihlalidir. Görsel, sesli ve büyütülmüş okumada aynı anlam önceliği sürer.

**Sınama:** Sadece ilk okumayı yapan kişi önemli engeli fark ediyor mu? Bir fotoğrafın çekiciliği, ticari ilişki veya gösterim kolaylığı motorun sırasını değiştiriyorsa tasarım ikinci karar motoruna dönüşmüştür; tercih reddedilir.

## 10. Odak yönetimi

Odak iki sorumluluktur: kullanıcının zihninde hangi sorunun etkin olduğu ve etkileşimde şu anda nerede bulunduğu. Bir görevde baskın devam açık olmalı; geri dönme, düzeltme ve vazgeçme yolları bulunabilir kalmalıdır.

Yeni sonuç, bildirim veya güncelleme kullanıcının okuduğu yeri kendiliğinden ele geçirmez. Bir alt görevden dönüşte önceki bağlam tanınır. Arama metni, seçili koşullar, liste konumu ve rota seçimleri korunur. Haritaya geçmek veya dış yol tarifinden dönmek yeni bir başlangıç sayılmaz.

Kritik bilgi değiştiğinde ilgili eski olumlu hüküm devam edemez; fakat bu, taslağı yeniden düzenleme yetkisi vermez. Değişen durum anlaşılır biçimde duyurulur. Kullanıcı işaretçi kullanmasa da etkin konumunu bulabilir; hiçbir temel bilgi yalnız üzerine gelince öğrenilmez.

**Sınama:** Bir kesinti veya düzenleme sonrası kişi “Neredeydim, ne değişti, şimdi ne yapabilirim?” sorularını cevaplayabiliyor mu? Odak tasarımın kullanıcıyı yönettiği bir araç değil, kişinin kendi işini sürdürmesini sağlayan sürekliliktir.

## 11. Kart felsefesi

Kart kullanılacaksa bir **değerlendirme birimi**dir. Yer kimliğini, o aramada neden bakmaya değer olduğunu, belirleyici ödünü ve gerekli sınırı birlikte taşır. Kartın amacı ayrıntıya tıklatmak için merak açığı yaratmak değildir; bazı yerleri açmadan elemek de görevini yerine getirmesidir.

Her kart aynı miktarda iddia taşımak zorunda değildir. Bilgisi az olan bir yerin boşluğu sahte özelliklerle doldurulmaz; görseli olmayan yer değersizleştirilmez. Ortak ölçütler karşılaştırmayı kolaylaştırır, yerin gerçek farkını silmez. Fotoğraf, kişisel uygunluk veya doğrulama işareti yerine geçmez.

Bir yerin ad aramasında bulunması onu uygun öneri yapmaz. Kayıt, öneri ve kullanıcının seçtiği taslak, sunumda bu anlamlarını korur. Zorunlu koşulu bilinmeyen aday, üzerine uyarı eklenerek doğrulanmış eşleşme grubuna alınamaz.

**Sınama:** Ayrıntıyı açmadan, kullanıcının bu yere neden bakacağı ve neyi bilmediği anlaşılabiliyor mu? Her kart aynı övgüyü taşıyorsa ya gerekçe zayıftır ya biçim yanlış işi yapıyordur. Bu bölüm kartın ölçüsünü, iç düzenini veya görünümünü belirlemez.

## 12. Liste felsefesi

Liste, seçeneklerin **ortak ölçütlerle ve anlamlı farklarıyla okunabildiği bir karşılaştırma alanıdır**. Başlı başına bir öneri gerekçesi olmayan sıra numarası veya genel yer puanı üretmez. İlk sırada olmak herkes için üstün olmak anlamına gelmez.

Kullanıcı anlaşılan ihtiyacı, sıralamanın anlamını, gösterilen kümenin kapsamını ve daha fazlasına nasıl ulaşacağını anlayabilir. Sayfanın sonu belirsiz akışa dönüşmez. Yer ayrıntısından dönüş aynı liste bağlamına gelir. Reddedilen yer aynı bağlamda başka bir övgüyle geri sokulmaz.

Kişisel listelerin anlamı ayrıdır. Gezeceğim Yerler niyeti; Gezdiğim Yerler kullanıcının ziyaret beyanını; rota günlük karar ilişkisini taşır. Hiçbiri tamamlama borcu, başarı serisi veya sosyal itibar değildir. Rotadaki sıranın değişmesi toplam yükü etkileyebilir; sıradan yer listesi aynı yapılabilirlik iddiasını taşımaz.

**Sınama:** Kullanıcı iki seçeneğin farkını zihninde tutmadan karşılaştırabiliyor, nerede kaldığını bulabiliyor ve kaydın ne anlama geldiğini ayırabiliyor mu? Daha yoğun görünüm ancak bu işleri iyileştiriyorsa seçilir.

## 13. Navigasyon felsefesi

Navigasyon kullanıcının ürün organizasyonunu öğrenmesini değil **niyetini kaybetmeden ilerlemesini** sağlamalıdır. Ayrı bir yere doğrudan gelen kişi önce şehir ve ilçe seçmeye zorlanmaz. Menü ve sayfa aileleri 01'e bağlı kalır.

Arama Keşfet'in durumudur; harita aynı seçeneklerin konum anlatımıdır. Rota ve kayıtlar 07 §0.2'de tanımlandığı gibi mevcut bağlamdaki görevlerdir. Kayıtlara dönüş Keşfet içindeki Kaydettiklerin yolundan bulunabilir kalır; görünmezlik sadelik sayılmaz. Yeni bir işlev, kendiliğinden yeni ana menü maddesi gerektirmez.

Geri dönüş ürün sözüdür. Kullanıcı yazısını, koşulunu, seçimini ve baktığı yeri yeniden kurmak zorunda kalmaz. Destek ve yöntem okumak da mevcut karardan koparmamalıdır. Dış hizmete geçişin ne yaptığı anlaşılır olur; yol tarifi açmak ziyaret veya rezervasyon sayılmaz.

**Sınama:** Kullanıcı geldiği yerin adını, yaptığı işi ve geri dönüş yolunu açıklayabiliyor mu? Bulunabilirlik sorunu varsa önce mevcut yolun adı, bağlamı ve görünürlüğü iyileştirilir; yeni portal son çare bile olsa önce referans kapsamı değerlendirilir.

## 14. Arama deneyimi

Arama, kullanıcının niyetini ürünün anlayabildiği kapsamla buluşturan bir anlaşmadır. Tam yer adı biliniyorsa doğrudan bulma; ihtiyaç belirtiliyorsa gerekçeli seçenek üretme işi yapılır. Kullanıcı doğru komutu bilmek veya yapay zekâya hitap etmeyi öğrenmek zorunda değildir.

Türkçe yazım farklılıkları ve bilinen adlar gereksiz çıkmaz yaratmamalıdır. Ancak belirsiz bir düzeltme başka şubeyi sessizce seçemez. Anlaşılan şehir, amaç ve koşul görünür ve düzeltilebilir kalır. Doğal dilin bir bölümü anlaşılamadıysa bütün isteğin karşılandığı söylenmez.

Netleştirme yalnız cevabı kararı değiştirecekse gerekir. “Sakin” sözündeki ses/yoğunluk ayrımı sonucu değiştirmiyorsa soru üretmek gerekmez. “En iyi” isteği genel sıralamaya çevrilmez. Yakınlık için kullanıcının seçtiği nokta veya isteğe bağlı konumu yeterli olabildiği ölçüde kullanılır; konum izni başlangıç şartı değildir.

**Sınama:** Kullanıcı kendi ifadesiyle sistemin anladığını karşılaştırıp tek bir yanlışı düzeltebiliyor mu? Arama ilerledikçe şartların unutulması veya her denemede uzun konuşma kurulması tasarım kusurudur. AI varlığı, aramanın konusu değil yardımın olası aracıdır.

## 15. Filtre mantığı

Filtre, sorguyu daraltan teknik bir araç olmanın ötesinde **hangi koşullar altında öneri istediğimizi görünür kılan kullanıcı kararıdır**. Kategori, deneyim, koşul ve coğrafya farklı sorulara cevap verir; eşdeğer etiket yığınına dönüşmez.

Tercih ile zorunlu koşulun farkını tasarım kendi başına belirleyemez. “Ucuz” bir tercih olabilir; kullanıcının açık toplam bütçe sınırı telafi edilemez. “Basamaksız erişim şart” ifadesi, çok iyi başka özelliklerle dengelenecek ağırlık değildir. Bir koşulun bilinmiyor olması da karşılandığı anlamına gelmez.

Koşul değiştiğinde yeni seçimin ve değerlendirme durumunun anlamı anlaşılır olur. Eski sonuçlar yeni filtreyi karşılıyormuş gibi görünmez. Koşulların neden sonucu azalttığı biliniyorsa açıklanır; bilinmiyorsa belirli bir filtre suçlanmaz. Kullanıcı tek koşulu değiştirebilir; bütün koşulları silmeye mecbur edilmez.

**Sınama:** Kullanıcı hangi sınırın uygulandığını, hangisinin öneri niteliğinde olduğunu ve kaldırmanın neyi değiştireceğini anlayabiliyor mu? Sadelik için erişim gereksinimini gizlemek de sonuca ulaşmak için bütçeyi habersiz artırmak da kabul edilmez.

## 16. Görsel kullanımı

Görsel içerik, yeri ve seçenekler arasındaki farkı anlamaya katkı sağlar. Üç meşru işi vardır: tanınmayı desteklemek, ilgili fiziksel bağlamı açıklamak ve gerçek yerin karakterini hissettirmek. Bu işler kanıt, uygunluk veya canlılık garantisiyle karıştırılmaz.

Görsel seçimde soru “etkileyici mi?” ile bitmez: hangi karar ayrımını açıklıyor, hangi yanlış beklentiyi doğurabilir, erişilemediğinde anlam nasıl korunuyor? Bir terasın görünmesi kapalı salonun, rampanın görünmesi bütün erişim yolunun bilgisi değildir.

Görsel yoğunluğu göreve bağlıdır. Yeni yer hakkında fikir edinmekte yararlı olan medya, dar bir bütçe ve süre karşılaştırmasını ağırlaştırabilir. Yalnız estetik akıcılık için gerekli koşul görünmez hale getirilemez. Medya yüklenmemesi bilinen metinle karar vermeyi engellemez.

**Sınama:** Görsel kaldırıldığında hangi anlam kayboluyor? Kaybolan yalnız gösterişse önceliği düşer. Kaybolan önemli anlam ise erişilebilir metinsel eşdeğeri de bulunmalıdır. Paylaşım özetleri dahil hiçbir görsel, taşıyamadığı kritik sınırı olumlu bir iddianın arkasına saklayamaz.

## 17. Fotoğraf kullanımı

Fotoğrafın temel görevi yeri **tanınabilir ve beklentisi ölçülü** kılmaktır. Estetik kalite önemlidir; fakat olağan koşulları yanlış temsil eden kusursuz kare ürünün güvenini aşındırabilir. Yer, yalnız seyrek yaşanan ideal anıyla anlatılmamalıdır.

Seçim, kararın konusuna bağlanır: fiziksel alan, ilgili bölüm, giriş, oturma ilişkisi veya çevre. Her şeyin fotoğraflanması zorunlu değildir. Görselin hangi yere ve bölüme ait olduğu belirsizse gerçek yer kanıtı gibi kullanılamaz. Saat ve mevsim bilinmiyorsa bunlar kadrajdan uydurulmaz.

Kadraj, düzeltme veya sunum; basamak, sıkışıklık ya da ilgili fiziksel engeli gizleyerek başka koşul vaat etmemelidir. Dekor fotoğrafı sessizliği, boş alan anlık müsaitliği, insan fotoğrafı o gruba uygunluğu kanıtlamaz. Yapay veya temsili görüntü gerçek mekânın belgesi yerine geçemez. Gerçek görüntü yoksa eksiklik dürüstçe kabul edilir.

**Sınama:** Kullanıcı gördüğü şeyden fotoğrafın desteklemediği bir güvence çıkarıyor mu? Fotoğrafsız ama bilgisi yeterli yer, yalnız medya eksikliği yüzünden daha az uygun sunuluyor mu? Hak ve atıf koşulları ile kişilerin gereksiz ifşa edilmemesi, editoryal seçimin sınırıdır.

## 18. Harita kullanımı

Harita **konum, bağlantı ve hareket yükünü anlamanın yardımcısıdır**. Şamandıra'nın başlangıç zorunluluğu veya ürün kimliğinin tamamı değildir. Yerlerin haritada çokluğu, doğru seçim alanının zenginliğini kanıtlamaz.

Liste ile harita aynı sorgu, koşul ve seçimi taşır. Haritayı kaydırmak mevcut ulaşım sınırını veya arama alanını habersiz değiştirmez. Mekânsal yakınlık, kullanılabilir yol veya fiziksel erişim anlamına gelmez. Kuş uçuşu mesafe, yürüme süresi gibi anlatılamaz. Plan çizgisi de canlı navigasyon veya kesin yapılabilirlik güvencesi değildir.

Harita temel kararı desteklemiyorsa kullanıcı listede kalabilir. Rota sırası, toplam yük ve önemli geçiş sınırları metinle anlaşılmalıdır. Bir durak seçimi haritada tanınabilir; otomatik uçuş veya geniş hareket kullanıcıyı takip etmeye zorlayamaz. Gerekli harita atıfları dekoratif sadelik adına kaybolmaz.

**Sınama:** Harita olmadan aynı yer seçilebiliyor ve günlük planın önemli sınırları anlaşılabiliyor mu? Harita açıldığında bir sorunun cevabı kolaylaşıyor mu? Cevap yoksa harita görünürlüğü azaltılır; yeni bağımsız merkez kurulmaz.

## 19. İkon dili

İkon tanımayı hızlandıran yardımcı bir işarettir. Yeni bir sözlük öğrenme zorunluluğu yaratmamalı; temel işlemin anlamı, durum veya erişilebilir adıyla birlikte anlaşılmalıdır. Aynı işaret aynı anlamı taşır; benzer görünümlü farklı eylemler belirsiz bırakılmaz.

Özellikle yıldız, kalp, kalkan ve onay işaretleri genel kalite, beğeni, güvence veya doğrulanma çağrışımı doğurabilir. Kaydetme ile beğenme; katkının alınması ile bilginin doğrulanması birbirinden ayrılmalıdır. İç güven düzeyini mekâna kefil olan bir simgeye çevirmek yasaktır.

Durum yalnız ikonla veya renkle anlatılmaz. Kullanıcı görseli tanıyamasa da eylemi seçebilir, sonucun beklediğini veya tamamlandığını anlayabilir. Yerel simge aşinalığı ve farklı kullanım alışkanlıkları sınanır; tasarım ekibinin sezgisi evrensel kabul edilmez.

**Sınama:** Kullanıcı simgeyi açıklamasız yanlış yorumluyorsa metin desteği artırılır veya işaret yeniden değerlendirilir. Bu belge ikon seti, çizgi kalınlığı veya biçim ailesi seçmez. Dilin ilkesi anlam tutarlılığı ve anlaşılabilirliktir.

## 20. İllüstrasyon kullanılmalı mı?

**Sınırlı ve gerekçeli olarak kullanılabilir; zorunlu marka malzemesi değildir.** Yöntemin soyut bir ayrımını anlatmayı veya kararsız bir başlangıcı daha davetkâr kılmayı gerçekten kolaylaştırıyorsa değerlidir. Her boşluk, hata veya başarı için resim üretmek gerekmez.

İllüstrasyon gerçek yer fotoğrafının, doğrulanmış haritanın veya eksik mekân bilgisinin yerine geçemez. Temsili olan içerik öyle anlaşılmalıdır. Kullanıcı bir çizimden fiziksel erişim veya gerçek yer düzeni sonucu çıkarmamalıdır.

Duygu zorlaması sınırdır. Boş listede üzgün karakter, vazgeçen kullanıcıya sitem veya başarıda zorunlu kutlama kullanılmaz. Hata durumunda açıklama ve kurtarma yolu önce gelir. Sıcaklık, sorunu hafife alma pahasına kurulamaz.

**Sınama:** İllüstrasyon olmadan kavram aynı kolaylıkta anlaşılıyorsa ekleme gerekçesi zayıftır. Anlama katkısı varsa da hareket, yükleme ve erişilebilirlik maliyeti değerlendirilir. Özgünlüğün tek taşıyıcısı çizim olmamalı; ürünün dili ve davranışı zaten karakter taşımalıdır.

## 21. Animasyonların amacı ne?

Animasyon yalnız **ilişkiyi, değişimi veya sürekliliği anlamayı** kolaylaştırmak için vardır. Kullanıcının eylemiyle yeni durum arasındaki bağı açıklayabilir; örneğin hangi seçimin değiştiğini fark ettirebilir. Dikkati tutmak, işlem süresini teatral hale getirmek veya AI'ı zeki göstermek gerekçe değildir.

Her hareketin hareketsiz karşılığı bulunur: anlaşılır durum, metinsel fark, başlık veya korunan odak. Hareket azaltıldığında bilgi ve kontrol azalmaz. Kullanıcının yeni eylemi animasyonun bitmesini beklemez; okuma ve işlem önüne gösteri konmaz.

Haritada otomatik uçuş, yapay rota üretim sahnesi, sürekli dikkat çağıran hareket ve zorunlu kutlama 07'nin sınırlarıyla bağdaşmaz. Çok az hareket de tek başına kalite ölçüsü değildir; işlevi olmayan hareket çıkarılır, işe yarayan hareket aynı anlamı erişilebilir biçimde destekler.

**Sınama:** Hareket kapalıyken görevin bütün anlamı korunuyor mu? Açıkken yanlış anlama veya bağlam kaybı azalıyor mu? Yalnız beğenilmesi yeterli değildir. Hareket süresi ve eğrisi bu anayasanın konusu değildir.

## 22. Mikro etkileşimler neden var?

Mikro etkileşim **“İsteğim algılandı mı, işlem gerçekleşti mi, geri alabilir miyim?”** sorularını cevaplar. Her küçük eylemin ardından yeni bir ekran veya tören açmaz. Kullanıcıyı gereksiz tekrar eyleminden ve sonuç tahmininden kurtarır.

İsteğin alınması, beklemesi, tamamlanması ve doğrulanamaması ayrı durumlardır. Kullanıcının taslak değişikliği hemen görülebilir; fakat dış kayıt veya gönderim tamamlanmadan kalıcı başarı söylenmez. Rotaya yer eklemek de o yerin uygunluk kontrolünü geçmiş olması anlamına gelmez.

Geri alma, kısa süreli bir mesajı yakalayabilmeye bağlı kalmaz; ilgili kaydın bağlamında bulunabilir. Geri alınan kullanıcı seçimi, yeni kapanma bilgisini veya geri çekilmiş bir iddiayı eski haline döndüremez. Bir etkileşimin kapsamı diğerine taşmaz: kopyalandı, gönderildi değildir.

**Sınama:** Kullanıcı eylemin sonucunu tahmin etmeden anlayabiliyor ve gerektiğinde düzeltebiliyor mu? Ses, titreşim ve hareket tek bildirim yolu olamaz. Fazla geri bildirim, yanlış yere müdahale ve üst üste mesajlar oluşuyorsa mikro etkileşim kendi amacını bozmuştur.

## 23. Loading deneyimi

Bekleme deneyiminin görevi zamanı eğlenceyle doldurmak değil, **isteğin durumunu anlaşılır ve kontrol edilebilir tutmaktır**. Kullanıcı neyin beklendiğini, hangi seçimin işlendiğini ve beklemeyi bırakınca ne olacağını bilmelidir.

Sorgu, koşullar ve taslak görünür kalır. Karar için anlamı tamamlanmış metin medya beklenmeden okunabilir. Ancak olumlu iddiayı önce, onu geçersiz kılan kritik bilgiyi sonra göstermek hız değildir; geçici yanlış güvencedir. Yükleme sırasında okunan içerik ve eylem hedefleri kullanıcıyı şaşırtacak biçimde yer değiştirmemelidir.

Gerçek ilerleme bilinmiyorsa yüzde veya kalan süre uydurulmaz. AI'ın hayalî düşünme aşamaları yazılmaz. Beklemeyi bırakma yolu işlem başından itibaren erişilebilir; uzayan beklemede daha belirgin olmalıdır. Geç gelen eski sonuç, son kullanıcı seçimini veya odağını geri alamaz.

**Sınama:** Kullanıcı yeniden basma ihtiyacı duymadan isteğin alındığını biliyor mu? Beklemeyi bırakınca işi korunuyor mu? Yalnız gerçekten korunabilen kayıt vaat edilir. Çevrimdışında tarihli temel bilgi kalabilir; yeni canlılık veya yapılabilirlik iddiası kurulamaz.

## 24. Boş durum ekranları

Boş durum, içeriğin yokluğu hakkında **belirli bir anlam** taşımalıdır. Aşağıdaki durumları tek “bir şey bulunamadı” anlatısına indirmek kullanıcıyı yanlış düzeltmeye yönlendirir.

| Durum | Taşıması gereken anlam | Tasarımın sınırı |
|---|---|---|
| Henüz kayıt yok | Kullanıcı buraya bir şey saklamadı | Eksik profil, geride kalma veya tamamlama borcu yaratılmaz |
| Bilinçli boş taslak | Kullanıcı henüz karar vermeden başlayabilir | Zorunlu form veya rastgele yer eklenmez |
| Koşullara eşleşme yok | Bilinen seçeneklerde bu sınırlar birlikte karşılanmadı | Bütçe/coğrafya kendiliğinden genişletilmez |
| Kritik bilgi eksik | Eşleşme için gerekli koşul doğrulanamıyor | Bilinmeyen, yok veya uygun gibi sunulmaz |
| Kapsam dışı coğrafya | Şamandıra o alanı yeterince bilmiyor | Orada seçenek olmadığı iddia edilmez |
| Ad bulunamadı | Kayıt veya ad ayrımı çözülemedi | Hayalî yer ve sessiz yanlış düzeltme yoktur |

Mevcut niyet korunur; bilinen neden kısa açıklanır ve en anlamlı devam seçeneği sunulur. Kullanıcı önerilen değişikliği yapmadan sonuç kapsamı değişmez. Taslağı tutmak, aynı koşullarla kalmak veya çıkmak geçerlidir.

**Sınama:** Kullanıcı sorunun kendi tercihi mi, bilgi kapsamı mı, henüz işlem yapmamış olması mı olduğunu ayırabiliyor mu? Hata bir boş durum değildir. Boşluğu dekoratif içerik, zayıf öneri veya ücretli davetle kapatmak kabul edilmez.

## 25. Hata ekranları

Hata deneyimi ürünün sorumluluk aldığı andır. **Neyin yapılamadığı, neyin korunduğu ve şimdi hangi yolun işe yarayabileceği** açık olmalıdır. Kullanıcıya teknik teşhis görevi veya kendi hatası olduğu duygusu verilmez.

Hatanın etkisi yerel kalır: harita çalışmıyorsa okunabilir liste; paylaşım çalışmıyorsa özel taslak kullanılabilir. Etkilenen uygunluk veya toplam değerlendirme ise olumluymuş gibi sürdürülemez. Hata mesajı kısa olmak uğruna belirsiz bir özür cümlesine indirgenmez.

İşlem sonucu bilinmiyorsa başarısızlık kesinleştirilmez. Önce ne olduğu anlaşılır; yeniden deneme kullanıcıyı çift kayıt veya çift gönderime götürmez. Destek yolu, kullanıcıyı uzun form veya üyelik zorunluluğuna sokmadan bulunabilir olmalıdır. Gerçekte korunmamış emek için “hiçbir şey kaybolmadı” denmez.

**Sınama:** Kullanıcı sorunu kendi sözleriyle açıklayıp kalan işini sürdürebiliyor mu? Aynı deneme sürekli aynı belirsizliğe dönüyorsa farklı devam veya destek gerekir. Hata anında mizah, reklam ve Premium teklifi kullanıcının işini gölgelememelidir.

## 26. Başarı ekranları

Başarı geri bildirimi **yalnız gerçekleşmiş işlemin kapsamını** anlatır. Çoğu küçük iş için ayrı bir başarı ekranı gerekmez. Kullanıcının kaldığı yerde net sonuç ve gerekiyorsa geri alma yeterlidir. Daha büyük sonuçlarda açıklamanın kapsamı artabilir; zorunlu kutlama oluşmaz.

| Gerçekleşen | Söylenebilecek anlam | Söylenemeyecek sonuç |
|---|---|---|
| Taslak kaydı tamamlandı | Belirtilen yerde saklandı | Rota kesin yapılabilir |
| Bağlantı kopyalandı | Kopyalama gerçekleşti | Mesaj gönderildi |
| Bir İz alındı | Gözlem kayda alındı | Bilgi doğrulandı/yayımlandı |
| Paylaşım kapatma doğrulandı | Yeni link açılışları kapalı | Dışarıdaki bütün kopyalar silindi |
| Yol tarifi açıldı | Dış yönlendirmeye geçildi | Kullanıcı ziyaret etti |
| Gün bitirildi | Kullanıcı bugün durdu | Memnuniyet veya başarısızlık kesinleşti |

Başarı anı yeni bir görev açmak için kullanılmaz. Kullanıcı ayrılabilir; sonraki eylem yalnız mevcut amacın doğal devamıysa görünür olur. Kayıt tarihi, bilgi doğrulama tarihi gibi sunulmaz.

**Sınama:** Kullanıcı neyin olduğunu ve neyin henüz olmadığını ayırabiliyor mu? Geri bildirim gereğinden fazla güvence veya tamamlama baskısı üretiyorsa sadeleştirilir. Memnuniyet, tasarımın ilan ettiği durum değil gerçek deneyimde araştırılacak sonuçtur.

## 27. CTA felsefesi

CTA, yani eyleme çağrı, **sonucu anlaşılır bir seçim teklifidir**. Kullanıcı tıklayınca ne olacağını ve önemli bir kapsam değişikliği doğup doğmayacağını öngörebilmelidir. Dil somut fiil ve işlemin nesnesini taşır; belirsiz heyecan cümleleri kararın yerini alamaz.

Bir görevde baskın devam bulunur. Bu öncelik reddetme, düzeltme, geri dönme veya ücretsiz devamı görünmez kılmaz. Eylemler eşit ağırlıkta yığılmadığı gibi tek bir sonuca zorlayan sunum da kurulmaz. Keşif kararı veren kullanıcıya her yerde rota oluşturma teklif etmek görevi gereksiz büyütür.

Kullanıcının açık, basit ve geri alınabilir eylemi tekrar onaylatılmaz. Özel bilgiyi paylaşma veya zorunlu koşuldan vazgeçme gibi ek sonuç doğuyorsa kapsam önce anlaşılır olur. İlgili kontrol, kararın gerçek bedeline göre gerekir; her işleme aynı sürtünme uygulanmaz.

**Sınama:** Kullanıcı eyleme geçmeden sonucu doğru tahmin edebiliyor mu? Kapatma, reddetme ve alternatif yol bulunabiliyor mu? Sahte kıtlık, geri sayım, bütçeyi küçümseyen davet ve emek harcandıktan sonra ödeme zorlaması yasaktır.

## 28. Güven hissi nasıl oluşturulur?

Güven, ürünün kusursuz görünmesinden değil **sözüyle davranışının ve dış dünyadaki karşılığının yeterince örtüşmesinden** birikir. Kullanıcıya daha emin hissettirmek tek başına amaç değildir; hissettiği güvenin dayanağın sınırıyla uyumlu olması gerekir.

Her öneride gerçek gerekçe ve önemli ödün bulunur. Belirsizlik ilgili iddiaya bağlanır. Bilginin kontrol tarihi yalnız gerçekten kontrol edilmiş alanı niteler. Olgu, çıkarım ve tahmin aynı kesinlikte konuşmaz. Bir yerin güçlü adres bilgisi, bilinmeyen erişimine genel güven veremez.

Yöntem, sorumluluk, düzeltme ve iletişim yolları bulunabilir kalır. Bir düzeltmenin alındığı, incelendiği ve sonucu etkilediği ayrı anlatılır. Şeffaflık ham yorum yayınına veya iç puan dökümüne dönüşmez. Gerekli atıflar korunur. Ticari ilişki varsa açıkça ayrılır; uygunluk veya organik sıra satın alamaz.

**Sınama:** Kullanıcı hangi iddiaya ne ölçüde dayanabileceğini, neyi henüz bilmediğimizi ve yanlışlığı nasıl bildireceğini anlatabiliyor mu? Genel “güvenilir yer” rozeti, AI onayı veya kusursuz estetik bu soruların cevabı olamaz.

## 29. Keşif hissi nasıl oluşturulur?

Keşif, **kendi amacıyla ilişkili ama henüz düşünmediği anlamlı bir olasılığı fark etmektir**. Her defasında şaşırtmak, daha çok yer göstermek veya kullanıcıyı dolaştırmak değildir. Tanıdık ihtiyaca yeni bir karşılık bulmak yeterli olabilir.

Alternatifin neden farklı olduğu açıklanır: aynı amacı daha az ulaşım, farklı alan veya başka bir ödünle karşılayabilir. Yenilik, az bilinme ve fotojeniklik tek başına uygunluk nedeni değildir. Çeşitlilik ana amacı ve zorunlu koşulları aşamaz.

Keşif özgürlük taşır. Kullanıcı daha fazlasını isteyebilir, önceki seçimini reddedebilir veya bugün alışıldık bir yer seçebilir. Geçmiş tercihi değişmez kimlik haline getirilmez. Henüz amacı olmayan kişiye kullanım amaçları açık başlangıçlar sunulabilir; kişiselleştirme varmış gibi konuşulmaz.

**Sınama:** Kullanıcı yeni seçeneğin kendi ihtiyacıyla ilişkisini anlayabiliyor mu? Gezinti süresinin uzaması tek başına keşif başarısı değildir. Sürekli merak boşluğu, “gizli cevher” üstünlüğü ve kaçırma endişesi yaratılıyorsa tasarım dikkat tüketimine kaymıştır.

## 30. Şamandıra neden Apple gibi görünmemeli?

Apple'dan alınabilecek ders amaçlılık, kullanıcı iradesi, tutarlılık ve ayrıntı özenidir. Resmî tasarım ilkeleri de ürünün amacına hizmet etmeyi, geri dönebilmeyi ve farklı kullanım biçimlerini desteklemeyi vurgular. Bu, belirli bir yüzey estetiğinin bütün ürünler için doğru olduğu anlamına gelmez. [Apple — Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles).

Şamandıra'nın konusu dış dünyadaki değişken yerler, kişisel ihtiyaçlar ve sınırlı bilgidir. Ürün sunumu estetiğini taklit ederek her şeyi kusursuz ve kesin göstermek, bu belirsizliği görünmez kılabilir. Kullanıcı yerin gerçek koşulunu anlamak için gelmiştir; marka gösterisini izlemek zorunda değildir.

Apple gibi görünmeme ilkesi aşinalıktan vazgeçmek değildir. Tanınan etkileşim anlamları kullanılabilir. Kaçınılacak şey, başka bir ürünün görünümünü özenin kanıtı saymaktır.

**Karar:** Apple'dan işçiliğe ve kullanıcı kontrolüne verilen önem alınır; Şamandıra'nın kimliği gerçek yer anlatımı, somut ödünler ve gerektiğinde açıkça söylenen bilinmeyen üzerinden kurulur.

## 31. Şamandıra neden Google Maps gibi görünmemeli?

Şamandıra, tek bakışta kullanıcıya “önce haritayı çözmeliyim” görevi vermemelidir. Ürünün ana sorusu, seçeneklerin bu ihtiyaca neden uyduğu ve hangi koşulda uymadığıdır. Konum bu değerlendirmenin önemli bir girdisidir; bütün kararın kendisi değildir.

Bu ayrım Google Maps'in yalnız harita veya puan sunduğu iddiasına dayanmaz. Kabul edilmiş 03 §19 zaten doğal dille ihtiyaç anlama ve öneri yeteneklerini dikkate alır. Buradaki karar bir özellik karşılaştırması değil, Şamandıra'nın dikkat önceliğidir.

Harita yoğunluğunu ana zenginlik işareti yapmak, birbirinden farksız kayıtları çoğaltmak veya mesafeyi bütün uygunluğun yerine koymak tercih edilmez. Buna karşılık yer kimliğinin netliği, yön bulma sürekliliği ve açık adres bilgisi değerlidir.

**Karar:** Konumu açıklayan aşinalık alınır; harita merkezli ürün beklentisi kopyalanmaz. Kullanıcı haritayı açmadan gerekçeli bir yer seçebiliyorsa Şamandıra kendi görevini doğru kurmuştur.

## 32. Şamandıra neden Booking gibi görünmemeli?

Şamandıra'nın temel işi satın alma veya rezervasyon tamamlama değildir. Kullanıcı ücretsiz bir yer seçebilir, tek bir mola planlayabilir ya da gitmemeye karar verebilir. İşlem kapatmaya göre kurulmuş bir sunumu aynen almak, bu geçerli sonuçları geri plana itebilir.

Burada Booking'in her akışının belirli bir davranışı kullandığı ileri sürülmüyor. Reddedilen yaklaşım, **rezervasyon odaklı pazar yeri mantığının Şamandıra'nın amacı yerine geçirilmesidir**. Müsaitlik, fiyat ve işlem sonu başka bir ürün için merkezi olabilir; Şamandıra bunları yalnız kendi karar kapsamı içinde ele alır.

Kapsamı açık maliyet, kullanım koşulu ve karşılaştırılabilir bilgi yararlı derslerdir. Sahte aciliyet, belirsiz toplam, kalabalık satış mesajı, genel puanı uygunluk yerine koyma ve ücretli görünürlüğü organik öneri gibi sunma ise hiçbir kaynaktan alınamaz.

**Karar:** Pratik koşulları açıklama disiplini alınır. Kullanıcının daha fazla harcaması, kararın kalitesi gibi sunulmaz. Yol tarifi veya rota seçimi rezervasyon gerçekleşmiş hissi yaratamaz.

## 33. Şamandıra neden Airbnb gibi görünmemeli?

Şamandıra insanı ve yerin karakterini önemsemelidir. Ancak güzel bir hayatın vitrini gibi algılanmak, kullanıcının kendi ihtiyacını değerlendirmesinin önüne geçebilir. Fotojenik ve tüketilebilir deneyimler, gündelik, sade veya ücretsiz seçeneklere tasarım yoluyla üstünlük kazanmamalıdır.

Airbnb referansından bu belge için seçilen ders, yerin somutluğunu ve insani bağlamını kaybetmemektir. Bu bir kurumsal ilke alıntısı veya güncel bütün arayüzlerin değerlendirmesi değildir. Alınacak dersin Şamandıra'ya uyarlanması tasarım yorumudur.

Şamandıra'nın güveni ev sahibi kişiliğine, sosyal beğeniye veya etkileyici fotoğrafa devredilemez. Kişisel uygunluk dayanağı, önemli ödün ve bilgi sınırı görünür kalır. İyi bir yer anlatısı estetik beğeniyi tek seçim ölçütüne dönüştürmez.

**Karar:** İnsani yakınlık ve yere özgü anlatım korunur. Rezervasyon paketi, statü çağrışımı veya fotoğrafın bütün kararı sürüklediği vitrin mantığı devralınmaz. Karakter gerçek koşullardan gelir.

## 34. Rakiplerden hangi prensipleri almalı?

Aşağıdaki markalar aynı tür rakipler değildir; farklı sorumluluklar için düşünme referanslarıdır. Resmî kaynakla desteklenen gözlem ile Şamandıra için yaptığımız yorum ayrılmıştır. Hiçbir dış kaynak, kabul edilmiş sekiz belgeden daha yüksek otorite değildir.

| Referans | Alınacak düşünme disiplini | Şamandıra'da karşılığı | Aktarım sınırı |
|---|---|---|---|
| Apple Human Interface | Amaç, kullanıcı iradesi, aşinalık ve özen | Başlangıç kolaylığı, geri dönüş, anlamlı tutarlılık | Marka görünümü veya platform estetiği kopyalanmaz |
| Linear | Hız, odak ve ayrıntılı işçilik; kendi kalite anlatısının vurgusu | Tekrar işi azaltma, kararlı durum, kullanıcının son seçimini koruma | Uzman kullanıcı yoğunluğu ve kısayol bilgisi önkoşul olmaz |
| Stripe | Bağlam içinde yardım; tutarlılık ve erişilebilirlik uğruna ifade sınırı | İlgili kararda ilgili bilgi, açıklanmış işlem sonucu | Pazarlama görünümü veya finansal iş akışı alınmaz |
| Notion | İçeriğe alan açma ve aynı bilgiyi farklı biçimde kullanabilme | Yer bilgisinin taşınabilir anlamı; taslak ve kayıt üzerinde sahiplik | Kullanıcı kendi sistemini kurmak zorunda kalmaz |
| Airbnb | Bu belgeye özgü yorum: insani bağlam ve yerin somut karakteri | Gerçek ortam, anlaşılır ziyaret koşulu, yargılamayan dil | Fotojenikliği ve sosyal kanıtı uygunluk yerine koyma yok |
| A24 Art Direction | Bu belgeye özgü yorum: tek tipleştirmeyen editoryal bakış | Gerçek yerlerin ayırt edici ayrıntısını korumak | Sinematik gizem, geciktirme veya atmosfer uğruna okunmazlık yok |
| Dieter Rams | Yararlılık, anlaşılabilirlik, dürüstlük, kalıcılık ve gereksiz olanı azaltma | Her unsurun işe yarama gerekçesi; iddianın sınırını aşmama | “Az tasarım” bilgiyi ve kontrolü eksiltme izni değildir |
| Google Maps | Bu ürün için seçilen ders: mekânsal süreklilik | Adres, seçili yer ve yol tarifinden dönüşün açıklığı | Harita veya yakınlık tek karar otoritesi olmaz |
| Booking | Bu ürün için seçilen ders: karar koşullarını karşılaştırılabilir kılma | Maliyetin kapsamı ve ziyaret şartlarının açıklığı | Rezervasyon dönüşümü Şamandıra'nın başarı ölçüsü olmaz |

Linear'ın kendi anlatısı hız, odak ve küçük ayrıntılara verilen önemi birlikte vurgular. Stripe Apps rehberi bağlam içindeki yardımı, tutarlılığı ve erişilebilirliği koruyan sınırları açıklar. Notion'ın rehberi içerik ve farklı bilgi görünümlerinin esnekliğini anlatır. Bunlardan çıkarılan Şamandıra kararları tabloda belirtilen uyarlamalardır. [Linear — Careers](https://linear.app/careers), [Stripe — Design your app](https://docs.stripe.com/stripe-apps/design), [Notion — A designer's ultimate guide](https://www.notion.com/help/guides/a-designers-ultimate-guide-to-using-notion).

Rams'ın on ilkesi bu belgenin on yasasının aynen aktarımı değildir. Yararlılık, dürüstlük, anlaşılabilirlik ve gereksiz olanı azaltma yönü alınmış; Şamandıra'nın kanıt, bağlam ve irade sorumluluğuna uyarlanmıştır. [Vitsœ — Good design](https://www.vitsoe.com/us/about/good-design).

**Aktarım testi:** Markanın adı çıkarıldığında ilke hâlâ kullanıcı sorununu açıklıyorsa kullanılabilir. “O ekip böyle yapıyor” tek başına gerekçe değildir.

## 35. Hangilerini kesinlikle almamalı?

Aşağıdaki yasaklar herhangi bir markanın bütün davranışlarına ilişkin suçlama değildir. Şamandıra'nın temel sözüyle bağdaşmayan tasarım yaklaşımlarını tanımlar.

| Alınmayacak yaklaşım | Neden reddedilir? |
|---|---|
| Genel yıldız, uygunluk yüzdesi veya yer güven rozeti | Farklı amaçları ve kritik bilinmeyenleri tek hükme eritir |
| Ham yorum, yorumcu ve yorum hacmiyle ikna | Kullanıcıya yorum çözümleme yükünü geri verir; kabul edilmiş yayın sınırını aşar |
| Fotojenik veya pahalı yere görsel üstünlük | Sunumun gizli uygunluk motoru olmasına yol açar |
| Sonsuz keşif, tamamlanacak koleksiyon ve ziyaret serisi | Dikkat tüketimini ve daha çok geziyi amaç haline getirir |
| Sahte kıtlık, baskılı teklif ve emeğin ardından ödeme | Kullanıcının kararını korku veya batık emekle yönlendirir |
| Ücretsiz deneyimde eksik güven, uyarı veya kontrol | Temel ürün sözünü ticari ayrıcalığa dönüştürür |
| AI gösterisi ve sahte ilerleme | Gerçek iş durumunu ve bilgi sınırını gizler |
| Sinematik belirsizlik veya yalnız estetik ikonografi | Yön bulmayı ve anlamayı performansa dönüştürür |
| Her özelliği görünür kılan uzman çalışma alanı | Küçük yer kararını sistem yönetimine büyütür |
| Tamamen boş başlangıç ve görünmez kontroller | Sadeliğin maliyetini kullanıcıya aktarır |
| Zorunlu üyelik, konum, profil veya katkı | İlk faydayı izin ve emek koşuluna bağlar |
| Varsayılan dış paylaşım, özel bilgili önizleme | Kontrol ve gizliliği sunum kolaylığına feda eder |
| Hareket, sürükleme, renk veya haritayı tek yol yapmak | Eşdeğer karar hakkını engeller |
| Kısalık adına engel ve kapsam silmek | İddianın anlamını değiştirir |

Bu yasaklar yüksek tıklama, beğeni veya gelir beklentisiyle geçersizleşmez. Bir uygulama detayı hakkında belirsizlik varsa yalnız görsel benzerlik üzerinden hüküm verilmez; kullanıcıya hangi anlamı taşıdığı incelenir.

## 36. Şamandıra'nın 10 tasarım yasası

Bu yasalar sonraki tasarım kararlarını değerlendirmek için yazılmıştır. Kullanıcı kabulü bekleyen bu belgenin önerdiği anayasal çerçevedir; önceki referansları değiştirmez.

| No | Tasarım yasası | Bağlayıcı sonuç | İhlal örneği |
|---|---|---|---|
| 1 | **Önce kullanıcının bu anki kararı.** | Her tercih belirli bir amaç, bağlam ve belirsizliğe hizmet eder | Sohbet yeri arayana zorunlu günlük plan açmak |
| 2 | **Gerekçe, önemli ödün ve kritik sınır ayrılmaz.** | Kullanıcı olumlu iddiayı sınırından bağımsız tüketmeye zorlanmaz | Akşam bilgisizliğini ayrıntıya saklamak |
| 3 | **Görünüm kanıttan daha kesin konuşamaz.** | Metin, görsel, ikon ve hareket aynı bilgi sınırını taşır | Taslak rotayı doğrulanmış güzergâh gibi sunmak |
| 4 | **Azaltılan içerik, karar hakkını azaltamaz.** | Sadelik tekrar ve ilgisiz yükü kaldırır; gerekli açıklama ve kontrol kalır | Geri alma veya engel bilgisini kaldırmak |
| 5 | **Kullanıcının güncel seçimi korunur.** | Geri dönüş, düzenleme, kesinti ve geç yanıt bağlamı ezmez | Yeni bütçenin üstüne eski aramayı getirmek |
| 6 | **Her öneri farkıyla anlam kazanır.** | Alternatif, aynı amacı hangi başka ödünle karşıladığını anlatır | Üç benzer kartı yalnız sayı dolsun diye sunmak |
| 7 | **Aynı karar hakkı her kullanım biçiminde vardır.** | Metin, mobil, klavye, yardımcı teknoloji ve azaltılmış hareket eşdeğerdir | Haritasız veya sürüklemesiz düzenleyememek |
| 8 | **Özen herkesin temel standardıdır.** | Ücretsiz kullanıcı aynı doğruluk, erişim ve temel kontrolü alır | Kritik koşulu Premium ayrıntısı yapmak |
| 9 | **Her durum gerçekleştiği kadar anlatılır.** | Bekleme, kayıt, doğrulama, paylaşım ve ziyaret ayrı kalır | Katkı alındığında bilgi güncellendi demek |
| 10 | **Kullanıcının zamanı kendisine aittir.** | Seçmeme, daha az durak, boş zaman, reddetme ve çıkış meşrudur | Karardan sonra sonsuz öneri veya zorunlu kutlama |

Bir yasa diğerini ihlal ederek sağlanamaz. Örneğin hızlı karar için kritik bilgi gizlenmez; bağlamı korumak için geri çekilmiş yanlış bilgi canlı tutulmaz. Çatışma §0.2'deki önceliklerle çözülür ve gerekçesi kaydedilir.

## 37. Tasarım kararları nasıl değerlendirilecek?

Anayasa bir zevk hakemliği veya her küçük iş için uzun onay süreci değildir. Tasarımcıdan beklenen, önemli bir tercihin hangi kullanıcı sorununu çözdüğünü ve hangi ilkeyi nasıl koruduğunu açıklamasıdır. Kararın ölçeği kadar gerekçe yeterlidir.

### 37.1. Karar kaydı

Sonraki çalışmalarda tartışmalı bir tasarım kararı için şu bilgiler yeterli açıklıkta kaydedilir:

1. Kullanıcının amacı, bağlamı ve zorunlu sınırı.
2. Azaltılmak istenen belirsizlik veya tekrar işi.
3. Dayanılan kabul edilmiş belge ve bu belgedeki ilgili yasa.
4. Seçilen yaklaşım ve elenen gerçek alternatif.
5. Kullanıcının anlayacağı anlam, kontrol ve çıkış.
6. Yanlış anlama riski, sınama yöntemi ve hangi bulguda değiştirileceği.

Her tercih için yeni belge, komite veya kullanıcı onayı gerekmez. Fakat bir ilkeyi ihlal eden yüksek dönüşüm oranı kabul gerekçesi yapılamaz. Ürün kapsamını değiştiren bir tercih tasarım detayı gibi geçirilmez.

### 37.2. Gözlenebilir değerlendirme soruları

| Sınanacak boyut | Görevde aranacak kanıt | Tek başına yeterli olmayan gösterge |
|---|---|---|
| İlk yön bulma | Kullanıcı nereden başlayacağını ve kapsamı açıklayabilir | İlk görüntüyü beğenme |
| Karar açıklığı | Seçme nedeni, önemli ödün ve bilinmeyeni kendi sözleriyle ayırır | Bir yere tıklama |
| Zorunlu koşul | Bilinmeyeni karşılanmış saymaz; engeli fark eder | Uyarının bir yerde bulunması |
| Kontrol | Tek koşulu düzeltir, öneriyi reddeder, geri alır ve çıkabilir | Eylem adlarının listelenmesi |
| Süreklilik | Kesinti ve geri dönüşte aynı işi yeniden kurmaz | Yalnız sorunsuz ana akış |
| Eşdeğerlik | Görselsiz, haritasız, klavyeyle ve büyütülmüş metinle karar verir | Standart ekranda güzel görünüm |
| Güvenin ölçülülüğü | Programı canlı durumdan; kaydı doğrulamadan ayırır | Ürünü güvenilir bulduğunu söyleme |
| Keşif | Yeni seçeneğin kendi amacıyla farkını açıklar | Daha çok içerik açma |
| Gerçek hayat karşılığı | Gönüllü geri bildirimde beklenti ve yaşanan koşul karşılaştırılır | Ziyaret veya durak sayısı |

İlk ve tekrar kullanıcılar, farklı okuma ve dijital deneyim düzeyleri, mobil/masaüstü ve yardımcı teknoloji kullanım biçimleri dikkate alınır. Az verili yer, görselsiz sonuç, çok uzun yer adı, bilinmeyen fiyat, kritik erişim açığı, yavaş bağlantı ve kapalı paylaşım gibi durumlar yalnız sorunsuz örneklerin dışında özellikle incelenir.

Araştırmada yalnız tamamlayanlar dinlenmez; vazgeçen, anlamayan ve sonuç bulamayan kişiler de mümkün olduğunca kapsanır. Gönüllü geri bildirimin yanlılığı açık tutulur. Sayısal başarı eşiği, süre vaadi veya katılımcı sonucu bu belgede icat edilmez; araştırma öncesinde ilgili görev için tanımlanır.

### 37.3. Hangi bulguda durulur, hangisinde iyileştirilir?

Kritik bilinmeyenin karşılanmış sanılması, özel bilginin istenmeden açılması, temel kontrolün erişilememesi veya ticari avantajın uygunluk gibi anlaşılması ilgili yaklaşımın ilerlemesini durdurur. Önce sorun giderilir.

Daha uzun okuma, düşük görsel beğeni veya daha az tıklama tek başına ret sebebi değildir. Gerekçeli karar daha anlaşılır hale geliyorsa bu bedel kabul edilebilir; karar kalitesini artırmıyorsa anlatım ve görev yükü azaltılır. Gereksiz susma ve boş sonuç da ölçülür: hiç öneri vermemek otomatik doğruluk başarısı değildir.

## 38. Öz eleştiri — 48 itiraz, düzeltme ve açık sınama

Bu eleştiriler yalnız kötü uygulama ihtimalleri değildir. Bazıları seçilen yaklaşımın doğal maliyetidir. Düzeltmeler ilgili bölümlere işlenmiştir; araştırma gerektiren noktalar çözülmüş gibi sunulmamıştır.

| No | Kendi yaklaşımıma itiraz | Gerçek risk | Nihai düzeltme / açık sınama |
|---|---|---|---|
| 1 | “Sakin rehberlik” fazla soyut bir tasarım yönü olabilir | Farklı tasarımcılar aynı sözle zıt kararlar savunur | §1 ve §37: her tercih için belirli karar farkı ve gözlenebilir kullanıcı sonucu istenir |
| 2 | “Doğru yer” paternalist bir vaat olabilir | Sistem kullanıcının nasıl yaşaması gerektiğine karar verir | §1, §14: doğruluğu güncel açık ihtiyaç tanımlar; bilinmeyen niyet tamamlanmaz |
| 3 | En kısa yol hız baskısına dönüşebilir | Kullanıcı önemli koşulu okumadan ilerler | Giriş, §8–9: hız toplam çaba olarak tanımlanır; kritik anlam kısaltılamaz |
| 4 | Dürüstlük adına çok fazla belirsizlik gösterilebilir | Kullanıcı yeniden araştırmacıya dönüşür | §8, §28: yalnız bu kararın gerekli sınırları öne çıkar; ilgisiz eksiklikler yüklenmez |
| 5 | Temkinli yaklaşım hiçbir şey önermemeye dönüşebilir | Sistem yanlışsız görünür ama fayda üretmez | §6, §37: dar dayanaklı öneri korunur; gereksiz susma ayrıca ölçülür |
| 6 | Önemli ödünü erken anlatmak kararı zorlaştırabilir | Kullanıcı iyi seçenekleri de baştan reddeder | §9, §28: ödün somut ve orantılı anlatılır; saklanmaz, anlaşılması sınanır |
| 7 | “Önemli bilgi” kararı ekibin zevkine kalabilir | Tasarımcı kendi ihtiyacını herkesinki sanır | §0, §9: açık koşul ve karar dayanağı esastır; önem bağlamla gerekçelendirilir |
| 8 | Premium his sınıfsal çağrışım taşıyabilir | Ücretsiz veya gündelik yerler değersizleşir | §4: premium his özen olarak tanımlanır; bütçe ve yer türü boyunca eşitlik sınanır |
| 9 | Ücretli Premium ile premium his yine karışabilir | Kullanıcı doğruluğun satın alındığını düşünür | §4, §27: temel standart ve ek kolaylık ayrılır; açılmamış özellik vaat edilmez |
| 10 | Minimalizm kontrolleri görünmez yapabilir | Ret, daha fazla sonuç ve kayıtlara dönüş bulunamaz | §5, §13: bulunabilirlik estetik sadeliğin şartıdır; kaybolan kontrol geri getirilir |
| 11 | Yeterli zenginlik ilkesi her şeyi eklemeye izin verebilir | Minimal yaklaşım kapsam genişlemesiyle aşınır | §6, §37: her ayrıntı karar farkını açıklamalı; ilgisiz özellik eklenmez |
| 12 | Boşluk kalite işareti olarak aşırı kullanılabilir | Karşılaştırılan bilgiler uzaklaşır, kaydırma artar | §7: bilgi ilişkisi ve hafıza yükü esas alınır; boşluk gerektiğinde azaltılır |
| 13 | Yoğunluğu azaltmak daha çok açma eylemi yaratabilir | Kısa metin toplam görevi uzatır | §8: toplam okuma/açma/geri dönme yükü birlikte gözlenir |
| 14 | Sabit bilgi sırası herkese aynı önceliği dayatabilir | Kullanıcının belirleyici koşulu geride kalır | §9: anlam iskeleti sabit; vurgu açık ihtiyaca göre değişir |
| 15 | Bağlama göre vurgu yön bulmayı bozabilir | Her sorgu başka düzene dönüşür | §9–10: kimlik ve devam ilişkileri tutarlı kalır; vurgu bütün düzeni oynatmaz |
| 16 | Bir baskın CTA manipülatif olabilir | Alternatif görünür olduğu halde fiilen seçilemez olur | §27: reddetme/düzeltme bulunabilirliği görevle sınanır; sadece varlığı yetmez |
| 17 | Az seçenek kullanıcının ufkunu daraltabilir | İlk küme bütün olasılıklar gibi anlaşılır | §8, §12: kapsam ve açık daha fazla yolu korunur; kümenin son olmadığı anlaşılmalıdır |
| 18 | Ortak kart mantığı yerleri tek tipleştirebilir | Kıyı, müze ve kafe aynı övgü diline sıkışır | §11, §16: ortak karar ölçütleri kalır; gerçek fark ve ilgili içerik değişebilir |
| 19 | Uzun kritik bilgi kartı ağırlaştırabilir | Kullanıcı bütün koşulları okumaz | §8–11: olumlu tekrar azalır; gerekli sınır korunur; alternatif sunum biçimi değerlendirilebilir |
| 20 | Bilinmeyen adayın görünürlüğü yanlış anlaşılabilir | Bulunan yer uygun öneri sanılır | §11, §14: bulma/öneri/taslak anlamları ayrı; uyarı bilinmeyeni eşleşmeye sokamaz |
| 21 | Liste ortaklığı genel sıralama hissi yaratabilir | İlk sıradaki yer evrensel olarak en iyi sanılır | §12: sorgu ve farklar açık; sıra numarası veya üstünlük dili gerekçe yerine geçmez |
| 22 | Kayıt türlerinin ayrımı öğrenme yükü doğurabilir | Gezeceğim, Gezdiğim ve rota birbirine karışır | §12–13: türler niyet/beyan/gün olarak anlatılır; biri diğerini otomatik üretmez |
| 23 | Yeni portal açmamak erişimi zorlaştırabilir | Kayıtlı işe dönmek uzun hale gelir | §13: mevcut Kaydettiklerin yolu görünür ve doğrudan olur; sorun önce mevcut yapı içinde çözülür |
| 24 | Doğal dil rahatlığı olduğundan fazla vaat yaratabilir | Kullanıcı her ihtiyacın anlaşıldığını sanır | §14: anlaşılan ve anlaşılmayan görünür; adla/açık seçimle alternatif giriş korunur |
| 25 | Netleştirmeyi azaltmak yanlış varsayımı artırabilir | Az soru uğruna kritik eksik kapanmış sayılır | §14–15: soru sayısı kota değildir; cevabı kararı değiştiren eksik sorulur |
| 26 | Tercih ile zorunlu koşul ayrımı zor olabilir | Kullanıcı hangi seçimin telafi edilemez olduğunu anlamaz | §15: gerçek sonuç üzerinden anlaşılabilirlik sınanır; ürün kendi başına sınıf atamaz |
| 27 | Çok kararlı filtre mantığı boş sonuçları artırabilir | Özellikle bilgi azlığında kullanıcı sıkışır | §24: bilgi açığı ve uyuşmazlık ayrılır; taslak korunur; sınır habersiz gevşetilmez |
| 28 | Görselleri ikincil görmek yerin karakterini kurutabilir | Ürün soğuk bir bilgi kataloğuna dönüşür | §16–17: gerçek ortam ve tanınma görselin meşru işleridir; tamamen kaldırılmaz |
| 29 | Fotoğraf kalitesi gizli sıralama etkisi yaratabilir | İyi fotoğraflanmış işletmeler üstün algılanır | §11, §17: fotoğrafsız yeterli yerlerle karşılaştırma sınanır; medya uygunluğu değiştiremez |
| 30 | Dürüst fotoğraf seçimi de taraflı olabilir | “Olağan an” editörün sezgisiyle seçilir | §17: kapsamı bilinmeyen kareden genelleme yapılmaz; temsil iddiası dar tutulur |
| 31 | Görsel kanıtı sınırlamak yararlı ayrıntıyı dışlayabilir | Gerçek basamak veya bölüm bilgisi kaybolur | §16–17: görüntü somut kapsamı için kullanılabilir; görünmeyen yol hakkında sonuç üretemez |
| 32 | Haritayı yardımcı tutmak mekânsal düşüneni yavaşlatabilir | Kullanıcı metinden konumu yeniden kurar | §18: harita isteğe bağlı ve kullanılabilir kalır; önemsizleştirilmez |
| 33 | Harita ile metin eşdeğerliği zor olabilir | Yakınlık ve geçiş yükü metinde eksik kalır | §18, §37: aynı kararın süre, kapsam ve önemli bağlantı koşullarıyla tamamlanması sınanır |
| 34 | İkon açıklamaları kalabalık yaratabilir | Her işaret gereksiz tekrar cümlesine dönüşür | §19: anlamı belirsiz/temel işlerde açıklama korunur; dekoratif tekrar azaltılır |
| 35 | İllüstrasyonu sınırlamak sıcaklığı azaltabilir | Ürün mekanik hissedilir | §20: yargılamayan dil ve gerçek yardım sıcaklığı taşır; anlam katkılı illüstrasyon mümkündür |
| 36 | Animasyon kısıtı sürekliliği zayıflatabilir | Sıra değişimi ani ve anlaşılmaz gelir | §21: işlevli hareket yasak değildir; metinsel fark ve odakla birlikte sınanır |
| 37 | Hareketsiz eşdeğer de gereğinden çok mesaj üretebilir | Yardımcı teknoloji kullanıcısı sürekli bölünür | §21–23: gerekli değişiklik kısa duyurulur; her ara durum tekrar edilmez |
| 38 | Gerçek başarıyı beklemek sistemi yavaş hissettirebilir | Kullanıcı eylemin alınmadığını sanır | §22–23: anlık algılandı bilgisi ile gerçek tamamlanma ayrı sunulur |
| 39 | İptal yolu işlem sonucu hakkında belirsizlik yaratabilir | Kullanıcı beklemeyi bıraktığında kaydın da iptal olduğunu sanır | §23, §25: beklemeyi bırakma ve işlemin gerçekleşmiş olma durumu kapsamıyla açıklanır |
| 40 | Boş durum ayrımları fazla terim gerektirebilir | Kullanıcı sistem durumlarını öğrenmek zorunda kalır | §24: iç durum adı yerine kendi kararına etkisi ve devam yolu anlatılır |
| 41 | Yerel hata yaklaşımı genel sorunu gizleyebilir | Kullanıcı listenin de güncel olmadığını fark etmez | §25: etkilenen bütün iddiaların sınırı açık; yalnız sağlam kalan iş devam eder |
| 42 | Kutlamasız başarı soğuk hissedilebilir | Emeğin karşılığı görünmez kalır | §26: kısa, sıcak ve gerçek sonuç bilgisi korunur; tören veya yeni görev gerekmez |
| 43 | Güvenin sınırlarını anlatmak ürün güvenini düşürebilir | Kullanıcı sürekli kuşku duyar | §28: hedef yüksek güven değil ölçülü güven; somut kapsam ve düzeltilebilirlik sınanır |
| 44 | Keşfi amaca bağlamak sürprizi azaltabilir | Kullanıcı yalnız zaten bildiği ihtiyaçların çevresinde kalır | §29: belirsiz amaçla başlangıç ve benzer uygunlukta yeni farklar korunur; rastgelelik dayatılmaz |
| 45 | Paylaşımda gizlilik ile açıklık çatışabilir | Özel koşul silinirken olumlu rota hükmü kalır | §0, §16, §26: kişisiz sınır anlatılır; taşınamıyorsa olumlu iddia da daralır |
| 46 | Marka referansları yine taklide dönüşebilir | İlkeler gerekçesiz estetik otorite olur | §30–35: kaynak ve yorum ayrılır; marka adı çıkarılarak aktarım testi yapılır |
| 47 | Gerçek hayat başarısını ölçmek zor ve yanlı olabilir | Yalnız cevap verenler dinlenir; erken çıkış başarı sayılır | §3, §37: davranış, bağımsız inceleme ve gönüllü karşılık birlikte değerlendirilir; sessizlikten sonuç yok |
| 48 | Anayasanın ayrıntısı tasarım bürokrasisi yaratabilir | Her küçük düzenleme için uzun savunma gerekir | §37: kaydın boyutu kararın etkisine göre olur; yasalar kısa kontrol, bölümler ihtiyaçta derinlik sağlar |

Bu itirazların ortak sonucu şudur: daha az içerik, daha az hareket veya daha fazla açıklama kendi başına doğru değildir. Doğru olan, kabul edilmiş sınırları korurken kullanıcının belirli kararı daha iyi anlamasını sağlayan tercihtir. Öz eleştiri bu sınırları yumuşatmaz; uygulama alanlarını netleştirir.

## 39. Alternatif tasarım yaklaşımları ve tercih gerekçesi

Aşağıdaki seçenekler ekrana veya stile dönüştürülmüş tasarımlar değildir. Ürünün dikkatini, bilgisini ve kullanıcıyla ilişkisini nasıl örgütleyeceğine dair alternatif felsefelerdir.

| Yaklaşım | Güçlü olduğu durum | Şamandıra için temel bedel | Nihai değerlendirme |
|---|---|---|---|
| Radikal minimalizm | Tek, iyi bilinen ve az belirsiz işlem | Ödün, bilgi sınırı ve alternatif kontrolü görünmezleşebilir | Bütün ürünün temeli olamaz; yalnız açık küçük görevlerin yalınlığı alınır |
| Harita merkezli keşif | Konum ve mekânsal ilişki kararı baskınsa | Kullanıcı uygunluğu harita işaretlerinden çıkarmak zorunda kalır | İsteğe bağlı yardımcı görünüm olarak değerli; ana felsefe değil |
| Editoryal seyahat dergisi | Yerle duygusal bağ kurma ve serbest okuma | Anlatıcının zevki kullanıcının ihtiyacını aşabilir; okuma uzar | Yer karakterine katkısı alınır; kararın önüne uzun anlatı konmaz |
| Rezervasyon/pazar yeri yaklaşımı | Belirli bir işlemi koşullarıyla tamamlamak | Gitmeme, ücretsiz seçim ve küçük gündelik kararlar geri plana düşer | Temel model seçilmez; pratik koşul açıklığı alınır |
| Her şeyi konuşarak çözen AI danışmanı | Kullanıcının ihtiyacı ilk anda belirsizse | Karşılaştırma konuşma hafızasına yüklenir; akıcılık sahte otorite yaratabilir | Niyet girişine yardımcı olabilir; bütün deneyim sohbet zorunluluğu değildir |
| Yoğun uzman çalışma alanı | Sık ve karmaşık plan yöneten kişi | İlk kullanıcıya araç ve görünüm yönetimi yükler | İsteğe bağlı derinlik dersi alınır; temel yer seçimi uzmanlık istemez |
| Tamamen nötr bilgi kataloğu | Olguları sade biçimde taramak | Bilginin ihtiyaca göre anlamını kullanıcı üretir; yer karakteri kaybolur | Güvenilir olgu disiplini alınır; uygunluk açıklamasının yerine geçmez |
| Eğlence ve oyunlaştırma | Amaç bizzat oyuna katılmaksa | Geziyi tamamlanacak seri, katkıyı borç, keşfi dikkat yarışına çevirir | Şamandıra'nın çekirdeğinde reddedilir |
| Amaç, kanıt ve kullanıcı iradesine dayanan sakin rehberlik | Küçük veya değişken yer kararında yeterli açıklık arayan kişi | İçerik seçimi disiplin ister; aşırı temkin veya aşırı sadeleşme riski sürer | Seçilen yaklaşım; §38'deki sınamalarla denetlenir |

### 39.1. Neden bu yaklaşım seçildi?

Şamandıra'nın varlık nedeni yer envanterini sergilemek, gezi içeriği tüketimini büyütmek veya kullanıcının gününü doldurmak değildir. Kabul edilmiş belgeler, **yer ile bu ihtiyacın ilişkisini açıklama sorumluluğunu** ürüne verir. Seçilen yaklaşım bu sorumluluğu doğrudan taşır.

Üç ihtiyacı birlikte karşılar. İlk olarak kullanıcı az ama gerekçeli seçenekle başlayabilir. İkinci olarak kararın önemli koşulu ve belirsizliği sonradan ortaya çıkmaz. Üçüncü olarak kullanıcı daha derine bakabilir, değiştirebilir veya durabilir. Diğer yaklaşımlar bu ihtiyaçların birinde güçlü olsalar da tek başlarına üçünü aynı öncelikte tutmaz.

Seçim ortalama bir tarz karışımı değildir. Harita mekânsal soru için; editoryal yaklaşım gerçek karakter için; konuşma belirsiz niyeti anlamak için kullanılabilir. Hepsi aynı karar sorumluluğuna bağlıdır. Bir aracın yararlı olması ayrı ürün merkezine dönüşmesini gerektirmez.

### 39.2. Kabul edilen bedeller

Bu yaklaşım ilk bakışta daha gösterişli bir seçenekten daha az çarpıcı görünebilir. Bazı kararlar daha uzun açıklama isteyebilir. Bilgi azlığında sonuç kümesi küçük kalabilir. İçerik üretimi ve değerlendirme disiplini gerektirir.

Bu bedeller peşinen başarı sayılmaz. Kullanıcı seçenek farkını anlamıyorsa, sürekli boş sonuçla kalıyorsa veya kontrolleri bulamıyorsa yaklaşımın sunumu iyileştirilir. Kanıtsız güvenceyi artırmak, kontrolü kaldırmak ve ticari baskı eklemek iyileştirme seçenekleri değildir.

### 39.3. Hangi koşulda yeniden düşünülür?

Harita olmadan mekânsal yükün sürekli yanlış anlaşıldığı görülürse ilgili görevde haritanın ağırlığı artabilir. Az içerik yanlış yoruma yol açıyorsa açıklama genişleyebilir. Yoğun karşılaştırma tekrarlanan bir ihtiyacı daha az çabayla karşılıyorsa mevcut bağlam içinde derinlik kazanabilir. Hareket gerçekten ilişkiyi anlamayı iyileştiriyorsa sınırlı biçimde kullanılabilir.

Bunlar ilkenin terk edilmesi değil aynı görevin daha iyi karşılanmasıdır. Yeni sayfa ailesi, temel kavram veya ticari hak değişikliği gerekiyorsa ilgili kabul edilmiş referans için açık değerlendirme gerekir; bu belge sessiz izin vermez.

## 40. Nihai Tasarım İlkeleri — öz eleştiri sonrası karar

**Şamandıra, insanın kendisi için doğru olan yeri anlayarak seçmesini sağlayan; açık, özenli ve yere özgü bir karar deneyimi kuracaktır.** Tasarımın karakteri sakin güven, somut anlatım ve gerçek kullanıcı kontrolünden doğacaktır. Ne kullanıcının zevkini belirleyecek ne de bilinmeyeni görünüşle kapatacaktır.

Bu bölüm önceki bölümlerden bağımsız ikinci bir yaklaşım değildir. §38'deki itirazlar ve §39'daki alternatifler değerlendirildikten sonra savunulan tek nihai yönü sabitler.

### 40.1. Deneyimin değişmez sözleri

- **Başlamak kolaydır.** Kullanıcı adıyla, ihtiyacıyla veya eksik bir fikirle başlayabilir. İlk yardım için hesap, izin, profil veya uzun hazırlık gerekmez.
- **Karar birlikte anlatılır.** Gerekçe, önemli ödün ve gerekli bilinmeyen aynı anlam bütünüdür. Sadeleşme bunları ayıramaz.
- **Güvence dayanağı aşmaz.** Olgu, çıkarım, tahmin, taslak ve kayıt kendi kapsamıyla görünür. Görsel veya hareket metnin söyleyemediği garantiyi veremez.
- **Karşılaştırma anlamlıdır.** Seçenekler gerçek farklarını taşır. İlk küme sınırlıdır; kapsamı ve daha fazlasını isteme yolu anlaşılır.
- **Seçim kullanıcıda kalır.** Koşullar sessizce gevşetilmez. Reddetmek, düzeltmek ve geri almak kolaydır. Son seçim geç yanıt veya görünüm değişimiyle ezilmez.
- **Özen herkes içindir.** Ücretsiz kullanım, düşük bağlantı ve yardımcı teknoloji aynı temel karar hakkını taşır. Ücretli kolaylık daha doğru bilgi satın aldıramaz.
- **Yer kendi gerçeğiyle anlatılır.** Fotoğraf ve editoryal seçim tanınmayı ve karakteri destekler. Pahalı, popüler veya fotojenik olma üstünlük değildir.
- **Araç amaca bağlıdır.** Harita, liste, kart, ikon, illüstrasyon ve animasyon bir sorunu çözdükleri ölçüde vardır. Hiçbiri kendi başına ürünün merkezi veya kalite kanıtı değildir.
- **Sorun da özenle karşılanır.** Boş sonuç, bilgi açığı, hata, bekleme ve çevrimdışı durum ayrı anlam taşır. Kalan iş ve gerçek kurtarma yolu anlaşılırdır.
- **Durabilmek tamamlanmış deneyimdir.** Kullanıcı yeterince bildiğinde ayrılabilir. Tek yer, boş zaman veya vazgeçme tasarım tarafından eksiklik sayılmaz; ölçümde otomatik memnuniyet de sayılmaz.

### 40.2. Nihai tasarım kararının kabul ölçütü

Bir tasarım kararı ancak şu soruların birlikte karşılandığı durumda bu anayasayla uyumludur:

1. Belirli bir kullanıcı kararına hizmet ediyor mu?
2. Önceki sekiz referansın anlamını ve kapsamını koruyor mu?
3. Kritik koşul ve bilinmeyen karar anında anlaşılabiliyor mu?
4. Kullanıcı öneriyi düzeltebiliyor, reddedebiliyor ve bağlamını kaybetmeden çıkabiliyor mu?
5. Aynı karar görselsiz, haritasız, klavyeyle ve hareket azaltıldığında da verilebiliyor mu?
6. Daha fazla ilgi yerine daha iyi anlama veya daha az tekrar işi sağladığı gösterilebiliyor mu?
7. Hangi kullanıcı bulgusunda değiştirileceği açık mı?

Bu sorular bir görsel beğeni puanına çevrilmez. Kritik anlam kaybı diğer olumlu özelliklerle telafi edilemez. Uyumlu ama faydası belirsiz bir tercih sınanabilir; açık ihlal kullanıcı deneyiyle meşrulaştırılamaz.

### 40.3. Tasarımın nihai tanımı

Şamandıra'nın minimalizmi gerekli olanı bulma disiplinidir. Zenginliği yerin gerçeğini ve kararın anlamını taşıma sorumluluğudur. Premium hissi tutarlı özendir. Keşfi kullanıcıya ait yeni olasılıktır. Güveni, bildiği kadar konuşması ve yanlışını düzeltebilmesidir.

> **İnsanlara en iyi yeri göstermeye çalışmaz.  
> Kendileri için doğru olan yeri  
> en kısa yoldan bulmalarını sağlar.**

Tasarımın görevi bu cümleyi görünüşe çevirmekten önce, her karar anında doğru kalmasını sağlamaktır.

## Bu dokümanın bağlı olduğu belgeler

- [00 Ürün Felsefesi](../00-product/00-urun-felsefesi.md)
- [01 Bilgi Mimarisi](../00-product/01-bilgi-mimarisi.md)
- [02 Product Language](../00-product/02-product-language.md)
- [03 Karar Motoru](../00-product/03-karar-motoru.md)
- [04 Sistem Mimarisi](../00-product/04-sistem-mimarisi.md)
- [05 AI Bilgi Motoru](../04-ai/05-ai-bilgi-motoru.md)
- [06 Akıllı Rota Motoru](../00-product/06-akilli-rota-motoru.md)
- [07 UX Karar Akışları](../02-ux/07-ux-karar-akislari.md)

Sekiz dosyanın kabulü bu görevdeki kullanıcı beyanına dayanır; dosyalar değiştirilmemiştir. Dış tasarım kaynakları bağlayıcı ürün referansı değildir; §30 ve §34'te belirtilen düşünme desteğidir.

## Bu dokümanın etkilediği belgeler

Aşağıdakiler **planlanan çalışmalardır; bu görevde oluşturulmamıştır**:

- 01-research altında UX Kullanıcı Doğrulama Planı: §37'deki ölçütleri ve §38'de açık kalan varsayımları 07'nin senaryolarıyla birlikte sınar.
- 03-design altındaki sonraki içerik ve tasarım çalışmaları: §36'daki on yasayı ve §40'taki nihai ilkeleri karar sınırı olarak kullanır.
- 06-frontend altında Web ve Mobil Davranış belgeleri: anlam, odak, geri dönüş, kesinti ve eşdeğer karar hakkını korur.
- 08-admin altında Bilgi Düzeltme ve Destek Deneyimi: alındı, incelendi, düzeltildi ve geri çekildi ayrımlarının iletişimini korur.
- 09-business altında Premium Değer ve Davet Politikası: temel özen standardını değiştirmeden ek kolaylığı değerlendirir.

Bu etkiler kabul edilmiş belgelerin değiştirildiği, yeni özelliklerin açıldığı veya sonraki uygulama işlerinin bu görevde yapıldığı anlamına gelmez.

## Bundan sonra okunması gereken belge

**UX Kullanıcı Doğrulama Planı**, docs/01-research altında planlanmaktadır; henüz mevcut değildir. 07 UX Karar Akışları ile bu belgedeki tasarım varsayımlarını birlikte sınamalıdır. Öncelik, gerekçe–ödün–bilinmeyen ayrımının anlaşılması, kayıt–uygunluk ayrımı, filtre kontrolü, karardan sonra baskısız çıkış ve farklı kullanım biçimlerinde eşdeğer görev tamamlamadır.

Ayrıca önceki belgelerde planlanan **05 Kanıt, Güncellik ve Yayın Politikası** çalışmasının konumu docs/04-ai/05-kanit-guncellik-yayin-politikasi.md olarak korunur. Henüz mevcut değildir; bu anayasa onun kanıt ve yayın eşiklerini belirlemez.

Güncel sıra ve durum için [Dokümantasyon dizini](../README.md).
