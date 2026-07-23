[[DNS]] [[DNS/DNS zone]] [[DNS/cloudflare]] [[AWS/Networking/Route53]]

# DNS record

> Name → type → value mapping in a zone — A/AAAA/CNAME/TXT/MX with TTL controlling cache stickiness.

## Mental model

Resolvers cache answers per **TTL** (seconds). Lower TTL before changes = faster global cutover. **CNAME** can't apex `@` on all providers (use ALIAS/ANAME at Route53/Cloudflare). **TXT** for SPF/DKIM/verification. Propagation = old TTL expiring everywhere, not instant magic.

```
Client → recursive resolver (cache TTL) → authoritative NS → zone file/RRset
```

## Standard config / commands

### Inspect current records

```bash
dig yourdomain.com A +short
dig www.yourdomain.com CNAME
dig yourdomain.com TXT
dig yourdomain.com NS
dig @8.8.8.8 yourdomain.com A    # bypass local cache
```

### Safe change procedure

1. Note current TTL (`dig yourdomain.com A` → ANSWER TTL)
2. Lower TTL to **300** (5 min); wait **old TTL** to expire
3. Change A/CNAME/TXT
4. Verify with multiple resolvers
5. Raise TTL again (3600+) when stable

### Common record types

| Type | Use |
|------|-----|
| A / AAAA | Host → IPv4 / IPv6 |
| CNAME | Alias hostname → hostname |
| TXT | SPF, DKIM, domain verify |
| MX | Mail routing (priority + host) |
| NS | Delegates subdomain to other DNS |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Old IP still resolves | TTL cache | Wait TTL; `dig @1.1.1.1` vs local |
| Apex CNAME rejected | Provider rules | ALIAS record or A to load balancer |
| Cert validation fails | `_acme-challenge` TXT | Add exact token; no extra quotes |
| Email bounces | MX + SPF TXT | MX points to mail host; SPF includes sender |
| Subdomain wrong zone | NS delegation | Child zone NS at parent |
| Intermittent answers | Split DNS | Internal vs public view mismatch |

## Gotchas

> [!WARNING]
> **CNAME at www only, apex A/ALIAS** — classic migration mistake.
>
> **Trailing dot** — FQDN in some UIs needs `@` or full stop semantics.
>
> **Wildcard `*` doesn't cover nested** — `*.example.com` ≠ `a.b.example.com` on all setups.

## When NOT to use

- Don't set TTL 0 in production — resolver load + instability.
- Don't chain CNAME → CNAME → … — flatten or use ALIAS.

## Related

[[DNS]] [[DNS/DNS zone]] [[DNS/cloudflare]] [[Security/certbot error]]
