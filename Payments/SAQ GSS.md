[[Payments/PSI GSS]] [[Payments/payment gateway]] [[Payments/PSP]] [[Security/TLS (Transport Layer Security)]]

# SAQ GSS (Self-Assessment Questionnaire — Guest Service System)

> PCI DSS self-assessment path when checkout is fully outsourced — merchant attests reduced cardholder-data environment — **PCI SSC SAQ programs**.

## Mental model

**SAQ** = merchant self-assessment against PCI DSS controls. **GSS (Guest Service System)** path applies when **all** payment acceptance is delegated to a validated third party — aligns with minimal-scope questionnaires (commonly **SAQ A** or provider-specific guidance).

```
Merchant environment          Provider hosted checkout
┌─────────────────────┐      ┌──────────────────────────┐
│ Web/app servers     │      │ Card entry + processing  │
│ NO CHD storage      │ ───► │ PCI validated PSP        │
│ Tokens/webhooks only│      │ AOC on file              │
└─────────────────────┘      └──────────────────────────┘
         │
         └── annual SAQ GSS/A + ASV scans if required
```

Pair with [[Payments/PSI GSS]] for technical architecture that qualifies.

## Standard config / commands

### SAQ selection (simplified — confirm with QSA/acquirer)

| Scenario | Typical SAQ |
|----------|-------------|
| Fully outsourced redirect checkout | SAQ A |
| Embedded fields, JS from PSP, no CHD on merchant | Often SAQ A-EP — verify with acquirer |
| Merchant stores/processes PAN | SAQ D |

### Annual compliance workflow

```text
1. Confirm architecture still matches GSS (no scope creep)
2. Collect PSP AOC + responsibility matrix
3. Complete correct SAQ (GSS/A variant per PCI SSC current docs)
4. ASV external scan if SAQ requires (usually N/A for pure SAQ A)
5. Submit to acquirer; retain evidence 3+ years
6. Security awareness training for staff (PCI req 12.6)
```

### Evidence pack

- Network diagram (CHD flows)
- Policies: incident response, access control, logging
- Pen test / vuln scan results if applicable
- Change tickets proving no PAN fields added to DB

### Merchant attestation fields

Officer signs attestation that:

- Listed controls implemented
- No prohibited storage of sensitive authentication data (CVV post-auth)
- Service providers PCI compliant

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Acquirer demands SAQ D | Scope creep | Architecture review; remove PAN touchpoints |
| Failed ASV scan | Merchant IP in scope | Fix vulns or clarify scan scope with ASV |
| Expired SAQ | Calendar | Recomplete before deadline — fines possible |
| Wrong SAQ version | PCI SSC updates | Download current PDF from pcisecuritystandards.org |
| M&A due diligence fail | Missing AOC chain | Collect subprocessors list |

## Gotchas

> [!WARNING]
> **SAQ GSS is not "no security"** — still patch servers, secure admin access, validate webhooks.

- **E-commerce + call center** mixed models — phone capture may blow GSS eligibility.
- **Multi-PSP** — each must be in scope documentation.
- **Logs/traces** accidentally capturing query params with tokens — rotate and redact.

## When NOT to use

- Any system component receives, stores, or transmits full PAN — SAQ GSS path invalid; use appropriate full SAQ.

## Related

[[Payments/PSI GSS]] [[Payments/payment gateway]] [[Payments/PSP]] [[Payments/Strip]] [[Security/TLS (Transport Layer Security)]]
