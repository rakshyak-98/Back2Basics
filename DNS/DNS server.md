[[DNS]] [[name server]] [[BIND]] [[Unbound]] [[CoreDNS]] [[dnsmasq]] [[PoserDNS]]

# DNS server

> A DNS server is software (or a managed service) that answers queries — either authoritatively from zone data or recursively by walking the global tree on behalf of clients.

## Interview Relevance

Interviewers check that you pick software by role (authoritative vs recursive vs cluster DNS) and know why open recursion is dangerous.

## Sources

- [RFC 1034 — Name server specification](https://datatracker.ietf.org/doc/html/rfc1034) — deep-dive
- [ISC BIND 9](https://www.isc.org/bind/) — overview

## Key Concepts

- **Authoritative role:** answers from zone data you publish — does not need to recurse for the world.
- **Recursive role:** walks root → TLD → auth on behalf of clients and caches.
- **Managed DNS:** [[Route53]], [[cloudflare]], registrar panels — same roles as software, less host ops.
- **Hardening:** lock recursion, rate-limit, patch — open resolvers amplify DDoS.

## Technical Details

| Note | Role |
|------|------|
| [[BIND]] | Industry-standard authoritative + recursive |
| [[Unbound]] | Validating recursive resolver |
| [[CoreDNS]] | Plugin-based DNS for Kubernetes |
| [[dnsmasq]] | Lightweight DHCP/DNS forwarder for LAN |
| [[PoserDNS]] | PowerDNS authoritative server |

Managed equivalents: [[Route53]], [[cloudflare]], registrar DNS panels.

| Need | Pick |
|------|------|
| Internet-facing zone master | BIND or PowerDNS with DNSSEC |
| Laptop / office resolver | Unbound forwarding to [[public resolver]] |
| Home router / Pi-hole adjacency | dnsmasq |
| Cluster service discovery | CoreDNS |
| Zero ops | Route 53 / Cloudflare |

```
Clients
   │
   ▼
Recursive resolver (Unbound / BIND recursion / 1.1.1.1)
   │
   ├── cache hit → answer
   └── cache miss → iterative query to authoritative chain
                           │
                           ▼
                   Authoritative NS (BIND / PowerDNS / Route53)
```

**Hardening checklist**

- Disable open recursion on authoritative-only hosts
- Rate limit and Response Policy Zones (RPZ) for malware domains
- Keep software patched (amplification attacks target old BIND versions)
- Monitor QPS and anomaly spikes

```bash
dig @ns1.example.com example.com SOA
dig @resolver-ip example.com A +dnssec
```

## Real-World Applications

Enterprises often run authoritative BIND/PowerDNS for public zones and Unbound (or a [[public resolver]]) for employee recursion; Kubernetes uses CoreDNS inside the cluster.

**Example:** A Pi-hole or home gateway runs dnsmasq for LAN names + DHCP while forwarding unknowns to 1.1.1.1.

## Pros/Cons or Trade-offs

- **Pro:** Self-hosted control of zones, DNSSEC, and split views.
- **Con:** Patching, open-resolver risk, and transfer/ACLs are your problem.
- **Pro (managed):** API-driven records and global anycast — trade vendor lock-in and query cost.

## Comparison

- vs [[name server]]: “nameserver” is the role in the protocol; “DNS server” here is the software/service map in this vault.
- vs [[public resolver]]: public resolvers are recursive-only for the Internet; they do not host your zone.

## Mistakes to Avoid

- Running open recursion on a public authoritative host — DDoS amplification.
- Choosing CoreDNS for Internet-facing zone masters (or BIND for Kubernetes service discovery) without a strong reason.
- Skipping health checks of both SOA (auth) and recursive DNSSEC paths.
