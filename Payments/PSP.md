[[Payments/payment gateway]] [[Payments/Strip]] [[Payments/PSI GSS]] [[Security/TLS (Transport Layer Security)]]

# PSP (Payment Service Provider)

> End-to-end payments intermediary — merchant accounts, processing, and often gateway UX — **Stripe/Adyen/Square class of vendors**.

## Mental model

A **PSP** connects **payers** and **merchants**: onboarding, compliance (KYC), payment method acceptance, settlement to bank account.

```
Customer payment ──► PSP ──► Acquiring bank ──► Card schemes ──► Issuing bank
                         │
                         └── software: APIs, dashboards, disputes, reports
```

| vs [[Payments/payment gateway]] | PSP often includes gateway + processing + merchant ID |
| vs [[Payments/payment gateway]] | Standalone gateway may plug into third-party acquirer |

PSPs provide **integration SDKs** for e-commerce and [[POS]] — checkout plugins, hosted pages, terminal APIs.

## Standard config / commands

### Choose PSP criteria

| Factor | Question |
|--------|----------|
| **Geography** | Currencies, local methods (UPI, iDEAL, SEPA) |
| **Model** | SaaS subscription vs marketplace ([[Payments/Strip]] Connect) |
| **PCI path** | Hosted vs embedded fields → SAQ type |
| **Payout speed** | T+2 vs instant |
| **Disputes** | Dashboard + webhook chargeback events |

### Integration checklist

```text
1. Create sandbox + live merchant accounts (separate keys)
2. Implement tokenized checkout (no PAN storage)
3. Webhooks with signature verification + idempotency store
4. Reconciliation job: PSP settlement report ↔ internal orders
5. Refund + partial refund API paths tested
```

### Example webhook idempotency store

```sql
CREATE TABLE payment_events (
  event_id TEXT PRIMARY KEY,
  processed_at TIMESTAMPTZ DEFAULT now()
);
```

### Reconciliation

```bash
# Nightly: download PSP balance report, match transaction IDs
# Alert on amount mismatch > threshold
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Merchant account restricted | KYC doc expiry | PSP dashboard compliance tasks |
| Settlement delay | Rolling reserve / new account | PSP risk policy; normal for startups |
| Method not available | Country/currency matrix | Enable payment method in dashboard |
| FX surprise | Presentment vs settlement currency | Display correct currency to user |
| Webhook secret rotated | 401 on verify | Update env; dual-secret window |

## Gotchas

> [!WARNING]
> **PSP holds merchant agreement** — chargebacks debit merchant; platform/marketplace liability differs with Connect.

- **Pass-through fees** — interchange + PSP markup; model unit economics early.
- **Multi-PSP** — failover routing complex; prefer one PSP until scale demands.
- **Stored credentials** — network tokens for subscriptions; PCI still applies to how you store tokens.

## When NOT to use

- Cash-only micro business — PSP fees exceed benefit.
- You are the bank — need licensing, not just API integration.

## Related

[[Payments/payment gateway]] [[Payments/Strip]] [[Payments/PSI GSS]] [[Payments/SAQ GSS]] [[Messaging/webhook]]
