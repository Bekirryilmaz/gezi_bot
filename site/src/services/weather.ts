import type { OpenMeteoForecast, WeatherData } from "@/types/weather";

const OPEN_METEO_KOKU = "https://api.open-meteo.com/v1/forecast";

const WMO_ACIKLAMALARI: Array<{ kodlar: number[]; metin: string }> = [
  { kodlar: [0], metin: "Açık" },
  { kodlar: [1], metin: "Çoğunlukla açık" },
  { kodlar: [2], metin: "Parçalı bulutlu" },
  { kodlar: [3], metin: "Kapalı" },
  { kodlar: [45, 48], metin: "Sisli" },
  { kodlar: [51, 53, 55, 56, 57], metin: "Çisenti" },
  { kodlar: [61, 63, 65, 66, 67], metin: "Yağmurlu" },
  { kodlar: [71, 73, 75, 77], metin: "Karlı" },
  { kodlar: [80, 81, 82], metin: "Sağanak yağış" },
  { kodlar: [85, 86], metin: "Kar sağanağı" },
  { kodlar: [95, 96, 99], metin: "Gök gürültülü fırtına" },
];

export function wmoAciklamasi(kod: number): string {
  const eslesen = WMO_ACIKLAMALARI.find((g) => g.kodlar.includes(kod));
  return eslesen?.metin ?? "Değişken";
}

export function havaDurumuGetir(
  enlem: number,
  boylam: number,
  sinyal?: AbortSignal,
): Promise<WeatherData> {
  const params = new URLSearchParams({
    latitude: String(enlem),
    longitude: String(boylam),
    current: "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
    daily: "weather_code,temperature_2m_max,temperature_2m_min",
    timezone: "auto",
    forecast_days: "5",
  });

  return fetch(`${OPEN_METEO_KOKU}?${params}`, { signal: sinyal }).then(
    async (yanit) => {
      if (!yanit.ok) {
        throw new Error(`Hava durumu alınamadı (${yanit.status})`);
      }
      const ham = (await yanit.json()) as OpenMeteoForecast;
      return openMeteoDonustur(ham);
    },
  );
}

export function openMeteoDonustur(ham: OpenMeteoForecast): WeatherData {
  const gunler = ham.daily.time.map((tarih, i) => ({
    date: tarih,
    maxTemp: ham.daily.temperature_2m_max[i] ?? 0,
    minTemp: ham.daily.temperature_2m_min[i] ?? 0,
    weatherCode: ham.daily.weather_code[i] ?? 0,
  }));

  return {
    current: {
      temperature: ham.current.temperature_2m,
      humidity: ham.current.relative_humidity_2m,
      windSpeed: ham.current.wind_speed_10m,
      weatherCode: ham.current.weather_code,
      description: wmoAciklamasi(ham.current.weather_code),
    },
    daily: gunler,
  };
}
