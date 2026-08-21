"""Rota icin sablon tabanli tavsiye / ozet metni (LLM yok)."""

from __future__ import annotations

from sunucu.rota_motoru.veri_tipleri import RotaSonucu, RotaTercihleri


def rota_tavsiyesi_uret(
    rota: RotaSonucu,
    tercihler: RotaTercihleri | None = None,
    konaklama_bolgesi: str | None = None,
) -> str:
    gun_sayisi = len(rota.gunler)
    toplam_mesafe = sum(g.toplam_mesafe_metre for g in rota.gunler)
    ortalama_gunluk_km = (toplam_mesafe / 1000) / max(gun_sayisi, 1)
    toplam_durak = sum(len(g.duraklar) for g in rota.gunler)

    cumleler: list[str] = [
        f"Bu rota {gun_sayisi} güne yayılmış {toplam_durak} duraktan oluşuyor; "
        f"günlük ortalama yaklaşık {ortalama_gunluk_km:.0f} km yol içeriyor."
    ]

    if ortalama_gunluk_km >= 25:
        cumleler.append(
            "Mesafeler biraz açık; arabanız varsa veya gün içi taksi/ulaşım planı yaparsanız daha rahat edilir."
        )
    elif ortalama_gunluk_km <= 8:
        cumleler.append(
            "Duraklar birbirine yakın; yürüyerek veya kısa mesafeli toplu taşımayla da yönetilebilir bir tempo."
        )
    else:
        cumleler.append(
            "Mesafe dengeli; bir gün yürüyüş + bir gün araç karışımıyla rahatlıkla tamamlanabilir."
        )

    if tercihler:
        if tercihler.sakin_tercih_et:
            cumleler.append("Sakinlik tercihin dikkate alındı; kalabalık eğilimli duraklar mümkün olduğunca geri planda bırakıldı.")
        if tercihler.ucuz_tercih_et:
            cumleler.append("Bütçe dostu yerler önceliklendirildi; yine de menü/giriş ücretlerini yerinde doğrula.")
        if tercihler.ilgi_agirliklari:
            en_guclu = max(tercihler.ilgi_agirliklari.items(), key=lambda kv: kv[1])
            etiket = en_guclu[0].replace("_puani", "").replace("_", " ")
            cumleler.append(f"Rotanın omurgası özellikle “{etiket}” ilgi alanına yaslanıyor.")

    if konaklama_bolgesi:
        cumleler.append(
            f"Konaklama için “{konaklama_bolgesi}” bandı, seçtiğin günlerin durak merkezine en uygun bölge olarak öne çıkıyor."
        )

    return " ".join(cumleler)


def konaklama_bolgesi_gerekce_uret(bolge_adi: str, durak_sayisi: int) -> str:
    return (
        f"Seçilen rotadaki {durak_sayisi} durağın coğrafi dağılımına bakıldığında "
        f"“{bolge_adi}” konaklama bölgesi günleri en az dağınık şekilde bağlamana yardımcı olur. "
        f"Burada bir tesis seçmek, sabah çıkışlarını ve akşam dönüşlerini kısaltır."
    )
