# Şamandıra — BAŞLANGIÇ REHBERİ (bugün, ~20 dakika)
> "Şimdi ben ne yapacağım?" sorusunun cevabı. Sırayla yapın, her adımın sonunda doğrulama yazıyor.

## Büyük resim: ne nereye gidiyor?

```
C:\Users\ebube\OneDrive\Desktop\buyuk_gezi_projesi\gezi_bot\   ← repo kökü
│
├── plan\                    ← ADIM 1: bu klasörü zip'ten buraya çıkarıyorsun
│   ├── BASLA.md             (bu dosya)
│   ├── 00_brief_eki.md      (her Cursor sohbetine yapıştırılacak güncel bağlam)
│   ├── 01..07_*.md          (strateji, SEO, araçlar, marka, deploy, mobil, talimatlar)
│   └── logo\                (SVG konseptler + onizleme.html + hero görsel)
│
├── .cursor\                 ← ADIM 2-4: skill'ler + MCP buraya kurulur
│   ├── skills\              (ui-ux-pro-max, react-best-practices, seo-audit)
│   ├── mcp.json             (Playwright, Context7, Postgres, Fetch)
│   ├── rules\               ← BUNLARI AJAN OLUŞTURACAK (T-00 görevi)
│   └── commands\            ← BUNLARI AJAN OLUŞTURACAK (T-00 görevi)
│
├── veri\ sunucu\ site\ ortak\ dokumanlar\ altyapi\   ← mevcut kod (dokunma)
└── calis.txt
```

**Mantık:** `plan/` klasörü = projenin "beyni". Cursor ajanı her görevde bu dokümanları OKUR, sen ona kısa talimat verirsin. Kurallar/skill'ler/MCP = ajanın donanımı. Kod yazmak yok — hepsini ajan yapacak, sen doğrulayacaksın.

---

## ADIM 1 — `plan/` klasörünü repoya koy (2 dk)

1. Arena workspace'inden **`samandira_plan_paketi.zip`** dosyasını indir (içinde hazır `plan/` klasörü var).
2. Zip'i **repo kökünde** (`C:\dev\buyuk_gezi_projesi\gezi_bot\`) dışa aktar → `gezi_bot\plan\BASLA.md` görünecek şekilde.
3. Doğrulama: repo kökünde `plan` klasörü var, içinde md dosyaları + `logo` klasörü.

> ✅ Repo OneDrive dışında (`C:\dev\...`) tutuluyor — doğru karar; OneDrive + git/`node_modules` senkron çakışması riski yok.

## ADIM 2 — Skill'leri kur (5 dk)

PowerShell aç, repo köküne git:

```powershell
cd C:\dev\buyuk_gezi_projesi\gezi_bot

# 1) UI/UX Pro Max — tasarım zekâsı (67 stil, 100 kural, tasarım sistemi üretici)   ✅ sizde kurulu
npx ui-ux-pro-max-cli init --ai cursor

# 2) Vercel React/Next.js performans kuralları — DİKKAT: skill'in gerçek adı "vercel-react-best-practices"
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices

# 3) Vercel web tasarım denetim kuralları (erişilebilirlik + UX + performans)
npx skills add vercel-labs/agent-skills --skill web-design-guidelines

# 4) Teknik SEO denetimi
npx skills add sickn33/antigravity-awesome-skills --skill seo-audit
```

**Ajan seçim ekranı (TUI) nasıl geçilir:** "Which agents do you want to install to?" listesinde Cursor, **Universal (.agents/skills)** grubunda "always included" yazar — yani ekstra seçim YAPMADAN doğrudan **Enter**'a bas. İkinci bir "Additional agents / Search:" ekranı gelirse arama kutusunu **boş bırakıp yine Enter**. En temizi: komutun sonuna **`-y`** ekle, TUI'yi tamamen atlar (TUI döngüye girer veya "Cancelled / targetAgents.includes is not a function" hatası verirse kesin çözüm budur):

```powershell
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices -y
```

Ekran yine döngüye girerse **Ctrl+C** ile çık ve manuel kopyala:

```powershell
git clone --depth 1 https://github.com/sickn33/antigravity-awesome-skills.git "$env:TEMP\aas"
New-Item -ItemType Directory -Force .cursor\skills | Out-Null
Copy-Item -Recurse "$env:TEMP\aas\skills\seo-audit" .cursor\skills\seo-audit
```

- Doğrulama: `.cursor\skills\` ve/veya `.agents\skills\` altında 4 skill klasörü: `ui-ux-pro-max`, `vercel-react-best-practices`, `web-design-guidelines`, `seo-audit`. Aynı skill **iki yerde birden** varsa tek yerde bırak (öneri: `.cursor\skills\`). Cursor'ı tamamen kapat-aç; sohbette `/` yazınca menüde görünsünler.
- Not: skills CLI kurulum sonunda bir kerelik "find-skills kurulsun mu?" sorar; evet dersen `~\.agents\skills\find-skills` (global) eklenir — opsiyonel meta-skill, kalması önerilir; istemezsen `Remove-Item -Recurse "$env:USERPROFILE\.agents\skills\find-skills"`.
- `npx` bulunamadıysa: Node 18+ gerekli (`node -v`) — site çalıştığı için muhtemelen zaten var.

> 4 skill'de kalıyoruz (her biri ajanın başlangıç bağlamına yalnızca ad/açıklama düzeyinde girer). Ayrıntı ve gerekçeler: `plan/03_cursor_araclari_kurulumu.md` §3b.

## ADIM 3 — MCP sunucuları (3 dk)

`.cursor\mcp.json` dosyasını oluştur (yoksa), içeriği:

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
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

(`uvx` yoksa: `pip install uv` — ya da fetch bloğunu şimdilik sil, kritik değil.)

Postgres MCP'yi **ADIM 4'ten sonra** ekleyeceğiz (parola dosyaya düz yazılmasın diye önce read-only rol açılıyor).

## ADIM 4 — Postgres'e salt-okur rol + MCP'ye ekle (5 dk)

```powershell
& "C:\PostgreSQL\bin\psql.exe" -U postgres -d gezi_veritabani
```
psql içinde sırayla (`GUCLU_PAROLA` yerine kendi üretin):
```sql
CREATE ROLE gezi_oku LOGIN PASSWORD 'GUCLU_PAROLA';
GRANT CONNECT ON DATABASE gezi_veritabani TO gezi_oku;
GRANT USAGE ON SCHEMA public TO gezi_oku;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO gezi_oku;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO gezi_oku;
\q
```

Sonra `mcp.json`'a bu bloğu ekle (diğerleriyle virgülle):
```json
"postgres": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-postgres",
    "postgresql://gezi_oku:GUCLU_PAROLA@localhost:5432/gezi_veritabani"]
}
```

Doğrulama: Cursor → Settings → **MCP** → **Reload** → 4 sunucu da yeşil.

> Not: `mcp.json` git'e girecekse parolayı dosyada bırakma — ya `.gitignore`'a al (`.cursor/mcp.json`) ya da Cursor'ın `${env:...}` desteğiyle ortam değişkeninden ver. Ajana bu dosyayı düzenletme.

## ADIM 5 — İlk Cursor görevi: T-00 (ajana yaptır, ~15-30 dk)

Yeni Cursor sohbeti (Agent modu) aç ve şunu yapıştır:

```
Önce plan/BRIF.md ve plan/00_brief_eki.md dosyalarını oku (proje brifi + güncel kararlar).
Şimdi plan/07_cursor_talimatlari.md içindeki T-00 görevini uygula.
Skills ve mcp.json'u ben kurdum — sen yalnızca doğrula.
Bitince commit ATMA; yapılan değişikliklerin listesini ve doğrulama sonuçlarını ver.
```

T-00; `.cursor/rules/` (4 kural dosyası), `AGENTS.md` güncellemesi, shadcn/ui, ESLint/Prettier/husky, Vitest/Playwright iskeleti ve `.cursor/commands/` kurulumunu ajana yaptırır. Sonucu gözle kontrol et, sonra **kendin** commit at:
```
git add -A && git commit -m "chore: Cursor araç kurulumu + plan klasörü (T-00)"
```

## ADIM 6 — Sıra: sonraki görevler

`plan/07_cursor_talimatlari.md`'deki bağımlılık sırası:

```
T-00 → T-01 (README gerçeği) → T-02 (Rotam→Şamandıra metinleri) → T-03 (logo/tema/404)
     → T-04 (prod build) → T-12 (deploy paketi) → T-05 (slug) → T-06 (SEO çekirdeği) → GSC'ye aç
     → T-07/T-08/T-09/T-10/T-11 (paralel) → T-13/T-14 → T-15
```

**T-03'ten önce tek ev ödevin var:** `plan/logo/onizleme.html`'i aç, A/B/C konseptlerinden birini ve sloganı Hiranur'la seç (benim önerim: ana logo C, harita markırı B, favicon A; slogan "Rotanı şamandıra ile bul."). Seçimi T-03 talimatının başına yaz.

Her görev için ritüel aynı: yeni sohbet → brif + "plan/00_brief_eki.md oku" → görev metnini yapıştır → doğrulamayı kendin çalıştır → sen commit at.

---

## Takıldığında (hızlı çözümler)

| Belirti | Çözüm |
|---|---|
| `npx: command not found` | Node 18+ kur (nodejs.org) veya terminali yeniden başlat |
| Skill `/` menüsünde yok | **Cursor repo kökünü klasör olarak açmalı.** Cursor 3'te açılışta gelen hub/Agents penceresi (sol tarafta "Repositories" listesi, Customize → Skills'te yalnız "User" bölümü) proje bağlamı TAŞIMAZ: proje skill'leri ve `.cursor/mcp.json` burada yüklenmez. Repo'yu yan listeden çift tıklayın ya da sağ üstteki **IDE ↗** düğmesiyle klasik IDE penceresinde açın → Ctrl+Shift+P → "Reload Window" → Customize → Skills'te "Project" bölümü gelir. Tüm görevleri (T-00 dahil) ve MCP yeşil kontrolünü bu IDE penceresinde yapın. Ek kontrol: klasör adı birebir `.cursor\skills\<ad>\SKILL.md` yapısında mı (dosya adı BÜYÜK harf); frontmatter'da `disable-model-invocation: true` satırı VARSA silin (skill'i gizler) |
| MCP kırmızı | Settings → MCP → Reload; Node sürümü; postgres rolü/parolası; PostgreSQL servisi çalışıyor mu (`C:\PostgreSQL\bin\pg_ctl.exe status -D C:\PostgreSQL\data`) |
| ui-ux-pro-max scriptleri Python istiyor | `python --version` 3.x olmalı (var: `.venv_test`); global yoksa python.org'dan kur |
| Ajan kural dışı iş yapıyor (commit atıyor, katman karıştırıyor) | `plan/00_brief_eki.md` §7'yi sohbetin başına tekrar yapıştır; rules dosyalarını T-00'da birebir oluşturduğundan emin ol |
| OneDrive dosya kilidi/senkron hatası | ADIM 1'deki uyarı: repoyu OneDrive dışına taşı |
