Sürüm öncesi kontrol. Commit atma; özeti raporla.

1. `cd site && npm run lint`
2. `cd site && npx tsc --noEmit`
3. Rota: repo kökünden `.\.venv_test\Scripts\python.exe -m pytest sunucu/rota_motoru/testler/ -v`
4. `cd site && npm run build` (veya `npx next build`)
5. Varsa Lighthouse / Playwright e2e özeti

Her adım: geçti/kaldı + kısa çıktı. Kırmızı varsa düzeltme önerme, önce raporu ver.
