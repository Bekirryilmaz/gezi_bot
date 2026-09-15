# Kategori Taksonomisi

Bu doküman, sitede yer alacak her "yer" (gezilecek yer, konaklama, restoran, kafe vb.)
için kullanılacak kategori ve etiket sistemini tanımlar. Buradaki her kategori/etiket,
`ortak/sabitler.py` dosyasında kod karşılığı olan bir sabit olarak bulunur —
yani bu doküman ile kod her zaman birebir eşleşir. Taksonomiyi değiştirdiğinde
her iki dosyayı da güncelle.

Tasarım mantığı katmanlıdır:

1. **Ana kategori + alt kategori**: Bir yerin "ne olduğu" (müze, plaj, kafe, otel vb.)
2. **Özellik etiketleri**: Bir yerin "nasıl olduğu" (alkollü mü, öğrenci dostu mu,
   ücretsiz mi vb.) — bir yer birden fazla etiket taşıyabilir
3. **Ticari / kürasyon etiketleri**: Şehrin klasiği, sponsorlu mekan gibi ürün
   ve gelir modeline ait işaretler (`OZEL_ETIKETLER`)
4. **Deneyim eksenleri**: Rota algoritmasının kullanıcı tercihleriyle eşleştirme
   yaparken kullandığı 0-100 arası puanlar (bu yer ne kadar "tarihi", ne kadar
   "eğlence" ağırlıklı vb.)
5. **Zaman dilimi uyumu**: Alt kategorinin günün hangi dilimlerinde doğal olduğu
   (`KATEGORI_ZAMAN_DILIMLERI`)
6. **Lojistik tampon süreleri**: Ziyaret süresine eklenen insan payı
   (`MEKAN_BEKLEME_SURELERI_DK`)

---

## 1. Ana Kategoriler ve Alt Kategoriler

### 1.1. GEZİLECEK_YER

| Alt kategori | Açıklama / örnekler |
|---|---|
| `tarihi_kulturel` | Müze, ören yeri, kale, tarihi cami/kilise/sinagog, tarihi konak, anıt, arkeolojik alan |
| `doga_manzara` | Şelale, kanyon, yayla, göl, orman, koru/mesire alanı, seyir terası, mağara |
| `plaj_su` | Ücretli plaj, ücretsiz/halk plajı, kano-sup noktası, dalış noktası, liman/marina |
| `eglence_aktivite` | Lunapark, tematik park, macera parkı (tırmanma, zipline), bowling/bilardo, at çiftliği |
| `gece_hayati` | Bar, gece kulübü, canlı müzik mekanı, meyhane |
| `alisveris` | Çarşı/pazar, tarihi çarşı, AVM, el sanatları/hediyelik eşya dükkanı |
| `spor_doga_yuruyus` | Yürüyüş/trekking parkuru, bisiklet parkuru, kamp/mangal alanı, tırmanış alanı |
| `dini_manevi` | Cami, kilise, türbe, ziyaret yeri (aktif ibadet mekanı olarak) |
| `fotograf_noktasi` | Manzara/fotoğraf çekimi için özellikle popüler noktalar |

### 1.2. KONAKLAMA

| Alt kategori | Açıklama |
|---|---|
| `otel` | Yıldızlı otel, butik otel |
| `pansiyon_apart` | Pansiyon, apart otel |
| `kamp_karavan` | Kamp alanı, karavan alanı, bungalov |
| `hostel` | Sırt çantalı gezginlere yönelik paylaşımlı konaklama |
| `ev_kiralama` | Airbnb tarzı ev/daire kiralama, seyahatsever uygulama tipi konaklama |

### 1.3. YEME_ICME

| Alt kategori | Açıklama |
|---|---|
| `restoran_lokanta` | Genel restoran/lokanta |
| `deniz_mahsulleri` | Balık/deniz ürünleri ağırlıklı mekanlar |
| `kebap_izgara` | Kebapçı, ızgara, et ağırlıklı mekanlar |
| `ev_yemekleri_esnaf` | Ev yemeği, esnaf lokantası, salaş/otantik mekanlar |
| `fine_dining_romantik` | Özel/romantik akşam yemeği mekanları |
| `sokak_lezzeti` | Sokak lezzetleri, büfe, hızlı yemek |
| `kafe` | Genel kafe (kahve içme amacı için doğrudan aday) |
| `internet_kafe` | Bilgisayar/oyun salonu; kahve amacı türetilmez |
| `tatli_pastane` | Tatlıcı, pastane, dondurmacı |
| `kahve_uzmanlik` | Üçüncü nesil/uzmanlık kahve mekanları |
| `meyhane_bar` | Alkollü içki eşliğinde yemek mekanları |
| `cay_bahcesi` | Alkolsüz, aile dostu oturma/çay bahçesi mekanları |

> Not: "Ucuz/pahalı", "öğrenci dostu", "alkollü/alkolsüz" gibi nitelikler alt kategori
> değil, aşağıdaki **özellik etiketleri** ile ifade edilir. Böylece bir mekan hem
> `kebap_izgara` hem `ogrenci_dostu=evet` hem `alkol_servisi=yok` olabilir — kategori
> patlamasına (her kombinasyon için ayrı kategori açmaya) gerek kalmaz.

---

## 2. Özellik Etiketleri (`ozellikler`)

Her yer, aşağıdaki etiketlerden uygun olanlarını taşır (veritabanında esnek bir
JSONB alanında tutulur, bkz. `dokumanlar/veri_sozlugu.md`):

| Etiket | Tip | Açıklama |
|---|---|---|
| `alkol_servisi` | evet/hayir | İçkili servis var mı |
| `ogrenci_dostu` | evet/hayir | Öğrenci bütçesine uygun mu |
| `aile_cocuk_dostu` | evet/hayir | Çocuklu ailelere uygun mu |
| `evcil_hayvan_dostu` | evet/hayir | Evcil hayvan kabul ediyor mu |
| `ucretsiz` | evet/hayir | Giriş/kullanım ücretsiz mi |
| `rezervasyon_gerekli` | evet/hayir | Önceden rezervasyon gerekiyor mu |
| `engelli_erisimi` | evet/hayir | Engelli erişimine uygun mu |
| `manzarali` | evet/hayir | Manzara sunuyor mu |
| `romantik` | evet/hayir | Çift/romantik ziyaret için uygun mu |
| `sakin_calisma_ortami` | evet/hayir | Dizüstü ile çalışılabilir, sakin mi (kafe için) |
| `canli_muzik` | evet/hayir | Canlı müzik var mı |
| `wifi` | evet/hayir | Ücretsiz internet var mı |
| `otopark` | evet/hayir | Otopark imkanı var mı |
| `fiyat_seviyesi` | 1-4 | 1=ucuz, 2=orta, 3=pahalı, 4=çok pahalı |
| `en_iyi_ziyaret_mevsimi` | metin | Örn. "yaz", "ilkbahar-sonbahar", "tum_yil" |
| `ortalama_ziyaret_suresi_dk` | sayı | Ortalama kaç dakika/saat sürdüğü (rota süresi hesaplamak için) |
| `kahvalti_verir` | evet/hayir | Kahvaltı hizmeti sunar (alt kategori değil; kafe, otel, restoran vb. taşıyabilir) |
| `sehrin_klasigi` | evet/hayir | Küratörlüğünü yaptığımız, şehrin simgesi / vazgeçilmezi (bkz. #2.1) |
| `sponsorlu_mekan` | evet/hayir | Ticari anlaşmalı / öne çıkan mekan (bkz. #2.1) |

### 2.1. Ticari ve kürasyon etiketleri (`OZEL_ETIKETLER`)

Amenite niteliklerinden (wifi, otopark, alkol servisi) ayrı tutulan, ürün
kurgusuna ait işaretler. Kod karşılığı: `ortak/sabitler.py::OzelEtiket` ve
`OZEL_ETIKETLER`. Saklama yeri yine `ozellikler` JSONB alanıdır — yeni kolon
açılmaz; rota/listeleme bu anahtarları okur.

| Etiket | Açıklama |
|---|---|
| `sehrin_klasigi` | Editöryel kürasyon: yerlilerin ve gezginlerin "bu şehre gelince burası" dediği yer. Organik öne çıkarma; reklam değildir. |
| `sponsorlu_mekan` | Ticari anlaşma ile listede/rotada görünürlük kazanmış yer. Kullanıcıya şeffaf işaretlenir. |
| `kahvalti_verir` | Hizmet: mekan kahvaltı sunar. Ana tür değildir; `kafe`, `otel`, `restoran_lokanta` vb. ile birlikte gelir. |

Bir yer birden fazla özel etiketi taşıyabilir. Hiçbiri yoksa alan yazılmaz /
`hayir` kabul edilir.

---

## 3. Aktivite Etiketleri (`aktiviteler`)

Kullanıcının "özellikle yapmak istediğim bir şey var" dediği senaryoda (yüzmek,
yürüyüş, kano vb.) kullanılan etiketler. Bir yer birden fazla aktiviteyi destekleyebilir.

`yuzme`, `yuruyus_trekking`, `kano_sup`, `dalis`, `at_binme`, `bisiklet`, `kamp`,
`fotografcilik`, `kus_gozlemciligi`, `tekne_turu`, `yamac_parasutu`, `kayak`
(Karadeniz'in iç/yayla kesimlerine büyüyünce kış turizmi için)

Bu liste büyüdükçe `ortak/sabitler.py` içindeki `Aktivite` sabitine
eklenerek genişletilir.

---

## 4. Deneyim Eksenleri (rota algoritması puanlama girdisi)

Kullanıcı "gezimin ne kadarı eğlence ne kadarı tarihi olsun" dediğinde, algoritma
her yeri bu eksenlerdeki puanına göre değerlendirir (her eksen 0-100 arası, bir
yer birden fazla eksende yüksek puan alabilir — örn. tarihi bir kale aynı zamanda
manzara/fotoğraf açısından da yüksek puanlı olabilir):

| Eksen | Açıklama |
|---|---|
| `tarihi_kulturel_puani` | Ne kadar tarihi/kültürel değer taşıyor |
| `eglence_puani` | Ne kadar eğlence/aktivite odaklı |
| `doga_macera_puani` | Ne kadar doğa/macera odaklı |
| `gastronomi_puani` | Ne kadar gastronomi/lezzet odaklı |
| `gece_hayati_puani` | Ne kadar gece hayatı odaklı |
| `rahatlatici_sakin_puani` | Ne kadar dinlenme/sakinlik odaklı |

Bu puanlar başlangıçta alt kategoriye göre otomatik varsayılan değer alır (örn.
`tarihi_kulturel` alt kategorisindeki bir yer otomatik olarak yüksek
`tarihi_kulturel_puani` alır), zamanla duygu analizinden çıkan yorumlarla ve elle
küratörlükle iyileştirilir. Detay için `dokumanlar/veri_sozlugu.md` içindeki
`yer_deneyim_puanlari` bölümüne bakabilirsin.

---

## 5. Şehir Kapsamı

Her yer bir `sehir_id` ile ilişkilidir. Böylece taksonomi şehirden bağımsızdır —
Samsun için oluşturulan bu sistem, yeni bir şehir (örn. Ordu, Trabzon) eklendiğinde
hiçbir değişiklik gerektirmeden aynen kullanılır.

---

## 6. Yer Profili Boyutları (yorumlardan sentezlenen çok boyutlu profil)

`deneyim_puanlari` (bölüm 4) rota algoritmasının "ne kadar tarihi/eğlence/doğa"
sorusuna cevap verirken, aşağıdaki boyutlar tamamen farklı bir soruya cevap
verir: **"bu yer gerçekte nasıl bir yer"** — ziyaretçi yorumlarından
damıtılan, kullanıcıya gösterilecek tanıtım metnini besleyen pratik bilgiler.
Bunlar sadece "olumlu/nötr/olumsuz" değil, somut ve çok yönlü bir profildir.
Üretim mantığı için `veri/duygu_analizi/yer_profili_cikarici.py` dosyasına bakınız.

| Boyut | Olası değerler | Açıklama |
|---|---|---|
| `fiyat_algisi` | `ucuz` / `orta` / `pahali` / `bilgi_yetersiz` | Yorumlarda fiyattan **nasıl bahsedildiği** (özellik etiketlerindeki `fiyat_seviyesi`'nden FARKLIDIR — o objektif/kaynak verisi, bu ise ziyaretçi ALGISI) |
| `ulasim_kolayligi` | `kolay` / `orta` / `zor` / `bilgi_yetersiz` | Yere ulaşımın yorumlarda nasıl tarif edildiği (merkezi/uzak, otopark, toplu taşıma) |
| `kalabalik_zamanlar` | Örn. `{"hafta_sonu_aksam": "kalabalik", "hafta_ici_genel": "sakin"}` | Hangi zaman diliminde kalabalık/sakin olduğuna dair yorumlardan çıkan örüntüler; yeterli veri yoksa o zaman dilimi hiç listelenmez |
| `ziyaretci_profili` | Örn. `{"aile": 0.42, "cift": 0.31, "ogrenci": 0.10}` | Yorumlarda hangi ziyaretçi tipinden (aile, çift, arkadaş grubu, yalnız, turist, yerli, öğrenci, çocuklu, genç, yaşlı) ne oranda bahsedildiği |

Her boyut, `konu_analizi.py` ile birebir aynı **şeffaf, anahtar kelime tabanlı**
yöntemle (BERT/kara kutu KULLANILMADAN) çıkarılır — hangi ifadenin bu
sınıflandırmayı tetiklediği her zaman `ornek_ifadeler` alanıyla geriye
izlenebilir. Yeterli sayıda yorum/bahsedilme yoksa (`bilgi_yetersiz`), o boyut
hakkında konuşmak yerine sessizce atlanır — veri yokken uydurma bir izlenim
verilmez.

Bu profil, `veri/duygu_analizi/anlatim_uretici.py` tarafından samimi bir
Türkçe tanıtım metnine ("duygu_ozeti") dönüştürülüp hem kullanıcıya gösterilir
hem de veritabanında `yerler.yer_profili` alanında saklanır.

**Faz 2 entegrasyon notu (rota algoritması, henüz uygulanmadı):** Rota
algoritması bu alanları kullanıcı tercihleriyle eşleştirebilir — örn. "sakin
bir yer istiyorum" tercihinde `kalabalik_zamanlar` değeri `kalabalik` olan
zaman dilimlerinde önerilmeyen/uyarılan yerler; "öğrenci dostu/ucuz" tercihinde
`fiyat_algisi=ucuz` olan yerlerin öne çıkarılması; "aile ile" tercihinde
`ziyaretci_profili.aile` oranı yüksek yerlerin önceliklendirilmesi gibi.

---

## 7. Bölge Profili (şehir/ilçe geneli tanıtım duygu analizi)

Bölüm 6'daki Yer Profili TEK bir yer (örn. bir restoran, bir müze) için
üretilirken, Bölge Profili bir BÖLGE için (şehir merkezi VEYA bir ilçe)
üretilir — belirli bir yerden değil, doğrudan o bölgeden/hakkında konuşan
Ekşi Sözlük yorumlarından. Amaç: kullanıcıya "Atakum nasıl bir ilçe?",
"İlkadım'da gece hayatı var mı?" gibi sorulara cevap verecek genel bir
tanıtım metni + duygu profili sunmak.

| Alan | Açıklama |
|---|---|
| `bolge_adi` | Şehir merkezi anahtarı (örn. `samsun`) veya bir ilçe adı (örn. `Atakum`) |
| `ilce_mi` | `true` ise bir ilçe, `false` ise şehir merkezi geneli |
| `genel_duygu_skoru` / `genel_duygu_etiketi` | Bölgeye dair yorumların genel duygu ortalaması |
| `on_plana_cikan_konular` | Bölge için en çok bahsedilen konular (bkz. aşağıdaki genişletilmiş konu listesi) ve bu konulardaki duygu yönü |
| `kullanilan_yorum_sayisi` | Profilin kaç yoruma dayandığı (şeffaflık için) |
| `duygu_ozeti` | `anlatim_uretici.py::bolge_tanitim_metni_uret` ile üretilen Türkçe tanıtım paragrafı |

Konu tespiti için `konu_analizi.py::KONU_ANAHTAR_KELIMELERI`'ne, Yer
Profili'nde kullanılan konulara (manzara, fiyat, hizmet vb.) ek olarak
bölge-tanıtımına özel şu konular eklenmiştir: `guvenlik`, `trafik`, `doga`,
`tarihi_doku`, `gece_hayati`, `yasam_maliyeti`.

Veri kaynağı SADECE Ekşi Sözlük'tür (bölge-geneli serbest metin sunan tek
kaynak); Google Maps/Booking.com yorumları belirli bir YERE bağlı olduğu
için (bkz. bölüm 6) bu profile katkı sağlamaz. `yer_ismi_tespiti.py` ile
tespit edilen fırsatçı bağlantılar sayesinde bir bölge yorumu AYRICA
bahsettiği belirli bir yerin (varsa) Yer Profili'ne de katkı sağlayabilir —
bkz. `veri/README.md` "Bölge Profili" bölümü.

Bu yapı şehirden bağımsızdır: `sehir_ayarlari.py::SehirAyari.ilceler` listesi
doldurulan HER şehir için (Samsun dışında yeni eklenen şehirler için de) aynı
kod hiçbir değişiklik gerektirmeden çalışır.

---

## 8. Dahili gözlem sinyali taksonomisi

Bu taksonomi ham veya işlenmiş kaynaklardan çıkarılan, yalnız iç incelemede
kullanılan `AdayGozlem` kayıtlarının ortak sözlüğüdür. Sinyal; kanıtlanmış
iddia, kullanıcıya dönük uygunluk kararı, puan veya yayın değildir. Yeni aile
eklemek önce bu tabloyu, sonra `ortak/sabitler.py::DahiliSinyalAilesi`
sabitini değiştirmeyi gerektirir.

Canonical aileler:

`sessiz_ortam`, `sohbet_uygunlugu`, `calisma_uygunlugu`, `aile_uygunlugu`,
`cocuk_uygunlugu`, `partner_uygunlugu`, `arkadas_grubu_uygunlugu`,
`acik_alan`, `manzara`, `kalabaliklik`, `wifi`, `otopark`, `priz`,
`rezervasyon`, `canli_muzik`, `kahve`, `yemek`, `kahvalti`, `tatli`,
`eglence`, `tarihi_kulturel`, `acik_hava`, `fiyat_algisi`, `genel_duygu`.

`genel_duygu` yalnız BERT'in karar dışı genel `sentiment_signal` ailesidir.
Karar tercihi, hard constraint, sıralama veya public iddia ailesi değildir.

### 8.1. Gözlem türleri ve yön

| Gözlem türü | Anlam | Örnek |
|---|---|---|
| `fact_signal` | Varlık/yokluk gibi doğrulanabilir, açık kaynak ifadesi | `wifi var`, `otopark yok`, `bahcesi var` |
| `experience_signal` | Belirli ziyaretçinin yaşadığı koşul veya amaç deneyimi | `wifi cok yavas`, `cocuklarla cok rahat`, `rezervasyonsuz yer bulamadik` |
| `sentiment_signal` | Genel beğeni/tepki; somut karar iddiası değildir | `guzel`, `mukemmel`, `kaliteli`, `en iyi`, `romantik` |

Yön yalnız `support` veya `counter` olur. Yön, iddianın doğruluğu değil,
spanın ilgili aile için destekleyici mi karşı mı olduğunu anlatır. Değer,
varlık/yoklukta boolean; deneyimde ise açık ve sürümlü küçük bir değer
sözlüğüdür. Genel BERT duygusu explicit aspect polarity için fallback olamaz;
yalnız `sentiment_signal` üretiminde kullanılabilir.

Canonical candidate varsayılan ve strict `canonical-v1` sözleşmesini kullanır.
Aile, tür, yön ve değer kombinasyonu aşağıdaki küçük sözlükte bulunmalıdır;
keyfi JSON değeri kabul edilmez. Sürüm alanı bulunmayan payload yalnız tarihî
zorunlu ve opsiyonel alanların exact shape'ini değiştirmeden taşıyorsa otomatik
`legacy` tanınır. Serialize edilen legacy model açık
`sozlesme_surumu=legacy` marker'ını korur; tam model dump şekli,
`otomatik_yayinlanabilir=false` ve `cikarim_yontemi=geriye_uyumlu` izleriyle
roundtrip edilebilir. Bunun dışındaki canonical izli yeni payload, marker'ı
`legacy` olarak verilse dahi strict canonical doğrulamaya girer; canonical
producer marker değiştirerek bu sözleşmeyi bypass edemez.

| Aile | Tür | Support değerleri | Counter değerleri |
|---|---|---|---|
| `wifi` | `fact_signal` | `true` | `false` |
| `wifi` | `experience_signal` | `kotu_degil`, `cok_yavas_degil` | `kotu`, `cok_yavas`, `cekmiyor` |
| `sessiz_ortam`, `aile_uygunlugu`, `cocuk_uygunlugu`, `calisma_uygunlugu` | `experience_signal` | `true` | `false` |
| `acik_alan`, `manzara`, `otopark`, `canli_muzik` | `fact_signal` | `true` | `false` |
| `manzara` | `experience_signal` | `guzel` | `gorunmuyor`, `goremedik` |
| `fiyat_algisi` | `experience_signal` | `uygun`, `pahali_degil` | `pahali` |
| `otopark` | `experience_signal` | — | `park_sorunu` |
| `rezervasyon` | `experience_signal` | — | `rezervasyonsuz_yer_bulunamadi` |
| `canli_muzik` | `experience_signal` | `cok_yuksek_degil` | `cok_yuksek` |
| `kalabaliklik` | `experience_signal` | `kalabalik` | `sakin` |
| `manzara`, `fiyat_algisi`, `yemek`, `kalabaliklik`, `kahvalti`, `sessiz_ortam`, `genel_duygu` | `sentiment_signal` | `olumlu` | `olumsuz` |

Fact karşı ifadesinin yakınındaki `degil` gibi açık olumsuzluk yönü tersine
çevirebilir; bu nedenle `wifi yok degil` support `true` olur. String deneyim
değerlerinde yalnız yukarıdaki ters karşılığı tanımlıysa yön çevrilir; karşılık
belirsizse candidate üretilmez.

### 8.2. İzlenebilirlik ve yayın sınırı

Her canonical aday kaynak, kaynak yorum/kayıt kimliği veya tam yorum içeriği
ile kaynak-yerden türetilen dahili review fingerprint'i, şube adayı,
aile/konu, yön/değer, gözlem türü, çıkarım yöntemi, model ve kural sürümü,
güven sınıfı ile güven kırılımı, zamansal durum, span hash'i ve dahili
referans taşır. Ham span geçici `ai_isleme` sırasında kullanılabilir; kalıcı
candidate çıktısında tutulması ayrıca `uzun_sureli_saklama=izinli` gerektirir.
Bu hak yoksa yalnız span hash'i ve dahili referans yazılır. Dokümana,
fixture'a veya kamusal çıktıya kaynak ham metni/yazar olarak kopyalanmaz.
`otomatik_yayinlanabilir` her durumda `false` kalır.

### 8.3. Hard constraint kuralları

1. `AdayGozlem` doğrudan hard constraint olamaz.
2. `sentiment_signal` ve `experience_signal`, sayıları veya güven sınıfları ne
   olursa olsun hard constraint olamaz.
3. Yalnız doğrulanmış, güncel, şubeye doğru bağlanmış, kullanım amacı için
   hakları izinli bir `fact_signal`; İddia/Geçerlilik ve yayın kapılarından
   geçtikten sonra Karar Motoru tarafından hard constraint girdisi olabilir.
4. `counter` sinyali sessizce olumluya çevrilemez; çelişkiyi veya bilinmeyeni
   görünür kılar. Destek sayısı karşı kanıtı iptal etmez.
5. `wifi`, `otopark`, `priz`, `rezervasyon` gibi ailelerde kaynakta açık
   var/yok ifadesi bulunmadığında değer tahmin edilmez. Genel duygu, yer puanı
   veya kategori bu boşluğu dolduramaz.

### 8.4. Yayımlanmış kategori → amaç fact eşlemesi

Yayımlanmış `Yer.alt_kategori` kimliği, aşağıdaki **doğrudan** eşlemelerde amaç
fact'idir. Eşlemede olmayan kategoriden amaç uydurulmaz. Google yorumu veya
dahili experience sinyali amaç fact'i üretemez. `internet_kafe` kahve amacı
türetmez. `sokak_lezzeti` yemek amacı fact'idir; aile/partner bağlamı
kategoriden türetilmez.

Eşleme seviyeleri: `direct_purpose_fact`, `weak_candidate_hint` (hard fact
değil), `no_purpose_inference`.

| Alt kategori | Amaç fact | Seviye |
|---|---|---|
| `kafe`, `kahve_uzmanlik` | `kahve_icmek` | direct |
| `internet_kafe` | — | no inference |
| `restoran_lokanta`, `kebap_izgara`, `deniz_mahsulleri`, `ev_yemekleri_esnaf`, `sokak_lezzeti`, `fine_dining_romantik`, `meyhane_bar` | `yemek_yemek` | direct |
| `tatli_pastane` | `tatli_yemek` | direct |
| `tarihi_kulturel` | `tarihi_kulturel_ziyaret` | direct |
| `eglence_aktivite` | `eglence` | direct |
| `doga_manzara`, `plaj_su` | `acik_hava` | direct |

Kod: `ortak/sabitler.py::ALT_KATEGORI_AMAC_ESLEMESI`, `amac_esleme_seviyesi`.

---

## 9. Kategori — zaman dilimi eşleştirmesi (`KATEGORI_ZAMAN_DILIMLERI`)

Rota motorunun bir durağı günün *hangi diliminde* önereceğini belirler.
İnsan gibi plan: kahvaltı sabah, fine dining akşam, gece hayatı gece.
Kod: `ortak/sabitler.py::ZamanDilimi` ve `KATEGORI_ZAMAN_DILIMLERI`.

Zaman dilimi anahtarları:

| Dilim | Anlam (kaba aralık, ayarlanabilir) |
|---|---|
| `sabah` | sabah / erken öğleden önce |
| `ogle` | öğle yemeği penceresi |
| `ikindi` | öğleden sonra / çay-kahve arası |
| `aksam` | akşam yemeği / gün batımı |
| `gece` | gece hayatı / geç saat |

Kod yardımcıları (`zaman_dilimi_uygun_mu`, `uygun_zaman_dilimleri`): sözlükte
olmayan alt kategori kısıtsızdır (tüm dilimler). Kahvaltı bir alt kategori
değildir; `kahvalti_verir` özelliği zaman eşlemesine girmez, rota motoru
bunu ayrı bir hizmet sinyali olarak kullanır.

Alt kategori → uyumlu dilimler (`kafe` ve konaklama alt kategorileri listede
yoksa kısıt uygulanmaz):

| Alt kategori | Zaman dilimleri |
|---|---|
| `kahve_uzmanlik` | `sabah`, `ikindi` |
| `restoran_lokanta`, `kebap_izgara`, `deniz_mahsulleri`, `ev_yemekleri_esnaf`, `sokak_lezzeti` | `ogle`, `aksam` |
| `fine_dining_romantik`, `meyhane_bar` | `aksam`, `gece` |
| `gece_hayati` | `gece` |
| `tarihi_kulturel`, `doga_manzara`, `dini_manevi`, `fotograf_noktasi`, `alisveris` | `sabah`, `ogle`, `ikindi` |
| `plaj_su`, `eglence_aktivite`, `spor_doga_yuruyus` | `sabah`, `ogle`, `ikindi` |
| `tatli_pastane`, `cay_bahcesi` | `ogle`, `ikindi`, `aksam` |

Zorunlu duraklar zaman dilimi dışındaysa yine dahil edilebilir (skorlamadaki
zorunlu-durak kuralıyla aynı ruh: kullanıcı isteği saati ezer).

---

## 10. Lojistik tampon süreleri (`MEKAN_BEKLEME_SURELERI_DK`)

`ortalama_ziyaret_suresi_dk` mekanın *içinde* geçirilen süredir. Buna ek olarak
park etme, kuyruk, garson bekleme, hesabı kapatma, tuvalet/dinlenme gibi insan
payı ana kategori bazında eklenir. Kod: `ortak/sabitler.py::MEKAN_BEKLEME_SURELERI_DK` ve `bekleme_payi_dk`
(sözlükte olmayan ana kategori için varsayılan 15 dk).

Rota zaman bütçesi ≈ ziyaret süresi + tampon + duraklar arası ulaşım.

| Ana kategori | Tampon (dk) | Örnek pay |
|---|---|---|
| `yeme_icme` | 30 | oturma, sipariş/garson, hesap |
| `gezilecek_yer` | 15 | bilet/kuyruk, tuvalet, fotoğraf molası |
| `konaklama` | 20 | check-in/out, park, odaya yerleşme |

Bu dakikalar ilk tahmindir; gerçek kullanım geri bildirimiyle
`zaman_butcesi.py` sabitleri gibi ayarlanması beklenir.

---

## 11. Rota coverage aileleri ve hazırlık durumu

Akıllı Rota motoru bu bölümle uygulanmaz. Yalnız hangi bilginin rota için
kritik, hangisinin karar için önemli, hangisinin isteğe bağlı olduğunu
sınıflandırır. Kod: `ortak/sabitler.py::RotaKapsamSinifi`,
`ROTA_KAPSAM_AILELERI`, `RotaHazirlikDurumu`, `TamamlikHucresi`,
`ZiyaretSuresiKaynagi`, `CalismaSaatiDurumu`, `RotaBilinmeyenDavranis`.

### 11.1. Kapsam sınıfları

| Sınıf | Anlam |
|---|---|
| `rota_kritik` | Yoksa durak yapılamaz veya gün planı savunulamaz |
| `karar_onemli` | Seçimi değiştirir; eksikse dürüstçe unknown kalır |
| `istege_bagli` | Anlatılabilir; rota adaylığını tek başına düşürmez |

| Aile / alan | Sınıf |
|---|---|
| canonical yer, şube, temiz isim, kategori | `rota_kritik` |
| canonical ilçe, koordinat | `rota_kritik` |
| amaç (`kahve_icmek`, `yemek_yemek`, `kahvalti`, `tatli_yemek`, `tarihi_kulturel_ziyaret`, `acik_hava`, `eglence`, `calisma`) | `rota_kritik` |
| `calisma_saatleri` | `rota_kritik` |
| ziyaret süresi | `karar_onemli` (bilinmiyorsa sezgisel yalnız planner yedegi) |
| `rezervasyon` | `karar_onemli` |
| `wifi`, `otopark`, `acik_alan`, `tekerlekli_sandalye_erisimi` | `karar_onemli` |
| aile/çocuk, çalışma/laptop, sakinlik, manzara, fiyat | `karar_onemli` |
| web sitesi, telefon | `istege_bagli` |

### 11.2. Tamamlık hücresi

`biliniyor`, `bilinmiyor`, `eskimis`, `celiskili`, `yalniz_dahili`.
`yalniz_dahili` yayımlanmış iddia değildir; OSM ham etiket veya NLP
aggregate olabilir. Kamusal skor üretilmez.

### 11.3. Ziyaret süresi kaynağı

| Kaynak | Fact mi? | Anlam |
|---|---|---|
| `dogrulanmis_sure` | Evet | Yayımlanmış süre iddiası (`verified_duration`) |
| `kullanici_secimi` | Hayır | O oturumun tercihi (`user_selected_duration`) |
| `planlama_tahmini` | Hayır | Kategori aralığı; yalnız rota planlama yedeği (`planning_estimate`) |
| `bilinmiyor` | Hayır | Süre yok (`unknown`) |

`planlama_tahmini` tek kesin sayı değildir: `minimum_dk` / `tipik_dk` /
`maksimum_dk` taşır. Kullanıcıya gerekiyorsa «Planlama için yaklaşık
45–75 dakika ayırdık» denir. «60 dakika sürer» denmez. Public fact
değildir.

### 11.4. Çalışma saati ayrıştırma durumu

OSM `opening_hours` ve birinci el/resmî kaynak aynı durum kümesini kullanır.
Tahmin yok. Google yorumundan saat türetilmez.

| Durum | Anlam |
|---|---|
| `known` | Desteklenen sözdizimi tam çözüldü |
| `partially_known` | Bazı kurallar çözüldü; PH/mevsim/yorum atlandı |
| `unknown` | Ham değer yok |
| `invalid` | Desteklenmeyen veya gece taşan sözdizimi |
| `stale` | Çözüldü ama gözlem tazeliği doldu |

`acik_iddiasi_kurulabilir` yalnız `known` ve taze kayıtta True olur.
`unknown` / `invalid` / `stale` yer «şimdi açık» sayılmaz.

### 11.5. Rota hazırlık durumu

Kamusal skor değildir. İç durum:

| Durum | Anlam |
|---|---|
| `rota_hazir` | Kimlik, koordinat, ilçe, amaç ve yayın uygun; çalışma saati yayımlanmış **ve** `known` |
| `rota_sinirli` | Temel uygun; saat unknown/partial/stale/yalnız dahili. Akıllı Rota limited aday olabilir; «Gitmeden önce saatini doğrula» |
| `kesif_adayi` | Keşfet/Bugün için bakılabilir; günlük dizi kurulmaz |
| `rota_kapali` | Karantina, geçersiz koordinat veya aktif olmayan şube |

`rota_hazir` sayısı tek GO kriteri değildir. `rota_sinirli` unknown
sözleşmesiyle kullanılabilir.

### 11.6. Rota unknown sözleşmesi (FAZ 26)

| Konu | Davranış |
|---|---|
| çalışma saati unknown | `limited_route` uyarı; hard blok değil; açık iddiası yok |
| ziyaret süresi estimate | `limited_route` uyarı; public fact değil |
| geçiş/transition unknown | `limited_route` uyarı |
| rezervasyon unknown | `limited_route` uyarı; kullanıcı zorunlu kıldıysa hard blok |
| geçici kapanış unknown | `limited_route` uyarı; açık varsayılmaz |
| kimlik karantina, geçersiz koordinat, şube pasif | `hard_block` |
