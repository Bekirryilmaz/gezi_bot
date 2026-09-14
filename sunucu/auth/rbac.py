from __future__ import annotations

from enum import StrEnum


class Yetki(StrEnum):
    INCELEME_GOR = "inceleme_gor"
    KIMLIK_DUZENLE = "kimlik_duzenle"
    CLAIM_INCELE = "claim_incele"
    YAYINLA = "yayinla"
    GERI_CEK = "geri_cek"
    KRITIK_MERGE_SPLIT = "kritik_merge_split"
    AUDIT_GOR = "audit_gor"
    HAK_DEGISTIR = "hak_degistir"
    IKINCI_INCELE = "ikinci_incele"


ROL_YETKILERI: dict[str, frozenset[Yetki]] = {
    "gozlemci": frozenset({Yetki.INCELEME_GOR}),
    "kimlik_editoru": frozenset({Yetki.INCELEME_GOR, Yetki.KIMLIK_DUZENLE}),
    "claim_editoru": frozenset({Yetki.INCELEME_GOR, Yetki.CLAIM_INCELE}),
    "yayinci": frozenset({Yetki.INCELEME_GOR, Yetki.CLAIM_INCELE, Yetki.YAYINLA, Yetki.GERI_CEK}),
    "risk_onayci": frozenset({Yetki.INCELEME_GOR, Yetki.IKINCI_INCELE, Yetki.KRITIK_MERGE_SPLIT, Yetki.GERI_CEK, Yetki.YAYINLA, Yetki.HAK_DEGISTIR}),
    "auditor": frozenset({Yetki.INCELEME_GOR, Yetki.AUDIT_GOR}),
    "yonetici": frozenset(kanit for kanit in Yetki),
}

KRITIK_EYLEMLER = frozenset({"canonical_merge", "split", "kritik_claim_yayini", "withdraw", "hak_degisikligi"})


def yetkileri_birlestir(roller: set[str]) -> frozenset[Yetki]:
    sonuc: set[Yetki] = set()
    for rol in roller:
        sonuc.update(ROL_YETKILERI.get(rol, frozenset()))
    return frozenset(sonuc)
