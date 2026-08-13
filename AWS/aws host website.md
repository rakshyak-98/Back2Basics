[[AWS]] [[How to connect Godaddy domain with AWS EC2 instance]] [[Networking/Route53]]

# aws host website

> S3 static website hosting — flip a bucket into an HTTP endpoint that serves `index.html` (and a custom error doc).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Website endpoints are **HTTP** (`s3-website-…`), public-read (or CloudFront+OAC). Not the same as the REST API endpoint. For HTTPS + custom domain, put CloudFront (or another CDN) in front.

```txt
Browser → (CloudFront) → S3 website endpoint → index.html
```

| Flag | Meaning |
|------|---------|
| `--index-document` | Object for `/` |
| `--error-document` | Object for missing keys (SPA often `index.html`) |

---

## Standard config / commands

```bash
aws s3 mb s3://$BUCKET
aws s3 website s3://$BUCKET --index-document index.html --error-document error.html
aws s3 sync ./dist s3://$BUCKET

# Bucket policy / Block Public Access must allow the read model you chose
# Prefer CloudFront + OAC over public website endpoint for prod HTTPS
```

| Knob | Why it matters |
|------|----------------|
| Website endpoint URL | Region-specific `s3-website-…` hostname |
| Public access block | Default deny — explicit open or CloudFront only |
| SPA routing | Error doc → `index.html` for client routes |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 403 Access Denied | BPA + policy + object ACL | Public policy or CloudFront OAC |
| 404 XML instead of page | Website hosting off / wrong key | Enable website; fix index name |
| HTTPS cert error on S3 site URL | Website endpoint is HTTP | CloudFront + ACM cert |
| Old assets after deploy | Cache | CloudFront invalidation; hash filenames |
| Custom domain NXDOMAIN | DNS | Route53/ALIAS to CloudFront or website endpoint |

---

## Gotchas

> [!WARNING]
> **Website hosting ≠ REST endpoint** — different hostnames and behaviors.

> [!WARNING]
> **Public buckets are easy to misconfigure** — prefer private bucket + CloudFront.

> [!WARNING]
> **No server-side logic** — redirects/routing limited; use CloudFront functions or a real app host.

---

## When NOT to use

- **Dynamic SSR / APIs** — EC2/ECS/Lambda+APIGW.
- **Private authenticated file share** — presigned URLs / application authentication, not public website mode.
- **Highly dynamic personalization** — needs compute, not static S3 alone.

---

## Related

[[Networking/Route53]] [[How to connect Godaddy domain with AWS EC2 instance]] [[AWS ECR]] [[https]]
