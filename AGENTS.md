# Şamandıra — repo ajan bağlamı

Ürün: **Şamandıra** (Alegre Group). Canonical: `https://şamandıra.com`. Repo adı henüz `gezi_bot` (GitHub’da `samandira` olacak). Kod tanımlayıcıları Türkçe karaktersiz kalır; kullanıcıya görünen metinde "Rotam" yok.

Mevcut `site/AGENTS.md` Next.js sürüm uyarısını korur — silme. Bu dosya kök bağlamdır.

## Komutlar (kaynak: `calis.txt`)

PostgreSQL yerelde `C:\PostgreSQL` (Docker yok). Venv: repo kökünde `.venv_test`.

```text
# PostgreSQL durum
C:\PostgreSQL\bin\pg_ctl.exe status -D C:\PostgreSQL\data

# Migrasyon (bir kez / şema değişince) — sunucu/ içinden
cd sunucu
..\.venv_test\Scripts\python.exe -m alembic upgrade head

# Aktarım — repo kökünden
.\.venv_test\Scripts\python.exe -m sunucu.veritabani.aktarim.calistir --sehir samsun

# API — repo kökü, port 8125
.\.venv_test\Scripts\python.exe -m uvicorn sunucu.api.uygulama:uygulama --host 127.0.0.1 --port 8125

# Site — port 3000
cd site
npm run dev -- --port 3000

# Rota motoru testleri — repo kökü
.\.venv_test\Scripts\python.exe -m pytest sunucu/rota_motoru/testler/ -v
```

Site: http://localhost:3000 · API/Swagger: http://127.0.0.1:8125/docs · `site/.env.local`: `NEXT_PUBLIC_API_URL=http://127.0.0.1:8125`

## Kritik uyarı

Kök / `sunucu/` / `site/` README’leri `calis.txt` ile hizalıdır. Çelişkide **`calis.txt`**, **`plan/00_brief_eki.md`** ve **`dokumanlar/`** kazanır. `plan/BRIF.md` tarihî belgedir; güncel karar `plan/00_brief_eki.md`’dedir.

## Doğrulama politikası

- **UI:** Playwright MCP ile tarayıcıda akış (ilgili sayfa + en az bir bağlı akış). Tek ekran görüntüsü kanıt sayılmaz.
- **API:** curl veya Swagger (`/docs`) ile uç doğrula.
- **Rota:** `pytest sunucu/rota_motoru/testler/ -v` + skor `kirilim` bozulmasın.

## Commit / push

Kullanıcı açıkça istemeden `git commit` / `git push` yapma.


## Bağlayıcı ürün referansları ve belge yeri — 13 Eylül 2026

Kullanıcının açık talimatıyla kabul edilmiş ürün referansları docs/00-product/00-urun-felsefesi.md, 01-bilgi-mimarisi.md, 02-product-language.md ve 03-karar-motoru.md dosyalarıdır. Ürün kararlarında bunlar eski planların ve yukarıdaki tarihsel doküman öncelik ifadesinin önündedir. docs/00-product/04-sistem-mimarisi.md bundan sonraki backend, frontend, admin, AI ve mobil geliştirmeler için mimari referanstır; ilk dört belgeyi sessizce değiştiremez. Çelişki varsa ilgili madde açıkça belirtilir.

Bütün yeni belgeler bu Git deposunun docs/ yapısında yaşar: 00-product, 01-research, 02-ux, 03-design, 04-ai, 05-api, 06-frontend, 07-backend, 08-admin, 09-business. Belgeleri kullanıcının Documents klasörüne kaydetme; bu konumda bulunan önceki proje belgelerini uygun depo klasörüne içeriklerini doğrulayarak taşı.

Her yeni belge title, version, status, phase, last_update, depends, affects ve author metadata alanlarıyla başlar. Sonunda bağlı belgeler, etkilediği belgeler ve bundan sonra okunması gereken belge bulunur. Henüz yazılmamış belge açıkça planlanan olarak işaretlenir. Dizin ve aktarım kaydı: docs/README.md. Commit/push kuralı aynen geçerlidir.
