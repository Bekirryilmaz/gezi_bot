---
title: "ADR-001 — Tek Yayın Kapısı ve Ayrık İç Admin"
version: "1.0"
status: "kabul_edildi"
phase: "Dalga-1B"
last_update: "2026-09-15"
depends:
  - "15-uygulama-fark-analizi-ve-mvp-uygulama-plani.md"
affects:
  - "../../sunucu/yayin/"
  - "../../sunucu/auth/"
  - "../../sunucu/admin/"
author: "Codex"
---

# ADR-001 — Tek yayın kapısı ve ayrık iç admin

## Karar

Modüler monolit korunur. Publication eligibility saf domain sonucu ve DB projection filtresi olarak tek merkezde yaşar. Withdrawal append-only kayıt + idempotent invalidation outbox üretir. Admin kimliği tüketici kimliğinden bağımsız, veritabanı-backed opaque session ve küçük statik RBAC matrisi kullanır. Kritik eylem, farklı aktörlü ikinci inceleme olmadan uygulanmaz. Public ve admin DTO/OpenAPI yüzeyleri ayrıdır.

## Gerekçe ve sonuç

Bu seçim mevcut FastAPI/PostgreSQL/Next.js deploy biçimine uyar; ayrı IAM, graph DB veya message broker işletim yükü eklemez. Bedeli, outbox consumer ölçeklemesi ve gelecekte OIDC geçişinin ayrıca yapılmasıdır. Audit DB trigger ile append-only'dir; application admini audit değiştiremez. Legacy yerler migration sırasında yalnız `sinirli_yayinlanabilir/legacy_gecis` projection'ı alır; yeni olumlu claim hak ve kanıt kapısını geçmeden yayımlanmaz.

## Bağlı belgeler

- [Uygulama planı](./15-uygulama-fark-analizi-ve-mvp-uygulama-plani.md)

## Etkilediği belgeler

- [Publication lifecycle](../07-backend/publication-lifecycle.md)
- [Admin auth runbook](../08-admin/admin-auth-runbook.md)

## Bundan sonra okunması gereken belge

[Publication lifecycle](../07-backend/publication-lifecycle.md).
