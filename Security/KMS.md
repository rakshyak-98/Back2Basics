[[TLS (Transport Layer Security)]] [[JWT authentication]] [[Security]] [[Token rotation]] [[aws STS (Security Token Service)]]

# KMS (Key Management Service)

> Managed cryptographic keys (often HSM-backed) so apps encrypt data without holding long-term master key material.

```txt
        KMS (Key Managemen ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Cloud security: envelope encryption, CMK vs data keys, and why apps call KMS …

## Sources
- [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/) — deep-dive
- [NIST SP 800-57 — Key Management](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final) — overview

## Key Concepts
- **Note:** KMS stores **Customer Master Keys (CMKs)**

```
- **Note:** App ──► GenerateDataKey ──► plaintext data key + encrypted blob
         │                         │
- **Note:** └── encrypt local data └── store encrypted key with ciphertext
```

- **Note:** **Key policy** (resource-based, mandatory on CMK) + **IAM** (identity-based) …


- **Core:** A Key Management Service stores and uses cryptographic keys (often in HSM-bac…

## Technical Details
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

- **`alias/prod-app`:** — human-friendly
- **Automatic key rotation:** (annual) — AWS rotates backing material

### Grants (cross-account / ephemeral)

- `CreateGrant` for scoped delegate access (e.g. AWS service on your behalf)

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `AccessDeniedException` on Decrypt | Key policy **and** IAM; VPC endpoint? | Add role to key policy; `kms:ViaService` conditions |
| S3 SSE-KMS upload fail | Bucket default encryption key; key policy for S3 | Allow S3 service principal in key policy |
| Lambda/RDS can't read secret | Secret encrypted with CMK; execution role lacks kms:Decrypt | Grant role on CMK used by Secrets Manager |
| Cross-account Deny | CMK not shared; external account principal | Key policy `Principal` for other account role |
| `DisabledException` | Key disabled or pending deletion | Re-enable; cancel deletion window (7–30 days) |
| Higher latency | KMS API per-object encrypt | Data key caching (within compliance bounds); batch |

## Mistakes to Avoid
- **Mistake:** IAM Allow alone is insufficient
- **Mistake:** Scheduled deletion is irreversible after waiting period
- **Mistake:** CloudWatch Logs SSE-KMS
- **Mistake:** Multi-Region keys (MRK)

## Pros/Cons or Trade-offs
- **Pro:** Master keys stay in HSM-backed service with IAM audit trails.
- **Con:** application-level secrets in environment variables without envelope — use Secrets Manager/SSM Parameter Store **with** KMS CMK.
- **Con:** Password hashing — KMS encrypt ≠ bcrypt/Argon2; use for **encryption at rest**, not password storage.
- **Con:** High-frequency per-field encrypt on hot path without cache — cost + latency; batch or use AES-GCM with rotated data keys.

## Comparison
- vs app-local key files: KMS keeps master keys in HSM-backed service with IAM audit.
- vs [[TLS (Transport Layer Security)]]: TLS protects data in transit


### Use cases
- Envelope-encrypt database fields or S3 objects with a data key, wrapping that…
