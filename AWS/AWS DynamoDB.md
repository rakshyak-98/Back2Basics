[[AWS]] [[IAM]] [[ARN (Amazon Resource Name)]] [[AWS Lambda]] [[Terraform setup]] [[AWS Billing and cost management]]

# AWS DynamoDB

> Managed key-value / document store — partition key design dominates performance; capacity mode and hot partitions dominate cost and throttles. Used for app data **and** Terraform state locks.

## Mental model

Every item lives in a **partition** chosen by the **partition key** (and optional sort key). Throughput is per-table (on-demand or provisioned RCU/WCU). **Streams** emit change records for Lambda. Strong vs eventual consistency is a read-time choice (strong costs more RCU).

```
App ──► GetItem / Query / PutItem
              │
              ├── partition key → shard
              └── Stream ──► Lambda
```

| Mode | When |
|------|------|
| **On-demand** | Spiky / unknown traffic |
| **Provisioned + auto scaling** | Steady predictable load |
| **TTL** | Expire items without custom sweeper |

Terraform S3 backend often uses a small DynamoDB table for **state locking** ([[Terraform setup]]).

## Standard config / commands

### Table sketch

```bash
aws dynamodb create-table \
  --table-name app-tasks \
  --attribute-definitions \
    AttributeName=pk,AttributeType=S AttributeName=sk,AttributeType=S \
  --key-schema \
    AttributeName=pk,KeyType=HASH AttributeName=sk,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST

aws dynamodb describe-table --table-name app-tasks \
  --query 'Table.{Status:TableStatus,Arn:TableArn,Keys:KeySchema}'
```

### Access patterns first

Design keys for **Query**, not Scan. GSIs for alternate access — each GSI has its own capacity/cost.

### IAM

Least privilege: `dynamodb:GetItem` / `Query` / `PutItem` on `arn:aws:dynamodb:REGION:ACCOUNT:table/app-tasks` (+ index ARNs if needed).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `ProvisionedThroughputExceeded` | Hot partition; CW `ThrottledRequests` | Better key design; on-demand; raise WCU/RCU |
| Scan is slow / expensive | Full table read | Add GSI / fix access pattern |
| Terraform `ConditionalCheckFailed` lock | Lock item stuck | `force-unlock` only if sure; see [[Terraform setup]] |
| Stream lag / duplicate processing | Shard iterator; Lambda concurrency | Idempotent handlers; DLQ |
| `ValidationException` key | Wrong types / missing key | Match AttributeDefinitions |
| Bill spike | On-demand heavy Scan; many GSIs; PITR | Kill Scans; drop unused indexes |

## Gotchas

> [!WARNING]
> **Hot partition** — monotonically increasing keys (timestamp alone) funnel writes to one shard.

> [!WARNING]
> **Scan for “just this once”** becomes a prod habit and a bill.

> [!WARNING]
> **Transactions** limited item count and require careful conflict handling — not a free ACID RDBMS.

> [!WARNING]
> **Strongly consistent read** does not work on GSI; only base table.

## When NOT to use

- **Complex joins / ad-hoc analytics** — RDS / warehouse.
- **Large objects** — store blob in [[AWS S3]], metadata in DynamoDB.
- **Multi-item relational integrity as primary model** — Postgres/RDS.

## Related

[[IAM]] · [[ARN (Amazon Resource Name)]] · [[AWS Lambda]] · [[AWS S3]] · [[Terraform setup]] · [[AWS Billing and cost management]] · [[AWS]]
