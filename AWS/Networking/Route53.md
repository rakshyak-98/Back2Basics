[[DNS]] [[DNS zone]] [[AWS Networking]] [[TLS (Transport Layer Security)]] [[How to connect Godaddy domain with AWS EC2 instance]]

# Route53

> AWS **authoritative DNS + health-checked routing + private zones** — not just "create an A record." **Route53 Developer Guide** + prod cutover war stories.

## Mental model

Route53 hosts **hosted zones** (public on the internet, or **private** associated with VPCs). Records answer queries; **routing policies** (weighted, latency, failover, geolocation) steer traffic. **Health checks** remove unhealthy targets from DNS answers (with caveats — DNS TTL caching delays failover).

```
Client resolver ──► Route53 (authoritative for zone) ──► A/AAAA/CNAME/ALIAS
                              │
                              └── health check ──► alarm / failover record
```

**ALIAS records** (Route53-only) point to AWS resources (ALB, CloudFront, S3 website) **without CNAME-at-apex limitation** and can be evaluated at zone apex (`example.com`).

## Standard config / commands

### Public hosted zone + ALB (common pattern)

| Record | Type | Target | Notes |
|--------|------|--------|-------|
| `app.example.com` | A (ALIAS) | ALB dualstack DNS name | Evaluate target health |
| `example.com` | A (ALIAS) | CloudFront or ALB | Apex requires ALIAS not CNAME |
| `_acme-challenge` | TXT | cert validation | Let's Encrypt / ACM DNS validation |

```bash
# List zones
aws route53 list-hosted-zones-by-name --dns-name example.com

# Upsert A alias to ALB
aws route53 change-resource-record-sets --hosted-zone-id Z123 --change-batch file://change.json
```

`change.json` (ALIAS to ALB):
```json
{
  "Changes": [{
    "Action": "UPSERT",
    "ResourceRecordSet": {
      "Name": "app.example.com",
      "Type": "A",
      "AliasTarget": {
        "HostedZoneId": "Z35SXDOTRQ7X7K",
        "DNSName": "dualstack.my-alb-123.us-east-1.elb.amazonaws.com",
        "EvaluateTargetHealth": true
      }
    }
  }]
}
```

### Private hosted zone (split-horizon)

- Create **private** zone `internal.corp.local`; associate with VPC(s).
- Same name can exist as public + private — **VPC resolver uses private** when associated.

### Registrar vs DNS host

- Domain registered at GoDaddy/Namecheap, **nameservers → Route53 NS** (four `ns-xxx.awsdns-xx.com` records).
- Or register in Route53 — NS automatic.

### TTL guidance

| Use case | TTL | Why |
|----------|-----|-----|
| Stable prod ALIAS | 60–300s | Faster failover vs cache churn tradeoff |
| Pre-cutover testing | 300–60s | Lower before migration, raise after stable |
| CDN/CloudFront fronted | 60s on origin names | Failover pairs with health checks |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Domain doesn't resolve at all | NS at registrar match Route53 zone; zone exists | Update registrar NS; wait propagation (up to 48h, often minutes) |
| Resolves old IP after change | TTL; cached at resolver/ISP | Lower TTL pre-change; `dig +trace`; flush local cache |
| Apex works, `www` doesn't (or reverse) | Missing record; CNAME at apex (invalid) | ALIAS at apex; CNAME for subdomains only |
| Private name resolves on laptop, not in VPC | PHZ VPC association; `enableDnsSupport` | Associate VPC; check hybrid DNS forwarders |
| Failover didn't switch | Health check region; TTL; EvaluateTargetHealth false | Fix health check path; enable eval; accept DNS delay |
| ACM cert stuck pending validation | TXT/CNAME record in **same** zone ACM expects | Create exact validation record Route53 can auto-create |
| `SERVFAIL` intermittent | Route53 query logging; lame delegations | Fix child NS; check DS/DNSSEC if enabled |

```bash
dig +short NS example.com
dig +short app.example.com @8.8.8.8
dig +trace app.example.com
aws route53 get-health-check-status --health-check-id xxx
```

## Gotchas

> [!WARNING]
> **DNS failover is not instant** — clients and resolvers cache TTL. Plan for **minutes** of bleed; use health checks + app-layer retries.

> [!WARNING]
> **CNAME at zone apex is invalid** (RFC) — use Route53 **ALIAS** for apex to ELB/CloudFront/S3.

> [!WARNING]
> **Weighted routing without health checks** — dead weight still gets traffic. Attach health checks or use active-active with care.

> [!WARNING]
> **Private zone association missing on new VPC** — new prod VPC won't resolve `db.internal` until PHZ linked.

## When NOT to use

- **Sub-millisecond failover requirement** — DNS alone insufficient; use anycast LB + health checks at L7/L4.
- **Complex geo compliance** — combine with CloudFront/Lambda@Edge; Route53 geolocation is coarse.
- **Full DNS server features (custom AXFR to random NS)** — Route53 is managed authoritative, not a general BIND replacement ([[servers/BIND]]).

## Related

[[DNS]] · [[DNS zone]] · [[AWS Networking]] · [[TLS (Transport Layer Security)]] · [[How to connect Godaddy domain with AWS EC2 instance]] · [[cloudflare]]
