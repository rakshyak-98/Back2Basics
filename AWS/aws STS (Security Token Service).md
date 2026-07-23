[[IAM]] [[ARN (Amazon Resource Name)]] [[JWT authentication]] [[Security]]

# AWS STS (Security Token Service)

> Short-lived **temporary credentials** (AccessKeyId, SecretAccessKey, SessionToken) instead of long-lived IAM user keys — foundation for roles, federation, and cross-account access. **AWS IAM docs** + incident stories from leaked static keys.

## Mental model

STS is AWS's **token mint**: you prove identity (IAM user, role, SAML/OIDC, or another account's role), STS returns credentials valid for **minutes to hours**, bound to an **IAM role's permissions**. Every `AssumeRole`, EC2 instance profile, Lambda execution role, and `aws sso login` session flows through STS.

```
Caller ──► sts:AssumeRole ──► temporary creds ──► AWS APIs (scoped to role policy)
                │
                └── CloudTrail logs who assumed what, when
```

**Permanent access keys** = long-lived secret on disk. **STS** = rotate automatically, auditable session, optional external-id/confused-deputy protection.

## Standard config / commands

### AssumeRole (CLI / automation)

```bash
# Who am I right now?
aws sts get-caller-identity

# Assume role in same or cross account
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/DeployRole \
  --role-session-name ci-deploy-$(date +%s) \
  --external-id "$EXTERNAL_ID"   # required if trust policy enforces it

# Export for shell (15–60 min typical)
eval "$(aws sts assume-role ... --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' --output text | \
  awk '{print "export AWS_ACCESS_KEY_ID="$1"\nexport AWS_SECRET_ACCESS_KEY="$2"\nexport AWS_SESSION_TOKEN="$3}')"
```

### Trust policy (cross-account — **ExternalId** for third parties)

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "AWS": "arn:aws:iam::PARTNER:role/TheirRole" },
    "Action": "sts:AssumeRole",
    "Condition": { "StringEquals": { "sts:ExternalId": "unique-shared-secret" } }
  }]
}
```

### Instance / pod identity (no keys on disk)

- **EC2 instance profile** → IMDS delivers rotating role creds (prefer IMDSv2: `HttpTokens: required`).
- **EKS IRSA** → OIDC trust to `sts:AssumeRoleWithWebIdentity`.
- **Lambda** → execution role creds injected by runtime.

### SSO / Identity Center

```bash
aws sso login --profile prod
aws sts get-caller-identity --profile prod   # shows assumed SSO role ARN
```

### Duration knobs

- `DurationSeconds`: 900–43200 (role max in trust policy caps this).
- Shorter for human sessions; CI can use 1h with OIDC federation (GitHub Actions → AWS).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `AccessDenied` on `AssumeRole` | Trust policy Principal; role name/ARN; ExternalId | Fix trust `Principal`; pass correct ExternalId |
| `ExpiredToken` mid-deploy | Session duration; clock skew on host | Re-assume; sync NTP; increase duration within max |
| Works locally, fails in CI | OIDC thumbprint/audience; repo/org condition | Fix IdP trust; scope `sub`/`aud` conditions |
| EC2/Lambda "can't reach AWS APIs" | Instance profile attached? IMDS blocked? | Attach profile; fix IMDS hop limit (containers need 2) |
| Cross-account S3/KMS denied after assume | **Resource policy** on bucket/key must trust role ARN | Update bucket/key policy for assumed role principal |
| `InvalidIdentityToken` (EKS) | Service account annotation `eks.amazonaws.com/role-arn` | IRSA setup; OIDC provider on cluster |

## Gotchas

> [!WARNING]
> **Assumed-role creds need all three env vars** — `AWS_SESSION_TOKEN` missing → obscure signature errors.

> [!WARNING]
> **Confused deputy**: cross-account trust without `ExternalId` or `aws:SourceAccount` condition — partner account could trick your role into acting on their resources. Always scope trust policies.

> [!WARNING]
> **IMDSv1 + SSRF** — attacker on instance steals role creds via metadata. Enforce IMDSv2; block metadata from untrusted containers (hop limit).

> [!WARNING]
> **CloudTrail `AssumeRole` ≠ data-plane access** — session may be valid but IAM policy or SCP denies the API call. Check identity **and** permission boundaries.

## When NOT to use

- **Long-lived IAM user access keys for apps** — use roles + STS; keys for break-glass humans only, rotated and scoped.
- **Embedding AssumeRole in every micro-request** — cache creds until ~5 min before expiry; use SDK default credential chain.
- **One mega-role for all environments** — separate roles per env/account; STS makes splitting cheap.

## Related

[[IAM]] · [[ARN (Amazon Resource Name)]] · [[Security group]] · [[AWS EC2]] · [[JWT authentication]]
