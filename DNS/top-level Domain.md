[[DNS]] · [[DNS zone]] · [[name server]] · [[Route53]] · [[Sub Domain]]

# top-level Domain

> A top-level domain (TLD) is the rightmost public label in a DNS name (`example.com` → TLD is `com`) — IANA delegates each TLD to a registry that sets registration policy and operates its nameservers.

---

## TLD categories

| Category | Examples | Notes |
|----------|----------|-------|
| **Generic (gTLD)** | `.com`, `.org`, `.net`, `.io` | ICANN-contracted registries |
| **Country-code (ccTLD)** | `.uk`, `.de`, `.jp` | National policies vary |
| **Sponsored** | `.edu`, `.gov`, `.museum` | Restricted eligibility |
| **New gTLD** | `.dev`, `.app`, `.cloud` | Often HSTS-preloaded by browsers |

Full list maintained by [IANA Root Zone Database](https://www.iana.org/domains/root/db).

## Delegation chain

```
. (root)
 └── com (TLD)  NS → Verisign / .com operators
      └── example.com  NS → your DNS host ([[Route53]], [[cloudflare]], [[BIND]])
```

Registrars (GoDaddy, Route 53 Registrar, etc.) sell **second-level** names under a TLD; they update registry data and provide glue for your [[name server]] choice.

## Operational implications

- **Propagation** — NS changes at TLD can take hours; plan TTL reduction before migration.
- **ccTLD rules** — some require local presence or specific [[name server]] counts.
- **Private TLD confusion** — do not invent `corp.local` as if it were a public TLD; use proper internal zones ([[DNS zone]]).

## Security

- **DNSSEC** at root and many TLDs validates chain of trust downward.
- **Certificate Transparency** and **CAA** records reduce mis-issuance risk for your domain under any TLD.

## Recall

- What is the difference between a registry and a registrar?
- Why does changing TLD nameservers affect the entire domain subtree?

## Sources

- [IANA — Top-Level Domains](https://www.iana.org/domains)
- [ICANN — How DNS works](https://www.icann.org/resources/pages/dns-what-is-2021-02-25-en)
