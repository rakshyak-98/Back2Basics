[[aws STS (Security Token Service)]] [[ARN (Amazon Resource Name)]] [[Security group]] [[AWS EC2]] [[AWS Lambda]]

# IAM

> Identity and Access Management decides which AWS principals can perform which API actions on which resources — an explicit `Deny` always wins over `Allow`.

```txt
        IAM ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               └── Use cases
```

## Why It Matters
- **Key signal:** IAM reviews probe least privilege, identity vs resource policies, role ass…

## Sources
- [IAM JSON policy reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html) — deep-dive
- [Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) — deep-dive

## Key Concepts
| Object | Role |
|--------|------|
| **Principal** | Who is calling: IAM user, role, federated user, or AWS service |
| **Policy** | JSON document listing `Effect`, `Action`, `Resource`, optional `Condition` |
| **User** | Long-lived identity; avoid access keys in production |
| **Group** | Collection of users for shared policy attachment |
| **Role** | Assumable identity with temporary credentials via [[aws STS (Security Token Service)]] |
| **Policy attachment** | Identity-based (on user/role/group) or resource-based (on S3 bucket, KMS key, etc.) |

- **Note:** Authorization is evaluated at request time. AWS combines all applicable polic…

## Technical Details
### Evaluation flow

```
API request
    │
    ▼
Authentication (SigV4, web identity, etc.)
    │
    ▼
Organization SCP (if in AWS Organizations) — maximum permission ceiling
    │
    ▼
Identity policy + resource policy + session policy
    │
    ▼
Permission boundary (if set) — caps effective permissions
    │
    ▼
Allow / implicit deny
```

- **Service control policies (SCPs):** apply to member accounts in an organizati…
- **Permission boundaries:** cap what an administrator can grant to a user or ro…

### Common failures

| Symptom | Likely cause |
|---------|----------------|
| `AccessDenied` on S3 | Missing identity policy, bucket policy, or KMS key policy |
| Lambda cannot reach VPC resource | Execution role lacks `ec2:CreateNetworkInterface` or security group blocks traffic |
| Cross-account access fails | Trust policy on target role does not list source principal |
| Admin cannot grant permission | Permission boundary or SCP blocks the action |

### CLI checks

```bash
aws sts get-caller-identity
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/MyRole \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/object-key
```

## Real-World Applications
- **Note:** **Prefer roles over users.** EC2 instance profiles, Lambda execution roles, a…

- **Note:** **Least privilege.** Start with AWS managed job-function policies only as a s…

- **Note:** **Break-glass users** should be MFA-protected, rarely used, and monitored wit…

### Trust policy (who can assume a role)

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "ec2.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
```

### Permission policy (what the role can do)

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::my-bucket/*"
  }]
}
```
