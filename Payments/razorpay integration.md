[[payment integration razorpay]] [[PSP]] [[payment gateway]] [[webhook]] [[Strip]]

# razorpay integration

> Razorpay Standard Checkout: your server creates an Order, the browser opens Checkout with that `order_id`, you verify the payment signature, and webhooks cover closed tabs.

## Interview Relevance

Interviewers look for the Order → Checkout → HMAC signature verify → webhook safety-net pattern, and why browser-returned fields alone are forgeable.

## Sources

- [Razorpay — Standard Checkout integration steps](https://razorpay.com/docs/payments/payment-gateway/web-integration/standard/integration-steps/) — deep-dive
- [Razorpay — Validate webhooks](https://razorpay.com/docs/webhooks/validate-test/) — deep-dive
- [Razorpay — Orders](https://razorpay.com/docs/payments/orders/) — overview

## Core Definition

Integration centers on a server-created Order that binds amount and currency. Checkout collects payment methods on Razorpay’s UI. Success returns `razorpay_order_id`, `razorpay_payment_id`, and `razorpay_signature` for server-side HMAC verification; `payment.captured` / `order.paid` webhooks confirm state if the client never calls back.

## Key Concepts

- **Order first:** prevents amount tampering and links payments to your pending record.
- **Checkout.js:** opens Razorpay UI with Key ID + `order_id` (never Key Secret in the browser).
- **Payment signature:** HMAC-SHA256 of `order_id|payment_id` with Key Secret.
- **Webhook signature:** separate HMAC over the raw body with the webhook secret (`X-Razorpay-Signature`).
- **Idempotency:** event order is not guaranteed — store processed event IDs.

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

## Real-World Applications

India-focused e-commerce (UPI, cards, netbanking), course purchases, and apps that need a hosted method picker quickly.

**Example:** User closes the browser after UPI success — handler step never runs; `payment.captured` webhook still marks the order paid after signature checks.

## Pros/Cons or Trade-offs

- **Pro:** Strong local methods and a clear Order-centric API.
- **Con:** Global card coverage and Connect-like products differ from [[Strip]].
- **Con:** Two signature schemes (Checkout vs webhook) — easy to mix up secrets.

## Comparison

- vs [[payment integration razorpay]]: this note is the full checkout path; that note focuses on authorize vs capture.
- vs [[Payment integration Strip]]: same hosted idea; Stripe uses Checkout Sessions / PaymentIntents instead of Razorpay Orders.
- vs raw card API: expands PCI scope — prefer Standard Checkout.

## Mistakes to Avoid

- Trusting frontend success without HMAC verification.
- Putting Key Secret in client JavaScript.
- Validating webhooks on a parsed JSON object instead of the raw body.
- Fulfilling twice when both handler and webhook arrive.
- Expecting webhook event order to be strict.
