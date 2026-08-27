import type { DistrictDetail } from "@/types/discovery";

const u = (id: string, w = 1200) =>
  `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${w}&q=80`;

const FOTO = {
  sahil: u("photo-1507525428034-b723cf961d3e"),
  delta: u("photo-1501785888041-af3ef285b470"),
  kus: u("photo-1444464666168-49d633b86797"),
  kale: u("photo-1552832230-c0197dd311b5"),
  magara: u("photo-1464822759023-fed622ff2c3b"),
  orman: u("photo-1441974231531-c6227db76b6e"),
  gol: u("photo-1439066615861-d1af74d74000"),
  sehir: u("photo-1480714378408-00b8d1e8e1c0"),
  vapur: u("photo-1544551763-46a013bb70d5"),
  teleferik: u("photo-1477959858617-67f85cf4f1df"),
  selale: u("photo-1432405977798-3b140da7e29f"),
  kanyon: u("photo-1506905925346-21bda4d32df4"),
  kaplica: u("photo-1544161515-4fd8dd21bc1c"),
  yayla: u("photo-1469474968028-56623f02e42e"),
  liman: u("photo-1520454974749-619e2b6b028c"),
  pide: u("photo-1513104890138-7c749659a591"),
  ekmek: u("photo-1509440159596-0249088772ff"),
  balik: u("photo-1559339352-11d035aa65de"),
  kahvalti: u("photo-1533089860892-a7c6f0a7ac25"),
  cay: u("photo-1576092768241-dec231879fc3"),
};

export const SAMSUN_ILCELERI: DistrictDetail[] = [
  {
    id: "atakum",
    name: "Atakum",
    slug: "atakum",
    coordinates: [41.34, 36.28],
    vibe: "Sahilin ve gün batımının adresi",
    highlights: {
      attractions: [
        { name: "Atakum Sahil Bandı", category: "sahil", desc: "Bisiklet ve gün batımı için kentin en işlek kıyı şeridi.", image: FOTO.sahil },
        { name: "Çobanlı Koyu", category: "sahil", desc: "Merkeze yakın, daha sakin bir deniz molası.", image: FOTO.liman },
      ],
      gastronomy: [
        { name: "Sahil balığı", desc: "Mevsim hamsi ve Karadeniz mezeleri.", image: FOTO.balik },
      ],
      travelTips: {
        tip: "Gün batımında sahil bandı; İlkadım’dan 15–25 dk.",
        bestTimeToVisit: "Mayıs–Eylül, akşam serinliğinde.",
        atmosphere: "Genç, hareketli, sahil-kent.",
        transport: "Dolmuş ve sahil yolu.",
      },
    },
  },
  {
    id: "ilkadim",
    name: "İlkadım",
    slug: "ilkadim",
    coordinates: [41.286, 36.33],
    vibe: "19 Mayıs’ın kalbi",
    highlights: {
      attractions: [
        { name: "Bandırma Vapuru ve Müze", category: "tarih", desc: "19 Mayıs’ın simgesi; kısa, yoğun bir ziyaret.", image: FOTO.vapur },
        { name: "Amisos Tepesi", category: "tarih", desc: "Antik mezar odaları ve kente bakış.", image: FOTO.kale },
      ],
      gastronomy: [
        { name: "Samsun pidesi", desc: "Kıymalı, kuşbaşılı, peynirli — merkez fırınlarında taze.", image: FOTO.pide },
      ],
      travelTips: {
        tip: "Öğleden önce müze ve çarşı; tramvay yürüyüş mesafesinde.",
        bestTimeToVisit: "Nisan–Haziran ve Eylül–Ekim.",
        atmosphere: "Tarihi merkez ve günlük şehir.",
        transport: "Otogar, tramvay, yürüme.",
      },
    },
  },
  {
    id: "canik",
    name: "Canik",
    slug: "canik",
    coordinates: [41.26, 36.34],
    vibe: "Tepeden Samsun",
    highlights: {
      attractions: [
        { name: "Samsun Teleferik", category: "kultur", desc: "Amisos–Batı Park hattı; deniz ve kent aynı karede.", image: FOTO.teleferik },
        { name: "Amisos Höyüğü", category: "tarih", desc: "Antik katmanlar, kısa trekking parkurları.", image: FOTO.kale },
      ],
      gastronomy: [
        { name: "Manzaralı kahvaltı", desc: "Tepelik kahvaltı evlerinde sakin bir sabah.", image: FOTO.kahvalti },
      ],
      travelTips: {
        tip: "Açık havada teleferik; sisli günde manzara kapanır.",
        bestTimeToVisit: "Açık ve rüzgârsız günler.",
        atmosphere: "Yamaç, seyir, sakin akşam.",
        transport: "İlkadım’dan kısa dolmuş veya teleferik.",
      },
    },
  },
  {
    id: "tekkekoy",
    name: "Tekkeköy",
    slug: "tekkekoy",
    coordinates: [41.21, 36.46],
    vibe: "Mağaraların gölgesi",
    highlights: {
      attractions: [
        { name: "Tekkeköy Mağaraları", category: "tarih", desc: "Prehistorik yerleşim izleri; kısa ve gölgeli bir yürüyüş.", image: FOTO.magara },
        { name: "Çınarlık orman içi", category: "doga", desc: "Piknik ve gölge arayanlar için.", image: FOTO.orman },
      ],
      gastronomy: [
        { name: "Köy kahvaltısı", desc: "Bal, kaymak, mısır ekmeği.", image: FOTO.kahvalti },
      ],
      travelTips: {
        tip: "Sabah erken mağaralar; Samsun–Ordu yolu üzerinde 20 dk.",
        bestTimeToVisit: "İlkbahar ve sonbahar.",
        atmosphere: "Yol üstü kültür molası.",
        transport: "Merkeze 20–25 dk.",
      },
    },
  },
  {
    id: "bafra",
    name: "Bafra",
    slug: "bafra",
    coordinates: [41.568, 35.907],
    vibe: "Deltanın ve Pidenin Başkenti",
    highlights: {
      attractions: [
        { name: "Kızılırmak Deltası Kuş Cenneti", category: "doga", desc: "Kuş göçü ve geniş ufuk; dürbün ve sabah ışığı şart.", image: FOTO.kus },
        { name: "Asarkale Kaya Mezarları", category: "tarih", desc: "Kayaya oyulmuş odalar; kısa bir tarih durağı.", image: FOTO.kale },
      ],
      gastronomy: [
        { name: "Çıtır Bafra Pidesi", desc: "Kapalı, uzun, kıymalı — ilçenin imzası.", image: FOTO.pide },
        { name: "Nokul", desc: "Cevizli, tarçınlı hamur tatlısı.", image: FOTO.ekmek },
      ],
      travelTips: {
        tip: "Kuşlar için şafak; pide öğle arası. Merkezden yaklaşık 1 saat.",
        bestTimeToVisit: "Nisan–Haziran (kuş göçü) ve Eylül.",
        atmosphere: "Ova, delta, taşra-kent.",
        transport: "Bafra otogarı düzenli sefer.",
      },
    },
  },
  {
    id: "carsamba",
    name: "Çarşamba",
    slug: "carsamba",
    coordinates: [41.199, 36.722],
    vibe: "Yeşilırmak ve pide ekolü",
    highlights: {
      attractions: [
        { name: "Yeşilırmak kenarı", category: "doga", desc: "Ova manzarası ve akşam yürüyüşü.", image: FOTO.delta },
        { name: "Çarşamba köprüleri", category: "kultur", desc: "Irmakla kurulan kentin iskeleti.", image: FOTO.sehir },
      ],
      gastronomy: [
        { name: "Çarşamba pidesi", desc: "Açık, yağlı, kıymalı — Bafra’dan ayrı bir ekol.", image: FOTO.pide },
      ],
      travelTips: {
        tip: "Öğle arası fırınlar; Samsun–Ünye yolu 40–50 dk.",
        bestTimeToVisit: "Yaz sonu ve sonbahar.",
        atmosphere: "Çarşı-pazar enerjisi.",
        transport: "Doğu sahil yolu.",
      },
    },
  },
  {
    id: "terme",
    name: "Terme",
    slug: "terme",
    coordinates: [41.209, 36.972],
    vibe: "Şelale ve Terme pidesi",
    highlights: {
      attractions: [
        { name: "Akalan Şelaleleri", category: "doga", desc: "Yağmur sonrası daha gür; kısa trekking.", image: FOTO.selale },
        { name: "Terme çarşısı", category: "kultur", desc: "Pide fırınları ve pazar günü kalabalığı.", image: FOTO.sehir },
      ],
      gastronomy: [
        { name: "Terme pidesi", desc: "İnce hamur, bol iç; üçüncü pide ekolü.", image: FOTO.pide },
      ],
      travelTips: {
        tip: "Şelale için yağış sonrası; Çarşamba üzerinden ~1 saat.",
        bestTimeToVisit: "Mayıs–Ekim.",
        atmosphere: "Küçük ilçe, doğa durakları.",
        transport: "Çarşamba aktarmalı.",
      },
    },
  },
  {
    id: "salipazari",
    name: "Salıpazarı",
    slug: "salipazari",
    coordinates: [41.083, 36.833],
    vibe: "Ormanın sessiz yüzü",
    highlights: {
      attractions: [
        { name: "Salıpazarı ormanları", category: "doga", desc: "Gölge, nem, kuş sesi — yaz kaçışı.", image: FOTO.orman },
        { name: "Dere kenarı", category: "doga", desc: "Hafta sonu piknik, yerel kalabalık.", image: FOTO.delta },
      ],
      gastronomy: [
        { name: "Mısır ekmeği", desc: "Köy fırınında, tereyağıyla.", image: FOTO.ekmek },
      ],
      travelTips: {
        tip: "Sabah erken orman; Çarşamba’dan özel araç daha rahat.",
        bestTimeToVisit: "Haziran–Eylül.",
        atmosphere: "Sakin, yeşil, yağmurlu.",
        transport: "İç hat, virajlı yol.",
      },
    },
  },
  {
    id: "ayvacik",
    name: "Ayvacık",
    slug: "ayvacik",
    coordinates: [40.991, 36.631],
    vibe: "Baraj gölünün sakinliği",
    highlights: {
      attractions: [
        { name: "Suat Uğurlu Barajı", category: "doga", desc: "Göl kenarı seyir ve fotoğraf.", image: FOTO.gol },
        { name: "Yeşilırmak vadisi", category: "doga", desc: "Dar vadi, sisli sabahlar.", image: FOTO.delta },
      ],
      gastronomy: [
        { name: "Alabalık", desc: "Baraj çevresinde taze ızgara.", image: FOTO.balik },
      ],
      travelTips: {
        tip: "Öğleden önce göl; Çarşamba–Ayvacık virajlı yolu.",
        bestTimeToVisit: "Yaz ve erken sonbahar.",
        atmosphere: "Kırsal, sakin.",
        transport: "Özel araç önerilir.",
      },
    },
  },
  {
    id: "vezirkopru",
    name: "Vezirköprü",
    slug: "vezirkopru",
    coordinates: [41.143, 35.455],
    vibe: "Kanyonun eşiği",
    highlights: {
      attractions: [
        { name: "Şahinkaya Kanyonu", category: "doga", desc: "Tekne veya seyir terası; günübirlik en güçlü durak.", image: FOTO.kanyon },
        { name: "Kunduz ormanları", category: "doga", desc: "Gölgeli yürüyüş, kamp potansiyeli.", image: FOTO.orman },
      ],
      gastronomy: [
        { name: "Közde et", desc: "Kanyon tesislerinde doyurucu öğle.", image: FOTO.kahvalti },
      ],
      travelTips: {
        tip: "Açık ve durgun havada kanyon; Samsun’dan ~1,5 saat, özel araç.",
        bestTimeToVisit: "Mayıs–Ekim.",
        atmosphere: "Doğa ağırlıklı.",
        transport: "Özel araç.",
      },
    },
  },
  {
    id: "havza",
    name: "Havza",
    slug: "havza",
    coordinates: [40.971, 35.662],
    vibe: "Kaplıcanın buharı",
    highlights: {
      attractions: [
        { name: "Havza kaplıcaları", category: "kultur", desc: "Termal oteller ve hamam kültürü.", image: FOTO.kaplica },
        { name: "Havza evleri", category: "tarih", desc: "Kurtuluş yıllarının izini süren sokaklar.", image: FOTO.sehir },
      ],
      gastronomy: [
        { name: "Kaplıca kahvaltısı", desc: "Yöresel peynir ve bal.", image: FOTO.kahvalti },
      ],
      travelTips: {
        tip: "Kış sezonu kaplıca; Samsun–Ankara istikameti ~1,5 saat.",
        bestTimeToVisit: "Kasım–Mart.",
        atmosphere: "Dinlenme, aile.",
        transport: "D795 güzergâhı.",
      },
    },
  },
  {
    id: "kavak",
    name: "Kavak",
    slug: "kavak",
    coordinates: [41.078, 36.04],
    vibe: "Sahil ile yayla arası",
    highlights: {
      attractions: [
        { name: "Kavak geçidi", category: "doga", desc: "Sis ve yamaç; kısa bir fotoğraf durağı.", image: FOTO.yayla },
        { name: "Köy yolları", category: "doga", desc: "Kısa sapmalarla yayla hissi.", image: FOTO.orman },
      ],
      gastronomy: [
        { name: "Yol üstü pide", desc: "Transit yolcunun klasiği.", image: FOTO.pide },
      ],
      travelTips: {
        tip: "Çay molası için dur; merkeze ~45 dk, D795 üzerinde.",
        bestTimeToVisit: "Yaz öğleden sonraları.",
        atmosphere: "Küçük geçiş ilçesi.",
        transport: "Ana yol üzeri.",
      },
    },
  },
  {
    id: "ladik",
    name: "Ladik",
    slug: "ladik",
    coordinates: [40.911, 35.892],
    vibe: "Göl ve yayla",
    highlights: {
      attractions: [
        { name: "Ladik Gölü", category: "doga", desc: "Kuşlar, ayna su; kışın buz kenarı.", image: FOTO.gol },
        { name: "Ladik yaylaları", category: "doga", desc: "Yaz serinliği, kısa trekking.", image: FOTO.yayla },
      ],
      gastronomy: [
        { name: "Yayla kahvaltısı", desc: "Tereyağı, bal, mısır ekmeği.", image: FOTO.kahvalti },
      ],
      travelTips: {
        tip: "Sabah sisinde göl; Havza veya Kavak üzerinden özel araç.",
        bestTimeToVisit: "Haziran–Eylül.",
        atmosphere: "Sakin, yayla.",
        transport: "Özel araç.",
      },
    },
  },
  {
    id: "alacam",
    name: "Alaçam",
    slug: "alacam",
    coordinates: [41.61, 35.595],
    vibe: "Batı kıyının sakin duruşu",
    highlights: {
      attractions: [
        { name: "Alaçam sahili", category: "sahil", desc: "Kalabalıksız Karadeniz kumu.", image: FOTO.sahil },
        { name: "Dürtün ormanları", category: "doga", desc: "Gölgeli yürüyüş ve piknik.", image: FOTO.orman },
      ],
      gastronomy: [
        { name: "Sezon hamsi", desc: "Sonbahar–kış, ızgara veya buğulama.", image: FOTO.balik },
      ],
      travelTips: {
        tip: "Hafta içi sahil boş; Bafra üzerinden kıyı yolu ~1,5 saat.",
        bestTimeToVisit: "Haziran–Eylül.",
        atmosphere: "Sakin, yerel.",
        transport: "Bafra aktarmalı.",
      },
    },
  },
  {
    id: "yakakent",
    name: "Yakakent",
    slug: "yakakent",
    coordinates: [41.633, 35.455],
    vibe: "Küçük liman, büyük ufuk",
    highlights: {
      attractions: [
        { name: "Çeşmeönü sahili", category: "sahil", desc: "Dar, temiz; gün batımına açık.", image: FOTO.sahil },
        { name: "Yakakent limanı", category: "kultur", desc: "Tekneler, martılar, kısa bir tur.", image: FOTO.liman },
      ],
      gastronomy: [
        { name: "Günün avı", desc: "Az süs, tuz ve limon.", image: FOTO.balik },
      ],
      travelTips: {
        tip: "Akşam Çeşmeönü; Alaçam kıyısından, merkeze ~2 saat.",
        bestTimeToVisit: "Temmuz–Ağustos, hafta içi.",
        atmosphere: "Balıkçı kasabası ritmi.",
        transport: "Kıyı yolu.",
      },
    },
  },
  {
    id: "19-mayis",
    name: "19 Mayıs",
    slug: "19-mayis",
    coordinates: [41.512, 36.085],
    vibe: "Kırsal sahilin nefesi",
    highlights: {
      attractions: [
        { name: "Engiz sahili", category: "sahil", desc: "Sakin, yerel plaj; yazlık hissi.", image: FOTO.sahil },
        { name: "Ballıca çevresi", category: "doga", desc: "Köy peyzajı, tarla ve ufuk.", image: FOTO.yayla },
      ],
      gastronomy: [
        { name: "Köy pidesi", desc: "Fırınlar az, lezzet dürüst.", image: FOTO.pide },
      ],
      travelTips: {
        tip: "Yaz öğleden sonra Engiz; Samsun–Bafra sapakları 40–50 dk.",
        bestTimeToVisit: "Haziran–Eylül.",
        atmosphere: "Kırsal sahil.",
        transport: "Bafra yolu sapakları.",
      },
    },
  },
  {
    id: "asarcik",
    name: "Asarcık",
    slug: "asarcik",
    coordinates: [41.033, 36.235],
    vibe: "Yayla havası",
    highlights: {
      attractions: [
        { name: "Asarcık yaylaları", category: "doga", desc: "Yaz serinliği, geniş ufuk.", image: FOTO.yayla },
        { name: "Köy manzaraları", category: "doga", desc: "Dürüst kareler, vitrin yok.", image: FOTO.orman },
      ],
      gastronomy: [
        { name: "Yayla kahvaltısı", desc: "Bal, kaymak, mısır ekmeği.", image: FOTO.kahvalti },
      ],
      travelTips: {
        tip: "Yaz sabahı yayla; Kavak/Çarşamba bağlantılı, özel araç şart.",
        bestTimeToVisit: "Temmuz–Ağustos.",
        atmosphere: "Kırsal, konaklama sınırlı.",
        transport: "Özel araç.",
      },
    },
  },
];
