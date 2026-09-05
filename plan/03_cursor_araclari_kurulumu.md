# Cursor Araçları & Skill'leri — Kurulum Rehberi (Şamandıra)
**Tarih:** 2026-09-05 · Amaç: Cursor ajanını bu projede **güvenilir, hızlı ve proje kurallarına sadık** çalıştıracak donanımı kurmak.

> 2026 Cursor ekosisteminde 5 katman var: (1) `AGENTS.md` — repo bağlamı, (2) `.cursor/rules/*.mdc` — her zaman/koşullu uygulanan kurallar, (3) `.cursor/commands/` — tekrarlayan görev şablonları, (4) **MCP sunucuları** (`.cursor/mcp.json`) — dış araç erişimi, (5) **SKILL.md** becerileri — taşınabilir, gerektikçe yüklenen prosedürler. Aşağıdaki kurulum bu katmanları bilinçli kullanır: az ama isabetli.

---

## 0. Kurulum sırası (özet tablo)

| # | Araç/katman | Ne kazandırır | Maliyet |
|---|---|---|---|
| 1 | `.cursor/rules/` (4 dosya) | Ajan her görevde proje kurallarını bilir (Türkçe isimler, katman ayrımı, taksonomi-önce, commit yasağı) | 10 dk |
| 2 | `AGENTS.md` güncellemesi | Komutlar/portlar/marka gerçeği (README'lerin yanlışını burada düzeltiriz) | 10 dk |
| 3 | **Context7 MCP** | Next.js 16 / React 19 / Tailwind 4 için **güncel doküman** — ajanın eğitim verisi eski, `site/AGENTS.md` zaten uyarıyor; halüsinasyon ilacı | 5 dk |
| 4 | **Playwright MCP** | Ajan siteyi tarayıcıda **kendisi gezip doğrular** (brif'in "tek ekran görüntüsü yetmez" kuralı otomatikleşir) | 5 dk |
| 5 | **PostgreSQL MCP (read-only)** | Ajan gerçek veriye bakar (60 yer mi, foto var mı, slug boş mu) — uydurma varsayım biter | 10 dk |
| 5b | **Skills** (`.cursor/skills/`): ui-ux-pro-max, react-best-practices, seo-audit | Tasarım zekâsı + Vercel performans kuralları + teknik SEO denetimi; gerektikçe yüklenir (rules gibi sürekli context yemez) | 10 dk |
| 6 | shadcn/ui + lucide + motion | Profesyonel, erişilebilir, tutarlı UI bileşenleri (Tailwind v4 + React 19 uyumlu) — "güzel kurgulanmış site"nin bel kemiği | 20 dk |
| 7 | ESLint 9 + Prettier + TS strict + husky/lint-staged/commitlint | Ajanın ürettiği kod kalite kapısından geçer | 20 dk |
| 8 | Playwright (e2e test paketi) | Kritik akışlar (keşif→detay→rota) regresyonda kırılmaz | 30 dk |
| 9 | Lighthouse CI | Performans/SEO/a11y bütçesi PR'da ölçülür | 20 dk |
| 10 | `schema-dts` + `next/og` | Tip güvenli JSON-LD + dinamik OG görselleri (paylaşım kartları) | 10 dk |
| 11 | `.cursor/commands/` (3 komut) | "görev yaz", "SEO denetle", "sürüm öncesi kontrol" tek satırla | 10 dk |
| 12 | GitHub Projects + branch koruması | İki kişilik ekipte iş takibi + iki göz kuralı | 15 dk |

**Bilinçli olarak KURMUYORUZ:** Storybook (şimdilik overkill), Sentry (trafik yokken gereksiz; Faz 2'de değerlendir), v0.dev (mevcut tasarım dili oturmuş), 21st.dev Magic MCP (opsiyonel, şimdilik gerek yok), vercel/next-sitemap paketi (Next 16'da `app/sitemap.ts` native).

---

## 1. `.cursor/rules/` — proje kuralları (kopyala-yapıştır hazır)

Cursor 2026 formatı: `.cursor/rules/*.mdc`, YAML frontmatter ile ne zaman uygulanacağı kontrol edilir. Aşağıdaki 4 dosyayı **olduğu gibi** oluşturun (Cursor talimatı doküman #07 T-00'da hazır).

### `000-proje.mdc` (alwaysApply: true)
```markdown
---
description: Şamandıra proje anayasası — her görevde geçerli
alwaysApply: true
---
# Şamandıra (repo: gezi_bot → samandira) — Genel Kurallar
- Ürün markası **Şamandıra**; kullanıcıya görünen hiçbir metinde "Rotam" bırakma. Stüdyo: Alegre Group.
- Tüm kod tanımlayıcıları, yorumlar, commit mesajları ve dokümanlar **Türkçe ve Türkçe karaktersiz**: `isletme_verisi`, `duygu_skoru`, `rota_olustur`.
- Yeni özellik sırası: önce `dokumanlar/kategori_taksonomisi.md` (gerekirse `veri_sozlugu.md`) → sonra `ortak/sabitler.py` → sonra kod. Taksonomi ile kod asla sapmaz.
- Kara kutu yok: her skor/öneri `kirilim` ile açıklanabilir olmalı. Anlatım metinleri şablon + sabit tohum; LLM kullanma. (Tek istisna: genel duygu skoru — Türkçe BERT modeli.)
- Şehir bağımsızlık: şehir bilgisi yalnız `veri/ortak/sehir_ayarlari.py` (SEHIRLER). Toplayıcı/API/rota/site koduna şehir adı gömme.
- Katmanlar: `veri/` (scraping+analiz) → `sunucu/` (DB+API+rota) → `site/` (Next.js). `ortak/` yalnız taksonomi sabitleri. Katmanlar arası import yasağı: site → sunucu kodu import edemez (yalnız HTTP API).
- JSONB esnek alanlar (`ozellikler`, `aktiviteler`, `deneyim_puanlari`, `konu_duygulari`, `yer_profili`) dururken yeni kolon/migration AÇMA; yeni etiket = taksonomi + sabit.
- Kullanıcı açıkça istemeden `git commit` / `git push` YAPMA.
- README'ler `calis.txt` ile hizalıdır. Çelişkide `calis.txt`, `plan/00_brief_eki.md` ve `dokumanlar/` kazanır.
- Ortamlar: API port 8125, site 3000, PostgreSQL yerelde C:\PostgreSQL (Docker yok), venv: `.venv_test`.
```

### `100-site.mdc` (globs: site/**)
```markdown
---
description: Next.js 16 site kuralları
globs: site/**/*.ts,site/**/*.tsx
---
# Site Kuralları (Next.js 16 App Router, React 19, Tailwind 4)
- Bu Next.js sürümü eğitim verinden farklı olabilir; API/props emin olmadığında **Context7 MCP** ile güncel dokümana bak, uydurma.
- Varsayılan server component; yalnız gerekiyorsa "use client". Veri çekme `site/src/lib/api.ts` üzerinden; component içine ham fetch yazma.
- Tipler `site/src/lib/types.ts` — Python şemalarıyla (sunucu/api/semalar.py) hizalı tut; API şeması değişince burayı da güncelle.
- Her sayfa `generateMetadata` ile benzersiz title/description üretir (şablonlar doküman #02 §4). MetadataBase tanımlı.
- Yer linkleri slug ile: `/yer/{sehir}/{slug}` — UUID linki YASAK (301 hariç).
- Görseller `next/image` + anlamlı Türkçe `alt`; harici görsel domain'leri `next.config.ts` remotePatterns'a eklenir.
- UI bileşenleri shadcn/ui + Tailwind tema tokenları (deniz/kopuk/kumsal/gunes + samandira vurgu); inline hex renk yazma, tema tokenı ekle.
- Erişilebilirlik: semantik HTML, klavye navigasyonu, kontrast; form/slider'lar label'lı.
- Değişiklik sonrası Playwright MCP ile tarayıcıda akışı doğrula (3000 portu): ilgili sayfa + en az 1 bağlı akış. Tek ekran görüntüsü kanıt sayılmaz.
```

### `200-seo.mdc` (globs: site/src/app/**, site/src/components/seo/**)
```markdown
---
description: SEO kuralları — sayfa üreten her görevde
globs: site/src/app/**/*.tsx,site/src/components/seo/**
---
# SEO Kuralları
- Her indexlenebilir sayfada: benzersiz title/description, canonical, JSON-LD (doküman #02 §5 haritası), breadcrumb.
- JSON-LD: schema-dts tipleriyle; `AggregateRating` KOYMA (Google politika ihlali — skorlarımız türetilmiş metrik).
- Query parametreli filtre sayfaları canonical'ını statik yola verir; statik kategori yolları tercih edilir.
- Yeni sayfa = sitemap.ts'e kayıt + (gerekirse) 301 eşlemesi.
- Yer sayfaları index eşiği: ≥1 fotoğraf + yeterli metin; eşik altı sayfa `noindex,follow`.
- Rota sihirbazı akışı `noindex,follow`; paylaşılan rota `/rota/{id}` indexlenebilir + OG image.
- Görev bitiminde kontrol: JSON-LD validator + Lighthouse SEO ≥ 95.
```

### `300-sunucu.mdc` (globs: sunucu/**, veri/**, ortak/**)
```markdown
---
description: Python katmanı kuralları (veri + sunucu)
globs: sunucu/**/*.py,veri/**/*.py,ortak/**/*.py
---
# Sunucu/Veri Kuralları
- Dış API şemaları `sunucu/api/semalar.py`, saklama modelleri `sunucu/veritabani/modeller.py` — karıştırma; şema değişikliğinde `site/src/lib/types.ts` hizalanır.
- Migration: Alembic, sıralı numara (0005+), geri alınabilir; mevcut migration'ları ASLA düzenleme.
- Rota motoru deterministik kalır: aynı girdi → aynı çıktı; `kirilim` alanını doldurmadan skor döndürme. Testler: `pytest sunucu/rota_motoru/testler/ -v` her rota değişikliğinde koşar.
- Keşif vitrini filtresi `sunucu/veritabani/sorgular.py`'de: konaklama gizli, yeme-içme eşikli (klasik/sponsor/kahvaltı veya duygu≥80). Filtreyi gevşetme; kürasyon görevleri ayrı tartışılır.
- Scraping: engel tespitte nazikçe dur, kesinti dayanıklılık (kaldığı yerden devam) korunur; TripAdvisor/Booking varsayılan kapalı kalır.
- Aktarım idempotent kalır: `python -m sunucu.veritabani.aktarim.calistir --sehir samsun` tekrar çalıştırılabilir olmalı.
- Yeni ortak yardımcı (slug, transliterasyon) `ortak/`a gider; veri ve sunucu aynı fonksiyonu kullanır.
```

---

## 2. `AGENTS.md` (repo kökü) — güncelleme şartları

Mevcut `site/AGENTS.md` iyi bir uyarı içeriyor (Next sürümü eğitim verisinden farklı). Kök `AGENTS.md`'ye eklenecekler:
- **Marka:** ürün adı Şamandıra, stüdyo Alegre Group, canonical domain.
- **Komutlar:** (calis.txt'ten doğrulanmış hâliyle) API: `.venv_test` + uvicorn 8125; site: `npm run dev -- --port 3000`; testler: pytest rota motoru; aktarım komutu; alembic upgrade head.
- **Kritik uyarı:** README'ler bayat; `calis.txt` + `dokumanlar/` güncel.
- **Doğrulama politikası:** UI görevleri Playwright MCP ile tarayıcıda; API görevleri curl/Swagger ile; rota görevleri test + kirilim kontrolü ile.
- Commit/push yasağı (kullanıcı istemeden).

---

## 3. MCP sunucuları — `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres",
        "postgresql://gezi_kullanici:gezi_sifre@localhost:5432/gezi_veritabani"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

Notlar:
- **playwright**: ajanın tarayıcı açıp `/sehir/samsun` akışını gezmesi, form doldurması, konsol hatası yakalaması için. Brif'in doğrulama kuralını otomatikleştirir.
- **context7**: `next@16`, `react@19`, `tailwindcss@4`, `shadcn` sorgularında güncel resmî doküman parçaları getirir. Kural dosyalarında ajana "emin değilsen Context7'ye sor" diyoruz.
- **postgres**: ⚠️ bu sunucu **read-only** sorgu için; yine de üretim parolasını `.cursor/mcp.json`'a düz yazmayın — yerelde ayrı, **salt-okur** bir DB kullanıcısı açın:
  ```sql
  CREATE ROLE gezi_oku LOGIN PASSWORD '<ayri-parola>';
  GRANT CONNECT ON DATABASE gezi_veritabani TO gezi_oku;
  GRANT USAGE ON SCHEMA public TO gezi_oku;
  GRANT SELECT ON ALL TABLES IN SCHEMA public TO gezi_oku;
  ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO gezi_oku;
  ```
  ve connection string'de bu kullanıcıyı kullanın. `.cursor/mcp.json` git'e giriyorsa parola `${env:...}` interpolasyonu veya `.gitignore`'a alınmış `.cursor/mcp.local.json` kullanın.
- **fetch**: ajanın rakip SERP/schema validator gibi sayfaları okuması için (opsiyonel ama ucuz).
- Kurulum sonrası: Cursor → Settings → MCP → **Reload**; her sunucunun "yeşil" olduğunu doğrula. Windows'ta `npx` için Node 18+, `uvx` için `pip install uv` gerekir.

---

## 3b. Skills (SKILL.md) — gerektikçe yüklenen uzmanlıklar

Cursor (2.4+) Agent Skills'i destekler: `.cursor/skills/<ad>/SKILL.md` (proje — git'e girer, ekiple paylaşılır) veya `~/.cursor/skills/` (kişisel). Rules her zaman açıktır (context maliyeti sabit); **skills açıklamaya göre eşleşince yüklenir** — bu yüzden ağır bilgi (tasarım sistemi, React performans kuralları, SEO denetim prosedürü) skill olarak kurulur. Otomatik tetiklenir ya da sohbette `/skill-adi` ile çağrılır.

### Kurulacak 4 skill (repo kökünde, PowerShell)

```powershell
cd C:\dev\buyuk_gezi_projesi\gezi_bot

# 1) ui-ux-pro-max — tasarım zekâsı (67 UI stili, 100 tasarım kuralı, tasarım sistemi üretici)
npx ui-ux-pro-max-cli init --ai cursor

# 2) Vercel React/Next.js performans kuralları (70 kural, öncelik sıralı) — gerçek skill adı:
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices

# 3) Vercel web tasarım denetim kuralları (erişilebilirlik/UX/performans compliance)
npx skills add vercel-labs/agent-skills --skill web-design-guidelines

# 4) seo-audit — teknik SEO denetimi (meta, structured data, OG, sitemap, Core Web Vitals)
npx skills add sickn33/antigravity-awesome-skills --skill seo-audit
```

TUI notu: ajan seçim ekranında Cursor "Universal (.agents/skills) — always included" grubundadır; ekstra seçim yapmadan **Enter** yeterli. TUI döngüye girer ya da "Cancelled / targetAgents.includes is not a function" hatası verirse komuta **`-y`** ekleyin (prompt'suz kurulum). seo-audit için manuel alternatif: `git clone --depth 1 https://github.com/sickn33/antigravity-awesome-skills.git $env:TEMP\aas` ardından `Copy-Item -Recurse "$env:TEMP\aas\skills\seo-audit" .cursor\skills\seo-audit`. Aynı skill hem `.agents\skills` hem `.cursor\skills` altındaysa tek kopya bırak. Kurulum sonunda önerilen `find-skills` (global, `~\.agents\skills`) opsiyoneldir; kalması önerilir.

| Skill | Ne verir | Bu projede ne zaman |
|---|---|---|
| **ui-ux-pro-max** | UI stilleri, palet/tipografi/UX guideline veritabanı, `search.py` ile tasarım sistemi üretimi (`--domain style/typography/chart`, `--stack react/html-tailwind`) | T-03 tema/logo entegrasyonu, hero, kart/sihirbaz UI'ı; sorgu örneği: "travel guide, coastal, trustworthy" — **ama marka kararı `plan/04`'ündür; skill'in önerdiği palet bizim paleti EZMEZ** |
| **react-best-practices** | Vercel mühendislik kuralları: request waterfall eliminasyonu, bundle optimizasyonu, server/client performans | tüm site görevlerinde otomatik; özellikle T-04 (prod build + Lighthouse) öncesi |
| **web-design-guidelines** | Vercel UI kod denetim kuralları: erişilebilirlik, UX, performans compliance | T-03/T-04 sonrası görsel kod denetimi; shadcn bileşen özelleştirmelerinde |
| **seo-audit** | Teknik SEO denetim prosedürü: meta/JSON-LD/OG/sitemap/CWV kontrol listesi + öncelikli aksiyon planı | T-06 sonrası, deploy öncesi ve her faz sonunda `/seo-audit` ile |

### Kurallar
- **3-4 skill'den fazla kurmayın:** her skill'in adı/açıklaması ajanın başlangıç bağlamına girer; fazlası gürültü + bakım yükü. İleride ihtiyaç olursa [skills.sh](https://skills.sh) ekosisteminden (`npx skills add ...`) veya `spencerpauly/awesome-cursor-skills` listesinden seçerek ekleyin.
- Opsiyonel (şimdilik kurmuyoruz): `find-skills` (meta skill — ajanın skill önermesi, `npx skills add vercel-labs/skills --skill find-skills`), `react-view-transitions` (animasyonlar; B-02 harita sonrası değerlendirilir), ecommerce-seo-audit (biz e-ticaret değiliz).
- ui-ux-pro-max'ın Python scriptleri (`search.py`) Python 3 ister — makinede var (`.venv_test` / global `python`), ek kurulum gerekmez.
- **Rules entegrasyonu (T-00'da ajana yaptırılacak):** `100-site.mdc` sonuna "UI görevlerinde ui-ux-pro-max skill'ini, performans konularında react-best-practices skill'ini kullan"; `200-seo.mdc` sonuna "SEO görevi bitiminde seo-audit skill'iyle denetim çalıştır" satırları eklenir.

---

## 4. UI yığını (site profesyonelliği için)

1. **shadcn/ui** — Radix + Tailwind üzerine kopyala-yapıştır bileşen sistemi; Tailwind v4 + React 19 + Next 16 ile uyumlu sürümü `npx shadcn@latest init` kurar. Tema: mevcut `deniz/kopuk/kumsal/gunes` tokenlarını shadcn `--background/--foreground/--primary...` değişkenlerine eşle; şamandıra vurgu rengi (doküman #04) `--primary` veya `--accent` olur.
   - Alınacak bileşenler (ihtiyaç sırasıyla): `button, card, badge, tabs, slider, dialog, sheet, breadcrumb, skeleton, sonner(toast), dropdown-menu, tooltip, input, select, checkbox`.
2. **lucide-react** ikonlar (shadcn ile gelir) — harita/pin yerine **şamandıra motifi** için özel SVG set (doküman #04'te).
3. **motion** (`npm i motion`) — mevcut `anim-yukselt-*` sınıflarının sürdürülebilir hâli; abartı animasyon yok, `prefers-reduced-motion` desteği şart.
4. Erişilebilirlik denetimi: `eslint-plugin-jsx-a11y` (ESLint kurulumunda dahil) + Playwright MCP ile klavye turu.

---

## 5. Kalite kapıları

```bash
# site/ içinde
npm i -D eslint@latest typescript-eslint eslint-plugin-jsx-a11y prettier prettier-plugin-tailwindcss husky lint-staged @commitlint/cli @commitlint/config-conventional
npx husky init
```
- **ESLint 9 flat config** (`eslint.config.mjs`): typescript-eslint + jsx-a11y + next/core-web-vitals.
- **Prettier** + tailwindcss plugin (sınıf sırası otomatik).
- **husky pre-commit:** `lint-staged` → eslint --fix + prettier; **commit-msg:** commitlint (conventional: `feat(site): ...`, `fix(sunucu): ...`) — Türkçe özet serbest, tip/scope İngilizce (araç uyumu).
- **TypeScript:** `strict: true` + `noUncheckedIndexedAccess` (yeni kodda `any` yasak — kural dosyasında da var).
- Python tarafı: `ruff` (lint+format) + `mypy --strict` kademeli (şimdilik `sunucu/api` ve `ortak/` kapsamda).

## 6. Test & ölçüm

- **Vitest** (site unit): slug üretimi, metadata şablonları, API sarmalayıcı parse testleri.
- **Playwright e2e** (`site/e2e/`): 3 kritik akış — (1) ana→keşif→yer detay, (2) rota sihirbazı senaryo 2 uçtan uca (alternatifler→seç→bölge önerisi), (3) SEO sözleşme testi: her sayfa türünde title/description/canonical/JSON-LD varlık asserti. Koşum: yerel API+site ayakta iken; ileride GitHub Actions.
- **Lighthouse CI** (`lighthouserc.json`): bütçeler doküman #02 §8'de (Perf≥85, SEO≥95, A11y≥95, BP≥95). Şimdilik yerel `lhci autorun`, Faz 2'de CI.
- Mevcut **pytest** rota motoru testleri korunur; her rota görevinde koşar (kural dosyasında yazıyor).

## 7. `.cursor/commands/` — görev şablonları

`.cursor/commands/gorev.md` (örnek; komutlar sohbetten `/gorev` ile çağrılır):
```markdown
Bu görev için doküman #07'deki şablonu kullan:
1) Amaç (kullanıcı ne görecek) 2) Katman (veri/sunucu/site/ortak) 3) Dosyalar
4) Yapılmayacaklar 5) Doğrulama adımı (Playwright MCP / curl / pytest)
6) Taksonomi değişiyorsa: önce dokumanlar/ + ortak/sabitler.py
Kod yazmadan önce ilgili dosyaları oku ve planını 5 maddede özetle; onay bekle.
```
Benzerleri: `/seo-denetle` (sayfa URL'i ver → title/desc/JSON-LD/canonical/img kontrol listesi döndür), `/surum-oncesi` (lint+test+build+lighthouse özet).

## 8. GitHub tarafı

- Repo `gezi_bot` → **`samandira`** olarak yeniden adlandır (GitHub otomatik redirect verir); açıklama: "Şamandıra — Karadeniz'in kişisel gezi rehberi ve rota planlayıcısı (Next.js + FastAPI + PostGIS)".
- `main` branch koruması: PR zorunlu, 1 onay (iki kişilik ekipte birbirinizin PR'ı), status check: lint+test.
- **GitHub Projects** board: Buzdolabı / Bu hafta / Cursor'da / İnceleme / Bitti.
- İki profil de bu repoyu **pin'lesin** (mevcut pin'ler zayıf; mezuniyet vitrini için kritik).
- Repo public mi kalacak? Öneri: geliştirme sırasında private, Faz 6 sonunda public (kod MIT/Apache + veri hariç + README'de canlı site & demo video). (Karar sorusu kullanıcıya soruldu.)

---

## 9. Kurulumun kendisi için Cursor talimatı

Bu kurulumu ajana yaptırmak için doküman #07'deki **T-00** talimatını kullanın (tek seferde tüm rules dosyaları + AGENTS.md + mcp.json + package kurulumları). MCP `postgres` kullanıcısını ve GitHub ayarlarını **elle** yapacaksınız (ajan DB rolü/parolası ve GitHub settings'e dokunmasın).
