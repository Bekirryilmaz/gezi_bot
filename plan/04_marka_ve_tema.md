# Şamandıra — Marka ve Tema Sistemi
**Tarih:** 2026-09-05 · K3 kararına göre: yüzey + repo/doküman rebrand · Logo konseptleri: `logo/` klasörü

---

## 1. Marka hikâyesi (neden Şamandıra?)

Şamandıra, denizcilikte **yol gösteren işaret**tir: sığlığı, güvenli geçidi, dönüş noktasını haber verir. Kaptan şamandıraları izleyerek rotasını bulur. Ürün tam olarak bunu yapıyor: şehrin gürültüsü içinde **görülmeye değer yerleri işaretliyor**, bölgeleri tanıtıyor ve gün gün **rotayı çiziyor**.

Metafor eşlemesi (tasarımda tutarlı kullanılır):

| Denizcilik | Ürün |
|---|---|
| Şamandıra (işaret) | Öne çıkan yer / öneri kartı / harita markırı |
| Rota hattı | Günlük gezi planı (slot zinciri) |
| Deniz | Karadeniz — arka plan, palet |
| Fener | Rehber yazıları (yön veren uzun içerik) |
| Pusula | Tercih sliderları (rota sihirbazı) |
| Demir atmak | Kaydedilen/paylaşılan rota |

**Konumlanma cümlesi:** "Şamandıra, Karadeniz'in kişisel gezi rehberi — keşfet, oku, gün gün rotanı kur."

## 2. İsim ve slogan kullanımı

- Yazım: **Şamandıra** (baş harf büyük, Türkçe karakterli). Logo wordmark'ta küçük harf: **şamandıra**.
- Kod/URL/e-posta gibi ASCII gereken her yerde: **samandira** (Türkçe karaktersiz — mevcut proje kuralıyla uyumlu).
- Slogan adayları (anket yapın — Instagram hikâyesi bile yeterli):
  1. **"Rotanı şamandıra ile bul."** (önerilen — eylem + marka bir arada, SEO başlıklarına uyar)
  2. "Şehri işaretleyen rehber."
  3. "Yönün belli, rotan hazır."
  4. "Karadeniz'in rota işareti."
- Title kalıbı: `Şamandıra — {sayfa konusu}` yerine konu önce: `{Konu} | Şamandıra` (SEO'da ilk 30 karakter altın). Ana sayfa: `Şamandıra — Samsun Gezi Rehberi ve Rota Planlayıcı`.

## 3. Renk sistemi

Mevcut tema (deniz/kopuk/kumsal/gunes) korunur; **şamandıra kırmızısı** vurgu rengi olarak eklenir. Gerçek deniz şamandıraları kırmızı/yeşildir; mevcut deniz yeşili paletiyle kırmızı-turuncu vurgu kontrastı güçlü ve denizcilik açısından doğru.

| Token | Hex (öneri) | Kullanım |
|---|---|---|
| `deniz-derin` (mevcut) | korunur | arka plan, footer, gece modu yüzeyler |
| `deniz` / `deniz-yuzey` (mevcut) | korunur | birincil yüzey, linkler |
| `kopuk` (mevcut) | korunur | metin, kart zemini |
| `kumsal` (mevcut) | korunur | ikincil zemin, bölüm ayraçları |
| `gunes` (mevcut) | korunur | ikincil vurgu, rozetler, hover |
| **`samandira` (YENİ)** | **#D6402C** | **birincil CTA, harita markırları, aktif durum, logo vurgusu** |
| `samandira-koyu` (YENİ) | #A92E1E | CTA hover/pressed |
| `signal` (YENİ, opsiyonel) | #F2B138 | uyarı/rozet ("Sponsorlu", "Klasik") |
| `yosun` (mevcut varsa korunur) | — | başarı/doğa etiketleri |

Kurallar: **60-30-10** — %60 nötr (kopuk/kumsal), %30 deniz tonları, %10 şamandıra kırmızısı (yalnız CTA + markır + logo). Kırmızıyı metin rengi olarak kullanma. Kontrast: `#D6402C` üzerine beyaz metin AA uyumlu (4.5:1 ≈ kontrol edildi, sınırda — buton metni kalın/büyükse geçer; gerekirse `samandira-koyu` kullan).

Tailwind v4'te token tanımı (`site/src/app/globals.css` içinde `@theme`):
```css
@theme {
  --color-samandira: #D6402C;
  --color-samandira-koyu: #A92E1E;
  --color-signal: #F2B138;
}
```

## 4. Logo

Üç konsept üretildi (`logo/` klasörü, SVG — ölçeklenebilir, düzenlenebilir):

- **Konsept A — `marka_a_samandira.svg`:** Geometrik şamandıra markı. Direk + tepe ışığı, kırmızı-beyaz gövde, altında iki dalga çizgisi. Favicon/app ikonu için en dayanıklısı.
- **Konsept B — `marka_b_pin_samandira.svg`:** Harita pini × şamandıra hibrit. "Yer" kavramını anında okutur; harita markırlarında ve keşif bağlamında güçlü.
- **Konsept C — `marka_c_kelime.svg`:** Yatay kilit — A markı + `şamandıra` wordmark (Fraunces) + slogan alt satırı. Header, OG kartı, sunum kapağı için.

Kullanım matrisi:

| Yer | Konsept |
|---|---|
| Favicon / apple-touch / PWA ikonu | A (tek renk beyaz varyantı `deniz-derin` zeminde) |
| Site header | C (kompakt: mark + wordmark) — mobilde yalnız A |
| OG kart / paylaşım | C + deniz degrade zemin |
| Harita markırı | B (mini şamandıra pinleri — jenerik pin YERİNE; ayırt edici imza) |
| App ikonu (ileride) | A, yuvarlatılmış kare, `deniz-derin` zemin |
| E-posta imzası / sunum | C |

Kurallar: logo etrafında en az mark yüksekliği kadar boşluk; `deniz-derin` zeminde beyaz/kırmızı versiyon, açık zeminde orijinal; logoyu fotoğraf üstüne doğrudan koyma (degrade scrim kullan); asla gölge/outline ekleme.

**Karar süreci önerisi:** `logo/onizleme.html`'i açın → A/B/C'yi yan yana görün → ikisini eleyip seçileni Hiranur'la netleştirin. Seçimden sonra: seçili konseptin (1) tam renk, (2) tek renk beyaz, (3) tek renk koyu varyantları + favicon seti (16/32/48/180/192/512) üretilir (T-03 talimatı).

## 5. Tipografi

- **Fraunces** (display — mevcut): başlıklar, logo wordmark, büyük sayılar. Karakter: sıcak, editoryal, "rehber" hissi.
- **Sora** (UI — mevcut): gövde, butonlar, etiketler. 
- Yeni kural: sayısal veri (puanlar, mesafeler, gün sayıları) Sora tabular-nums ile; duygu özeti blokları Fraunces italic alıntıyla açılabilir (öznel/nesnel ayrımını tipografi de anlatsın — brif'in "iki metin türü karışmasın" kuralına görsel destek).
- Her iki fontta latin-ext var (ş, ı, ğ sorunsuz). `next/font` mevcut kurulum korunur.

## 6. Görsel dil ve motifler

- **Dalga ayraçlar:** bölümler arası ince SVG dalga çizgisi (kumsal→deniz geçişleri).
- **Rota hattı:** kesikli çizgi + düğüm noktalarında mini şamandıra (liste numaralandırması bile şamandıra düğümüyle: "1. durak" yerine küçük marka ikonu + sayı).
- **Işık/parlama:** tepe ışığında küçük `gunes` parlaması — hero'da deniz üstünde uzak fener silueti (illüstrasyon, fotoğraf değil).
- **Fotoğraf stili:** gerçek Samsun fotoğrafları, gün ışığı, hafif soğuk deniz tonu; filtre tutarlılığı için tek LUT/preset (Lightroom'da tek ayar, tüm fotoğraflara aynı).
- **İllüstrasyon:** şimdilik yok; gerekirse düz vektör, 2 renk (deniz + şamandıra).
- **Boş durum metinleri (tone of voice):** samimi, kısa, Karadeniz sıcaklığı, emoji yok:
  - Boş liste: "Bu filtreyle kıyıda köşede bir şey kalmadı. Filtreleri gevşetip tekrar bakalım mı?"
  - Hata: "Pusula şaştı — sayfayı yenileyip tekrar dener misin?"
  - CTA kalıbı: "Rotanı kur", "Keşfe başla", "Bölgeyi tanı" (emir kipinde ama nazik).

## 7. "Sponsorlu" ve güven rozetleri

- `sponsorlu_mekan` rozeti: `signal` (#F2B138) zemin, koyu metin, "Sponsorlu" — **her görünümde zorunlu** (etik + yasal şeffaflık; skor kırılımındaki +30 zaten görünür).
- `sehrin_klasigi` rozeti: deniz tonlu, "Şehrin Klasiği".
- Güven satırı (footer): "Önerilerimizin nedenini gösteririz: her skorun kırılımı açık." → şeffaflık, rakiplerden ayrışma cümlesi.
- Footer atıf satırı (yasal): `Harita verisi © OpenStreetMap katkıda bulunanlar` (yalnız harita/OSM verisi kullanılan sayfalarda görünür de olur; footer'da küçültülmüş tek satır yeter).

## 8. Üretilecek marka varlıkları (checklist)

- [ ] Logo kararı (A/B/C) — kullanıcı + Hiranur
- [ ] Seçili logonun 3 renk varyantı (tam / beyaz / koyu) — SVG
- [ ] Favicon seti: `favicon.ico` (16/32/48), `apple-touch-icon.png` (180), PWA `icon-192/512.png`, `manifest.json`
- [ ] `og-default.png` (1200×630): deniz degrade + C kilit + slogan (next/og ile dinamik sürüm T-07'de; statik fallback bu)
- [ ] X/Twitter + Instagram profil görseli (1:1 A markı) ve kapak (C + deniz)
- [ ] Tek sayfalık marka rehberi PDF (B2B/sponsorluk görüşmeleri için — Faz 5)
- [ ] E-posta imza şablonu (ASCII adres, logo PNG)

## 9. TÜRKPATENT marka ön araştırması (manuel, ~1 saat)

1. `turkpatent.gov.tr` → marka araştırma (ücretsiz ön arama): "ŞAMANDIRA" kelime markası, sınıflar: **39** (seyahat düzenleme, rota planlama), **42** (yazılım/SaaS), **41** (yayıncılık/rehber içerik), (opsiyonel **43** yiyecek-içecek değil — kapsam dışı).
2. Benzer marka yoksa başvuru (~10 yıl koruma; öğrenci indirimi yok ama ücret makul, ~birkaç bin TL + vekil opsiyonel).
3. Alan adı zaten sizde; sosyal hesapları hemen alın: `@samandira` / `@samandirarehber` (Instagram, X, TikTok, YouTube) — ASCII handle kullanın (IDN handle desteklenmiyor).
4. "Alegre Group" için de 35/42 sınıf ön araştırması (B2B'ye geçince).
