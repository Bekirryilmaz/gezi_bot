from veri.cografya.ilce_siniri import (
    geojson_to_wkt,
    ilce_adini_esle,
    ilce_kayitlarini_derle,
    kume_dogrula,
    resmi_ilce_adlari,
)


def test_samsun_resmi_ilce_kumesi_17dir():
    adlar = resmi_ilce_adlari("samsun")
    assert len(adlar) == 17
    assert "Atakum" in adlar
    assert "19 Mayıs" in adlar


def test_ilce_adi_takma_ve_eksik_fazla_dogrulanir():
    resmi = resmi_ilce_adlari("samsun")
    assert ilce_adini_esle("Ondokuzmayıs", resmi) == "19 Mayıs"
    assert ilce_adini_esle("Atakum", resmi) == "Atakum"
    assert ilce_adini_esle("Olmayan", resmi) is None
    rapor = kume_dogrula({"Atakum"}, resmi)
    assert rapor["tam"] is False
    assert "İlkadım" in rapor["eksik"] or "Ilkadim" in {x.replace("İ", "I") for x in rapor["eksik"]}
    assert rapor["beklenen"] == 17


def test_geojson_polygon_multipolygon_wkt_uretir():
    wkt = geojson_to_wkt(
        {"type": "Polygon", "coordinates": [[[36.0, 41.0], [36.2, 41.0], [36.2, 41.2], [36.0, 41.2], [36.0, 41.0]]]}
    )
    assert wkt.startswith("MULTIPOLYGON")
    assert "36.0 41.0" in wkt


def test_relation_dis_ring_ilce_kaydina_donusur():
    element = {
        "type": "relation",
        "id": 12345,
        "tags": {"name": "Atakum", "admin_level": "6", "boundary": "administrative"},
        "members": [
            {
                "type": "way",
                "role": "outer",
                "geometry": [
                    {"lon": 36.0, "lat": 41.0},
                    {"lon": 36.2, "lat": 41.0},
                    {"lon": 36.2, "lat": 41.2},
                    {"lon": 36.0, "lat": 41.2},
                    {"lon": 36.0, "lat": 41.0},
                ],
            }
        ],
    }
    derleme = ilce_kayitlarini_derle([element], sehir_anahtari="samsun")
    assert derleme["kayitlar"][0]["ilce_adi"] == "Atakum"
    assert derleme["kayitlar"][0]["kaynak_kayit_id"] == "relation/12345"
    assert derleme["dogrulama"]["tam"] is False
