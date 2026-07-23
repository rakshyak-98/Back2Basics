[[Payments/SAQ GSS]] [[Payments/payment gateway]] [[Payments/PSP]] [[Security/TLS (Transport Layer Security)]]

# PSI GSS (PCI Guest Service System)

> PCI SSC program: outsource entire payment page/checkout to qualified provider — dramatically shrink merchant PCI scope — **PCI DSS SAQ selection**.

## Mental model

**PSI GSS** (Payment Card Industry **Guest Service System**) describes when a merchant uses a **third-party hosted** checkout such that **cardholder data never enters merchant systems**.

```
Shopper enters card ──► Hosted payment page (PSP) ──► networks
                              │
Merchant site ────────────────┘ only receives token / redirect result
(no PAN, no track, no CVV on merchant servers)
```

Eligible merchants may qualify for simplified **SAQ** (Self-Assessment Questionnaire) — historically aligned with **SAQ A**-style scope when **all** card data handled by compliant service provider.

Works with [[Payments/PSI GSS]] companion concept on questionnaire side — see [[Payments/SAQ GSS]].

## Standard config / commands

### Scope reduction checklist

```text
☐ Checkout UI fully hosted OR iframe from PCI-validated provider
☐ Merchant JS cannot access card fields (cross-origin isolation)
☐ No PAN/CVV in URLs, logs, analytics, support tickets
☐ Webhooks use tokens only; verify TLS 1.2+
☐ Written agreement: provider is PCI DSS compliant (AOC on file)
☐ Annual SAQ correct type signed by officer
```

### Hosted redirect pattern

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

### iframe / embedded fields

- Use official SDK fields — not custom `<input>` for PAN
- CSP `frame-src` allow PSP origin only
- PostMessage results — validate origin

### Documentation for audit

- Store provider **AOC** (Attestation of Compliance) + responsibility matrix
- Network diagram showing CHD boundaries
- List all systems that could touch cardholder data (should be empty for true GSS)

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| QSA rejects SAQ A claim | PAN passed through merchant API | Move to hosted fields |
| Card data in application logs | Debug logging body | Redact; structured logging policy |
| Analytics pixel on checkout page | Third-party script access | Remove from hosted page or use redirect |
| Custom CSS overlay on card field | Breaks isolation | Use provider-approved styling hooks |
| Mobile WebView checkout | In-app browser rules | Use provider mobile SDK |

## Gotchas

> [!WARNING]
> **One misconfigured API route** that accepts raw card JSON expands scope to full SAQ D instantly.

- **Mail-order / phone** MOTO flows are separate scope — not GSS.
- **Staff "keying in"** card on merchant admin panel = CHD on your systems.
- **Provider change** — revalidate AOC and SAQ type annually and on vendor switch.

## When NOT to use

- Business requirement to own entire checkout UX with raw card API — accept full PCI program.
- Provider lacks current PCI validation — no scope magic.

## Related

[[Payments/SAQ GSS]] [[Payments/payment gateway]] [[Payments/PSP]] [[Payments/Strip]] [[Security/TLS (Transport Layer Security)]]
