[[DNS]] · [[Unbound]] · [[cloudflare]] · [[dig]]

# public resolver

> A public recursive resolver (1.1.1.1, 8.8.8.8, 9.9.9.9) answers DNS queries for anyone on the Internet — use them when your ISP resolver is slow, filtered, or untrusted, understanding they see every name you look up.

---

## How they differ from authoritative servers

Public resolvers **do not host your zone**. They cache answers from authoritative [[name server]]s on your behalf, applying privacy and security policies (logging, DNSSEC validation, malware blocking).

```
Your laptop → 1.1.1.1 (recursive) → root/TLD/auth → cached answer
```

## Major providers

| Resolver | IPv4 | Notes |
|----------|------|-------|
| **Cloudflare** | 1.1.1.1, 1.0.0.1 | [[cloudflare]]; 1.1.1.1 for Families variants |
| **Google** | 8.8.8.8, 8.8.4.4 | Widely used; logs per policy |
| **Quad9** | 9.9.9.9 | Blocks known malicious domains |
| **OpenDNS** | 208.67.222.222 | Cisco Umbrella consumer tier |

DoH/DoT endpoints exist for encrypted transport to the same backends.

## Configure as upstream

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

## Privacy trade-off

The operator sees query metadata (timing, source IP, QNAME). For sensitive lookups, run your own [[Unbound]] forwarder or full recursive resolver.

## Testing

```bash
dig @1.1.1.1 example.com A
dig @8.8.8.8 example.com A +dnssec
```

Compare with `dig +trace` to see authoritative path without cache.

## Recall

- Why can a public resolver return different answers than your corporate resolver for the same name?
- What does DNS-over-HTTPS change about who can see your queries on the wire?

## Sources

- [RFC 8499 — DNS Terminology](https://datatracker.ietf.org/doc/html/rfc8499)
- [Cloudflare 1.1.1.1 resolver](https://developers.cloudflare.com/1.1.1.1/)
- [Google Public DNS](https://developers.google.com/speed/public-dns)
