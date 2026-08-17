[[payment gateway]] [[PSP]] [[PSI GSS]] [[Strip]] [[razorpay integration]] [[webhook]]

# Payment break down json

> Payment breakdown JSON is the structured price and payment-state payload a booking or checkout API returns — line totals, taxes, add-ons, and flags like SCA required — so the client can show “what you pay” without inven…

```txt
        Payment break down ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask how you model money in APIs (minor units, currency codes), h…

## Sources
- [ISO 4217 — Currency codes](https://www.iso.org/iso-4217-currency-codes.html) — overview
- [Stripe — Amounts (minor units)](https://docs.stripe.com/currencies#zero-decimal) — deep-dive
- [EMVCo — 3-D Secure](https://www.emvco.com/emv-technologies/3d-secure/) — overview

## Key Concepts
- **Server is source of truth:** quote and re-price on the server; client displays returned fields.
- **Length of stay / rate rules:** quoted rates depend on check-in date and nights
- **SCA / 3DS flags:** `scaRequired: true` means the client must complete Strong Customer Authentica…
- **Null payment nodes:** `digitalPayment: null` often means “not yet collected” or “pay at property.”
- **Idempotent confirmation:** `confNumber` ties the commercial breakdown to a durable reservation id.


- **Core:** A breakdown object lists the components of a charge (room nights, taxes, fees…

## Technical Details
- Illustrative hospitality-style GraphQL shape (field names vary by vendor):

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

- Prefer explicit money objects in new designs:

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

## Mistakes to Avoid
- **Mistake:** Recomputing grand total in the client from partial line items
- **Mistake:** Treating `digitalPayment: null` as an error when pay-at-property…
- **Mistake:** Ignoring `scaRequired` and marking the booking prepaid
- **Mistake:** Mixing major and minor currency units in the same object without…
- **Mistake:** Logging full payment method blobs embedded inside breakdown payl…

## Pros/Cons or Trade-offs
- **Pro:** One payload drives receipt UI, SCA branching, and support tools.
- **Con:** Vendor-specific nesting (GraphQL wrappers) is noisy — map to an internal DTO.
- **Con:** Null-heavy graphs are easy to misread as “payment failed” vs “not collected.”

## Comparison
- vs [[payment gateway]] charge response: gateway returns processor codes
- vs [[Strip]] / [[razorpay integration]] webhooks: webhooks confirm money movement
- vs client-only cart math: unsafe for tax and promo rules.


### Use cases
- Hotel booking engines, airline ancillaries, and cart APIs that return tax-inc…

- **Example:** Reservation returns `scaRequired: true` and a non-null `sca` act…
