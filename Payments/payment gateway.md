[[PSP]] [[Strip]] [[PSI GSS]] [[SAQ GSS]] [[TLS (Transport Layer Security)]] [[webhook]]

# Payment gateway

> A payment gateway sits between the merchant site or POS and the acquirer — it tokenizes sensitive data, routes to card networks, and returns authorization and capture results.





## Interview Relevance
Interviewers check whether you know gateway versus [[PSP]], PCI scope by integration pattern, and why redirects/webhooks — not client success pages — decide payment state.

## Sources
- [Wikipedia — Payment gateway](https://en.wikipedia.org/wiki/Payment_gateway) — overview
- [PCI SSC — SAQ instructions and guidelines](https://www.pcisecuritystandards.org/document_library/) — deep-dive
- [Stripe — Payment Intents (authorize/capture model)](https://docs.stripe.com/payments/paymentintents) — overview

## Core Definition
The gateway is the software integration layer for card-not-present (and often wallet) payments. Money settles through the acquirer; the gateway provides APIs, hosted fields, tokens, and webhooks. A [[PSP]] may bundle gateway + processing + merchant account; a standalone gateway may plug into a third-party acquirer.

## Key Concepts
- **Not the money pipe:** settlement is acquirer-side; gateway returns authorization and capture outcomes.
- **Tokenization:** browser/SDK collects PAN; merchant server sees tokens only when designed correctly.
- **Authorize then capture:** hold funds at checkout; capture on ship — void unused authorization.
- **Idempotency:** retries with the same key prevent double charges on timeouts.
- **Webhook as truth:** client redirects lie; signed server callbacks confirm final state.

## Technical Details
```
Shopper → Merchant site → Payment Gateway → Acquirer → Card networks → Issuer
                │                │
                └── often hosted checkout (iframe/redirect) ──► reduced PCI scope
```

| Property | Typical behavior |
|----------|------------------|
| Money flow | Settles via acquirer; gateway is software |
| Connection | Merchant server or browser SDK to gateway API |
| Methods | Cards, wallets, BNPL, bank debits (region-dependent) |

| Pattern | PCI impact | Control |
|---------|------------|---------|
| Hosted checkout (redirect) | Lowest — often SAQ A | Less UX control |
| Embedded iframe / fields | Low — often SAQ A / A-EP | Branded-ish UX |
| Direct API (server-side PAN) | High — SAQ D | Full control — avoid |

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

```bash
GATEWAY_API_URL=https://api.sandbox.gateway.com   # development
GATEWAY_API_URL=https://api.gateway.com           # production
# Never share merchant keys across environments
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Authorization succeeds, order missing | No webhook handler | Idempotent webhook + retry |
| Decline spike | AVS/CVV, fraud filters | Gateway risk settings |
| Currency mismatch | Minor vs major units | Pass cents; ISO 4217 code |
| Timeout duplicate charges | No idempotency | Same key on retry |
| PCI audit failure | PAN in logs/DB | Tokenize; review SAQ type |

## Real-World Applications
E-commerce checkout, hotel deposits, and subscription first charges that later move to stored credentials / network tokens.

**Example:** Shopper closes the tab after 3-D Secure — the success URL never runs; a `payment.succeeded` webhook still marks the order paid.

## Pros/Cons or Trade-offs
- **Pro:** Hosted/embedded patterns shrink PCI scope dramatically.
- **Con:** Less UX control than raw card API (which expands scope).
- **Con:** Marketplace split payouts need platform products ([[Strip]] Connect-style), not a bare gateway alone.

## Comparison
- vs [[PSP]]: PSP often includes gateway + merchant account + KYC; gateway alone may be only the API layer.
- vs [[PSI GSS]] / [[SAQ GSS]]: architecture and questionnaire paths for outsourced card entry.
- vs direct bank ACH/wire: gateway adds little for invoice-only B2B.

## Mistakes to Avoid
- Treating the client success redirect as proof of payment.
- Posting raw PAN to your API and claiming hosted-checkout scope.
- Retrying charges without an idempotency key.
- Mixing sandbox and live keys in one environment.
- Logging full card or payment-method objects.
