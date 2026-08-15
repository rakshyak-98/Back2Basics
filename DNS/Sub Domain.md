[[DNS]] [[top-level Domain]] [[DNS zone]] [[dns record]] [[name server]]

# Sub Domain

> A subdomain is any domain below another in the DNS tree (`api.example.com` under `example.com`) — you delegate it with NS records or manage it in the same zone with individual records.

## Interview Relevance

Interviewers ask same-zone records vs NS delegation, wildcard depth, and how TLS SANs cover hostnames — ownership and blast-radius design.

## Sources

- [RFC 1034 — Domain name space and resource records](https://datatracker.ietf.org/doc/html/rfc1034) — deep-dive
- [RFC 4592 — Wildcards in the DNS](https://datatracker.ietf.org/doc/html/rfc4592) — deep-dive

## Key Concepts

- **Labels:** left-to-right specificity — leftmost is the most specific host label.
- **Same-zone records:** simple one-admin model (`api.example.com A …`).
- **Child zone delegation:** parent publishes NS (and glue) — child team owns its [[DNS zone]].
- **Wildcards:** `*.example.com` matches one label depth, not arbitrary depth.

## Technical Details

```
api.example.com
│   │      │
│   │      └── registered domain (apex)
│   └── labels (subdomains)
└── leftmost = most specific host
```

Each label can have its own records or be **delegated** to a separate [[DNS zone]] with its own [[name server]] set.

| Approach | When |
|----------|------|
| **Records in parent zone** | `api.example.com A 10.0.0.5` — simple, one admin |
| **Child zone delegation** | Team owns `staging.example.com` NS → their DNS host |

```
staging.example.com.  NS  ns1.staging-provider.net.
staging.example.com.  NS  ns2.staging-provider.net.
```

```
*.example.com.  A  203.0.113.50
```

Matches one level (`foo.example.com`) but not `bar.foo.example.com` unless another wildcard exists deeper.

| Subdomain | Typical use |
|-----------|-------------|
| `www` | Web front door (often CNAME to CDN) |
| `api` | REST/gRPC backends |
| `mail` | MX target host |
| `_dmarc`, `_domainkey` | Email authentication [[dns record]] |
| `internal` | Private split-horizon only |

TLS certificates must include every hostname clients hit — use SAN certificates or wildcard `*.example.com` (does not cover apex).

## Real-World Applications

Product environments (`prod`, `staging`), service prefixes (`api`, `cdn`), and email auth labels under the same registered domain.

**Example:** Platform delegates `k8s.example.com` NS to cluster DNS ops while marketing keeps apex records in the parent zone.

## Pros/Cons or Trade-offs

- **Pro (same zone):** one place to edit; fewer glue/DS moving parts.
- **Pro (delegation):** team autonomy and smaller blast radius.
- **Con (delegation):** broken NS/glue or DNSSEC DS mistakes take the whole subtree offline.

## Comparison

- vs [[top-level Domain]]: TLD is the public rightmost label (`com`); subdomain sits under a registered name.
- vs [[DNS zone]]: a subdomain may or may not be its own zone — zone cut happens only with NS delegation.

## Mistakes to Avoid

- Assuming `*.example.com` covers `a.b.example.com`.
- Expecting wildcard TLS `*.example.com` to cover the apex `example.com`.
- Delegating without glue when NS hostnames are inside the child zone.
