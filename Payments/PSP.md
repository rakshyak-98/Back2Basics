[[payment gateway]] [[Strip]] [[PSI GSS]] [[SAQ GSS]] [[TLS (Transport Layer Security)]] [[webhook]]

# PSP (Payment Service Provider)

> A Payment Service Provider (PSP) connects payers and merchants — onboarding, KYC, payment-method acceptance, APIs, and settlement to a bank account.

```txt
        PSP (Payment Servi ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask how you pick a PSP (geography, PCI path, payouts, disputes) …

## Sources
- [Wikipedia — Payment service provider](https://en.wikipedia.org/wiki/Payment_service_provider) — overview
- [PCI SSC — Third-party service providers](https://www.pcisecuritystandards.org/) — overview
- [Stripe — Connect (platform / marketplace model)](https://docs.stripe.com/connect) — deep-dive

## Key Concepts
- **Core:** A PSP bundles software and acquiring relationships so a merchant can accept c…

## Technical Details
```
Customer payment ──► PSP ──► Acquiring bank ──► Card schemes ──► Issuing bank
                         │
                         └── software: APIs, dashboards, disputes, reports
```

| Factor | Question |
|--------|----------|
| Geography | Currencies, local methods (UPI, iDEAL, SEPA) |
| Model | SaaS subscription vs marketplace ([[Strip]] Connect) |
| PCI path | Hosted vs embedded fields → SAQ type |
| Payout speed | T+2 vs instant |
| Disputes | Dashboard + webhook chargeback events |

```text
1. Create sandbox + live merchant accounts (separate keys)
2. Implement tokenized checkout (no PAN storage)
3. Webhooks with signature verification + idempotency store
4. Reconciliation job: PSP settlement report ↔ internal orders
5. Refund + partial refund API paths tested
```

```sql
CREATE TABLE payment_events (
  event_id TEXT PRIMARY KEY,
  processed_at TIMESTAMPTZ DEFAULT now()
);
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Merchant account restricted | KYC doc expiry | PSP dashboard compliance tasks |
| Settlement delay | Rolling reserve / new account | Normal early; confirm risk policy |
| Method unavailable | Country/currency matrix | Enable method in dashboard |
| FX surprise | Presentment vs settlement currency | Show correct currency to user |
| Webhook secret rotated | Verify fails | Update secret; dual-secret window |

## Mistakes to Avoid
- **Mistake:** Sharing live and sandbox keys across environments
- **Mistake:** Fulfilling orders from unsigned webhooks
- **Mistake:** Ignoring chargeback and reserve policies when pricing
- **Mistake:** Storing PAN “just for retries” instead of network tokens / PSP t…
- **Mistake:** Assuming marketplace liability matches a simple merchant account…

## Pros/Cons or Trade-offs
- **Pro:** Fast path to accept payments without acquiring licenses.
- **Con:** Fees (interchange + markup) shape unit economics — model early.
- **Con:** Multi-PSP failover is complex; prefer one until scale demands.

## Comparison
- vs [[payment gateway]]: gateway may be only the API
- vs becoming an acquirer/bank: licensing and capital — not an API integration.
- vs cash-only micro business: PSP fees can exceed benefit.


### Use cases
- Online stores, subscription SaaS, and marketplaces that need split payouts to…

- **Example:** Nightly job downloads the PSP balance report and alerts when `tr…
