[[DNS]] [[DNS zone]] [[dns record]] [[BIND]] [[Unbound]] [[DNS server]]

# name server

> A nameserver answers DNS queries for zones it is authoritative for, or recursively resolves names on behalf of clients — confuse the two roles and you will open an open resolver or break delegation.

```txt
        name server ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Classic question: authoritative vs recursive vs stub

## Sources
- [RFC 1034 — Domain concepts and facilities](https://datatracker.ietf.org/doc/html/rfc1034) — deep-dive
- [ICANN — Root servers](https://www.iana.org/domains/root/servers) — overview

## Key Concepts
- **Authoritative:** answers from zone data (primary or secondary).
- **Recursive (resolver):** walks from root hints; caches answers.
- **Stub resolver:** OS/libc forwards to a configured recursive resolver.
- **Primary vs secondary:** edits on master; secondaries sync via NOTIFY + AXFR/IXFR.

## Technical Details
| Role | Behavior |
|------|----------|
| **Authoritative** | Answers from zone data (primary or secondary) |
| **Recursive (resolver)** | Walks the tree starting at root hints; caches answers |
| **Stub resolver** | Forwards to configured recursive resolver |

- An open recursive server on the public Internet amplifies DDoS

```
Root (.)  →  TLD (.com, .org)  →  Registrant zone (example.com)
```

- Each level refers to **NS records** pointing downward.
- Your registrar publishes NS for your domain at the TLD.

| | Primary (master) | Secondary (slave) |
|---|----------------|-------------------|
| **Edits** | Zone file or API changes here | Read-only copy |
| **Distribution** | NOTIFY + AXFR/IXFR to secondaries | Polls SOA serial |
| **Failure** | Promote secondary or restore from backup | Serves if primary down |

| Server | Typical role |
|--------|--------------|
| [[BIND]] | Authoritative + recursive (enterprise, ISP) |
| [[Unbound]] | Validating recursive resolver |
| [[CoreDNS]] | Kubernetes cluster DNS, plugins |
| [[dnsmasq]] | DHCP + local forwarding on edge/LAN |
| [[PoserDNS]] | Authoritative server (PowerDNS) |

```bash
dig @ns1.example.com example.com SOA    # direct authoritative
dig @8.8.8.8 example.com A               # recursive path
```

- Health checks: SOA serial increases after edits
- Application-layer [[DNS rebinding]] defenses are separate from nameserver har…

## Mistakes to Avoid
- **Mistake:** Offering recursion to `0.0.0.0/0` on Internet-facing hosts
- **Mistake:** Mismatching parent NS at the TLD with NS/glue in the child zone
- **Mistake:** Editing only the secondary

## Pros/Cons or Trade-offs
- **Pro:** Separating auth and recursion reduces blast radius and open-resolver risk.
- **Con:** Combined auth+recursion on one public IP is convenient and dangerous.
- **Pro:** Secondaries give read availability without shared writable storage.

## Comparison
- vs [[DNS server]]: nameserver emphasizes protocol roles
- vs [[public resolver]]: a public resolver is a recursive nameserver open to the Internet


### Use cases
- Registrar NS glue points at your authoritative pair

- **Example:** Two anycast NS hosts
