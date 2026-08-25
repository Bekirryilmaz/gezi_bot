# API (`sunucu/api/`)

FastAPI ile yazılmış REST API. `veri/` katmanından `veritabani/aktarim/` ile
aktarılmış veriyi okuyup sunar, `rota_motoru/`'nu çağırıp kişiselleştirilmiş
rota üretir. Şu an tek tüketicisi Swagger arayüzüdür (`site/` Faz 3'te
eklenecek).

## Çalıştırma

```bash
uvicorn sunucu.api.uygulama:uygulama --reload
```

`http://127.0.0.1:8000/docs` adresinde otomatik Swagger arayüzü açılır —
tüm uç noktaları buradan, gerçek Samsun verisiyle deneyebilirsin.

## Dosyalar

- `uygulama.py` — `FastAPI()` uygulaması, CORS middleware, router'ların
  bağlanması.
- `semalar.py` — İstek/cevap Pydantic şemaları. `sunucu/veritabani/modeller.py`
  (veritabanı şeması) ile BİLEREK ayrı tutulur: biri "nasıl saklandığı",
  diğeri "dışarıya nasıl gösterildiği/istendiği".
- `yerler_router.py` — Şehir ve yer listeleme/detay uç noktaları.
- `rotalar_router.py` — Rota oluşturma/getirme + sabit (küratörlüğü yapılmış)
  rota listeleme uç noktaları.

## Uç Noktalar

| Metod & Yol | Açıklama |
|---|---|
| `GET /sehirler` | Aktif şehirleri listeler |
| `GET /sehirler/{sehir_anahtari}/yerler` | `{ yerler, toplam_sayi }`. Varsayılan `sadece_kesif=true`: konaklama gizlenir; yeme-içme yalnızca `sehrin_klasigi` / `sponsorlu_mekan` / `kahvalti_verir` veya duygu ≥ 80/100. `sadece_kesif=false` kısıtlamasız (rota motoru/test). |
| `GET /yerler/{yer_id}` | Bir yerin tam detayını getirir (yer profili, duygu özeti, örnek yorumlar dahil) |
| `POST /rotalar/olustur` | Kullanıcı tercihlerine göre kişiselleştirilmiş rota üretir (bkz. aşağıdaki senaryolar) |
| `GET /rotalar/{rota_id}` | Daha önce üretilmiş, paylaşılabilir linkli bir rotayı getirir |
| `GET /sabit-rotalar` | Elle küratörlüğü yapılmış hazır rotaları listeler (opsiyonel `bolge` filtresi) |

### `POST /rotalar/olustur` — Senaryo Seçimi

İstekteki konaklama bilgisine göre otomatik karar verilir:

- `konaklama_yer_id` **VEYA** `konaklama_enlem` + `konaklama_boylam`
  verilmişse → **Senaryo 1** (konaklama bölgesi belli).
- Hiçbiri verilmemişse → **Senaryo 2** (konaklama bölgesi belli değil,
  algoritma en iyi adayların ağırlık merkezine göre bir konaklama önerir ve
  cevapta `konaklama_onerisi` alanını doldurur).

Örnek istek gövdesi (Senaryo 1):

```json
{
  "sehir_anahtari": "samsun",
  "gun_sayisi": 2,
  "konaklama_yer_id": "<veritabanindaki bir KONAKLAMA yerinin id'si>",
  "tercihler": {
    "ilgi_agirliklari": { "tarihi_kulturel_puani": 0.7, "doga_macera_puani": 0.3 },
    "aktiviteler": ["yuzme"],
    "zorunlu_duraklar": [],
    "ucuz_tercih_et": false,
    "sakin_tercih_et": false
  }
}
```

Cevap, her gün için sıralı durakları (her durağın skor kırılımıyla birlikte
— hangi bileşenin puana ne kadar katkı yaptığı, "kara kutu değil" ilkesiyle)
ve toplam mesafe/süre tahminlerini içerir.
