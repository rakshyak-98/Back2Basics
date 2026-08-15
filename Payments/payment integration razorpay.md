[[razorpay integration]] [[payment gateway]] [[PSP]] [[webhook]] [[Strip]]

# payment integration razorpay

> Razorpay capture confirms an authorized payment and moves money toward settlement — without capture (when required), an authorization can expire and never pay you.

## Interview Relevance

Interviewers separate authorization (hold) from capture (take funds), ask when auto-capture is enough, and how partial capture / failure webhooks should update order state.

## Sources

- [Razorpay — Capture payments](https://razorpay.com/docs/payments/payments/capture-settings/) — deep-dive
- [Razorpay — Payments API](https://razorpay.com/docs/api/payments/) — deep-dive
- [Razorpay — Webhooks (payments)](https://razorpay.com/docs/webhooks/payments/) — overview

## Core Definition

After the customer authenticates, a payment may be authorized but not yet captured. Capture is the merchant/PSP step that finalizes the charge against that authorization. Razorpay can auto-capture on success or leave capture to your API for delayed fulfillment (for example, ship-then-capture).

## Key Concepts

- **Authorize:** issuer approves a hold — funds may be reserved.
- **Capture:** converts the authorization into a capturable/settling payment.
- **Auto-capture:** Checkout settings capture immediately — simpler shops.
- **Manual / delayed capture:** call capture API after inventory check or shipment.
- **Partial capture / void:** capture less than authorized, or release the hold if you cannot fulfill.

## Technical Details

```
Checkout success → payment authorized
        │
        ├─ auto-capture on ──► payment.captured webhook → mark Paid
        │
        └─ manual mode ──► your server POST /payments/:id/capture
                              │
                              └─ payment.captured / payment.failed
```

```javascript
// Manual capture after business checks
await razorpay.payments.capture(paymentId, amountPaise, 'INR');
```

| Mode | When to use |
|------|-------------|
| Auto-capture | Digital goods / always-in-stock |
| Manual capture | Physical goods, fraud review, hotel-style holds |
| Partial capture | Ship subset; release remainder |

| Symptom | Check | Fix |
|---------|-------|-----|
| Authorization success, never settled | Capture never called / expired | Capture before authorization expiry; alert on stuck Authorized |
| Capture amount mismatch | Paise vs rupees | Use smallest currency unit |
| Double capture error | Retry without idempotency | Treat already-captured as success |
| Order Paid too early | Listening only to authorize | Wait for `payment.captured` when manual |
| Customer charged, no stock | Captured before inventory lock | Capture after reservation |

## Real-World Applications

Marketplaces that verify inventory after payment UI success, hotels holding deposits, and merchants that auto-capture digital downloads.

**Example:** Order stays `Authorized` overnight because manual capture was enabled and the worker crashed — monitor aging authorizations and capture or release before expiry.

## Pros/Cons or Trade-offs

- **Pro:** Delayed capture reduces charging for unfulfillable orders.
- **Con:** Authorization windows expire — ops must watch stuck payments.
- **Con:** More states to model (`Authorized`, `Captured`, `Failed`) than auto-capture shops.

## Comparison

- vs [[razorpay integration]]: full Order/Checkout/verify path vs this capture-focused note.
- vs [[Strip]] authorize/capture: same commerce idea; Stripe uses PaymentIntent `capture_method`.
- vs void/refund: void/release before capture; refund after capture.

## Mistakes to Avoid

- Marking orders paid on authorization when your settings require capture.
- Capturing a different amount/currency than the Order without a deliberate partial-capture design.
- Ignoring `payment.failed` after a capture attempt.
- Mixing auto-capture Dashboard settings with code that also calls capture.
