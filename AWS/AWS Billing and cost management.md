[[AWS EC2]] [[AWS Lambda]] [[AWS ECR]] [[IAM]]

# AWS Billing and cost management

> AWS bills per service, per second or per request — surprises usually come from data transfer, idle Elastic IPs, unattached EBS volumes, and resources left running in forgotten regions.

```txt
        AWS Billing and co ──┬── Why it matters
               ├── Sources
               └── Mechanism
```

## Why It Matters
- **Key signal:** Reviewers ask about AWS Billing and cost management to see whether you can…

## Sources
- [AWS Billing and Cost Management User Guide](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-what-is.html) — overview
- [AWS Pricing Calculator](https://calculator.aws/) — overview

## Technical Details
### How charges compose

| Category | Examples |
|----------|----------|
| **Compute** | EC2 hours, Lambda GB-seconds, Fargate vCPU/memory |
| **Storage** | EBS GB-months, S3 tiers, ECR image storage |
| **Networking** | Data transfer out to internet, NAT Gateway hourly + per-GB |
| **Requests** | S3 GET/PUT, API Gateway, Route 53 queries |
| **Licensing** | Marketplace AMIs, Windows/RHEL surcharges |

- **Free Tier:** applies to new accounts for 12 months on select services

### Cost control tools

| Tool | Purpose |
|------|---------|
| **Cost Explorer** | Trends, forecasts, filtering by tag/service |
| **Budgets** | Alerts at dollar or percent thresholds |
| **Cost Anomaly Detection** | ML-flagged unusual spend |
| **Billing alarms (CloudWatch)** | Legacy threshold on estimated charges |
| **Organizations + SCPs** | Consolidated billing, policy guardrails |

### Tagging strategy

- Enforce tags (`Environment`, `Team`, `CostCenter`) via [[IAM]] or Service Con…
- Untagged resources make chargeback impossible.

```bash
aws ce get-cost-and-usage \
  --time-period Start=2026-08-01,End=2026-08-13 \
  --granularity DAILY \
  --metrics BlendedCost \
  --group-by Type=TAG,Key=Environment
```

### Common waste

- Stopped EC2 still paying for attached [[EBS (Elastic Block Store)]]
- Unassociated [[Elastic IP]] addresses
- Old EBS snapshots and AMIs
- NAT Gateway processing large video egress — consider CloudFront
- Multi-AZ RDS when dev only needs single-AZ

### Savings instruments

- **Savings Plans / Reserved Instances:** — commit to steady compute usage
- **Spot Instances:** — interruptible batch work on [[AWS EC2]]
- **S3 Intelligent-Tiering / lifecycle rules:** — move cold data to Glacier
