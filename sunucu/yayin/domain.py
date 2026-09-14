from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum

from sunucu.bilgi.domain import BilgiDurumu, HakDurumu


class YayinUygunlukDurumu(StrEnum):
    YAYINLANABILIR = "yayinlanabilir"
    SINIRLI_YAYINLANABILIR = "sinirli_yayinlanabilir"
    YAYINLANAMAZ = "yayinlanamaz"
    YENIDEN_DOGRULAMA_GEREKLI = "yeniden_dogrulama_gerekli"


class KullanimTuru(StrEnum):
    LISTE = "liste"
    DETAY = "detay"
    ARAMA = "arama"
    KESFET = "kesfet"
    ROTA_ADAYI = "rota_adayi"
    PAYLASIM = "paylasim"
    CACHE_PROJECTION = "cache_projection"
    KARAR = "karar"


class YayinNedeni(StrEnum):
    UYGUN = "uygun"
    SINIRLI_POLITIKA = "sinirli_politika"
    CANONICAL_GECERSIZ = "canonical_gecersiz"
    SUBE_GECERSIZ = "sube_gecersiz"
    IDDIA_PASIF = "iddia_pasif"
    SURUM_GECERSIZ = "surum_gecersiz"
    HAK_BILINMIYOR = "hak_bilinmiyor"
    HAK_UYGUN_DEGIL = "hak_uygun_degil"
    BILGI_BILINMIYOR = "bilgi_bilinmiyor"
    ESKIMIS = "eskimis"
    CELISKILI = "celiskili"
    GERI_CEKILMIS = "geri_cekilmis"
    ZAMAN_KAPSAMI_DISINDA = "zaman_kapsami_disinda"
    KULLANIM_IZNI_YOK = "kullanim_izni_yok"
    YAYIN_KAYDI_YOK = "yayin_kaydi_yok"


@dataclass(frozen=True)
class YayinGirdisi:
    canonical_gecerli: bool
    sube_gecerli: bool
    iddia_aktif: bool = True
    surum_gecerli: bool = True
    hak_durumu: HakDurumu = HakDurumu.IZINLI
    bilgi_durumu: BilgiDurumu = BilgiDurumu.BILINIYOR
    geri_cekilmis: bool = False
    gecerlilik_baslangici: datetime | None = None
    gecerlilik_bitisi: datetime | None = None
    izinli_kullanimlar: frozenset[KullanimTuru] = frozenset(KullanimTuru)
    sinirli: bool = False


@dataclass(frozen=True)
class YayinUygunlukSonucu:
    durum: YayinUygunlukDurumu
    nedenler: tuple[YayinNedeni, ...]
    kullanim_turu: KullanimTuru

    @property
    def kamusal_kullanilabilir(self) -> bool:
        return self.durum in {
            YayinUygunlukDurumu.YAYINLANABILIR,
            YayinUygunlukDurumu.SINIRLI_YAYINLANABILIR,
        }


def yayin_uygunlugunu_degerlendir(
    girdi: YayinGirdisi,
    kullanim_turu: KullanimTuru,
    *,
    simdi: datetime | None = None,
) -> YayinUygunlukSonucu:
    simdi = simdi or datetime.now(timezone.utc)
    nedenler: list[YayinNedeni] = []
    if not girdi.canonical_gecerli:
        nedenler.append(YayinNedeni.CANONICAL_GECERSIZ)
    if not girdi.sube_gecerli:
        nedenler.append(YayinNedeni.SUBE_GECERSIZ)
    if not girdi.iddia_aktif:
        nedenler.append(YayinNedeni.IDDIA_PASIF)
    if not girdi.surum_gecerli:
        nedenler.append(YayinNedeni.SURUM_GECERSIZ)
    if girdi.geri_cekilmis or girdi.bilgi_durumu is BilgiDurumu.GERI_CEKILMIS:
        nedenler.append(YayinNedeni.GERI_CEKILMIS)
    if girdi.hak_durumu is HakDurumu.BILINMIYOR:
        nedenler.append(YayinNedeni.HAK_BILINMIYOR)
    elif girdi.hak_durumu is not HakDurumu.IZINLI:
        nedenler.append(YayinNedeni.HAK_UYGUN_DEGIL)
    if girdi.bilgi_durumu is BilgiDurumu.BILINMIYOR:
        nedenler.append(YayinNedeni.BILGI_BILINMIYOR)
    elif girdi.bilgi_durumu is BilgiDurumu.ESKIMIS:
        nedenler.append(YayinNedeni.ESKIMIS)
    elif girdi.bilgi_durumu is BilgiDurumu.CELISKILI:
        nedenler.append(YayinNedeni.CELISKILI)
    if girdi.gecerlilik_baslangici and simdi < girdi.gecerlilik_baslangici:
        nedenler.append(YayinNedeni.ZAMAN_KAPSAMI_DISINDA)
    if girdi.gecerlilik_bitisi and simdi >= girdi.gecerlilik_bitisi:
        nedenler.append(YayinNedeni.ZAMAN_KAPSAMI_DISINDA)
    if kullanim_turu not in girdi.izinli_kullanimlar:
        nedenler.append(YayinNedeni.KULLANIM_IZNI_YOK)

    yeniden = {YayinNedeni.HAK_BILINMIYOR, YayinNedeni.BILGI_BILINMIYOR, YayinNedeni.ESKIMIS}
    if nedenler:
        durum = (
            YayinUygunlukDurumu.YENIDEN_DOGRULAMA_GEREKLI
            if set(nedenler).issubset(yeniden)
            else YayinUygunlukDurumu.YAYINLANAMAZ
        )
        return YayinUygunlukSonucu(durum, tuple(dict.fromkeys(nedenler)), kullanim_turu)
    if girdi.sinirli:
        return YayinUygunlukSonucu(
            YayinUygunlukDurumu.SINIRLI_YAYINLANABILIR,
            (YayinNedeni.SINIRLI_POLITIKA,),
            kullanim_turu,
        )
    return YayinUygunlukSonucu(YayinUygunlukDurumu.YAYINLANABILIR, (YayinNedeni.UYGUN,), kullanim_turu)
