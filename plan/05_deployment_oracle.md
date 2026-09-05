# Şamandıra — Oracle Cloud'a Canlıya Alma (şamandıra.com)
**Tarih:** 2026-09-05 · Hedef: dev tunnel'dan kalıcı, hızlı, güvenli yayına geçiş · Süre: ~1 tam gün (manuel adımlar dahil)

> Karar doğrulandı: Oracle **Always Free** Ampere A1 kotası (4 OCPU / 24 GB RAM / 200 GB blok / 10 TB egress) **PAYG hesaplarında ücretsiz kalıyor**; Haziran 2026'daki kısıtlama yalnızca Free Tier (PAYG'ye yükseltilmemiş) hesapları etkiledi. PAYG'ye yükseltmiş olmanız doğru hamleydi — ayrıca PAYG'de "boşta kaldı diye instance'ı geri alma" (idle reclaim) riski de yok. Yine de bütçe alarmı kurun (aşağıda).

---

## 0. Hedef mimari

```
İnternet
  └─ GoDaddy DNS: şamandıra.com (A → Oracle reserved IPv4)
       └─ Oracle VCN ingress: 80, 443 (22: sadece sizin IP)
            └─ Caddy (otomatik Let's Encrypt, punycode cert, www→apex 301, güvenlik başlıkları)
                 ├─ site  (Next 16 standalone, iç port 3000)
                 │    ├─ SSR fetch → http://api:8125 (docker ağı)
                 │    └─ tarayıcı → /backend/* rewrite → http://api:8125 (next.config.ts)
                 ├─ api   (FastAPI/uvicorn, iç port 8125; opsiyonel: api. alt alan adı)
                 ├─ db    (PostGIS, iç port 5432 — DIŞA KAPALI)
                 └─ umami (analitik, iç port 3001; caddy /umami veya umami. alt alan adı)
```

Kurallar: DB ve API public internet'e **açılmaz** (API yalnız opsiyonel `api.` alt alan adıyla + CORS kısıtlı). Scraping hattı sunucuya **kurulmaz** (K2 kararı — toplayıcılar geliştirme makinesinde kalır). Sunucuda yaşayan: DB + API + site + Caddy + Umami.

---

## 1. Oracle konsolu (manuel, ~30 dk)

1. **Instance:** Compute → Instances → Create:
   - Image: **Ubuntu 24.04 LTS (aarch64)**
   - Shape: **VM.Standard.A1.Flex → 4 OCPU / 24 GB RAM** (Always Free etiketini görün; PAYG'de $0)
   - Boot volume: 50 GB (kota 200 GB toplam; veri için 100 GB block volume ekleyin → `/opt` veya docker volume'a mount)
   - Public IP: **Reserved** alın (ephemeral IP instance durursa değişir, DNS kırılır)
   - SSH: kendi public key'iniz (`C:\Users\ebube\.ssh\id_ed25519.pub` — yoksa `ssh-keygen -t ed25519`)
   - İsim: `samandira-01`
2. **VCN ingress kuralları** (Security List): TCP 80 ← 0.0.0.0/0, TCP 443 ← 0.0.0.0/0, TCP 22 ← **sizin IP** (veya geçici olarak 0.0.0.0/0, sonra daraltın).
3. **Billing → Budgets:** $1 eşikli alarm (yanlışlıkla ücretli kaynak açılırsa haberiniz olsun; normalde fatura $0).
4. **Object Storage:** `samandira-yedek` bucket (Always Free: 20 GB) — DB yedekleri buraya.

## 2. Sunucu hazırlığı (SSH, ~30 dk)

Windows'tan: `ssh ubuntu@<REZERVE_IP>`

```bash
# Oracle Ubuntu imajlarında iptables 80/443'ü BLOKLAR — klasik tuzak:
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save

# Temel
sudo timedatectl set-timezone Europe/Istanbul
sudo hostnamectl set-hostname samandira
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose-v2 fail2ban ufw git curl
sudo systemctl enable --now docker fail2ban
sudo usermod -aG docker ubuntu   # yeniden giriş gerekir

# unattended-upgrades zaten gelir; doğrula:
sudo systemctl status unattended-upgrades
```

⚠️ Not: Oracle imajındaki iptables kuralları ufw'dan önce gelir; ufw'u ayrıca açmayın ya da kuralları ufw ile yönetip `netfilter-persistent`'ı buna göre güncelleyin. En basiti: yukarıdaki iptables yaklaşımında kalın, ufw'u kurmayın.

## 3. Veri taşıma (Windows → sunucu, ~20 dk)

```powershell
# 1) Yerel PG sürümünü not et (sunucudaki imaj aynı major olmalı):
C:\PostgreSQL\bin\psql.exe -U gezi_kullanici -d gezi_veritabani -c "SELECT version();"

# 2) Dump (custom format, PostGIS dahil):
C:\PostgreSQL\bin\pg_dump.exe -U gezi_kullanici -Fc -f C:\yedek\gezi_2026xxxx.dump gezi_veritabani

# 3) Aktar (WinSCP veya scp):
scp C:\yedek\gezi_2026xxxx.dump ubuntu@<IP>:/home/ubuntu/
```

Sunucuda (compose ayağa kalktıktan sonra — §5):
```bash
docker compose exec -T db createdb -U gezi_kullanici gezi_veritabani   # ilk kez
cat ~/gezi_2026xxxx.dump | docker compose exec -T db pg_restore -U gezi_kullanici -d gezi_veritabani --no-owner
# doğrula:
docker compose exec db psql -U gezi_kullanici -d gezi_veritabani -c "SELECT count(*) FROM yerler;"
```
Alembic: sunucuda `alembic upgrade head` (API konteynerinde) — dump güncelse no-op olur.

Ayrıca: `veri/cikti/*.jsonl` arşivini (ham veri) **sunucuya değil** Object Storage'a yedekleyin (K2: scraping sunucuda yaşamaz; ama veri kaybına karşı arşiv şart).

## 4. Repo düzeni (T-12 talimatı üretir)

Cursor'a ürettirilecek dosyalar (`deploy/` klasörü):
```
deploy/
  docker-compose.yml
  .env.example            # sırlar şablonu (gerçek .env sunucuda, git'te YOK)
  caddy/Caddyfile
  api/Dockerfile          # python:3.12-slim, uvicorn, alembic
  site/Dockerfile         # node:22-alpine multi-stage → .next/standalone
  scripts/yedekle.sh      # pg_dump + rotasyon (7 günlük / 4 haftalık)
  scripts/rclone-yedek.md # Object Storage'a gönderim kurulum notu
  scripts/saglik.sh       # healthz kontrolleri
```

**Caddyfile** (IDN → punycode ile yazılır):
```
www.xn--amandra.com-3zb60d {
    redir https://xn--amandra.com-3zb60d{uri} permanent
}

xn--amandra.com-3zb60d {
    encode zstd gzip
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Content-Type-Options "nosniff"
        Referrer-Policy "strict-origin-when-cross-origin"
        X-Frame-Options "SAMEORIGIN"
        -Server
    }
    reverse_proxy site:3000
}

api.xn--amandra.com-3zb60d {
    encode gzip
    reverse_proxy api:8125
}
```

**docker-compose.yml iskeleti** (T-12'de tamamlanır):
```yaml
services:
  db:
    image: postgis/postgis:16-3.4        # ← yerel PG major sürümüyle eşitle (16/17)
    environment:
      POSTGRES_DB: gezi_veritabani
      POSTGRES_USER: gezi_kullanici
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes: [pgdata:/var/lib/postgresql/data]
    restart: unless-stopped
    # ports YOK — dışa kapalı

  api:
    build: {context: .., dockerfile: deploy/api/Dockerfile}
    environment:
      VERITABANI_URL: postgresql+psycopg://gezi_kullanici:${DB_PASSWORD}@db:5432/gezi_veritabani
      API_IZINLI_ORIGINLER: https://xn--amandra.com-3zb60d,https://şamandıra.com
    depends_on: [db]
    restart: unless-stopped

  site:
    build:
      context: ..
      dockerfile: deploy/site/Dockerfile
      args:
        NEXT_PUBLIC_API_URL: http://api:8125    # SSR iç ağ; tarayıcı /backend kullanır
    depends_on: [api]
    restart: unless-stopped

  caddy:
    image: caddy:2-alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./caddy/Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    restart: unless-stopped

volumes: {pgdata: {}, caddy_data: {}, caddy_config: {}}
```

Kritik env notları:
- **CORS Origin punycode olur:** tarayıcılar IDN sitelerde `Origin: https://xn--amandra.com-3zb60d` gönderir → `API_IZINLI_ORIGINLER`'de punycode **zorunlu** (Unicode varyantı eklemek zararsız).
- `NEXT_PUBLIC_*` değişkenleri **build anında** gömülür: site imajı `http://api:8125` ile build edilir (SSR docker içinden çözer); tarayıcı tarafı her zaman göreceli `/backend/*` kullanmalı (mevcut mimari zaten böyle — T-12'de doğrulanacak).
- `next.config.ts`: `output: 'standalone'` eklenir; `/backend` rewrite hedefi env'den (`BACKEND_INTERNAL_URL`, default `http://127.0.0.1:8125`; docker'da `http://api:8125`).

## 5. GoDaddy DNS

| Kayıt | Tür | Değer |
|---|---|---|
| `@` (xn--amandra.com-3zb60d) | A | `<REZERVE_IP>` |
| `www` | A | `<REZERVE_IP>` (Caddy 301'ler) |
| `api` | A | `<REZERVE_IP>` |
| `_google-site-verification` | TXT | GSC doğrulama değeri |

GoDaddy panelinde alan adı zaten IDN olarak görünür; kayıt ekranında `www` gibi ASCII alt adlar yeterli. DNS yayılması 5 dk–24 saat; `nslookup xn--amandra.com-3zb60d` ile doğrulayın. Sertifika: DNS çözüldükten sonra Caddy Let's Encrypt'ten otomatik alır (HTTP-01; 80 açık olmalı).

## 6. İlk açılış (sunucuda)

```bash
git clone https://github.com/<hesap>/samandira.git && cd samandira/deploy
cp .env.example .env && nano .env        # DB_PASSWORD üret: openssl rand -hex 24
docker compose build && docker compose up -d
docker compose ps                         # hepsi healthy/up
curl -I https://xn--amandra.com-3zb60d    # 200 beklenir
# pg_restore (§3) → alembic upgrade head (api konteynerinde) → /healthz kontrolü
```

## 7. Yedekleme (cron)

```bash
# /etc/cron.d/samandira-yedek
0 3 * * * ubuntu /opt/samandira/deploy/scripts/yedekle.sh >> /var/log/samandira-yedek.log 2>&1
```
`yedekle.sh`: `pg_dump -Fc` → `/opt/yedek/db_$(date +%F).dump` → 7 günden eski günlükleri sil, ayın 1'i haftalık kopyayı tut → `rclone copy /opt/yedek oracle-object:samandira-yedek` (rclone config: OCI Object Storage, auth = instance principal veya access key). **Ayda 1 restore tatbikatı** yapın (yedek almayan sistem = yedek almıyor).

## 8. Operasyon rutinleri

| İş | Komut/alışkanlık |
|---|---|
| Loglar | `docker compose logs -f site api caddy` |
| Yeniden yayın | `git pull && docker compose build site && docker compose up -d site` (ileride GH Actions + webhook) |
| Sağlık | `scripts/saglik.sh` + ücretsiz UptimeRobot (https + ana sayfa + /api healthz) |
| Güncelleme | unattended-upgrades açık; ayda 1 `docker compose pull` (caddy, db minor) |
| Fatura | ayda 1 kontrol: $0 (Always Free kaynaklar) |
| Instance durursa | reserved IP korunur; DNS değişmez |

## 9. Yayına geçiş gününün kontrol listesi

1. [ ] Oracle instance + iptables + docker hazır
2. [ ] DNS A kayıtları → reserved IP (yayılma beklendi)
3. [ ] `deploy/` dosyaları T-12 ile üretildi, `.env` dolduruldu
4. [ ] DB dump taşındı, restore + `alembic upgrade head` doğrulandı (`SELECT count(*) FROM yerler;`)
5. [ ] `https://şamandıra.com` 200 + sertifika geçerli + www 301
6. [ ] Prod build performansı: Lighthouse ≥ 85 (tunnel/dev mod kıyasıyla not alın)
7. [ ] GSC: alan adı mülkü (DNS TXT) + sitemap gönderimi; Bing Webmaster
8. [ ] UptimeRobot + bütçe alarmı aktif
9. [ ] Dev tunnel'lar kapatıldı; `calis.txt` ve README'ler yeni adreslerle güncellendi
10. [ ] Yedek cron çalıştı, ilk dump Object Storage'da görüldü

## 10. Alternatif: Coolify (opsiyonel kolaylık)

Kendinden yönetilen "Vercel benzeri" panel (ARM64 destekli, ücretsiz): git push → otomatik build/deploy, SSL, domain yönetimi. 24 GB RAM'de rahat çalışır. **Öneri:** ilk kurulumu düz compose ile yapın (öğrenme + kontrol); yayın otomasyonu ihtiyacı doğarsa Coolify'a geçin. İkisi aynı makinede yaşayabilir.
