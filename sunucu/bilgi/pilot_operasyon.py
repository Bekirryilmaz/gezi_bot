"""Pilot havuz, kuyruk triyaji ve grup inceleme CLI. Kor otomatik yayin yoktur."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from sunucu.admin.grup_inceleme import GRUP_AZAMI, grup_incelemeyi_uygula
from sunucu.admin.grup_kuyruk import grup_adaylarini_listele
from sunucu.admin.kuyruk_triyaj import inceleme_kuyrugunu_triyaj_et
from sunucu.auth.rbac import Yetki, yetkileri_birlestir
from sunucu.auth.servis import AdminBaglami, _rolleri_al, admin_olustur, oturum_ac
from sunucu.bilgi.pilot_havuzu import (
    gold_sec,
    havuz_ozeti,
    havuzu_sec,
    sehir_idsini_bul,
    veritabanindan_adaylar,
)
from sunucu.bilgi.pilot_kapsam import (
    havuz_kapsamini_kur,
    kuyruk_sayimi,
    matris_kolon_ozeti,
    nlp_kapsam_ozeti,
    rota_durum_ozeti,
    rota_simulasyonu,
    saat_durum_ozeti,
    sure_kaynak_ozeti,
    tarihi_neden_ozeti,
)
from sunucu.bilgi.resmi_saat import resmi_saatleri_isle
from sunucu.veritabani.admin_modelleri import AdminKullanici
from sunucu.veritabani.baglanti import OturumUretici

_AILE_SIRASI = (
    "calisma_saatleri",
    "wifi",
    "otopark",
    "acik_alan",
    "rezervasyon",
    "yer_turu",
    "telefon",
    "web_sitesi",
    "adres",
)


def _yayinci_baglam(oturum: Session) -> AdminBaglami:
    kullanicilar = oturum.query(AdminKullanici).filter_by(aktif_mi=True).all()
    for kullanici in kullanicilar:
        roller = _rolleri_al(oturum, kullanici.id)
        yetkiler = yetkileri_birlestir(set(roller))
        if Yetki.YAYINLA in yetkiler:
            kayit, _token, _csrf = oturum_ac(
                oturum, kullanici, ip=None, user_agent="pilot-operasyon"
            )
            return AdminBaglami(kullanici, kayit, roller, yetkiler)
    import secrets

    parola = secrets.token_urlsafe(18)
    kullanici = admin_olustur(
        oturum,
        eposta="faz254-operasyon@localhost",
        gorunen_ad="FAZ 25.4 operasyon",
        parola=parola + "Aa1",
        roller={"yonetici"},
    )
    roller = frozenset({"yonetici"})
    yetkiler = yetkileri_birlestir(set(roller))
    kayit, _token, _csrf = oturum_ac(oturum, kullanici, ip=None, user_agent="pilot-operasyon")
    return AdminBaglami(kullanici, kayit, roller, yetkiler)


def _rapor(oturum: Session, sehir_adi: str) -> dict[str, Any]:
    sehir_id = sehir_idsini_bul(oturum, sehir_adi)
    adaylar = veritabanindan_adaylar(oturum, sehir_id)
    havuz = havuzu_sec(adaylar)
    gold = gold_sec(havuz)
    kayitlar = havuz_kapsamini_kur(oturum, havuz, gold_idleri={a.sube_id for a in gold})
    return {
        "sehir": sehir_adi,
        "aday_havuz": len(adaylar),
        "kaliteli_aday": sum(1 for a in adaylar if a.puan >= 70),
        "havuz": havuz_ozeti(havuz),
        "gold_sayisi": len(gold),
        "gold_idleri": [a.sube_id for a in gold],
        "rota_durum": rota_durum_ozeti(kayitlar),
        "matris_ozet": matris_kolon_ozeti(kayitlar),
        "nlp": nlp_kapsam_ozeti(kayitlar),
        "saat_durum": saat_durum_ozeti(kayitlar),
        "sure_kaynak": sure_kaynak_ozeti(kayitlar),
        "tarihi": tarihi_neden_ozeti(kayitlar),
        "simulasyon": rota_simulasyonu(kayitlar),
        "kuyruk": kuyruk_sayimi(oturum),
        "kayitlar": kayitlar,
        "otomatik_yayin": False,
    }


def _grup_incele(
    oturum: Session,
    *,
    sehir_adi: str,
    yalniz_gold: bool,
    yalniz_pilot: bool,
    aile: str | None,
    yaz: bool,
    gerekce: str,
) -> dict[str, Any]:
    sehir_id = sehir_idsini_bul(oturum, sehir_adi)
    havuz = havuzu_sec(veritabanindan_adaylar(oturum, sehir_id))
    gold = gold_sec(havuz)
    if yalniz_gold:
        subeler = {a.sube_id for a in gold}
    elif yalniz_pilot:
        subeler = {a.sube_id for a in havuz}
    else:
        subeler = None
    aileler = (aile,) if aile else _AILE_SIRASI
    baglam = _yayinci_baglam(oturum) if yaz else None
    ozet: dict[str, Any] = {
        "onaylanan": 0,
        "atlanan": 0,
        "hatalar": 0,
        "aile": {},
        "otomatik_yayin": False,
    }
    for aile_kodu in aileler:
        adaylar = grup_adaylarini_listele(
            oturum, aile=aile_kodu, sube_idleri=subeler, yalniz_dusuk_risk=True
        )
        uygun_idleri = [a["dosya_id"] for a in adaylar if a["grup_uygun"]]
        ozet["aile"][aile_kodu] = {"aday": len(adaylar), "uygun": len(uygun_idleri)}
        if not yaz or not uygun_idleri:
            continue
        assert baglam is not None
        for bas in range(0, len(uygun_idleri), GRUP_AZAMI):
            parca = uygun_idleri[bas : bas + GRUP_AZAMI]
            sonuc = grup_incelemeyi_uygula(
                oturum,
                baglam=baglam,
                dosya_idleri=parca,
                gerekce=gerekce,
                istek_id=f"pilot-grup-{aile_kodu}-{bas}",
            )
            ozet["onaylanan"] += len(sonuc.onaylanan)
            ozet["atlanan"] += len(sonuc.atlanan)
            ozet["hatalar"] += len(sonuc.hatalar)
            ozet["aile"][aile_kodu]["onaylanan"] = ozet["aile"][aile_kodu].get(
                "onaylanan", 0
            ) + len(sonuc.onaylanan)
    return ozet


def main() -> None:
    parser = argparse.ArgumentParser(description="FAZ 25.5 rota kritik veri operasyonu")
    parser.add_argument("--sehir", default="Samsun")
    parser.add_argument("--rapor", action="store_true")
    parser.add_argument("--triyaj", action="store_true")
    parser.add_argument("--grup-inceleme", action="store_true")
    parser.add_argument("--resmi-saat", action="store_true")
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--gold", action="store_true")
    parser.add_argument("--aile", default=None)
    parser.add_argument("--yaz", action="store_true")
    parser.add_argument(
        "--gerekce",
        default=(
            "Pilot rota-kritik calisma saati resmi kaynak ve dusuk risk OSM "
            "adaylari incelendi; kor otomatik yayin yok."
        ),
    )
    parser.add_argument("--cikti", type=Path)
    args = parser.parse_args()
    with OturumUretici() as oturum:
        cikti: dict[str, Any] = {}
        sehir_id = sehir_idsini_bul(oturum, args.sehir)
        havuz = havuzu_sec(veritabanindan_adaylar(oturum, sehir_id))
        if args.triyaj:
            cikti["triyaj"] = inceleme_kuyrugunu_triyaj_et(
                oturum,
                dry_run=not args.yaz,
                pilot_sube_idleri={a.sube_id for a in havuz},
            )
        if args.resmi_saat:
            baglam = _yayinci_baglam(oturum) if args.yaz else None
            cikti["resmi_saat"] = resmi_saatleri_isle(
                oturum,
                baglam=baglam,
                havuz=havuz,
                yaz=args.yaz,
                gerekce=args.gerekce,
            )
        if args.grup_inceleme:
            cikti["grup_inceleme"] = _grup_incele(
                oturum,
                sehir_adi=args.sehir,
                yalniz_gold=args.gold,
                yalniz_pilot=args.pilot and not args.gold,
                aile=args.aile,
                yaz=args.yaz,
                gerekce=args.gerekce,
            )
        if args.rapor or not (args.triyaj or args.grup_inceleme or args.resmi_saat):
            cikti["rapor"] = _rapor(oturum, args.sehir)
            if "kayitlar" in cikti["rapor"] and args.cikti is None:
                ozet = dict(cikti["rapor"])
                ozet.pop("kayitlar", None)
                cikti["rapor_ozet"] = ozet
        if args.yaz:
            oturum.commit()
        metin = json.dumps(cikti, ensure_ascii=False, indent=2, default=str)
        if args.cikti:
            args.cikti.parent.mkdir(parents=True, exist_ok=True)
            args.cikti.write_text(metin + "\n", encoding="utf-8")
        goster = dict(cikti)
        if "rapor" in goster and "kayitlar" in goster["rapor"] and args.cikti is None:
            goster["rapor"] = {k: v for k, v in goster["rapor"].items() if k != "kayitlar"}
        print(json.dumps(goster, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
