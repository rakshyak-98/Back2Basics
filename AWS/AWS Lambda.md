[[IAM]] [[ARN (Amazon Resource Name)]] [[aws STS (Security Token Service)]] [[AWS ECR]] [[AWS Networking]]

# AWS Lambda

> AWS Lambda — runs your function on events and bills only while it runs.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

Lambda is **stateless compute on demand**: an event (API Gateway, SQS, S3, EventBridge, cron) invokes a **handler** in a managed runtime (or container image). You do not manage servers; you manage **execution role**, **memory**, **timeout**, **concurrency**, and **triggers**. Cold start = new execution environment; warm reuse is best-effort, not a guarantee.

```
Event source ──► Lambda service ──► execution env (runtime + your code)
                      │                    │
                      ├── concurrency gate │── handler(event, context)
                      └── IAM role (STS)   └── /tmp, env vars, layers
```

| Knob                        | What it actually controls                               |
| --------------------------- | ------------------------------------------------------- |
| **Memory**                  | CPU share scales with memory (more MB ≈ more vCPU)      |
| **Timeout**                 | Hard kill after N seconds (max 15 min)                  |
| **Reserved concurrency**    | Cap for this function (also reserves from account pool) |
| **Provisioned concurrency** | Pre-warmed envs — kills cold starts, costs money idle   |
| **Execution role**          | What AWS APIs the function can call ([[IAM]])           |

Billing ≈ **requests + GB-seconds** (and provisioned concurrency if used). Retries multiply both.

## Standard config / commands

### 1. Prerequisites

```bash
aws configure          # or: aws sso login
aws sts get-caller-identity
```

Need: account access, a region, and an [[IAM]] role Lambda can assume (`lambda.amazonaws.com` trust).

### 2. Execution role (required)

```json
// Trust — who may assume this role
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "lambda.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
```

Attach least-privilege policies. Minimum for logs:

- `arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole` (CloudWatch Logs)

VPC-attached functions also need:

- `arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole` (ENI create/describe/delete)

```bash
aws iam create-role --role-name lambda-api-exec \
  --assume-role-policy-document file://trust-lambda.json

aws iam attach-role-policy --role-name lambda-api-exec \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

### 3. Create function (zip runtime)

```bash
# handler file: index.mjs  →  exports.handler
zip function.zip index.mjs

aws lambda create-function \
  --function-name api-handler \
  --runtime nodejs20.x \
  --role arn:aws:iam::ACCOUNT:role/lambda-api-exec \
  --handler index.handler \
  --timeout 10 \
  --memory-size 256 \
  --zip-file fileb://function.zip \
  --environment "Variables={NODE_ENV=production,LOG_LEVEL=info}" \
  --architectures arm64
```

| Setting           | Prod default                     | Why                                            |
| ----------------- | -------------------------------- | ---------------------------------------------- |
| `--timeout`       | 3–30s for APIs; longer for batch | Fail fast; don't hide hung deps                |
| `--memory-size`   | Start 256–512; load-test         | Under-memory = CPU starve + timeouts           |
| `--architectures` | `arm64` when deps allow          | Often cheaper/faster per GB-s                  |
| Env vars          | Non-secrets only                 | Secrets → Secrets Manager / SSM, not plain env |
| Ephemeral `/tmp`  | ≤ 512 MB–10 GB (config)          | Not durable storage                            |

### 4. Update code / config

```bash
aws lambda update-function-code \
  --function-name api-handler \
  --zip-file fileb://function.zip

aws lambda update-function-configuration \
  --function-name api-handler \
  --timeout 15 \
  --memory-size 512 \
  --environment "Variables={NODE_ENV=production,LOG_LEVEL=debug}"

# Wait until LastUpdateStatus = Successful before next update
aws lambda get-function-configuration --function-name api-handler \
  --query '{State:State,LastUpdateStatus:LastUpdateStatus,Timeout:Timeout,Memory:MemorySize}'
```

### 5. Invoke & logs

```bash
aws lambda invoke \
  --function-name api-handler \
  --payload '{"ping":true}' \
  --cli-binary-format raw-in-base64-out \
  response.json && cat response.json

aws logs tail /aws/lambda/api-handler --follow
```

### 6. Concurrency & async behavior

```bash
# Cap this function (also reserves from account unreserved pool)
aws lambda put-function-concurrency \
  --function-name api-handler \
  --reserved-concurrent-executions 50

# Async invoke retry / DLQ (SQS or SNS)
aws lambda put-function-event-invoke-config \
  --function-name api-handler \
  --maximum-retry-attempts 2 \
  --destination-config '{"OnFailure":{"Destination":"arn:aws:sqs:REGION:ACCOUNT:lambda-dlq"}}'
```

### 7. Triggers (wire after function exists)

| Source | Typical setup |
|--------|----------------|
| **API Gateway / HTTP API** | Integration → Lambda permission `lambda:InvokeFunction` for `apigateway.amazonaws.com` |
| **SQS** | Event source mapping; set batch size + partial failure reporting |
| **S3** | Bucket notification + resource-based policy on function |
| **EventBridge / cron** | Rule target = function ARN |
| **ALB** | Target group type `lambda` |

```bash
# Example: allow EventBridge to invoke
aws lambda add-permission \
  --function-name api-handler \
  --statement-id AllowEventBridge \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:REGION:ACCOUNT:rule/my-rule
```

### 8. Container image (large deps / custom runtime)

Build → push [[AWS ECR]] → create function from image URI. Image must implement the [Lambda Runtime API](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html) (or use an AWS base image).

```bash
aws lambda create-function \
  --function-name api-handler-img \
  --package-type Image \
  --code ImageUri=ACCOUNT.dkr.ecr.REGION.amazonaws.com/api:latest \
  --role arn:aws:iam::ACCOUNT:role/lambda-api-exec \
  --timeout 30 \
  --memory-size 1024
```

### 9. VPC (only when you must reach private resources)

Attach private subnets + SG that can reach RDS/ElastiCache. Requires NAT (or VPC endpoints) for public AWS APIs and the internet. Expect **longer cold starts** (ENI attach). Prefer VPC endpoints for S3/Secrets Manager/STS over blanket NAT.

```bash
aws lambda update-function-configuration \
  --function-name api-handler \
  --vpc-config SubnetIds=subnet-aaa,subnet-bbb,SecurityGroupIds=sg-xxx
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `AccessDeniedException` / can't talk to S3/Dynamo | Execution role policies; resource policies | Least-privilege allow on role; fix resource ARN ([[ARN (Amazon Resource Name)]]) |
| Timeout near limit | CW Logs duration; downstream latency; memory | Raise memory (CPU) or timeout; fix hung I/O; shorten work |
| Cold start latency spikes | Init duration in logs; VPC?; large package | Slim package; arm64; provisioned concurrency; avoid VPC if possible |
| `ResourceConflictException` on update | Previous update still in progress | Poll `LastUpdateStatus`; serialize deploys |
| Throttling (`429` / `Rate exceeded`) | Reserved concurrency too low; account concurrency | Raise reserved or account limit; backpressure at source |
| Async retries / duplicate side effects | Event source retry + DLQ empty | Idempotent handler; DLQ + alarm; SQS partial batch failure |
| Can't reach RDS in VPC | Subnets, SG, route, ENI role policy | Fix SG path; attach VPCAccessExecutionRole; multi-AZ subnets |
| `CodeStorageExceededException` | Account code storage quota | Delete old versions; use images or S3 for large artifacts |
| Handler not found | `--handler` path vs export name | Fix `file.export`; zip from correct root (no nested junk folder) |

## Gotchas

> [!WARNING]
> **Retries are a feature** — SQS, async invoke, and stream consumers retry. Non-idempotent writes → duplicate charges, double emails, double orders. Design for at-least-once.

> [!WARNING]
> **Reserved concurrency = 0** effectively disables invokes. Setting reserved on many functions can starve the account unreserved pool.

> [!WARNING]
> **VPC Lambda without NAT/endpoints** — function cannot reach public internet or many AWS APIs; looks like mysterious timeouts.

> [!WARNING]
> **Env vars are not secret storage** — visible to anyone with `GetFunctionConfiguration`. Use Secrets Manager / SSM + IAM; cache secrets in-process carefully.

> [!WARNING]
> **`/tmp` and global variables survive warm invokes** — useful for connection reuse; dangerous for request-scoped state leaking between invokes.

> [!WARNING]
> **15-minute hard max** — long ETL belongs on Fargate, Batch, Step Functions, or EC2 — not a stretched Lambda timeout.

## When NOT to use

- **Steady 24/7 high-QPS with tiny payloads** — often cheaper/simpler on ECS/Fargate or EC2 behind an ALB once always-on.
- **Workloads needing >15 minutes wall clock** — Step Functions + workers, Batch, or a job runner.
- **WebSockets / sticky long-lived connections** — API Gateway WebSocket + Lambda is possible but awkward; consider dedicated connection brokers.
- **Heavy GPU / specialized hardware** — not Lambda's model (use appropriate compute).

## Related

[[IAM]] · [[ARN (Amazon Resource Name)]] · [[aws STS (Security Token Service)]] · [[AWS ECR]] · [[AWS Networking]] · [[Security group]] · [[AWS EC2]] · [[node serverless]]
