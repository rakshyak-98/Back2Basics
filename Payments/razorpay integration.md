[[payment integration razorpay]] [[PSP]] [[payment gateway]] [[webhook]] [[Strip]]

# razorpay integration

> Razorpay Standard Checkout: your server creates an Order, the browser opens Checkout with that `order_id`, you verify the payment signature, and webhooks cover closed tabs.

```txt
        razorpay integrati ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers look for the Order → Checkout → HMAC signature verify → webhook …

## Sources
- [Razorpay — Standard Checkout integration steps](https://razorpay.com/docs/payments/payment-gateway/web-integration/standard/integration-steps/) — deep-dive
- [Razorpay — Validate webhooks](https://razorpay.com/docs/webhooks/validate-test/) — deep-dive
- [Razorpay — Orders](https://razorpay.com/docs/payments/orders/) — overview

## Key Concepts
- **Core:** Integration centers on a server-created Order that binds amount and currency.…

## Technical Details
```
1. User clicks Pay
2. Frontend → Backend: create Order
3. Backend → Razorpay Orders API → order_id (save Pending)
4. Frontend opens Checkout with order_id
5. User pays in Razorpay UI
6. Frontend receives payment_id + signature
7. Backend verifies HMAC; mark Paid
8. Webhook payment.captured / order.paid as safety net
```

```javascript
// Verify Checkout handler signature (Node)
const crypto = require('crypto');
const body = orderId + '|' + paymentId;
const expected = crypto
  .createHmac('sha256', keySecret)
  .update(body)
  .digest('hex');
if (expected !== razorpaySignature) throw new Error('Invalid signature');
```

```javascript
// Webhook — use raw body
Razorpay.validateWebhookSignature(rawBody, signatureHeader, webhookSecret);
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Signature mismatch | Wrong secret / parsed body | Raw body; correct Key/webhook secret |
| Paid in dashboard, app Pending | No webhook / handler failed | Subscribe events; return 200 quickly |
| Double payment on order | Order not used / reused wrongly | One active Order per checkout attempt |
| Test vs live confusion | Key mode mismatch | Separate Key ID/Secret per environment |
| Amount tampered | Client-only amount | Always create Order server-side |

## Mistakes to Avoid
- **Mistake:** Trusting frontend success without HMAC verification
- **Mistake:** Putting Key Secret in client JavaScript
- **Mistake:** Validating webhooks on a parsed JSON object instead of the raw b…
- **Mistake:** Fulfilling twice when both handler and webhook arrive
- **Mistake:** Expecting webhook event order to be strict

## Pros/Cons or Trade-offs
- **Pro:** Strong local methods and a clear Order-centric API.
- **Con:** Global card coverage and Connect-like products differ from [[Strip]].
- **Con:** Two signature schemes (Checkout vs webhook) — easy to mix up secrets.

## Comparison
- vs [[payment integration razorpay]]: this note is the full checkout path
- vs [[Payment integration Strip]]: same hosted idea
- vs raw card API: expands PCI scope — prefer Standard Checkout.


### Use cases
- India-focused e-commerce (UPI, cards, netbanking), course purchases, and apps…

- **Example:** User closes the browser after UPI success
