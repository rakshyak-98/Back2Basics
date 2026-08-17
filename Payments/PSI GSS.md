[[SAQ GSS]] [[payment gateway]] [[PSP]] [[Strip]] [[TLS (Transport Layer Security)]] [[webhook]]

# PSI GSS (PCI Guest Service System)

> Payment Card Industry Guest Service System (PSI GSS) means the shopper types the card on a PCI-validated provider’s hosted page or iframe — your servers never see PAN, track, or CVV.

```txt
        PSI GSS (PCI Guest ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers test PCI scoping: when hosted checkout keeps you on a short SAQ,…

## Sources
- [PCI SSC — Document library (SAQ instructions)](https://www.pcisecuritystandards.org/document_library/) — deep-dive
- [PCI SSC — SAQ A eligibility (outsourced e-commerce)](https://www.pcisecuritystandards.org/) — overview
- [Wikipedia — PCI DSS](https://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard) — overview

## Key Concepts
- **No CHD on merchant systems:** no PAN, CVV, or track data in apps, logs, or tickets.
- **Hosted redirect or provider iframe:** payment UI originates from the validated [[PSP]].
- **AOC on file:** provider Attestation of Compliance and a responsibility matrix.
- **Token / webhook results:** your API stores payment tokens and order ids — not cards.
- **Scope creep:** one route that accepts raw card JSON ends GSS eligibility.


- **Core:** GSS-style architecture (hospitality and retail jargon for outsourced card ent…

## Technical Details
```
Shopper enters card ──► Hosted payment page (PSP) ──► networks
                              │
Merchant site ────────────────┘ only receives token / redirect result
(no PAN, no track, no CVV on merchant servers)
```

```text
☐ Checkout UI fully hosted OR iframe from PCI-validated provider
☐ Merchant JS cannot access card fields (cross-origin isolation)
☐ No PAN/CVV in URLs, logs, analytics, support tickets
☐ Webhooks use tokens only; verify TLS 1.2+
☐ Written agreement: provider is PCI DSS compliant (AOC on file)
☐ Annual SAQ correct type signed by officer
```

```javascript
// Merchant server — create session, redirect URL only
const session = await psp.createCheckoutSession({
  orderId,
  amount,
  successUrl: 'https://shop.example/success',
  cancelUrl: 'https://shop.example/cart',
});
res.redirect(session.url);
// Card entry happens entirely on PSP domain
```

- **Embedded fields:** use the official SDK fields
- Set CSP `frame-src` to the PSP origin.
- Validate `postMessage` origins.

| Symptom | Check | Fix |
|---------|-------|-----|
| QSA rejects SAQ A claim | PAN passed through merchant API | Move to hosted fields |
| Card data in application logs | Debug logging body | Redact; structured logging policy |
| Analytics pixel on checkout page | Third-party script access | Remove or use full redirect |
| Custom CSS overlay on card field | Breaks isolation | Provider-approved styling only |
| Mobile WebView checkout | In-app browser rules | Provider mobile SDK |

## Mistakes to Avoid
- **Mistake:** Accepting raw card JSON “only in staging” on merchant APIs
- **Mistake:** Letting support tools paste PANs into tickets
- **Mistake:** Overlaying custom inputs on provider iframes
- **Mistake:** Assuming analytics scripts on the checkout page are out of scope
- **Mistake:** Skipping annual AOC collection when switching PSPs

## Pros/Cons or Trade-offs
- **Pro:** Dramatically smaller compliance questionnaire when eligibility is real.
- **Con:** Less control over card-field UX than a direct API (which expands scope).
- **Con:** Vendor changes require fresh AOC and SAQ review.

## Comparison
- vs [[SAQ GSS]]: PSI GSS is the technical pattern; SAQ GSS is the attestation path.
- vs direct PAN API: full cardholder-data environment — typically SAQ D.
- vs MOTO / staff key-entry: not GSS — CHD lands on merchant systems.


### Use cases
- Hotel booking engines, restaurant online ordering, and any guest-facing check…

- **Example:** Front desk never keys cards into the admin panel
