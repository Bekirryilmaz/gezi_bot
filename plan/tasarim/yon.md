# Şamandıra — Görsel Yön ve Tasarım Sözleşmesi

**Tarih:** 2026-09-05 · **Oturum:** tek yaratıcı tur (Opus, K10) · **Çıktı:** yalnız doküman — kod yok, uygulama yok.
**Dayandığı kararlar:** K5 (çıta "oha"), K6 (bölge kilidi yok), K7 (SEO + GEO baş kriter), **K8 (logo FİNAL)**, **K9 (hero = fotoğraf sekansı)**, K10 (model bütçesi) — `00_brief_eki.md` §3.
**Uygulayacak model:** Grok 4.6 extra high. Auto mod yasak (K10).

Bu dosya `plan/04_marka_ve_tema.md`'nin **üzerine** okunur. Çelişkide bu dosya kazanır.

---

## 0. Karar özeti (10 madde)

1. **Ana yön: "Mürekkep ve Tuz"** — sıcak kağıt üzerine **bordo mürekkep**; fotoğraf tam kanat *plaka* olarak girer, sayfanın iskeletini tipografi kurar, etki zamanlamadan gelir (süslemeden değil). Yedek yön: **"Fener Nöbeti"** (koyu, veri-cihazı hissi).
2. **Bordo (#6C0000) artık marka mürekkebidir**, vurgu değil: kağıt üzerinde 11,2:1 kontrastla **başlık rengi olarak kullanılabilir**. `samandira #D6402C` %10 kuralıyla yalnız CTA/aktif durum/markır; `deniz` ailesi veri-rota-harita katmanına iner.
3. **Hero: asimetrik split** (metin solda 5/12, fotoğraf plakası sağda 7/12, sağ kenara taşar). Metin **hiçbir zaman fotoğrafın üstünde değil** — "tam ekran fotoğraf + ortada dev yazı" klişesi kırılır, kontrast ve LCP kazanılır.
4. **Sekans mekanizması iki fazlı:** Faz A = açılış (18 kare / 1,5 s, zaman tetikli, tek sefer, kesilebilir), Faz B = seyir (48 kare / 900 px kaydırma payı = 18,8 px/kare). Mobil 36 kare. Bütçe: masaüstü ≤ 900 KB, mobil ≤ 380 KB.
5. **İki üretim yolu:** A = kendi çekimimizden kare çıkarımı (gerçek flipbook, hedef). B = Unsplash ile **plaka kurgusu** (7–9 fotoğraf, çapraz geçiş) — köprü; bileşen arayüzü aynı kalır, fotoğraflarımız gelince yol A'ya geçilir.
6. **Fotoğrafsız kart birinci sınıf durumdur** (bugün DB'de 1.719 yer, **0 fotoğraf**). Varsayılan kart tipografiktir; fotoğraf geldiğinde aynı kutu oranına oturur, ızgara adımı ve kart yüksekliği değişmez → CLS 0.
7. **Marquee kararı: RED.** Sürekli otomatik kayan şerit (WCAG 2.2.2) yerine kullanıcı kontrollü yatay şerit. `T-16` madde 9'un "kategori marquee bandı" ve mevcut `.serit-kaydir`/`.dalga`/`.sonar-halka`/`.samandira-suz` sınıfları emekliye ayrılır.
8. **Şamandıra göndermesi 11 "ufak trik"le sınırlıdır** (§5 kapalı liste). Ağır tema yasak: dalga bandı, çıpa/pusula ikonu, halat dokusu, denizci dili.
9. **Hareket sözleşmesi:** mesafe ≤ 24 px, yalnız `transform`/`opacity`, giriş animasyonları tek sefer, ekran dışında duraklar, `prefers-reduced-motion`'da içerik **son okunabilir halinde** durur (hidrasyona güvenli tercih okuma zorunlu).
10. **Yerleşim sözleşmesi eşiklidir:** 1 şehir / 0 rehber / 0 fotoğraf / 0 kayıtlı rota durumunda da sayfa "boş" değil "erken" görünür; modüller dolarken hiçbir bölüm yeniden tasarlanmaz, yalnız varyant değiştirir.

### Bu doküman neyi geçersiz kılar

| Geçersiz | Yerine |
|---|---|
| Eski Ufuk logo matrisi (Faz 1) | K8: `plan/logo/secili/logo.png`; güncel matris `04_marka_ve_tema.md` §4 + bu dosya §1.6 |
| `04_marka_ve_tema.md` §6 "prosedürel deniz / hero'da fotoğraf yok", "dalga ayraçlar", "rota hattı motifi" | K9 fotoğraf sekansı (§2) + §5 ufak trikler |
| `logo/arastirma.md` §8 "bölümlenmiş kaydırma anlatısı: ufuk → sığlık → rota → demir" (isimlendirme) | §4.2 koreografi haritası — bölüm adları denizcilikten değil **kullanıcı sorusundan** türer |
| `07_cursor_talimatlari.md` T-16 madde 9 (marquee, sonar halkası, süzülen şamandıra) | §4.4 (marquee red), §5 (ufak trikler) |
| `ufuk-*.svg`, `LogoUfuk`, `HeroUfuk`, `DenizUfku`, `UfukCizgisi` | Emekli. Yerine: `LogoKaro`, `KelimeKilidi`, `HeroKapak` |

---

## 1. Görsel yön

### 1.1 Ana yön — "Mürekkep ve Tuz" (kod adı: `murekkep`)

**Tek cümle:** *Bir seyir defterinin sıcak kağıdı üzerine bordo mürekkeple basılmış çağdaş atlas; fotoğraf sayfaya plaka gibi çakılır, tipografi taşıyıcı sistemdir, hareket yalnız zamanlamada duyulur.*

**Neden ödül ayarında:**
- Ödüllü seyahat işlerinde baskın renk **fotoğraf ve zemindir**, marka rengi %10'u geçmez (Awwwards travel taraması, iki turdur doğrulandı). Bu yön o disiplini token seviyesine yazıyor.
- Typewolf "Site of the Day" listesinde tekrarlayan formül **yüksek kontrastlı display serif + nötr grotesk** (Grenette+Styrene, Editorial Old+Neue Montreal, Tobias+Diatype). Fraunces + Sora tam bu formül; ölçek sıçraması eksikti, §1.3 onu kapatıyor.
- Asimetri **kenar notu ızgarasından** gelir (12 kolonun sol 1 kolonu etiket/skor/tarih için ayrılır), eğik bloklardan veya dekoratif kaostan değil. Kalıcı, ölçeklenen bir asimetri.
- Bugünkü gerçeği (0 fotoğraf) kusur değil karakter yapar: tipografik kart bu yönde **kasıtlı** durur.

**Neden "alışıldık kurumsal gezi sitesi" değil:** Figma Community'de "travel" kategorisinin adı bile **Travel *Booking***. O kalıbın parçaları — hero ortasında nereye/ne zaman/kaç kişi arama kutusu, "Book now", turkuaz-turuncu gradyan, yuvarlak avatarlı yorum karuseli, uçak/valiz/pasaport ikonografisi, polaroid çerçeve, el yazısı script font — **hiçbiri kullanılmaz**. Şamandıra bir rezervasyon hunisi değil, **atlas + defter**: hero'da arama kutusu yok; "Rotanı kur" bir plan aracının kapısıdır, bir satış çağrısı değil.

### 1.2 Palet genişletmesi (logodaki bordoyla uyumlu)

Logodan **ölçülen** değerler: zemin `#6C0000` (108,0,0 — tek kanal doygun bordo), çizgi `#FFFFFF`, karo köşe yarıçapı kenarın **%14,6'sı**. Palet bu iki değerin üzerine, tek hue'lu bir ramp olarak kuruldu; mevcut `samandira`/`samandira-koyu` bu rampın parlak basamakları olarak **zaten uyumlu** (6C0000 → A92E1E → D6402C).

| Token | Değer | Durum | Rol | Alan payı |
|---|---|---|---|---|
| `bordo-950` | `#2E0405` | yeni | en derin yüzey: alt bant, hero scrim dibi, gece bölümü | — |
| `bordo-900` | `#4A0708` | yeni | koyu blok: alıntı kutusu, koyu kart, CTA bandı | — |
| **`bordo`** | **`#6C0000`** | **yeni (marka kilidi)** | logo karosu, koyu ana yüzey, **başlık mürekkebi** (kağıtta 11,2:1) | **%25** |
| `bordo-700` | `#8E1710` | yeni | koyu zeminde hover/hairline, ikinci koyu ton | — |
| `samandira` | `#D6402C` | mevcut | birincil CTA, aktif durum, harita markırı, seçim | **%10** |
| `samandira-koyu` | `#A92E1E` | mevcut | CTA hover/pressed, `destructive` | — |
| `signal` | `#F2B138` | mevcut | rozet ("Sponsorlu"), fener parlaması, uyarı | ≤%3 |
| `kagit` | `#F4EFE7` | mevcut | sayfa zemini | **%60 (kagit+tuz)** |
| `kagit-koyu` | `#EBE3D6` | mevcut | ikinci zemin, bölüm ayrımı, tablo şeridi | — |
| `tuz` | `#FBF8F3` | yeni | kart/yüzey zemini — **saf beyaz yerine** | — |
| `ink` | `#142126` | mevcut | gövde metni (kağıtta 12,5:1) | — |
| `deniz` / `deniz-derin` | `#0A4D5C` / `#063642` | mevcut, **rol değişti** | veri katmanı: rota hattı, grafik ekseni, harita çizgisi, bağlantı altı çizgisi | %5 |
| `yosun` / `kumsal` / `gunes` / `kopuk` | mevcut | rol daraldı | grafik serileri, kategori işaretleri, ince zeminler | %5 |

**Saf beyaz (`#FFFFFF`) yalnız iki yerde:** logo çizgisi ve fotoğraf üstündeki metin. Kart zemini `tuz`.

**Ölçülmüş kontrast sözleşmesi** (uygulamada bu sayılar doğrulanır):

| Çift | Oran | Karar |
|---|---|---|
| `#FFFFFF` / `bordo #6C0000` | **12,8:1** | AAA — koyu yüzeyde her boy metin serbest |
| `ink` / `kagit` | **12,5:1** | gövde metni |
| `bordo` / `kagit` | **11,2:1** | **başlıklar bordo mürekkeple yazılabilir** |
| `#FFFFFF` / `samandira` | **4,53:1** | AA sınırda: buton metni ≥16 px **ve** ≥600 ağırlık; küçültülecekse `samandira-koyu` |
| `samandira` / `kagit` | **3,96:1** | ⛔ metin rengi olarak **yasak**; yalnız ikon/kenarlık/büyük sayı (3:1 eşiği) |
| `#FFFFFF` / `bordo-700` | 9,2:1 | koyu zeminde ikincil yüzey |

**60-30-10 güncellemesi:** %60 nötr (kagit + tuz + kagit-koyu) · %25 bordo ailesi (koyu bloklar + fotoğraf scrim + başlık mürekkebi) · %10 `samandira` · %5 deniz/signal/grafik. Kırmızı hâlâ **asla** gövde metni rengi değil.

### 1.3 Tipografi ölçeği

Aile kilidi korunur: **Fraunces** (display) + **Sora** (UI/gövde), `next/font`, latin-ext. Üçüncü font **eklenmez** — etiket katı Sora'nın uppercase + geniş tracking varyantıyla kurulur (yedek yön hariç, §1.7).

| Kat | Font / ağırlık | Boyut (375 → 1280) | Satır | Harf aralığı | Kullanım |
|---|---|---|---|---|---|
| Kapak | Fraunces 500–600 | 44 → **100 px** | 0,98–1,02 | −0,03em | yalnız hero `h1` |
| Bölüm | Fraunces 500 | 30 → 54 | 1,05 | −0,02em | `h2` |
| Alt bölüm | Fraunces 500 | 22 → 30 | 1,15 | −0,015em | `h3`, ilçe adı, kart grubu |
| Kart başlığı | Sora 600 | 17 → 19 | 1,25 | −0,01em | yer/rehber/şehir kartı |
| Gövde | Sora 400 | 16 → 17 | 1,60–1,65 | 0 | tanıtım, editoryal — **ölçü 62–68 karakter** |
| İndeks gövdesi | Sora 400 | 14 → 15 | 1,50 | 0 | liste, yan bilgi, tablo (yoğun yüzeyler) |
| Etiket | Sora 500 | 11 px sabit | 1,2 | **+0,24em**, uppercase | bölüm etiketi, rozet, kenar notu |
| Büyük sayı | Fraunces 500, tabular | 40 → 72 | 1,0 | −0,02em | istatistik bandı |
| Satır içi sayı | Sora 500, tabular | miras | — | 0 | skor, mesafe, süre, gün |

**Kurallar:** (a) kapak → gövde ölçek sıçraması **≥ 4×** (Typewolf ölçümü 3,6×; hedef daha agresif); (b) aynı ekranda en fazla **3 tipografik kat** yan yana; (c) tüm başlıklarda `text-wrap: balance`, paragraflarda `text-pretty`; (d) sayı içeren her yerde `tabular-nums` — sayı değişince satır kaymaz (1.719 → 1.804 geçişi yerleşimi bozmaz); (e) hiyerarşi **boyutla** kurulur, ağırlık zıplamasıyla değil; (f) tırnak `“ ”`, üç nokta `…`, marka adı ve ölçü birimlerinde bölünmez boşluk (`1.719 yer`, `40 km`).

### 1.4 Boşluk ve ritim

- **Taban 4 px.** Ölçek: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128 / 160.
- **Bölüm ritmi:** mobil 64 (dar) – 80 (normal); 1280 **128** (normal) – **160** (kapak sonrası ilk bölüm ve doruk CTA öncesi). Yoğunluk kademesi: pazarlama yüzeyleri ferah, indeks/liste yüzeyleri sıkı (kart içi 16/12).
- **Kabuk:** içerik 1200 px maks; kenar payı 20 (375) / 40 (768) / 64 (1280+). Editoryal kolon 660–720 px.
- **Izgara:** 12 kolon. İçerik 2–11 kolonda yaşar; **sol 1 kolon "kenar notu"** için ayrılır (etiket, skor, tarih, "3/12" sayacı). 1280 altında kenar notu başlığın üstüne düşer, ızgara 6 kolona iner, 375'te tek kolon.
- **Dikey ritim kilidi:** kart ızgarası adımı sabit — 1 satırda 3 kart (1280), 2 kart (768), 1 kart (375); kart yüksekliği **içerikten bağımsız sabit** (başlık 2 satır + özet 2 satır `line-clamp`).

### 1.5 Doku ve ışık

- **Kağıt dokusu:** statik SVG gürültü, kağıt zeminlerde **%3–4** opaklık, koyu bloklarda %6. Animasyon yok, `background-attachment: fixed` yok (mobil kaydırma maliyeti).
- **Fotoğraf plakası iki katman taşır:** (1) `bordo-950` → şeffaf dikey scrim (alt %70'e kadar) — plakanın altına oturan etiketin okunması için; (2) **çok hafif sıcak duotone** (bordo + kagit) **yalnız hero'da**. İçerik fotoğraflarında duotone **yok** — yerin gerçek rengini değiştirmek yanıltıcıdır.
- **Işık:** tek kaynak, sol üst, düşük açı. Parlama (glow) yalnız birincil CTA ve marka noktasında: yarıçap ≤ 24 px, opaklık ≤ %35, rengi `samandira` veya `signal`.
- **Gölge yasağı:** kartlarda ve panellerde `box-shadow` yok. Yükseklik **tonla** (tuz/kagit-koyu farkı) ve **1 px hairline** ile anlatılır: kağıt üzerinde `bordo` %12, koyu üzerinde `kagit` %14. Yalnız üst üste binen katmanlar (sheet, dialog, dropdown) gölge kullanır.
- **Glassmorphism, mesh/aurora gradyan, neon, 3B kabartma: yasak.** (Skill'in "Aurora UI" önerisi bu turda da reddedildi — jenerik SaaS işareti.)

### 1.6 Köşe dili ve marka kullanımı

Köşe dili **doğrudan logodan** türer ve üç kademeyle sınırlıdır:

| Yüzey | Yarıçap | Not |
|---|---|---|
| Marka karosu (logo, app ikonu, favicon zemini, OG karosu) | **kenarın %14,6'sı** (orana bağlı) | ölçüldü; yalnız marka karosunda oransal yarıçap kullanılır |
| Medya plakası | 0 px tam kanat · ızgara içinde 4 px | fotoğraf "çakılır", yumuşamaz |
| Kart / panel | 12 px | |
| Kontrol (buton, giriş, select) | 8 px | mevcut `--radius: 10 px` → 8 |
| Filtre çipi | 999 px | **tek** yuvarlak öğe; ayrışması kasıtlı |

Aynı ekranda en fazla 3 farklı yarıçap görünür.

**Logo kullanım matrisi (K8 — dosya sabit, yalnız üretim varlığı çıkarılır):**

| Yer | Varyant |
|---|---|
| Üst bant (masaüstü) | marka karosu 32 px + wordmark `şamandıra` (Fraunces, küçük harf, −0,02em) |
| Üst bant (mobil) | yalnız marka karosu 28 px |
| Alt bant | karo 40 px + wordmark, tek renk `kagit` (koyu zemin) |
| Favicon 16/32/48 + `.ico` | **sadeleştirilmiş türev**: 16 px'te kafes/anemometre okunmaz → gövde + fener + tek dalga; kompozisyon birebir korunur, yeni konsept değil |
| Apple-touch 180 / PWA 192 / 512 | tam illüstrasyon, bordo karo |
| Maskable 512 | aynı, güvenli bölge ≥ %18 kenar payı |
| OG kart (1200×630) | bordo zemin + karo + slogan + GEO tanım cümlesi |
| Harita markırı | jenerik damla pin **yasak**; logodan alınmış halka + nokta |
| Fotoğraf üstü | doğrudan konmaz; scrim veya karo zemini şart |

Boşluk: logo etrafında en az karo yüksekliğinin **%35'i**. Minimum: karo ≥ 24 px (wordmark'lı kilitte ≥ 28 px). Gölge/outline/eğim/renk değişimi **yasak**.

### 1.7 Yedek yön — "Fener Nöbeti" (kod adı: `fener`)

**Tek cümle:** *Gece nöbeti: bordo-siyah derin yüzey, logonun kendi dili olan beyaz hairline çizim, karanlıktan ışıkla çıkan fotoğraflar, bir seyir cihazı gibi okunan veriler.*

| Boyut | Karar |
|---|---|
| Palet | Zemin `gece #1A0304`; yüzey `bordo-900`; hairline `kagit` %14; metin `kopuk` (17,4:1); vurgu `samandira`; ışık `signal`. Kağıt tonları yalnız "ışıklı ada" bloklarında. |
| Tipografi | Ana yönün ölçeği + **tek mono kat** (DM Mono veya JetBrains Mono, yalnız 11–13 px etiket/sayı). Bedeli: +1 font (subset ≈ 14 KB) — Typewolf SOTD'de mono üçüncü kat standart hâle geldi. |
| Boşluk | Bir kademe sıkı: bölüm ritmi 96–112 (1280), kart içi 12/8; veri yoğun yüzeyler öne çıkar. |
| Doku / ışık | Film grain %5; **statik** ışık süpürmesi (gradyan, animasyon değil); fotoğraf kenarları karanlığa doğru sönümlenir (vignette maskesi). |
| Köşe | **0 px** (keskin) — yalnız marka karosu %14,6 ve çip 999 px. |
| Ne zaman devreye girer | (a) fotoğraf hattı 3 aydan uzun boş kalırsa — fotoğrafsız site koyu yüzeyde daha kasıtlı durur; (b) kullanıcı kağıt zemini "fazla sakin" bulursa. |
| Riski (yedek olma nedeni) | Uzun editoryal metin (rehber yazıları, ilçe tanıtımları) koyu zeminde daha yorucu okunur; K7 gereği içerik ağırlığı artacağı için varsayılan olamaz. Ayrıca `color-scheme: dark` + form/scrollbar bakımı ek iş. |

İki yön **aynı tokenları** kullanır, yalnız zemin/metin eşlemesi ve köşe/doku değerleri değişir → yön değişimi bir tema geçişidir, yeniden tasarım değil.

---

## 2. Hero mekanizması — fotoğraf sekansı (flipbook)

### 2.1 Kompozisyon

**Asimetrik split** (klişe kırıcı ana hamle): 1280'de metin sol **5/12**, plaka sağ **7/12** ve sağ kenara taşar (full-bleed sağ); plaka yüksekliği 78vh, üst hizası üst bandın 24 px altı. 375'te plaka üstte (4:5, ekranın ~%52'si), metin altta.

Metin bloğu sırası: **etiket** (11 px, `GEZİ REHBERİ`) → **h1** (Fraunces 100 px, iki satır, `balance`) → **GEO tanım cümlesi** (Sora 17/1,65 — K7 gereği birebir sabit metin) → **çift CTA** ("Rotanı kur" birincil / "Keşfe başla" ikincil) → **mikro kanıt satırı** (`1.719 yer · 15 ilçe · 6 deneyim ekseni`, tabular).

**Metin asla fotoğrafın üstünde değil.** Kazanç: kontrast garantisi (scrim hesabı yok), LCP elemanı metin olabilir, mobilde okunurluk sabit.

### 2.2 Mekanizma: iki faz

| Faz | Tetikleyici | Kare | Süre / mesafe | Eğri |
|---|---|---|---|---|
| **A — açılış** | zaman (sayfa yükünde, **tek sefer**) | 18 (mobil 12) | 1,5 s ≈ 12 fps | kare aralıkları ease-out: başta 90 ms → sonda 140 ms (`--ease-cikis` hissi). "Kamera duruyor" etkisi |
| **B — seyir** | kaydırma (scrub, ileri-geri) | 48 (mobil 24) | 900 px kaydırma payı = **18,8 px/kare** (mobil 520 px = 21,7 px/kare) | lineer scrub + ~100 ms `lerp` yumuşatma (kaydırma jitter'ını gizler) |

Toplam benzersiz kare: **66 masaüstü / 36 mobil**. Gerekçe: rahat bant 15–20 px/kare (10 px altı görülmeyen kareye para ödemek, 30 px üstü basamaklı görünmek); 60–180 kare aralığı üstünde algılanan akıcılık artmıyor, bayt artıyor. Faz A kendiliğinden hareketi **1,5 s < 5 s** olduğu için duraklat kontrolü gerekmez; Faz B tamamen kullanıcı kontrolündedir.

**Kesilebilirlik:** kullanıcı Faz A sırasında kaydırırsa Faz A anında biter ve Faz B devralır (yarı yolda kalan animasyon yok).

### 2.3 Varlık ve bütçe

| Kalem | Masaüstü | Mobil |
|---|---|---|
| Kare genişliği | 1600 px (kırpım 4:3) | 900 px (kırpım 4:5, ayrı set) |
| Format | AVIF birincil + WebP yedek (q 72–80) | aynı |
| Kare başı hedef | ≈ 13 KB | ≈ 10 KB |
| **Sekans toplam bütçesi** | **≤ 900 KB** | **≤ 380 KB** |
| Kapak karesi (ayrı) | ≤ 120 KB, `priority` | ≤ 90 KB |

**Yükleme stratejisi:** kapak (kare 01) `fetchpriority="high"` → kare 02–12 hemen (eager) → kalanlar **ikili altbölme** sırasıyla (ortadan başlayıp aralıkları bölerek: hızlı kaydıran kullanıcı boşluk görmez), en fazla **6 eşzamanlı** istek. Henüz gelmemiş kare istenirse **en yakın yüklü kare** çizilir — asla boş çerçeve. Kanvas ölçüsü gösterim ölçüsüne eşitlenir (fazla piksel = boşa bellek), kutu `aspect-ratio` ile önceden ayrılır (CLS 0).

### 2.4 İki üretim yolu

| | **Yol A — kendi çekimimiz (hedef)** | **Yol B — Unsplash köprüsü** |
|---|---|---|
| Kaynak | Tek çekim 4–6 s, sabit tripod veya **yavaş** pan/tilt, 30 fps → kare çıkarımı | 7–9 fotoğraf |
| Mekanizma | Gerçek flipbook: kare kare aynı sahne | **Plaka kurgusu:** iki katman çapraz geçiş; plaka 1,1 s tutar, geçiş 320 ms; kaydırmada plaka indeksi ilerlemeye bağlanır |
| Neden | "Video hissi" yalnız sürekli kamera hareketinde oluşur | Farklı fotoğraflar flipbook yapmaz — dürüst adı **sinema kurgusu**; ara kare üretilmez |
| Seçim şartı | — | Aynı ışık sıcaklığı, ufuk yüksekliği ±%8, yatay çizgi hizası tutmalı; tutmazsa slayt gösterisi gibi durur |
| Geçiş | — | Fotoğraflarımız gelince yol A'ya geçilir; **bileşen arayüzü, kapak ve fallback aynı kalır** |

Sahne fikri (her iki yolda aynı): **"gün açılışı"** — ufuk çizgisi/şafak → kıyıya yaklaşma → yerin ortaya çıkışı. Bölge-nötr (K6): tanınabilir şehir silueti değil, **kıyı/ufuk/ışık**.

### 2.5 Fallback zinciri

| Koşul | Davranış |
|---|---|
| `prefers-reduced-motion: reduce` | Yalnız **statik kapak** karesi; hiçbir ek kare indirilmez; h1/CTA/kanıt satırı son okunabilir halinde |
| JS yok / hata / sekans yüklenemedi | Statik kapak (`<img>`), hero tam işlevli kalır |
| `saveData` veya `effectiveType` 2g/3g | Sekans hiç istenmez, statik kapak |
| `deviceMemory < 4` veya `hardwareConcurrency ≤ 4` | Mobil sekans (36 kare) kullanılır |
| Sekans yüklenirken | Kapak görünür kalır, hazır olunca **aynı çerçevede** devralır |
| Hero ekran dışında / sekme gizli | Sekans durur, RAF iptal |

**Erişilebilirlik:** kanvas/plaka `aria-hidden="true"` (anlam metinde), kapak `alt=""` (dekoratif), hero başlığı gerçek `h1`. Hero'da otomatik dönen içerik yok → duraklat düğmesi gerekmez.

**Performans hedefi:** mobil LCP ≤ 2,5 s (LCP elemanı kapak karesi veya h1), CLS ≤ 0,02, Faz B'de uzun görev yok (kare çizimi tek `drawImage`).

### 2.6 Görsel kaynak kuralları (K9 — kapalı liste)

1. **Kendi çekimimiz** birincil kaynak; telif "Alegre Group"; künye `plan/tasarim/gorsel-kaynak.md`.
2. **Unsplash** yalnız köprü: lisans ticari kullanıma açık ve atıf zorunlu değil — **fakat API kullanılmaz** (API Şartları atıf + indirme takibi zorunluluğu getirir; elle indirme bu yükü doğurmaz).
3. **Tanınabilir yüz olan kare kullanılmaz** (model izni lisansta doğrulanmaz). **Marka/logo/tabela görünen kare kullanılmaz** (marka hakları lisansa dâhil değil).
4. **Unsplash karesi asla belirli bir yerin fotoğrafı gibi sunulmaz.** Sekans atmosferdir; yer kartı ve yer detay fotoğrafı **yalnız kendi çekimimizdir** (K2 kırmızı çizgisi (c) + yanıltmama ilkesi).
5. Yasak: scraping fotoğrafı, hotlink, stok video, AI ile üretilmiş fotoğraf, mp4/webm/gif hero.
6. Her kare için künye kaydı zorunlu: dosya adı, fotoğraf kimliği/URL, fotoğrafçı, indirme tarihi, lisans metni sürümü. (Unsplash'ın tazminat/garanti taahhüdü yok — provenans arşivi bizim savunmamız.)
7. Fotoğrafı olmayan yer: **degrade + kategori işareti** fallback; asla boş kutu, asla alakasız stok fotoğraf.

---

## 3. Bileşen envanteri (davranış tanımı — kod yok)

Ortak sözleşme: her bileşen (a) `kagit` ve `bordo` zeminde çalışır, (b) veri eksikken **bozulmaz**, (c) klavyeyle erişilebilir + görünür odak halkası taşır, (d) tıklanabilir alanı ≥ 44×44 px, (e) hareketi `prefers-reduced-motion`'da kapanır, (f) uzun metni `line-clamp`/`truncate` ile keser (esnek çocuklarda `min-w-0`).

### 3.1 Üst bant (`SiteHeader`)
- **Amaç:** her sayfada marka + ana gezinme + birincil CTA.
- **Anatomi:** sol marka kilidi · orta gezinme · sağ "Rotanı kur" (birincil, mobilde ikon+etiket) · mobilde sheet menü.
- **Davranış:** sticky. Sayfa başındayken **saydam ve çizgisiz** (hero'ya karışır); 64 px kaydırmadan sonra zemin `kagit` %92 + alt hairline belirir (geçiş 280 ms). Aşağı kaydırırken **gizlenmez** (gezi sitesinde kaybolan navbar yönelim kaybettirir).
- **Kurallar:** yükseklik 64 px (mobil 56) **sabit** — kaydırmada küçülmez (yerleşim zıplaması olmaz). Aktif bağlantı: bordo etiket + altında **tek nokta** (§5.1). Bölüm çapaları için `scroll-margin-top: 4,5rem`. Var olmayan sayfaya **ölü link yasağı** — bağlantı sayfa yayına girince eklenir (§6.3 eşikleri). Odak halkası sticky bandın altında kalmaz.

### 3.2 Alt bant (`SiteFooter`)
- **Anatomi:** 4 kolon — (1) marka kilidi + slogan + GEO tanım cümlesi, (2) sayfalar, (3) yasal, (4) güven satırı + OSM atfı.
- **Kurallar:** zemin `bordo` (12,8:1 beyaz metin), doku %6. **`Harita verisi © OpenStreetMap katkıda bulunanlar` satırı kaldırılamaz** (ODbL). Güven cümlesi: "Önerilerimizin nedenini gösteririz: her skorun kırılımı açık." Kaynak adı (Google/Ekşi/TripAdvisor) **geçmez** (K2). Yalnız yayında olan sayfalara link.

### 3.3 Medya plakası (`Plaka` — yeni, kart ailesinin temeli)
- **Amaç:** fotoğraflı ve fotoğrafsız durumu **tek** bileşende birleştirmek; sitenin en kritik büyüme sözleşmesi (bugün 0 fotoğraf, yarın 1.719).
- **Anatomi:** sabit oranlı kutu (16:10 kart, 4:3 hero, 4:5 mobil hero) · fotoğraf **veya** tipografik dolgu · alt scrim · sol alt etiket yuvası · sağ üst rozet yuvası.
- **Tipografik dolgu (fotoğrafsız):** `kagit-koyu` zemin + kategori işareti (hairline, 24 px) + ince ızgara dokusu; **degrade klişesi yok**. Fotoğrafsız kart "eksik" değil "sade" görünür.
- **Kurallar:** oran her iki durumda **aynı** → fotoğraf gelince ızgara adımı değişmez (CLS 0). `width`/`height` her zaman verilir; kart üstü fotoğraflar `loading="lazy"`, hero kapağı `priority`. Fotoğraf üstü metin varsa scrim zorunlu.

### 3.4 Kart ailesi
| Kart | Anatomi | Zorunlu | Notlar |
|---|---|---|---|
| **Yer kartı** (`YerKarti`) | Plaka · başlık (2 satır maks) · ilçe · özet 2 satır · rozet katı · skor | rozet katı **yer ayırır** (boşsa görünmez, yükseklik sabit) | Tıklama alanı tüm kart, ama `a` başlıkta (Cmd+tık çalışır). Skor `tabular` |
| **Şehir kartı** (`SehirKarti`) | Plaka (geniş) · şehir adı Fraunces · "N yer · M ilçe" · kısa tanıtım | sayı satırı gerçek veriden | 3 varyant: **vitrin** (tek şehir, tam genişlik), **ızgara** (2–3), **şerit** (4+) — §6.2 |
| **Bölge kartı** (yeni) | ilçe adı · duygu özeti ilk cümlesi · yer sayısı · "bölgeyi tanı" | — | Bölgeler sayfası + yer detayında "aynı ilçede" |
| **Rehber kartı** (`RehberKarti`) | Plaka · üst etiket (konu) · başlık · okuma süresi · tarih | tarih `Intl` ile | 0 yazı varken bölüm hiç render edilmez |
| **Rota kartı** (yeni) | gün sayısı · duraklar zinciri (mini) · baskın eksen · "rotayı gör" | — | Kayıtlı/sabit rotalar için; 0 kayıt varken bölüm gizli |

**Kart hover:** yükselme **yok**, gölge **yok** → hairline `bordo` %12 → %40 + alt kenarda 1 px `samandira` çizgisi ("su hattı", §5.10) + başlık altı çizgisi. Süre 180 ms. Basılı halde 1 px içe iner (yalnız `transform`, yerleşim kaymaz).

### 3.5 CTA ailesi (`Dugme`)
| Varyant | Görünüm | Kullanım |
|---|---|---|
| Birincil | `samandira` zemin, beyaz ≥600 ağırlık, 8 px köşe, ışık ≤ %35 | sayfada **en fazla 1** (hero + doruk CTA aynı sayfada ikisi de birincil olabilir, arada değil) |
| İkincil | Şeffaf zemin, 1 px `bordo` çerçeve, bordo metin | hero'nun ikinci eylemi, bölüm CTA'sı |
| Hayalet | Çerçevesiz, bordo metin + hover'da `kagit-koyu` zemin | kart içi, tablo içi |
| Metin bağlantısı | Bordo metin + 1 px `deniz` altı çizgi (hover'da kalınlaşır) | gövde metni içinde |
| **Bölüm sonu mini CTA** | Hayalet + sağ ok, etiket katı tipografi | her bölümün sonunda (dönüşümü sayfa sonuna bırakmamak) |

**Kurallar:** metin **belirgin** olur ("Rotanı kur", "Bölgeyi tanı"), "Devam"/"Tıkla" yasak. Emir kipi + nazik ton (04 §6). Yükleme durumunda buton **etkin kalır** istek başlayana kadar, sonra spinner + `…`. İkon-only buton `aria-label` şart. `cursor: pointer` her tıklanabilirde.

### 3.6 Rozetler (`Rozet`)
| Rozet | Renk | Kural |
|---|---|---|
| **Sponsorlu** | `signal` zemin, koyu metin | **her görünümde zorunlu** (etik + yasal şeffaflık) |
| Şehrin Klasiği | `deniz` hairline + deniz metin | veri boşsa görünmez ama yer ayrılır |
| Kategori | `kagit-koyu` zemin, ink metin | taksonomiden; renk kodlaması **tek başına anlam taşımaz** (metin şart) |
| Skor | hairline çerçeve + tabular sayı | tıklanınca kırılıma götürür (kara kutu yok) |
| Durum ("Yeni", "Hazırlanıyor") | hairline, ince | içerik büyümesinde kullanılır |

Rozet katı **tek satır**, taşarsa `nowrap` + fazlası "+2" olarak toplanır (sarma yasağı — kart yüksekliği sabit).

### 3.7 Bölüm başlığı (`BolumBasligi`)
- **Anatomi:** kenar notunda etiket (11 px/0,24em) · `h2` Fraunces · tek satır açıklama (isteğe bağlı) · sağda hayalet aksiyon ("tümünü gör").
- **Kurallar:** başlık **kullanıcı sorusundan** türer ("Nereye gidilir?", "Hangi bölge sana göre?"), denizcilik metaforundan değil (K8: ağır tema yasak). Başlık hiyerarşisi atlamaz; her `h2` çapa alır (`scroll-margin-top`).

### 3.8 İstatistik bandı (`IstatistikBandi`)
- **Gerçek veri (2026-09-05 ölçüldü):** 1.719 yer · 15 ilçe (18 bölge profili) · 6 deneyim ekseni · 1 şehir.
- **Kurallar:** **yorum sayısı asla gösterilmez** (K2 kaynak ifşası). Sayılar API'den gelir, elle yazılmaz. **En az 3 gerçek metrik** yoksa bant render edilmez. Sayaç animasyonu: tek sefer, 900 ms, `tabular-nums`, indirgenmiş harekette **son değer** doğrudan. Sayı büyürken yerleşim kaymaz (sabit genişlik alanı). "1 şehir" utanılacak sayı değil — yanında "Samsun'da başladık" bağlamı verilir.

### 3.9 Veri blokları (`DuyguOzeti`, `SkorKirilim`)
- **Duygu özeti:** Fraunces italic alıntı açılışı + şablon anlatım (öznel); üstünde "ziyaretçi yorumlarından derlenmiştir" jenerik künyesi. **Ham yorum metni ve yorumcu adı yok**; `ornek_ifade` anonim ve ≤10 kelime. Tanıtım metni (nesnel) ile **tipografik olarak ayrı** görünür.
- **Skor kırılımı:** her bileşen için satır: etiket · çubuk · tabular değer. Çubuk 0'dan değere 550 ms; indirgenmiş harekette dolu başlar. Toplam skor tıklanabilir kırılımı açar. **Kara kutu yasağı**: kırılım her zaman erişilebilir.

### 3.10 Filtre çipi (`FiltreCip`)
- **Anatomi:** etiket + sayı (`Müze 42`). Seçili: `samandira` hairline + `samandira` %10 zemin + 4 px nokta; seçili olmayan: hairline `bordo` %12.
- **Kurallar:** durum **URL'e yazılır** (paylaşılabilir/derin bağlanabilir filtre). Sayı 0 olan çip **görünür ama devre dışı** (kullanıcı kapsamı anlar). Çip satırı yatay kaydırılabilir; kaydırma göstergesi kenarda soluklaşan maske. Klavye: sekme + ok tuşları.

### 3.11 Boş durumlar (`BosDurum` — 5 tip)
| Tip | Metin (04 §6 tonu) | Eylem |
|---|---|---|
| Filtre sonucu boş | "Bu filtreyle kıyıda köşede bir şey kalmadı. Filtreleri gevşetip tekrar bakalım mı?" | "Filtreleri temizle" |
| Veri henüz yok (yeni şehir/modül) | "Burayı henüz işaretlemedik." | "Şimdilik Samsun'a bak" |
| Hata | "Pusula şaştı — sayfayı yenileyip tekrar dener misin?" | "Yenile" |
| 404 | "Sayfa bulunamadı — pusula şaştı" | "Ana sayfa" + "Keşfe başla" |
| Kapsam dışı / hazırlanıyor | "Bu bölüm hazırlanıyor." | ilgili yayında olan sayfaya yönlendirme |
**Kurallar:** illüstrasyon yok — **tek hairline ufuk çizgisi + tek nokta** (§5.6). Emoji yok. Her boş durum **en az bir çıkış yolu** verir. Hata metni ne yapılacağını söyler.

### 3.12 İskelet yükleyiciler (yeni)
| İskelet | Nerede |
|---|---|
| Kart iskeleti | keşif ızgarası, şehir/rehber/rota şeritleri |
| Liste iskeleti | bölgeler listesi, "yakındaki yerler" |
| Metin iskeleti | tanıtım/duygu özeti blokları (3 satır, son satır %60) |
| Plaka iskeleti | hero ve yer detay kapağı |
**Kurallar:** iskelet **gerçek yerleşimin ölçüsünü birebir** taşır (aynı yükseklik, aynı ızgara adımı) → içerik gelince sıçrama olmaz, CLS 0. Parlama (shimmer) **aşağıdan yukarı** akar (§5.8), 1,4 s döngü; indirgenmiş harekette **sabit** düz ton (döngü yok). Yükleme metni `…` ile biter. 300 ms'den kısa yüklemede iskelet gösterilmez (yanıp sönme).

---

## 4. Hareket dili

### 4.1 Zamanlama tokenları ve temel kural

| Token | Değer | Kullanım |
|---|---|---|
| `--sure-hizli` | 180 ms | hover, odak, çip, buton |
| `--sure-orta` | 280 ms | üst bant zemini, açılır katman, sekme |
| `--sure-yavas` | 550 ms | bölüm reveal, skor çubuğu |
| `--sure-sahne` (yeni) | 900 ms | hero Faz A, sayaç |
| `--ease-cikis` | `cubic-bezier(0.22, 1, 0.36, 1)` | giriş/ortaya çıkış (mevcut) |
| `--ease-giris` (yeni) | `cubic-bezier(0.4, 0, 0.2, 1)` | durum değişimi, kapanış |

**Temel kural:** giriş hareketi **mesafe ≤ 24 px** + opaklık 0→1; yalnız `transform`/`opacity`; `transition: all` yasak; her giriş **tek sefer** (`once`); çıkış girişten hızlı; animasyon kullanıcı girdisiyle kesilebilir.

### 4.2 Sayfa başına kaydırma koreografisi

| Sayfa | Bölüm sırası ve hareket |
|---|---|
| **Ana sayfa** | (1) **Kapak** — sekans Faz A (yükte) → Faz B (kaydırmada), metin sabit · (2) **Kanıt** — istatistik bandı, sayaç tek sefer · (3) **"Ne yapar?"** üç kart — kademeli 60 ms · (4) **Şehir vitrini** — plaka + kenar notu, plakada paralaks 6% · (5) **Rota şeridi** — kullanıcı kontrollü yatay şerit · (6) **Doruk CTA** — bordo blok, 550 ms reveal. Bölüm 3 ve 4 sonunda mini CTA. |
| **Keşif listesi** (`/sehir/…`) | Kısa hero bandı (30vh, statik) → sticky filtre çipleri (ikinci sıra, üst bandın altına yapışır) → kart ızgarası: **yalnız ilk ekrandaki kartlar** 40 ms kademeyle girer, altı anında (uzun listede kademe rahatsız eder) · `content-visibility: auto` |
| **Yer detay** | Kapak plakası (paralaks yok) → başlık bloğu → tanıtım (nesnel) → duygu özeti (alıntı açılışı, 550 ms) → skor kırılımı (çubuklar 550 ms, tek sefer) → yakındaki yerler (kademeli) |
| **Bölgeler** | Liste; her satır hover'da kenar notu belirir (180 ms). Girişte kademe 40 ms, ilk 8 satır |
| **Rota sihirbazı** | Adım geçişleri 180 ms (opaklık + 8 px), **yön duyarlı** (ileri/geri). Sonuç: gün gün zaman çizelgesi 80 ms kademeyle. Slider'lar anında (hiç gecikme yok) |
| **Rehber yazısı** | Üstte 2 px okuma ilerleme hattı (§5.2); başlıklarda `scroll-margin`; görsel plakaları girişte 550 ms |
| **Yasal/kurumsal** | Hareket yok. Yalnız bağlantı hover'ları |

Bölüm adları **kullanıcı sorusudur** ("Nereye gidilir?"), denizcilik metaforu değil — `arastirma.md` §8'in *ufuk → sığlık → rota → demir* isimlendirmesi K8'in "ağır tema yasak" kuralıyla düşer.

### 4.3 Mikro etkileşimler

| Öğe | Tetik | Değişim | Süre | İndirgenmişte |
|---|---|---|---|---|
| Kart | hover/focus | hairline koyulaşır + alt 1 px `samandira` çizgi + başlık altı çizgisi | 180 ms | yalnız renk değişimi (anında) |
| Birincil CTA | hover | zemin `samandira-koyu` + ışık %35 | 180 ms | renk değişimi |
| Aktif gezinme | sayfa değişimi | nokta bir kez nabız atar (§5.1) | 400 ms, tekrarsız | nokta sabit |
| Filtre çipi | seçim | zemin + nokta belirir, sayı güncellenir | 180 ms | anında |
| Skor çubuğu | görünür olma | 0 → değer | 550 ms | dolu başlar |
| Sayaç | görünür olma | son basamaktan yukarı sayar (§5.12) | 900 ms | son değer |
| Kopyala/paylaş | tıklama | buton etiketi "Kopyalandı" + `aria-live="polite"` | 1,6 s sonra geri | aynı (metin değişimi harekete bağlı değil) |
| Form odağı | focus-visible | 2 px `samandira` odak halkası, offset 2 px | anında | aynı |

### 4.4 Paralaks ve marquee kararları

- **Paralaks: kısıtlı ve dekoratif.** Yalnız (a) hero plakası ve (b) şehir vitrini plakası; `yPercent` **6** (bant 5–15'in alt ucu). **Metin, buton, kart ve kontrollere paralaks yasak.** 768 px altında paralaks tamamen kapalı. Aktif değilken `will-change` kaldırılır.
- **Marquee: RED.** Sonsuz kayan şerit, 5 saniyeden uzun otomatik harekettir; duraklat/durdur/gizle kontrolü gerektirir ve bu kontrol her zaman görsel kirlilik yaratır. Yerine: **kullanıcı kontrollü yatay şerit** — sürükleme + ok tuşları + `scroll-snap`, kenarlarda soluklaşan maske, "N/M" sayacı. Mevcut `.serit-kaydir`, `.dalga`, `.sonar-halka`, `.samandira-suz` sınıfları kaldırılır.
- **Kaydırma ele geçirme (scroll-jacking) yasak:** hero dâhil hiçbir bölüm kaydırmayı pinleyip kullanıcıyı hapsetmez. Faz B, hero doğal olarak ekrandan çıkarken çalışır — 900 px, yani bir ekran boyundan az.

### 4.5 İndirgenmiş hareket sözleşmesi

| Normal | `prefers-reduced-motion: reduce` |
|---|---|
| Hero Faz A + Faz B | **Statik kapak**; kare indirilmez |
| Bölüm reveal (opaklık + 24 px) | İçerik **son okunabilir halinde** (opaklık 1, kayma 0) |
| Kademeli kart girişi | Hepsi anında |
| Paralaks | 0 |
| Sayaç / skor çubuğu | Son değer / dolu |
| İskelet parlaması | Sabit düz ton |
| Yatay şerit `scroll-behavior: smooth` | `auto` |
| Hover geçişleri | Renk değişimi kalır (geçiş süresi 0) |

**Zorunlu teknik kural (Faz 1'de bulunan hidrasyon hatası tekrarlamasın):** tercih **doğrudan** render dallanmasında okunmaz. Sunucu tercihi bilemez; ilk render herkeste hareketli varyant, tercih effect içinde bağlanır (hidrasyona güvenli tek hook). Ayrıca: ekran dışında/gizli sekmede animasyon durur; sayfa geçişinde 300 ms üstü animasyon yok.

**Performans sözleşmesi:** yalnız `transform`/`opacity`; `will-change` yalnız aktif katmanda; ağır sahneler `next/dynamic`; SVG animasyonu sarmalayıcı `div` üzerinden (donanım hızlandırma); uzun listelerde `content-visibility: auto`; render içinde yerleşim okuması (`getBoundingClientRect` vb.) yasak.

---

## 5. Şamandıra göndermeleri — yalnız "ufak trikler" (kapalı liste)

**Kural (K8):** Site şamandıra konseptini birebir yansıtmaz. Aşağıdaki 11 madde **listenin tamamıdır**; yenisi eklenmeden önce kullanıcı onayı gerekir. Her trik tek bir detayda yaşar, adı sayfada geçmez, fark edilmesi zorunlu değildir.

1. **Aktif gezinme noktası** — aktif bağlantının altında çizgi değil **tek 4 px nokta** (`samandira`); sayfa değişiminde bir kez nabız atar (400 ms), sonra durur.
2. **Seyir hattı** — sağ kenarda 2 px'lik kaydırma ilerleme hattı; ucunda 4 px bordo nokta. Uzun sayfalarda (rehber, yer detay) görünür.
3. **Kesilen ayraç** — bölüm ayracı tek hairline, tam ortasında 6 px boşluk: logodaki "beyaz çizginin denizi kesmesi" hamlesinin sessiz karşılığı. Dalga **yok**.
4. **Kırılım halkası** — skor kırılımında **yalnız en yüksek** bileşenin çubuğunun ucunda 6 px halka.
5. **Batmış seçim** — `::selection` bordo zemin + kağıt metin ("suya batmış" hissi). (Mevcut kırmızı seçim rengi bordoya çevrilir.)
6. **Boş durum ufku** — illüstrasyon yerine tek hairline yatay çizgi + üstünde tek nokta.
7. **Markır** — harita/kart işareti jenerik damla pin değil, logodan alınmış **halka + nokta**.
8. **Yükselen su** — iskelet parlaması soldan sağa değil **aşağıdan yukarı** akar.
9. **Fener parlaması** — birincil CTA hover'ında ≤ 24 px yarıçaplı, ≤ %35 opaklıkta sıcak parlama; sürekli değil, yalnız hover.
10. **Su hattı** — kart hover'ında gölge değil, alt kenarda 1 px `samandira` çizgi.
11. **Tek tam tema noktası** — bordo karo yalnız marka karosunda tam güçle görünür (favicon, app ikonu, OG); sayfa içinde bordo **mürekkeptir**, dekor değil.

**Yasak (ağır tema):** her bölümde dalga bandı veya animasyonlu su · çıpa / pusula gülü / dümen / can simidi / gemi direği ikonografisi · halat-düğüm dokusu · denizci (breton) çizgi deseni · "ahoy / kaptan / demir at / rota çiz" tipi dil süsü · sonar halkası animasyonu · süzülen/sallanan şamandıra · deniz mavisi baskın zemin · uçak/valiz/pasaport/harita-pini klişeleri.

---

## 6. İçerik büyüme öngörüsü ve yerleşim sözleşmesi

### 6.1 Bugünkü gerçek (2026-09-05, veritabanından ölçüldü)

| Varlık | Bugün | Yakın hedef |
|---|---|---|
| Şehir | **1** (Samsun) | 2–3 (B-04) |
| Yer kaydı | **1.719** (vitrin ilk 60'ı gösteriyor) | aynı + kürasyon eşiği (T-08) |
| İlçe | **15** ayrı ilçe · **18** bölge profili | aynı |
| Tanıtım metni | 1.719/1.719 dolu | aynı |
| **Fotoğraf** | **0** | 30 yer (manuel çekim #7) |
| Rehber yazısı | 0 | 3+ (T-15) |
| Slug | **yok** (URL'ler UUID) | `yerler.slug` (T-05) |
| Yorum | 19.609 (**sitede asla gösterilmez** — K2) | — |

Tasarım bu tabloya göre kurulur: **site boş değil, fotoğrafsız.** Yön (§1) tam bu yüzden tipografi-öncelikli.

### 6.2 Yerleşim sözleşmesi (bozulmama garantileri)

| Bölüm | 0 / az içerik | Çok içerik | Garanti |
|---|---|---|---|
| Şehir vitrini | 1 şehir → **vitrin** varyantı (tam genişlik plaka + tanıtım) | 2–3 → ızgara · 4+ → kullanıcı kontrollü şerit + "tümü" | Varyant değişir, **bölüm yeniden tasarlanmaz** |
| Keşif ızgarası | 60 kayıt | 1.719 kayıt → "daha fazla yükle" + `content-visibility` | Izgara adımı ve kart yüksekliği sabit |
| Yer kartı | fotoğrafsız (tipografik plaka) | fotoğraflı | **Aynı oran, aynı yükseklik** → CLS 0, karışık liste bozulmaz |
| Rozet katı | veri boş → görünmez | 3+ rozet → `nowrap` + "+2" | Satır yüksekliği **her durumda ayrılmış** |
| Rehber bölümü | 0 yazı → bölüm **render edilmez**, navbar linki yok | 1–2 → gizli · 3+ → 3'lük şerit | Ölü link asla |
| Rota bölümü | 0 kayıtlı rota → bölüm gizli, CTA sihirbaza gider | N → rota kartları | — |
| İstatistik bandı | <3 gerçek metrik → bant yok | sayılar büyür | `tabular-nums` + sabit genişlik → yerleşim kaymaz |
| İlçe/rehber metni | 40 kelime | 1.200 kelime | Üç uzunlukta (kısa/orta/uzun) test edilir |
| Bağlantı üretimi | UUID | slug (T-05) | Kart bağlantısı **tek yerden** üretilir; geçişte yerleşim değişmez |
| Yer detay yan bilgi | profil zayıf → alan gizlenir | dolu profil | "Bilinmiyor" yazan boş satır yok; alan tümüyle gizlenir |

### 6.3 Görünürlük eşikleri (ölü link ve boş bölüm yasağı)

| Sayfa/bölüm | Görünme eşiği |
|---|---|
| Navbar "Şehirler" | ≥ 2 yayında şehir (1 şehirde doğrudan `/sehir/samsun`) |
| Navbar "Rehber" | ≥ 1 yayında yazı |
| Ana sayfa rehber şeridi | ≥ 3 yazı |
| Ana sayfa rota şeridi | ≥ 3 sabit/kayıtlı rota |
| Yer detay "yakındaki yerler" | ≥ 3 sonuç |
| Yer detay galerisi | ≥ 1 **kendi** fotoğrafımız |
| İstatistik bandı | ≥ 3 gerçek metrik |
| `/sponsorluk` | büyüme kararı değişene kadar `noindex`, görünür link yok |

### 6.4 Boş sayfa iskeletleri ("ilk gün" görünümü)

Her yeni sayfa türü, veri gelmeden önce de **tamamlanmış** görünmek zorundadır: hero + tek anlamlı bölüm + çıkış yolu. Beyaz boşluk bırakılmaz.

| Rota | İlk gün görünümü |
|---|---|
| `/rehber` (0 yazı) | Sayfa **yayına alınmaz**; hazır olunca açılır (navbar linki eşikle gelir) |
| `/sehir/{yeni-sehir}` (veri yok) | Hero (şehir adı + "hazırlanıyor" rozeti) + "Şimdilik Samsun'a bak" kartı + rota sihirbazı CTA'sı |
| `/yer/{slug}` (profil zayıf) | Plaka (tipografik) + tanıtım + "bu yer için henüz yeterli izlenim yok" satırı + yakındaki yerler + ilçe kartı |
| `/rota/{id}` (bulunamadı/süresi geçmiş) | 404 tonunda boş durum + "Yeni rota kur" birincil CTA |
| Keşif (filtre sonucu 0) | Filtre boş durumu + seçili filtrelerin listesi + "Filtreleri temizle" |
| `/bolgeler` (profil yok) | İlçe listesi (yalnız ad + yer sayısı) + "bölge profilleri hazırlanıyor" satırı |
| `/hakkimizda`, `/gizlilik`, `/kullanim-kosullari`, `/iletisim` | İçerik-önce, hareketsiz; hero yerine kenar notlu başlık bloğu |

---

## 7. Kaynak taraması (bu tur)

| # | Kaynak | URL | Bu turda çıkarılan |
|---|---|---|---|
| 1 | Awwwards — Travel | https://www.awwwards.com/websites/travel/ | 18 aday; yeni isimler: Vita Travels (Phenomenon Studio), Lithuania Travel, Artemii Lebedev (SOTD/DEV), Vovi, Zeitler, McArnolds. Zemin `#F8F8F8` — galeri bile saf beyaz kullanmıyor. Kart anatomisi: görsel + üretici + köşe rozeti (`HM`/`SOTD`) |
| 2 | Design Prompts | https://designprompts.dev/ | 30 stil taksonomisi. **Bizim mahalle:** Monochrome/Newsprint/Academia/Bold Typography ("stark, editorial, oversized serif"). **Kaçınılacak mahalle:** SaaS, Professional, Enterprise, Material, Flat, Neumorphism, Claymorphism. Filtre dili `MODE / TYPE` |
| 3 | Lapa Ninja — Motion | https://www.lapa.ninja/motion/ | 1.005 hareketli site ayrı tür olarak kürate ediliyor. Etiket dağılımı: Creative 5.003, Minimal 3.051, **Photography 510**, Typography 712 — **"Travel" ilk 40 etikette yok** (niş = fırsat) |
| 4 | Lapa Ninja | https://www.lapa.ninja/ | 7.478 landing; kategori ağırlıkları yukarıdaki tabloda |
| 5 | 21st.dev | https://21st.dev/ | 12.000+ bileşen; hero **adlandırılmış bir ürün**: "Animated Hero", "Shimmer Button", **"Number Ticker"** (istatistik bandı sayacı standart bir bileşen). Kod kopyalanmaz (T-16 yasağı), yalnız bileşen dili not edildi |
| 6 | animations.dev | https://animations.dev/ | Hareket sözlüğü: *easing, timing, spring, purpose, taste, **orchestration**, accessibility, performance*. Kurs yapısı: 8 teori dersi + 4 yürüyüş (Family Drawer, Dynamic Island, Navigation Menu, SVG) → hareket "orkestrasyon" olarak öğretiliyor, efekt olarak değil |
| 7 | Godly | https://godly.website/ | Kategori dili: Web / Interface / Branding / Product / Typography / Motion / Illustration / 3D / **Editorial** / Print / Packaging. Vitrin başlıkları hero'yu tek başına iş olarak anıyor ("Ice Fracture Hero", "N233 Agency Hero") |
| 8 | Typewolf — Site of the Day | https://www.typewolf.com/site-of-the-day | Son 9 SOTD font çifti: Grenette+Styrene, Cardinal+Sweet Sans+Baskerville, Swear+**DM Mono**, DaVinci+Suisse, Editorial Old+Neue Montreal, Tobias+**Diatype Mono** → formül: **display serif + nötr grotesk (+ mono etiket katı)**. Fraunces+Sora doğrulandı; mono kat yedek yöne alındı |
| 9 | Figma Community — Travel | https://www.figma.com/community/website-templates/travel-booking | Kategorinin adı **"Travel *Booking*"**; şablon adları jenerik ("Travel Website Landing Page", "Botique Travel Website Wireframes"). Kaçınma listesinin kaynağı: hero arama kutusu, "Book now", avatar karuseli |
| 10 | Mobbin | https://mobbin.com/browse/web/apps | (önceki tur) İstatistik bandı sosyal kanıt yerine geçiyor: "1.428 apps / 621.500+ screens" |
| 11 | Behance — travel brand identity | https://www.behance.net/search/projects/travel%20brand%20identity | (önceki tur) Seyahat kimliği klişeleri → benzemezlik filtresi |
| 12 | Codrops — OPTIKKA kare sekansı | https://tympanus.net/codrops/2025/10/16/creating-smooth-scroll-synchronized-animation-for-optikka-from-html5-video-to-frame-sequences/ | Video → kare sekansı geçişinin gerekçesi; ilk 10 kare hemen, kalanı arka planda; kaydırma yönüne göre ±5 kare ön yükleme; masaüstü/mobil ayrı kare sayısı |
| 13 | scroll-frame-sequence (teknik referans) | https://github.com/tangyistudio/scroll-frame-sequence | **Kare/piksel bandı: 15–20 px/kare** (Apple AirPods ≈ 18,5); 10 px altı görünmez kareye ödeme, 30 px üstü basamaklı; mobil 48 kare alt örnekleme; ikili altbölme yükleme; `maxConcurrent 6` |
| 14 | Scroll-Stop Playbook 2026 | https://causeandeffectsp.com/blog/scroll-stop-animations-2026-playbook/ | 30–60 kare akıcı hissediyor; WebP %75–85; **toplam < 1 MB**; ilk 8–12 kare eager; en sık hata 4–8 MB'lık kare seti (LCP katliamı) |
| 15 | Scroll-driven media desenleri | https://www.css-scroll-driven.com/scroll-driven-view-transition-implementation-patterns/scroll-driven-media-and-gallery-effects/ | Kutuyu önceden ayır (`aspect-ratio`) — en yüksek değerli tek düzeltme; pinlenmiş yığınlar en pahalı desen, landing'de yeri var, doküman sayfasında yok |
| 16 | Unsplash Lisansı + API Şartları | https://help.unsplash.com/en/articles/2612332-what-do-you-mean-by-compiling-images-to-replicate-a-similar-or-competing-service | Ticari kullanım serbest, atıf zorunlu değil; **API kullanımında atıf + indirme takibi zorunlu**; rakip servis derlemek yasak; marka hakkı ve model izni **dâhil değil**; tazminat yok → K9 kuralları (§2.6) |
| 17 | Vercel Web Interface Guidelines | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | Denetim listesi (bu turda çekilen sürüm): odak halkası, `transition: all` yasağı, görsel boyutları, `aria-live`, `Intl.*`, tabular sayılar, `text-wrap: balance`, `overscroll-behavior`, hidrasyon güvenliği |
| 18 | `ui-ux-pro-max` (yerel skill) | — | `--variance 8 --motion 8 --density 4`: desen **Scroll-Triggered Storytelling** (kabul), stil Brutalism (kısmi kabul: keskin köşe + görünür ızgara **yedek yönde**), palet `#EA580C`+`#0891B2` (**red** — marka kilidi), tipografi Playfair+Inter (**red** — Fraunces+Sora eşdeğeri), hareket kademesi Complex→**Standard'a indirildi** (Lighthouse bütçesi) |

**Benzemezlik kuralı (uygulandı):** ilham yalnız **desen düzeyinde** (ölçek, ritim, katman, zamanlama, yükleme stratejisi) alındı; hiçbir görsel, kod veya kompozisyon kopyalanmadı.

---

## 8. Doğrulama kapıları (uygulama bunları kanıtlamadan kapanmaz)

1. **Tarayıcı akışı** (tek ekran görüntüsü kanıt değil): 375 px + 1280 px'te ana sayfa → keşif → yer detay → bölgeler → rota sihirbazı (senaryo 2, uçtan uca) turu.
2. **Sekans bütçesi:** ağ sekmesinde sekans toplam bayt ≤ 900 KB (masaüstü) / ≤ 380 KB (mobil); kapak karesi LCP elemanı.
3. **Lighthouse mobil:** Perf ≥ 80, SEO ≥ 95, A11y ≥ 90, BP ≥ 90. **CLS ≤ 0,02**.
4. **CLS ikili test:** keşif ızgarası **tamamı fotoğrafsız** ve **yarısı fotoğraflı** iki durumda ölçülür; ızgara adımı değişmemeli.
5. **İndirgenmiş hareket:** `reducedMotion: reduce` ile yükleme → 0 hidrasyon uyuşmazlığı, 0 konsol hatası, hiçbir sekans karesi indirilmemiş, tüm içerik son okunabilir halinde.
6. **Kontrast:** §1.2 tablosundaki 6 çift ölçülür; `samandira` metin olarak hiçbir yerde geçmiyor.
7. **Erişilebilirlik:** sayfa başına tek `h1`, başlık sıralamasında atlama yok, dekoratif SVG'lerde `role="img"` sayısı 0, tıklama hedefleri ≥ 44 px, sticky bant odaklanan öğeyi kapatmıyor.
8. **Ölü link taraması:** navbar + footer + kart bağlantılarının tamamı 200 dönüyor.
9. **Marka:** hiçbir yüzeyde "Rotam" yok; Ufuk varlıkları kaldırılmış; logo `plan/logo/secili/logo.png` türevi.
10. **K2:** yorum sayısı hiçbir yerde görünmüyor, ham yorum/yorumcu adı render edilmiyor, OSM atfı footer'da.

### Uygulama paketleri (Grok 4.6 extra high)

| Paket | İçerik | Ön koşul | Durum |
|---|---|---|---|
| **P1 — Marka varlıkları** | K8 PNG'den üretim seti (vektörleştirme **yok**): favicon/ico/apple-touch/PWA/maskable/OG + şeffaf/açık karo; Ufuk varlık/bileşen yok; header kilidi | — | **kapandı** |
| **P2 — Tokenlar** | §1.2 palet, §1.3 tipografi ölçeği, §1.4 boşluk, §1.6 köşe, §4.1 zamanlama tokenları; eski dalga/sonar/marquee CSS'inin kaldırılması | P1 | açık |
| **P3 — Bileşen kütüphanesi** | §3'ün tamamı + `/tasarim-sistemi` vitrininin yeni sözleşmeye göre güncellenmesi | P2 | açık |
| **P4 — Hero** | §2 (Yol B ile başlar: 7–9 Unsplash plakası + künye dosyası); fallback zinciri ve bütçe kanıtı | P3 | açık |
| **P5 — Sayfa makyajı** | §4.2 koreografi haritası, §6 yerleşim sözleşmesi ve eşikleri | P4 | açık |
| **P6 — Doğrulama** | §8'in 10 kapısı + rapor | P5 | açık |
