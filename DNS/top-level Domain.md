[[DNS]] [[DNS zone]] [[name server]] [[Route53]] [[Sub Domain]] [[cloudflare]]

# top-level Domain

> A top-level domain (TLD) is the rightmost public label in a DNS name (`example.com` → TLD is `com`) — IANA delegates each TLD to a registry that sets registration policy and operates its nameservers.

```txt
        top-level Domain ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers distinguish registry vs registrar, gTLD vs ccTLD policy, and why…

## Sources
- [IANA — Top-Level Domains](https://www.iana.org/domains) — overview
- [IANA Root Zone Database](https://www.iana.org/domains/root/db) — deep-dive
- [ICANN — How DNS works](https://www.icann.org/resources/pages/dns-what-is-2021-02-25-en) — overview

## Key Concepts
- **Registry:** operates the TLD zone and sets eligibility rules.
- **Registrar:** sells second-level names under a TLD and updates registry data / glue.
- **Categories:** gTLD, ccTLD, sponsored, new gTLD — policies and HSTS preload differ.
- **Delegation:** TLD NS point at your chosen authoritative [[name server]]s for `example.com`.

## Technical Details
| Category | Examples | Notes |
|----------|----------|-------|
| **Generic (gTLD)** | `.com`, `.org`, `.net`, `.io` | ICANN-contracted registries |
| **Country-code (ccTLD)** | `.uk`, `.de`, `.jp` | National policies vary |
| **Sponsored** | `.edu`, `.gov`, `.museum` | Restricted eligibility |
| **New gTLD** | `.dev`, `.app`, `.cloud` | Often HSTS-preloaded by browsers |

```
. (root)
 └── com (TLD)  NS → Verisign / .com operators
      └── example.com  NS → your DNS host ([[Route53]], [[cloudflare]], [[BIND]])
```

- Registrars (GoDaddy, Route 53 Registrar, etc.) sell **second-level** names un…

- **Operational implications:** 

- **Propagation:** — NS changes at TLD can take hours; plan TTL reduction before migration.
- **ccTLD rules:** — some require local presence or specific [[name server]] counts.
- **Private TLD confusion:** — do not invent `corp.local` as if it were a public TLD

- **Security:** DNSSEC at root and many TLDs validates chain of trust downward

## Mistakes to Avoid
- **Mistake:** Confusing registry (runs `.com`) with registrar (sells `example.…
- **Mistake:** Inventing `corp.local` as a faux public TLD instead of a private…
- **Mistake:** Changing TLD nameservers without overlapping TTLs and dual hosti…

## Pros/Cons or Trade-offs
- **Pro:** Shared global namespace under ICANN/IANA governance.
- **Con:** ccTLD and sponsored TLDs add eligibility and nameserver constraints.
- **Con:** TLD NS changes are slow and affect the entire domain subtree.

## Comparison
- vs [[Sub Domain]]: TLD is the public suffix layer
- vs root zone: root delegates TLDs; TLDs delegate registrant zones.


### Use cases
- Choosing `.com` vs `.io` vs ccTLD for product branding

- **Example:** Lower apex TTL, dual-publish records at old and new DNS hosts, t…
