[[AWS]] [[AWS Lambda]] [[IAM]] [[ARN (Amazon Resource Name)]] [[CloudWatch]]

# AWS SQS

> Managed queue — **at-least-once** delivery, visibility timeout, DLQ. The standard antidote to synchronous fan-out and Lambda retry storms. Pair with SNS for pub/sub fan-out (SNS → SQS), not as a separate leaf here.

## Mental model

Producer **SendMessage**; consumer **ReceiveMessage** → process → **DeleteMessage**. While in flight, message is **invisible** for `VisibilityTimeout`. Fail to delete → becomes visible again (retry). After `maxReceiveCount`, message goes to **DLQ**.

```
Producer ──► SQS queue ──► consumer (Lambda / worker)
                  │              │
                  └── DLQ ◄──────┘ after N receives
```

| Queue type | Semantics |
|------------|-----------|
| **Standard** | Best-effort ordering; at-least-once; nearly unlimited TPS |
| **FIFO** | Exactly-once *processing* within dedup window; order per message group; lower TPS |

## Standard config / commands

### Create + DLQ

```bash
aws sqs create-queue --queue-name app-jobs-dlq
# note QueueUrl / Arn

aws sqs create-queue --queue-name app-jobs \
  --attributes '{
    "VisibilityTimeout":"60",
    "MessageRetentionPeriod":"345600",
    "RedrivePolicy":"{\"deadLetterTargetArn\":\"ARN_DLQ\",\"maxReceiveCount\":\"3\"}"
  }'
```

### Lambda event source

- Batch size + **ReportBatchItemFailures** for partial success
- Visibility timeout ≥ **Lambda timeout** (rule of thumb: visibility ≥ 6× function timeout for retries)

```bash
aws sqs get-queue-attributes --queue-url "$URL" --attribute-names All
aws sqs receive-message --queue-url "$URL" --max-number-of-messages 1 --wait-time-seconds 20
```

### SNS fan-out (pattern)

SNS topic → multiple SQS subscriptions (filter policies) → independent consumers. IAM: SNS publish + SQS policy allow SNS principal.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Messages reappear / duplicates | Visibility too short; no delete; crash mid-handler | Raise visibility; idempotent consumer; delete after success |
| DLQ filling | Poison messages; schema change | Fix consumer; replay after fix; alarm on DLQ depth |
| Lambda timeout + SQS retry storm | Timeout vs visibility; batch | Align timeouts; partial batch failure; concurrency reserve |
| FIFO stuck behind one group | Long processing on one `MessageGroupId` | Split groups; parallel groups |
| `AccessDenied` send/receive | Queue policy + IAM | Grant producer/consumer ARNs |
| In-flight max | Many invisibles | Scale consumers; find hung workers |

## Gotchas

> [!WARNING]
> **At-least-once** — design for duplicates (idempotency keys).

> [!WARNING]
> **VisibilityTimeout < consumer time** → duplicate parallel processing of same message.

> [!WARNING]
> **Long polling** (`WaitTimeSeconds=20`) cuts empty receives and cost — use it.

> [!WARNING]
> **Large payloads** — SQS max 256 KB; use S3 pointer pattern for bigger bodies.

## When NOT to use

- **Request/response RPC with low latency** — sync API or Step Functions Express carefully.
- **Strict global ordering of all messages** — FIFO only per group; else Kafka/Kinesis.
- **Pub/sub to many heterogeneous subscribers without queues** — SNS alone (lossy if subscriber down) — prefer SNS→SQS.

## Related

[[AWS Lambda]] · [[IAM]] · [[ARN (Amazon Resource Name)]] · [[CloudWatch]] · [[AWS S3]] · [[AWS]]
