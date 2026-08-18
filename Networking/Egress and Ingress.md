[[Networking]] [[outbound ip]] [[NAT (Network Address Translation)]] [[network gateway]]

# Egress and Ingress

> Ingress is traffic in; egress is traffic out — cloud bills and firewalls care most about egress.

## Mental model

**Say it in one breath:** From the VPC’s view — ingress enters from the internet (or peers); egress leaves toward the internet (or other networks).

```txt
Internet ── ingress ──► VPC / host
Internet ◄── egress ─── VPC / host
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Ingress** | Traffic coming in | “SG/NACL allow inbound on 443.” |
| --- | --- | --- |
| **Egress** | Traffic going out | “NAT Gateway + data-transfer cost.” |
| **Data transfer OUT** | Bytes leaving the cloud boundary | “Usually the bill line that hurts.” |
| **Same-region / same-AZ** | Stay local | “S3/CloudWatch in-region often avoids egress fees.” |

### Who usually pays (cloud mental table)

| Direction | Name | Example | Typical cost |

| Internet → INTO VPC | Ingress | User loads your site | Often free (or cheap) |
| --- | --- | --- | --- |
| OUT OF VPC → internet | **Egress** | EC2 pulls packages, sends logs | Metered — watch this |
| Cross-region copy | Egress-like | Replicate to another region | Almost always paid |

> [!INFO]
> Same region for S3, CloudWatch, SSM; cache packages inside the VPC; shorten log retention — cut egress before buying more bandwidth.

## Standard config / commands

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

| Security group egress | Default “all out” is easy; lock down for least privilege |
| --- | --- |
| NAT Gateway | Shared egress IP + hourly + per-GB cost |
| VPC endpoints | Private path to S3/API — less public egress |
| Log retention | Infinite retention ⇒ endless storage *and* transfer patterns |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Spike in bill | CE data-transfer by service | Move traffic same-region; add VPC endpoints; CDN |
| Outbound API fails | SG egress / NACL / route to NAT | Allow dest ports; fix default route `0.0.0.0/0` |
| Inbound works, callbacks fail | Egress blocked or wrong [[outbound ip]] | Open egress; whitelist new NAT IP at peer |
| Cross-AZ surprise cost | Architecture diagram | Collapse chatty tiers into one AZ or accept the fee |

## Gotchas

> [!WARNING]
> **Ingress free ≠ egress free** — serving 1 GB in often means ~1 GB out to the client (that egress can cost).

> [!WARNING]
> **“Allow all egress”** — convenient until malware phones home or you fail a compliance audit.

> [!WARNING]
> **NAT IP changes** — partners whitelisting your egress IP break when you rebuild the NAT Gateway.

## When NOT to use

- **Treating “ingress/egress” as only AWS terms** — same words apply to k8s NetworkPolicies, service meshes, and host firewalls.
- **Optimizing ingress while ignoring egress** — most surprise bills are outbound.
- **Blocking all egress without a plan** — package updates, DNS, and SaaS APIs will die.

## Related

[[Networking]] [[outbound ip]] [[NAT (Network Address Translation)]] [[network gateway]] [[CIDR (Classless Inter-Domain Routing)]]
