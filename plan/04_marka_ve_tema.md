# Şamandıra — Marka ve Tema Sistemi
**Tarih:** 2026-09-05 · Güncelleme: 2026-09-05 (K8 logo FİNAL + `yon.md` paleti) · K3: yüzey + repo/doküman rebrand

**Karar kaynağı (tek metin):** `plan/00_brief_eki.md` §3. Görsel yön / hero / hareket: `plan/tasarim/yon.md`. Tarihçe (Faz 1 Ufuk turu, reddedilen konseptler): `plan/logo/arastirma.md` + `plan/logo/arsiv/`. Final işaret: `plan/logo/secili/logo.png`.

---

## 1. Marka hikâyesi (neden Şamandıra?)

Şamandıra, denizcilikte **yol gösteren işaret**tir: sığlığı, güvenli geçidi, dönüş noktasını haber verir. Kaptan şamandıraları izleyerek rotasını bulur. Ürün tam olarak bunu yapıyor: şehrin gürültüsü içinde **görülmeye değer yerleri işaretliyor**, bölgeleri tanıtıyor ve gün gün **rotayı çiziyor**.

Metafor ürün ve ses tonunda kalır; **yüzeye yayılmaz** (K8). Görsel gönderme yalnız `plan/tasarim/yon.md` §5 kapalı listesidir.

| Denizcilik | Ürün (dil / veri, süs değil) |
|---|---|
| Şamandıra (işaret) | Öne çıkan yer / öneri kartı / harita markırı |
| Rota hattı | Günlük gezi planı (slot zinciri) |
| Deniz | Keşif alanı |
| Fener | Rehber yazıları |
| Pusula | Tercih sliderları (rota sihirbazı) |
| Demir atmak | Kaydedilen/paylaşılan rota |

**Konumlanma (kilit, 2026-09-05):** slogan + GEO tanım cümlesi birlikte kullanılır; ikisi de bölge-nötrdür (K6). Şehir adı yalnız veri katmanından (açık şehir) gelir.

- Slogan: **Gezilecek yerleri işaretler.**
- Tanım: **Şamandıra, bir şehirdeki gezilecek yerleri deneyim eksenlerine göre puanlayan ve gün gün rota kuran bir gezi rehberidir.**

Eski "Karadeniz'in kişisel gezi rehberi" cümlesi geçersizdir.

## 2. İsim ve slogan kullanımı

- Yazım: **Şamandıra** (baş harf büyük, Türkçe karakterli). Logo wordmark'ta küçük harf: **şamandıra**.
- Kod/URL/e-posta gibi ASCII gereken her yerde: **samandira**.
- **Slogan (kilit):** "Gezilecek yerleri işaretler." — header, footer, OG, hero H1 (noktasız). Aday listesi ve GEO gerekçesi: `plan/logo/arastirma.md` §5 (tarihçe) — seçim kilit.
- **GEO tanım cümlesi (kilit):** yukarıdaki tanım; ana sayfa, meta description, Organization JSON-LD, `llms.txt` ve `/hakkimizda` kelimesi kelimesine aynı kalır (`02_seo_mimarisi.md` §11).
- **CTA:** "Rotanı kur" (birincil), "Keşfe başla" (ikincil).
- Title: konu önce, marka sonda `{Konu} · Şamandıra`. Ana sayfa: `Şamandıra — Gezilecek Yerler ve Rota Planlayıcı`.

## 3. Renk sistemi

Kaynak: logodan ölçülen **bordo `#6C0000`** + mevcut `samandira` rampı. Tam tablo, kontrast çiftleri ve alan payları: **`plan/tasarim/yon.md` §1.2**. Özet:

| Token | Hex | Rol |
|---|---|---|
| `bordo-950` | `#2E0405` | en derin yüzey, scrim dibi |
| `bordo-900` | `#4A0708` | koyu blok, CTA bandı |
| **`bordo`** | **`#6C0000`** | logo karosu, koyu yüzey, **başlık mürekkebi** (kağıtta 11,2:1) |
| `bordo-700` | `#8E1710` | koyu hover / hairline |
| `samandira` | `#D6402C` | birincil CTA, aktif durum, markır — **%10** |
| `samandira-koyu` | `#A92E1E` | CTA hover/pressed |
| `signal` | `#F2B138` | "Sponsorlu" rozeti, fener parlaması |
| `kagit` | `#F4EFE7` | sayfa zemini |
| `kagit-koyu` | `#EBE3D6` | ikinci zemin |
| `tuz` | `#FBF8F3` | kart yüzeyi (saf beyaz yerine) |
| `ink` | `#142126` | gövde metni |
| `deniz` / `deniz-derin` | `#0A4D5C` / `#063642` | veri katmanı: rota/harita/grafik — birincil zemin değil |
| `yosun` / `kumsal` / `gunes` / `kopuk` | mevcut | grafik serileri, ince zeminler |

**60-25-10-5:** %60 nötr (kagit+tuz+kagit-koyu) · %25 bordo ailesi · %10 `samandira` · %5 deniz/signal. `samandira` **gövde metni rengi olarak yasak** (kağıtta 3,96:1). Buton üstü beyaz ≥16 px ve ≥600 ağırlık.

Saf beyaz yalnız logo çizgisi ve fotoğraf üstü metin. Kart zemini `tuz`.

## 4. Logo (K8 — FİNAL)

Kaynak dosya **sabittir:** `plan/logo/secili/logo.png` — bordo karo (`#6C0000`) üzerine beyaz çizgi şamandıra (kafes kule, fener, anemometre, bağlama halkaları, dalga). Köşe yarıçapı kenarın **%14,6'sı**. Cursor çizgiyi, kompozisyonu, oranı ve renkleri **değiştirmez**; yalnız üretim varlıkları üretir.

Ufuk / Sonar / Rota / Demir ve A-B-C turları tarihçedir (`plan/logo/arsiv/`).

Üretim (site): `site/public/logo/karo-seffaf.png`, `karo-acik.png`, `karo.png`; `icon-16/32/48.png` + `favicon.ico`; `icon-180.png` / `apple-touch-icon.png`; `icon-192.png`, `icon-512.png`, `icon-512-maskable.png`; `site/public/og-default.png`.

Kullanım matrisi:

| Yer | Varyant |
|---|---|
| Üst bant (masaüstü) | karo 32 px + wordmark `şamandıra` (Fraunces, küçük harf, −0,02em) |
| Üst bant (mobil) | yalnız karo 28 px |
| Alt bant | karo 40 px + wordmark |
| Favicon 16/32/48 + `.ico` | aynı karo, bordo zemin, ölçek (kompozisyon değişmez) |
| Apple-touch 180 / PWA 192 / 512 | tam karo, bordo zemin |
| Maskable 512 | aynı, güvenli bölge ≥ %18 kenar payı |
| OG kart / paylaşım | bordo zemin + karo + wordmark + slogan + GEO tanım (`og-default.png`) |
| Harita markırı | jenerik damla pin yasak; logodan halka + nokta (`yon.md` §5.7) |
| Açık zemin (e-posta, slayt) | `karo-acik.png` (kağıt üstüne karo) |
| Şeffaf kenar | `karo-seffaf.png` (dış köşeler alfa; illüstrasyon aynı) |

**Kelime kilidi:** karo + wordmark; boşluk ≈ karo kenarının 0,35 em'i. Minimum: karo ≥ 16 px tek başına; kilitte ≥ 24 px. Bileşen: `KelimeKilidi` + `LogoKaro` (`next/image`).

Kurallar: logo etrafında en az karo yüksekliğinin %35'i kadar boşluk; fotoğraf üstüne doğrudan konmaz (scrim veya karo zemini); gölge / outline / eğim / renk kaydırma **yasak**.

## 5. Tipografi

Ölçek tablosu: `plan/tasarim/yon.md` §1.3. Aile kilidi:

- **Fraunces** (display): başlıklar, logo wordmark, büyük sayılar.
- **Sora** (UI): gövde, butonlar, etiketler.
- Display 40px+: `letter-spacing: -0.02em` (kapak −0,03em), satır 0,98–1,1.
- Etiket katı: 11px, `uppercase`, `tracking-[0.24em]`.
- Sayısal veri: Sora `tabular-nums`; duygu özeti Fraunces italic alıntıyla açılabilir.
- Her iki fontta latin-ext var. `next/font` kurulumu korunur. Üçüncü font ana yönde yok.

## 6. Görsel dil ve motifler

Uygulama şartnamesi: **`plan/tasarim/yon.md`**. Kısa kilit:

- Ana yön **"Mürekkep ve Tuz"**; yedek **"Fener Nöbeti"** (`yon.md` §1.1 / §1.7).
- Hero = fotoğraf sekansı (K9), video yok; görsel kaynak kapalı liste (`yon.md` §2.6).
- Ağır denizcilik teması **yasak**. Gönderme yalnız 11 ufak trik (`yon.md` §5).
- Marquee / dalga bandı / sonar halkası / süzülen şamandıra **emekli**.
- **Boş durum metinleri (tone of voice):** samimi, kısa, bölge-nötr, emoji yok:
  - Boş liste: "Bu filtreyle kıyıda köşede bir şey kalmadı. Filtreleri gevşetip tekrar bakalım mı?"
  - Hata: "Pusula şaştı — sayfayı yenileyip tekrar dener misin?"
  - 404: "Sayfa bulunamadı — pusula şaştı"
  - CTA kalıbı: "Rotanı kur", "Keşfe başla", "Bölgeyi tanı" (emir kipinde ama nazik).

## 7. "Sponsorlu" ve güven rozetleri

- `sponsorlu_mekan` rozeti: `signal` (#F2B138) zemin, koyu metin, "Sponsorlu" — **her görünümde zorunlu** (etik + yasal şeffaflık; skor kırılımındaki +30 zaten görünür).
- `sehrin_klasigi` rozeti: deniz tonlu, "Şehrin Klasiği".
- Güven satırı (footer): "Önerilerimizin nedenini gösteririz: her skorun kırılımı açık." → şeffaflık, rakiplerden ayrışma cümlesi.
- Footer atıf satırı (yasal): `Harita verisi © OpenStreetMap katkıda bulunanlar` (yalnız harita/OSM verisi kullanılan sayfalarda görünür de olur; footer'da küçültülmüş tek satır yeter).

## 8. Üretilecek marka varlıkları (checklist)

- [x] Logo kararı — **K8:** `plan/logo/secili/logo.png`
- [x] Slogan + GEO tanım cümlesi kilidi
- [x] Şeffaf + açık zemin karo PNG
- [x] Favicon seti: `favicon.ico` (16/32/48), `apple-touch-icon.png` (180), PWA `icon-192/512.png` + maskable, `manifest`
- [x] `og-default.png` (1200×630): bordo zemin + kilit + slogan + tanım
- [ ] X/Twitter + Instagram profil görseli (1:1 karo) ve kapak — manuel
- [ ] Tek sayfalık marka rehberi PDF (B2B/sponsorluk görüşmeleri için — Faz 5)
- [ ] E-posta imza şablonu (ASCII adres, `karo-acik.png`)

## 9. TÜRKPATENT marka ön araştırması (manuel, ~1 saat)

1. `turkpatent.gov.tr` → marka araştırma (ücretsiz ön arama): "ŞAMANDIRA" kelime markası, sınıflar: **39** (seyahat düzenleme, rota planlama), **42** (yazılım/SaaS), **41** (yayıncılık/rehber içerik), (opsiyonel **43** yiyecek-içecek değil — kapsam dışı).
2. Benzer marka yoksa başvuru (~10 yıl koruma; öğrenci indirimi yok ama ücret makul, ~birkaç bin TL + vekil opsiyonel).
3. Alan adı zaten sizde; sosyal hesapları hemen alın: `@samandira` / `@samandirarehber` (Instagram, X, TikTok, YouTube) — ASCII handle kullanın (IDN handle desteklenmiyor).
4. "Alegre Group" için de 35/42 sınıf ön araştırması (B2B'ye geçince).
