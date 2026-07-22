[[aws STS (Security Token Service)]] [[ARN (Amazon Resource Name)]] [[Security group]] [[AWS EC2]]

# IAM

> **Who can do what to which resource** — users, groups, roles, policies, permission boundaries, and SCPs (org level). **AWS IAM best practices** + audit findings from over-privileged CI roles.

## Mental model

IAM is AWS's authorization graph: **principals** (users, roles, federated identities) assume **policies** (identity-based + resource-based) evaluated at API call time. **Roles** (with [[aws STS (Security Token Service)]]) are the production default; **users + access keys** are legacy/break-glass.

```
Request ──► AuthN (who) ──► IAM policy eval ──► Allow/Deny ──► API
                │                    │
                └── SCP (org max)    └── resource policy (S3/KMS/Lambda)
```

**Deny always wins.** Permission boundary caps what a role/user can ever receive even if admin attaches `AdministratorAccess`.

## Standard config / commands

### Role for compute (pattern)

```json
// Trust policy — who can assume
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "ec2.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
```

Attach **managed or inline policy** with least privilege — e.g. `s3:GetObject` on `arn:aws:s3:::my-bucket/*`, not `s3:*`.

```bash
aws iam get-role --role-name AppRole
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123:role/AppRole \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/key
```

### Groups for humans

- Humans in **groups** (`Developers`, `ReadOnly`); permissions on groups, not individual users.
- **MFA** enforced via policy condition `aws:MultiFactorAuthPresent`.

### Audit tooling (built-in)

| Tool | Scope | Use |
|------|-------|-----|
| **Credentials Report** | Account — all users, key age, MFA | Quarterly key rotation audit |
| **Access Advisor** | Per user/role — last used services | Right-size policies; remove stale grants |
| **Access Analyzer** | External access paths | Find public S3, cross-account trust |

```bash
aws iam generate-credential-report && aws iam get-credential-report --query 'Content' --output text | base64 -d
```

### Identity Center (SSO)

- Prefer **IAM Identity Center** over long-lived IAM users for console/CLI (`aws sso login`).
- Permission sets = roles in target accounts.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `AccessDenied` despite "Admin" | SCP? Permission boundary? Session policy? | Org SCP; boundary; explicit Deny in policy |
| CI deploy role stopped working | OIDC trust repo branch; role session name | Fix IdP condition keys |
| Cross-account S3/KMS fail after role fix | **Resource policy** on bucket/key | Add `Principal` for role ARN |
| `InvalidUserID.NotFound` | Wrong account/ partition in [[ARN (Amazon Resource Name)]] | Fix ARN |
| New hire can't console login | Identity Center assignment; IdP sync | Assign permission set; SCIM/group mapping |
| `AccessDeniedException` on PassRole | `iam:PassRole` for deployment roles | Scope PassRole to specific role ARNs |

## Gotchas

> [!WARNING]
> **Default service roles** (`AWSServiceRoleForSupport`, `AWSServiceRoleForTrustedAdvisor`) — AWS-managed; don't delete; not where your app permissions live.

> [!WARNING]
> **Policy size limit (6144 chars inline)** — use managed policies + composition; refactor with policy variables in Terraform.

> [!WARNING]
> **`Resource: "*"` + `Action: "*"` on CI role** — full account compromise if pipeline leaked. Scope to deployment ARNs.

> [!WARNING]
> **IAM eventual consistency** — new role/policy may take seconds; retry with backoff in automation.

## When NOT to use

- **IAM users with access keys for application runtime** — use instance profile / IRSA / Lambda execution role.
- **Shared root account credentials** — enable root MFA; lock root to break-glass only.
- **Duplicating AWS-managed policy by copy-paste** — attach `AWS managed` and add small custom policy for deltas.

## Related

[[aws STS (Security Token Service)]] · [[ARN (Amazon Resource Name)]] · [[Security group]] · [[AWS EC2]] · [[AWS ECR]]
