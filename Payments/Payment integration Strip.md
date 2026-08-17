[[Strip]] [[payment gateway]] [[PSP]] [[webhook]] [[express concepts]] [[SAQ GSS]]

# Payment integration Strip

> *(Stripe Checkout integration.)* The browser asks your API for a Checkout Session, redirects to Stripe’s hosted page, then your server confirms payment via webhook — not the return URL alone.

```txt
        Payment integratio ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want the end-to-end Checkout flow: create session server-side, r…

## Sources
- [Stripe — Checkout quickstart](https://docs.stripe.com/checkout/quickstart) — deep-dive
- [Stripe — Checkout Session API](https://docs.stripe.com/api/checkout/sessions) — deep-dive
- [Stripe — Fulfill orders with webhooks](https://docs.stripe.com/checkout/fulfillment) — overview

## Key Concepts
- **Server creates the session:** price, currency, `success_url`, `cancel_url`, and metadata (`orderId`).
- **Client only redirects:** no secret key in the browser.
- **Return URL ≠ paid:** user can close the tab; webhook still arrives.
- **Idempotent fulfillment:** store Stripe event IDs; retries must not double-ship.
- **PCI path:** hosted Checkout aligns with reduced SAQ when no PAN touches your servers ([[S…


- **Core:** Checkout Session integration outsources card entry to Stripe. Your backend cr…

## Technical Details
```
Browser ──POST /checkout-session──► Your API ──create Checkout Session──► Stripe
   │                                      │
   ◄────────── session.url ───────────────┘
   │
   └─ redirect to Stripe Checkout ──► success_url
                                      │
Stripe ──webhook checkout.session.completed──► Your API (verify signature, fulfill)
```

```javascript
// Server — create session
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: [{ price: 'price_123', quantity: 1 }],
  success_url: 'https://shop.example/success?session_id={CHECKOUT_SESSION_ID}',
  cancel_url: 'https://shop.example/cart',
  metadata: { orderId },
});
res.json({ url: session.url });
```

```javascript
// Client — redirect after confirm dialog
const { url } = await api.post('applications/checkout-session', { body: {} });
if (url) window.location.href = url;
```

```javascript
// Webhook — raw body required
event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);
if (event.type === 'checkout.session.completed') {
  const session = event.data.object;
  await fulfillOrder(session.metadata.orderId, session.id);
}
```

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Redirect never starts | Session create failed / no `url` | Check API error; secret key mode |
| Paid but order pending | Webhook not configured | Stripe CLI locally; Dashboard endpoint live |
| Signature failure | `express.json` before webhook | `express.raw` on webhook route |
| Double fulfill | Retries without idempotency | Upsert on `event.id` / session id |
| Wrong mode keys | `sk_test` vs `sk_live` | Separate environments |

## Mistakes to Avoid
- **Mistake:** Exposing `sk_live` / `sk_test` in frontend bundles
- **Mistake:** Marking orders paid from `success_url` alone
- **Mistake:** Skipping webhook signature verification
- **Mistake:** Reusing one Checkout Session across unrelated orders
- **Mistake:** Ignoring `metadata.orderId` so fulfillment cannot map the sessio…

## Pros/Cons or Trade-offs
- **Pro:** Fast PCI-friendly integration; Stripe owns card UI and SCA.
- **Con:** Less control than Payment Element / custom PaymentIntents.
- **Con:** Mobile WebViews and in-app browsers need extra care for redirects.

## Comparison
- vs [[Strip]] PaymentIntents + Elements: more UX control, slightly more PCI/JS surface.
- vs [[razorpay integration]]: same redirect/hosted idea; different order and signature APIs.
- vs direct charge API with PAN: expands PCI to SAQ D — avoid.


### Use cases
- Application fees, course checkout, and any one-page “pay then unlock” flow th…

- **Example:** Frontend shows “Redirecting to Payment,” POSTs to `applications/…
