[[DNS]] [[DNS zone]] [[name server]] [[top-level Domain]] [[Sub Domain]] [[servers/DSN records]]

# dns record

> A DNS record is a typed tuple (owner name, class, type, TTL, rdata) published in a zone — operations break when TTL, CNAME chains, or apex constraints are wrong.

```txt
        dns record ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask for record anatomy, CNAME-at-apex rules, and TTL strategy

## Sources
- [RFC 1035 — Resource record definitions](https://datatracker.ietf.org/doc/html/rfc1035#section-3.2) — deep-dive
- [RFC 7208 — SPF](https://datatracker.ietf.org/doc/html/rfc7208) — deep-dive

## Key Concepts
- **Owner + type + rdata:** the lookup key and payload
- **TTL:** how long resolvers may cache
- **CNAME exclusivity:** standard DNS forbids other types at the same owner
- **Delegation records:** NS (and glue) cut the tree into child [[DNS zone]]s.

## Technical Details
```
owner-name  TTL  IN  TYPE  RDATA
```

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

- **CNAME constraints:** zone apex (`example.com`) historically could not be CN…

- **Mail authentication:** (see [[servers/DSN records]]):

```
example.com.  TXT  "v=spf1 include:_spf.google.com ~all"
default._domainkey.example.com.  TXT  "v=DKIM1; k=rsa; p=..."
_dmarc.example.com.  TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"
```

| Scenario | TTL guidance |
|----------|--------------|
| Pre-migration | Lower TTL hours before change |
| Stable production | 300–3600s common |
| CDN failover | Provider may ignore low TTL at edge |

```bash
dig +noall +answer www.example.com A
dig +short TXT example.com
```

## Mistakes to Avoid
- **Mistake:** Putting a CNAME at the apex without provider ALIAS/ANAME support
- **Mistake:** Leaving multi-hour TTLs during a cutover
- **Mistake:** Multiple SPF TXT records

## Pros/Cons or Trade-offs
- **Pro:** Typed records keep concerns separate (address vs mail vs cert policy).
- **Con:** CNAME chains and apex rules surprise people migrating to CDNs.
- **Con:** Very low TTLs increase recursive query load worldwide.

## Comparison
- vs [[DNS zone]]: a zone is the administrative unit; records are the rows inside it.
- vs hosts file lines: no TTL, type system, or global publication.


### Use cases
- Every hostname clients hit is one or more records in a [[DNS zone]].

- **Example:** Moving `www` to a CDN
