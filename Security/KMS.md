[[TLS (Transport Layer Security)]] [[JWT authentication]] [[Security]] [[Token rotation]]

# KMS (Key Management Service)

> **Managed encryption keys** — envelope encryption for AWS services and your apps; keys never leave HSM in plaintext. **AWS KMS docs** + outages when key policy and IAM both had to align.

## Mental model

KMS stores **Customer Master Keys (CMKs)** — symmetric (default) or asymmetric (sign/verify). Data is encrypted with **data keys**; data keys are wrapped by CMK (**envelope encryption**). Every use calls `kms:Decrypt/GenerateDataKey` — logged in CloudTrail.

```
App ──► GenerateDataKey ──► plaintext data key + encrypted blob
         │                         │
         └── encrypt local data      └── store encrypted key with ciphertext
```

**Key policy** (resource-based, mandatory on CMK) + **IAM** (identity-based) **both** must allow — unlike most AWS resources where IAM alone suffices.

## Standard config / commands

### CMK key policy (minimum + admin)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Enable IAM policies",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::123456789012:root" },
      "Action": "kms:*",
      "Resource": "*"
    },
    {
      "Sid": "Allow app role",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::123456789012:role/AppRole" },
      "Action": ["kms:Decrypt", "kms:GenerateDataKey"],
      "Resource": "*"
    }
  ]
}
```

### Encrypt/decrypt (SDK pattern)

```bash
aws kms encrypt --key-id alias/prod-app --plaintext fileb://secret.bin --output text --query CiphertextBlob
aws kms decrypt --ciphertext-blob fileb://blob.bin --query Plaintext --output text | base64 -d
```

### Aliases vs key ids

- **`alias/prod-app`** — human-friendly; rotate underlying CMK with alias re-point (manual or automation).
- **Automatic key rotation** (annual) — AWS rotates backing material; **same key id**, decrypt old ciphertext still works.

### Grants (cross-account / ephemeral)

- `CreateGrant` for scoped delegate access (e.g. AWS service on your behalf) — audit in CloudTrail.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `AccessDeniedException` on Decrypt | Key policy **and** IAM; VPC endpoint? | Add role to key policy; `kms:ViaService` conditions |
| S3 SSE-KMS upload fail | Bucket default encryption key; key policy for S3 | Allow S3 service principal in key policy |
| Lambda/RDS can't read secret | Secret encrypted with CMK; execution role lacks kms:Decrypt | Grant role on CMK used by Secrets Manager |
| Cross-account Deny | CMK not shared; external account principal | Key policy `Principal` for other account role |
| `DisabledException` | Key disabled or pending deletion | Re-enable; cancel deletion window (7–30 days) |
| Higher latency | KMS API per-object encrypt | Data key caching (within compliance bounds); batch |

## Gotchas

> [!WARNING]
> **IAM Allow alone is insufficient** — CMK key policy must trust the caller (unless account root delegation pattern used correctly).

> [!WARNING]
> **Scheduled deletion is irreversible after waiting period** — all ciphertext using that CMK becomes undecryptable.

> [!WARNING]
> **CloudWatch Logs SSE-KMS** — needs key policy for `logs.region.amazonaws.com`.

> [!WARNING]
> **Multi-Region keys (MRK)** — replicate for DR; same key material; not the same as automatic rotation.

## When NOT to use

- **App-level secrets in env vars without envelope** — use Secrets Manager/SSM Parameter Store **with** KMS CMK.
- **Password hashing** — KMS encrypt ≠ bcrypt/Argon2; use for **encryption at rest**, not password storage.
- **High-frequency per-field encrypt on hot path without cache** — cost + latency; batch or use AES-GCM with rotated data keys.

## Related

[[TLS (Transport Layer Security)]] · [[JWT authentication]] · [[Token rotation]] · [[Security]] · [[aws STS (Security Token Service)]]
