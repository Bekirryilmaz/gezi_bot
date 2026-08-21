# Altyapı

## Şu An

`docker-compose.yml` sadece yerel geliştirme için PostgreSQL + PostGIS veritabanını
ayağa kaldırır. Kullanımı için kök `README.md` içindeki "Kurulum" bölümüne bakabilirsin.

## Faz 3'te Eklenecekler

- `sunucu` (FastAPI) ve `site` (Next.js) servisleri `docker-compose.yml`'a eklenecek
- Nginx reverse proxy + Let's Encrypt (certbot) ile SSL/domain bağlama
- Oracle Cloud Free Ampere sunucusuna (arm64) dağıtım betiği
- Veritabanı için otomatik yedekleme (cron ile `pg_dump`)
- Scraping ve duygu analizi işleri için zamanlanmış görevler (systemd timer / cron),
  bunlar her zaman açık servisler değil, periyodik olarak çalışan işler olacak
