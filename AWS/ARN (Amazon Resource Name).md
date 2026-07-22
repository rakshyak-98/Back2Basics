[[IAM]] [[aws STS (Security Token Service)]] [[AWS EC2]] [[AWS ECR]]

# ARN (Amazon Resource Name)

> **Universal resource identifier** for IAM policies, CloudTrail, cross-service references, and CLI `--resource-arn`. Format is strict — one wrong segment = `AccessDenied` or wrong resource.

## Mental model

Every AWS resource that policies reference gets an **ARN**: partition, service, region (sometimes empty), account, resource path. IAM evaluates **string match** on ARNs in policies; typos and missing account ids are silent until runtime.

```
arn : partition : service : region : account-id : resource
│      aws         s3        (empty)  123456789012   bucket/key
│      aws         ec2       us-east-1 123456789012   instance/i-0abc...
│      aws         iam       (empty)  123456789012   role/AppRole
```

Some services use **path-style** resources (`role/Team/App`), others **ARN generators** (S3 object = bucket + key).

## Standard config / commands

### Common ARN shapes

| Service | Example ARN | Notes |
|---------|-------------|-------|
| IAM user | `arn:aws:iam::123456789012:user/john` | No region |
| IAM role | `arn:aws:iam::123456789012:role/AppRole` | Used in trust + PassRole |
| EC2 instance | `arn:aws:ec2:us-east-1:123456789012:instance/i-0abc` | Region required |
| S3 object | `arn:aws:s3:::my-bucket/path/file.txt` | Bucket name in resource |
| Lambda | `arn:aws:lambda:us-east-1:123456789012:function:my-fn` | |
| KMS key | `arn:aws:kms:us-east-1:123456789012:key/uuid` | Key policies use full ARN |
| ECR image | `arn:aws:ecr:us-east-1:123456789012:repository/app` | |

### Policy snippets (exact ARN matters)

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/production/*"
}
```

```bash
# Resolve ARN from CLI
aws sts get-caller-identity   # account id
aws ec2 describe-instances --instance-ids i-xxx --query 'Reservations[0].Instances[0].InstanceArn'
aws iam get-role --role-name AppRole --query 'Role.Arn'
```

### Partitions

- `aws` — commercial; `aws-us-gov`, `aws-cn` — isolated partitions; ARNs **don't cross** partitions.

### Wildcards in policies

- `arn:aws:s3:::my-bucket/*` — all objects; not other buckets.
- `*` in action/resource — last resort; prefer prefix scoping.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Policy "looks right" but Deny | Wrong account id in ARN | Copy ARN from `describe-*` API |
| Cross-region copy/snapshot fail | Source/dest ARNs region mismatch | Use region-local ARNs |
| KMS `InvalidArnException` | Key ARN vs alias (`alias/xxx`) | Use key id ARN in key policies |
| EventBridge target fail | Target ARN service mismatch | Verify full target ARN format |
| Organization SCP not applying | ARN in member account vs org id | SCP uses different principal patterns |

## Gotchas

> [!WARNING]
> **S3 ARN has no region in resource** — but bucket is regional; policies still work; **some services need bucket location** for cross-region ops.

> [!WARNING]
> **IAM ARNs never include region** — `arn:aws:iam::123:role/x` is global within partition.

> [!WARNING]
> **Assumed-role session ARN** in CloudTrail differs from role ARN — use `sessionContext` for attribution.

> [!WARNING]
> **Copy-paste from console** sometimes shows **partial ARN** — always verify six colon segments (except optional empty region).

## When NOT to use

- **Human-readable naming in automation** — construct from API responses; don't hand-build instance ids.
- **ARN as secret** — ARNs are identifiers, not authorization; knowing ARN doesn't grant access without policy.

## Related

[[IAM]] · [[aws STS (Security Token Service)]] · [[AWS EC2]] · [[AWS ECR]] · [[Security group]]
