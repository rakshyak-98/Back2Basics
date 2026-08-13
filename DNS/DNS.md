[[TCP]] · [[UDP]] · [[DNS zone]] · [[name server]] · [[dig]] · [[public resolver]]

# DNS

> The Domain Name System maps human-readable names to records (A, AAAA, CNAME, MX, …) through a distributed, cached hierarchy — when lookups fail, the fault is usually resolver configuration, TTL caching, or a wrong authoritative answer.

---

## Resolution chain

```
Application
    │
    ▼
Stub resolver (glibc, systemd-resolved, mobile OS)
    │
    ▼
Recursive resolver (ISP, 8.8.8.8, corporate [[Unbound]], [[public resolver]])
    │  iterative queries
    ▼
Root servers (. ) → TLD servers (.com) → authoritative [[name server]] for zone
    │
    ▼
Answer + TTL cached at each hop
```

Defined in [RFC 1035](https://datatracker.ietf.org/doc/html/rfc1035) with extensions for DNSSEC ([RFC 4033](https://datatracker.ietf.org/doc/html/rfc4033)), EDNS0, and newer transports (DoH, DoT).

## Record types you operate daily

| Type | Purpose |
|------|---------|
| **A / AAAA** | IPv4 / IPv6 address |
| **CNAME** | Alias to another name (not at zone apex with standard DNS) |
| **MX** | Mail exchanger priority + host |
| **TXT** | SPF, DKIM, DMARC, verification tokens |
| **NS** | Delegates subdomain to other nameservers |
| **SOA** | Zone metadata (serial, refresh, TTL defaults) |
| **SRV** | Service location (port, priority, weight) |
| **CAA** | Which CAs may issue certificates for the domain |

See [[dns record]] for field-level detail.

## Transport

- **UDP/53** — default; 512-byte traditional limit without EDNS
- **TCP/53** — truncation (TC bit), large responses, zone transfers (AXFR)
- **DNS-over-TLS (DoT)** — [RFC 7858](https://datatracker.ietf.org/doc/html/rfc7858)
- **DNS-over-HTTPS (DoH)** — [RFC 8484](https://datatracker.ietf.org/doc/html/rfc8484)

## Debugging toolkit

```bash
dig example.com A +trace
dig @8.8.8.8 example.com A
dig example.com MX
host -t TXT example.com
```

Compare **stub → recursive → authoritative** answers to locate stale cache vs wrong zone data.

## Local naming beyond global DNS

- **[[mDNS]]** — `.local` on LAN ([RFC 6762](https://datatracker.ietf.org/doc/html/rfc6762))
- **[[LLMNR]]** — Windows link-local name resolution (avoid on untrusted networks)
- **Split-horizon / private zones** — same name, different answers inside corporate network ([[DNS zone]])

## Security topics in this folder

- [[DNS rebinding]] — browser same-origin bypass via DNS TTL tricks
- [[cloudflare]] — operator patterns for public DNS and proxy
- Server software: [[BIND]], [[Unbound]], [[CoreDNS]], [[dnsmasq]]

## Recall

- What is the difference between recursive and authoritative nameservers?
- When does a resolver switch from UDP to TCP for DNS?

## Sources

- [RFC 1035 — Domain Names](https://datatracker.ietf.org/doc/html/rfc1035)
- [ICANN DNS overview](https://www.icann.org/resources/pages/dns-what-is-2021-02-25-en)
- Kleppmann, *Designing Data-Intensive Applications* — DNS as example of partitioned naming
