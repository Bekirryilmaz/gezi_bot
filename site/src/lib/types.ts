export type Sehir = {
  id: string;
  anahtar: string;
  isim: string;
  plaka_kodu: string | null;
  bolge: string | null;
  merkez_enlem: number | null;
  merkez_boylam: number | null;
};

export type YerOzet = {
  id: string;
  isim: string;
  ana_kategori: string;
  alt_kategori: string;
  ilce: string | null;
  enlem: number;
  boylam: number;
  kaynakta_puan_ortalamasi: number | null;
  duygu_skoru_ortalama: number | null;
  kapak_fotografi_url: string | null;
};

export type YerListeCevabi = {
  yerler: YerOzet[];
  toplam_sayi: number;
};

export type OrnekYorum = {
  yazar_takma_adi: string | null;
  yorum_metni: string;
  kaynakta_puan: number | null;
  duygu_etiketi: string | null;
};

export type YerDetay = YerOzet & {
  adres: string | null;
  aciklama: string | null;
  tanitim_metni: string | null;
  telefon: string | null;
  web_sitesi: string | null;
  ozellikler: Record<string, unknown>;
  aktiviteler: string[];
  fotograf_urlleri: string[];
  deneyim_puanlari: Record<string, number>;
  yer_profili: Record<string, unknown>;
  duygu_ozeti: string | null;
  ornek_yorumlar: OrnekYorum[];
};

export type BolgeProfili = {
  bolge_adi: string;
  ilce_mi: boolean;
  genel_duygu_skoru: number | null;
  genel_duygu_etiketi: string | null;
  on_plana_cikan_konular: Array<{
    konu?: string;
    duygu_etiketi?: string;
    bahsedilme_sayisi?: number;
  }>;
  kullanilan_yorum_sayisi: number;
  duygu_ozeti: string | null;
  tanitim_metni: string | null;
};

export type RotaTercihleri = {
  ilgi_agirliklari?: Record<string, number>;
  aktiviteler?: string[];
  zorunlu_duraklar?: string[];
  ucuz_tercih_et?: boolean;
  sakin_tercih_et?: boolean;
};

export type RotaTalebi = {
  sehir_anahtari: string;
  gun_sayisi: number;
  konaklama_yer_id?: string | null;
  konaklama_enlem?: number | null;
  konaklama_boylam?: number | null;
  konaklama_bolge_adi?: string | null;
  alternatif_sayisi?: number;
  tercihler?: RotaTercihleri;
};

export type RotaDuragi = {
  yer: YerOzet;
  sira: number;
  onceki_duraktan_mesafe_metre: number;
  tahmini_ziyaret_suresi_dk: number;
  skor_kirilimi: Record<string, number>;
};

export type GunPlani = {
  gun_no: number;
  duraklar: RotaDuragi[];
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
