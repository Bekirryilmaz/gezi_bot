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

CORS: `API_IZINLI_ORIGINLER` (varsayılan `http://localhost:3000` ve
`http://127.0.0.1:3000`).

## Dosyalar

- `uygulama.py` — FastAPI uygulaması, CORS, router bağlama
- `semalar.py` — İstek/cevap Pydantic. `veritabani/modeller.py` (saklama) ile
  bilinçli ayrı: biri nasıl durduğu, diğeri dışarıya nasıl göründüğü
- `yerler_router.py` — Şehir, keşif listesi, yer detay, bölgeler
- `rotalar_router.py` — Rota üretme / getirme / alternatifler / bölge önerisi /
  sabit rotalar

Site tipleri `site/src/lib/types.ts` bu şemalarla hizalı tutulur.

## Uç noktalar (9 genel)

`plan/00_brief_eki.md` §4: API ayakta. Aşağıdaki tablo brif §8 / kod ile aynıdır.

| Metod | Yol | Açıklama |
|---|---|---|
| GET | `/sehirler` | Aktif şehirler |
| GET | `/sehirler/{sehir_anahtari}/yerler` | `{ yerler, toplam_sayi }`. `limit` / `offset`. Varsayılan `sadece_kesif=true` |
| GET | `/sehirler/{sehir_anahtari}/bolgeler` | Şehir merkezi + ilçe duygu profilleri |
| GET | `/yerler/{yer_id}` | Detay: profil, duygu özeti, örnek ifadeler |
| POST | `/rotalar/olustur` | Tek rota (Senaryo 1 veya eski Senaryo 2) |
| POST | `/rotalar/olustur-alternatifler` | 2–3 alternatif; otel dayatma yok (sitenin Senaryo 2’si) |
| POST | `/rotalar/{rota_id}/konaklama-bolgesi-oner` | Seçilen rotaya baskın ilçe + gerekçe + örnek tesis |
| GET | `/rotalar/{rota_id}` | Kayıtlı, paylaşılabilir rota |
| GET | `/sabit-rotalar` | Elle küratör rotalar (`bolge` filtresi opsiyonel) |

Şemada gizli: `GET /` (sağlık mesajı), `GET /sehirler-tanimli` (`include_in_schema=false`).

### Keşif vitrini

`sadece_kesif=true` (site varsayılanı, `sorgular.py`):

- Konaklama gizlenir
- Yeme-içme yalnız `sehrin_klasigi` / `sponsorlu_mekan` / `kahvalti_verir`
  **veya** duygu ≥ 80/100 (skor ≥ 0.6)
- Gezilecek yer serbest

Rota motoru `sadece_kesif=false` ile kısıtsız çeker. Ham yorum metni ve
yorumcu adı dönülmez; `ornek_ifade` kısa ve anonim kalır.

### Rota senaryoları

**Senaryo 1 — konaklama belli:** `konaklama_yer_id` veya `konaklama_enlem` +
`konaklama_boylam` veya `konaklama_bolge_adi` (ilçe merkezi
`sehir_ayarlari.ilce_merkezleri`). `POST /rotalar/olustur`.

**Senaryo 2 — belli değil (sitenin kullandığı akış):**

1. `POST /rotalar/olustur-alternatifler` → “Dengeli keşif” / “Tarih & kültür” /
   “Doğa & manzara” benzeri alternatifler
2. Kullanıcı birini seçer
3. `POST /rotalar/{id}/konaklama-bolgesi-oner` → bölge önerisi (otel zorunlu değil)

Eski `POST /rotalar/olustur` konaklama yoksa hâlâ otel önerir (geriye uyumluluk).

Örnek gövde (Senaryo 1):

```json
{
  "sehir_anahtari": "samsun",
  "gun_sayisi": 2,
  "konaklama_yer_id": "<konaklama yer uuid>",
  "tercihler": {
    "ilgi_agirliklari": { "tarihi_kulturel_puani": 0.7, "doga_macera_puani": 0.3 },
    "aktiviteler": ["yuzme"],
    "zorunlu_duraklar": [],
    "ucuz_tercih_et": false,
    "sakin_tercih_et": false
  }
}
```

Cevaptaki her durağın `kirilim` alanı skor bileşenlerini açıklar (kara kutu yok).
Sonuç `kullanici_rotalari` tablosuna yazılır; commit API katmanındadır.
