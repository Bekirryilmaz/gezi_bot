import type { AramaSonucu, VeriDurumu } from "@/lib/types";

export function SonucListesi({
  durum,
  sonuclar,
  hataMesaji,
}: {
  durum: VeriDurumu;
  sonuclar: AramaSonucu[];
  hataMesaji?: string;
}) {
  if (durum === "loading") return <p role="status">Sonuçlar aranıyor…</p>;
  if (durum === "error" || durum === "unavailable")
    return <p role="alert">{hataMesaji ?? "Arama şu anda kullanılamıyor."}</p>;
  if (durum === "insufficient")
    return <p role="status">Bu koşulları değerlendirecek yeterli bilgi yok.</p>;
  if (durum === "empty")
    return <p role="status">Bu aramayla eşleşen yayımlanabilir sonuç yok.</p>;
  return (
    <ul aria-label="Arama sonuçları" className="grid gap-3">
      {sonuclar.map((sonuc, sira) => (
        <li
          key={sonuc.yer?.branch_id ?? `${sonuc.sonuc_turu}-${sonuc.etiket}-${sira}`}
          className="border-deniz/10 rounded-2xl border bg-white p-4"
        >
          <p className="font-semibold">{sonuc.etiket}</p>
          <p className="text-deniz/70 text-sm">
            {sonuc.sonuc_turu === "yer_kimligi"
              ? "Yer"
              : sonuc.sonuc_turu === "baglamsal_aday"
                ? "İlgili aday"
                : sonuc.sonuc_turu}
            {sonuc.cografya.ilce_ismi ? ` · ${sonuc.cografya.ilce_ismi}` : ""}
          </p>
        </li>
      ))}
    </ul>
  );
}
