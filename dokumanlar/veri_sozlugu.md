# Veri Sözlüğü

Bu doküman veritabanındaki (`sunucu/veritabani/modeller.py`) her tabloyu ve alanı
Türkçe olarak açıklar. Kod yazmasan bile veri kalitesini kontrol ederken bu
dosyaya bakarak her alanın ne anlama geldiğini anlayabilmen için hazırlandı.

## Genel İlkeler

- **Her tablonun `id` alanı** rastgele üretilen bir metin kimliktir (UUID),
  sıra numarası değildir. Bu, farklı kaynaklardan gelen verileri birleştirirken
  çakışma riskini ortadan kaldırır.
- **JSONB alanlar** (`ozellikler`, `aktiviteler`, `deneyim_puanlari`,
  `konu_duygulari`, `duraklar`, `tercihler`, `gunler`) esnek yapılardır — yani
  içindeki alt alanlar veritabanı şeması değiştirilmeden (migration
  gerekmeden) genişletilebilir. Bunların hangi alt alanları içerdiği
  `dokumanlar/kategori_taksonomisi.md` içinde tanımlıdır.
- **Zaman alanları** (`*_zamani`) her zaman UTC olarak saklanır.

## Tablo: `sehirler`

Platformun kapsadığı her şehir. Samsun ilk kayıttır.

| Alan | Açıklama |
|---|---|
| `isim` | Şehir adı (örn. "Samsun") |
| `plaka_kodu` | İl plaka kodu (örn. "55") |
| `bolge` | Bölgesel gruplama (örn. "Karadeniz") — bölgesel rota üretiminde kullanılır |
| `merkez_enlem`, `merkez_boylam` | Şehir merkezinin koordinatları (varsayılan harita odağı için) |
| `aktif_mi` | Sitede yayında mı (yeni eklenen ama henüz hazır olmayan şehirler için `false`) |

## Tablo: `yerler`

Bir gezilecek yer, konaklama veya yeme-içme mekanı. `ana_kategori` ve
`alt_kategori` değerleri için `dokumanlar/kategori_taksonomisi.md` #1'e bakınız.

| Alan | Açıklama |
|---|---|
| `sehir_id` | Bu yerin hangi şehre ait olduğu |
| `konum` | Coğrafi nokta (enlem/boylam), rota algoritmasının mesafe hesaplarında kullanılır |
| `ozellikler` | dokumanlar/kategori_taksonomisi.md #2'deki etiketler (alkol_servisi, ogrenci_dostu vb.) |
| `aktiviteler` | dokumanlar/kategori_taksonomisi.md #3'teki aktiviteler (yuzme, kano_sup vb.) |
| `kaynakta_puan_ortalamasi` / `kaynakta_puan_sayisi` | Kaynağın (örn. Google) kendi ham puanı — bizim duygu analizimizden **farklıdır** |
| `duygu_skoru_ortalama` | Bu yere ait tüm yorumların duygu analizi sonucu ortalaması (-1 ile +1 arası). `veri/duygu_analizi` tarafından hesaplanır |
| `deneyim_puanlari` | dokumanlar/kategori_taksonomisi.md #4'teki 6 eksende (tarihi, eğlence, doğa, gastronomi, gece hayatı, sakinlik) 0-100 puan. Rota algoritmasının kullanıcı tercihleriyle eşleştirdiği ana veri |
| `yer_profili` | dokumanlar/kategori_taksonomisi.md #6'daki çok boyutlu profil (fiyat algısı, ulaşım kolaylığı, kalabalık zamanlar, ziyaretçi profili). `veri/duygu_analizi/yer_profili_cikarici.py` tarafından üretilir |
| `duygu_ozeti` | `yer_profili`'nden sentezlenen, kullanıcıya doğrudan gösterilecek samimi Türkçe tanıtım metni. `veri/duygu_analizi/anlatim_uretici.py` tarafından üretilir |

## Tablo: `yer_kaynaklari`

Bir `Yer` kaydının hangi ham veri kaynaklarından (OSM, Google Maps, Ekşi Sözlük,
TripAdvisor) geldiğini izler. Aynı fiziksel yer birden fazla kaynakta bulunabilir;
`veri/esleme` bunları tek bir `Yer` satırına bağlar ama izini burada tutar.

## Tablo: `konaklama_detaylari`

Sadece `ana_kategori = konaklama` olan yerler için ek bilgiler (gecelik fiyat
aralığı, rezervasyon linkleri, oda sayısı). Diğer yer tiplerinde bu tablo boştur.

## Tablo: `yorumlar`

Her ham veya işlenmiş yorum. `duygu_skoru`, `duygu_etiketi`, `konu_duygulari`
alanları `veri/duygu_analizi` pipeline'i tarafından doldurulur.

| Alan | Açıklama |
|---|---|
| `duygu_skoru` | -1 (tamamen olumsuz) ile +1 (tamamen olumlu) arası genel duygu puanı |
| `duygu_etiketi` | "olumlu" / "notr" / "olumsuz" |
| `konu_duygulari` | Örn: `[{"konu": "manzara", "duygu_etiketi": "olumlu"}, {"konu": "fiyat", "duygu_etiketi": "olumsuz"}]` — bir yorumun farklı konular hakkında farklı duygular içerebileceğini yansıtır |
| `analiz_model_adi` | Hangi modelin bu analizi yaptığı (izlenebilirlik için) |

## Tablo: `sabit_rotalar`

Bizim elle küratörlüğünü yaptığımız, bilinen/hazır rotalar (örn. Karya/Likya
Yolu, Antep-Urfa gastronomi rotası). Algoritma tarafından değil, elle
oluşturulur — `duraklar` alanına gün gün, sıralı durak listesi girilir.

## Tablo: `kullanici_rotalari`

Algoritmanın (Faz 2) kullanıcı tercihlerine göre ürettiği kişisel rota.

| Alan | Açıklama |
|---|---|
| `tercihler` | Kullanıcının girdiği tüm tercihler: gün sayısı, ilgi ağırlıkları, aktiviteler, zorunlu duraklar, (varsa) konaklama yeri |
| `gunler` | Üretilen rota: her gün için sıralı durak listesi |
| `konaklama_onerisi_yer_id` | Senaryo 2'de (konaklama belli değilse) algoritmanın önerdiği konaklama bölgesi |
