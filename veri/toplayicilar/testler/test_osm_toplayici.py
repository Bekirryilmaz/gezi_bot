from veri.toplayicilar.osm_toplayici import (
    _elementi_yere_donustur,
    kaynak_idlerini_ayir,
    osm_etiketini_koru,
)
from sunucu.bilgi.osm_ozellik_servisi import ozellikleri_birlestir


def test_osm_limited_required_yes_no_birbirine_cevrilmez():
    assert osm_etiketini_koru("wheelchair", "limited") == "limited"
    assert osm_etiketini_koru("reservation", "required") == "required"
    assert osm_etiketini_koru("wheelchair", "yes") == "yes"
    assert osm_etiketini_koru("wheelchair", "customers") is None
    assert osm_etiketini_koru("parking", "unknown") is None


def test_osm_yapilandirilmis_etiketler_ozelliklere_ve_booleanlara_ayrilir():
    element = {
        "type": "node",
        "id": 1,
        "lat": 41.3,
        "lon": 36.3,
        "tags": {
            "name": "Sentetik Kafe",
            "amenity": "cafe",
            "wheelchair": "limited",
            "internet_access": "wlan",
            "outdoor_seating": "yes",
            "parking": "no",
            "reservation": "required",
            "opening_hours": "Mo-Su 08:00-22:00",
            "socket": "yes",
            "cuisine": "coffee_shop",
            "fee": "no",
            "phone": "+90 362 000 00 00",
            "website": "https://example.org",
        },
    }
    yer = _elementi_yere_donustur(element, "Samsun")
    assert yer is not None
    oz = yer.ozellikler
    assert oz.engelli_erisimi is None
    assert oz.wheelchair == "limited"
    assert oz.wifi is True
    assert oz.internet_access == "wlan"
    assert oz.acik_alan is True
    assert oz.outdoor_seating == "yes"
    assert oz.otopark is False
    assert oz.parking == "no"
    assert oz.rezervasyon_gerekli is None
    assert oz.reservation == "required"
    assert oz.opening_hours == "Mo-Su 08:00-22:00"
    assert oz.socket == "yes"
    assert oz.cuisine == "coffee_shop"
    assert oz.ucretsiz is True
    assert oz.fee == "no"
    assert yer.telefon == "+90 362 000 00 00"
    assert yer.web_sitesi == "https://example.org"


def test_osm_kaynak_id_ayrimi_ve_ozellik_birlestirme_limited_korur():
    gruplar = kaynak_idlerini_ayir(["node/1", "way/2", "ilgici/3", "node/x"])
    assert gruplar["node"] == [1]
    assert gruplar["way"] == [2]
    assert gruplar["relation"] == []
    birlesik = ozellikleri_birlestir({"wifi": True, "hakkinda": "eski"}, {"wheelchair": "limited", "wifi": False})
    assert birlesik["wheelchair"] == "limited"
    assert birlesik["wifi"] is False
    assert birlesik["hakkinda"] == "eski"
