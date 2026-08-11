[[DNS]] [[DNS server]] [[Unbound]] [[BIND]]

# PoserDNS

> PowerDNS — split DNS stack: Authoritative answers your zones, Recursor walks the internet, optional dnsdist load-balances and shields them.

---

## Mental model

**Say it in one breath:** PowerDNS is modular — don’t run one god-daemon; put authoritative, recursive, and (optionally) dnsdist on the roles they fit. Zones often live in MySQL/Postgres instead of only flat files.

```txt
Client → dnsdist (optional) ┬→ Authoritative (your domains, DB/API)
                            └→ Recursor (resolve the rest, DNSSEC)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Authoritative** | Serves zones you own | “Hosting customers’ domains on PDNS Auth.” |
| **Recursor** | Resolves for clients | “Like [[Unbound]], but PowerDNS Recursor.” |
| **dnsdist** | DNS LB / filter / DoH-DoT front | “DDoS and policy sit in dnsdist.” |
| **Backend** | Where records live (gmysql, gpgsql, bind) | “We drive DNS from the provisioning DB.” |
| **API** | HTTP control plane | “Automation without editing zone files.” |

### vs peers

| Need | Typical pick |
|------|----------------|
| Classic file zones | [[BIND]] |
| Validating recursive only | [[Unbound]] |
| DB-backed authoritative + API | PowerDNS Authoritative |
| K8s service discovery | [[CoreDNS]] |

---

## Standard config / commands

```bash
# Packages differ by distro — auth vs recursor vs dnsdist are separate
pdns_control ping
pdns_control list-zones
dig @127.0.0.1 example.com SOA

# Recursor
rec_control get-qty queries
dig @127.0.0.1 google.com
```

```ini
# Authoritative sketch — gmysql backend
launch=gmysql
gmysql-host=127.0.0.1
gmysql-user=pdns
gmysql-password=...
gmysql-dbname=pdns
api=yes
api-key=...
webserver=yes
```

| Knob | Why it matters |
|------|----------------|
| Separate auth vs recursive IPs | Mixing roles on one VIP confuses ops and attackers |
| DNSSEC keys in DB | Backup and rollover procedures required |
| dnsdist rules | Bad ACL → open resolver or blocked customers |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NXDOMAIN for your domain | Auth not loaded / wrong backend | `list-zones`; DB connectivity; SOA serial |
| Clients resolve slowly | Recursor upstream / RPZ | Check `rec_control`; root priming; forwarding |
| API 401 | api-key / webserver bind | Fix key; bind to mgmt network only |
| SERVFAIL on signed zones | DNSSEC break | Validate DS/DNSKEY chain; check clocks |
| Sudden traffic spike | Abuse / open recursive | Close recursion; put dnsdist rate limits |
| Zone update not visible | Serial / NOTIFY / cache | Bump serial; NOTIFY secondaries; flush caches |

---

## Gotchas

> [!WARNING]
> **Filename says PoserDNS — product is PowerDNS** — search docs under PowerDNS.

> [!WARNING]
> **Open resolver** — a Recursor on `0.0.0.0` without ACL becomes an amplification node.

> [!WARNING]
> **Auth ≠ Recursor config** — wrong daemon, wrong package, wrong control socket.

---

## When NOT to use

- **Tiny home LAN** — [[dnsmasq]] is enough.
- **Only need validating recursive** — [[Unbound]] is leaner.
- **Kubernetes-only DNS** — [[CoreDNS]] is the native fit.

---

## Related

[[DNS server]] [[DNS]] [[DNS zone]] [[BIND]] [[Unbound]] [[CoreDNS]] [[dnsmasq]] [[dns record]] [[DSN records]]
