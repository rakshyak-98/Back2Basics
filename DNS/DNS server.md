[[DNS]] · [[name server]] · [[BIND]] · [[Unbound]] · [[CoreDNS]] · [[dnsmasq]]

# DNS server

> A DNS server is software (or a managed service) that answers queries — either authoritatively from zone data or recursively by walking the global tree on behalf of clients.

---

## Software map in this vault

| Note | Role |
|------|------|
| [[BIND]] | Industry-standard authoritative + recursive |
| [[Unbound]] | Validating recursive resolver |
| [[CoreDNS]] | Plugin-based DNS for Kubernetes |
| [[dnsmasq]] | Lightweight DHCP/DNS forwarder for LAN |
| [[PoserDNS]] | PowerDNS authoritative server |

Managed equivalents: [[Route53]], [[cloudflare]], registrar DNS panels.

## Choose by job

| Need | Pick |
|------|------|
| Internet-facing zone master | BIND or PowerDNS with DNSSEC |
| Laptop / office resolver | Unbound forwarding to [[public resolver]] |
| Home router / Pi-hole adjacency | dnsmasq |
| Cluster service discovery | CoreDNS |
| Zero ops | Route 53 / Cloudflare |

## Architecture sketch

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

## Hardening checklist

- Disable open recursion on authoritative-only hosts
- Rate limit and Response Policy Zones (RPZ) for malware domains
- Keep software patched (amplification attacks target old BIND versions)
- Monitor QPS and anomaly spikes

## Health verification

```bash
dig @ns1.example.com example.com SOA
dig @resolver-ip example.com A +dnssec
```

## Recall

- What is the difference between hosting a zone and running a recursive resolver?
- Why is open recursion a DDoS amplification risk?

## Sources

- [RFC 1034 — Name server specification](https://datatracker.ietf.org/doc/html/rfc1034)
- [ISC BIND 9](https://www.isc.org/bind/)
