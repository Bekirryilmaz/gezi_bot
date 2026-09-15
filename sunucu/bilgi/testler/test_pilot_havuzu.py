from sunucu.bilgi.pilot_havuzu import PilotAday, gold_sec, havuzu_sec, kaliteli_mi


def _aday(**degisiklik) -> PilotAday:
    veri = dict(
        sube_id="s",
        yer_id="y",
        isim="Gunevi",
        alt_kategori="kafe",
        ilce_id="i",
        ilce_adi="Atakum",
        kimlik_sinifi="guclu",
        puan=150,
        amac="kahve_icmek",
        osm_aileleri=("wifi", "calisma_saatleri"),
        nlp_preference=2,
        public_claim=1,
        kahvalti=False,
        calisma=False,
        koordinat_gecerli=True,
    )
    veri.update(degisiklik)
    return PilotAday(**veri)


def test_karantina_internet_kafe_ve_dusuk_puan_kaliteli_degil():
    assert not kaliteli_mi(_aday(kimlik_sinifi="karantina", isim="."))
    assert not kaliteli_mi(_aday(alt_kategori="internet_kafe", amac=None))
    assert not kaliteli_mi(
        _aday(
            puan=10,
            kimlik_sinifi="kullanilabilir",
            osm_aileleri=(),
            nlp_preference=0,
            public_claim=0,
        )
    )
    assert kaliteli_mi(_aday())


def test_havuz_amac_kotasi_ve_zayif_kovayi_doldurmaz():
    kahveler = [
        _aday(
            sube_id=f"k{i}",
            yer_id=f"yk{i}",
            isim=f"Kafe {i}",
            ilce_adi="Atakum" if i < 10 else "Ilkadim",
        )
        for i in range(25)
    ]
    yemek = [
        _aday(
            sube_id=f"y{i}",
            yer_id=f"yy{i}",
            isim=f"Lokanta {i}",
            alt_kategori="restoran_lokanta",
            amac="yemek_yemek",
            ilce_adi="Ilkadim",
        )
        for i in range(8)
    ]
    zayif_eglence = [
        _aday(
            sube_id="e1",
            yer_id="ye1",
            isim="Tek salon",
            alt_kategori="eglence_aktivite",
            amac="eglence",
            puan=80,
            kimlik_sinifi="kullanilabilir",
            osm_aileleri=("wifi",),
            public_claim=0,
            nlp_preference=0,
        )
    ]
    havuz = havuzu_sec(kahveler + yemek + zayif_eglence)
    assert sum(1 for a in havuz if a.amac == "kahve_icmek") <= 18
    assert sum(1 for a in havuz if a.amac == "yemek_yemek") == 8
    assert not any(a.amac == "eglence" for a in havuz)
    gold = gold_sec(havuz)
    assert gold
    assert all(
        set(a.osm_aileleri) & {"calisma_saatleri", "wifi", "acik_alan", "otopark", "rezervasyon"}
        for a in gold
    )
    assert len(gold) <= 40
