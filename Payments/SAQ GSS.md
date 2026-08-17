[[PSI GSS]] [[payment gateway]] [[PSP]] [[Strip]] [[TLS (Transport Layer Security)]]

# SAQ GSS (Self-Assessment Questionnaire — Guest Service System)

> PCI DSS self-assessment when checkout is fully outsourced — the merchant attests a reduced cardholder-data environment using the correct SAQ (often SAQ A / A-EP class).

```txt
        SAQ GSS (Self-Asse ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask which SAQ fits hosted redirect versus embedded fields versus…

## Sources
- [PCI SSC — SAQ instructions and guidelines](https://www.pcisecuritystandards.org/document_library/) — deep-dive
- [PCI SSC — Official SAQ forms](https://www.pcisecuritystandards.org/) — deep-dive
- [Wikipedia — PCI DSS](https://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard) — overview

## Key Concepts
- **Core:** An SAQ is a merchant-completed questionnaire matching a defined eligibility p…

## Technical Details
```
Merchant environment          Provider hosted checkout
┌─────────────────────┐      ┌──────────────────────────┐
│ Web/app servers     │      │ Card entry + processing  │
│ NO CHD storage      │ ───► │ PCI validated PSP        │
│ Tokens/webhooks only│      │ AOC on file              │
└─────────────────────┘      └──────────────────────────┘
         │
         └── annual SAQ (A / GSS-aligned) + scans if required
```

| Scenario | Typical SAQ |
|----------|-------------|
| Fully outsourced redirect checkout | SAQ A |
| Embedded provider fields, no CHD on merchant | Often SAQ A or A-EP — verify with acquirer |
| Merchant stores/processes PAN | SAQ D |

```text
1. Confirm architecture still matches GSS (no scope creep)
2. Collect PSP AOC + responsibility matrix
3. Complete correct current SAQ from PCI SSC
4. ASV external scan if the SAQ requires it
5. Submit to acquirer; retain evidence 3+ years
6. Security awareness training for staff (PCI req 12.x)
```

- Officer attestation typically covers: listed controls implemented

| Symptom | Check | Fix |
|---------|-------|-----|
| Acquirer demands SAQ D | Scope creep | Architecture review; remove PAN touchpoints |
| Failed ASV scan | Merchant IP in scope | Fix vulns or clarify scan scope |
| Expired SAQ | Calendar | Recomplete before deadline |
| Wrong SAQ version | PCI SSC updates | Download current PDF |
| M&A diligence fail | Missing AOC chain | Collect subprocessors list |

## Mistakes to Avoid
- **Mistake:** Treating SAQ GSS/A as a paperwork-only exercise while PAN sits i…
- **Mistake:** Using an outdated SAQ PDF after a PCI SSC revision
- **Mistake:** Mixing phone (MOTO) card capture with “hosted-only” claims
- **Mistake:** Forgetting multi-PSP documentation when several providers are in…
- **Mistake:** Skipping re-attestation after a provider or architecture change

## Pros/Cons or Trade-offs
- **Pro:** Shortest path when architecture truly outsources CHD.
- **Con:** Not “no security” — patch servers, lock admin access, validate webhooks.
- **Con:** Mixed e-commerce + call-center capture often breaks eligibility.

## Comparison
- vs [[PSI GSS]]: questionnaire versus technical pattern — both required.
- vs SAQ D: full program when any system component handles PAN.
- vs QSA on-site assessment: large merchants / service providers may need more than SAQ.


### Use cases
- Hotel brands and franchises attesting guest web booking, franchisees using co…

- **Example:** Acquirer rejects “SAQ A” because the booking API accepted `cardN…
