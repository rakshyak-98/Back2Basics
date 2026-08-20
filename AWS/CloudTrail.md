[[AWS]] [[IAM]] [[CloudWatch]] [[AWS S3]] [[ARN (Amazon Resource Name)]]

# CloudTrail

> Account **API audit trail** — who called what, from where, succeeded or denied. Not application logs ([[CloudWatch]]); not a metrics system. Org trails and data events are the scale/cost knobs.

## Mental model

CloudTrail records **management events** (control plane: `Create*`, `Delete*`, `AssumeRole`, …) by default. **Data events** (S3 object-level, Lambda invoke) are opt-in and expensive at volume. Trails deliver to **S3** (and optionally CloudWatch Logs / EventBridge).

```
AWS API call ──► CloudTrail ──► S3 (encrypted) + optional CW Logs
                     │
                     └── EventBridge rule ──► alert on root / console login without MFA
```

| Event class | Examples | Default |
|-------------|----------|---------|
| Management | IAM, EC2 run-instances, STS AssumeRole | On |
| Data | S3 GetObject, Lambda Invoke | Off (enable selectively) |
| Insight | Unusual API rate patterns | Optional |

## Standard config / commands

### Org / multi-account

- One **organization trail** in the management account → member events land in a central bucket.
- Bucket policy + SCP: prevent members from disabling logging.

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=ConsoleLogin \
  --max-results 20

aws cloudtrail get-trail-status --name org-trail
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=Username,AttributeValue=Alice
```

### Hardening checklist

| Control | Why |
|---------|-----|
| Multi-region trail | Catch us-east-1 and “wrong region” activity |
| Log file validation | Detect tampering |
| SSE-KMS on S3 | Encrypt trail bucket |
| Separate security account bucket | Blast radius |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Event missing | Region; data vs management; delay (~minutes) | Right region; enable data events if needed; wait |
| `AccessDenied` in trail but app works | Different principal / session | Match assumed-role session ARN |
| Trail not delivering | S3 bucket policy; KMS; SNS | Fix destination permissions |
| Huge S3 bill | Data events on busy bucket | Narrow selectors; Athena lifecycle |
| Lookup empty for IAM user | Used role/SSO session name | Search by `ResourceName` / event source |

## Gotchas

> [!WARNING]
> **CloudTrail is not real-time** — expect short delay; for near-real-time detections use EventBridge on trail or CloudWatch metric filters carefully.

> [!WARNING]
> **Data events on high-traffic S3** can dominate cost — sample by prefix.

> [!WARNING]
> **Assumed-role sessions** appear as role session names — correlate with `sharedEventID` / `sourceIPAddress`.

> [!WARNING]
> **Disabling trail is itself an event** — alert on `StopLogging` / `DeleteTrail`.

## When NOT to use

- **App debug logs / stack traces** — [[CloudWatch]] Logs.
- **Packet-level forensics** — VPC Flow Logs / Traffic Mirroring.
- **Replacing IAM Access Analyzer / Config** — complementary, not identical.

## Related

[[IAM]] · [[aws STS (Security Token Service)]] · [[CloudWatch]] · [[AWS S3]] · [[ARN (Amazon Resource Name)]] · [[AWS]]
