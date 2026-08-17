[[Networking]] [[outbound ip]] [[NAT (Network Address Translation)]] [[network gateway]] [[CIDR (Classless Inter-Domain Routing)]]

# Egress and Ingress

> Ingress is traffic in; egress is traffic out — cloud bills and firewalls care most about egress.

```txt
        Egress and Ingress ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask ingress/egress to check cloud networking cost awareness and …

## Sources
- [Wikipedia — Egress and Ingress](https://en.wikipedia.org/wiki/Egress_and_Ingress) — overview

## Key Concepts
- **Ingress:** traffic coming into a VPC or host → security groups / NACLs allow inbound por…
- **Egress:** traffic leaving a VPC or host → often via [[NAT (Network Address Translation)…
- **Data transfer OUT:** bytes leaving the cloud boundary → the bill line that typically hurts.
- **Stay local when possible:** same-region / same-AZ paths → often avoid or reduce egress fees.

## Technical Details
```txt
Internet ── ingress ──► VPC / host
Internet ◄── egress ─── VPC / host
```

| Word | Plain meaning | Interview phrasing |
|------|---------------|-------------------|
| **Ingress** | Traffic coming in | Security group / NACL allow inbound on 443. |
| **Egress** | Traffic going out | NAT Gateway + data-transfer cost. |
| **Data transfer OUT** | Bytes leaving the cloud boundary | Usually the bill line that hurts. |
| **Same-region / same-AZ** | Stay local | S3/CloudWatch in-region often avoids egress fees. |

- Who usually pays (cloud mental table):

| Direction | Name | Example | Typical cost |
|-----------|------|---------|--------------|
| Internet → INTO VPC | Ingress | User loads your site | Often free (or cheap) |
| OUT OF VPC → internet | **Egress** | EC2 pulls packages, sends logs | Metered — watch this |
| Cross-region copy | Egress-like | Replicate to another region | Almost always paid |

- Same region for S3, CloudWatch, SSM; cache packages inside the VPC; shorten l…

```bash
# AWS: rough data-transfer spend this month
aws ce get-cost-and-usage \
  --time-period Start=$(date -u +"%Y-%m-01"),End=$(date -u +"%Y-%m-%d") \
  --granularity MONTHLY \
  --metrics "UnblendedCost" "UsageQuantity" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["Data Transfer"]}}'
```

| Knob | Why it matters |
|------|----------------|
| Security group egress | Default “all out” is easy; lock down for least privilege |
| NAT Gateway | Shared egress IP + hourly + per-GB cost |
| VPC endpoints | Private path to S3/API — less public egress |
| Log retention | Infinite retention ⇒ endless storage and transfer patterns |

| Symptom | Check | Fix |
|---------|-------|-----|
| Spike in bill | Cost Explorer data-transfer by service | Move traffic same-region; add VPC endpoints; CDN |
| Outbound API fails | Security group egress / NACL / route to NAT | Allow destination ports; fix default route `0.0.0.0/0` |
| Inbound works, callbacks fail | Egress blocked or wrong [[outbound ip]] | Open egress; whitelist new NAT IP at peer |
| Cross-AZ surprise cost | Architecture diagram | Collapse chatty tiers into one AZ or accept the fee |

## Mistakes to Avoid
- **Mistake:** Treating ingress free as "serving traffic is free"
- **Mistake:** Leaving "allow all egress" forever
- **Mistake:** Ignoring NAT IP changes
- **Mistake:** Optimizing inbound allow-lists while ignoring outbound cost and …
- **Mistake:** Blocking all egress without a plan for DNS, updates, and require…

## Pros/Cons or Trade-offs
- **Pro:** Clear directional language for firewalls and billing; locking egress improves least privilege and reduces surprise spend.
- **Con:** Over-restricting egress breaks package updates, DNS, and SaaS APIs; NAT Gateway convenience carries hourly and per-GB cost.

## Comparison
- vs host firewall only: ingress/egress apply equally to cloud security groups,…


### Use cases
- Cloud cost control, firewall policy, and partner IP allow-lists on your [[out…
