"""OSM admin_level=6 ilce sinirlarini sehir ayarlarindaki resmi isimlerle esler."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from veri.ortak.metin_araclari import turkce_kucuk_harf
from veri.ortak.sehir_ayarlari import sehir_getir

ILCE_SINIRI_SURUMU = "faz25.2-osm-admin6-v1"
HGM_CAPRAZ_KONTROL_NOTU = (
    "HGM ucretsiz ilce siniri veri seti resmi nitelik tasimaz; "
    "OSM ODbL admin_level=6 relation'lari canonical kaynaktir, HGM yalniz capraz kontroldur."
)
_ILCE_TAKMA: dict[str, str] = {
    "ondokuzmayis": "19 mayis",
    "19 mayis": "19 mayis",
    "ilk adim": "ilkadim",
}
_HARF_KATMA = str.maketrans(
    {
        "ı": "i",
        "İ": "i",
        "I": "i",
        "ş": "s",
        "Ş": "s",
        "ğ": "g",
        "Ğ": "g",
        "ü": "u",
        "Ü": "u",
        "ö": "o",
        "Ö": "o",
        "ç": "c",
        "Ç": "c",
    }
)


def ilce_adini_norm(ad: str) -> str:
    temiz = turkce_kucuk_harf(ad).translate(_HARF_KATMA).strip()
    return _ILCE_TAKMA.get(temiz, temiz)


def resmi_ilce_adlari(sehir_anahtari: str) -> list[str]:
    return list(sehir_getir(sehir_anahtari).ilceler)


def ilce_adini_esle(osm_adi: str, resmi_adlar: list[str]) -> str | None:
    hedef = ilce_adini_norm(osm_adi)
    for resmi in resmi_adlar:
        if ilce_adini_norm(resmi) == hedef:
            return resmi
    return None


def kume_dogrula(eslesen: set[str], resmi_adlar: list[str]) -> dict[str, Any]:
    resmi = set(resmi_adlar)
    return {
        "eksik": sorted(resmi - eslesen),
        "fazla": sorted(eslesen - resmi),
        "tam": resmi == eslesen,
        "sayi": len(eslesen),
        "beklenen": len(resmi),
    }


def geojson_to_wkt(geometri: dict[str, Any]) -> str:
    tur = geometri.get("type")
    koordinatlar = geometri.get("coordinates")
    if tur == "Polygon":
        return f"MULTIPOLYGON({_polygon_wkt(koordinatlar)})"
    if tur == "MultiPolygon":
        ic = ",".join(_polygon_wkt(p) for p in koordinatlar)
        return f"MULTIPOLYGON({ic})"
    raise ValueError("yalniz Polygon/MultiPolygon kabul edilir")


def _polygon_wkt(rings: list[list[list[float]]]) -> str:
    parcalar = []
    for ring in rings:
        if not ring:
            continue
        kapanmis = ring if ring[0] == ring[-1] else [*ring, ring[0]]
        noktalar = ", ".join(f"{x} {y}" for x, y in kapanmis)
        parcalar.append(f"({noktalar})")
    return f"({', '.join(parcalar)})"


def overpass_ilce_sorgusu(iso_kod: str) -> str:
    return (
        f'[out:json][timeout:180];\n'
        f'area["ISO3166-2"="{iso_kod}"]->.sehir;\n'
        f'relation["boundary"="administrative"]["admin_level"="6"](area.sehir);\n'
        f"out tags geom;"
    )


def relation_geojson(element: dict[str, Any]) -> dict[str, Any] | None:
    uyeler = element.get("members") or []
    dis_halkalar: list[list[list[float]]] = []
    for uye in uyeler:
        if uye.get("type") != "way" or uye.get("role") == "inner":
            continue
        geometri = uye.get("geometry") or []
        if len(geometri) < 4:
            continue
        halka = [[nokta["lon"], nokta["lat"]] for nokta in geometri]
        if halka[0] != halka[-1]:
            halka.append(halka[0])
        dis_halkalar.append(halka)
    if not dis_halkalar:
        return None
    if len(dis_halkalar) == 1:
        return {"type": "Polygon", "coordinates": dis_halkalar}
    return {"type": "MultiPolygon", "coordinates": [[halka] for halka in dis_halkalar]}


def checksum_uret(deger: Any) -> str:
    ham = json.dumps(deger, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(ham.encode("utf-8")).hexdigest()


def ilce_kayitlarini_derle(
    elementler: list[dict[str, Any]],
    *,
    sehir_anahtari: str,
) -> dict[str, Any]:
    resmi = resmi_ilce_adlari(sehir_anahtari)
    kayitlar = []
    eslesen: set[str] = set()
    for element in elementler:
        if element.get("type") != "relation":
            continue
        etiketler = element.get("tags") or {}
        osm_adi = etiketler.get("name:tr") or etiketler.get("name")
        if not osm_adi:
            continue
        resmi_ad = ilce_adini_esle(osm_adi, resmi)
        geometri = relation_geojson(element)
        if resmi_ad is None or geometri is None:
            continue
        eslesen.add(resmi_ad)
        kayitlar.append(
            {
                "ilce_adi": resmi_ad,
                "kaynak": "openstreetmap",
                "kaynak_kayit_id": f"relation/{element['id']}",
                "veri_surumu": ILCE_SINIRI_SURUMU,
                "checksum": checksum_uret({"id": element["id"], "geom": geometri}),
                "geometri": geometri,
                "wkt": geojson_to_wkt(geometri),
                "cekilme_zamani": datetime.now(UTC).isoformat(),
                "provenance": {
                    "lisans": "ODbL",
                    "atif": "OpenStreetMap katkicilari",
                    "admin_level": "6",
                    "hgm_capraz_kontrol": HGM_CAPRAZ_KONTROL_NOTU,
                    "osm_name": osm_adi,
                },
            }
        )
    return {"kayitlar": kayitlar, "dogrulama": kume_dogrula(eslesen, resmi)}


def overpass_json(sorgu: str, *, timeout: int = 180) -> dict[str, Any]:
    import requests

    adresler = (
        "https://overpass.kumi.systems/api/interpreter",
        "https://overpass.private.coffee/api/interpreter",
        "https://overpass-api.de/api/interpreter",
    )
    son_hata: Exception | None = None
    for adres in adresler:
        try:
            yanit = requests.post(
                adres,
                data={"data": sorgu},
                headers={"User-Agent": "Samandira/25.2 (ilce-siniri; https://samandira.com)"},
                timeout=timeout,
            )
            if yanit.status_code == 200:
                return yanit.json()
            son_hata = RuntimeError(f"{adres} HTTP {yanit.status_code}")
            if yanit.status_code in {429, 504, 502} and timeout > 20:
                continue
        except Exception as hata:  # mirrors sirayla denenir
            son_hata = hata
    if son_hata is not None:
        raise son_hata
    raise RuntimeError("Overpass yanit vermedi")


def overpass_ilce_etiket_sorgusu(iso_kod: str) -> str:
    return (
        f'[out:json][timeout:90];\n'
        f'area["ISO3166-2"="{iso_kod}"]->.sehir;\n'
        f'relation["boundary"="administrative"]["admin_level"="6"](area.sehir);\n'
        f"out tags;"
    )


def overpass_relation_geom_sorgusu(relation_id: int) -> str:
    return f"[out:json][timeout:60];\nrel({relation_id});\nout geom;"


def nominatim_ilce_geojson(ilce_adi: str, sehir_ismi: str) -> dict[str, Any] | None:
    import time

    import requests

    time.sleep(1.1)
    yanit = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={
            "q": f"{ilce_adi}, {sehir_ismi}, Turkiye",
            "format": "json",
            "polygon_geojson": 1,
            "limit": 5,
            "accept-language": "tr",
        },
        headers={"User-Agent": "Samandira/25.2 (ilce-siniri; https://samandira.com)"},
        timeout=30,
    )
    yanit.raise_for_status()
    for oge in yanit.json():
        if oge.get("osm_type") != "relation" or oge.get("class") != "boundary":
            continue
        geometri = oge.get("geojson")
        if not isinstance(geometri, dict) or geometri.get("type") not in {"Polygon", "MultiPolygon"}:
            continue
        return oge
    return None


def ilceleri_cek(sehir_anahtari: str) -> dict[str, Any]:
    sehir = sehir_getir(sehir_anahtari)
    resmi = resmi_ilce_adlari(sehir_anahtari)
    kayitlar = []
    eslesen: set[str] = set()
    for resmi_ad in resmi:
        oge = nominatim_ilce_geojson(resmi_ad, sehir.isim)
        if oge is None:
            continue
        geometri = oge["geojson"]
        eslesen.add(resmi_ad)
        kayitlar.append(
            {
                "ilce_adi": resmi_ad,
                "kaynak": "openstreetmap",
                "kaynak_kayit_id": f"relation/{oge['osm_id']}",
                "veri_surumu": ILCE_SINIRI_SURUMU,
                "checksum": checksum_uret({"id": oge["osm_id"], "geom": geometri}),
                "geometri": geometri,
                "wkt": geojson_to_wkt(geometri),
                "cekilme_zamani": datetime.now(UTC).isoformat(),
                "provenance": {
                    "lisans": "ODbL",
                    "atif": "OpenStreetMap katkicilari",
                    "admin_level": "6",
                    "saglayici": "nominatim",
                    "hgm_capraz_kontrol": HGM_CAPRAZ_KONTROL_NOTU,
                    "osm_name": oge.get("name") or oge.get("display_name"),
                },
            }
        )
    return {"kayitlar": kayitlar, "dogrulama": kume_dogrula(eslesen, resmi)}
