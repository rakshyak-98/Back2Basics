[[DNS]] [[DNS zone]] [[mail server]] [[SMTP]]

# DSN records

> DNS records — rows in a zone that tell resolvers where a name points (A/AAAA), who receives mail (MX), which NS is authoritative, and more.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Records]]
- [[#MX]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** A name is not an IP — records are typed answers (`A`, `MX`, `TXT`, …) stored on authoritative servers and cached by resolvers for a TTL.

```txt
example.com
├── A      → 203.0.113.10
├── AAAA   → 2001:db8::1
├── MX     → mail.example.com
├── NS     → ns1.example.com
├── TXT    → "v=spf1 ..."
├── CNAME  → target.example.net
└── SRV    → _service._tcp → host:port
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **RRset** | All records of one type at a name | “TTL and DNSSEC apply to the RRset.” |
| **TTL** | How long resolvers may cache | “Low TTL = faster change, more query load.” |
| **Apex** | Zone root (`example.com`) | “CNAME at apex is usually forbidden.” |
| **MX** | Mail routing hostname | “MX is a name; you still need A/AAAA.” |
| **TXT** | Free-form; SPF/DKIM/verification | “Auth for email and domain proofs.” |

---

## Standard config / commands

```bash
dig example.com A +noall +answer
dig example.com MX
dig example.com NS
dig example.com TXT
dig www.example.com CNAME
dig -t CAA example.com

# Trace delegation
dig +trace example.com
```

| Knob | Why it matters |
|------|----------------|
| TTL | Cut for cutovers; raise for stable apex |
| Multiple A/AAAA | Simple client load spread (not a full LB) |
| CAA | Limits which CAs may issue certs |

---

## Records

| Type | Job |
|------|-----|
| **A** | Name → IPv4 |
| **AAAA** | Name → IPv6 |
| **CNAME** | Alias → another name (no other types at that node) |
| **MX** | Who accepts mail for the domain |
| **NS** | Authoritative nameservers for the zone |
| **TXT** | SPF, DKIM, domain verification, misc |
| **CAA** | Allowed certificate authorities |
| **SRV** | Service location (host + port + priority) |
| **SOA** | Zone metadata (serial, timers, primary) |

Also see [[dns record]] and [[DNS zone]].

---

## MX

MX points to a **hostname**, not an IP. Delivery path:

```txt
send to alice@example.com
   → dig MX example.com  → mail.example.com
   → dig A mail.example.com → 203.0.113.50
   → [[SMTP]] connect
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Site IP wrong after change | TTL / old cache | Wait TTL; flush local; lower TTL before next cut |
| Mail won’t deliver | MX + A for MX host | Fix MX target; add A/AAAA; check PTR |
| CNAME + other records | Apex CNAME conflict | Use ALIAS/ANAME at provider or A/AAAA at apex |
| SPF fail | TXT `v=spf1` | Align sending IPs; avoid too many lookups |
| Cert issuance denied | CAA | Add CA; wait TTL |
| Some regions old data | Secondary lag | Check serial/NOTIFY/AXFR |

---

## Gotchas

> [!WARNING]
> **Filename “DSN” is a typo — these are DNS records** (DSN also means Delivery Status Notification in mail — different thing).

> [!WARNING]
> **CNAME cannot coexist** with NS/MX/A at the same node — classic apex footgun.

> [!WARNING]
> **MX → CNAME** — discouraged; point MX at a real A/AAAA name.

---

## When NOT to use

- **App config that changes every second** — use a service registry; DNS TTL is a poor control plane.
- **Secrets** — TXT is world-readable; don’t put passwords in DNS.
- **Geo traffic steering beyond basics** — need GSLB/Anycast product, not one A record.

---

## Related

[[DNS]] [[dns record]] [[DNS zone]] [[name server]] [[mail server]] [[SMTP]] [[cloudflare]]
