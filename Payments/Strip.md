[[Payments/payment gateway]] [[Payments/PSP]] [[Payments/PSI GSS]] [[Payments/SAQ GSS]] [[NodeJS/Packages/SuperTokens]]

# Strip

> *(Filename typo: **Stripe**)* — Payment processor API for cards, subscriptions, Connect marketplaces — **Stripe docs + PCI scope reduction**.

## Mental model

Stripe is a **PSP** that handles card network rails, tokenization, and compliance tooling. Your server uses **secret key**; browser uses **publishable key** + Stripe.js / Elements — raw PAN never touches your disk if integrated correctly.

```
Browser (Stripe.js) ──PaymentMethod id──► Your API ──► Stripe API
                              │                           │
                              └── no raw card on your server └── charges, subs, payouts
```

| Product | Use |
|---------|------|
| **Checkout** | Hosted payment page — smallest PCI scope |
| **Payment Intents** | Custom UI + SCA (3DS) |
| **Connect** | Marketplace split payouts |
| **Billing** | Subscriptions + invoices |
| **Webhooks** | Async payment state — source of truth |

## Standard config / commands

### Node.js integration

```bash
npm install stripe
```

```javascript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2024-06-20', // pin version in prod
});

// Create PaymentIntent (server)
const intent = await stripe.paymentIntents.create({
  amount: 1999,
  currency: 'usd',
  automatic_payment_methods: { enabled: true },
});
// Return client_secret to frontend
```

### Webhook (verify signature — mandatory)

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

### CLI local testing

```bash
stripe login
stripe listen --forward-to localhost:3000/webhooks/stripe
stripe trigger payment_intent.succeeded
```

### Idempotency (retries)

```javascript
await stripe.paymentIntents.create(params, {
  idempotencyKey: `order-${orderId}`,
});
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `card_declined` | Radar rules / insufficient funds | Dashboard logs; test cards in test mode |
| Webhook 400 | Raw body parsed as JSON | Use `express.raw` on webhook route only |
| Double charge | Retry without idempotency key | Same key per logical operation |
| SCA required loop | Off-session charge | Use SetupIntent + on-session confirmation |
| Connect payout stuck | KYC / capabilities | Dashboard Connect onboarding status |
| Test keys in prod | `sk_test` in env | Separate secrets per env; doppler/CI scan |

## Gotchas

> [!WARNING]
> **Never log full PaymentMethod or card objects** — PCI and secret data exposure.

- **Webhook order not guaranteed** — design idempotent handlers; store event IDs.
- **Amount in cents** — off-by-100 bugs are common.
- **Radar + 3DS** — EU PSD2 requires SCA; test with Stripe test cards triggering auth.
- **Connect** — platform liability for negative balances; read reserves docs.

## When NOT to use

- Pure crypto/on-chain payments — different stack.
- In-person only with no online — simpler terminal SDK may suffice.
- Countries Stripe doesn't support — local PSP via [[Payments/PSP]].

## Related

[[Payments/payment gateway]] [[Payments/PSP]] [[Payments/PSI GSS]] [[Payments/SAQ GSS]] [[Messaging/webhook]]
