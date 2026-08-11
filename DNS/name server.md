[[DNS]] [[DNS zone]] [[DNS server]] [[DSN records]]

# name server

> Name server — authoritative DNS server that stores and answers the official records for a zone (what NS records point at).

---

## Mental model

**Say it in one breath:** Resolvers follow NS delegations until they hit a name server that is **authoritative** for `example.com` and returns A/MX/TXT from that zone — not a recursive cache guessing.

```txt
Root → TLD (.com) → NS ns1.dns-provider.com (authoritative for example.com)
                              │
                         answers A/MX/...
```

```txt
example.com.    3600   IN   NS   ns1.dns-provider.com.
example.com.    3600   IN   NS   ns2.dns-provider.com.
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Authoritative** | Has the zone’s official data | “AA bit set — this is the source.” |
| **Delegation** | Parent NS points to child NS | “Registrar NS set must match zone NS.” |
| **Primary / secondary** | Hidden master vs AXFR slaves | “Secondaries copy; primaries edit.” |
| **Glue** | A/AAAA for NS inside the child zone | “Without glue, chicken-and-egg.” |
| **Recursive resolver** | Different role — walks the tree for clients | “Unbound/8.8.8.8 are not your NS.” |

---

## Standard config / commands

```bash
dig +short NS example.com
dig NS example.com @a.gtld-servers.net   # what the parent delegates
dig example.com SOA
dig +nssearch example.com

# Compare parent delegation vs apex NS RRset
dig NS example.com @ns1.dns-provider.com
```

| Knob | Why it matters |
|------|----------------|
| ≥2 NS on different networks | Single NS outage = domain dark |
| SOA serial | Secondaries and operators use it for change tracking |
| NOTIFY/AXFR ACLs | Leaks and stale secondaries |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Domain works at registrar dig, not public | Parent NS ≠ zone NS | Align delegation at registrar |
| SERVFAIL | Auth down / lame delegation | Fix NS targets; heal primaries |
| Stale answers on one NS | Secondary not transferring | Fix AXFR/TSIG; bump serial; NOTIFY |
| NS hostname won’t resolve | Missing glue | Add glue A/AAAA at parent |
| Slow failover | High NS TTLs | Lower before maintenance; diversify anycast |

---

## Gotchas

> [!WARNING]
> **Lame delegation** — parent points at a host that doesn’t answer authoritatively for the zone.

> [!WARNING]
> **Registrar “nameservers” UI** — that edits *delegation*, not necessarily your zone file contents.

> [!WARNING]
> **Using a recursive IP as NS** — looks fine in a browser cache test; breaks AA and DNSSEC.

---

## When NOT to use

- **You only need to resolve other people’s domains** — run a recursive ([[Unbound]]), not authoritative NS.
- **Kubernetes ClusterIP names** — [[CoreDNS]] in-cluster, not public name servers.
- **One-off local aliases** — `/etc/hosts` or [[dnsmasq]] for a laptop lab.

---

## Related

[[DNS]] [[DNS zone]] [[DNS server]] [[DSN records]] [[BIND]] [[PoserDNS]] [[public resolver]]
