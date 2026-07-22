[[AWS/AWS EC2]] [[AWS/IAM]] [[AWS/ARN (Amazon Resource Name)]]

# AWS Billing and Cost Management

> Where money leaks show up — Free Tier tracking, Cost Explorer, bills by service, and alarms before finance pings you.

## Mental model

AWS bills per account (consolidated billing in Organizations). **Cost Explorer** aggregates usage; **Bills** shows line items by service (EC2, S3, data transfer). Free Tier is per-service limits, not one global bucket. Untagged resources make chargeback impossible.

```
Usage (API calls, hours, GB) → CUR/Billing → Cost Explorer → Budgets/Alerts
```

## Standard config / commands

### Console paths

1. **Billing and Cost Management** → **Bills** → filter by month → **Charges by service**
2. **Free Tier** (left menu) → usage vs limit per service
3. **Cost Explorer** → daily/monthly by service, linked account, tag
4. **Budgets** → email at 80%/100% forecast

### CLI (Cost Explorer)

```bash
aws ce get-cost-and-usage \
  --time-period Start=2026-01-01,End=2026-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

### Cost hygiene checklist

| Action | Why |
|--------|-----|
| Tag `Environment`, `Owner` | Allocate spend |
| Delete unused EBS/NAT/EIP | Silent bleeders |
| S3 lifecycle + Intelligent-Tiering | Storage creep |
| Reserved/Savings Plans (steady load) | EC2/RDS discount |
| Enable **Cost Anomaly Detection** | Spike alerts |

Free Tier reference: [AWS Free Tier](https://aws.amazon.com/free/)

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected EC2 charge | Running instances all regions | `ec2 describe-instances --region us-east-1` (repeat regions) |
| Data transfer spike | Cost Explorer DT line | CloudFront for egress; same-AZ traffic |
| NAT Gateway $$$ | Hours + GB processed | VPC endpoints; reduce cross-AZ NAT hairpin |
| S3 pennies → dollars | Storage class, versions | Lifecycle delete old versions |
| Free Tier exceeded | Free Tier dashboard | Service actually "Always Free" vs 12-month |
| Multiple accounts surprise | Organizations | Consolidated bill; SCP limits |

## Gotchas

> [!WARNING]
> **Stopped EC2 still pays for EBS** — terminate or snapshot+delete volume.
>
> **Elastic IP unattached** — charged when not associated.
>
> **Regional resources** — bill shock often from wrong region left running.

## When NOT to use

- Don't optimize pennies before measuring — enable Cost Explorer tags first month.
- Don't buy 3-year RIs on spiky/dev workloads — use On-Demand + autoscaling first.

## Related

[[AWS/AWS EC2]] [[AWS/AWS EBS(Elastic Block Store)]] [[AWS/IAM]]
