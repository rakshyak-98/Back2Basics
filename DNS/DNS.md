[[TCP]] [[UDP]] [[DNS zone]] [[name server]] [[dig]] [[public resolver]] [[dns record]]

# DNS

> The Domain Name System maps human-readable names to records (A, AAAA, CNAME, MX, …) through a distributed, cached hierarchy — when lookups fail, the fault is usually resolver configuration, TTL caching, or a wrong authoritative answer.

## Interview Relevance

Interviewers probe whether you can walk stub → recursive → authoritative, explain TTL/caching, and pick the right record type — not just recite “DNS turns names into IPs.”

## Sources

- [RFC 1035 — Domain Names](https://datatracker.ietf.org/doc/html/rfc1035) — deep-dive
- [RFC 4033 — DNS Security Introduction](https://datatracker.ietf.org/doc/html/rfc4033) — deep-dive
- [ICANN DNS overview](https://www.icann.org/resources/pages/dns-what-is-2021-02-25-en) — overview

## Key Concepts

- **Hierarchy:** root → TLD → zone — answers come from the authoritative [[name server]] for that cut of the tree.
- **Caching + TTL:** every hop may cache — stale answers often look like “DNS is broken” after a change.
- **Recursive vs authoritative:** resolvers walk the tree; authoritative servers only answer for zones they host ([[DNS server]]).
- **Record types:** typed tuples (A, MX, TXT, …) — wrong type or apex constraints break apps ([[dns record]]).

## Technical Details

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

**Transport**

- **UDP/53** — default; 512-byte traditional limit without EDNS
- **TCP/53** — truncation (TC bit), large responses, zone transfers (AXFR)
- **DNS-over-TLS (DoT)** — [RFC 7858](https://datatracker.ietf.org/doc/html/rfc7858)
- **DNS-over-HTTPS (DoH)** — [RFC 8484](https://datatracker.ietf.org/doc/html/rfc8484)

```bash
dig example.com A +trace
dig @8.8.8.8 example.com A
dig example.com MX
host -t TXT example.com
```

Compare **stub → recursive → authoritative** answers to locate stale cache vs wrong zone data.

Local naming beyond global DNS: [[mDNS]] (`.local`), [[LLMNR]] (Windows link-local), and split-horizon / private [[DNS zone]]s.

## Real-World Applications

Every browser, API client, and mail server depends on DNS before the first TCP connect.

**Example:** After cutting TTL and updating an A record, half the fleet still hits the old IP — recursive caches have not expired; dig at `@ns1` (authoritative) vs `@8.8.8.8` (public recursive) isolates the lag.

## Pros/Cons or Trade-offs

- **Pro:** Globally distributed, cached naming — scales without a single central database of all hosts.
- **Con:** TTL delays change visibility — fast failover needs low TTL (more query load) or health-aware CDNs.
- **Con:** Cleartext UDP/53 leaks QNAMEs on the wire — DoT/DoH encrypt transport but still trust the resolver.

## Comparison

- vs [[mDNS]] / [[LLMNR]]: global DNS needs servers and FQDNs; link-local multicast resolves names without a central [[name server]].
- vs hosts file: static local overrides — no delegation, no TTL, no global consistency.

## Mistakes to Avoid

- Blaming “DNS” without checking which hop is wrong — stub, recursive cache, or authoritative zone data.
- Expecting instant global updates with multi-hour TTLs still cached.
- Confusing recursive open resolvers with authoritative zone hosting ([[DNS rebinding]] and amplification risks differ).
