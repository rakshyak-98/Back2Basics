[[DNS]] [[public resolver]] [[Route53]] [[DNS zone]] [[dns record]]

# cloudflare

> Cloudflare operates a global anycast DNS network as registrar, authoritative DNS host, and public resolver (1.1.1.1) — the orange-cloud proxy adds CDN, DDoS protection, and WAF in front of your origin.

## Interview Relevance

Interviewers use Cloudflare to test proxied vs DNS-only records, apex CNAME flattening, and how CDN SSL modes interact with origin certificates.

## Sources

- [Cloudflare DNS documentation](https://developers.cloudflare.com/dns/) — deep-dive
- [Cloudflare Learning — DNS](https://www.cloudflare.com/learning/dns/what-is-dns/) — overview

## Key Concepts

- **Authoritative DNS:** host zones with API-driven records and fast propagation.
- **1.1.1.1:** [[public resolver]] for clients — separate product from your hosted zone.
- **Orange cloud (proxied):** HTTP/S through Cloudflare edge — clients see Cloudflare IPs, not origin.
- **Grey cloud (DNS only):** direct to origin IP — required for many non-HTTP protocols and mail.

## Technical Details

| Product | Role |
|---------|------|
| **Authoritative DNS** | Host zones; fast propagation; API-driven records |
| **1.1.1.1 resolver** | [[public resolver]] for clients |
| **Proxy (orange cloud)** | HTTP/S traffic through Cloudflare edge; hides origin IP |
| **DNSSEC** | One-click signing for hosted zones |
| **Workers / R2** | Edge compute and storage adjacent to DNS |

```
A  www  203.0.113.10  Proxied (orange)  → clients see Cloudflare anycast IPs
A  api  10.0.0.5      DNS only (grey)    → direct to origin IP exposed
```

Proxied mode enables caching, bot management, and SSL modes (flexible/full/strict) — misconfigured SSL mode causes redirect loops or certificate errors.

**Common record tasks**

- **APEX** — CNAME flattening at `@` to external targets
- **Workers routes** — `workers.dev` or custom host patterns
- **Email** — keep MX/TXT grey-cloud or use Email Routing product

```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer $CF_API_TOKEN"
```

| | Cloudflare DNS | Route 53 |
|---|----------------|----------|
| **Integration** | CDN/WAF bundled | Native AWS alias to ALB/S3 |
| **Pricing** | Free tier generous for DNS | Per-zone + query pricing |
| **Private zones** | Limited patterns | VPC private hosted zones |

Many teams use Cloudflare at the edge and AWS behind it.

## Real-World Applications

Marketing sites and APIs sit behind orange-cloud; SSH, SMTP, and game servers stay grey-cloud to the real IP.

**Example:** Toggle `www` from grey to orange — dig now returns Cloudflare anycast addresses; origin IP disappears from public DNS (still reachable if previously leaked).

## Pros/Cons or Trade-offs

- **Pro:** Bundled CDN/WAF/DNSSEC with simple UI and API.
- **Con:** Proxied mode is HTTP-centric — wrong for mail MX and many TCP apps.
- **Con:** SSL mode mistakes (Flexible) cause redirect loops or cleartext-to-origin.

## Comparison

- vs [[Route53]]: Cloudflare leans edge/CDN; Route 53 leans AWS aliases and VPC private zones.
- vs self-hosted [[BIND]]: less zone-file ops, more vendor control of the edge.

## Mistakes to Avoid

- Orange-clouding MX/TXT or SSH endpoints — mail and non-HTTP break.
- Using Flexible SSL to an origin that redirects HTTP→HTTPS — infinite redirects.
- Assuming hiding origin IP in DNS means the old IP is secret forever.
