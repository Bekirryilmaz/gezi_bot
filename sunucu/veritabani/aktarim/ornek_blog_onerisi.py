"""Tek seferlik: tum alanlari dolu, onayli ornek blog onerisi."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sunucu.api.mekan_onerileri_router import _oneri_yer_aktar
from sunucu.veritabani.baglanti import OturumUretici
from sunucu.veritabani.modeller import MekanOneri, OneriYorum

SLUG = "gizli-cinaralti-koyu-samsun-ornek"
GORSELLER = [
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1473116763249-2faaef81ccda?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=1600&q=80",
]


def calistir() -> str:
    oturum = OturumUretici()
    try:
        eski = oturum.query(MekanOneri).filter(MekanOneri.slug == SLUG).first()
        if eski:
            oturum.delete(eski)
            oturum.commit()

        kayit_id = str(uuid.uuid4())
        simdi = datetime.now(timezone.utc)
        oneri = MekanOneri(
            id=kayit_id,
            slug=SLUG,
            baslik="Gizli Çınaraltı Koyu",
            kategori="gizli_koy",
            sehir="Samsun",
            ilce="Atakum",
            aciklama=(
                "Sabah sis henüz dağılmamışken sahile indim. Tabelası yok, durak adı da yok; "
                "yalnızca çınarın gölgesinden denize süzülen dar bir patika var. Su berrak, "
                "kalabalık henüz uyanmamış. Termosumu kayalığa koyup yarım saat kimseyle "
                "konuşmadan oturdum. ŞAMANDIRA’da aradığım şey tam olarak buydu: haritada "
                "küçük, yerelde büyük bir sükûnet."
            ),
            ziyaretci_tuyosu="Gün doğumundan hemen sonra gel; öğleden sonra rüzgâr sertleşir ve kum uçar.",
            adres_tarifi=(
                "Atakum sahil yolunu batıya takip et. Çobanlı mezarlığı levhasından sonra "
                "ikinci toprak sapaktan sola in. Kırmızı boyalı kayığın yanındaki çınarın "
                "altından 400 metre yürü; koy kendiliğinden açılır."
            ),
            araba_erisimi="zor",
            yurume_mesafesi="Sapaktan koy ağzına 8-10 dk yürüme",
            yol_durumu="Toprak patika",
            toplu_tasima="22 numaralı otobüs Çobanlı durağında in; duraktan 15 dk yürüyüş.",
            enlem=41.3472,
            boylam=36.2481,
            fotograf_urlleri=GORSELLER,
            onayli_fotograflar=GORSELLER,
            begeni_sayisi=24,
            gorunur_tarif=True,
            gorunur_ulasim=True,
            gorunur_koordinat=True,
            gorunur_tuyo=True,
            tarih_baglam=(
                "Bu kıyı şeridi Osmanlı döneminde küçük sandal barınağı olarak anılırdı; "
                "çınar, köyün eski sınır ağacı sayılırmış. Yazılı bir kitabe yok ama "
                "yerliler hâlâ ‘çınaraltı iskelesi’ der."
            ),
            editor_notu=(
                "Kalabalıklaşmasın diye tam pin’i paylaşıyoruz ama lütfen çöp bırakma, "
                "müzik açma. Burası hâlâ mahallenin sabah çayı yeri."
            ),
            yayin_zamani=simdi,
            gonderen_eposta="ornek.kesif@samandira.local",
            durum="onaylandi",
        )
        oturum.add(oneri)
        oturum.flush()
        yer = _oneri_yer_aktar(oturum, oneri)
        oneri.yer_id = yer.id
        oturum.add(
            OneriYorum(
                oneri_id=oneri.id,
                yazar_adi="Elif Kaya",
                icerik="Geçen hafta gittim, tarif birebir tuttu. Çınarın altı gerçekten gölgeli; termos şart.",
                durum="yayinda",
            )
        )
        oturum.add(
            OneriYorum(
                oneri_id=oneri.id,
                yazar_adi="Mert Aydın",
                icerik="Toprak sapak yağmurdan sonra kaygan. Düşük tabanlı araba zorlanır, yürüyerek inmek daha rahat.",
                durum="yayinda",
            )
        )
        oturum.commit()
        return oneri.slug
    except Exception:
        oturum.rollback()
        raise
    finally:
        oturum.close()


if __name__ == "__main__":
    print(calistir())
