# Görsel künye — hero kapak karesi

**Kapsam:** yalnız ana sayfa hero'su (`site/public/hero/`). **Tarih:** 2026-09-05; **REV:** 2026-09-06.
**Dayanak:** K9 (`00_brief_eki.md`) + `yon-v2.md` (P4 reddi) + `yon-v3.md` (poster LCP / scroll-video).

> **P4-REV:** `masaustu/k-*` ve `mobil/k-*` kare sekansı emekli. Sitede yalnız
> `kapak-masaustu.*` / `kapak-mobil.*` durur. Aşağıdaki plaka tablosu kapak
> provenansıdır (Unsplash kimlik + URL). Ham JPEG arşivi (`hero-kaynak/`)
> 2026-09-08 silindi — ajan bağlamını şişirmemek için; çapraz geçiş kurgusu
> **yeniden üretilmez**.
>
> **v3 notu (2026-09-08):** Kapak karesi `yon-v3.md` sözleşmesinde **LCP posteridir**
> (video gelince de poster olarak kalır veya videonun ilk karesinden yenilenir).
> Kling AI ile üretilecek hero videosunun künyesi (araç, tarih, sahne tarifi,
> yüz/marka/tabela yok denetimi) video tesliminde bu dosyaya eklenir.
> Ham JPEG arşivi geri getirilmez.

Bu dosya provenans arşividir: Unsplash lisansı tazminat/garanti taahhüdü vermez, savunmamız
kaydın kendisidir (yon.md §2.6 madde 6).

---

## Üretim yolu

| | |
|---|---|
| Yol | **B — Unsplash plaka kurgusu** (köprü). Fotoğraflarımız gelince Yol A'ya geçilir; bileşen arayüzü, kapak ve fallback aynı kalır. |
| Plaka sayısı | 9 |
| Edinme | **Elle indirme** (`images.unsplash.com` CDN, tarayıcıdan seçim). **Unsplash API kullanılmadı** — API Şartları atıf + indirme takibi zorunluluğu getirir (yon.md §2.6 madde 2). |
| İşçilik | Kırpım (4:3 masaüstü / 4:5 mobil, merkez) · doygunluk ×0,58 · hafif sıcak duotone: `bordo #6C0000` %16 + `kagit #F4EFE7` %8, `soft-light`. Foto hissi korunur; içerik fotoğraflarında duotone **yok** (yon.md §1.5). |
| Kurgu | Çapraz geçiş + tek yönlü kamera itişi (ölçek 1,000→1,055, yatay kayma %4,5). Duruş 4 kare, geçiş 4 kare (mobil 2/2). Ara kare **üretilmez**. |
| Sahne | "Gün açılışı": ufuk/şafak → kıyıya yaklaşma → yerin ortaya çıkışı. Bölge-nötr (K6): tanınabilir şehir silueti yok. |
| Betik | emekli — `hero_kare_uretim.mjs` silindi; kapak karesi yerinde kalır |
| Lisans metni | **Unsplash Lisansı** — https://unsplash.com/license · sürüm: 2026-09-05 tarihinde erişilen metin. Ticari kullanım serbest, atıf zorunlu değil; marka hakkı ve model izni **dâhil değildir**, tazminat yoktur. |

## Uygunluk denetimi (yon.md §2.6 madde 3–4)

Dokuz karenin tamamı indirme sonrası tek kontak karede gözle denetlendi (ham arşiv silindi; kayıt bu tablodadır):

- **Tanınabilir yüz:** yok — hiçbir karede insan figürü yok.
- **Marka / logo / tabela:** yok.
- **Sunum:** kareler sekans içinde **atmosfer** olarak kullanılır; hiçbir kare belirli bir yerin
  fotoğrafı gibi sunulmaz. Hero plakası `aria-hidden`, kapak `alt=""` (dekoratif). Yer kartı ve
  yer detay fotoğrafı **yalnız kendi çekimimiz** olacaktır (K2 kırmızı çizgisi (c)).

## Plakalar

Sekans sırası soldan sağa: **09 → 08 → 07 → 01 → 02 → 03 → 04 → 05 → 06**.

| Sıra | Dosya | Fotoğraf kimliği | Fotoğrafçı | Fotoğraf sayfası | İndirme |
|---|---|---|---|---|---|
| 1 | `plaka-09.jpg` | `photo-1451485435476-a244439c78cd` | Pierre Leverrier | https://unsplash.com/photos/landscape-photography-of-sea-k0Ynnf2CbKw | 2026-09-05 |
| 2 | `plaka-08.jpg` | `photo-1613082852603-f4f1187885ea` | Adrian Balcan | https://unsplash.com/photos/body-of-water-during-sunset-tGHOTZgJaDQ | 2026-09-05 |
| 3 | `plaka-07.jpg` | `photo-1759693482882-ba82ac0f2898` | Lars Schneider | https://unsplash.com/photos/misty-beach-with-waves-crashing-on-shore-VdrcD9KlZUA | 2026-09-05 |
| 4 | `plaka-01.jpg` | `photo-1762980966982-2cc919519ec3` | Luke Yang | https://unsplash.com/photos/coastal-cliffs-shrouded-in-morning-fog-at-sunrise-K6LQgxKYJeY | 2026-09-05 |
| 5 | `plaka-02.jpg` | `photo-1784646450786-bc07a20d3b81` | Baptiste Riethmann | https://unsplash.com/photos/a-serene-coastal-landscape-at-sunrise-with-hills-and-ocean-F1lTav4_WlI | 2026-09-05 |
| 6 | `plaka-03.jpg` | `photo-1759107576150-c373766e6959` | Marshall Iden | https://unsplash.com/photos/sunrise-over-a-rocky-coastline-with-a-sea-stack-WgUhDizwULs | 2026-09-05 |
| 7 | `plaka-04.jpg` | `photo-1737547670396-ae9fd016aae5` | Saim Alam | https://unsplash.com/photos/a-large-body-of-water-with-cliffs-in-the-background-ri2safL0HMk | 2026-09-05 |
| 8 | `plaka-05.jpg` | `photo-1707007730851-c53cc2879f00` | Phill Brown | https://unsplash.com/photos/a-view-of-a-beach-with-waves-coming-in-to-shore-S7YTvzJnf0w | 2026-09-05 |
| 9 | `plaka-06.jpg` | `photo-1785129775578-22326652294e` | Tahamie Farooqui | https://unsplash.com/photos/hazy-beach-with-waves-and-scattered-rocks-ZOrOd3lml7Y | 2026-09-05 |

Ham JPEG kopyaları silindi. Provenans: bu tablodaki Unsplash kimliği + fotoğraf sayfası URL'si. Sitedeki kapak: `site/public/hero/kapak-*`.

## Gerçekleşen bütçe (ölçüm: `plan/tasarim/hero-butce.json`)

| Kalem | Masaüstü | Mobil |
|---|---|---|
| Kare ölçüsü (AVIF) | 1600×1200 (4:3) | 900×1125 (4:5) |
| Toplam benzersiz kare | 66 (Faz A 18 + Faz B 48) | 36 (Faz A 12 + Faz B 24) |
| Sekans karesi (kapak hariç) | 65 | 35 |
| **Sekans toplamı (AVIF)** | **833,7 KB** / bütçe 900 KB ✅ | **330,3 KB** / bütçe 380 KB ✅ |
| Kare başı (AVIF) | 12,8 KB (hedef ≈13) | 9,4 KB (hedef ≈10) |
| **Kapak karesi (AVIF)** | **66,7 KB** / bütçe 120 KB ✅ | **40,2 KB** / bütçe 90 KB ✅ |
| Kaydırma payı → px/kare | 900 px / 48 kare = **18,75 px/kare** | 520 px / 24 kare = **21,67 px/kare** |
| WebP yedeği (AVIF'siz tarayıcı) | 1200×900, 1.426,9 KB | 675×844, 430,8 KB |

**WebP notu:** yedek yol AVIF desteklemeyen tarayıcılar içindir (Safari ≤15, Firefox <93).
Bütçe sözleşmesi birincil yol (AVIF) üzerinden tutulur; yedek yol kare ölçüsü ×0,75'e indirilerek
maliyeti sınırlandırıldı — kanvas gösterim ölçüsüne ölçeklediği için görünür bedeli yalnız
kaydırma sırasında hafif yumuşamadır. Kapak her iki yolda tam çözünürlüktedir.
