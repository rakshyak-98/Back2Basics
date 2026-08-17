[[IAM]] [[AWS Networking]] [[AWS ECR]] [[AWS cli commands]]

# AWS Lambda

> Lambda runs your code in response to events without managing servers — cold starts, timeout limits, and IAM execution roles are usually what bite first.





## Interview Relevance
Lambda questions probe cold starts, IAM execution roles, concurrency limits, and when containers/EC2 fit better.

## Sources
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) — deep-dive
- [Lambda quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html) — overview

## Technical Details
### Execution model

1. **Upload** deployment package or container image to Lambda.
2. **Configure** handler, runtime (or container), memory, timeout, environment variables.
3. **Attach** execution role ([[IAM]]) with least-privilege permissions.
4. **Invoke** via API Gateway, SQS, EventBridge, S3 notifications, direct invoke, etc.

Lambda scales concurrent executions per account and per function. **Reserved concurrency** caps or guarantees capacity.

### Key limits (verify current docs for your region)

| Setting | Typical bound |
|---------|----------------|
| Timeout | 15 minutes max |
| Memory | 128 MB – 10,240 MB (affects CPU proportionally) |
| Deployment package | 50 MB zipped direct upload; larger via S3 |
| /tmp storage | 512 MB – 10,240 MB configurable |
| Environment variables | 4 KB total |

### VPC access

Functions in a VPC get ENIs in your subnets for private resource access (RDS, ElastiCache). Cold starts increase because ENI setup takes time. Prefer **VPC endpoints** for AWS APIs to avoid NAT.

### Packaging

```bash
zip function.zip index.mjs
aws lambda create-function \
  --function-name hello \
  --runtime nodejs20.x \
  --role arn:aws:iam::123456789012:role/lambda-exec \
  --handler index.handler \
  --zip-file fileb://function.zip
```

Container images pull from [[AWS ECR]] using the same Lambda service.

### Observability

- **CloudWatch Logs** — `/aws/lambda/<function-name>`
- **X-Ray** — distributed tracing when enabled
- **Metrics** — Duration, Errors, Throttles, ConcurrentExecutions

### Cost drivers

Invocations, duration (GB-seconds), provisioned concurrency, and data transfer. Right-size memory by profiling — more memory can reduce total cost if execution time drops enough.
