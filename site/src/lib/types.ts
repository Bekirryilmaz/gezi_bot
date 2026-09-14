export type Sehir = {
  id: string;
  anahtar: string;
  isim: string;
  plaka_kodu: string | null;
  bolge: string | null;
  merkez_enlem: number | null;
  merkez_boylam: number | null;
};

export type SehirIstatistikleri = {
  sehir_anahtari: string;
  yer_sayisi: number;
  kesif_yer_sayisi: number;
  ilce_sayisi: number;
  bolge_profili_sayisi: number;
  deneyim_ekseni_sayisi: number;
};

export type YerOzet = {
  id: string;
  isim: string;
  ana_kategori: string;
  alt_kategori: string;
  ilce: string | null;
  enlem: number;
  boylam: number;
  kapak_fotografi_url: string | null;
  ticari_bildirim: "sponsorlu" | null;
};

export type YerListeCevabi = {
  yerler: YerOzet[];
  toplam_sayi: number;
};

export type YerDetay = YerOzet & {
  adres: string | null;
  aciklama: string | null;
  tanitim_metni: string | null;
  telefon: string | null;
  web_sitesi: string | null;
  aktiviteler: string[];
  fotograf_urlleri: string[];
};

export type BolgeProfili = {
  bolge_adi: string;
  ilce_mi: boolean;
  tanitim_metni: string | null;
  enlem?: number | null;
  boylam?: number | null;
};

export type RotaTercihleri = {
  ilgi_agirliklari?: Record<string, number>;
  aktiviteler?: string[];
  zorunlu_duraklar?: string[];
  ucuz_tercih_et?: boolean;
  sakin_tercih_et?: boolean;
};

export type GunlukPlanTalebi = {
  sehir_anahtari: string;
  tercihler?: RotaTercihleri;
};

export type GunlukPlanDuragi = {
  yer: YerOzet;
  sira: number;
  onceki_duraktan_mesafe_metre: number;
  tahmini_ziyaret_suresi_dk: number;
};

export type GunlukPlanCevap = {
  id: string;
  sehir_anahtari: string;
  duraklar: GunlukPlanDuragi[];
  toplam_mesafe_metre: number;
  toplam_sure_dakikasi: number;
  rota_tavsiyesi?: string | null;
};

/** Tarihsel rota kayitlarini okumak icin korunan, public akista kullanilmayan tipler. */
export type RotaTalebi = GunlukPlanTalebi & {
  gun_sayisi: number;
  konaklama_yer_id?: string | null;
  konaklama_enlem?: number | null;
  konaklama_boylam?: number | null;
  konaklama_bolge_adi?: string | null;
  alternatif_sayisi?: number;
};

export type GunPlani = {
  gun_no: number;
  duraklar: GunlukPlanDuragi[];
  toplam_mesafe_metre: number;
  toplam_sure_dakikasi: number;
};

export type KonaklamaBolgesiOnerisi = {
  bolge_adi: string;
  gerekce: string | null;
  enlem: number | null;
  boylam: number | null;
  ornek_konaklamalar: YerOzet[];
};

export type RotaCevap = {
  id: string;
  sehir_anahtari: string;
  gun_sayisi: number;
  gunler: GunPlani[];
  konaklama_onerisi: YerOzet | null;
  rota_tavsiyesi?: string | null;
  konaklama_bolgesi_onerisi?: KonaklamaBolgesiOnerisi | null;
  alternatif_etiketi?: string | null;
};

export type AlternatifRotalarCevap = {
  alternatifler: RotaCevap[];
};

export type ApiHataZarfi = {
  hata: {
    kod: string;
    mesaj: string;
    durum: "empty" | "insufficient" | "unavailable" | "error";
    request_id: string;
  };
};

export type VeriDurumu =
  "loading" | "empty" | "insufficient" | "unavailable" | "error" | "ready";
