# Rota Motoru (`sunucu/rota_motoru/`)

Kullanıcı tercihlerine göre kişiselleştirilmiş gezi rotası üreten algoritma.
**Kütüphanesiz** (dış ML/optimizasyon bağımlılığı yok) — her adım saf Python
ile, adım adım izlenebilir şekilde yazılmıştır; hiçbir sonuç "kara kutu"
değildir (skorlar her zaman bir kırılımla döner).

## Zincir

```
skorlama.py -> zaman_butcesi.py -> kumeleme.py -> gunluk_slotlari_diz -> rota_olusturucu.py
```

- **`veri_tipleri.py`** — Veritabanından (SQLAlchemy) BAĞIMSIZ saf veri
  tipleri (`AdayYer`, `RotaTercihleri`, `RotaSonucu`, ...). Böylece
  aşağıdaki modüller gerçek bir veritabanı bağlantısı olmadan, sentetik
  verilerle test edilebilir.
- **`skorlama.py`** — `yer_uygunluk_puani(yer, tercihler, yol_suresi_dk=...) -> SkorSonucu`.
  Deneyim ekseni + aktivite + fiyat/sakinlik + kaynak kalitesi + ticari
  etiket bonusları (`sponsorlu_mekan` +30, `sehrin_klasigi` +15). Yol süresi
  ziyaret süresinin 1.5 katını aşarsa skor yarıya iner (`yol_yorgunlugu_cezasi`).
  Zorunlu duraklar her zaman en üstte. Her sonuç bir `kirilim` sözlüğüyle döner.
- **`zaman_butcesi.py`** — Bir günün kaç durak kaldırabileceğini hesaplar
  (ortalama ziyaret süresi + haversine mesafeye dayalı kaba ulaşım süresi
  tahmini). Sabitler (`GUNLUK_GEZI_DAKIKASI`, `ORTALAMA_SEHIR_ICI_HIZ_KMH`)
  dosyanın başında açıkça belirtilir, gerçek kullanıcı geri bildirimiyle
  ayarlanması beklenir.
- **`kumeleme.py`** — `gunlere_boluster(...)`. Konaklama noktasından
  (Senaryo 1) veya en iyi adayların ağırlık merkezinden (Senaryo 2) her
  adaya olan **açıyı (bearing)** hesaplayıp yerleri açıya göre sıralar,
  `gun_sayisi` kadar bitişik açısal dilime böler — k-means gibi rastgele
  başlangıca bağlı olmayan, deterministik bir yöntem. Ardından her günü
  zaman bütçesine göre budar (en düşük skorlu duraklar önce çıkar).
- **`siralama.py`** — TSP sezgiseli (nearest-neighbor + 2-opt). Gün içi sıra
  artık slot şablonundadır; bu modül birim testleri ve yedek olarak durur.
- **`rota_olusturucu.py`** — Orkestratör. Günleri bearing ile böler, her günü
  sabah / öğle / ikindi / akşam slotlarına dizer. Geçiş maliyeti =
  yol + ziyaret + `bekleme_payi_dk(ana_kategori)`. Sonuç `KullaniciRotasi`
  tablosuna kaydedilir (flush; commit API katmanının sorumluluğundadır).

## Senaryolar

- **Senaryo 1 (konaklama belli)**: `senaryo_1_rota_olustur(oturum, sehir_id,
  konaklama_noktasi, gun_sayisi, tercihler)`. Adayları çeker (konaklama
  noktasından `_MAKSIMUM_ADAY_MESAFESI_METRE` içindekiler + zorunlu
  duraklar) → skorlar → en iyi N'i seçer → günlere kümeler → her günü
  slot şablonuna göre dizer (kahvaltı/gezilecek, öğle yemeği ≤20 km,
  öğleden sonra gezilecek/kafe, akşam yemeği).
- **Senaryo 2 (konaklama belli değil)**: `senaryo_2_rota_olustur(oturum,
  sehir_id, gun_sayisi, tercihler)`. Aynı skorlamayla önce en iyi adayları
  seçer, ağırlık merkezini hesaplar, o merkeze en yakın/en kaliteli
  `KONAKLAMA` yerini önerir, sonra **Senaryo 1'i o önerilen noktayla
  çağırır** (kod tekrarını önler).

## Bilinen Basitleştirmeler

- `_MAKSIMUM_ADAY_MESAFESI_METRE` (40 km): varsayılan deneyim puanları alt
  kategori bazında verildiği için (yere özel değil), mesafe filtresi
  olmadan şehrin çok uzak bir ilçesindeki bir yer, merkezdeki bir yerle aynı
  puanı alıp yanlışlıkla rotaya girebilir. Bu sabit, MVP için makul bir
  şehir-içi gezi yarıçapı varsayımıdır.
- `ORTALAMA_SEHIR_ICI_HIZ_KMH` (30 km/sa) ve `GUNLUK_GEZI_DAKIKASI` (8 saat):
  kaba varsayımlardır, gerçek kullanım verisiyle ayarlanması beklenir.
- Kümeleme sonrası zaman bütçesi budaması, duraklar SKOR sırasına göre
  eklenerek yapılır; gün içi nihai sıra slot şablonundadır. Bütçe tahmini
  gerçek rota mesafesinden biraz farklı olabilir.

## Testler

```bash
python -m pytest sunucu/rota_motoru/testler/ -v
```

`skorlama.py`, `kumeleme.py`, `siralama.py` ve `gunluk_slotlari_diz` saf
fonksiyonlar olduğu için sentetik `AdayYer` verisiyle test edilir — gerçek
bir veritabanı bağlantısı gerekmez. `rota_olusturucu.py`'nin DB'ye bağlı
senaryoları ve API + DB bütünleşik testi Swagger (`/docs`) üzerinden
yapılır.
