[[DNS]] · [[dns record]] · [[name server]] · [[BIND]] · [[Route53]]

# DNS zone

> A DNS zone is the contiguous portion of the DNS tree administered as one unit with a single SOA record — split zones when delegation, compliance, or blast-radius boundaries require it.

---

## Zone vs domain

A **domain** is a name in the tree (`example.com`). A **zone** is what you load into a nameserver: all records for which this server is **authoritative**, ending at delegation boundaries (child `NS` records).

```
example.com zone
├── SOA, NS for example.com
├── www.example.com A
├── api.example.com A
└── delegates sub.example.com ──► separate zone on other NS
```

## SOA record fields

```
example.com. IN SOA ns1.example.com. hostmaster.example.com. (
  2026081301  ; serial (bump on every change)
  7200        ; refresh
  3600        ; retry
  1209600     ; expire
  300 )       ; minimum TTL
```

Serial format often `YYYYMMDDnn`. Secondary servers poll SOA serial for zone transfers (AXFR/IXFR).

## Public vs private zones

| Type | Resolves where |
|------|----------------|
| **Public** | Global Internet via registrar NS delegation |
| **Private** (Split-horizon) | Inside VPC/corporate resolver only — same name may differ from public |

[[Route53]] private hosted zones associate with VPCs. [[BIND]] views implement split DNS on self-hosted servers.

## Zone file operations

```bash
# BIND example
named-checkzone example.com /etc/bind/db.example.com
rndc reload example.com
```

Cloud operators use APIs ([[Route53]], [[cloudflare]]) instead of zone files.

## Delegation

Parent zone publishes `NS` + glue `A/AAAA` for child nameservers. Broken delegation (missing glue, wrong NS) makes the child zone unreachable.

```bash
dig +trace sub.example.com
```

## Recall

- What triggers a secondary server to pull a zone update?
- When would you split `api.example.com` into its own zone?

## Sources

- [RFC 1035 — Zones and zone transfers](https://datatracker.ietf.org/doc/html/rfc1035)
- [BIND 9 Administrator Reference Manual — zones](https://bind9.readthedocs.io/)
