[[payment gateway]] [[Strip]] [[PSI GSS]] [[SAQ GSS]] [[TLS (Transport Layer Security)]] [[webhook]]

# PSP (Payment Service Provider)

> A Payment Service Provider (PSP) connects payers and merchants — onboarding, KYC, payment-method acceptance, APIs, and settlement to a bank account.





## Interview Relevance
Interviewers ask how you pick a PSP (geography, PCI path, payouts, disputes) and how you reconcile webhooks and settlement reports without double-fulfilling orders.

## Sources
- [Wikipedia — Payment service provider](https://en.wikipedia.org/wiki/Payment_service_provider) — overview
- [PCI SSC — Third-party service providers](https://www.pcisecuritystandards.org/) — overview
- [Stripe — Connect (platform / marketplace model)](https://docs.stripe.com/connect) — deep-dive

## Core Definition
A PSP bundles software and acquiring relationships so a merchant can accept cards and local methods without becoming a bank. Many PSPs include a [[payment gateway]]; the merchant still owns chargeback liability unless a platform product shifts responsibility by design.

## Recall Cues
- Why do interviewers care about how you pick a PSP (geography, PCI path, payouts, disputes) and how you reconcile webhooks and settlement reports without double-fulfilling orders?
- What is step 1: Create sandbox + live merchant accounts (separate keys)?
- What is step 2: Implement tokenized checkout (no PAN storage)?
- What is step 3: Webhooks with signature verification + idempotency store?
- What is step 4: Reconciliation job: PSP settlement report ↔ internal orders?
- What is step 5: Refund + partial refund API paths tested?
- What mistake is **Sharing live and sandbox keys across environments**?
- What mistake is **Fulfilling orders from unsigned webhooks**?

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
- Sharing live and sandbox keys across environments.
- Fulfilling orders from unsigned webhooks.
- Ignoring chargeback and reserve policies when pricing.
- Storing PAN “just for retries” instead of network tokens / PSP tokens.
- Assuming marketplace liability matches a simple merchant account ([[Strip]] Connect differs).

## Comparison
- vs [[payment gateway]]: gateway may be only the API; PSP usually includes merchant account and settlement.
- vs becoming an acquirer/bank: licensing and capital — not an API integration.
- vs cash-only micro business: PSP fees can exceed benefit.

## Real-World Applications
Online stores, subscription SaaS, and marketplaces that need split payouts to sellers.

**Example:** Nightly job downloads the PSP balance report and alerts when `transaction_id` amounts diverge from internal `orders.total` by more than a threshold.

## Pros/Cons or Trade-offs
- **Pro:** Fast path to accept payments without acquiring licenses.
- **Con:** Fees (interchange + markup) shape unit economics — model early.
- **Con:** Multi-PSP failover is complex; prefer one until scale demands.
