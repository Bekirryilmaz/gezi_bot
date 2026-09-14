# API (`sunucu/api/`)

FastAPI REST API. Aktarılmış kataloğu sunar; `rota_motoru/` ile kişiselleştirilmiş
rota üretir. Tüketici: **Şamandıra sitesi** (`site/`, Next.js). Swagger:
http://127.0.0.1:8125/docs

## Çalıştırma

Repo kökünden:

```text
.\.venv_test\Scripts\python.exe -m uvicorn sunucu.api.uygulama:uygulama --host 127.0.0.1 --port 8125
```

Port **8125** (`calis.txt` ile aynı; 8000 değil). `site/.env.local`:
`NEXT_PUBLIC_API_URL=http://127.0.0.1:8125`. Tarayıcı istekleri aynı origin
üzerinden `/backend/*` rewrite ile gelir (CORS ihtiyacını azaltır). SSR
doğrudan `NEXT_PUBLIC_API_URL`’e gider.

CORS: development varsayılanı `http://localhost:3000` ve
`http://127.0.0.1:3000`; production'da `API_IZINLI_ORIGINLER` zorunlu,
wildcard/localhost reddedilir. Her cevap `X-Request-ID` taşır; loglar JSON
allow-list'tir ve query/header/body yazmaz.

## Dosyalar

- `uygulama.py` — FastAPI uygulaması, CORS, health/readiness, router bağlama
- `altyapi.py` — Request ID, tipli hata, structured log, gövde/write limitleri
- `semalar.py` — İstek/cevap Pydantic. `veritabani/modeller.py` (saklama) ile
  bilinçli ayrı: biri nasıl durduğu, diğeri dışarıya nasıl göründüğü
- `yerler_router.py` — Şehir, keşif listesi, yer detay, bölgeler
- `rotalar_router.py` — Tek günlük public üretim ve tarihsel read-only uçlar

Site tipleri `site/src/lib/types.ts` bu şemalarla hizalı tutulur.

## Kamusal uç noktalar

`plan/00_brief_eki.md` §4: API ayakta. Aşağıdaki tablo brif §8 / kod ile aynıdır.

| Metod | Yol | Açıklama |
|---|---|---|
| GET | `/sehirler` | Aktif şehirler |
| GET | `/sehirler/{sehir_anahtari}/yerler` | `{ yerler, toplam_sayi }`. `limit` / `offset`. Varsayılan `sadece_kesif=true` |
| GET | `/sehirler/{sehir_anahtari}/bolgeler` | Şehir merkezi + ilçe tanıtımları |
| GET | `/yerler/{yer_id}` | Allow-list yer detayı; iç analiz alanı yok |
| POST | `/v1/gunluk-planlar` | Tek günlük plan; `Idempotency-Key` zorunlu |
| GET | `/health` | Süreç liveness |
| GET | `/readiness` | PostgreSQL + PostGIS readiness |

Şemada gizli tarihsel uçlar yeni kayıt üretmez. Eski çok günlük ve konaklama
POST uçları kontrollü `410 Gone` döndürür; eski kayıtlar silinmez.

### Keşif vitrini

`sadece_kesif=true` (site varsayılanı, `sorgular.py`):

- Konaklama gizlenir
- Yeme-içme yalnız `sehrin_klasigi` / `kahvalti_verir`
  **veya** duygu ≥ 80/100 (skor ≥ 0.6)
- Gezilecek yer serbest

Rota motoru `sadece_kesif=false` ile kısıtsız çeker. Sponsor bayrağı adaylık,
sıra veya skoru değiştirmez; yalnız `ticari_bildirim` olarak açıklanabilir.
Public DTO; yorum/yazar, örnek ifade, duygu/puan, yorum hacmi, profil ve skor
kırılımı alanlarını hiçbir JSON seviyesinde taşımaz.

### Tek günlük rota

Örnek gövde:

```json
{
  "sehir_anahtari": "samsun",
  "tercihler": {
    "ilgi_agirliklari": { "tarihi_kulturel_puani": 0.7, "doga_macera_puani": 0.3 },
    "aktiviteler": ["yuzme"],
    "zorunlu_duraklar": [],
    "ucuz_tercih_et": false,
    "sakin_tercih_et": false
  }
}
```

`gun_sayisi`, konaklama ve alternatif sayısı extra-field doğrulamasıyla
reddedilir. İç motor kırılımı veritabanında korunabilir ama public cevaba
çıkmaz. Sonuç `kullanici_rotalari` tablosuna tek gün olarak yazılır.
