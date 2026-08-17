[[payment gateway]] [[PSP]] [[PSI GSS]] [[Strip]] [[razorpay integration]] [[webhook]]

# Payment break down json

> Payment breakdown JSON is the structured price and payment-state payload a booking or checkout API returns — line totals, taxes, add-ons, and flags like SCA required — so the client can show “what you pay” without inventing math.





## Interview Relevance
Interviewers ask how you model money in APIs (minor units, currency codes), how SCA/3DS flags drive UI, and why the client must not recompute trusted totals from sticky local state.

## Sources
- [ISO 4217 — Currency codes](https://www.iso.org/iso-4217-currency-codes.html) — overview
- [Stripe — Amounts (minor units)](https://docs.stripe.com/currencies#zero-decimal) — deep-dive
- [EMVCo — 3-D Secure](https://www.emvco.com/emv-technologies/3d-secure/) — overview

## Core Definition
A breakdown object lists the components of a charge (room nights, taxes, fees, add-ons) plus payment orchestration fields (`digitalPayment`, `sca`, `scaRequired`). Hospitality reservation APIs often nest this under `createReservation` / confirmation payloads alongside `confNumber` and stay dates.

## Key Concepts
- **Server is source of truth:** quote and re-price on the server; client displays returned fields.
- **Length of stay / rate rules:** quoted rates depend on check-in date and nights — front desk may re-verify at arrival.
- **SCA / 3DS flags:** `scaRequired: true` means the client must complete Strong Customer Authentication before funds settle.
- **Null payment nodes:** `digitalPayment: null` often means “not yet collected” or “pay at property.”
- **Idempotent confirmation:** `confNumber` ties the commercial breakdown to a durable reservation id.

## Technical Details
Illustrative hospitality-style GraphQL shape (field names vary by vendor):

```json
{
  "data": {
    "createReservation": {
      "data": {
        "digitalPayment": null,
        "enroll": {
          "hhonorsNumber": null,
          "resourceAlreadyExists": true
        },
        "mfa": null,
        "sca": null,
        "reservation": {
          "confNumber": "54129806",
          "arrivalDate": "2025-04-27",
          "departureDate": "2025-04-30",
          "cancelEligible": true,
          "modifyEligible": true,
          "scaRequired": false,
          "specialRateOptions": {
            "corporateId": null,
            "groupCode": null,
            "promoCode": null
          }
        }
      }
    }
  }
}
```

| Field cluster | Meaning |
|---------------|---------|
| Stay dates / length | Commercial basis for nightly rates |
| `specialRateOptions` | Corporate, group, loyalty, promo pricing |
| `sca` / `scaRequired` | Whether 3DS/SCA challenge is needed |
| `digitalPayment` | Tokenized online payment result, if any |
| `confNumber` | Durable booking id for support and webhooks |

Prefer explicit money objects in new designs:

```json
{
  "currency": "USD",
  "amounts": {
    "roomSubtotal": 45000,
    "taxes": 5200,
    "fees": 1500,
    "grandTotal": 51700
  },
  "amountsAreMinorUnits": true,
  "scaRequired": false
}
```

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| UI total ≠ charged | Client recomputed taxes | Display server `grandTotal` only |
| SCA loop | Ignored `scaRequired` | Drive 3DS UI from flags |
| Pay-at-property surprise | `digitalPayment` null not handled | Branch UX on null vs token |
| Rate dispute at check-in | Stale quote | Re-fetch breakdown before payment |
| FX confusion | Major vs minor units | Document and test ISO 4217 minor units |

## Real-World Applications
Hotel booking engines, airline ancillaries, and cart APIs that return tax-inclusive breakdowns before calling a [[PSP]].

**Example:** Reservation returns `scaRequired: true` and a non-null `sca` action URL — the app must complete authentication before treating the stay as prepaid.

## Pros/Cons or Trade-offs
- **Pro:** One payload drives receipt UI, SCA branching, and support tools.
- **Con:** Vendor-specific nesting (GraphQL wrappers) is noisy — map to an internal DTO.
- **Con:** Null-heavy graphs are easy to misread as “payment failed” vs “not collected.”

## Comparison
- vs [[payment gateway]] charge response: gateway returns processor codes; breakdown JSON is the merchant commercial view.
- vs [[Strip]] / [[razorpay integration]] webhooks: webhooks confirm money movement; breakdown JSON explains the quote.
- vs client-only cart math: unsafe for tax and promo rules.

## Mistakes to Avoid
- Recomputing grand total in the client from partial line items.
- Treating `digitalPayment: null` as an error when pay-at-property is valid.
- Ignoring `scaRequired` and marking the booking prepaid.
- Mixing major and minor currency units in the same object without a flag.
- Logging full payment method blobs embedded inside breakdown payloads.
