[[IAM]] [[aws STS (Security Token Service)]] [[AWS EC2]] [[AWS Lambda]] [[AWS ECR]]

# ARN (Amazon Resource Name)

> An ARN is the stable, globally unique identifier AWS uses in IAM policies, CloudTrail logs, and cross-service references — get the partition, service, region, account, and resource path wrong and authorization silently…

```txt
        ARN (Amazon Resour ──┬── Why it matters
               ├── Sources
               ├── Concepts
               └── Mechanism
```

## Why It Matters
- **Key signal:** ARN literacy shows you can scope IAM policies precisely

## Sources
- [Identify AWS resources using ARNs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) — deep-dive
- [AWS service authorization reference](https://docs.aws.amazon.com/service-authorization/latest/reference/reference.html) — deep-dive

## Key Concepts
```
arn:partition:service:region:account-id:resource
```

| Segment | Examples |
|---------|----------|
| `partition` | `aws` (commercial), `aws-cn`, `aws-us-gov` |
| `service` | `s3`, `ec2`, `iam`, `lambda`, `kms` |
| `region` | `us-east-1`; global services often use `*` or empty |
| `account-id` | 12-digit AWS account number |
| `resource` | Service-specific path or ID |

Examples:

```
- **Note:** arn:aws:ec2:us-east-1:123456789012:instance/i-0abcd1234efgh5678
arn:aws:s3:::my-bucket/object-key
arn:aws:iam::123456789012:role/AppRole
arn:aws:lambda:us-east-1:123456789012:function:processor
```

- **Note:** S3 ARNs omit region and account in the bucket form

## Technical Details
### Where ARNs matter

- **IAM policies:** — `Resource` elements almost always use ARN patterns with `*` wildcards.
- **Resource-based policies:** — S3 bucket policies, KMS key policies, Lambda function URLs reference princi…
- **CloudTrail:** — `eventSource`, `resources`, and `recipientAccountId` tie events to ARNs.
- **Cross-account access:** — trust policies list principal ARNs; resource policies grant them access.

### Wildcards in policies

```json
"Resource": "arn:aws:s3:::logs-*/*"
```

- `*` matches within a segment; `?` matches a single character.
- Overly broad `Resource: "*"` is convenient in sandboxes and dangerous in prod…

### ARN vs name vs ID

| Identifier | Example | Use |
|------------|---------|-----|
| ARN | `arn:aws:ec2:...:instance/i-abc` | Policies, auditing |
| Resource ID | `i-0abc123` | Console, many CLI calls |
| Friendly name | `web-server-1` | Human operations; not always unique globally |
