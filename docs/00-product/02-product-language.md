---
title: "02 Product Language"
version: "1.0"
status: "kabul-edilmis-referans"
phase: "urun-tanimi"
last_update: "2026-09-13"
depends:
  - "00-urun-felsefesi.md"
  - "01-bilgi-mimarisi.md"
affects:
  - "03-karar-motoru.md"
  - "04-sistem-mimarisi.md"
author: "Codex; kabul yetkisi: proje sahibi"
---

> Depoya aktarım notu — 13 Eylül 2026: Kaynak: 2-Ürün Veri Modeli görevinin nihai yanıtı (01a09907-38c8-7832-ad1b-08a9827c29b3). Kullanıcının bu görevdeki beyanıyla kabul edilmiş referanstır. Özgün gövde korunmuş; yalnız metadata, köken notu ve belge ilişkileri eklenmiştir. Gövdedeki öneri/durum ifadeleri tarihsel haliyle bırakılmıştır.

Şamandıra’nın ürün dili için önerdiğim temel karar şu:

**Yeri özellikleriyle anlarız. Kullanıcının ihtiyacıyla birlikte değerlendiririz. Sonucu gerekçesi ve sınırlarıyla anlatırız.**

Bu üç işi birbirine karıştırmamalıyız. “Müzik yüksek” yer hakkında bir değerlendirmedir. “Uzun sohbet için zorlayabilir” bu değerlendirmenin bir ihtiyaca göre anlamıdır. “Sana uygun” ise kullanıcının ne istediğini bilmeden kurulamayacak bir sonuçtur.

Kabul edilmiş Ürün Felsefesi ve Bilgi Mimarisi’ni esas aldım. Aşağıdaki sözlük; onların kategori, deneyim, koşul ve coğrafya ayrımını korur. Yeni sayfalar, genel kalite sıralamaları veya kullanıcıya gösterilecek yorum yapıları önermez.

Bu, savunduğum tek ürün dili önerisidir. Kavramların kullanıcı kararına etkisine ilişkin gerekçeler ürün hipotezidir; kullanıcılarla doğrulanmış sonuçlar gibi sunulmamalıdır.

**1. Önce hangi yaklaşımları eledim?**

| Yaklaşım | Çekici tarafı | Neden temel dil olamaz? |
|---|---|---|
| Atmosfer, enerji, tempo gibi soyut eksenlerle yer profili | Kısa ve kolay karşılaştırılabilir görünür. | Aynı sözcük farklı insanlar için farklı şeyler anlatır. Bağımsız puanlar aynı kanıtı tekrar sayabilir. |
| Yüzlerce özellikten oluşan yer kataloğu | Kapsamlıdır; genişlemeye açık görünür. | Kullanıcı, özelliklerin kendi ihtiyacı açısından anlamını yine kendisi çözmek zorunda kalır. |
| Yalnızca “sohbet için”, “çocuklarla”, “çalışmak için” etiketleri | Kullanıcının amacına doğrudan yaklaşır. | Etiketin neden verildiği kaybolur. Yeni ihtiyaçlar geldikçe etiket sayısı büyür; koşullar görünmez olur. |
| Her yer için serbest AI anlatısı | Doğal ve akıcıdır. | Aynı sözcüklerin anlamı, kesinlik düzeyi ve karşılaştırma zemini kayabilir. |
| Tek uygunluk puanı | Sonucu basitleştirir. | Vazgeçilmez koşulları, ödünleri ve bilinmeyenleri tek sayıda eritir. |

Seçtiğim yaklaşım, **somut yer bilgisi ile bağlama bağlı uygunluk açıklamasını birleştirir.** Kullanıcı az sayıda anlamlı cümle görür; bu cümlelerin arkasında tutarlı kavramlar bulunur.

---

**2. Ürün dilinin omurgası**

Şamandıra’nın bütün değerlendirmesi dört kavram ailesine dayanmalı:

| Kavram ailesi | Cevapladığı soru | İçeriği |
|---|---|---|
| **Karar bağlamı** | Ne yapmak istiyorum, hangi sınırlar içinde? | Amaç, tercih, zorunlu koşul, ziyaret bağlamı |
| **Yer bilgisi** | Burası nedir, burada neyle karşılaşabilirim? | Kimlik, tür, coğrafya, olanaklar, ortam ve ziyaret koşulları |
| **Karar anlamı** | Bunlar benim seçimim açısından ne ifade ediyor? | Uygunluk, tercih gerekçesi, ödün, engel, alternatif farkı |
| **Bilginin sınırı** | Bu anlatıma hangi koşullarda dayanabilirim? | Dayanak, güven, geçerlilik bağlamı, güncellik, bilinmeyenler |

Bunlar kullanıcıya sunulacak dört bölüm adı değildir. Ürünün ortak düşünme dilidir.

**“Yer profili” bu bilgilerin bütünü olabilir; kendi başına yeni bir özellik veya puan değildir.**

---

**3. Karar bağlamının nihai sözlüğü**

| Kavram | Kullanıcı açısından anlamı | Neden var; kararı nasıl değiştirir? | Ürün içindeki yeri |
|---|---|---|---|
| **Amaç** | “Orada ne yapmak istiyorum?” | Aynı özellik farklı amaçlarda farklı anlam taşır. Kalabalık, canlı bir buluşmayı destekleyip sessiz okumayı zorlaştırabilir. | Uygunluk değerlendirmesinin başlangıcı. Kullanıcıya anlaşılmış hali gösterilir. |
| **Tercih** | “Olursa seçimimi iyileştirir.” | Seçenekler arasında öncelik kurar; gerektiğinde ödün verilebilir. | Amaçtan ayrı tutulur. Manzara, daha az ses, kısa ulaşım gibi. |
| **Zorunlu koşul** | “Bu sağlanmıyorsa seçemem.” | Diğer avantajlarla telafi edilemez. | Eşleşmenin sınırıdır. Bütçe üst sınırı veya basamaksız erişim gibi. |
| **Ziyaret bağlamı** | “Ne zaman, kimlerle, nereden ve ne kadar zaman ayırarak?” | Uygunluğun hangi ziyaret için değerlendirildiğini belirler. | Zaman, birlikte gidilen kişiler, başlangıç noktası, ulaşım biçimi ve zaman sınırı bunun altındadır. |

Burada üç kesin ayrım var:

- **Tercih ile zorunlu koşulun farkını ürün kendi başına uyduramaz.** “Ucuz olsun” ifadesinden kesin bir bütçe sınırı çıkarılmaz.
- **Birlikte gidilen kişiler, otomatik ihtiyaç paketi değildir.** “Çocukla” demek otomatik olarak oyun alanı istemek değildir. Grup büyüklüğü de uzun sohbet istemek anlamına gelmez.
- **Ziyaret bağlamı, kalıcı kullanıcı kimliği değildir.** Bu akşamki sakinlik ihtiyacı kişiyi “sakin mekân insanı” yapmaz.

Birden fazla amaç birlikte bulunabilir. “Yemek yiyip uzun konuşmak” tek etikete sıkıştırılmaz. Amaçlar çatışıyorsa çatışma gizlenmez.

Bu kavramların dayanağı öncelikle kullanıcının açık ifadesidir. Geçmiş davranış ancak ikincil, değiştirilebilir bir işaret olabilir. Anlaşılmayan veya söylenmeyen ihtiyaç tamamlanmış gibi gösterilmez.

---

**4. Yer hakkında konuşacağımız temel kavramlar**

Aşağıdaki kavramların her biri bağımsız bir karar sorusuna cevap verir. Alt ayrıntılar ancak ilgili yer türünde ve karar bağlamında anlamlıysa kullanılır.

| Kavram | Kullanıcı açısından anlamı | Neden var; kararı değiştirir mi? | Altında ne bulunur? |
|---|---|---|---|
| **Yer kimliği** | “Tam olarak hangi yer?” | Evet. Yanlış şube veya aynı adlı başka bir yer bütün değerlendirmeyi geçersiz kılar. | Ad, ayırt edici konum, şube veya giriş ayrımı |
| **Yer türü** | “Burası ne?” | Evet. Temel beklentiyi kurar; tek başına uygunluğu kanıtlamaz. | Kafe, müze, park gibi sınıflandırmalar |
| **Coğrafi bağlam** | “Nerede arıyorum; yer nerede?” | Evet. Arama alanını ve çevre içindeki konumu belirler. | Şehir, ilçe, tanınabilir çevre; şehir üstü gruplama olarak bölge |
| **Olanaklar** | “Burada ne yapabilirim; hangi imkânlar var?” | Evet. Bir amacın mümkün olup olmadığını belirler. | Yeme-içme, yürüyüş alanı, sergi, oturma alanı; ilgili tesis ve hizmetler |
| **Fiziksel ortam** | “Nasıl bir çevrede bulunacağım?” | İhtiyaca göre. Açık alan, gölge veya oturma düzeni seçimi değiştirebilir. | İç/dış alan, korunaklılık, ışık, gölge, oturma düzeni, manzara |
| **Ses ortamı** | “Dinlemek, konuşmak veya odaklanmak ne kadar kolay?” | Evet; özellikle sohbet, dinlenme ve çalışma amaçlarında. | Sesin kaynağı, baskınlığı ve iletişime etkisi |
| **Yoğunluk** | “Alanı başkalarıyla ne ölçüde paylaşacağım?” | Evet. Hareket, yer bulma ve kişisel alan beklentisini değiştirir. | Kalabalıklık, kullanım sıkışıklığı, oturma yeri bulma örüntüsü |
| **Kullanım koşulları** | “Burada yapmak istediğim şeye hangi kurallar uygulanıyor?” | Evet. Bir olanak bulunsa bile kullanılamayabilir. | Rezervasyon, yaş/katılım sınırı, evcil hayvan kuralı, oturum süresi, ilgili hizmet kısıtları |
| **Zaman ihtiyacı** | “Bu ziyaret ne kadar zaman ister?” | Evet. Kısa mola ile uzun ziyaret arasında seçim yaptırır. | Ziyaret süresi, bekleme ve hizmet süresi; ayrı ayrı |
| **Maliyet** | “Bu ziyaret bütçemde neye karşılık gelir?” | Evet. Giriş, tüketim ve zorunlu ek giderler kararı değiştirebilir. | Kapsamı belli tutar veya aralık, para birimi, ücret koşulları |
| **Ulaşım** | “Seçtiğim başlangıçtan buraya gitmek ne gerektirir?” | Evet. Mesafe, süre ve ulaşım biçimi seçim yükünü değiştirir. | Yolculuk süresi/mesafesi, aktarma, son yaklaşım ve ilgili erişim koşulları |
| **Fiziksel erişim** | “Girişe ve kullanacağım alana ulaşabilir miyim?” | Evet; bazı kullanıcılar için zorunlu koşuldur. | Basamak, rampa, asansör, yol yüzeyi, eğim ve ilgili tesislere erişim |
| **Ziyaret durumu** | “Planladığım ziyareti gerçekleştirebilir miyim?” | Evet; bazen bütün kararı geçersiz kılar. | Çalışma saatleri, geçici/kalıcı kapanma, bakım, ziyaret kısıtlaması |

Bazı ayrımlar özellikle korunmalı:

**Yoğunluk ve ses birleştirilmez.** Sessiz ama dolu bir müze ile boş ama yüksek müzikli bir kafe farklı deneyimlerdir.

**Ulaşım ve fiziksel erişim birleştirilmez.** Yakında olmak, girişe veya içerideki alana erişilebildiğini göstermez.

**Olanak ve uygunluk birleştirilmez.** Masa bulunması çalışmaya, açık alan bulunması yağmurda kullanıma, çocuk sandalyesi bulunması her çocuklu ziyarete uygunluğu kanıtlamaz.

**Maliyet ve fiyat algısı birleştirilmez.** “Pahalı bulunuyor” ifadesi kişinin bütçe sınırını karşılaştırabileceği tutar değildir.

**Zaman ihtiyacının parçaları birbirine karıştırılmaz.** Ziyaretin kendisi, kuyrukta bekleme ve ulaşım farklı yüklerdir. Toplam süre ancak bu parçalar yeterince biliniyorsa anlatılabilir.

---

**5. Atmosfer, tempo, enerji ve sohbet uygunluğu hakkında karar**

| Aday kavram | Nihai karar | Gerekçe |
|---|---|---|
| **Atmosfer** | Bağımsız değerlendirme ekseni olmaktan çıkar. Ortam anlatısında kullanılabilir. | Tek başına kararı açıklamaz. Fiziksel ortam, ses ve yoğunluğun anlaşılır bir özeti olabilir. Ayrı puanı olmaz. |
| **Tempo** | Kaldırılır; anlamı ilgili kavrama taşınır. | Hizmet hızıysa zaman ihtiyacına, kalabalık hareketiyse yoğunluğa, ziyaret süresiyse yine zaman ihtiyacına aittir. |
| **Enerji** | Temel sözlükten çıkarılır. | “Yüksek enerji” ölçülebilir ve ortak anlamlı bir karar bilgisi değildir. Gerekiyorsa müzik, etkinlik ve yoğunluk somut olarak anlatılır. |
| **Sohbet uygunluğu** | Korunur; **amaca bağlı uygunluk** altında yer alır. | Kullanıcının doğrudan karar sorusudur. Ancak yerin kalıcı ve bağımsız bir niteliği gibi saklanıp her durumda tekrarlanmaz. |
| **Sakinlik** | Bağımsız puan olmaz; kullanıcı isteği ve koşullu anlatım olarak kalır. | Az ses, az insan ve düşük hareket aynı şey değildir. Hangisinin kastedildiği değerlendirmede ayrıştırılır. |
| **Konfor** | Genel eksen olmaz; somut koşullara ayrılır. | Oturma, sıcaklık, gölge, sıkışıklık ve fiziksel efor farklı ihtiyaçlara karşılık gelir. |
| **Aile dostu / çocuk dostu** | Genel uygunluk etiketi olarak kullanılmaz. | Yaş, ihtiyaç, olanak, erişim ve kullanım kuralları bilinmeden fazla geniş bir sonuçtur. |
| **Romantik / samimi / otantik** | Evrensel yer niteliği olmaz. Kullanıcı isteği olarak anlaşılmaya çalışılır. | Kültüre ve kişiye göre anlamları değişir. Loş ışık, masa aralığı veya tarihî yapı gibi somut karşılıkları varsa açıklanır. |
| **Kalite** | Genel yer puanı olarak kullanılmaz. | Lezzet, hizmet, bakım ve beklenti karşılığı tek hükümde toplanamaz. |
| **Popülerlik / trend / gizli cevher** | Uygunluk kavramı olmaz. | Çok bilinmek veya az bilinmek tek başına kullanıcı faydası değildir. |
| **Güvenli** | Genel çıkarım etiketi olarak kullanılmaz. | Sessizlikten, ziyaretçi profilinden veya şikâyet yokluğundan güvenlik sonucu çıkarılamaz. Somut, güncel ziyaret kısıtları ayrıca anlatılır. |

Burada günlük dili yasaklamıyoruz. **Günlük dildeki bir sözcüğün, içeride belirsiz bir puana dönüşmesini önlüyoruz.**

“Daha sakin bir yer” araması anlaşılabilir. Ürün bunun karşılığında neden daha sakin saydığını açıklayabilmelidir.

---

**6. Karar anlamının nihai sözlüğü**

Şamandıra’nın asıl çıktısı bu aileden oluşur:

| Kavram | Kesin anlamı | Kullanıcıya nasıl yansır? |
|---|---|---|
| **Uygunluk** | Bir yerin, belirtilen amaç ve koşulları belirli ziyaret bağlamında karşılayabilmesi | “Hafta içi kısa bir yürüyüş için uygun bir seçenek.” |
| **Tercih gerekçesi** | Bu seçeneği değerlendirmeye değer kılan, ihtiyaca bağlı neden | “Ayırdığın sürede kısa parkuru tamamlayabilirsin.” |
| **Ödün** | Seçim yapılırsa kabul edilmesi gereken, zorunlu koşulu ihlal etmeyen sınırlılık | “Manzara için açık alanda oturman gerekir; gölge sınırlı.” |
| **Engel** | Ziyareti veya açık bir zorunlu koşulun karşılanmasını önleyen durum | “Kullanılacak alana yalnız merdivenle ulaşılıyor.” |
| **Alternatif farkı** | Başka bir yerin aynı karar açısından hangi anlamlı farkı sunduğu | “Daha kısa ulaşım gerektiriyor; yürüyüş alanı daha küçük.” |
| **Karar özeti** | En önemli gerekçe, ödün ve gerekli bilgi sınırının kısa birleşimi | Yer ve Keşfet anlatısının özeti; yeni bir puan veya bağımsız değerlendirme değildir. |

**Ödün ile engel arasındaki fark kritiktir.** Basamaksız erişim zorunluysa merdiven “küçük dezavantaj” değildir.

Benzer şekilde, “erişim bilgisi bilinmiyor” da erişim engeli olduğu anlamına gelmez. Ancak zorunlu koşulun karşılandığını söylemeye yetmez.

Uygunluk için şu anlamlar birbirinden ayrılmalı:

- **Uygunluğu desteklenen:** İlgili amaç için yeterli dayanak var; belirtilen zorunlu koşullar karşılanıyor.
- **Koşula bağlı:** Uygunluk belirli saat, bölüm veya kullanım biçiminde geçerli.
- **İhtiyaçla uyuşmayan:** Bilinen bir özellik amaçla veya zorunlu koşulla çelişiyor.
- **Değerlendirilemeyen:** Karar için gerekli bilgi eksik.

Bunlar kullanıcıya zorunlu rozetler olarak gösterilmez. Cümlelerin anlamını sabitler.

Kullanıcı ihtiyacını belirtmediyse kişisel uygunluk üretilmez. Yer yine açıklanabilir:

> “Kısa yürüyüş yapmak isteyenler için kıyı boyunca bir güzergâh sunuyor.”

---

**7. Her yer kavramı hangi bilgilerden üretilebilir?**

Ham yorumlar yalnızca iç kanıt havuzuna girer. Alıntı, yorum sayımı, yorumcu kimliği veya “insanlar şöyle söylüyor” anlatımı ürün çıktısı olmaz.

| Kavram | Kullanılabilecek dayanaklar | Güveni yükselten şey | Hiç üretilmemesi gereken durum |
|---|---|---|---|
| **Yer kimliği** | Resmî kayıt, doğrulanmış konum, işletme bilgisi | Ad, konum ve şube bilgisinin uyuşması | Kaynakların aynı yeri anlattığı belirlenemiyorsa kimlik kesinleştirilmez; bağlı çıkarımlar yayımlanmaz. |
| **Yer türü** | Güncel faaliyet bilgisi, işletme bilgisi, doğrulanmış gözlem | Fiilî kullanımın türü desteklemesi | Yalnız ad veya eski sınıflandırma varsa kesin tür iddiası kurulmaz. |
| **Coğrafi bağlam** | Doğrulanmış koordinat, idari ve coğrafi bilgi | Yer ile sınır/çevre eşleşmesinin doğruluğu | Yakınlıktan ilçe aidiyeti veya tüm çevreye ilişkin deneyim hükmü çıkarılmaz. |
| **Olanaklar** | Doğrulanmış bilgi, işletme bildirimi, güncel gözlem; destekleyici yorumlar | Olanağın mevcut ve kullanılabilir olduğunun anlaşılması | Yalnız yer türünden veya eski bir anmadan varlık sonucu çıkarılmaz. |
| **Fiziksel ortam** | Güncel ve ilgili görseller, gözlem, işletme bilgisi, açıklayıcı yorumlar | Hangi bölümün ve koşulun anlatıldığının bilinmesi | Kadraj dışı alanlar, bütün gün gölge veya mevsim boyu korunaklılık varsayılmaz. |
| **Ses ortamı** | Bağlamı anlaşılabilen bağımsız deneyim anlatımları, ilgili gözlem | Aynı koşullarda tutarlılık; sesin kaynağı ve etkisinin açıklığı | Tek olay, belirsiz “sakin” ifadesi veya dekor fotoğrafından genel ses profili çıkarılmaz. |
| **Yoğunluk** | Zamanı bilinen gözlemler, bağımsız deneyim örüntüleri; varsa uygun güncel veri | Gün/saat ayrımı ve tekrarlanan örüntü | Yorum sayısından, ününden veya tek etkinlikten olağan yoğunluk çıkarılmaz. |
| **Kullanım koşulları** | Güncel resmî/işletme kuralları, doğrulanmış bilgi | Kuralın kapsamının ve geçerliliğinin açık olması | Bir ziyaretçiye tanınan istisna genel kural sayılmaz. |
| **Zaman ihtiyacı** | Resmî ziyaret/etkinlik süresi, güzergâh bilgisi, bağlamlı gözlemler | Hangi faaliyet ve koşul için olduğunun bilinmesi; tutarlı aralık | Kısa yorumdan ziyaret süresi, tek beklemeden olağan bekleme üretilmez. |
| **Maliyet** | Güncel tarife, menü, bilet veya doğrulanmış fiyat bilgisi | Tarih, para birimi, kişi/ürün kapsamı ve ek ücretlerin açıklığı | Öznel “ucuz/pahalı” anlatımından tutar veya bütçe uyumu üretilmez. |
| **Ulaşım** | Doğrulanmış konum, ulaşım ağı ve güzergâh bilgisi | Başlangıç, ulaşım biçimi ve zaman koşulunun bilinmesi | Kuş uçuşu mesafeden yürüme süresi veya yürünebilirlik çıkarılmaz. |
| **Fiziksel erişim** | Ayrıntılı doğrulanmış gözlem, kapsamı açık erişim bilgisi | Girişten kullanılacak alana kadar ilgili yolun anlaşılması | Tek rampa fotoğrafından bütün yer için erişilebilirlik ilan edilmez. |
| **Ziyaret durumu** | Güncel resmî duyuru, doğrulanmış işletme bilgisi | İddianın zamanıyla uyumlu güncellik; istisnaların kontrolü | Eski saatlerden kesin “şu an açık”, yorum yokluğundan kapanma çıkarılmaz. |

İşletme bilgisi başlı başına değersiz değildir. Ancak yetkinliği konuya bağlıdır: rezervasyon kuralı için anlamlı dayanak olabilir; “şehrin en huzurlu yeri” ifadesi huzurun doğrulaması değildir.

**Doğrulanmış bilgi de bir kaynak adı değildir.** Belirli bir iddianın, ilgili kapsamda kontrol edilmiş olma durumudur.

---

**8. Güven seviyesi nasıl belirlenmeli?**

**Güven yere değil, tek tek iddialara aittir.**

Bir yerin adresi sağlam, fiyatı eski, ses ortamı ise bilinmiyor olabilir. Bunların ortalamasını alıp yere “yüksek güven” vermek kullanıcıyı yanıltır.

Her iddia şu sorularla değerlendirilir:

| Ölçüt | Sorduğu soru |
|---|---|
| **Doğrudanlık** | Kanıt bu iddiayı gerçekten destekliyor mu, yoksa dolaylı bir işaret mi? |
| **Kaynağın konuya uygunluğu** | Bu kaynak bu konuyu bilebilecek durumda mı? |
| **Bağımsızlık** | Tek bir anlatının tekrarlarını mı, ayrı dayanakları mı görüyoruz? |
| **Güncellik** | Bilgi, bu özelliğin değişme hızına göre hâlâ kullanılabilir mi? |
| **Bağlam kapsamı** | Kanıt iddia edilen saat, mevsim, bölüm ve kullanım biçimini kapsıyor mu? |
| **Tutarlılık** | Çelişki var mı; varsa zaman veya bölüm farkıyla açıklanabiliyor mu? |
| **Anlam açıklığı** | Söylenen şey gerçekten anlaşılmış mı; ironi, belirsiz sıfat veya yanlış yer eşleşmesi olabilir mi? |

İç değerlendirmede üç güven düzeyi yeterlidir:

| Düzey | Anlamı | Yayın sonucu |
|---|---|---|
| **Sağlam** | İddiaya uygun, yeterince güncel ve kapsamı açık dayanak var; önemli çelişki çözülmüş. | Kanıtın izin verdiği kapsamda anlatılabilir. |
| **Sınırlı** | Anlamlı dayanak var; fakat kapsam, güncellik veya tutarlılık sınırı bulunuyor. | Yalnız kapsam daraltılarak ve sınır kararla birlikte açıklanarak kullanılabilir. |
| **Yetersiz** | İddiayı savunacak dayanak yok. | İddia üretilmez. Karar için önemliyse eksiklik söylenir. |

“Bilinmiyor”, “çelişkili”, “eskimiş” ve “uygulanamaz” birer güven puanı değildir. Bilginin neden kullanılamadığını veya neden aranmadığını anlatan farklı durumlardır.

Ek kurallar:

- Çok sayıda tekrar, bağımsız kanıt sayılmaz.
- AI’ın kendi yanıtına güvenmesi, dış dünyaya ilişkin kanıt değildir.
- Tek bir güncel ve yetkili duyuru, belirli bir olguyu destekleyebilir. Deneyim genellemesi aynı mantıkla tek anlatıdan çıkarılamaz.
- “Olabilir” eklemek, dayanıksız iddiayı yayımlanabilir yapmaz.
- Kaydın yakın zamanda işlenmiş olması, deneyimin yakın zamanda yaşandığını göstermez.
- Güvenilirlik yüksek olsa bile bir örüntü kesin gelecek vaadi değildir.

Sayısal eşikleri bu aşamada uydurmamalıyız. “On yorum varsa güvenlidir” gibi bir kural; yorumların bağımsızlığını, bağlamını ve değişim hızını açıklamaz.

---

**9. Uygunluk nasıl türetilmeli?**

Uygunluk, bütün yer özelliklerinin ortalaması değildir. **İlgili ihtiyacın gerektirdiği dayanakların birlikte değerlendirilmesidir.**

Örneğin uzun sohbet için:

- Ses ortamı temel dayanak olabilir.
- Karşılıklı oturmaya elveren düzen katkı sağlayabilir.
- Oturum süresi sınırı kararı değiştirebilir.
- Belirli saatlerde yer bulma güçlüğü önemli ödün olabilir.
- Kullanıcının ulaşım veya bütçe sınırı ayrıca karşılanmalıdır.

Yalnız “müzik düşük” bilgisiyle bütün bu sonuçlara ulaşılamaz.

Türetilmiş bir açıklamanın güveni, karar için gerekli ama belirsiz bir dayanağın üzerini örtemez. Adresin çok sağlam bilinmesi, bilinmeyen erişim koşulunu telafi etmez.

Zorunlu koşullarda işlem sırası nettir:

1. Karşılamadığı bilinen yer, uyumlu sonuçlara girmez.
2. Karşılayıp karşılamadığı bilinmeyen yer, doğrulanmış eşleşme gibi sunulmaz.
3. Karşıladığı bilinen yerler arasında amaç ve tercihler değerlendirilir.
4. Ödünler ve önemli bilgi sınırları sonuçla birlikte açıklanır.

Kullanıcının adını aradığı bir yer, koşullarına uymasa da bulunabilir. **Bir yeri bulmak ile onu önermek farklı ürün eylemleridir.**

---

**10. Hangi durumlarda hiçbir anlatım üretilmemeli?**

Bütün kavramlar için ortak yayın sınırı şu olmalı:

- Dayanak başka yer, başka şube veya belirsiz bir bölüme aitse.
- Eski bilgiyle güncel durum iddia edilecekse.
- Tekil olaydan kalıcı özellik çıkarılacaksa.
- Kanıtın kapsamadığı saat, mevsim veya alan hakkında genelleme yapılacaksa.
- Çelişki, ortalama alınarak görünmez kılınıyorsa.
- Yer türünden stereotip üretiliyorsa: “Kütüphane olduğu için kesin sessizdir.”
- Ziyaretçi grubunun varlığından o gruba uygunluk çıkarılıyorsa.
- Bir şeyden söz edilmemesi, onun yokluğu veya sorunsuzluğu sayılıyorsa.
- Bir özelliğin anlamı yeterince açık değilse.
- Kullanıcı bağlamı bilinmeden kişisel uygunluk iddia edilecekse.

İki ek ayrım gerekli:

**Bilgi eksikliği:** İddia kuracak dayanağımız yoktur.

**Uygulanamazlık:** Kavram bu yer veya kullanım için anlamlı değildir.

Bir parkta masa rezervasyonu olmaması, doldurulması gereken eksik bilgi değildir. Bir kafede erişim bilgisinin bulunmaması ise ilgili kullanıcı için önemli eksiklik olabilir.

Her kavram her yer için üretilmeye çalışılmamalı.

---

**11. Yer sayfasında ve Keşfet’te ne görünmeli?**

Kabul edilmiş Bilgi Mimarisi’ndeki sıra korunmalı. Sözlük, bütün kavramların her sayfada gösterilmesini gerektirmez.

| Kavram | Yer sayfası | Keşfet |
|---|---|---|
| **Kimlik, tür, konum** | Her zaman; doğrulanabilen temel bilgiler | Her sonuçta |
| **Anlaşılan amaç ve koşullar** | Kullanıcı bağlamı varsa gerekçeye yansır | Ortak arama bağlamında görünür ve değiştirilebilir |
| **Tercih gerekçesi** | Ana karar bilgisidir | Her öneride kısa ve aramaya bağlı |
| **Ödün veya engel** | Kararı etkiliyorsa erken görünür | Seçimi değiştiren koşul sonuçla birlikte görünür |
| **Olanaklar** | İlgili olanlar; tam liste zorunlu değil | Amacı veya alternatif farkını açıklıyorsa |
| **Fiziksel ortam, ses, yoğunluk** | Beklenen deneyimi açıklayacak kadar | Aramayla ilgili ayırt edici olanlar |
| **Kullanım koşulları** | İlgili kurallar; zorunlu koşullar öne çıkar | Eşleşmeyi veya seçimi etkiliyorsa |
| **Zaman ihtiyacı, maliyet** | Dayanağı ve kapsamıyla | Belirtilen süre/bütçe veya önemli ödün açısından |
| **Ulaşım, fiziksel erişim** | İlgili ayrıntılarıyla | Kullanıcının sınırı veya belirleyici fark varsa |
| **Ziyaret durumu** | Ziyareti engelleyen durum en başta | Sonucu geçersiz kılan durum saklanmaz |
| **Bilgi sınırı ve güncellik** | İlgili iddianın yanında; ayrıca genel yöntem bağlantısı | Kararı etkileyen eksiklik sonuçla birlikte |
| **Alternatif farkı** | Anlamlı alternatif varsa; mimarideki en çok üç sınırıyla | Seçenekler arasındaki farkın anlatımında |
| **İç güven puanı ve analiz sinyalleri** | Gösterilmez | Gösterilmez |

Yer sayfasının omurgası böyle kalır:

**Hangi yer → neden seçilebilir / neden seçilmemeli → nasıl bir deneyim → kararı değiştiren koşullar → gitmek için gereken bilgiler → bilgi sınırları → anlamlı alternatifler.**

Keşfet ise her yerin bütün profilini anlatmaz. Ortak bağlam altında **neden bakmaya değer olduğunu ve önemli farkını** anlatır.

Bilgi sadeleştirilirken zorunlu koşula ilişkin eksiklik veya engel sadeleştirme dışında tutulur.

---

**12. Şehir ve ilçe dilinde ne değişir?**

Aynı kavramlar korunur; iddianın kapsamı değişir.

- Şehir, **nerede aramanın anlamlı olduğunu** açıklar.
- İlçe, **seçilen alan içindeki farkları** açıklar.
- Bölge, kabul edilmiş mimarideki gibi şehir üstü coğrafi gruplamadır.
- Yer içindeki teras, salon veya parkur bölümü ise **değerlendirmenin geçerli olduğu alanı** belirtir.

Bu anlamlar aynı “bölge” sözcüğü altında birbirine karıştırılmaz.

Bir ilçedeki birkaç sakin yerden “ilçe sakindir” sonucu çıkarılmaz. Coğrafi anlatının ayrıca o kapsamı destekleyen dayanağı olmalıdır.

Şehirler arasında “orta kalabalık”, “ucuz” veya “yakın” sözcüklerinin anlamı sessizce değiştirilmez. Göreli karşılaştırma yapılıyorsa referansı açıklanır; bütçe ve ulaşım kararlarında mümkün olduğunca kapsamı belli tutar, süre ve mesafe kullanılır.

---

**13. Yalnızca içeride kalacak değerlendirmeler**

İçeride üç farklı iş var. Bunları tek “AI skoru” altında toplamamalıyız.

| İç değerlendirme | Neden var? | Kullanıcıya ne yansır? |
|---|---|---|
| **Kanıt yeterliliği** | İddianın yayımlanabilirliğini belirler. | Gerekli olduğunda somut bilgi sınırı |
| **Kaynak bağımsızlığı ve tekrar kontrolü** | Aynı anlatının çok kanıtmış gibi sayılmasını önler. | Sayısal skor veya kaynak dökümü yansımaz. |
| **Çelişki değerlendirmesi** | Hangi iddianın hangi kapsamda savunulabileceğini belirler. | “Akşam saatleri için net bir değerlendirme yapamıyoruz.” gibi sonuç |
| **Anlam çıkarma belirsizliği** | Yanlış yorumlama ihtimalini denetler. | Gerekiyorsa değerlendirmeden kaçınma |
| **Yer eşleştirme güveni** | Yanlış yer/şube bilgisinin birleşmesini önler. | Belirsiz eşleşmede iddianın yayımlanmaması |
| **Amaçla eşleşme derecesi** | Uygun adaylar arasında sıralamaya yardım eder. | Yüzde yerine somut tercih gerekçesi |
| **Tercihlerin ağırlığı** | Kullanıcının açık önceliklerini sıralamaya taşır. | Anlaşılan öncelikler; teknik ağırlıklar değil |
| **Seçenek benzerliği** | İlk kümenin birbirinin kopyası olmasını önler. | Anlamlı alternatif farkları |
| **Bağlam içindeki ret bilgisi** | Reddedilen yeri yeniden dayatmayı önler. | Kullanıcının geri alabileceği seçim durumu |
| **Kapsam değerlendirmesi** | Sonuç yokluğunu dünya hakkında yanlış hükme çevirmeyi önler. | “Bu koşullarda yeterince bildiğimiz bir yer bulamadık.” |

**Yalnız sıralama motoruna ait olanlar:** eşleşme derecesi, tercih ağırlıkları, seçenek benzerliği ve aynı karar bağlamındaki ret etkisidir. Bunlar kullanıcıya yer özelliği olarak çıkmaz.

Kanıt yeterliliği ve güncellik ise yalnız sıralama konusu değildir; öncelikle iddianın kullanılabilirliğini belirler.

Şunlar hiçbir zaman kullanıcı çıktısı olmamalı:

- Ham yorum veya yeniden yazılmış yorum pasajları.
- Yorumcu kimliği ve kişi profilleri.
- Duygu, konu sıklığı veya yorum hacmi puanları.
- Açıklanamayan “%93 sana uygun” sonuçları.
- İç model talimatları, ara muhakeme ve teknik ağırlıklar.
- Şüpheli kaynak/manipülasyon tespitlerinden türetilmiş kanıtsız suçlamalar.
- Kaynak platform dökümleri; kabul edilmiş atıf yükümlülükleri saklıdır.

Bazı değerlendirmeler ise **gizli kullanılmak üzere de üretilmemeli:**

- Yorumculardan çıkarılmış gelir, sınıf veya hassas kimlik profilleri.
- “Kaliteli müşteri kitlesi”, “düşük seviye ziyaretçi” gibi hükümler.
- Ücret, gösteriş veya popülerlikten türetilmiş genel üstünlük.
- Ticari ilişkinin uygunluk avantajına çevrilmesi.

Bunları kullanıcıdan gizlemek sorunu çözmez; kararın içinde yer almamaları gerekir.

---

**14. Şamandıra cümlesinin kuralları**

Ürünün kendi diliyle konuşması, çıkarımı olgu gibi söylemesi anlamına gelmez.

Her karar cümlesi gerektiği kadar şu dört şeyi taşır:

**Geçerli koşul + somut özellik + karar açısından anlamı + önemli sınır.**

Aşağıdaki örnekler kurmacadır; gerçek yer iddiası değildir.

| Kullanılmayacak ifade | Şamandıra’nın ifadesi |
|---|---|
| “Yorumlarda en çok sakinliği övülüyor.” | “Hafta içi gündüzleri düşük ses düzeyi uzun sohbeti destekliyor.” |
| “Enerjisi yüksek, atmosferi harika.” | “Akşamları müzik belirgin; sessiz konuşmak isteyenleri zorlayabilir.” |
| “Aile dostu.” | “Çocuk sandalyesi var. Bebek arabasıyla kullanılacak alana erişim bilgisi net değil.” |
| “Fiyat performans mekânı.” | “Güncel fiyat bilgisi bulunmadığından bütçene uyduğunu doğrulayamıyoruz.” |
| “Şu an sakin.” | “Hafta içi sabahları daha düşük yoğunluk beklenebilir; anlık durum bilinmiyor.” |
| “Tam sana göre.” | “İstediğin kısa yürüyüşü destekliyor; gölgeli alanı sınırlı.” |
| “Yakın ve kolay ulaşılır.” | “Seçtiğin başlangıçtan yürüyüş süresi yaklaşık 15 dakika.” |
| “Erişilebilir.” | “Ana giriş basamaksız. Üst kattaki alana erişim doğrulanmadı.” |

Bu örneklerdeki olumlu cümleler de ancak ilgili dayanak varsa kullanılabilir.

Ek dil kuralları:

- “Sessiz”, “ücretsiz”, “açık” gibi ifadeler gerekli kapsamı taşır.
- “Daha sakin” bir karşılaştırmaysa neye göre olduğu anlaşılır.
- “Gidebilirsin” ifadesi eksik zorunlu koşulun üzerini örtemez.
- Kullanıcının amacı bilinmiyorsa “sana” yerine kullanım amacı belirtilir.
- Önemli belirsizlik yöntem sayfasına veya metnin sonuna saklanmaz.
- Metni zenginleştirmek için aynı kanıt farklı sıfatlarla tekrar edilmez.
- Kullanıcıya ilgili belirsizlik anlatılır; iç analiz süreci yüklenmez.

---

**15. Bu sözlük beş yıl sonra nasıl genişler?**

Çekirdek kavramların anlamı sabit kalmalı; yer türlerine özgü ayrıntılar bunların altına eklenmeli.

Örneğin:

| Yeni ihtiyaç veya yer türü | Mevcut dilde karşılığı |
|---|---|
| Müzede rehberli ziyaret | Olanak + kullanım koşulu + zaman ihtiyacı |
| Parkurda zemin ve eğim | Fiziksel erişim; yürüyüş amacına bağlı uygunluk |
| Kafede bilgisayarla çalışmak | Olanaklar + kullanım koşulları + ses ortamı + zaman |
| Konaklamada belirli giriş saati | Ziyaret bağlamı + kullanım koşulları |
| Belirli bir beslenme ihtiyacı | Zorunlu koşul + kapsamı açık olanak/hizmet bilgisi |
| Teras ile salonun farklı deneyimleri | Aynı yer içinde farklı geçerlilik kapsamları |

Yeni bir ayrıntı için yeni üst kavram açılması gerekmez.

Yeni temel kavram ancak şu soruların tümüne savunulabilir cevap varsa eklenmeli:

1. Mevcut kavramlarla açıklanamayan hangi karar farkını taşıyor?
2. Kullanıcı bu farkı anlayıp seçiminde kullanabiliyor mu?
3. Ayrı bir kavram olması, aynı şeyi iki kez saymamızı önlüyor mu?
4. Hangi dayanakla üretileceği ve ne zaman susacağı belli mi?
5. Başka şehirlerde ve ilgili yer türlerinde aynı anlamını koruyor mu?

Bir kavramın anlamı değişiyorsa bu, sessiz bir metin düzenlemesi sayılmaz. Ona bağlı eski açıklamalar ve uygunluk kararları yeniden değerlendirilmelidir. API, AI ve frontend aynı sözcüğe farklı anlamlar yükleyemez.

Sözlüğün yayımlanabilir hale gelmesi de bütün şehirlerde bütün kavramların doldurulmasını gerektirmez. **Kapsam büyüyebilir; bilgi sınırları aynı dürüstlükle korunur.**

---

**16. Kendi önerime son itirazlarım**

**“Bu kadar iç ayrım ürünü ağırlaştırmaz mı?”**  
Hepsi kullanıcıya aynı anda gösterilirse ağırlaştırır. Bu yüzden çıktı bir özellik tablosunu doldurmak değil, kararı değiştiren birkaç bilgiyi seçmektir. İç ayrıntı, dış anlatımı sadeleştirmeye hizmet etmeli.

**“Soyut sıfatları azaltmak yerin karakterini kaybettirmez mi?”**  
Yalnız kuru tesis bilgisi kullanılırsa kaybettirir. Bu yüzden ortam anlatısı korunuyor. Ancak “samimi atmosfer” yerine küçük salon, yakın masalar, belirgin müzik gibi dayanaklı özelliklerden anlam kuruluyor.

**“Sohbet uygunluğu yine belirsiz değil mi?”**  
Evet, tek etiket halinde bırakılırsa belirsiz. Savunulabilir olması; hangi ziyaret bağlamında, hangi özelliklerle ve hangi sınırla üretildiğinin açıklanmasına bağlı.

**“Yetersiz bilgide susmak az sonuç üretmez mi?”**  
Üretebilir. Bu, bilgi kapsamının gerçek sınırıdır. Çözüm düşük güvenli çıkarımları kesinleştirmek değil, karar için gerekli kanıtı geliştirmektir. Somut bilgileri yeterli bir yer, deneyim anlatısı eksik diye bütünüyle yok sayılmaz; bildiğimiz kadar anlatılır.

**“Sonuçları karşılaştırmak için puan gerekmez mi?”**  
İç sıralama değerlendirmesi gerekebilir. Kullanıcının karşılaştırması ise ortak karar ölçütleri üzerinden yapılabilir: daha kısa ulaşım, daha düşük ses, daha uzun bekleme, belirli bütçe sınırı. Tek sayının örttüğü farklar bunlardır.

**“Bu önerinin hâlâ doğrulanması gereken tarafı ne?”**  
Kullanıcıların özellikle tercih–zorunlu koşul, yoğunluk–ses ve ödün–engel ayrımlarını anlayıp kullanabilmesi. Değerlendirme çalışmalarında da aynı kanıttan benzer kapsam ve kesinlikte açıklamalar üretilebilmesi gerekir. Başarı, kavram sayısı veya metin beğenisiyle değil, daha doğru anlaşılan seçenekler ve daha az kötü sürprizle sınanmalıdır.

Savunduğum nihai sözlükte **atmosfer bağımsız puan değildir; tempo ve enerji temel kavram değildir; sohbet uygunluğu ise bağlama bağlı bir sonuçtur.**

Şamandıra’nın bütün kararlarını taşıyan cümle şudur:

> **Bu yer, yapmak istediğin şey için şu nedenle anlamlı. Seçersen şu koşulu kabul etmen gerekir. Kararını etkileyen şu noktayı ise henüz yeterince bilmiyoruz.**

---

## Belge ilişkileri — depoya aktarım eki

### Bu dokümanın bağlı olduğu belgeler

- [00-urun-felsefesi.md](./00-urun-felsefesi.md)
- [01-bilgi-mimarisi.md](./01-bilgi-mimarisi.md)

### Bu dokümanın etkilediği belgeler

- [03-karar-motoru.md](./03-karar-motoru.md)
- [04-sistem-mimarisi.md](./04-sistem-mimarisi.md)

### Bundan sonra okunması gereken belge

[03-karar-motoru.md](./03-karar-motoru.md)
