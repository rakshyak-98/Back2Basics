[[DNS]] [[DNS zone]] [[DSN records]] [[name server]] [[top-level Domain]]

# Sub Domain

> Subdomain — a name under your zone (`api.example.com`) with its own records — or a delegated child zone with its own NS.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#DNS record]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `api.example.com` is just another owner name in the `example.com` [[DNS zone]] (usually an A/AAAA/CNAME) — unless you **delegate** it with NS records to another name server.

```txt
example.com (zone)
├── www     A/CNAME     ← subdomain label in same zone
├── api     A
└── corp    NS ns1.other…  ← delegated subdomain (child zone)
```

Browser types `https://api.example.com` → stub resolver asks recursive → authoritative returns records for that label.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Label** | One hop (`api`) | “Subdomain is a label under the parent.” |
| **Zone cut** | Delegation via NS | “Child has its own SOA and NS.” |
| **Glue** | A/AAAA for in-bailiwick NS | “Needed when NS lives under the child.” |
| **Wildcard** | `*.example.com` | “Matches one label; not a substitute for real names.” |
| **TTL** | Cache lifetime | “Cut TTL before a subdomain migration.” |

---

## Standard config / commands

```bash
# Same-zone subdomain
dig +short api.example.com A
dig api.example.com ANY +noall +answer

# Is it delegated?
dig NS api.example.com
dig +trace api.example.com
```

```txt
; in example.com zone — simple subdomain
api     300  IN  A      203.0.113.20
www     300  IN  CNAME  api.example.com.

; delegated subdomain
corp    3600 IN  NS     ns1.corp-dns.net.
corp    3600 IN  NS     ns2.corp-dns.net.
```

| Knob | Why it matters |
|------|----------------|
| CNAME vs A | CNAME can’t sit with other types at that node |
| Delegation NS | Wrong NS = corp.example.com black hole |
| Certificates | Each hostname needs SAN/coverage |

---

## DNS record

| Type | Role for subdomains |
|------|---------------------|
| **A / AAAA** | Point host to address |
| **CNAME** | Alias to another hostname |
| **MX** | Mail for that name (rare on deep subs) |
| **NS** | Delegate a child zone |
| **SOA** | Present at zone apex (parent or child) |

Authoritative server = the DNS server with the official answers for that zone’s records.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NXDOMAIN for `api.` | Record missing / wrong zone | Add A/AAAA/CNAME; publish serial |
| Parent works, child dead | Broken delegation | Fix child NS + glue; check child SOA |
| Some users hit old IP | TTL | Wait/flush; lower TTL next time |
| Cert name mismatch | Hostname not on cert | Reissue with SAN for subdomain |
| Wildcard not matching `a.b.example.com` | `*` is one label | Add explicit name or `*.b.example.com` |

---

## Gotchas

> [!WARNING]
> **Delegation orphans** — parent NS points at child that isn’t configured; looks like random SERVFAIL.

> [!WARNING]
> **`www` as CNAME to apex** — fine; **apex as CNAME** — usually not (use ALIAS/ANAME or A/AAAA).

> [!WARNING]
> **Cookie / CORS / TLS are per-hostname** — a subdomain is a different security origin.

---

## When NOT to use

- **Per-tenant isolation on the public internet** — careful with cookie scope and wildcards; sometimes separate registrable domains.
- **Replacing service discovery inside a mesh** — use mesh DNS/CoreDNS, not public subdomain sprawl.
- **Secrets in hostname labels** — names appear in logs and Cert transparency.

---

## Related

[[DNS]] [[DNS zone]] [[DSN records]] [[dns record]] [[name server]] [[top-level Domain]] [[cloudflare]]
