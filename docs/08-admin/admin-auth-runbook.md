---
title: "İç Admin Kimliği ve Operasyon Runbook'u"
version: "1.0"
status: "uygulandi"
phase: "Dalga-1B"
last_update: "2026-09-15"
depends:
  - "../05-engineering/15-uygulama-fark-analizi-ve-mvp-uygulama-plani.md"
affects:
  - "../../sunucu/auth/"
  - "../../sunucu/admin/"
  - "../../site/src/app/admin/"
author: "Codex"
---

# İç admin kimliği ve operasyon runbook'u

Bu kimlik alanı tüketici hesabı değildir. Admin API `/v1/admin/*`, dokümantasyonu `/v1/admin/docs`, arayüzü `/admin` altındadır. Public OpenAPI admin sözleşmesini içermez.

## İlk kullanıcı

Önce `0008`–`0010` migration'ları uygulanır. Parola komut satırı argümanına veya shell geçmişine yazılmaz:

```text
.\.venv_test\Scripts\python.exe -m sunucu.auth.bootstrap --eposta admin@example.com --ad "Operasyon Sorumlusu" --roller yonetici
```

Parola en az 14 karakterdir. Hazır parola veya varsayılan admin oluşturulmaz. Production'da TLS zorunludur; oturum cookie'si `HttpOnly`, `Secure`, `SameSite=Strict`; yazma istekleri ayrıca CSRF token ister. Veritabanında yalnız token/CSRF/IP/User-Agent özetleri tutulur. `ADMIN_OTURUM_SURESI_DK` varsayılanı 480 dakikadır.

## Rol ve kritik işlem

Roller: `gozlemci`, `kimlik_editoru`, `claim_editoru`, `yayinci`, `risk_onayci`, `auditor`, `yonetici`. Yetki varsayılan olarak yoktur. Canonical merge, split, kritik claim yayını, withdrawal ve hak değişikliği ikinci inceleme bekler. Talebi açan aktör kendi talebini onaylayamaz.

İhlal veya hesap kaybında `admin_kullanicilari.aktif_mi=false` yapılır ve kullanıcının açık oturumlarına `iptal_zamani` verilir. Audit satırları güncellenmez/silinmez; PostgreSQL trigger bunu engeller. Audit'e parola, token, secret veya ham kişisel veri yazılmaz.

## Bağlı belgeler

- [Uygulama planı](../05-engineering/15-uygulama-fark-analizi-ve-mvp-uygulama-plani.md)
- [Publication lifecycle](../07-backend/publication-lifecycle.md)

## Etkilediği belgeler

Bu runbook `sunucu/README.md` ve `site/README.md` çalışma notlarını somutlaştırır.

## Bundan sonra okunması gereken belge

[Publication lifecycle](../07-backend/publication-lifecycle.md).
