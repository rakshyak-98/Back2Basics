[[AWS]] [[AWS EC2]] [[AMI (Amazon Machine Image)]] [[ALB (Application Load Balancer)]] [[CloudWatch]] [[IAM]]

# AWS Auto Scaling

> **Auto Scaling Group (ASG)** keeps N healthy EC2 instances from a **launch template** — scale on CloudWatch metrics, replace unhealthy, instance refresh for AMI rollouts. Misaligned health checks cause terminate loops.

## Mental model

ASG desires `min / desired / max` capacity across **subnets (AZs)**. Launch template defines AMI, type, SG, IAM profile, user-data. Scaling policies adjust desired. **ELB health** vs **EC2 status checks** decide replace behavior.

```
Launch template ──► ASG (min/desired/max) ──► instances in AZs
                          │
                          ├── CloudWatch alarm ──► scale out/in
                          └── Target group health ──► replace
```

## Standard config / commands

### Launch template + ASG checklist

| Setting | Prod choice | Why |
|---------|-------------|-----|
| Launch template version | `$Latest` or pinned `$Number` | Pin for prod rollouts |
| Subnets | Private app, ≥2 AZ | HA |
| Target group | Attach ASG to ALB TG | ELB health |
| Health check type | **ELB** when behind ALB | Replace bad app, not just dead VM |
| Health check grace | 300s+ | Avoid kill during boot |
| IMDSv2 | required | SSRF mitigation |
| Instance refresh | Rolling with warmup | AMI deploy without downtime |

```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names app-prod
aws autoscaling set-desired-capacity --auto-scaling-group-name app-prod --desired-capacity 4
aws autoscaling start-instance-refresh --auto-scaling-group-name app-prod \
  --preferences MinHealthyPercentage=90,InstanceWarmup=300
```

### Scaling policy types

| Policy | Use |
|--------|-----|
| Target tracking (CPU / ALBRequestCountPerTarget) | Default |
| Step scaling | Custom breakpoints |
| Scheduled | Known diurnal load |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Scale-out but targets unhealthy | User-data; SG; app not listening | Fix LT; grace period |
| Terminate loop | ELB health failing; grace too short | Fix `/health`; raise grace |
| Won't scale in | Min size; scale-in protection | Lower min; clear protection |
| Uneven AZ capacity | Subnet/AZ imbalance | Balanced AZ; check LT network |
| Instance refresh stuck | Failed launches; capacity | Check `DescribeInstanceRefreshes`; capacity in AZ |
| Spiky flapping | Alarm cooldown / warmup | Longer cooldown; target tracking |

## Gotchas

> [!WARNING]
> **EC2 health only** ignores app 500s — use **ELB** health with ALB.

> [!WARNING]
> **Cooldown + warmup** — aggressive scale-in during deploy kills new instances.

> [!WARNING]
> **Spot + ASG** — need mixed instances / capacity rebalance or face sudden capacity loss.

> [!WARNING]
> **Changing LT doesn't replace running instances** — start instance refresh or terminate to recycle.

## When NOT to use

- **One snowflake VM** — plain EC2 until you need HA/scale.
- **Container orchestration** — ECS/EKS services scale tasks, not classic ASG (though EC2 capacity provider uses ASG under the hood).
- **Pure serverless event work** — Lambda concurrency.

## Related

[[AWS EC2]] · [[AMI (Amazon Machine Image)]] · [[ALB (Application Load Balancer)]] · [[CloudWatch]] · [[AWS ECS]] · [[IAM]] · [[AWS]]
