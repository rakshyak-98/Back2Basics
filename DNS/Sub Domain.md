[[DNS]] · [[top-level Domain]] · [[DNS zone]] · [[dns record]]

# Sub Domain

> A subdomain is any domain below another in the DNS tree (`api.example.com` under `example.com`) — you delegate it with NS records or manage it in the same zone with individual records.

---

## Naming

```
api.example.com
│   │      │
│   │      └── registered domain (apex)
│   └── labels (subdomains)
└── leftmost = most specific host
```

Each label can have its own records or be **delegated** to a separate [[DNS zone]] with its own [[name server]] set.

## Same zone vs delegation

| Approach | When |
|----------|------|
| **Records in parent zone** | `api.example.com A 10.0.0.5` — simple, one admin |
| **Child zone delegation** | Team owns `staging.example.com` NS → their DNS host |

Delegation example in parent zone:

```
staging.example.com.  NS  ns1.staging-provider.net.
staging.example.com.  NS  ns2.staging-provider.net.
```

## Wildcards

```
*.example.com.  A  203.0.113.50
```

Matches one level (`foo.example.com`) but not `bar.foo.example.com` unless another wildcard exists deeper.

## Common patterns

| Subdomain | Typical use |
|-----------|-------------|
| `www` | Web front door (often CNAME to CDN) |
| `api` | REST/gRPC backends |
| `mail` | MX target host |
| `_dmarc`, `_domainkey` | Email authentication [[dns record]] |
| `internal` | Private split-horizon only |

## Certificate coverage

TLS certificates must include every hostname clients hit — use SAN certificates or wildcard `*.example.com` (does not cover apex).

## Recall

- What is the difference between `api.example.com` as an A record vs delegated child zone?
- Does a wildcard at `*.example.com` cover `deep.api.example.com`?

## Sources

- [RFC 1034 — Domain name space and resource records](https://datatracker.ietf.org/doc/html/rfc1034)
- [RFC 4592 — Wildcards in the DNS](https://datatracker.ietf.org/doc/html/rfc4592)
