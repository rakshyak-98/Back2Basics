[[DNS]] · [[DNS zone]] · [[name server]] · [[top-level Domain]] · [[Sub Domain]]

# dns record

> A DNS record is a typed tuple (owner name, class, type, TTL, rdata) published in a zone — operations break when TTL, CNAME chains, or apex constraints are wrong.

---

## Record anatomy

```
owner-name  TTL  IN  TYPE  RDATA
```

Example:

```
www.example.com.  300  IN  A  203.0.113.10
```

| Field | Meaning |
|-------|---------|
| **Owner** | FQDN with trailing dot in zone files |
| **TTL** | Seconds resolvers may cache (lower = faster propagation, more query load) |
| **CLASS** | Almost always `IN` (Internet) |
| **TYPE** | Kind of record |
| **RDATA** | Type-specific payload |

## Common types

| Type | RDATA | Notes |
|------|-------|-------|
| **A** | IPv4 | 32-bit address |
| **AAAA** | IPv6 | 128-bit address |
| **CNAME** | target hostname | No other records at same owner (with exceptions/CDN patterns) |
| **MX** | preference + host | Lower preference = higher priority |
| **TXT** | one or more strings | 255-char chunk limit per string |
| **NS** | nameserver hostname | Delegation |
| **PTR** | hostname | Reverse DNS in `in-addr.arpa` / `ip6.arpa` |
| **SRV** | priority weight port target | `_service._proto.name` |
| **CAA** | flags tag value | Certificate issuance policy |

## CNAME constraints

Standard DNS forbids CNAME coexisting with other record types at the same owner name. **Zone apex** (`example.com`) historically could not be CNAME; use ALIAS/ANAME at providers ([[Route53]], [[cloudflare]]) or A/AAAA records.

## Mail authentication records

```
example.com.  TXT  "v=spf1 include:_spf.google.com ~all"
default._domainkey.example.com.  TXT  "v=DKIM1; k=rsa; p=..."
_dmarc.example.com.  TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"
```

See [[Protocol/SMTP]] and [[servers/DSN records]] (mail-related DNS).

## TTL strategy

| Scenario | TTL guidance |
|----------|--------------|
| Pre-migration | Lower TTL hours before change |
| Stable production | 300–3600s common |
| CDN failover | Provider may ignore low TTL at edge |

## Verify

```bash
dig +noall +answer www.example.com A
dig +short TXT example.com
```

## Recall

- Why can a CNAME at `www` differ from apex `A` records?
- What does MX preference number mean?

## Sources

- [RFC 1035 — Resource record definitions](https://datatracker.ietf.org/doc/html/rfc1035#section-3.2)
- [RFC 7208 — SPF](https://datatracker.ietf.org/doc/html/rfc7208)
