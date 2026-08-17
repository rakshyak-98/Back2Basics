[[DNS]] [[dns record]] [[name server]] [[BIND]] [[Route53]] [[Sub Domain]]

# DNS zone

> A DNS zone is the contiguous portion of the DNS tree administered as one unit with a single SOA record — split zones when delegation, compliance, or blast-radius boundaries require it.





## Interview Relevance
Interviewers want zone vs domain clarity, SOA serial/transfer behavior, and when to delegate a child zone — classic ops and systems design signal.

## Sources
- [RFC 1035 — Zones and zone transfers](https://datatracker.ietf.org/doc/html/rfc1035) — deep-dive
- [BIND 9 Administrator Reference Manual — zones](https://bind9.readthedocs.io/) — deep-dive

## Core Definition
A **domain** is a name in the tree (`example.com`). A **zone** is what you load into a nameserver: all records for which this server is **authoritative**, ending at delegation boundaries (child `NS` records).

## Key Concepts
- **SOA:** one per zone — serial, refresh, retry, expire, minimum TTL drive secondary sync.
- **Delegation boundary:** child NS records end the parent zone’s authority for that subtree.
- **Public vs private:** same name can answer differently inside VPC/corporate resolvers (split-horizon).
- **Transfers:** AXFR/IXFR move zone data primary → secondary after NOTIFY or SOA poll.

## Technical Details
```
example.com zone
├── SOA, NS for example.com
├── www.example.com A
├── api.example.com A
└── delegates sub.example.com ──► separate zone on other NS
```

```
example.com. IN SOA ns1.example.com. hostmaster.example.com. (
  2026081301  ; serial (bump on every change)
  7200        ; refresh
  3600        ; retry
  1209600     ; expire
  300 )       ; minimum TTL
```

Serial format often `YYYYMMDDnn`. Secondary servers poll SOA serial for zone transfers (AXFR/IXFR).

| Type | Resolves where |
|------|----------------|
| **Public** | Global Internet via registrar NS delegation |
| **Private** (Split-horizon) | Inside VPC/corporate resolver only — same name may differ from public |

[[Route53]] private hosted zones associate with VPCs. [[BIND]] views implement split DNS on self-hosted servers.

```bash
# BIND example
named-checkzone example.com /etc/bind/db.example.com
rndc reload example.com
dig +trace sub.example.com
```

Cloud operators use APIs ([[Route53]], [[cloudflare]]) instead of zone files. Parent zone publishes `NS` + glue `A/AAAA` for child nameservers — broken delegation (missing glue, wrong NS) makes the child unreachable.

## Real-World Applications
Registrar NS point at your hosted zone; teams often split `staging.` or `corp.` into separate zones for ownership.

**Example:** Marketing keeps `example.com` at Cloudflare; platform owns `api.example.com` via NS delegation to Route 53 — each team’s blast radius stops at the delegation cut.

## Pros/Cons or Trade-offs
- **Pro:** Clear admin boundary and SOA-driven replication to secondaries.
- **Con:** Extra zones mean glue, DS/DNSSEC, and monitoring per cut — oversplitting adds ops cost.
- **Con:** Split-horizon bugs — clients leak wrong answers across network edges.

## Comparison
- vs domain: domain is a name; zone is the authoritative dataset for a contiguous cut of the tree.
- vs [[Sub Domain]]: a subdomain may live as records in the parent zone or as its own delegated zone.

## Mistakes to Avoid
- Forgetting to bump SOA serial after edits — secondaries never pull.
- Missing glue A/AAAA for in-bailiwick NS hosts — child zone fails to resolve.
- Treating “zone” and “domain” as synonyms when debugging delegation.
