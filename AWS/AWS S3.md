[[AWS]] [[IAM]] [[ARN (Amazon Resource Name)]] [[KMS]] [[CloudFront]] [[AWS Billing and cost management]]

# AWS S3

> Object storage by key — durable, cheap at rest, expensive when you get egress / versioning / public-access wrong. **S3 User Guide** + Access Analyzer findings.

## Mental model

S3 is a **flat keyspace** inside a **bucket** (bucket name is global DNS-like). Objects have ACL/policy evaluation: **Block Public Access** + **bucket policy** + **IAM** + optional **object ACL**. Encryption at rest is SSE-S3 or SSE-KMS ([[KMS]]). Versioning + lifecycle control cost and recovery.

```
Client ──► PutObject / GetObject / Presigned URL
              │
              ├── Block Public Access (account/bucket)
              ├── Bucket policy + IAM
              └── SSE-S3 / SSE-KMS
```

| Pattern | Use |
|---------|-----|
| Private app data | Block Public Access on; IAM / VPC endpoint |
| Static website | Website hosting **or** CloudFront + OAC (prefer CDN) |
| Terraform state | Versioned + encrypted bucket ([[Terraform setup]]) |

## Standard config / commands

### Create private bucket (prod defaults)

```bash
aws s3api create-bucket --bucket my-app-prod-123 --region us-east-1
# Outside us-east-1 add: --create-bucket-configuration LocationConstraint=REGION

aws s3api put-public-access-block --bucket my-app-prod-123 \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

aws s3api put-bucket-encryption --bucket my-app-prod-123 \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms","KMSMasterKeyID":"alias/prod-s3"}}]}'

aws s3api put-bucket-versioning --bucket my-app-prod-123 \
  --versioning-configuration Status=Enabled
```

### Sync / list

```bash
aws s3 sync ./dist s3://my-app-prod-123/ --delete
aws s3 ls s3://my-app-prod-123/ --recursive --human-readable
```

### Presigned URL (time-boxed GET/PUT)

```bash
aws s3 presign s3://my-app-prod-123/path/file.pdf --expires-in 900
```

### Lifecycle (cost control)

```json
{
  "Rules": [{
    "ID": "expire-old-versions",
    "Status": "Enabled",
    "NoncurrentVersionExpiration": { "NoncurrentDays": 30 },
    "Filter": { "Prefix": "" }
  }]
}
```

```bash
aws s3api put-bucket-lifecycle-configuration --bucket my-app-prod-123 \
  --lifecycle-configuration file://lifecycle.json
```

### Static website hosting

Turns a bucket into website mode (index/error documents). Prefer [[CloudFront]] + private origin for HTTPS and edge; website endpoint is HTTP and older pattern.

```bash
aws s3 website s3://$BUCKET --index-document index.html --error-document error.html
```

| Flag | Meaning |
|------|---------|
| `aws s3 website` | Enable website hosting mode |
| `s3://$BUCKET` | Target bucket |
| `--index-document` | Object served at `/` |
| `--error-document` | Custom 404 (still needs public or CloudFront error pages) |

Public website needs a **bucket policy** allowing `s3:GetObject` **and** Block Public Access relaxed for that policy — easy to get wrong; CloudFront OAC keeps the bucket private.

### VPC endpoint

Gateway endpoint for S3 (route table entry, no hourly charge) — prefer over NAT for private-subnet `PutObject`/`GetObject`.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 403 Access Denied | Block Public Access; bucket policy; IAM; KMS key policy | Align all four; Access Analyzer |
| Works in console, fails in app | Wrong role / region / bucket ARN | Fix [[ARN (Amazon Resource Name)]]; region endpoint |
| SSE-KMS upload fail | Key policy for role + `s3.amazonaws.com` | [[KMS]] |
| Website 403 / XML error | Public access + policy + website endpoint URL | Policy; or switch to CloudFront |
| Bill spike | Versions, incomplete multipart, data transfer | Lifecycle; abort MPU; CloudFront for egress |
| Terraform state lock weirdness | DynamoDB lock table + bucket versioning | [[Terraform setup]] · [[AWS DynamoDB]] |

## Gotchas

> [!WARNING]
> **Block Public Access overrides a “public” bucket policy** — intentional; don't disable account-wide BPA lightly.

> [!WARNING]
> **Object ACLs are legacy** — prefer bucket owner enforced + policies.

> [!WARNING]
> **Website endpoint ≠ REST endpoint** — different hostname; HTTPS on website endpoint is not ACM-friendly (use CloudFront).

> [!WARNING]
> **Versioning without lifecycle** — deleted “keys” become noncurrent versions that still bill.

## When NOT to use

- **POSIX shared filesystem** — [[AWS EFS (Elastic File System)]] / FSx.
- **Low-latency database** — RDS / DynamoDB, not S3 as primary store.
- **Public static site without CDN** — use [[CloudFront]] for TLS and caching.

## Related

[[AWS]] · [[IAM]] · [[ARN (Amazon Resource Name)]] · [[KMS]] · [[CloudFront]] · [[AWS Billing and cost management]] · [[Terraform setup]] · [[AWS DynamoDB]]
