[[AWS]] [[AWS S3]] [[ALB (Application Load Balancer)]] [[Route53]] [[TLS (Transport Layer Security)]] [[AWS Billing and cost management]]

# CloudFront

> Global CDN — caches at edge, terminates HTTPS with ACM (**us-east-1** for CloudFront certs), fronts S3 or ALB. Misconfigured OAC/OAI leaves buckets public or origins unreachable.

## Mental model

CloudFront **distribution** has **behaviors** (path → origin + cache policy). Viewer → edge → (cache hit) or origin fetch. S3 origins should stay **private** via **Origin Access Control (OAC)** (prefer over legacy OAI).

```
Viewer ──► Edge POP ──► cache hit?
                │ no
                └── Origin (S3 / ALB / custom)
```

| Origin | Pattern |
|--------|---------|
| S3 | OAC + bucket policy allow CloudFront service principal |
| ALB | Origin protocol HTTPS; optional custom header secret |
| Custom | Domain + TLS; forward Host carefully |

## Standard config / commands

### Certs

- Viewer HTTPS cert must be in **ACM us-east-1** (N. Virginia), even if origin is elsewhere.
- ALB origin certs are **regional** ACM in the ALB region.

### S3 + OAC (prod static)

1. Create distribution with S3 REST origin (not website endpoint) + OAC.
2. Bucket policy: allow `s3:GetObject` from CloudFront distribution ARN / service.
3. Block Public Access remains **on**.

```bash
aws cloudfront list-distributions \
  --query 'DistributionList.Items[].{Id:Id,Domain:DomainName,Status:Status}'
aws cloudfront create-invalidation --distribution-id E123 --paths "/*"
```

### Cache

| Setting | Prod default |
|---------|----------------|
| Cache policy | CachingOptimized or custom TTLs |
| Origin request policy | Forward only needed headers/cookies/query |
| Compress | Enabled |

### DNS

Route53 **ALIAS** to `dxxx.cloudfront.net` ([[Route53]]).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 403 from CloudFront on S3 | OAC/OAI; bucket policy; BPA | Fix OAC policy; use REST endpoint |
| Cert won't attach | ACM not in us-east-1 | Reissue/request cert in us-east-1 |
| Stale content | TTL; no invalidation | Invalidate; versioned object keys (`app.abc123.js`) |
| 502/504 to ALB origin | Origin SG; health; TLS name | Allow CloudFront? (actually SG can't filter CF easily — use secret header or prefix list patterns); fix origin |
| CORS errors | Origin vs CF behavior | Configure CF response headers policy or origin CORS |
| High bill | Invalidation `/*`; egress; many requests | Versioned assets; fewer invalidations |

## Gotchas

> [!WARNING]
> **S3 website endpoint as origin** fights OAC — use REST API endpoint + OAC.

> [!WARNING]
> **Invalidation `/*` is slow and billable** — prefer content-hashed filenames.

> [!WARNING]
> **Forwarding all cookies/headers** destroys cache hit ratio.

> [!WARNING]
> **OAI is legacy** — new setups use **OAC**.

## When NOT to use

- **Private admin APIs with no caching benefit** — ALB/API Gateway alone may suffice.
- **WebSockets** — limited; use API Gateway WebSocket or NLB patterns.
- **Non-HTTP protocols** — not CloudFront's job.

## Related

[[AWS S3]] · [[ALB (Application Load Balancer)]] · [[Route53]] · [[TLS (Transport Layer Security)]] · [[AWS Billing and cost management]] · [[AWS]]
