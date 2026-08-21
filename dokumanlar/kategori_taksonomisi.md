# Kategori Taksonomisi

Bu doküman, sitede yer alacak her "yer" (gezilecek yer, konaklama, restoran, kafe vb.)
için kullanılacak kategori ve etiket sistemini tanımlar. Buradaki her kategori/etiket,
`veri/ortak/sabitler.py` dosyasında kod karşılığı olan bir sabit olarak bulunur —
yani bu doküman ile kod her zaman birebir eşleşir. Taksonomiyi değiştirdiğinde
her iki dosyayı da güncelle.

Tasarım mantığı üç katmanlıdır:

1. **Ana kategori + alt kategori**: Bir yerin "ne olduğu" (müze, plaj, kafe, otel vb.)
2. **Özellik etiketleri**: Bir yerin "nasıl olduğu" (alkollü mü, öğrenci dostu mu,
   ücretsiz mi vb.) — bir yer birden fazla etiket taşıyabilir
3. **Deneyim eksenleri**: Rota algoritmasının kullanıcı tercihleriyle eşleştirme
   yaparken kullandığı 0-100 arası puanlar (bu yer ne kadar "tarihi", ne kadar
   "eğlence" ağırlıklı vb.)

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
| `kafe` | Genel kafe |
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

---

## 3. Aktivite Etiketleri (`aktiviteler`)

Kullanıcının "özellikle yapmak istediğim bir şey var" dediği senaryoda (yüzmek,
yürüyüş, kano vb.) kullanılan etiketler. Bir yer birden fazla aktiviteyi destekleyebilir.

`yuzme`, `yuruyus_trekking`, `kano_sup`, `dalis`, `at_binme`, `bisiklet`, `kamp`,
`fotografcilik`, `kus_gozlemciligi`, `tekne_turu`, `yamac_parasutu`, `kayak`
(Karadeniz'in iç/yayla kesimlerine büyüyünce kış turizmi için)

Bu liste büyüdükçe `veri/ortak/sabitler.py` içindeki `Aktivite` sabitine
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
