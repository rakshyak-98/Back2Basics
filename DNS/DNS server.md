[[DNS]] [[name server]] [[BIND]] [[Unbound]] [[CoreDNS]] [[dnsmasq]] [[PoserDNS]]

# DNS server

> A DNS server is software (or a managed service) that answers queries — either authoritatively from zone data or recursively by walking the global tree on behalf of clients.

```txt
        DNS server ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers check that you pick software by role (authoritative vs recursive…

## Sources
- [RFC 1034 — Name server specification](https://datatracker.ietf.org/doc/html/rfc1034) — deep-dive
- [ISC BIND 9](https://www.isc.org/bind/) — overview

## Key Concepts
- **Authoritative role:** answers from zone data you publish — does not need to recurse for the world.
- **Recursive role:** walks root → TLD → auth on behalf of clients and caches.
- **Managed DNS:** [[Route53]], [[cloudflare]], registrar panels
- **Hardening:** lock recursion, rate-limit, patch — open resolvers amplify DDoS.

## Technical Details
| Note | Role |
|------|------|
| [[BIND]] | Industry-standard authoritative + recursive |
| [[Unbound]] | Validating recursive resolver |
| [[CoreDNS]] | Plugin-based DNS for Kubernetes |
| [[dnsmasq]] | Lightweight DHCP/DNS forwarder for LAN |
| [[PoserDNS]] | PowerDNS authoritative server |

- Managed equivalents: [[Route53]], [[cloudflare]], registrar DNS panels.

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

- **Hardening checklist:** 

- Disable open recursion on authoritative-only hosts
- Rate limit and Response Policy Zones (RPZ) for malware domains
- Keep software patched (amplification attacks target old BIND versions)
- Monitor QPS and anomaly spikes

```bash
dig @ns1.example.com example.com SOA
dig @resolver-ip example.com A +dnssec
```

## Mistakes to Avoid
- **Mistake:** Running open recursion on a public authoritative host
- **Mistake:** Choosing CoreDNS for Internet-facing zone masters (or BIND for K…
- **Mistake:** Skipping health checks of both SOA (auth) and recursive DNSSEC p…

## Pros/Cons or Trade-offs
- **Pro:** Self-hosted control of zones, DNSSEC, and split views.
- **Con:** Patching, open-resolver risk, and transfer/ACLs are your problem.
- **Pro (managed):** API-driven records and global anycast

## Comparison
- vs [[name server]]: “nameserver” is the role in the protocol
- vs [[public resolver]]: public resolvers are recursive-only for the Internet


### Use cases
- Enterprises often run authoritative BIND/PowerDNS for public zones and Unboun…

- **Example:** A Pi-hole or home gateway runs dnsmasq for LAN names + DHCP whil…
