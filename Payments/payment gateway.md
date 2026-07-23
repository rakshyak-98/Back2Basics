[[Payments/PSP]] [[Payments/Strip]] [[Payments/PSI GSS]] [[Security/TLS (Transport Layer Security)]]

# Payment gateway

> Merchant-facing HTTP/API front door to payment networks — authorizes and captures without merchant touching card rails directly — **e-commerce integration model**.

## Mental model

A **payment gateway** sits between merchant site/[[POS]] and acquirer/processor. It tokenizes sensitive data, routes to card networks, returns auth/capture result.

```
Shopper → Merchant site → Payment Gateway → Acquirer → Card networks → Issuer
                │                │
                └── often hosted checkout (iframe/redirect) ──► reduced PCI scope
```

| Property | Typical behavior |
|----------|------------------|
| **Not in money flow** | Settles via acquirer; gateway is software layer |
| **Connection** | Merchant server or browser plugin to gateway API |
| **Methods** | Cards, wallets, BNPL, bank debits (region-dependent) |

Gateway ≠ [[Payments/PSP]] entirely — PSP may own gateway + processing + merchant account, but role here is **integration API**.

## Standard config / commands

### Integration patterns

| Pattern | PCI impact | Control |
|---------|------------|---------|
| **Hosted checkout** (redirect) | Lowest — SAQ A | Less UX control |
| **Embedded iframe** (Fields) | Low — SAQ A-EP | Branded-ish UX |
| **Direct API** (server-side PAN) | High — SAQ D | Full control — avoid |

### Typical authorize + capture flow

```javascript
// 1. Client obtains payment token from gateway JS (never POST PAN to your server)
// 2. Server:
const result = await gateway.charge({
  amount: 5000,
  currency: 'USD',
  paymentToken: tokenFromClient,
  idempotencyKey: orderId,
});
// 3. Capture later for shipments:
await gateway.capture(result.transactionId, { amount: 5000 });
```

### Webhooks for final state

Treat gateway callback as truth for `succeeded` / `chargeback` — don't rely only on redirect URL (user can close tab).

### Environment separation

```bash
GATEWAY_API_URL=https://api.sandbox.gateway.com   # dev
GATEWAY_API_URL=https://api.gateway.com           # prod
# Never share merchant keys across envs
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth succeeds, order not created | Missing webhook handler | Idempotent webhook + retry |
| Decline spike | AVS/CVV rules, fraud filters | Gateway dashboard risk settings |
| Currency mismatch | Minor units vs major | Pass cents; ISO 4217 code |
| Timeout duplicate charges | No idempotency | Same key on retry |
| PCI audit failure | PAN in logs/DB | Tokenize; SAQ type review |

## Gotchas

> [!WARNING]
> **Client-side success redirect ≠ paid** — always confirm via server-side API or signed webhook.

- **3DS / SCA** — auth may require redirect; handle `requires_action` states.
- **Partial capture** — auth amount may exceed shipped total; void unused auth.
- **MOTO vs e-commerce** — different interchange and fraud rules.

## When NOT to use

- Internal B2B invoicing with wire/ACH only — gateway adds little value.
- Marketplace split payouts without platform product — need Connect-style [[Payments/PSP]] features.

## Related

[[Payments/PSP]] [[Payments/Strip]] [[Payments/PSI GSS]] [[Payments/SAQ GSS]] [[Security/TLS (Transport Layer Security)]]
