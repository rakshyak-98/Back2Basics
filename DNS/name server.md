[[DNS]] · [[DNS zone]] · [[dns record]] · [[BIND]] · [[Unbound]]

# name server

> A nameserver answers DNS queries for zones it is authoritative for, or recursively resolves names on behalf of clients — confuse the two roles and you will open an open resolver or break delegation.

---

## Roles

| Role | Behavior |
|------|----------|
| **Authoritative** | Answers from zone data (primary or secondary) |
| **Recursive (resolver)** | Walks the tree starting at root hints; caches answers |
| **Stub resolver** | Forwards to configured recursive resolver |

An open recursive server on the public Internet amplifies DDoS — lock down [[Unbound]] and [[BIND]] recursion to trusted networks.

## Authoritative tiers in the global tree

```
Root (.)  →  TLD (.com, .org)  →  Registrant zone (example.com)
```

Each level refers to **NS records** pointing downward. Your registrar publishes NS for your domain at the TLD.

## Primary vs secondary

| | Primary (master) | Secondary (slave) |
|---|----------------|-------------------|
| **Edits** | Zone file or API changes here | Read-only copy |
| **Distribution** | NOTIFY + AXFR/IXFR to secondaries | Polls SOA serial |
| **Failure** | Promote secondary or restore from backup | Serves if primary down |

## Software in this vault

| Server | Typical role |
|--------|--------------|
| [[BIND]] | Authoritative + recursive (enterprise, ISP) |
| [[Unbound]] | Validating recursive resolver |
| [[CoreDNS]] | Kubernetes cluster DNS, plugins |
| [[dnsmasq]] | DHCP + local forwarding on edge/LAN |
| [[PoserDNS]] | Authoritative server (PowerDNS) |

## Query path

```bash
dig @ns1.example.com example.com SOA    # direct authoritative
dig @8.8.8.8 example.com A               # recursive path
```

## Health checks

- **SOA serial** increases after edits
- **DNSSEC** validation if enabled (`dig +dnssec`)
- **Latency** and **QPS** under attack ([[DNS rebinding]] defenses at application layer are separate)

## Recall

- Why should public authoritative servers not offer recursion to the world?
- What is the difference between NS records at the parent vs in the child zone?

## Sources

- [RFC 1034 — Domain concepts and facilities](https://datatracker.ietf.org/doc/html/rfc1034)
- [ICANN — Root servers](https://www.iana.org/domains/root/servers)
