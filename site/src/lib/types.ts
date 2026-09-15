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

export type KararSonucuTuru =
  | "onerilebilir"
  | "kosula_bagli_onerilebilir"
  | "ihtiyacla_uyusmuyor"
  | "kritik_bilgi_bilinmiyor"
  | "kapsam_disi"
  | "netlestirme_gerekli"
  | "servis_gecici_kullanilamiyor";

export type KararUygunlugu = "uygun" | "uygun_degil" | "degerlendirilemiyor";

export type KararGerekcesi = {
  kod: string;
  mesaj: string;
  ilgili_kosul: string | null;
};

export type KararSonucu = {
  karar_id: string;
  yer: {
    place_id: string;
    canonical_id: string;
    branch_id: string;
    isim: string;
  } | null;
  karar_turu: KararSonucuTuru;
  anlasilan_ihtiyac: Record<string, unknown>;
  uygunluk: KararUygunlugu;
  gerekceler: KararGerekcesi[];
  kritik_engeller: KararGerekcesi[];
  onemli_odunler: KararGerekcesi[];
  bilinmeyenler: KararGerekcesi[];
  zaman_ve_kapsam: Record<string, unknown>;
  bilgi_surumu: string;
  politika_surumu: string;
  yayin_surumu: number | null;
  anlamli_alternatif_farki: string | null;
  trace_reference: string | null;
};

export type KararDegerlendirmeCevabi = {
  sonuclar: KararSonucu[];
  trace_reference: string;
};

export type KosulDurumu = "uygun" | "uygun_degil" | "degerlendirilemiyor";

export type AramaSonucuTuru =
  "yer_kimligi" | "kategori" | "sehir" | "ilce" | "baglamsal_aday";

export type AramaCografya = {
  sehir_id: string;
  sehir_anahtari: string;
  sehir_ismi: string;
  ilce_id: string | null;
  ilce_ismi: string | null;
};

export type AramaSonucu = {
  sonuc_turu: AramaSonucuTuru;
  etiket: string;
  yer: {
    place_id: string;
    canonical_id: string;
    branch_id: string;
    isim: string;
  } | null;
  cografya: AramaCografya;
  ana_kategori: string | null;
  alt_kategori: string | null;
  eslesme_nedeni:
    | "tam_ad"
    | "ad_baslangici"
    | "yazim_yakinligi"
    | "kategori"
    | "sehir"
    | "ilce"
    | "baglam";
  yayin_durumu: "yayinda";
  kosul_durumlari: Record<string, KosulDurumu>;
};

export type AramaFiltreDurumu = {
  sehir: string;
  ilce: string | null;
  tur: string | null;
  zorunluKosullar: string[];
  tercihler: string[];
};

export type AramaCevabi = {
  sorgu: string;
  sonuclar: AramaSonucu[];
  uygulanan_filtreler: {
    sehir_id: string;
    ilce_id: string | null;
    tur: string | null;
    cografi_baglam: { sehir: string; ilce: string | null; alan: string | null };
    zorunlu_kosullar: Array<Record<string, unknown>>;
    tercihler: Array<Record<string, unknown>>;
  };
  sonraki_cursor: string | null;
  degerlendirilemeyen_aday_sayisi: number;
};

export type AramaFiltreKatalogu = {
  sehir_id: string;
  sehir_anahtari: string;
  ilceler: Array<{ id: string; isim: string; sehir_id: string }>;
  turler: Array<{ kod: string; etiket: string }>;
  somut_kosullar: Array<{ kod: string; etiket: string; iddia_ailesi: string }>;
};

export type KararBaglami = {
  amac: string | null;
  cografi_baglam: { sehir: string; ilce: string | null; alan: string | null };
  zaman?: {
    ziyaret_tarihi?: string | null;
    baslangic?: string | null;
    bitis?: string | null;
    degerlendirme_zamani?: string | null;
  };
  ulasim_bicimi?: string | null;
  butce_ust_siniri?: number | null;
  sure_ust_siniri_dakika?: number | null;
  zorunlu_kosullar?: Array<Record<string, unknown>>;
  tercihler?: Array<Record<string, unknown>>;
  reddedilen_yerler?: string[];
  sabitlenen_yerler?: string[];
  anlasilmayan_kritik_girdiler?: string[];
  bilgi_surumu?: string;
  politika_surumu?: string;
};

export type KesfetSecenegi = {
  yer: NonNullable<AramaSonucu["yer"]>;
  cografya: AramaCografya;
  ana_kategori: string | null;
  alt_kategori: string | null;
  neden_bu: string;
  anlamli_fark: string;
  karar_sonucu: KararSonucu;
};

export type KesfetCevabi = {
  durum: "success" | "empty" | "insufficient";
  secenekler: KesfetSecenegi[];
  kimlik_eslesmeleri: Array<NonNullable<AramaSonucu["yer"]>>;
  kullanilan_baglam: Record<string, unknown>;
  sinirlama_nedeni: string;
  degerlendirilemeyen_aday_sayisi: number;
  daha_fazla_var_mi: boolean;
  trace_reference: string | null;
};

export type BugunAmaci = "kahve_icmek" | "yemek_yemek" | "tarihi_kulturel_ziyaret";

export type BugunNeYapalimTalebi = {
  serbest_metin?: string | null;
  niyet: {
    sehir: string;
    ilce?: string | null;
    amac?: BugunAmaci | null;
    kisi_baglami?: string | null;
    istenen_zaman?: string | null;
    sure_dakika?: number | null;
    ulasim_bicimi?: string | null;
    butce_ust_siniri?: number | null;
    zorunlu_kosullar?: string[];
    tercihler?: string[];
  };
  haric_yerler?: string[];
};

export type BugunNeYapalimCevabi = {
  durum: "clarification" | "success" | "empty" | "insufficient";
  anlasilan_ihtiyac_ozeti: string;
  netlestirme: {
    soru: string;
    alan: "amac";
    secenekler: Array<{ deger: BugunAmaci; etiket: string }>;
  } | null;
  baglam: KararBaglami;
  bugun_baglami: {
    degerlendirme_zamani: string;
    saat_dilimi: string;
    ziyaret_tarihi: string;
    aciklik_bilgisi: "dogrulanmiyor";
    aciklik_aciklamasi: string;
  };
  kesfet: KesfetCevabi | null;
  kesfet_sorgusu: string | null;
};

export type IlceKapsami = {
  id: string;
  isim: string;
  slug: string;
  yayinlanmis_yer_turleri: string[];
  ayri_sayfa_var: boolean;
  kesfet_url: string;
};

export type SehirKapsami = {
  sehir_id: string;
  sehir_anahtari: string;
  sehir_ismi: string;
  manifest_surumu: string;
  kimlik_aramasi_destekleniyor: boolean;
  karar_kapsami_destekleniyor: boolean;
  yayinlanmis_yer_sayisi: number;
  desteklenen_yer_turleri: string[];
  desteklenen_iddia_aileleri: string[];
  ilceler: IlceKapsami[];
  kapsam_aciklamasi: string;
};

export type IlceDetayi = {
  cografya: {
    sehir_id: string;
    sehir_anahtari: string;
    sehir_ismi: string;
    ilce_id: string;
    ilce_slug: string;
    ilce_ismi: string;
  };
  ayri_sayfa_var: boolean;
  ozgun_karar_bilgileri: string[];
  yayinlanmis_yer_turleri: string[];
  kesfet_url: string;
  kapsam_aciklamasi: string;
};

export type KamusalYerDetayi = {
  yer: NonNullable<AramaSonucu["yer"]>;
  cografya: {
    sehir_id: string;
    sehir_anahtari: string;
    sehir_ismi: string;
    ilce_id: string | null;
    ilce_slug: string | null;
    ilce_ismi: string | null;
  };
  ana_kategori: string;
  alt_kategori: string;
  adres: string | null;
  aciklama: string | null;
  telefon: string | null;
  web_sitesi: string | null;
  enlem: number;
  boylam: number;
  fotograf_urlleri: string[];
  pratik_bilgiler: Array<{
    aile: string;
    deger: unknown;
    kapsam: Record<string, unknown>;
    gecerlilik_baslangici: string | null;
    gecerlilik_bitisi: string | null;
    dogrulanma_zamani: string | null;
    guncellik_anlami: string;
  }>;
  karar_sonucu: KararSonucu | null;
  kritik_bilinmeyenler: string[];
  kapsam_anlami: string;
  duzeltme_girisi: { etiket: string; aciklama: string; href: string | null };
};
