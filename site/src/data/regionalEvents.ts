import type { RegionalEvent } from "@/types/events";

/** 2026–2027 dönemine göre mock festival takvimi (29 Ağustos 2026 civarı canlı/yakın örnekler içerir). */
export const REGIONAL_EVENTS: RegionalEvent[] = [
  {
    id: "samsun-kultur-yolu-2026",
    title: "Samsun Kültür Yolu Festivali",
    citySlug: "samsun",
    cityName: "Samsun",
    category: "kultur_sanat",
    startDate: "2026-08-22",
    endDate: "2026-09-07",
    summary:
      "Karadeniz’in sahil sahnesinde tiyatro, konser, sergi ve sokak sanatının buluştuğu Kültür Yolu durağı. Atakum sahili ve şehir merkezinde ücretsiz açık hava programları.",
    badge: "Kültür Yolu Festivali",
    imageUrl:
      "https://images.unsplash.com/photo-1492684223066-81342eea348d?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Ucretsiz",
  },
  {
    id: "bafra-kapikaya-2026",
    title: "Bafra Kapıkaya Doğa Sporları & Kültür Festivali",
    citySlug: "samsun",
    cityName: "Samsun",
    district: "Bafra",
    category: "doga_yayla",
    startDate: "2026-09-18",
    endDate: "2026-09-20",
    summary:
      "Kapıkaya kanyonunda trekking, rafting gösterileri ve Bafra’nın tütün-pirinç mutfağıyla iç içe yerel kültür şenliği.",
    badge: "Doğa & Kültür",
    imageUrl:
      "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Katılıma Açık",
  },
  {
    id: "adana-portakal-cicegi-2027",
    title: "Uluslararası Portakal Çiçeği Karnavalı",
    citySlug: "adana",
    cityName: "Adana",
    category: "geleneksel",
    startDate: "2027-04-03",
    endDate: "2027-04-06",
    summary:
      "Çukurova’nın bahar müjdecisi: kortej, sokak tiyatrosu ve portakal çiçeği kokulu karnaval. Adana’nın en renkli bahar ritüeli.",
    badge: "Uluslararası Festival",
    imageUrl:
      "https://images.unsplash.com/photo-1527529482837-4690079db1fe?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Ucretsiz",
  },
  {
    id: "adana-lezzet-2026",
    title: "Adana Lezzet Festivali",
    citySlug: "adana",
    cityName: "Adana",
    category: "gastronomi",
    startDate: "2026-10-02",
    endDate: "2026-10-05",
    summary:
      "Kebap, şalgam ve baharatın başkentinde açık hava tadım noktaları, usta sohbetleri ve sokak lezzeti parkurları.",
    badge: "Hasat Zamanı",
    imageUrl:
      "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Katılıma Açık",
  },
  {
    id: "alacati-ot-2027",
    title: "Alaçatı Ot Festivali",
    citySlug: "izmir",
    cityName: "İzmir",
    district: "Çeşme",
    category: "gastronomi",
    startDate: "2027-04-01",
    endDate: "2027-04-05",
    summary:
      "Ege’nin yabani ot mutfağı, taş sokaklarda atölyeler ve Alaçatı’nın bahar sofrası. Urla–Çeşme hattının en sevilen hasat şenliği.",
    badge: "Hasat Zamanı",
    imageUrl:
      "https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Katılıma Açık",
  },
  {
    id: "izmir-caz-2026",
    title: "İzmir Avrupa Caz Festivali",
    citySlug: "izmir",
    cityName: "İzmir",
    category: "muzik",
    startDate: "2026-10-08",
    endDate: "2026-10-18",
    summary:
      "Kordon’dan sahne salonlarına uzanan caz haftası. Avrupa’nın Ege durağında açık hava ve kulüp konserleri.",
    badge: "Müzik & Sahne",
    imageUrl:
      "https://images.unsplash.com/photo-1511192336575-5a79af67a986?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Biletli",
  },
  {
    id: "urla-enginar-2027",
    title: "Urla Enginar Festivali",
    citySlug: "izmir",
    cityName: "İzmir",
    district: "Urla",
    category: "gastronomi",
    startDate: "2027-04-18",
    endDate: "2027-04-20",
    summary:
      "Enginarın başkenti Urla’da üretici standları, şef gösterileri ve yarımadanın bahar bağ rotası.",
    badge: "Hasat Zamanı",
    imageUrl:
      "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Ucretsiz",
  },
  {
    id: "canakkale-kultur-yolu-2026",
    title: "Çanakkale Kültür Yolu Festivali",
    citySlug: "canakkale",
    cityName: "Çanakkale",
    category: "kultur_sanat",
    startDate: "2026-09-05",
    endDate: "2026-09-20",
    summary:
      "Troya’nın kapısında sahne sanatları, sergiler ve Boğaz kıyısında açık hava konserleri. Kültür Yolu’nun Çanakkale durağı.",
    badge: "Kültür Yolu Festivali",
    imageUrl:
      "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Ucretsiz",
  },
  {
    id: "bozcaada-bagbozumu-2026",
    title: "Bozcaada Bağbozumu Festivali",
    citySlug: "canakkale",
    cityName: "Çanakkale",
    district: "Bozcaada",
    category: "gastronomi",
    startDate: "2026-09-19",
    endDate: "2026-09-21",
    summary:
      "Ada bağlarında hasat, şarap tadımı ve Ege ezgileri. Bozcaada’nın en şiirsel sonbahar hafta sonu.",
    badge: "Hasat Zamanı",
    imageUrl:
      "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Biletli",
  },
  {
    id: "edirne-kirkpinar-2027",
    title: "Tarihi Kırkpınar Yağlı Güreşleri",
    citySlug: "edirne",
    cityName: "Edirne",
    category: "geleneksel",
    startDate: "2027-07-02",
    endDate: "2027-07-08",
    summary:
      "Dünyanın en eski spor şenliği: yağlı güreş, davul-zurna ve Edirne’nin festivale dönüşen yaz haftası.",
    badge: "Uluslararası Festival",
    imageUrl:
      "https://images.unsplash.com/photo-1540747913346-19e32dc3e7e5?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Katılıma Açık",
  },
  {
    id: "edirne-kakava-2027",
    title: "Kakava Hıdırellez Şenlikleri",
    citySlug: "edirne",
    cityName: "Edirne",
    district: "Sarayiçi",
    category: "geleneksel",
    startDate: "2027-05-05",
    endDate: "2027-05-06",
    summary:
      "Roman kültürünün bahar ateşi, Tunca kenarında müzik ve dilek ritüelleri. Trakya’nın en coşkulu Hıdırellez’i.",
    badge: "Geleneksel Şenlik",
    imageUrl:
      "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Ucretsiz",
  },
  {
    id: "ayder-kardan-adam-2027",
    title: "Ayder Kardan Adam Festivali",
    citySlug: "rize",
    cityName: "Rize",
    district: "Çamlıhemşin",
    category: "doga_yayla",
    startDate: "2027-02-14",
    endDate: "2027-02-16",
    summary:
      "Ayder Yaylası’nda kardan heykeller, kış sporları ve Hemşin kültürü. Karadeniz’in en sevimli kış şenliği.",
    badge: "Yayla Şenliği",
    imageUrl:
      "https://images.unsplash.com/photo-1483921020237-2ff51e8f4a90?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Katılıma Açık",
  },
  {
    id: "rize-yayla-senligi-2027",
    title: "Kaçkar Yayla Şenlikleri",
    citySlug: "rize",
    cityName: "Rize",
    district: "Çamlıhemşin",
    category: "doga_yayla",
    startDate: "2027-07-18",
    endDate: "2027-07-20",
    summary:
      "Yüksek yaylalarda horon, kemençe ve otantik sofra. Yazın Kaçkar eteklerinde geleneksel yayla buluşması.",
    badge: "Yayla Şenliği",
    imageUrl:
      "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Ucretsiz",
  },
  {
    id: "datca-badem-2027",
    title: "Datça Badem Çiçeği Festivali",
    citySlug: "mugla",
    cityName: "Muğla",
    district: "Datça",
    category: "gastronomi",
    startDate: "2027-02-07",
    endDate: "2027-02-09",
    summary:
      "Pembe-beyaz badem bahçelerinde yürüyüş, yerel ürün pazarları ve Datça’nın kış sonu bahar müjdesi.",
    badge: "Hasat Zamanı",
    imageUrl:
      "https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Ucretsiz",
  },
  {
    id: "mugla-lezzet-2026",
    title: "Muğla Lezzet Festivali",
    citySlug: "mugla",
    cityName: "Muğla",
    category: "gastronomi",
    startDate: "2026-10-10",
    endDate: "2026-10-12",
    summary:
      "Ege–Akdeniz mutfağının Muğla yorumu: zeytinyağı, balık ve yayla otları. İl genelinden üretici sofraları.",
    badge: "Hasat Zamanı",
    imageUrl:
      "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Katılıma Açık",
  },
  {
    id: "gastroantep-2026",
    title: "Uluslararası GastroAntep Festivali",
    citySlug: "gaziantep",
    cityName: "Gaziantep",
    category: "gastronomi",
    startDate: "2026-09-15",
    endDate: "2026-09-21",
    summary:
      "UNESCO gastronomi şehrinin uluslararası sofrası: baklava, kebap, Antep fıstığı ve dünya şeflerinin buluşması.",
    badge: "Uluslararası Festival",
    imageUrl:
      "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Biletli",
  },
  {
    id: "kapadokya-balon-cappadox-2026",
    title: "Kapadokya Balon Festivali (Cappadox)",
    citySlug: "nevsehir",
    cityName: "Nevşehir",
    district: "Kapadokya",
    category: "kultur_sanat",
    startDate: "2026-09-10",
    endDate: "2026-09-13",
    summary:
      "Peri bacaları üzerinde sıcak hava balonları, çağdaş sanat ve vadi konserleri. Kapadokya’nın eylül gökyüzü şenliği.",
    badge: "Uluslararası Festival",
    imageUrl:
      "https://images.unsplash.com/photo-1641128324972-af3212f0f6bd?auto=format&fit=crop&w=1200&q=80",
    ticketOrAccess: "Biletli",
  },
];
