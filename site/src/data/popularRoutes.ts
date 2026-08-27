export interface PopularRoute {
  id: string;
  title: string;
  category: "trekking" | "roadtrip" | "kultur_tren" | "doga_kanyon";
  badge: string;
  location: string;
  duration: string;
  distance: string;
  difficulty: "Kolay" | "Orta" | "Zor";
  summary: string;
  highlights: string[];
  bestSeason: string;
  imageUrl: string;
  startPoint: { name: string; coordinates: [number, number] };
  endPoint: { name: string; coordinates: [number, number] };
  pathCoordinates: Array<[number, number]>;
}

const u = (id: string, w = 1400) =>
  `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${w}&q=80`;

function hat(
  start: { name: string; coordinates: [number, number] },
  duraklar: Array<[number, number]>,
  end: { name: string; coordinates: [number, number] },
): Array<[number, number]> {
  return [start.coordinates, ...duraklar, end.coordinates];
}

const LIKYA_BAS = { name: "Fethiye / Ölüdeniz", coordinates: [36.5772, 29.1244] as [number, number] };
const LIKYA_BIT = { name: "Antalya / Geyikbayırı", coordinates: [36.8725, 30.4608] as [number, number] };
const KARYA_BAS = { name: "Muğla / Bozburun", coordinates: [36.6853, 28.0435] as [number, number] };
const KARYA_BIT = { name: "Aydın / Bafa Gölü", coordinates: [37.5028, 27.4239] as [number, number] };
const EKSPRES_BAS = { name: "Ankara Garı", coordinates: [39.936, 32.8427] as [number, number] };
const EKSPRES_BIT = { name: "Kars Garı", coordinates: [40.6074, 43.1006] as [number, number] };

export const POPULER_ROTALAR: PopularRoute[] = [
  {
    id: "likya-yolu",
    title: "Likya Yolu",
    category: "trekking",
    badge: "Dünyanın En İyi 10 Yürüyüş Yolu",
    location: "Muğla — Antalya",
    duration: "25–30 gün",
    distance: "540 km",
    difficulty: "Orta",
    summary:
      "Sunday Times’ın dünyanın en iyi 10 uzun mesafe yürüyüşünden saydığı antik Likya patikası.",
    highlights: ["Ölüdeniz", "Kelebekler Vadisi", "Patara", "Gelidonya Feneri"],
    bestSeason: "Nisan–Haziran & Eylül–Kasım",
    imageUrl: u("photo-1507525428034-b723cf961d3e"),
    startPoint: LIKYA_BAS,
    endPoint: LIKYA_BIT,
    pathCoordinates: hat(LIKYA_BAS, [
      [36.541, 29.123],
      [36.202, 29.637],
      [36.244, 29.985],
      [36.416, 30.478],
    ], LIKYA_BIT),
  },
  {
    id: "karya-yolu",
    title: "Karya Yolu",
    category: "trekking",
    badge: "En Uzun Kıyı Yürüyüşü",
    location: "Muğla — Aydın",
    duration: "40+ gün",
    distance: "820 km",
    difficulty: "Zor",
    summary:
      "Türkiye’nin en uzun kıyı yürüyüşü; Bozburun, Datça ve Gökova’nın el değmemiş koyları.",
    highlights: ["Bozburun", "Datça Yarımadası", "Gökova Körfezi"],
    bestSeason: "Mart–Mayıs & Ekim–Kasım",
    imageUrl: u("photo-1533105079780-92b9be482077"),
    startPoint: KARYA_BAS,
    endPoint: KARYA_BIT,
    pathCoordinates: hat(KARYA_BAS, [
      [36.737, 27.686],
      [36.855, 28.274],
      [37.04, 28.32],
      [37.38, 27.72],
    ], KARYA_BIT),
  },
  {
    id: "frig-yolu",
    title: "Frig Yolu",
    category: "trekking",
    badge: "Kültür Rotası",
    location: "Afyon — Ankara — Eskişehir — Kütahya",
    duration: "20–25 gün",
    distance: "506 km",
    difficulty: "Orta",
    summary:
      "Antik Frig Vadisi’nin kaya anıtları ve peri bacaları arasında uzanan ödüllü kültür patikası.",
    highlights: ["Frig Vadisi", "Kaya Anıtları", "Peri Bacaları"],
    bestSeason: "Nisan–Haziran & Eylül–Ekim",
    imageUrl: u("photo-1464822759023-fed622ff2c3b"),
    startPoint: { name: "Afyonkarahisar / Seydiler", coordinates: [38.87, 30.61] },
    endPoint: { name: "Gordion / Polatlı", coordinates: [39.647, 31.989] },
    pathCoordinates: [
      [38.87, 30.61],
      [39.201, 30.714],
      [39.444, 30.694],
      [39.55, 31.35],
      [39.647, 31.989],
    ],
  },
  {
    id: "dogu-karadeniz-yaylalar",
    title: "Doğu Karadeniz Yaylalar & Geçitler",
    category: "roadtrip",
    badge: "İkonik Doğa Sürüşü",
    location: "Trabzon — Rize — Artvin",
    duration: "4–6 gün",
    distance: "450 km",
    difficulty: "Orta",
    summary:
      "Fırtına Vadisi, Pokut–Huser bulut denizi, Ayder ve Kaçkar eteklerinde Türkiye’nin en görkemli doğa sürüşü.",
    highlights: ["Fırtına Vadisi", "Pokut & Huser", "Ayder", "Kaçkar"],
    bestSeason: "Haziran–Eylül",
    imageUrl: u("photo-1469474968028-56623f02e42e"),
    startPoint: { name: "Trabzon", coordinates: [41.0027, 39.7168] },
    endPoint: { name: "Artvin", coordinates: [41.1828, 41.8183] },
    pathCoordinates: [
      [41.0027, 39.7168],
      [40.619, 40.295],
      [41.02, 40.52],
      [40.958, 41.103],
      [41.1828, 41.8183],
    ],
  },
  {
    id: "kapadokya-ihlara",
    title: "Kapadokya Vadileri & Ihlara Kanyonu",
    category: "doga_kanyon",
    badge: "Volkanik Keşif",
    location: "Nevşehir — Aksaray",
    duration: "2–4 gün",
    distance: "35–60 km",
    difficulty: "Kolay",
    summary:
      "Peri bacaları, yeraltı şehirleri, Güvercinlik ve Aşk Vadisi boyunca eşsiz volkanik keşif.",
    highlights: ["Güvercinlik Vadisi", "Aşk Vadisi", "Ihlara Kanyonu"],
    bestSeason: "Nisan–Haziran & Eylül–Ekim",
    imageUrl: u("photo-1570939274717-7eda259b50ed"),
    startPoint: { name: "Göreme / Güvercinlik", coordinates: [38.6431, 34.8289] },
    endPoint: { name: "Ihlara Kanyonu", coordinates: [38.237, 34.307] },
    pathCoordinates: [
      [38.6431, 34.8289],
      [38.655, 34.84],
      [38.45, 34.55],
      [38.237, 34.307],
    ],
  },
  {
    id: "dogu-ekspresi",
    title: "Turistik Doğu Ekspresi & İpek Yolu",
    category: "kultur_tren",
    badge: "Kültür Rotası",
    location: "Ankara — Kars",
    duration: "24–26 saat",
    distance: "1.310 km",
    difficulty: "Kolay",
    summary:
      "Kemaliye Karanlık Kanyon, Çifte Minare ve Ani ile Türkiye’nin en popüler nostaljik tren yolculuğu.",
    highlights: ["Karanlık Kanyon", "Çifte Minare", "Ani Ören Yeri"],
    bestSeason: "Aralık–Mart (kış) & Nisan–Mayıs",
    imageUrl: u("photo-1474487548417-781cb714017f"),
    startPoint: EKSPRES_BAS,
    endPoint: EKSPRES_BIT,
    pathCoordinates: hat(EKSPRES_BAS, [
      [38.7312, 35.4787],
      [39.7477, 37.0179],
      [39.75, 39.5],
      [39.9043, 41.2679],
    ], EKSPRES_BIT),
  },
  {
    id: "kuzey-ege-kazdaglari",
    title: "Kuzey Ege & Kazdağları Sürüşü",
    category: "roadtrip",
    badge: "Manzaralı Yolculuk",
    location: "Çanakkale — Balıkesir",
    duration: "3–5 gün",
    distance: "320 km",
    difficulty: "Kolay",
    summary:
      "Adatepe, Yeşilyurt taş köyleri, Assos ve oksijen deposu Kazdağları Milli Parkı.",
    highlights: ["Adatepe", "Yeşilyurt", "Assos", "Kazdağları"],
    bestSeason: "Mayıs–Ekim",
    imageUrl: u("photo-1441974231531-c6227db76b6e"),
    startPoint: { name: "Çanakkale", coordinates: [40.1553, 26.4142] },
    endPoint: { name: "Balıkesir", coordinates: [39.6484, 27.8826] },
    pathCoordinates: [
      [40.1553, 26.4142],
      [39.488, 26.337],
      [39.566, 26.618],
      [39.7, 26.85],
      [39.6484, 27.8826],
    ],
  },
  {
    id: "st-paul-yolu",
    title: "St. Paul Yolu",
    category: "trekking",
    badge: "Tescilli Uzun Yürüyüş",
    location: "Antalya — Isparta / Eğirdir",
    duration: "20–27 gün",
    distance: "500 km",
    difficulty: "Zor",
    summary:
      "Türkiye’nin ikinci tescilli uzun yürüyüşü; Toroslar, Yazılı Kanyon ve Eğirdir Gölü manzaralı.",
    highlights: ["Toros Dağları", "Yazılı Kanyon", "Eğirdir Gölü"],
    bestSeason: "Nisan–Haziran & Eylül–Ekim",
    imageUrl: u("photo-1506905925346-21bda4d32df4"),
    startPoint: { name: "Antalya / Perge", coordinates: [36.961, 30.854] },
    endPoint: { name: "Eğirdir", coordinates: [37.8744, 30.8506] },
    pathCoordinates: [
      [36.961, 30.854],
      [37.15, 30.7],
      [37.48, 31.22],
      [37.8744, 30.8506],
    ],
  },
];
