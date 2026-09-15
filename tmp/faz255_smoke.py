import json
import urllib.request


def getir(url: str) -> int:
    with urllib.request.urlopen(url, timeout=20) as yanit:
        return yanit.status


def gonder(url: str, govde: dict) -> tuple[int, dict]:
    istek = urllib.request.Request(
        url,
        data=json.dumps(govde).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(istek, timeout=60) as yanit:
        return yanit.status, json.loads(yanit.read())


print("docs", getir("https://qk4cmqnw-8125.euw.devtunnels.ms/docs"))
print("localdocs", getir("http://127.0.0.1:8125/docs"))

for etiket, metin in (
    ("kahve", "Samsun'da bugun kahve icmek istiyorum."),
    ("tarih", "Samsun'da tarihi yer gezmek istiyorum."),
    ("yemek", "Samsun'da yemek yemek istiyorum."),
):
    durum_kodu, cevap = gonder(
        "http://127.0.0.1:8125/v1/bugun-ne-yapalim",
        {"serbest_metin": metin, "niyet": {"sehir": "Samsun"}},
    )
    adlar = []
    kesfet = cevap.get("kesfet") or {}
    for secenek in kesfet.get("secenekler") or []:
        yer = secenek.get("yer") or {}
        adlar.append(yer.get("ad") or yer.get("isim"))
    print(etiket, durum_kodu, cevap.get("durum"), adlar[:6], "n=", len(adlar))
