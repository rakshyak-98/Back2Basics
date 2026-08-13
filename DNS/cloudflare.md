[[DNS]] · [[public resolver]] · [[Route53]] · [[DNS zone]]

# cloudflare

> Cloudflare operates a global anycast DNS network as registrar, authoritative DNS host, and public resolver (1.1.1.1) — the orange-cloud proxy adds CDN, DDoS protection, and WAF in front of your origin.

---

## Products relevant to DNS operations

| Product | Role |
|---------|------|
| **Authoritative DNS** | Host zones; fast propagation; API-driven records |
| **1.1.1.1 resolver** | [[public resolver]] for clients |
| **Proxy (orange cloud)** | HTTP/S traffic through Cloudflare edge; hides origin IP |
| **DNSSEC** | One-click signing for hosted zones |
| **Workers / R2** | Edge compute and storage adjacent to DNS |

## DNS-only vs proxied records

```
A  www  203.0.113.10  Proxied (orange)  → clients see Cloudflare anycast IPs
A  api  10.0.0.5      DNS only (grey)    → direct to origin IP exposed
```

Proxied mode enables caching, bot management, and SSL modes (flexible/full/strict) — misconfigured SSL mode causes redirect loops or certificate errors.

## Common record tasks

- **APEX** — CNAME flattening at `@` to external targets
- **Workers routes** — `workers.dev` or custom host patterns
- **Email** — keep MX/TXT grey-cloud or use Email Routing product

## API example

```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer $CF_API_TOKEN"
```

## vs [[Route53]]

| | Cloudflare DNS | Route 53 |
|---|----------------|----------|
| **Integration** | CDN/WAF bundled | Native AWS alias to ALB/S3 |
| **Pricing** | Free tier generous for DNS | Per-zone + query pricing |
| **Private zones** | Limited patterns | VPC private hosted zones |

Many teams use Cloudflare at the edge and AWS behind it.

## Recall

- What changes when you toggle a record from grey to orange cloud?
- Why might email break if you accidentally proxy MX records?

## Sources

- [Cloudflare DNS documentation](https://developers.cloudflare.com/dns/)
- [Cloudflare Learning — DNS](https://www.cloudflare.com/learning/dns/what-is-dns/)
