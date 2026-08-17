[[payment gateway]] [[PSP]] [[Payment integration Strip]] [[PSI GSS]] [[SAQ GSS]] [[webhook]] [[TLS (Transport Layer Security)]]

# Strip

> *(Filename typo for **Stripe**.)* Stripe is a Payment Service Provider API for cards, wallets, subscriptions, and Connect marketplaces — use Checkout or Elements so card data never hits your server.

```txt
        Strip ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers expect PaymentIntents, webhook signature verification with the r…

## Sources
- [Stripe — Documentation](https://docs.stripe.com/) — deep-dive
- [Stripe — Webhooks](https://docs.stripe.com/webhooks) — deep-dive
- [Stripe — Payment Intents](https://docs.stripe.com/payments/paymentintents) — overview
- [Stripe — Checkout](https://docs.stripe.com/payments/checkout) — overview

## Key Concepts
- **Checkout:** hosted payment page — smallest PCI scope for many shops.
- **PaymentIntents:** server-created intent + client confirmation — supports SCA / 3-D Secure.
- **Connect:** platforms and marketplaces with split payouts.
- **Billing:** subscriptions and invoices.
- **Webhooks:** async state (`payment_intent.succeeded`, disputes) — verify signatures.


- **Core:** Stripe provides APIs and client SDKs so merchants accept payments under Strip…

## Technical Details
```
Browser (Stripe.js) ──PaymentMethod id──► Your API ──► Stripe API
                              │                           │
                              └── no raw card on your server └── charges, subs, payouts
```

| Product | Use |
|---------|------|
| Checkout | Hosted page — smallest PCI scope |
| Payment Intents | Custom UI + SCA (3DS) |
| Connect | Marketplace split payouts |
| Billing | Subscriptions + invoices |
| Webhooks | Async payment state — source of truth |

```bash
npm install stripe
```

```javascript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2024-06-20', // pin version in production
});

const intent = await stripe.paymentIntents.create({
  amount: 1999,
  currency: 'usd',
  automatic_payment_methods: { enabled: true },
}, {
  idempotencyKey: `order-${orderId}`,
});
// Return client_secret to the frontend
```

```javascript
import express from 'express';

app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }
  if (event.type === 'payment_intent.succeeded') { /* fulfill order */ }
  res.json({ received: true });
});
```

```bash
stripe login
stripe listen --forward-to localhost:3000/webhooks/stripe
stripe trigger payment_intent.succeeded
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `card_declined` | Radar / funds | Dashboard logs; test cards in test mode |
| Webhook 400 | Body parsed as JSON | `express.raw` on webhook route only |
| Double charge | Retry without idempotency | Same key per logical operation |
| SCA required loop | Off-session charge | SetupIntent + on-session confirmation |
| Connect payout stuck | KYC / capabilities | Connect onboarding status |
| Test keys in production | `sk_test` in environment | Separate secrets; scan CI |

## Mistakes to Avoid
- **Mistake:** Logging full PaymentMethod or card objects
- **Mistake:** Parsing the webhook body as JSON before signature verification
- **Mistake:** Treating amounts as major units (off-by-100 bugs)
- **Mistake:** Fulfilling from the success URL without a verified webhook or re…
- **Mistake:** Using Dashboard webhook secrets against Stripe CLI-forwarded eve…

## Pros/Cons or Trade-offs
- **Pro:** Excellent docs, test clocks/cards, and PCI-reducing Checkout/Elements.
- **Con:** Country coverage gaps — fall back to a local [[PSP]].
- **Con:** Connect platforms inherit negative-balance and reserve complexity.

## Comparison
- vs [[payment gateway]]: Stripe is a full [[PSP]] with gateway APIs built in.
- vs [[Payment integration Strip]]: this note is the platform
- vs [[razorpay integration]]: Razorpay is stronger for India/UPI
- vs crypto-only stacks: different rails entirely.


### Use cases
- SaaS subscriptions, one-time e-commerce Checkout, and marketplaces paying out…

- **Example:** EU card requires Strong Customer Authentication
