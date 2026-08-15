[[DNS]] [[Unbound]] [[cloudflare]] [[dig]] [[name server]]

# public resolver

> A public recursive resolver (1.1.1.1, 8.8.8.8, 9.9.9.9) answers DNS queries for anyone on the Internet — use them when your ISP resolver is slow, filtered, or untrusted, understanding they see every name you look up.

## Interview Relevance

Interviewers ask privacy vs convenience, DoH/DoT, and why corporate split-horizon names fail when you hard-code 8.8.8.8.

## Sources

- [RFC 8499 — DNS Terminology](https://datatracker.ietf.org/doc/html/rfc8499) — overview
- [Cloudflare 1.1.1.1 resolver](https://developers.cloudflare.com/1.1.1.1/) — overview
- [Google Public DNS](https://developers.google.com/speed/public-dns) — overview

## Key Concepts

- **Recursive only:** they cache answers from authoritative [[name server]]s — they do not host your zone.
- **Policy variants:** malware blocking (Quad9), family filters, logging policies differ by operator.
- **Encrypted transport:** DoH/DoT hide queries on the path to the resolver — the operator still sees QNAMEs.
- **Split-horizon conflict:** public answers may disagree with internal private zones.

## Technical Details

```
Your laptop → 1.1.1.1 (recursive) → root/TLD/auth → cached answer
```

| Resolver | IPv4 | Notes |
|----------|------|-------|
| **Cloudflare** | 1.1.1.1, 1.0.0.1 | [[cloudflare]]; 1.1.1.1 for Families variants |
| **Google** | 8.8.8.8, 8.8.4.4 | Widely used; logs per policy |
| **Quad9** | 9.9.9.9 | Blocks known malicious domains |
| **OpenDNS** | 208.67.222.222 | Cisco Umbrella consumer tier |

DoH/DoT endpoints exist for encrypted transport to the same backends.

### systemd-resolved

```ini
# /etc/systemd/resolved.conf
[Resolve]
DNS=1.1.1.1#cloudflare-dns.com 8.8.8.8
DNSOverTLS=yes
```

### /etc/resolv.conf (direct)

```
nameserver 1.1.1.1
nameserver 8.8.8.8
```

Corporate networks may **block** alternate resolvers — use split tunnel or accept internal resolver for split-horizon names.

```bash
dig @1.1.1.1 example.com A
dig @8.8.8.8 example.com A +dnssec
dig +trace example.com
```

## Real-World Applications

Traveling laptops, CI runners, and home networks often pin a public resolver for speed or to bypass ISP filtering.

**Example:** Office Wi-Fi hijacks DNS to a captive portal — DoH to 1.1.1.1 may bypass it (policy and security implications vary).

## Pros/Cons or Trade-offs

- **Pro:** Fast anycast, DNSSEC validation, optional threat blocking.
- **Con:** Operator sees query metadata (timing, source IP, QNAME).
- **Con:** Breaks private hosted zone names unless you keep a local forwarder ([[Unbound]]) for internal suffixes.

## Comparison

- vs authoritative [[name server]]: public resolvers do not publish your MX/A records for the world to query as NS.
- vs self-hosted [[Unbound]]: you keep cache and forwarding policy on-box; still may forward to a public resolver.

## Mistakes to Avoid

- Pointing production servers at a public resolver and expecting VPC-private names to resolve.
- Assuming DoH means “nobody sees my queries” — the resolver operator still does.
- Ignoring enterprise policy that blocks or redirects alternate resolvers.
