---
title: "03 Karar Motoru"
version: "1.0"
status: "kabul-edilmis-referans"
phase: "urun-tanimi"
last_update: "2026-09-13"
depends:
  - "00-urun-felsefesi.md"
  - "01-bilgi-mimarisi.md"
  - "02-product-language.md"
affects:
  - "04-sistem-mimarisi.md"
author: "Codex; kabul yetkisi: proje sahibi"
---

> Depoya aktarım notu — 13 Eylül 2026: Kaynak: 3-Karar Motoru görevinin samandira-karar-motoru-v1.md çıktısı (01a09917-48a3-7440-aa53-6552cbd73e57). Kullanıcının bu görevdeki beyanıyla kabul edilmiş referanstır. Özgün gövde korunmuş; yalnız metadata, köken notu ve belge ilişkileri eklenmiştir. Gövdedeki öneri/durum ifadeleri tarihsel haliyle bırakılmıştır.

# Şamandıra — Karar Motoru

**Decision Engine · Nihai belge önerisi v1.0 · 13 Eylül 2026**

Bu belge; API, AI, Frontend, Akıllı Rota, öneri sistemi, gelecekteki işletme bilgi girişi ve kullanıcı deneyimi için ortak karar referansıdır. Ürün kurallarını tanımlar; uygulanmış veya kullanıcılarla doğrulanmış bir sistem tarif etmez. Kod, API uçları, veritabanı şeması ve arayüz tasarımı içermez.

> Şamandıra, insanlara en iyi yeri göstermeye çalışmaz. Kendileri için doğru olan yeri en az belirsizlik ve çabayla bulmalarını sağlar.

## 0. Bağlayıcı referanslar ve kapsam

Çalışmada **0-Ürün Felsefesi**, **1-Bilgi Mimarisi** ve **2-Ürün Veri Modeli** görevlerinin nihai metinleri okundu. Bilgi Mimarisi'nin 13 Eylül 2026 tarihli dosyası da esas alındı. Bu üç belge, kullanıcının bu çalışmadaki talimatıyla kabul edilmiş referanslardır. Karar Motoru onların temel yönünü değiştirmez.

Referansların görevleri birbirini tamamlar: Ürün Felsefesi neyi amaçladığımızı ve neyi yapamayacağımızı; Bilgi Mimarisi karar bilgisinin nerede karşılandığını; Product Language kavramların anlamını; bu belge ise hangi kanıttan hangi karara gidilebileceğini belirler. Çelişki yeni metinle sessizce çözülmez; ilgili referans açıkça yeniden değerlendirilir.

Korunan kararlar:

- Kullanıcı ham yorum, yeniden yazılmış yorum pasajı, yorumcu adı, yorum puanı veya konu sıklığı görmez. “İnsanlar böyle söylüyor” anlatımı kullanılmaz.
- Uygunluk yere yapıştırılmış kalıcı bir özellik değildir. Belirli amaç, koşul ve ziyaret bağlamı için üretilir.
- Güven tek tek iddialara aittir. İç düzeyler **Sağlam, Sınırlı, Yetersiz** olarak kalır.
- Uygunluk durumları **Uygunluğu desteklenen, Koşula bağlı, İhtiyaçla uyuşmayan, Değerlendirilemeyen** olarak kalır. Bunlar zorunlu kullanıcı rozetleri değildir.
- Atmosfer bağımsız puan değildir. Tempo ve enerji yeni karar eksenleri olarak geri getirilmez. Rota içindeki zaman dağılımı, kalış süresi ve fiziksel yük somut biçimde değerlendirilir.
- Keşfet ilk değerlendirmede üç ila beş seçenek hedefler; sayı doldurulmaz. Yer sayfasındaki anlamlı alternatifler en çok üçtür.
- Akıllı Rota bir karar yeteneğidir. Ayrı rota portalı, zorunlu gezi planlayıcısı veya yeni sayfa ailesi kararı değildir. İşletme girdilerini değerlendirmek de işletme panelini bu mimariye kendiliğinden eklemez.
- Ödeme ve ortaklık, uygunluk kanıtı veya organik sıra avantajı satın alamaz.

Belgedeki yerler, süreler, bütçeler ve örnek konuşmalar kurmacadır. Sayısal örnekler evrensel eşik değildir.

## 1. Karar Motoru tam olarak nasıl çalışır?

**Motorun temel işi: Bir yer hakkındaki kullanılabilir bilgiyi, bu ziyaretin ihtiyacıyla ilişkilendirip gerekçeli bir seçim alanı oluşturmaktır.** Başarı ölçüsü her soruya bir yer söylemek değildir; savunulabilir bir seçim veya vazgeçme kararı sağlayabilmektir.

Motor iki ilişkili süreç yürütür. Birincisi, kullanıcı arama yapmasa da yerler hakkında hangi iddiaların kullanılabileceğini güncel tutar. İkincisi, bir karar anında yalnız ilgili iddiaları kullanarak seçenek üretir. Böylece her aramada bütün yorumları yeniden okuyup yeni bir yer kişiliği uydurmaz.

### Bilgiyi karara hazırlama

1. **Girdinin kullanılabilirliğini kontrol et.** Kaynağın kullanım koşulları, kapsadığı yer, gözlem zamanı ve özgün kökeni biliniyor mu? İçerikteki yönlendirmeler kanıt olarak değerlendirilir; motorun kurallarını değiştiremez.
2. **Yeri ve kapsamı eşleştir.** Aynı isimli şubeleri, taşınmış işletmeleri, salon ile terası ve mevsimsel bölümleri ayır. Şube belirsizse deneyim bilgilerini birleştirme.
3. **İddiaları ayır.** “Bahçede müzik yoktu ama içeride yüksekti” tek bir sakinlik hükmüne dönüşmez. İki farklı kapsamda ses gözlemidir.
4. **Dayanakları değerlendir.** Tekrarları, bağımlı kaynakları, güncelliği, çelişkiyi ve anlam belirsizliğini incele. Her iddianın bilgi türünü ve güvenini belirle.
5. **Kullanım iznini belirle.** İddia yayımlanabilir mi, yalnız dar kapsamda mı kullanılabilir, yoksa yeniden doğrulama mı gerekir? İçeride bulunmak kullanıcıya sunulmaya yetmez.

### Karar anında çalışma

| Aşama | Yapılan iş | Korunan sınır |
|---|---|---|
| Bağlamı anla | Amaç, tercih, zorunlu koşul ve ziyaret bağlamını ayır. | Söylenmeyen ihtiyaç tamamlanmış sayılmaz. |
| Gerekirse netleştir | Yanıtı adayları veya kritik bir koşulu değiştirecek en değerli soruyu seç. | Uzun başlangıç anketi yoktur. |
| Adayları bul | Coğrafya, tür, olanak ve amaç ilişkisine göre yeterli aday havuzu kur. | Yalnız popüler veya en çok verisi olan yerleri tarama. |
| Gerçekleşebilirliği denetle | Yer kimliği, ziyaret durumu, kullanım koşulları ve zorunlu sınırları kontrol et. | Engel veya kritik bilinmeyen ortalamada eritilmez. |
| Uygunluğu değerlendir | İlgili yer özelliklerinin bu amacı destekleyip desteklemediğini değerlendir. | Genel beğeni ve duygu puanı uygunluk değildir. |
| Seçenekleri karşılaştır | Açık öncelikler, ödünler ve karar açısından önemli belirsizliklerle karşılaştır. | Daha iyi bilinmek, otomatik olarak daha uygun olmak değildir. |
| Seçkiyi oluştur | Benzer derecede uygun seçenekler arasında anlamlı farkları koru. | Çeşitlilik açık ihtiyacı geriye itemez. |
| Gerekçeyi üret | Gerçekte kullanılan neden, önemli ödün ve bilgi sınırını anlat. | Sonradan ikna edici bir hikâye uydurulmaz. |
| Son kontrolü yap | Cümleler kararı ve dayanakların kapsamını doğru taşıyor mu? | AI, koşulu veya belirsizliği metinden düşüremez. |
| Sonuçtan öğren | Kullanıcının düzeltmesini ve varsa deneyim karşılığını ilgili bilgiye bağla. | Tıklama veya ziyaret tek başına memnuniyet değildir. |

AI; dili anlar, gözlemleri ayrıştırır, bağlam farklarını bulmaya yardım eder ve izin verilen kararı anlaşılır anlatır. **Zorunlu koşulu gevşetmek, kanıtsız iddiayı geçirmek ve ticari avantaj eklemek AI'ın takdirinde değildir.** Akıcı anlatım son kontrolü geçmezse daha sade, kanıtı izlenebilir ifade kullanılır; gerekiyorsa iddia hiç üretilmez.

Motorun sonuçları yalnız öneri değildir: belirli yeri bulma, sınırlı kapsamda bilgi verme, netleştirme isteme, yeterli eşleşme bulamama ve geçici hizmet sorunu da geçerli sonuçlardır. Bir yerin adını arayan kullanıcıya kayıt gösterilebilir; bu, o yeri koşullarına uygun önerdiğimiz anlamına gelmez.

## 2. Bir yer nasıl “uygun” değerlendirilir?

Uygunluk şu ilişkiye bağlıdır: **yer + amaç + zorunlu koşullar + tercihler + ziyaret bağlamı + kullanılabilir dayanak**. Kişi değişmeden gün veya amaç değiştiğinde sonuç değişebilir.

| Uygunluk durumu | Kararın anlamı |
|---|---|
| Uygunluğu desteklenen | İlgili amaç için yeterli dayanak var ve belirtilen zorunlu koşullar karşılanıyor. Memnuniyet garantisi değildir. |
| Koşula bağlı | Uygunluk bilinen bir saat, bölüm veya kullanım biçiminde geçerli. Bu koşul açıkça anlatılır; kritik bilgi eksikliği bu duruma taşınmaz. |
| İhtiyaçla uyuşmayan | Bilinen özellik ana amaçla veya zorunlu koşulla çelişiyor. Bu ziyaret için verilen sonuç, genel yer yargısı değildir. |
| Değerlendirilemeyen | Bu uygunluk sonucunun gerekli dayanağı yetersiz. Bilinen somut bilgiler yine anlatılabilir. |

### Önce telafi edilemeyen sınırlar

| Zorunlu koşulun durumu | Motorun davranışı |
|---|---|
| Karşılandığı yeterli dayanakla biliniyor | İlgili koşul geçilir; diğer koşullar ayrıca kontrol edilir. |
| Karşılanmadığı biliniyor | Yer, bu bağlamın uyumlu önerilerinden çıkarılır. |
| Karşılanıp karşılanmadığı bilinmiyor | Yer doğrulanmış eşleşmeler arasına girmez. Eksiklik önemliyse belirtilir. |
| İlgili kaynaklar çözülemeyen biçimde çelişiyor | Koşul karşılanmış kabul edilmez; doğrulama gerekir. |
| Yalnız belirli bölüm veya saatte karşılanıyor | Kullanıcının ziyareti o kapsamla örtüşüyorsa değerlendirilir; kapsam açıkça söylenir. |

“Ucuz olsun” kesin para sınırı değildir. “İki kişi toplam en fazla 1.200 TL” zorunlu üst sınırdır; kişi başı fiyat veya yalnız giriş ücretiyle karşılanmış sayılmaz. Kapsamı belli tüketim, zorunlu ek ücretler ve kullanıcı bütçeye dahil ettiyse ulaşım birlikte değerlendirilir. Tahmini aralığın üst tarafı sınırı aşıyorsa “bütçene uyuyor” denmez.

Fiziksel erişimde girişten kullanılacak alana kadar gereken bütün yol değerlendirilir. Basamaksız giriş, kullanılacak katın ve gerekli tesislerin erişimini tek başına kanıtlamaz. Kullanıcının belirtilmemiş ihtiyaçları otomatik eklenmez.

### Ardından amaç ve tercihler

Amaç için hangi bilgilerin gerekli olduğu, Product Language kavramlarıyla tanımlanır. Bu birer genel yer etiketi değildir:

| Amaç örneği | Uygunluğu taşıyan bilgiler | Tek başına yetmeyen bilgi |
|---|---|---|
| Uzun sohbet | İlgili saatte ses ortamı, oturma olanağı, kalışa ilişkin kullanım koşulları; yoğunluğun etkisi | Düşük müzik bilgisi, iki saat oturulabildiğini göstermez. |
| Bilgisayarla çalışmak | Çalışmaya izin, gerekli olanaklar, ses ve kalış koşulları; kullanıcının süre ihtiyacı | Masa veya priz bulunması çalışmaya izin verildiği anlamına gelmez. |
| Kısa yürüyüş | Kullanılabilir güzergâh, süre, yüzey/eğim ve ziyaret durumu | Yakın bir yeşil alanın bulunması yürünebilir parkuru kanıtlamaz. |
| Yağmurda vakit geçirmek | Kullanılabilir kapalı/korunaklı alan ve ona ulaşım; varsa kapasite koşulu | Bir şemsiyenin fotoğrafı yağmurdan korunma güvencesi değildir. |

Hangi dayanağın gerekli olduğu, ifadenin kapsamına bağlıdır. “Müzik düşük” iddiası ile “bu akşam iki saat kesintisiz konuşmaya uygun” iddiası aynı kanıtı istemez. İkincisi için kalış koşulu veya akşam ses bilgisi yoksa ilk bilgi yine anlatılabilir; geniş uygunluk hükmü kurulmaz.

Sıralama mantığı şu sırayı korur:

1. Ziyaretin gerçekleşmesini ve zorunlu koşulları sağlayan adayları ayır.
2. Ana amacın desteklenmesini değerlendir; açık amaçla güçlü çelişkisi olanı eşdeğer seçenek yapma.
3. Kullanıcının belirttiği tercih önceliklerine göre anlamlı ödünleri karşılaştır.
4. Kararı değiştirebilecek belirsizlikleri karşılaştır. Sonuç küçük bir varsayımla tersine dönüyorsa güçlü bir üstünlük iddiası kurma.
5. Benzer uygunlukta gereksiz ulaşım, bekleme, masraf ve tekrar yükünü azalt; anlamlı alternatif farkını koru.

Bütün kararları taşıyan tek toplam puan veya evrensel ağırlık seti yoktur. İç karşılaştırma değerleri kullanılabilir; engelleri ve güven düzeylerini tek sayıya gömemez. Yerlerin sırası değiştiğinde hangi kullanıcı önceliği veya kanıtın değiştiği açıklanabilmelidir.

Örneğin A aynı sohbet koşullarını daha kısa ulaşım ve daha düşük maliyetle sağlıyorsa B'nin ilk seçkide yer alması için ilgili bir ek avantajı gerekir. B'nin manzarası ancak kullanıcı için anlamlıysa fark yaratır. Belirtilmemiş bir manzara tercihi A'yı geriye itmez.

### Grup kararı

Grubun bilinen zorunlu koşulları birlikte korunur; bir kişinin erişim gereksinimi çoğunluk tercihine yenilmez. Önce herkesin ziyaret edebileceği ortak alan aranır. Ardından ortak amaç ve ifade edilen tercih farkları değerlendirilir. Hesabın sahibinin geçmişi grubun zevki sayılmaz.

Ortak çözüm yoksa uyuşmazlık açıklanır. Kimin hangi koşulundan vazgeçeceğini motor belirlemez. Bir kişinin “vazgeçebilirim” demesi başka bir kişinin aynı koşulunu kaldırmaz.

## 3. Kararı etkileyen ana bileşenler

| Bileşen | Karardaki görevi | Kötü kullanım sınırı |
|---|---|---|
| Açık amaç ve öncelikler | Aranacak deneyimi tanımlar. | Yer türüne veya geçmişe indirgenmez. |
| Zorunlu koşullar | Uyumlu seçeneğin sınırını çizer. | Ortalama avantajla telafi edilmez. |
| Yer kimliği, türü ve olanakları | Hangi yerin hangi faaliyeti destekleyebileceğini belirler. | Türden deneyim stereotipi çıkarılmaz. |
| Fiziksel ortam, ses, yoğunluk | Deneyimin somut koşullarını anlatır. | Soyut atmosfer/enerji puanına dönüşmez. |
| Kullanım koşulları ve ziyaret durumu | Olanakların ne zaman ve nasıl kullanılabildiğini belirler. | Açılış saati kapasite veya rezervasyon onayı sayılmaz. |
| Maliyet, zaman ihtiyacı, ulaşım, fiziksel erişim | Kararın gerçek yükünü ve yapılabilirliğini belirler. | Kuş uçuşu yakınlık kolay erişim sayılmaz. |
| Gün, saat, mevsim, hava ve özel olaylar | Kanıtın bu ziyarete taşınıp taşınamayacağını belirler. | Geçmiş örüntü canlı durum gibi anlatılmaz. |
| Dayanak, güven ve kapsam | Hangi kararın savunulabileceğini sınırlar. | Veri hacmi kaliteye veya uygunluğa eşitlenmez. |
| Öğrenilmiş tercihler | Eksik açık önceliklerde, izin verilen ölçüde yardımcı olur. | Bugünkü isteğe ve reddetmeye üstün gelemez. |
| Diğer seçenekler ve rota ilişkisi | Anlamlı farkı ve ziyaret dizisinin bütünlüğünü belirler. | Kendi başına yakınlık veya çeşitlilik yeterli değildir. |

Duygu analizi bağımsız bir uygunluk bileşeni değildir. Belirli bir olayın, özelliğin veya beklenti farkının anlaşılmasına yardım edebilir. “Kalabalığa bayıldım” yoğunluğu olumlu bir kalite puanına dönüştürmez; kalabalık gözlemi ile kişinin tepkisi ayrılır. Ziyaret sayısı da talep/yoğunluk araştırmasına girdi olabilir; memnuniyeti göstermez.

## 4. Kesin bilgi, çıkarım ve tahmin nasıl ayrılır?

“Kesin bilgi” ifadesi değişmez gerçek anlamında kullanılmamalıdır. Ürün dilindeki karşılığı, **belirli kapsam ve tarihte doğrulanmış olgudur**. Bilginin türü ile güven düzeyi farklıdır: Bir çıkarım sağlam dayanaklı olabilir ve yine de çıkarım olarak kalır.

| Bilgi türü | Tanım | Örnek ve kullanım sınırı |
|---|---|---|
| Doğrulanmış olgu | Kapsamı açık biçimde kontrol edilmiş mevcut özellik veya ilan edilmiş kural | “Ana giriş basamaksız.” Kullanılacak üst kata ilişkin hüküm içermez. |
| Doğrulanmamış bildirim/gözlem | Bir kaynağın söylediği veya bir anda gözlemlediği bilgi | “İşletmenin bildirdiği saatler…” Bildirimin varlığı ile fiilî durumun doğruluğu ayrıdır. |
| Çıkarım | İlgili dayanakların birlikte yorumlanmasıyla elde edilen bağlamsal sonuç | “Hafta içi gündüz düşük ses uzun sohbeti destekliyor.” Kapsanan saat ve alanı aşamaz. |
| Tahmin | Gelecek zamana veya doğrudan gözlenmeyen duruma ilişkin beklenti | “Cumartesi öğleden sonra daha yoğun olabilir.” Dayanak, zaman ufku ve belirsizlik gerekir. |

Coğrafi hesaplama da kullandığı verinin sınırını taşır. Koordinatlardan hesaplanan mesafe, yürüyüş yolu değildir. Yol ağı ve geçiş bilgisi bilinse bile gelecekteki ulaşım süresi yaklaşık bir değerdir. Hava tahmini, bir terasın kesin kapanacağı anlamına gelmez; kapanma kuralı ayrıca bilinmelidir.

“Programda 22.00'ye kadar açık” bir çalışma saati bilgisidir. “Şu an açık” daha güncel dayanak isteyen durum iddiasıdır. “Vardığında açık olacak” varış saati ve istisnaları içeren geleceğe dönük değerlendirmedir. “Yer bulacaksın” ise bunların hiçbirinden tek başına üretilemez.

Her iddia içeride neyi anlattığını, hangi yer/bölüm/zaman için geçerli olduğunu, dayanağını, gözlem tarihini, bilgi türünü ve kullanım sınırını korur. Bu bir veritabanı şeması değil, bütün bileşenlerin korumak zorunda olduğu anlam bütünlüğüdür.

## 5. Confidence — güven seviyesi nasıl oluşur?

**Güven, belirli bir iddianın belirtilen kapsamda ne ölçüde savunulabildiğidir. Kullanıcının memnun kalma yüzdesi değildir.** Mekâna genel güven rozeti verilmez.

Değerlendirme; doğrudanlık, kaynağın konuya uygunluğu, bağımsızlık, güncellik, bağlam kapsamı, tutarlılık ve anlam açıklığını birlikte kullanır. Bu ölçütlerin sabit ağırlıklı ortalaması alınmaz. Yanlış şube eşleşmesi gibi bir hata, çok sayıda olumlu işaretle giderilemez.

### Güven üretme sırası

1. Kimlik ve anlam belirsizliğini kontrol et. Yanlış yere bağlanan veya ne söylediği anlaşılmayan kanıt elenir ya da incelemeye ayrılır.
2. Kanıtın iddiaya doğrudan ve konu bakımından uygun olup olmadığını değerlendir.
3. Aynı kökenden kopyalanan dayanakları tek kanıt ailesi olarak ele al. İki sağlayıcı aynı işletme duyurusunu taşıyorsa iki bağımsız doğrulama yoktur. Köken bağımsızlığı belirsizse bağımsız olduğu varsayılmaz.
4. Gözlem zamanı ile değerlendirilmek istenen zamanı karşılaştır. Yeni içe aktarılan eski bilgi taze sayılmaz.
5. Saat, bölüm, gün ve mevsim kapsamını kontrol et. Çelişki kapsam farkıyla açıklanabiliyorsa iddiayı böl.
6. Çözülemeyen önemli çelişkiyi ve temsil eksikliğini koru. Çoğunluk oyuyla silme.
7. İddiaya **Sağlam, Sınırlı veya Yetersiz** güven ver; hangi kapsamda kullanılabileceğini belirle.

| Düzey | Üretim koşulu | Karara etkisi |
|---|---|---|
| Sağlam | İddiaya uygun, yeterince güncel ve kapsamı açık dayanak; önemli çelişki çözülmüş | O kapsamda kullanılabilir. Çıkarım veya tahmin kesin olguya dönüşmez. |
| Sınırlı | Anlamlı dayanak var; kapsam, güncellik veya tutarlılık sınırı sürüyor | Kapsam daraltılır ve ilgili sınır açıklanır. Kritik zorunlu koşulu doğrulanmış geçirmeye yetmez. |
| Yetersiz | Savunulabilir iddia için gerekli dayanak yok veya temel sorun çözülmemiş | İddia üretilmez; kararı etkiliyorsa eksiklik belirtilir. |

Güven yükselmesi ile iddia kapsamının daralması karıştırılmaz. “Akşamları sessiz” desteklenmiyor ama “salı öğlen iç salonda müzik düşük” destekleniyorsa daha geniş iddia doğrulanmış olmaz; farklı ve daha dar bir iddia kullanılabilir.

### Güvenin sonuca taşınması

Sonuç, gerekçesini taşıyan zorunlu dayanaklardan daha güçlü sunulamaz. Bir yere ait bütün bilgilerin en düşük güvenini almak da yanlıştır: sohbet kararı için ilgisiz bir otopark eksikliği uygunluk değerlendirmesini düşürmez. Sınırlayıcı olan, **bu kararın bağlı olduğu gerekli dayanaklardır**.

Adres sağlam, merdiven bilgisi belirsizse basamaksız erişim arayan kullanıcı için karar belirsizdir. Aynı yer başka bir kullanıcıya yalnız doğrulanmış adresi ve ziyaret saatleriyle anlatılabilir.

### Güncellik ve kalibrasyon

Anlık doluluk ve geçici kapanma hızlı; fiyat, saat ve kullanım kuralları değişken; yapı ve coğrafi özellikler daha yavaş değişebilir. Hepsine tek geçerlilik süresi uygulanmaz. Tadilat, işletmeci değişikliği veya etkinlik duyurusu, normal yenileme zamanı gelmeden bağlı iddiaları yeniden değerlendirmeyi tetikler.

Başlangıçta “10 katkı = sağlam” veya “güven %85'i aşınca yayımla” gibi temelsiz eşikler konmaz. Her iddia ailesi için gerekli kanıt türü, kapsam, güncellik ve istisna kuralları tanımlanır. Otomatik yayın açılmadan önce bağımsız kontrol örnekleriyle yanlış iddia ve yanlış kesinlik oranları incelenir.

Kontroller şehir, yer türü, saat, bilgi türü ve güven düzeyine göre ayrılır. Tahminlerde ifade edilen süre/maliyet aralıklarının gerçekleşmeleri ne ölçüde kapsadığı; çıkarımlarda anlatılan deneyimle gözlemin örtüşmesi incelenir. Ortak bir ülke ortalaması, bir şehirdeki sistematik hatayı gizleyemez. Eşikler ve yenileme aralıkları bu sonuçlarla ayarlanır; AI'ın kendine güvenmesi kanıt sayılmaz.

## 6. AI hangi durumda “Bilmiyorum” demelidir?

AI bütün yer hakkında susmak yerine bilmediği belirli şeyi söylemelidir. Ancak eksik nokta önerinin zorunlu dayanağıysa uygunluk iddiasından da vazgeçmelidir.

| Durum | Söylenecek sınır | Devam yolu |
|---|---|---|
| Açık zorunlu koşul doğrulanamıyor | “İç salona basamaksız erişimi doğrulayamıyoruz.” | Bu koşulu bilinen seçenekleri göster; yoksa eşleşme olmadığını söyle. |
| Canlı durum soruluyor, yalnız geçmiş örüntü var | “Şu anki yoğunluğu bilmiyoruz.” | Varsa geçmiş örüntüyü ayrı ve zamanıyla anlat. |
| Kanıt kapsamı ziyaret zamanını karşılamıyor | “Akşam saatleri için yeterli ses bilgimiz yok.” | Gündüz verisini akşama taşımadan bilinen kısmı açıkla. |
| Kimlik/şube belirsiz | “Bu bilginin hangi şubeye ait olduğunu netleştiremedik.” | Eşleşmeyi düzelt; bağlı deneyim anlatısını durdur. |
| Çelişki çözülemiyor | “Ziyaret saatine ilişkin bilgiler çelişiyor.” | Güncel doğrulama yolu varsa sun; saat uydurma. |
| Kullanıcı ihtiyacı anlaşılamıyor | “Sakinlikten az ses mi, az insan mı istediğin net değil.” | Kararı değiştirecek kısa netleştirme yap. |
| Öngörü olağan kapsamın dışında | “Etkinlik günündeki beklemeyi güvenilir biçimde tahmin edemiyoruz.” | Daha az bu koşula bağlı seçenek veya plan sun. |

“Olabilir”, “muhtemelen” veya “sanırım” eklemek kanıtsız bir iddiayı kullanılabilir yapmaz. Genel güvenlik, alerjen riski veya bütün alanı kapsayan erişilebilirlik gibi geniş güvenceler; şikâyet yokluğundan, kişi profilinden veya yüzeysel gözlemden çıkarılmaz.

Motor ayrıca **ne olursa değerlendirebileceğini** bilmelidir: doğru şube, güncel kural, ilgili alanın gözlemi veya kullanıcının ziyaret saati. Kullanıcıya her seferinde doğrulama işi yüklenmez; sistemin sorumluluğundaki veri açığı içeride iyileştirme ihtiyacı olarak kalır.

## 7. Eksik veri olduğunda sistem nasıl davranır?

Eksiklik başarısızlıkları gizleyen tek bir “sonuç yok” durumuna çevrilmez.

| Durum | Ürün davranışı |
|---|---|
| Karar için ilgisiz bilgi eksik | Kullanıcının dikkatini tüketmez; mevcut iddiaları düşürmez. |
| İkincil tercih bilgisi eksik | O tercihin karşılandığı iddia edilmez. Ana amaç destekleniyorsa bilinen gerekçelerle değerlendirme sürebilir. |
| Ana uygunluk iddiasının gerekli dayanağı eksik | Geniş uygunluk üretilmez; daha dar, dayanaklı bilgi verilir. |
| Zorunlu koşul eksik | Doğrulanmış eşleşmelerden ayrılır. “Koşula bağlı” etiketiyle eksik bilgi aklanmaz. |
| Bilgi eskimiş | Güncel iddia olarak kullanılmaz; anlamlıysa tarihli bilgi olarak tutulur. |
| Kaynaklar çelişkili | Önce kapsam ayrıştırılır; çözülmezse ilgili sonuç durdurulur. |
| Kavram uygulanamaz | Eksik sayılmaz; gereksiz bilgi tamamlatılmaz. |
| Şehir/alan kapsamı yetersiz | Dünyada seçenek olmadığı değil, sistemin yeterince bilmediği söylenir. |
| Geçici veri hizmeti sorunu | Kapsam yokluğundan ayrı anlatılır; eski sonuç canlıymış gibi sunulmaz. |
| Koşullar altında bilinen eşleşme yok | Hangi sınırın belirleyici olduğu açıklanır; değişiklik ancak kullanıcı seçerse uygulanır. |

Yeni veya az bilinen yerin deneyim metni zayıf diye bütün kayıt görünmez yapılmaz. Kimliği ve temel bilgileri bilinen yer bulunabilir; yalnız desteklenen amaçlar için önerilebilir. Veri azlığı kalite düşüklüğü değildir. Buna karşılık veri eşitliği adına bilmediğimiz zorunlu koşulları onaylamak da doğru değildir.

Eksikliği azaltmak için adayları anlamlı biçimde ayıracak bilgi öncelenir. Kimlik, kapanma, erişim ve zorunlu ücret gibi yanlışlığı kararı bozan alanlar; metni güzelleştirecek ikincil özelliklerden önce gelir. Yer sahibinden veya kullanıcıdan istenen katkı da bu belirli açığı hedefler.

Coğrafya, bütçe, süre ve zorunlu koşullar sessizce genişletilmez. Ayrı bir genişletme önerisi, neyin değişeceğini ve neden işe yarayabileceğini açıkça söyler. Varsayılan bir öneriyi reddetmek kalıcı bir kişilik çıkarımı oluşturmaz.

## 8. Önerinin gerekçesi kullanıcıya nasıl açıklanır?

Bir öneri, kullanıcının şu dört şeyi anlayabilmesini sağlamalıdır: **Neden değerlendiriyorum? Hangi ödünü kabul ediyorum? Neyi yeterince bilmiyoruz? Hangi koşulda başka seçeneğe geçmeliyim?**

Gerekçe, karar üretildikten sonra metni çekici hale getirmek için bulunmaz. Motorun gerçekten kullandığı dayanaklardan oluşturulur. Kullanıcıya ara muhakeme veya teknik ağırlık verilmez; kararın anlaşılabilir nedenleri verilir.

Örnek karar özeti:

> “İstediğin uzun sohbeti hafta içi gündüz düşük müzik düzeyi ve kalış süresi sınırı olmaması destekliyor. Daha yakın seçeneğe göre yürüyüş biraz uzun. Akşam için aynı değerlendirmeyi yapamıyoruz.”

Bu cümle, ancak her dayanağın ilgili kapsamı destekleniyorsa kullanılır. “Kalış sınırı bilmiyoruz” ile “kalış sınırı yok” farklıdır. Maliyet veya fiziksel erişim zorunluysa onların sonucu da görünür; kısa açıklama uğruna çıkarılmaz.

Gerekçenin ayrıntısı karar riskine göre artar. İlgisiz bütün belirsizlikleri sıralamak kullanıcıya analiz yükünü geri verir. Buna karşılık başlığı olumlu, kritik koşulu dipte olan bir öneri kabul edilmez. Bilginin kontrol tarihi, yalnız kontrol edilen iddiaya bağlanır; genel sayfa tarihi bütün bilgilerin yenilendiği anlamına gelmez.

“Neden bu seçenek?” sorusunun daha derin cevabı, ilgili özelliklerin ve önemli bilgi sınırlarının açıklaması olabilir. Kaynak türü veya doğrulama kapsamı gerektiğinde anlatılır; ham yorum ve yorumcuya açılan kapı oluşturulmaz. Referanslardaki gerekli veri/lisans atıfları korunur.

### Açıklamanın doğruluğu için ürün kontrolleri

- Gerekçeden bir özellik çıkarıldığında kararın dayanağı gerçekten değişiyor mu? Değişmiyorsa o özellik belirleyici neden gibi anlatılmaz.
- Aynı kanıt farklı kullanıcılar için farklı anlam taşıyabilir; fakat kanıtın kendisi kullanıcının zevkine göre değiştirilemez.
- “Daha az ses” gibi karşılaştırma aynı zaman, bölüm ve değerlendirme kapsamını kullanır. Farklı kapsamlar eşitmiş gibi karşılaştırılmaz.
- Kullanıcının önceliği değiştiğinde gerekçe ve sıra birlikte yeniden değerlendirilir. Metin tek başına yeniden yazılmaz.
- Kullanıcının reddettiği yer aynı bağlamda yeni sıfatlarla tekrar önerilmez.

## 9. Alternatif mekânlar nasıl seçilir?

Alternatif, ilk yerin yakınında bulunan herhangi bir yer değildir. **Aynı kararın anlamlı başka bir çözümüdür.** Önce ana amaç ve zorunlu koşullar korunur; sonra bir ödünün nasıl değiştiği gösterilir.

Alternatif üretme sırası:

1. Kullanıcının açık ret nedeni varsa onu kullan. “Uzak” ile “yüksek müzik” farklı adaylar gerektirir. Ret nedeni bilinmiyorsa kişisel neden uydurma.
2. Mevcut karar bağlamını koru. Aynı bütçe, erişim ve süre sınırlarını uygula.
3. İlk seçeneğin önemli ödününü azaltan veya kullanıcının açık başka önceliğini destekleyen adayları bul.
4. Değiş tokuşu anlat: “Daha kısa ulaşım; açık alan daha küçük.”
5. Benzer seçenekleri azalt. Ayrımı açıklanamayan ikinci kopya yerine daha az seçenek sun.

| Alternatif ilişkisi | Kullanıcıya sunduğu değer | Korunan sınır |
|---|---|---|
| Aynı amaç, daha az ulaşım | Zaman ve hareket yükünü azaltır. | Yakınlık ana amacın kaybını gizleyemez. |
| Aynı amaç, daha net ziyaret koşulu | Belirli kritik belirsizliği azaltır. | Genel “daha güvenilir mekân” hükmü kurulmaz. |
| Aynı amaç, farklı ödün | Daha az ses karşılığında daha uzun yol gibi seçim sağlar. | Kullanıcının zorunlu sınırı ödün sayılmaz. |
| Aynı rota rolü, farklı risk | Yağıştan daha az etkilenen mola gibi dayanıklı seçenek sağlar. | Yeni durakla tüm kalan rota tekrar kontrol edilir. |

Keşfet'te üç ila beş ilk seçenek hedefi ve Yer'de en çok üç alternatif sınırı korunur. Uygun alternatif yoksa yapay bir seçenek eklenmez. Kullanıcı isterse daha fazla sonucu açıkça talep edebilir.

Farklı amaç veya genişletilmiş coğrafya ancak açık bir değişiklik seçeneği olarak sunulur. Aynı şartları karşılamayan yer “alternatif” adı altında uyumlu sonuçlara sokulmaz. Sonuçların sırası küçük belirsizliklerle değişiyorsa aralarında güçlü üstünlük anlatmak yerine temel farklar anlatılır.

## 10. Akıllı Rota: anlamlı deneyim dizisi

**Akıllı Rota, kullanıcının amacını birbiriyle uyumlu ziyaretlere ve geçişlere bölen; toplam yükü, koşulları ve aksama halinde devam edebilme olanağını birlikte değerlendiren karar yeteneğidir.**

Bir rota “en iyi mekânlar toplamı” değildir. Birbirinden iyi iki yer, aynı zaman diliminde birlikte kötü bir plan oluşturabilir. Yolculuk, bekleme ve dinlenme deneyimin parçalarıdır. Daha çok durak başarı göstergesi değildir.

### 10.1. Ne zaman devreye girer?

Kullanıcı birden fazla faaliyet, belirli bir süreyi doldurma veya ziyaretler arasında anlamlı bağlantı istediğinde değerlendirilir: “İki saatimiz var, biraz yürüyüp oturarak konuşalım.” Tek bir kafe arayana rota şart koşulmaz. Tek yer isteği en iyi biçimde karşılıyorsa tek yer önerisi yeterlidir.

Keşfet ve mevcut yer bağlamıyla ilişkilidir. Bu belge ayrı bir rota sayfası, rezervasyon merkezi veya navigasyon ürünü açmaz. Yol geometrisi, dönüşler ve ulaşım tahminleri mevcut harita hizmetlerinden gelebilir. Şamandıra hangi durakların neden, hangi sırayla ve ne kadar süreyle anlamlı olduğunu üstlenir.

### 10.2. Rota bağlamı

Gerekli bilgiler: amaç veya amaçlar, öncelikleri, başlangıç zamanı, ayrılabilecek toplam süre, başlangıç noktası, gerekli bitiş noktası, ulaşım biçimi, bütçe ve zorunlu koşullar. Grup için bilinen ortak sınırlar da korunur.

Her alanın baştan sorulması gerekmez. Konum izni olmadan kullanıcı başlangıç seçebilir. Başlangıç veya bitiş bilinmiyorsa yalnız duraklar arasındaki plan verilebilir; kapıdan kapıya toplam süre iddia edilmez. Dönüşün dahil olup olmadığı açık olmalıdır.

“Çok yorulmayalım” talebi somut yürüme süresi, eğim, ayakta kalma ve mola ihtiyacı üzerinden anlaşılır. Yaş veya grup kimliğinden otomatik efor sınırı türetilmez. Kullanıcının sınırı karar için gerekliyse kısa bir netleştirme yapılır.

### 10.3. Her durağın bir işi olmalı

Rota içinde bir durak ana amacı karşılayabilir, başka bir faaliyeti tamamlayabilir, dinlenme sağlayabilir veya bitiş noktasına anlamlı geçiş oluşturabilir. Bu roller yalnız o rotaya aittir; yeni kalıcı mekân etiketleri değildir.

Her durak için motor şunları cevaplamalıdır:

- Burada hangi amaç karşılanıyor?
- Bu durağın sıradaki yeri neden anlamlı?
- Ziyaretin işe yaraması için gereken süre nedir; hangi süre isteğe bağlıdır?
- O zaman aralığında kullanılabilir mi; son giriş veya kapanış koşulu var mı?
- Hangi maliyet, bekleme, yürüme veya fiziksel erişim yükünü ekliyor?
- Çıkarılırsa ana amaç hâlâ karşılanır mı; yerini hangi özellikte bir durak alabilir?

Sırf yol üzerinde olduğu, popüler olduğu veya ticari ilişki taşıdığı için durak eklenmez. Art arda benzer faaliyetler ancak kullanıcının isteği bunu gerektiriyorsa anlamlıdır. Çeşitlilik zorunlu bir tat programına dönüşmez.

### 10.4. Oluşturma ve seçim sırası

1. Ana amacı ve vazgeçilmez ziyaretleri belirle. Kullanıcının sabitlediği duraklar ancak uyuşmazlık açıklanarak değiştirilebilir.
2. Her gerekli faaliyet için uygunluğu desteklenen sınırlı aday kümesi oluştur.
3. Duraklar arası gerçek bağlantıyı, kullanılacak girişleri ve ulaşım biçimini değerlendir. Kuş uçuşu yakınlıktan geçiş üretme.
4. Varış zamanını hesaplamaya yetecek süre bilgileriyle aday dizileri kur. Açılış, son giriş, etkinlik ve rezervasyon saatlerini o varışa göre kontrol et.
5. Ulaşım, anlamlı kalış, bekleme, geçiş, gerekiyorsa dönüş ve aksama payını toplam süreye dahil et. Aynı yürüyüşü hem etkinlik hem ulaşım diye iki kez sayma.
6. Toplam bütçeyi aynı kapsamda hesapla. Ucuz duraklar, toplam planın bütçeye sığdığını kendiliğinden göstermez.
7. Ortak hava, etkinlik, ulaşım veya kapanma risklerinin birden fazla durağı birlikte etkileyip etkilemediğini kontrol et.
8. Yapılabilir diziler arasında amacı daha iyi karşılayan, gereksiz yükü daha az ve bozulduğunda daha kolay sürdürülebilen planı seç.
9. Her durağın rolünü, önemli ödünü, plan varsayımlarını ve gerekli alternatifini açıkla.
10. Son açıklamadan önce dizinin tamamını yeniden kontrol et. Tek tek geçerli duraklardan geçersiz toplam üretme.

Öncelik sırası: **zorunlu koşullar → ana amacın karşılanması → zaman ve toplam yükün yapılabilirliği → anlamlı tamamlayıcılık → benzer planlar arasında daha az gereksiz yol ve çaba**. En kısa plan otomatik kazanmaz; daha uzun planın ek yükü karşılayan açık bir amacı olmalıdır.

### 10.5. Süre ve belirsizlik

Tahmini süreler gerektiğinde aralık olarak anlatılır. Ortalama sürelerin toplamı, yetişme garantisi değildir. Kuyruk veya trafik gibi aynı olaydan etkilenen süreler bağımsızmış gibi ele alınmaz. Kapanışa yetişmek için ancak bütün sürelerin en iyi ihtimalde gerçekleştiği plan önerilmez.

Zorunlu toplam süre, bilinmeyen kritik bir geçiş yüzünden doğrulanamıyorsa plan “iki saate sığar” diye sunulmaz. Daha kısa bir plan, daha iyi bilinen bağlantı veya yalnız bilinen kapsam önerilir. Belirsizliği sayısal olarak modellemek mümkün değilse keyfî dakika payı ekleyip kesinlik yaratılmaz.

Gerekli bir rezervasyonun yapılabilir olması, rezervasyonun yapıldığı anlamına gelmez. Plan bu koşula bağlıysa açıklanır. Başarılı rezervasyon veya kapasite onayı olmadan kullanıcıya yer ayrılmış izlenimi verilmez.

### 10.6. Kurmaca rota örneği

İstek: “İki saatimiz var. Kısa yürüyüşten sonra uzun sohbet edelim. Sonunda başladığımız noktaya dönelim; toplam yürüyüş 35 dakikayı aşmasın.”

Aşağıdaki aralıkların ve bağlantıların ilgili ziyaret için yeterli dayanağı olduğu varsayılmıştır:

| Parça | İşlev | Süre |
|---|---|---|
| Başlangıçtan kıyıya geçiş | Yürüyüşe erişim | 5 dakika |
| Kısa kıyı yürüyüşü | İlk açık amaç | 15 dakika |
| Kapalı oturma alanına geçiş | İki amacı birbirine bağlama | 5 dakika |
| Oturarak sohbet | Öncelikli ikinci amaç | 55–65 dakika |
| Başlangıca dönüş | Bitiş koşulunu sağlama | 5–10 dakika |
| Giriş/yerleşme ve küçük gecikme payı | Planın aşırı sıkışmasını önleme | 10–15 dakika |

Toplam planlanan aralık 95–115 dakika, toplam yürüyüş 30–35 dakikadır. Beş dakikalık ek durak, yalnız zaman kaldığı için eklenmez. Giriş payı için dayanak yoksa veya oturma yerine ulaşma süresi belirsizse bu hesap aynı kesinlikle kullanılamaz.

Sıralamanın gerekçesi: kısa hareketten sonra uzun ve kesintisiz oturma; bitiş noktasına yakın son durak; geri dönüş yükünün kontrolü. Başka bir istekte ters sıra daha uygun olabilir. Bu bir evrensel rota şablonu değildir.

Oturma alanının yalnız terası varsa yağmur riski planın ana amacını etkileyebilir. Yedek de başka bir açık teras olursa aynı riski taşır. Mümkünse aynı sohbet amacını destekleyen kapalı bir seçenek değerlendirilir ve geçişler yeniden hesaplanır. Yağmur nedeniyle yürüyüşün çıkarılması kullanıcının açık amacını değiştirir; motor bunu sessizce yapmaz.

### 10.7. Rota güveni ve yeniden planlama

Rota güveni, mekân güvenlerinin ortalaması değildir. Ana amacın bağlı olduğu durak, geçiş, zaman penceresi ve kullanım koşulları birlikte değerlendirilir. İlgili bir geçişin fiziksel erişimi bilinmiyorsa bütün rota için erişim iddiası kurulamaz.

Yeniden değerlendirme tetikleri: kullanıcının geç başlaması, bir durağı reddetmesi, amaç/sınır değiştirmesi veya yeni kapanma, hava, kapasite ve ulaşım bilgisi. Sistem yalnız ulaşabildiği güncellemelerden yararlanır; erişmediği canlı bilgiyi izliyormuş gibi davranmaz.

Tamamlanan ziyaretler geriye dönük değiştirilmez. Kalan sürede ana amaç ve zorunlu koşullar korunur; önce ek faaliyetler azaltılır, sonra aynı rolü karşılayan seçenek aranır. Amaç artık gerçekleştirilemiyorsa bu söylenir. Kullanıcının onaylamadığı rezervasyon veya harcama yapılmaz.

Küçük tahmin dalgalanmaları sürekli rota değişikliğine yol açmamalıdır. Yeniden plan ancak uygulanabilirliği, ana amacı veya anlamlı bir yükü değiştiriyorsa sunulur. Kullanıcı planını koruyabilir; bilinen yeni engel bunun karşılığında saklanmaz. Planı erken bitirmek veya tek durakta kalmak da meşru sonuçtur.

## 11. Kullanıcı tercihleri zamanla nasıl öğrenilir?

**Kişi tek profile dönüştürülmez. Öğrenilen şey, belirli bağlamlarda yardımcı olabilecek ve kullanıcı tarafından değiştirilebilecek tercih işaretleridir.** “Sakin insan”, “lüks seven”, “aile profili” gibi kalıcı kimlikler kurulmaz.

Öncelik sırası:

1. Bu karar için açık amaç, koşul ve düzeltmeler.
2. Kullanıcının açıkça hatırlanmasını istediği, hâlâ geçerli tercihler.
3. Aynı bağlamda tekrarlanan açık geri bildirimler.
4. Anlamı sınırlı davranış işaretleri.

| İşaret | Öğrenilebilecek şey | Öğrenilemeyecek şey |
|---|---|---|
| “Bu aramada sessizlik önemli değil.” | Bu karar için ses tercihinin önceliği düşer. | Kullanıcı artık hiçbir zaman sessizlik istemez. |
| “Bunu hatırla: uzun yürüyüş istemiyorum.” | Kullanıcı kontrollü, değiştirilebilir tercih | Yaş, sağlık durumu veya fiziksel kapasite teşhisi |
| “Bu akşam çok uzakta.” | Aynı bağlamda ulaşım yüküne itiraz | O yerin kalitesiz olduğu veya hep reddedileceği |
| Yer sayfasını açma/kaydetme | İlgi veya daha sonra değerlendirme olasılığı | Gidildiği, beğenildiği veya bütün özelliklerin sevildiği |
| Yol tarifine geçiş | Ziyaret niyeti işareti | Gerçek ziyaret ve memnuniyet |
| “Konuşmak kolaydı; bekleme uzundu.” | Ses değerlendirmesi ile bekleme gözlemi ayrı ayrı | Bütün yer için olumlu/olumsuz puan |
| Hiç geri bildirim vermeme | Sonucun bilinmediği | Memnuniyet veya memnuniyetsizlik |

Davranıştan çıkarılan tercihler düşük etkili başlamalı, bağlamla sınırlandırılmalı ve kullanılmadıkça etkileri azalmalıdır. Kullanıcının açıkça hatırlattığı koşul, sessizce davranışla geçersizleştirilmez; güncelleme kullanıcı kontrolünde olur. Çelişen davranış hemen eski tercihi silmez; farklı gün, grup veya amaç olasılığı değerlendirilir.

Kişiselleştirme açıklanabilir olmalıdır: “Bu aramada kısa ulaşımı öne aldık.” Kullanıcı hatırlanan tercihleri görebilmeli, düzeltebilmeli, silebilmeli ve yalnız o oturum için kullanım isteyebilmelidir. Bu bir bağımsız profil sayfası gerektirmez. Hesapsız ve kalıcı öğrenme olmadan da temel karar desteği çalışmalıdır.

Konum geçmişi, hassas kimlik veya kişilerin birlikte görülme örüntülerinden gereksiz profiller üretilmez. Grup kararı bir kişinin kalıcı geçmişine yazılmaz. Anonim katkı vermek, kendiliğinden kişisel tercih geçmişi oluşturma izni değildir.

### Yeni seçeneklere açıklık

Motor yalnız daha önce seçilen türleri tekrar etmez. Ana amaç ve zorunlu koşulları karşılayan, benzer uygunlukta anlamlı farklı seçenekler değerlendirilebilir. Yenilik tek başına üstünlük değildir; bilinmeyen bir erişim koşulu “keşif” adına geçilemez.

Öğrenmenin kendi önerilerini doğrulayan bir döngüye dönüşmesi izlenir. Kullanıcı yalnız gösterilen yerleri seçebileceğinden, seçilmeyen veya hiç gösterilmeyen yerler sevilmiyor sayılmaz. Değerlendirmeler sunulan seçenek kümesini ve sıra etkisini hesaba katmalıdır.

## 12. Anonim kullanıcı katkıları sisteme nasıl beslenir?

Katkının görevi genel bir yer puanı üretmek değil, **belirli bir karar bilgisini doğrulamak, düzeltmek veya sınırlandırmaktır**. Kamuya açık yorum sayfası ve yorumcu itibarı sistemi kurulmaz.

Uygun katkı örnekleri: “Bugün 14.00'te iç salonda konuşurken ses yükseltmek gerekti mi?”, “Kullandığın girişte basamak var mıydı?”, “Bekleme yaklaşık ne kadardı?” Her soruda “bilmiyorum / gözlemlemedim / gitmedim” gibi dürüstçe yanıtlamama olanağı bulunur. Sessizliği onaylamaya yönlendiren soru kullanılmaz.

Süreç:

1. İlgili yer ve mümkünse bölüm belirlenir. Ziyaret zamanı ile katkı gönderme zamanı ayrılır.
2. Gözlem, kişisel tercih ve genel yargı birbirinden ayrılır. Serbest metin kabul edilirse de ham metin ürün çıktısı olmaz.
3. Gereksiz kişi bilgileri ve üçüncü kişileri tanımlayan ayrıntılar karar kanıtına taşınmaz.
4. Tekrar, aynı olay ve muhtemel ortak köken kontrol edilir. Aynı kişinin tekrarı veya bir etkinliğin çoklu anlatımı, farklı günlerden örüntü sayılmaz.
5. Katkı ilgili iddia ve bağlama eklenir; hemen genel yer niteliği oluşturmaz.
6. Yeni bilgi mevcut anlatımla çatışıyorsa güncellik veya kapsam yeniden değerlendirilir. Gerekirse ilgili iddia geri çekilir.
7. Yanlış olduğu sonradan anlaşılan katkının etkilediği çıkarımlar da düzeltilir; yalnız ham katkıyı kaldırmak yeterli değildir.

Anonimlik, katkı sahibinin kullanıcıya görünmemesini sağlar; içeride ne tutulduğu konusunda yanıltıcı söz verilmez. Sistem tekrar denetimi için sınırlı bir tanımlayıcı kullanıyorsa bunu “hiçbir iz tutulmuyor” diye anlatamaz. En az veriyle denetim hedeflenir; kalıcı konum takibi ve zorunlu kimlik belgesi varsayılan katkı şartı olmaz.

Tam anonimlik bağımsız katkı sayısını kesin bilmeyi zorlaştırır. Bu durumda kökeni belirsiz tekrarların kanıt etkisi sınırlandırılır; kusursuz manipülasyon tespiti iddia edilmez. Ziyaret yakınlığı sinyali varsa bile bir kişinin içeride olduğunu veya gözleminin doğru olduğunu tek başına kanıtlamaz.

Tek bir ayrıntılı olumsuz gözlem otomatik genel hüküm üretmez; fakat kritik bir mevcut iddiayı yeniden doğrulama nedeni olabilir. Açık, ilgili ve ciddi yeni çelişki varsa eski olumlu güvence inceleme boyunca durdurulabilir. Belirsiz suçlama, kamuya açık bir suçlama veya kapanma ilanı olarak yayımlanmaz.

Katkıların değeri çoğunluğa katılmalarıyla ölçülmez. Gerçek bir aykırı gözlemi “diğerleriyle uyuşmuyor” diye cezalandıran itibar modeli kurulmaz. Katkı miktarı, olumlu görüş veya sık ziyaret üzerinden puan/rekabet teşviki verilmez.

## 13. Yönetici tarafından eklenen mekân tecrübeleri

Yönetici kaynağın gözlem koşullarını daha iyi kaydedebilir; bu, kişisel beğenisini ürün gerçeğine dönüştürmez. **Yönetici ayrıcalığı yayın işlemini yönetme yetkisidir; kanıt gereksiniminden muafiyet değildir.**

Bir tecrübe şu ayrımları korur: gözlem zamanı, bölüm, kullanılan giriş/alan, faaliyet, özel etkinlik veya davet durumu; doğrudan görülen özellik, işletmeden duyulan bilgi ve kişisel değerlendirme. “Çok sevdim” uygunluk dayanağı değildir. “Cumartesi 20.00'de iç salonda karşılıklı konuşmak için sesi yükseltmek gerekti” dar kapsamlı ses gözlemidir.

Tek yönetici ziyareti, kontrol ettiği somut fiziksel özelliğe güçlü dayanak sağlayabilir. Haftanın tüm günleri için deneyim genellemesi sağlayamaz. Aynı geziye katılan üç yönetici, üç farklı zaman örüntüsü değildir. Davetli ziyaret, özel servis veya tanışıklık olağan deneyimi temsil etmeyebilir; kapsam değerlendirmesinde korunur.

Yönetici notu işletme veya anonim katkıyla çeliştiğinde unvana göre kazanmaz. Tarih, bölüm, doğrudanlık ve doğrulama kapsamı karşılaştırılır. Erişim gibi kritik geniş iddialar ve ciddi çelişkiler gerektiğinde ikinci bağımsız kontrol gerektirir; her düşük etkili kayıt için aynı iş yükü yaratılmaz.

İçeride düzeltme, askıya alma ve yeniden yayımlama gerekçesi izlenebilir olmalıdır. Bir yöneticinin “öne çıkar” tercihi organik uygunluk sırasına giremez. Yönetici tecrübesi eklemek, editoryal favoriler listesi oluşturmaz.

## 14. İşletme bilgileri hangi ağırlıkla kullanılır?

**Bütün işletme bilgilerine uygulanacak tek yüzde yoktur. Ağırlık iddia türüne, işletmenin o konudaki yetkinliğine, doğrudanlığa, güncelliğe ve doğrulama kapsamına bağlıdır.** Kimliği doğrulanmış işletme, bütün iddiaları doğrulanmış işletme demek değildir.

| Bilgi | İşletmenin kanıt rolü | Kullanım sınırı |
|---|---|---|
| Güncel tarife, menü, rezervasyon ve kullanım kuralı | Birincil kaynak olmaya uygundur. | Tarih, kapsam ve zorunlu ek ücretler açık olmalı; önemli çelişki çözülmeli. |
| Özel gün saatleri, geçici kapanma, tadilat | Doğrudan güncelleme kaynağı olabilir. | Doğru şube ve geçerlilik aralığı kontrol edilir; geçmiş duyuru kalıcılaştırılmaz. |
| Olanak varlığı ve kullanılabilirliği | Anlamlı doğrudan bildirimdir. | “Var” ile ziyaret saatinde kullanılabilir ayrılır. |
| Ayrıntılı fiziksel erişim bilgisi | İlgili dayanak sağlar. | Genel “erişilebiliriz” beyanı yetmez; gereken yolun kapsamlı doğrulaması aranır. |
| Fiilî doluluk veya rezervasyon kontenjanı | Zamanlı ve kapsamlı veri varsa kullanılabilir. | Toplam kapasite, boş kapasite değildir; eski bildirim canlı sayılmaz. |
| “Sessiz”, “en iyi”, “aile dostu”, “çok kaliteli” | Pazarlama/öznel beyan | Bağımsız deneyim doğrulaması ve uygunluk bonusu değildir. |
| Rakip hakkındaki iddia | Çıkar ilişkisi taşıyan bildirim | Rakibi cezalandırmak için doğrudan kullanılmaz; somut veri varsa ayrıca doğrulanır. |

İşletmeden gelen olumsuz bir kullanım bilgisi, örneğin “bilgisayarla çalışmaya izin verilmiyor”, işletmenin yetkili olduğu bir kural olarak anlamlıdır; sırf olumsuz diye bekletilmez. Olumlu pazarlama cümleleri aynı yetkiyle deneyim gerçeği kabul edilmez.

İşletme; yanlış bilgiyi düzeltebilir, dayanak sunabilir, tarihli değişiklik bildirebilir ve itirazının değerlendirilme durumunu öğrenebilir. Desteklenen olumsuz içgörüyü silemez, güven düzeyini elle seçemez, kendisini “sohbet için uygun” ilan ederek son kararı belirleyemez.

Gelecekte bilgi girişi için panel geliştirilirse istenenler, Product Language kavramlarına bağlı somut ve kapsamı belli bilgiler olmalıdır. Panelde daha fazla alan doldurmak organik sıra bonusu getirmez. Yeni ve doğru bilgi bir zorunlu koşulun doğrulanmasını sağlayabilir; bu bilgiye dayalı değişimdir, ödeme veya panel kullanımı ödülü değildir.

## 15. Kullanıcıya ne görünür, içeride ne kalır?

| Kullanıcıya görünür | Gerekçe |
|---|---|
| Anlaşılan amaç, sınırlar ve önemli varsayımlar | Kullanıcı yanlış anlaşılmayı düzeltebilsin. |
| İlgili somut yer bilgisi ve uygunluk nedeni | Seçimin neden anlamlı olduğunu anlayabilsin. |
| Önemli ödün, engel ve bilgi eksikliği | Yanlış beklentiyle karar vermesin. |
| İddianın geçerli olduğu saat, alan ve gerektiğinde kontrol tarihi | Bilginin kapsamını aşmasın. |
| Alternatifin farkı ve rota duraklarının işlevi | Başka seçeneğin neyi değiştirdiğini anlayabilsin. |
| Öğrenilmiş tercihlerin anlaşılır karşılığı ve kontrolü | Kişiselleştirmeyi düzeltebilsin veya kapatabilsin. |
| Yöntem, ticari ilişki açıklaması, düzeltme yolu ve gerekli atıflar | Ürünün sorumluluğunu ve bilgiye yaklaşımını değerlendirebilsin. |

| Sistem içinde kalır | Kullanıcıya yansıyan sonuç |
|---|---|
| Ham kaynak içeriği, yorumlar ve yorumcu bilgileri | Yalnız dayanaklı karar içgörüsü; ham pasaj gösterilmez. |
| Tekrar/köken ilişkileri, manipülasyon işaretleri | İddianın kullanılabilirliği; kanıtsız suçlama yoktur. |
| İç güven değerlendirmeleri, eşleşme değerleri, tercih ağırlıkları | Anlaşılır gerekçe ve gerekli sınır; yüzde/puan yoktur. |
| Aday eleme ve kararın izlenebilir kaydı | Gerekirse neden bu sonucun verildiği açıklanabilir. |
| Model talimatları, ara muhakeme ve deneme metinleri | Denetlenmiş nihai açıklama |
| Kaynak platform dökümleri ve sağlayıcı ayrıntıları | Gerekli atıflar ve kararın ilgili bilgi sınırı korunur. |

Kullanıcıya görünmemek sınırsız iç erişim veya süresiz saklama anlamına gelmez. Ham içerik, hassas katkı ve karar kayıtlarına erişim görevle sınırlandırılır; saklama ihtiyacı ve süresi tanımlanır. Gereksiz kişi profilleri, sosyal sınıf/gelir çıkarımları ve ticari uygunluk bonusları içeride kullanılmak üzere de üretilmez.

Kısa metin kullanıcıyı bilginin kesinliği konusunda yanıltamaz. Bir belirsizliğin teknik nedeni içeride kalabilir; karar üzerindeki etkisi kalamaz. Genel yöntem sayfası, belirli yerdeki kritik eksikliğin yerine geçmez.

## 16. API ileride motoru nasıl beslemeli?

API'nin ürün görevi, **kanıtı bağlamından koparmadan taşımak ve kararın anlamını bütün tüketicilerde korumaktır**. Bir sağlayıcının puanını veya kendi AI özetini Şamandıra hükmü olarak aktarmak değildir.

Her yeni bilgi aktarımı şu soruların cevaplarını taşımalı ya da hangisinin bilinmediğini açıkça belirtmelidir:

- Hangi yer, şube, bölüm, giriş veya güzergâh anlatılıyor?
- Hangi özellik, kural, durum veya gözlem bildiriliyor?
- Olay ne zaman gözlendi; bilgi ne zaman gönderildi; hangi zaman aralığı için geçerli?
- Bu doğrudan kayıt mı, öznel deneyim mi, çıkarım mı, tahmin mi?
- Asıl kaynak nedir; başka yerden türetilmiş veya kopyalanmış olabilir mi?
- Kapsam, birim ve koşullar nedir? Fiyat kişi başına mı, etkinlik toplamı mı; süre yalnız yolculuk mu?
- Bilgi nasıl kontrol edildi; kaynak “doğrulanmış” derken tam olarak neyi kastediyor?
- Kullanım, türetme, saklama, atıf ve silme koşulları nedir?
- Bu yeni bir gözlem mi, önceki kaydın düzeltmesi mi, geri çekilmesi mi?

Sağlayıcının boş alanı “yok”, hata yanıtı “kapalı”, eski yanıtı “şu an” anlamına gelmez. Düzeltme geldiğinde sadece yeni cümle eklenmez; geçersizleşen önceki iddia ve ona dayanan uygunluk/rota sonuçları yeniden değerlendirilir.

Harita, hava, işletme ve kullanıcı katkısı farklı kanıt türleri olarak kalır. İki API'nin aynı kaynağı taşıması bağımsızlığı artırmaz. Dış AI özetinde özgün dayanak ve kapsam izlenemiyorsa özet doğrulanmış olguya çevrilmez. Şamandıra'nın önceki çıktısının geri gelmesi de yeni kanıt sayılmaz.

### Motorun diğer bileşenlere verdiği anlam

Çıktı yalnız serbest paragraf olmamalıdır. Karar bağlamı, uygunluk durumu, gerçekten kullanılan gerekçeler, ödün/engel, önemli bilinmeyen, geçerlilik kapsamı, alternatif farkı ve varsa rota koşulları ayrıştırılabilir anlamlar olarak korunmalıdır. Bu bölüm alan adı veya teknik şema tanımlamaz.

Frontend gerekçeyi kısaltabilir; “bilinmiyor”u “uygun”a veya tahmini olguya çeviremez. AI cümleyi doğal kurabilir; yeni dayanak ekleyemez. Rota tek yer kararından yararlanabilir; kendi bağlantı ve toplam yük değerlendirmesini atlayamaz. İşletme girdisi motoru besleyebilir; motorun hükmünü doğrudan yazamaz.

Gerekli kullanıcı bağlamı aktarılır; bütün geçmiş her kaynağa gönderilmez. İzin verilmeyen veri kullanılmaz. Bir kaynağın kullanım koşulları ham yorum veya yorumcu göstermeyi gerektiriyor ve bu ürün kararıyla bağdaştırılamıyorsa o kaynak bu çıktı için kullanılmaz; farklı izin veya uygun kaynak aranır. Bu bir kullanım kabul kuralıdır; belirli bir sağlayıcının mevcut sözleşmesi hakkında hukukî hüküm değildir.

Geçici kesintide hangi yeteneğin kaybolduğu açık olur. Örneğin anlık ulaşım bilgisi yokken geçmiş süre güncelmiş gibi sunulmaz; yeterli dayanak varsa yaklaşık ve kapsamı belli bilgiye dönülür. Kritik zorunlu sınır artık değerlendirilemiyorsa olumlu sonuç sürdürülmez.

## 17. 81 şehir, 100.000+ yer ve milyonlarca kullanıcıda sürdürülebilirlik

Sürdürülebilirlik, bütün yerler için aynı anda zengin metin üretmekten gelmez. **Ortak karar dili, doğru yerde yeterli kanıt, değişikliklerin etkisini izleme ve karar başına makul işletim yükü** gerekir. Bu bölüm kapasiteyi ölçülmüş gibi sunmaz; ölçeğe çıkışın ürün şartlarını tanımlar.

### 17.1. Kapsam yer sayısıyla ölçülmez

Bir şehrin sisteme eklenmesi bütün amaçlar için kapsandığı anlamına gelmez. Kimliği bilinen yerler, belirli amaçlar için yeterli bilgisi olan yerler ve kritik koşulları doğrulanabilen yerler içeride ayrı izlenir. Bunlar yer kalitesi sınıfları veya yeni kullanıcı rozetleri değildir.

“81 şehirde varız” iddiası, yalnız şehir adlarının bulunmasına dayanamaz. Kapsam şehir × yer türü × amaç × ilgili zaman koşulu bakımından değerlendirilir. Bir şehirde gündüz yürüyüşe yardım edebilmek, akşam sohbet veya basamaksız rota kararına hazır olmak değildir. Referanslardaki özgün karar bilgisi olmadan şehir/ilçe sayfası açmama kuralı korunur.

### 17.2. Ortak dil, yerel kanıt

Kavram anlamları ülke genelinde aynı kalır. “Ucuz”, “yakın” ve “sakin” için şehirden şehre sessizce farklı ölçüler kullanılmaz. Göreli karşılaştırma varsa referans belirtilir; mümkün olduğunda kapsamı belli tutar, süre ve somut koşul kullanılır.

Benzer şehir veya kategoriler, hangi bilginin aranacağını öğretmek için kullanılabilir. Bir şehirdeki örüntü başka bir yerde olgu üretmez. Bölgesel önkabuller ve yer türü stereotipleri özellikle az verili yerlerin boşluğunu dolduramaz.

### 17.3. Her karar için her şeyi yeniden üretme

Yer hakkındaki tekrar kullanılabilir iddialar ile kullanıcı bağlamına bağlı uygunluk ayrı ele alınır. Kimlik ve temel olanak gibi görece kalıcı bilgi uygun süreyle yeniden kullanılabilir. Kullanıcının bütçesi, ziyaret saati ve o anki koşullar kararda yeniden uygulanır.

Bir arama için 100.000 yerin bütün metinlerini yeniden analiz etmek gerekmez. Coğrafya, amaç ve koşullar ilgili adayları daraltır; daha ayrıntılı değerlendirme ihtiyaç duyulan aday ve iddialara uygulanır. Daraltma yalnız popülerlik veya yüksek yorum hacmiyle yapılmaz; uygun olabilecek az bilinen yerleri daha başlangıçta dışlamamalıdır.

İşletim hedefi yalnız düşük maliyet değildir. Karar yanıt süresi, dış veri maliyeti, yeniden değerlendirme yükü ve insan incelemesi ihtiyacı karar kalitesiyle birlikte izlenir. Yoğunlukta önce metin zenginliği veya ikincil ayrıntı azaltılır; kritik kontrol ve dürüstlük kaldırılmaz.

### 17.4. Doğrulama ve yenileme önceliği

Öncelik dört etkene dayanır: yanlışlığın kullanıcı kararındaki etkisi, bilginin değişme hızı, mevcut belirsizlik/çelişki ve bilginin karar vermeyi ne ölçüde mümkün kılacağı. Kullanım talebi yardımcıdır; tek ölçüt değildir.

Sadece en çok tıklanan yerleri yenilemek, çok bilinen yerlerin daha çok önerildiği döngüyü güçlendirir. Kritik hata ve güncellik işleri yanında, az kapsanan şehir ve ihtiyaçların bilgilerini geliştirmek için düzenli kapasite ayrılır. Eksik kapsama sahip yerin kanıt eşiği düşürülmez; kanıt toplama önceliği iyileştirilir.

Her iddia ailesinin yenileme kuralı, sorumlusu ve olağandışı değişiklik tetikleri bulunur. Güncellik süresi ölçümlerle belirlenir. Tek bir ülke çapı süre bütün bilgi türlerine uygulanmaz.

### 17.5. İnsan incelemesi seçici ve denetlenebilir olmalı

Her yorumun elle okunması sürdürülebilir değildir. İnsan emeği; yanlış yer birleştirmeleri, kritik çelişkiler, geniş kapsamlı erişim iddiaları, şüpheli toplu katkılar ve örnekleme yoluyla kalite denetimine yoğunlaşır.

Rutin ve kapsamı açık bilgiler tanımlı kurallarla işlenebilir. Aynı kanıtı inceleyen farklı değerlendiricilerin aynı kavram ve kesinlik düzeyine ulaşması kontrol edilir. Uyuşmazlık yalnız çalışan hatası sayılmaz; sözlük veya kanıt kuralı belirsiz olabilir.

### 17.6. Düzeltme zinciri ve geri alma

Bir iddia geri çekildiğinde onu gerekçe olarak kullanan yer açıklaması, uygunluk kararı ve rota varsayımı belirlenebilmelidir. Sadece kaynak kaydının güncellenmesi yetmez. Halen gösterilen veya tekrar kullanılacak ilgili sonuçlar yeniden değerlendirilir.

Etkin bir rota gibi hâlâ geçerli kararı bozan yeni bilgi varsa, ürünün izin verilen iletişim kapsamı içinde kullanıcıya anlamlı değişiklik bildirilir. İlgisiz eski her karara bildirim gönderilmez. Kullanıcının geçmişte gördüğü sonucun hangi bilgiyle üretildiği, gerekli ve sınırlı saklama koşullarıyla denetlenebilir olur.

### 17.7. Model ve kural değişiklikleri

Yeni model daha akıcı yazdığı için doğrudan bütün şehirlere açılmaz. Önce ortak karar örneklerinde aynı kanıtla ürettiği sonuç, engel koruması, kapsam doğruluğu ve belirsizlik dili karşılaştırılır. Ardından sınırlı kapsamda davranış ve kullanıcı sonuçları izlenir.

Değişiklikler sürümlenir. Hangi kuralın, kavramın veya model değişiminin hangi sonucu etkilediği anlaşılabilir olmalıdır. Kritik hata artarsa ilgili yetenek/kapsam durdurulabilir veya önceki doğrulanmış davranışa dönülebilir. Kapsam büyümesi, kontrol edilmemiş karar türlerinin otomatik açılması değildir.

### 17.8. Sahiplik ve işletim sorumluluğu

| Sorumluluk | Hesap vermesi gereken konu |
|---|---|
| Ürün karar sorumlusu | Amaç, uygunluk kuralları, zorunlu sınırlar, açıklama ve özellik kabulü |
| Bilgi kalitesi sorumlusu | İddia ölçütleri, yenileme, çelişki çözümü ve kapsam |
| Değerlendirme sorumlusu | Kanıt/çıktı denetimi, hata oranları, kalibrasyon ve kapsam farkları |
| Veri kaynağı ve işletim sorumlusu | Kullanılabilirlik, köken, düzeltme/geri çekme ve kesinti davranışı |

Küçük ekipte roller aynı kişilerde bulunabilir; sorumluluklar kaybolmaz. Ticari ekip kaynak doğrulama sonucunu, uygunluk kuralını veya organik sıralamayı kendi hedefiyle değiştiremez. Kritik istisnanın gerekçesi ve kim tarafından verildiği içeride izlenebilir olur.

### 17.9. Başarı nasıl ölçülür?

Ana değerlendirme, **kullanıcının gerekçesini anlayabildiği bir karar verebilmesi ve yaşanan deneyimin anlatımla örtüşmesidir**. Tek bir metrik bütün ürünü temsil etmez.

| Ölçüm | Ne anlatır? | Yanlış yorumlama önlemi |
|---|---|---|
| Karar verebilme ve gerekçeyi doğru anlama | Seçenekler arasında bilinçli seçim veya vazgeçme mümkün mü? | Sadece “seçti” olayına bakılmaz; hangi ödünü anladığı araştırılır. |
| Beklenti–deneyim örtüşmesi | İlgili somut vaat ziyaretle karşılık buldu mu? | Ziyaret etmediyse veya geri bildirim yoksa başarı sayılmaz. |
| Karar çabası | Tekrarlanan arama, gereksiz soru ve bilgi bulma yükü azaldı mı? | Kısa oturum tek başına iyi sonuç değildir; vazgeçip kaçmış olabilir. |
| Kritik yanlış olumlu sonuç | Zorunlu koşul karşılanıyor denip karşılanmadı mı? | Ülke ortalamasıyla gizlenmez; tekil olay da incelenir. |
| Gereksiz değerlendirememe | Yeterli kanıt varken motor sustu mu veya iyi aday kaçtı mı? | Yalnız daha çok susarak hata oranını düşürmek ödüllendirilmez. |
| İddia/güven doğruluğu | Sağlam ve sınırlı anlatımlar fiilen ne ölçüde destekleniyor? | Tür, şehir, zaman ve kapsam bazında ayrılır. |
| Kapsam ve gösterim dağılımı | Az bilinen/az kapsanan uygun yerler erişilebilir mi? | Eşit gösterim zorlanmaz; açıklanamayan dışlama araştırılır. |
| Rota yapılabilirliği | Öngörülen süre, erişim ve kullanım koşulları birlikte gerçekleşti mi? | Her durağın tamamlanması başarı şartı değildir. |
| Düzeltme süresi ve etki temizliği | Hatalı bilgiye bağlı sonuçlar ne kadar hızlı düzeldi? | Yalnız ham kaydın güncellenme süresi ölçülmez. |
| Karar başına işletim yükü | Yanıt süresi, veri maliyeti, inceleme kapasitesi sürdürülebilir mi? | Maliyet azalması kritik hata artışını meşrulaştırmaz. |

Kullanıcı katkısıyla ölçülen sonuçlarda yanıt verenlerin herkesi temsil etmeyebileceği korunur. Geri bildirim oranı ve hangi bağlamlardan geldiği bilinir; küçük veya yanlı örneklerden ülke çapında başarı ilan edilmez. Kullanıcı araştırması ve bağımsız iddia denetimi, davranış ölçümlerini tamamlar.

### 17.10. Önerilerin gerçek koşulları değiştirmesi

Milyonlarca kişiye aynı “düşük yoğunluk” seçeneğini önermek, zamanla o örüntüyü değiştirebilir. Motor kendi öneri etkisini de değişim ihtimali olarak ele almalıdır. Toplu gösterim veya yol tarifine geçiş, fiilî ziyaret ve doluluk sayılmaz; ilgili bilginin yeniden kontrol edilmesini gerektiren sınırlı bir işarettir.

Güncel ve kullanılabilir kapasite bilgisi varsa karara katılır. Benzer uygunluktaki seçeneklerin anlamlı çeşitliliği korunabilir; kullanıcılar açık ihtiyaçlarına daha az uyan yerlere sistemin yükünü dağıtmak amacıyla gönderilmez. Bir yerin görünürlük kazanmasından sonra anlatılan yoğunluk ile gözlenen deneyim ayrışıyorsa önce iddia ve tahmin güncellenir. Önceki “sakin” anlatısını korumak için ters kanıt bastırılmaz.

## 18. Karar Motoru'nun bağlayıcı prensipleri

1. **Karar birimi bağlamsal uygunluktur.** Evrensel yer üstünlüğü üretilmez.
2. **Bugünkü açık ihtiyaç önceliklidir.** Öğrenilmiş geçmiş onu geçersiz kılamaz.
3. **Zorunlu koşul telafi edilemez.** Başka avantajlar engeli ortadan kaldırmaz.
4. **Bilinmeyen, yok veya uygun demek değildir.** Eksik bilginin kendi sonucu vardır.
5. **Güven iddiaya aittir.** Yer geneli ortalama güven, kritik eksikliği örtemez.
6. **Bilgi türü korunur.** Olgu, bildirim, çıkarım ve tahmin aynı kesinlikle konuşmaz.
7. **Kanıtın kapsamı aşılmaz.** Saat, bölüm, mevsim ve kullanıcı amacı taşınırken yeniden değerlendirilir.
8. **Tekrar bağımsızlık değildir.** Aynı kökenin çoğalması güveni yapay biçimde artırmaz.
9. **Anlatım dayanağı aşamaz.** “Olabilir” dayanıksız iddiaya izin vermez.
10. **Gerekçe kararla birlikte doğar.** Sonradan ikna amacıyla uydurulmaz.
11. **Vazgeçme nedeni kararın parçasıdır.** Önemli ödün, engel ve belirsizlik saklanmaz.
12. **Kullanıcıya içgörü verilir.** Ham yorum, yorumcu ve yorum puanı ürün çıktısı değildir.
13. **Alternatifin farkı açıklanır.** Yakınlık veya benzer kategori tek başına yeterli değildir.
14. **Çeşitlilik uygunluğu bozamaz.** Keşif, zorunlu sınırları ve ana amacı korur.
15. **Rota bütün olarak değerlendirilir.** Durakların toplamı, uygulanabilir deneyim dizisi olmak zorundadır.
16. **Az veya hiç önermemek geçerlidir.** Sonuç sayısını doldurmak amaç değildir.
17. **Öğrenme kullanıcı kontrolündedir.** Değiştirilebilir, silinebilir ve bağlama bağlı kalır.
18. **Kaynağın yetkisi konuya bağlıdır.** İşletme veya yönetici statüsü genel doğruluk değildir.
19. **Ticari çıkar kararı satın alamaz.** Uygunluk, güven ve organik sıra ödeme avantajından bağımsızdır.
20. **Kapsam dürüstçe büyür.** Veri azlığı kalite düşüklüğü değildir; bilgi açığı uydurmayla kapanmaz.
21. **Düzeltme bağlı sonuçlara yayılır.** Hatalı kaynağın etkisi öneri ve rotadan da çıkarılır.
22. **Aynı kavram her bileşende aynı anlama gelir.** API, AI ve Frontend kendi uygunluk tanımlarını üretemez.
23. **Başarı gerçek karar faydasıdır.** Tıklama, ürün süresi, rezervasyon ve durak sayısı tek başına başarı değildir.
24. **Karar denetlenebilir ve geri alınabilir olmalıdır.** Kural/model değişikliği izlenir; hatalı yetenek sınırlandırılabilir.

### Yeni özellikler için zorunlu kabul kapısı

Her yeni özellik, geliştirme kapsamına alınmadan önce şu sorulara somut cevap vermelidir:

| Kabul sorusu | Gerekli cevap |
|---|---|
| Hangi karar anına yardım ediyor? | Kullanıcı, amaç, sınır ve bugün yaşanan belirsizlik |
| Mevcut dil ve mimaride yeri ne? | Kullandığı kavramlar; mevcut yapının neden yeterli/yetersiz olduğu |
| Hangi dayanakla hangi sonucu üretiyor? | Gerekli kanıt, kapsam, bilgi türü ve güven kuralı |
| Ne zaman susacak veya daralacak? | Bilinmeyen, çelişki, eskime ve kesinti davranışı |
| Hangi zorunlu koşulu yanlış geçirebilir? | Kritik hata senaryosu ve onu önleyen kural |
| Kullanıcı neyi anlayıp değiştirebilir? | Gerekçe, ödün, önemli sınır ve kontrol |
| Hangi bilgi ve emeği istiyor? | Veri ihtiyacı, kullanıcı çabası ve işletim yükü |
| Ticari veya davranışsal yanlılık yaratıyor mu? | Uygunluk ve gösterim üzerindeki etkilerin denetimi |
| İşe yaradığını nasıl anlayacağız? | Karar faydası, yanlış iddia, gereksiz susma ve kapsam ölçümleri |
| Hangi sonuçta daraltılacak veya kaldırılacak? | Önceden belirlenmiş başarısızlık ve geri alma ölçütleri |

İlkeyle çelişen özellik ilgi görse de kabul edilmez. Fayda veya kanıt eşiği belirsizse küçük kapsamda sınanır; belirsizliği ürünün tamamına yayılmaz. Sayısal yayın eşikleri, ilgili karar türü için doğrulama sonuçları görülmeden evrensel sabit olarak belirlenmez.

## 19. Diğer ürünlerden çıkarılan dersler ve bu önerinin eleştirisi

### Güncel ürünleri doğru okumak

Şamandıra'nın varlık gerekçesi “diğerleri yalnız puan gösterir, biz AI kullanırız” olamaz. Google Maps'in 12 Mart 2026 tarihli Ask Maps duyurusu doğal dille karmaşık ihtiyaçları anlama ve kişiselleştirilmiş önerileri; Tripadvisor Trips AI ile planlamayı; Yelp'in Review Insights duyurusu yorumlardaki konu bazlı değerlendirmeleri açıklıyor. Benzer araçların varlığı, Şamandıra'nın karar kurallarını ve hesap verebilirliğini daha önemli kılar. [Google Ask Maps](https://blog.google/products-and-platforms/products/maps/ask-maps-immersive-navigation/), [Tripadvisor Trips](https://www.tripadvisor.com/Trips), [Yelp Review Insights](https://blog.yelp.com/news/end-of-year-product-release-2024/).

Aşağıdaki güçlü yönler resmî ürün açıklamalarına dayanır. Sınırlılık sütunu, **bu yeteneklerin Şamandıra'nın karar ihtiyacını tek başına karşılamakta nerede yetersiz kalabileceğine dair ürün değerlendirmesidir**; rakiplerin iç motorları hakkında ölçülmüş hata iddiası değildir. Özelliklerin her ülkede ve kullanıcıda aynı kapsamda bulunduğu varsayılmaz.

| Ürün | Güçlü taraf ve dayanak | Şamandıra açısından sınırlılık/öğrenme |
|---|---|---|
| Google Maps | Yer, navigasyon, doğal dille keşif ve alternatif yol ödünlerini birlikte ele alıyor. [Resmî duyuru](https://blog.google/products-and-platforms/products/maps/ask-maps-immersive-navigation/) | “Maps yalnız en kısa yolu bulur” karşıtlığı geçersizdir. Şamandıra'nın savunacağı şey belirli zorunlu koşulları, kanıt sınırlarını ve deneyim dizisini tutarlı biçimde korumaktır. |
| Tripadvisor | Kaydedilen yerler, ortak planlama ve AI önerileriyle gezi düzenlemeyi destekliyor. [Trips](https://www.tripadvisor.com/Trips) | Geziyi düzenlemek küçük bir günlük kararın yükünü kendiliğinden azaltmaz. Şamandıra tek yer ihtiyacını uzun plana büyütmemeli; genel beğeniyi bağlamsal uygunluğa eşitlememeli. |
| Yelp | Review Insights konu bazlı duygu değerlendirmeleriyle yorumlara erişimi kolaylaştırmayı amaçlıyor. [Ürün duyurusu](https://blog.yelp.com/news/end-of-year-product-release-2024/) | Konu hakkındaki olumlu duygu, belirli kullanıcı amacı veya zorunlu koşul için yeterlilik değildir. Şamandıra ses gözlemini, kişinin sese tepkisini ve amaçla ilişkisini ayırmalı. |
| Foursquare | Yer verisi ve konumsal bağlam sağlar; veri doğrulamada insan, yazılım ve üçüncü taraf yollarını birlikte tanımlar. [Places](https://foursquare.com/products/places/), [Places Overview](https://docs.foursquare.com/data-products/docs/places-overview) | Zengin yer/ziyaret bilgisi o ziyaretteki niyeti ve memnuniyeti kendiliğinden göstermez. Şamandıra köken, şube, zaman ve kullanım kapsamına dikkat etmeli. |
| Airbnb Experiences | Yerel kişilerce yürütülen faaliyetler, program ve katılım koşullarıyla deneyimi somutlaştırır. [Experiences](https://www.airbnb.com/host/experiences) | Programlı ve rezervasyona dayanan deneyim modeli, spontane ve ücretsiz yer seçimlerinin tamamını temsil etmez. Şamandıra amaç ve sıra açıklığını almalı; her faaliyeti satın alınan pakete çevirmemeli. |
| Apple Maps | Yolculuk biçimleri, yönlendirme ve rotaya durak ekleme gibi ulaşım görevlerini destekler. [Apple Maps kullanıcı kılavuzu](https://support.apple.com/en-mide/guide/iphone/iph02f94fc1c/ios) | Navigasyonun sürekliliği, eklenen durakların neden birlikte anlamlı olduğunu kendiliğinden çözmez. Şamandıra deneyim ilişkisini üstlenirken ulaşım gerçekliğini korumalı. |

### Kendi önerime itirazlar ve nihai kararlar

| İtiraz | Gerçek risk | Karar ve doğrulama yolu |
|---|---|---|
| “Tek puan olmadan sıralama keyfî kalır.” | Gizli ve değişken tercih ağırlıkları açıklamayı anlamsızlaştırabilir. | Karşılaştırma öncelikleri ve kullanılan gerekçeler izlenir. Aynı kanıt/bağlamda açıklanamayan sıra değişimi incelenir. |
| “Katı kanıt kuralları az verili yerleri yok eder.” | Eski ve çok görünür yerler kalıcı avantaj kazanabilir. | Bilinmeyen kalite eksisi değildir; kapsam geliştirme kapasitesi ayrılır. Dar ama yeterli bilgiyle öneriye izin verilir, kritik koşul uydurulmaz. |
| “Yorumları kaldırmak kullanıcı denetimini azaltır.” | Kullanıcı yalnız Şamandıra'nın yorumuna mahkûm kalabilir. | Somut gerekçe, kapsam, ilgili güncellik, yöntem ve düzeltme yolu korunur. Ham yorum göstermemek motorun sorumluluğunu artırır. |
| “Kapsamı daraltmak her yer için yüzlerce durum üretir.” | Bakım yükü ve metin karmaşası büyüyebilir. | Yalnız kararı değiştiren, kanıtı olan zaman/alan ayrımları üretilir. Bütün olası kombinasyonlar doldurulmaz. |
| “Çok belirsizlik anlatmak karar verdirmez.” | Kullanıcı yeniden araştırmacıya dönüşebilir. | Yalnız kararın sonucunu değiştiren sınırlar öne çıkarılır. Kritik eksiklik kısa metin uğruna gizlenmez. |
| “Deneyim rotası fazla planlayıcı olabilir.” | Kullanıcı dinlenmek isterken plan tamamlama baskısı doğabilir. | Her durak gerekçelenir; tek yer veya erken bitiş geçerli sayılır. Tamamlama sayısı başarı metriği değildir. |
| “İşletmeye dayanmak reklamı gerçeğe dönüştürür.” | Pazarlama beyanı olumlu uygunluk üretebilir. | Kural/tarife yetkisi ile deneyim iddiası ayrılır. Genel işletme doğrulama rozeti bütün iddiaları geçiremez. |
| “Anonimlik manipülasyonu kolaylaştırır.” | Bağımsız kişi sayısı belirsiz olabilir. | Kökeni belirsiz tekrarın etkisi sınırlanır; düşük veri toplamayla yapılan kontrolün sınırı kabul edilir. |
| “Kişiselleştirme kişiyi geçmişine kapatır.” | Daha önce gösterilen seçenekler öğrenmeyi daraltır. | Açık ihtiyaç üstün tutulur; bağlamlı öğrenme, sıfırlama ve benzer uygunlukta farklı seçenekler korunur. |
| “Doğru görünmek için sürekli bilmiyorum diyebilir.” | Motor kullanıcının gerçek karar ihtiyacını karşılamaz. | Yanlış olumlu sonuçla birlikte gereksiz susma ve kaçırılan uygun seçenekler ölçülür. |
| “Güzel gerekçe yanlış kararı örtebilir.” | Akıcı metin sahte kesinlik yaratabilir. | Gerekçe yalnız kararın gerçek dayanağından gelir; kanıt-kapsam denetimi anlatım beğenisinden önce gelir. |

Bu eleştirilerden sonra savunulan yaklaşım; sabit yer puanı, yorum özeti ürünü veya yalnız genel bir AI sohbeti değildir. **Kapsamı belli iddialar, bağlama bağlı uygunluk, telafi edilemeyen sınırlar ve açıklanabilir seçenek ilişkileriyle çalışan tek bir karar çerçevesidir.** Farkın değeri, kullanıcı araştırması ve gerçek deneyim karşılığıyla gösterilmek zorundadır; bu belge tek başına rekabet üstünlüğü kanıtı değildir.

## 20. Kabul senaryoları ve uygulamaya geçiş sınırı

Bu senaryolar gelecekteki bileşenlerin ortak ürün kabul örnekleridir; çalıştırılmış yazılım testi veya doğrulanmış saha sonucu değildir.

| Senaryo | Beklenen karar |
|---|---|
| Çok sevilen bir yerde gerekli basamaksız erişimin olmadığı biliniyor | Kullanıcının bu koşulu için uyumlu önerilere girmez. |
| Aynı yerde erişim hiç bilinmiyor | Erişim var/yok denmez; doğrulanmış eşleşme gibi sunulmaz. |
| Sessiz olduğu yalnız hafta içi öğlen biliniyor, arama cuma gecesi | Gündüz çıkarımı geceye taşınmaz; ilgili uygunluk değerlendirilemeyebilir. |
| İşletme “çok sakin” diyor, ilgili akşam gözlemleri yüksek müziği destekliyor | Pazarlama beyanı gözlemleri bastırmaz; kapsamlı ses sonucu kullanılır. |
| İki sağlayıcı aynı işletme duyurusunu kopyalamış | Tek köken kabul edilir; bağımsız güven artışı oluşmaz. |
| Yeni bir yerin deneyim katkısı yok, gereken somut koşullar yeterince doğrulanmış | Sırf yeni diye elenmez; yalnız desteklenen amaç ve kapsam için değerlendirilir. |
| Kullanıcı geçen hafta sessizlik istedi, bugün canlı müzik istiyor | Bugünkü açık amaç kullanılır; geçmiş koşul dayatılmaz. |
| Kullanıcı bir yere baktı ama gitmedi | Ziyaret veya memnuniyet öğrenilmez. |
| İki uygun durak tek tek açık, ikinciye varış son girişten sonra | Rota uygulanabilir sayılmaz; sıra veya aday yeniden değerlendirilir. |
| Uygun açık hava planının yedeği de aynı yağışa bağlı | Yedek bağımsız çözüm sayılmaz; ortak risk açıklanır. |
| Hava verisi geçici olarak alınamıyor | “Yağış yok” sonucu üretilmez; bilinen kapsamla sınırlı davranılır. |
| Bütçe aralığının üst tarafı kullanıcının zorunlu sınırını aşıyor | “Bütçene uyuyor” denmez; belirsizlik veya uyuşmazlık korunur. |
| Kullanıcı bütçeye uymayan bir yeri adıyla arıyor | Yer bulunur; bulunabilirlik öneri uygunluğu anlamına gelmez. |
| Ücretli işletme ile ücretsiz kayıt aynı kanıt ve bağlama sahip | Ödeme, güven ve organik sırada avantaj sağlamaz. |
| Yer kimliği hatalı birleştirilmiş ve sonradan ayrılmış | Bağlı iddialar, öneriler ve rotalar yeniden değerlendirilir. |
| İki kişi için ortak çözüm yok; birinin zorunlu koşulu diğerinin tercihiyle çatışıyor | Çatışma açıklanır; çoğunluk veya hesap sahibi adına koşul kaldırılmaz. |
| Metin kısaltılırken önemli “akşam bilgisi yok” sınırı kaybolmuş | Çıktı kabul edilmez; sınır geri getirilir veya iddia daraltılır. |
| Çok az seçenek bilinen bir şehirde sonuç bulunamıyor | “Burada uygun yer yok” değil, bilgi kapsamını belirten ifade kullanılır. |
| Kullanıcı rotanın bir durağında kalıp devam etmek istemiyor | Ret veya başarısız kullanıcı sayılmaz; kalan plan isteğe göre değerlendirilir. |

### Uygulama öncesinde tamamlanması gereken doğrulamalar

Bu belge ürün yönünü ve davranış kurallarını belirler. Her karar yeteneği yayımlanmadan önce ilgili kavram için kanıt kabul ölçütleri, güncellik politikası, hata ölçümü, insan incelemesi sınırı ve kesinti davranışı somutlaştırılmalıdır. Bunlar temel felsefeyi yeniden tartışma gerekçesi değil, tanımlanan kararı güvenilir biçimde uygulama yükümlülüğüdür.

Kullanıcılarla özellikle şu ayrımlar sınanmalıdır: tercih–zorunlu koşul, ödün–engel, geçmiş örüntü–canlı durum, koşula bağlılık–bilinmeyen. Kullanıcının kısa metinden bunları doğru anlaması gerekir. İçeride de farklı değerlendiricilerin aynı kanıtı benzer kapsam ve güvenle yorumlaması aranır.

Ölçek kademeli büyütülür: önce seçilmiş amaç ve coğrafyalarda tek yer kararı; ardından yeterli bağlantı bilgisi bulunan sınırlı rota bağlamları; sonra aynı kabul kurallarıyla daha geniş kapsam. Bu sıra zorunlu bir geliştirme takvimi değildir; tek yer kararının güvenini kurmadan rota anlatımının belirsizliği çoğaltmasını önleyen yayın bağımlılığıdır.

Belgenin bağlayıcı karar cümlesi:

> **Bu yer veya ziyaret dizisi, yapmak istediğin şey için şu nedenle anlamlı. Seçersen şu koşulu kabul etmen gerekir. Kararını etkileyen şu noktayı ise henüz yeterince bilmiyoruz.**

## Ek — Tek bir kararın baştan sona örneği

Bu örnek gerçek yer önerisi değildir. Amaç, aynı kuralların tek bir seçimde nasıl birleştiğini göstermektir.

**İstek:** “Salı 14.00'te iki kişi bir saat sohbet edeceğiz. İç salona basamaksız erişim şart. Başlangıç noktamızdan yürüyerek en fazla 15 dakika olsun. Daha az müzik tercih ederiz.”

Anlaşılan amaç sohbet; zorunlu koşullar belirtilen iç salona basamaksız erişim, bir saatlik kullanımın mümkün olması ve 15 dakikalık ulaşım sınırıdır. Düşük müzik tercihtir. Kullanıcı bütçe belirtmediği için kesin bütçe sınırı uydurulmaz. Aşağıdaki karşılaştırmada çalışma saatleri ve süre bilgileri ilgili ziyaret için yeterli dayanağa sahip varsayılmıştır.

| Aday | İlgili dayanaklar | Motorun kararı |
|---|---|---|
| A | İç salona basamaksız erişim doğrulanmış; bir saat kalış mümkün; yürüyüş 10–12 dakika; salı gündüz düşük müzik için sağlam çıkarım | Uygunluğu desteklenen; açık düşük müzik tercihini karşılaması gerekçede kullanılır. |
| B | Aynı zorunlu koşullar doğrulanmış; yürüyüş 6–8 dakika; konuşmayı engellemeyen fakat daha belirgin müzik için sağlam çıkarım | Uygunluğu desteklenen; daha kısa ulaşım karşılığında daha belirgin müzik sunan alternatif. |
| C | Yürüyüş 5 dakika; müzik düşük; iç salonun erişimi bilinmiyor | Bu istek için değerlendirilemeyen; doğrulanmış eşleşmelere girmez. |
| D | Yürüyüş 8 dakika; iç salona yalnız merdivenle erişildiği doğrulanmış | İhtiyaçla uyuşmayan; düşük müzik olsa bile zorunlu koşulu geçemez. |
| E | Gündüz düşük müzik biliniyor; salı günü kapalı olduğu güncel biçimde doğrulanmış | Bu ziyaret için uygun önerilere girmez. |

İlk seçkide A ve B bulunur; üç ila beş hedefini doldurmak için C eklenmez. A, kullanıcının açık müzik tercihini daha iyi karşılar. B daha kısa ulaşım farkıyla anlamlıdır; ikisinin de zorunlu ulaşım sınırını sağlaması bu ödünü meşru kılar. B'nin daha yakın olması D'nin erişim engelini veya C'nin eksikliğini telafi edemez.

Kullanıcıya verilebilecek sonuç:

> “A, salı gündüz düşük müzik düzeyiyle bir saatlik sohbet isteğini destekliyor. Kullanacağınız iç salona erişim basamaksız; seçtiğiniz başlangıçtan yürüyüş yaklaşık 10–12 dakika. Daha kısa yürümek istersen B 6–8 dakika uzaklıkta; müzik daha belirgin.”

Bu cümle, yer bulunacağı veya hiç beklenmeyeceği garantisi içermez. Bu koşullar kararı etkileyebilecek düzeyde bilinmiyorsa ayrıca belirtilmeli; tam bir saatlik ziyaretin mümkün olduğu sonucunu taşıyamıyorsa öneri daraltılmalıdır.

Kullanıcı “Daha kısa yürümek daha önemli” derse B öne geçebilir. Bu yeni öncelik, yalnız mevcut karar için geçerlidir. Kullanıcı “A'nın yanına bir yer daha ekle” demediği için rota oluşturulmaz. Aynı konuşmada zorunlu erişim koşulu kaldırılmadıkça C ve D uygun alternatiflere dönüşmez.


---

## Belge ilişkileri — depoya aktarım eki

### Bu dokümanın bağlı olduğu belgeler

- [00-urun-felsefesi.md](./00-urun-felsefesi.md)
- [01-bilgi-mimarisi.md](./01-bilgi-mimarisi.md)
- [02-product-language.md](./02-product-language.md)

### Bu dokümanın etkilediği belgeler

- [04-sistem-mimarisi.md](./04-sistem-mimarisi.md)

### Bundan sonra okunması gereken belge

[04-sistem-mimarisi.md](./04-sistem-mimarisi.md)
