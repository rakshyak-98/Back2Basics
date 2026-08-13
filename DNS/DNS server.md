<!-- note-strategy: operational -->
[[DNS]] [[name server]] [[DNS zone]] [[DSN records]] [[Unbound]]

# DNS server

> DNS server — process that answers DNS queries on port 53 — either authoritative for zones you own, or recursive/caching for clients.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Clients ask a DNS server “what’s the A for `api.example.com`?” — an **authoritative** server answers from its zone; a **recursive** server walks the hierarchy (or forwards) and caches.

```txt
App → stub (/etc/resolv.conf)
        → recursive ([[Unbound]], 8.8.8.8, corp DNS)
             → root → TLD → authoritative [[name server]]
        ← A/AAAA/MX/… ([[DSN records]])
```

| Role | Listens for | Software examples |
|------|-------------|-------------------|
| Authoritative | Queries for *your* zones | [[BIND]], PowerDNS Auth ([[PoserDNS]]), NSD |
| Recursive / caching | Client lookups for *everything* | [[Unbound]], BIND recursive, PowerDNS Recursor |
| Both on one box | Possible but separate IPs/ACLs | Avoid open recursion on auth VIPs |
| Cluster / LAN helpers | Local names + forward | [[CoreDNS]], [[dnsmasq]] |

Port **53** UDP (and TCP for large/AXFR). Not an HTTP server.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Authoritative** | Source of truth for a zone | “We host NS for example.com.” |
| **Recursive** | Finds answers for clients | “Stub resolvers talk to a recursive.” |
| **Forwarder** | Recursive that asks upstream only | “Branch office forwards to HQ DNS.” |
| **Open resolver** | Recurses for the world | “Amplification risk — ACL it.” |
| **Zone** | Set of records under a domain | “Stored as files or in a DB.” |

---

## Standard config / commands

```bash
ss -ulnp | grep ':53'
dig @127.0.0.1 example.com A
dig @127.0.0.1 example.com SOA
dig +tcp @127.0.0.1 example.com

# Is this server authoritative?
dig example.com A @ns1.example.com   # expect AA flag in header
```

| Knob | Why it matters |
|------|----------------|
| Listen address / ACL | Bind to internal NIC; don’t open recursion to `0.0.0.0/0` |
| UDP + TCP 53 | Truncation and zone transfers need TCP |
| Query logging | Debug storms; watch PII/retention |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Timeout to :53 | Process down / firewall | Start daemon; allow 53/udp+tcp |
| NXDOMAIN for your domain | Wrong role / empty zone | Load zone on auth; fix NS delegation |
| SERVFAIL | Upstream / DNSSEC / loop | Check forwarders; fix validation; break loops |
| Works for IP, not name | Client resolv.conf | Fix stub servers; DHCP DNS options |
| Intermittent wrong IP | Cache TTL / multi-NS skew | Align secondaries; lower TTL for cutover |
| Reflection abuse | Open recursive | `allow-recursion` / views; firewall |

---

## Gotchas

> [!WARNING]
> **One machine *can* do both roles** — still split addresses and ACLs so the internet can’t recurse through your auth IP.

> [!WARNING]
> **systemd-resolved stub on 127.0.0.53** — apps aren’t talking to your real DNS server until you check the path.

> [!WARNING]
> **Docker embeds 127.0.0.11** — container DNS failures are often daemon config, not “the corporate DNS server.”

---

## When NOT to use

- **You only need a public lookup from a laptop** — use an existing [[public resolver]]; don’t stand up infra.
- **Service discovery inside K8s only** — [[CoreDNS]], not a second BIND for ClusterIP names.
- **Storing non-DNS data** — directories and DBs exist; DNS is a lookup cache hierarchy.

---

## Related

[[DNS]] [[name server]] [[DNS zone]] [[DSN records]] [[Unbound]] [[BIND]] [[CoreDNS]] [[dnsmasq]] [[PoserDNS]] [[public resolver]]
