[[DNS]] [[DNS zone]] [[name server]] [[top-level Domain]] [[Route53]]

# Top-Level Domain (TLD)

> **Rightmost DNS label** in a name (`example.com` → TLD is `com`) — delegated by root, operated by registry, sold by registrars. Matters for DNSSEC, resolver behavior, and policy (who can register what).

## Mental model

The DNS tree is hierarchical: **root (`.`)** → **TLD** (`.com`, `.org`, `.uk`) → **SLD** (`example` in `example.com`) → subdomains (`www`). **ICANN** policy; **registry** runs TLD nameservers; **registrar** (GoDaddy, Route53 Registrar) is where you pay and set **delegation NS**.

```
. (root) ──► .com (TLD) ──► example.com (registered zone) ──► www.example.com
                  │
                  └── NS glue at parent points to authoritative servers
```

**gTLD** (`.com`, `.dev`) vs **ccTLD** (`.uk`, `.de`) — ccTLD often has residency/eligibility rules. **Public suffix** list defines cookie/site boundaries (`co.uk` is suffix, not registrable `uk` alone).

## Standard config / commands

### Delegation (what actually makes a TLD "work" for you)

| Step | Action | Where |
|------|--------|-------|
| Register | Buy `example.com` | Registrar |
| Host DNS | Create zone; get NS records | Route53, Cloudflare, BIND |
| Delegate | Set NS at registrar → zone NS | Registrar panel |
| Verify | `dig NS example.com +trace` | CLI |

```bash
# Trace delegation chain to authoritative
dig +trace example.com A

# Which TLD/registrar (RDAP/WHOIS)
whois example.com | grep -i 'Name Server\|Registrar'

# Public Suffix check (cookie domain scope)
# https://publicsuffix.org/ — e.g. app.herokuapp.com is NOT a registrable "TLD"
```

### Choosing TLD (engineering lens)

- **`.dev`** — HSTS preload eligible (HTTPS-only expectation).
- **`.app`** — similar HTTPS-leaning policies on some resolvers.
- **Brand TLD** — marketing; same DNS mechanics, higher cost.

### Subdomain vs separate domain

- `api.example.com` — same zone, same cert SAN/wildcard `*.example.com`.
- `example.io` — separate zone, separate DNSSEC/DMARC lifecycle.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Domain "not found" / NXDOMAIN | Registration expired; wrong TLD spelling | Renew; verify WHOIS |
| Partial global resolution | NS mismatch at registrar vs zone | Align NS; wait TTL (up to 48h) |
| `com` works, `co.uk` cookie weird | Public suffix rules | Set `Domain=` cookie per eTLD+1 rules |
| DNSSEC SERVFAIL | DS record at registrar stale | Update DS after KSK rollover |
| Email SPF/DMARC fail on new TLD | No MX/TXT at delegation | Add records at authoritative zone |
| Internal "TLD" collision | Using `.local` / `.corp` on internet | Use `.internal` (RFC 6762 guidance) or subdomain under owned domain |

## Gotchas

> [!WARNING]
> **Registrar ≠ DNS host** — expiry at registrar kills delegation even if Route53 zone exists.

> [!WARNING]
> **ccTLD transfer locks** — some require local presence; plan migrations early.

> [!WARNING]
> **Wildcard cert doesn't cross TLD** — `*.example.com` doesn't cover `example.io`.

> [!WARNING]
> **Split-horizon + public TLD** — don't register fake public TLD for internal use; use private zones ([[DNS zone]]).

## When NOT to use

- **Debating TLD for infra** — pick one registered domain; use subdomains for envs (`staging.example.com`).
- **Deep TLD policy research in ops runbooks** — registrar support for disputes; ops cares about NS and TTL.

## Related

[[DNS]] · [[DNS zone]] · [[name server]] · [[Route53]] · [[cloudflare]] · [[mDNS]]
