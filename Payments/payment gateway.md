[[PSP]] [[Strip]] [[PSI GSS]] [[SAQ GSS]] [[TLS (Transport Layer Security)]] [[webhook]]

# Payment gateway

> A payment gateway sits between the merchant site or POS and the acquirer — it tokenizes sensitive data, routes to card networks, and returns authorization and capture results.

```txt
        Payment gateway ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers check whether you know gateway versus [[PSP]], PCI scope by inte…

## Sources
- [Wikipedia — Payment gateway](https://en.wikipedia.org/wiki/Payment_gateway) — overview
- [PCI SSC — SAQ instructions and guidelines](https://www.pcisecuritystandards.org/document_library/) — deep-dive
- [Stripe — Payment Intents (authorize/capture model)](https://docs.stripe.com/payments/paymentintents) — overview

## Key Concepts
- **Not the money pipe:** settlement is acquirer-side
- **Tokenization:** browser/SDK collects PAN
- **Authorize then capture:** hold funds at checkout; capture on ship — void unused authorization.
- **Idempotency:** retries with the same key prevent double charges on timeouts.
- **Webhook as truth:** client redirects lie; signed server callbacks confirm final state.


- **Core:** The gateway is the software integration layer for card-not-present (and often…

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

## Mistakes to Avoid
- **Mistake:** Treating the client success redirect as proof of payment
- **Mistake:** Posting raw PAN to your API and claiming hosted-checkout scope
- **Mistake:** Retrying charges without an idempotency key
- **Mistake:** Mixing sandbox and live keys in one environment
- **Mistake:** Logging full card or payment-method objects

## Pros/Cons or Trade-offs
- **Pro:** Hosted/embedded patterns shrink PCI scope dramatically.
- **Con:** Less UX control than raw card API (which expands scope).
- **Con:** Marketplace split payouts need platform products ([[Strip]] Connect-style), not a bare gateway alone.

## Comparison
- vs [[PSP]]: PSP often includes gateway + merchant account + KYC
- vs [[PSI GSS]] / [[SAQ GSS]]: architecture and questionnaire paths for outsourced card entry.
- vs direct bank ACH/wire: gateway adds little for invoice-only B2B.


### Use cases
- E-commerce checkout, hotel deposits, and subscription first charges that late…

- **Example:** Shopper closes the tab after 3-D Secure
