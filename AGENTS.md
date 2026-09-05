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
