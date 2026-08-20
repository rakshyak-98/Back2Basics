[[AWS]] [[AWS Lambda]] [[AWS EC2]] [[CloudTrail]] [[AWS Billing and cost management]] [[KMS]]

# CloudWatch

> Metrics, logs, alarms, and dashboards for AWS resources — **not** a full SIEM by itself. Empty log groups and “forgot retention” are the usual on-call and bill surprises.

## Mental model

| Pillar | What | Unit |
|--------|------|------|
| **Metrics** | Time series (CPU, Latency, custom) | Namespace + dimensions |
| **Logs** | Log groups → streams → events | Ingestion + storage GB |
| **Alarms** | Threshold / anomaly on a metric | → SNS / Auto Scaling / etc. |
| **Dashboards** | Widgets over metrics/logs | Console / API |

```
Service / agent ──► PutMetricData / PutLogEvents
                         │
                         ├── Alarm ──► SNS / ASG
                         └── Logs Insights query
```

Lambda logs land in `/aws/lambda/<function>`. EC2 needs agent or custom metrics for memory/disk (CPU is free via hypervisor).

## Standard config / commands

### Tail Lambda / app logs

```bash
aws logs tail /aws/lambda/api-handler --follow
aws logs filter-log-events --log-group-name /aws/lambda/api-handler \
  --filter-pattern "ERROR" --start-time $(($(date +%s)*1000 - 3600000))
```

### Alarm on high error rate (sketch)

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name api-5xx \
  --metric-name HTTPCode_Target_5XX_Count \
  --namespace AWS/ApplicationELB \
  --statistic Sum --period 60 --evaluation-periods 3 --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=LoadBalancer,Value=app/prod/xxx \
  --alarm-actions arn:aws:sns:REGION:ACCOUNT:oncall
```

### Retention (set explicitly)

```bash
aws logs put-retention-policy --log-group-name /aws/lambda/api-handler --retention-in-days 14
```

### Logs Insights

```
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 50
```

### SSE-KMS on log groups

Needs key policy allowing `logs.<region>.amazonaws.com` ([[KMS]]).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No Lambda logs | Execution role has `AWSLambdaBasicExecutionRole`? | Attach basic logging policy |
| Wrong log group | Function name / version / alias | Tail correct `/aws/lambda/...` |
| Alarm flapping | Period vs evaluation; missing data | Treat missing as ignore/notBreaching; widen window |
| Metric empty | Wrong dimension names (case-sensitive) | Copy dimensions from console metric |
| Bill spike | Ingestion volume; never-expire groups | Retention; sample; filter noisy debug |
| Agent not shipping | CW agent config; IMDS; instance profile | Fix IAM `logs:PutLogEvents`; restart agent |

## Gotchas

> [!WARNING]
> **Default log retention is Never expire** — set retention on every group or pay forever.

> [!WARNING]
> **High-cardinality custom metrics** (unique user id as dimension) → cost explosion.

> [!WARNING]
> **CloudWatch ≠ CloudTrail** — CW is telemetry; API audit is [[CloudTrail]].

> [!WARNING]
> **Cross-account / org** — need observability account + OAM or curated sharing; don't assume one region sees all.

## When NOT to use

- **Long-term forensic audit of every API call** — CloudTrail (+ archive to S3).
- **Full APM distributed traces alone** — X-Ray / OpenTelemetry + CW as sink.
- **Sub-second streaming analytics** — Kinesis / OpenSearch pipelines.

## Related

[[AWS Lambda]] · [[AWS EC2]] · [[ALB (Application Load Balancer)]] · [[CloudTrail]] · [[AWS Billing and cost management]] · [[KMS]] · [[AWS]]
