[[Route53]] [[Security group]] [[AWS EC2]] [[NAT (Network Address Translation)]] [[DNS]]

# AWS Networking

> VPC + subnets + routing + SG/NACL — the **network shell** every AWS service lives in. **AWS Well-Architected (Reliability/Security)** + on-call VPC debug muscle memory.

## Mental model

AWS networking is **regional isolation inside a VPC**: you own private IP space, carve **subnets** per AZ, attach **route tables** (where traffic goes), and gate traffic with **Security Groups** (stateful, instance-level) and **NACLs** (stateless, subnet-level). Public subnets reach the internet via **Internet Gateway (IGW)**; private subnets reach out via **NAT Gateway/GW** or **VPC endpoints** (stay on AWS backbone, no public IP).

```
Internet ──► IGW ──► public subnet (ALB, bastion)
                      │
                      └── NAT GW ──► private subnet (app, RDS)
```

Default VPC works for labs; production uses explicit CIDR planning, separate public/private/database tiers, and **no** surprise default-SG wide open rules.

## Standard config / commands

### VPC layout (typical prod)

| Tier | Subnet | Route | Attach |
|------|--------|-------|--------|
| Public | `10.0.1.0/24` (AZ-a), `10.0.2.0/24` (AZ-b) | `0.0.0.0/0` → IGW | ALB, NAT GW |
| Private app | `10.0.10.0/24`, `10.0.11.0/24` | `0.0.0.0/0` → NAT GW | EC2, ECS, Lambda (VPC) |
| Private data | `10.0.20.0/24`, `10.0.21.0/24` | local only | RDS, ElastiCache |

- **CIDR**: `/16` VPC, `/24` subnets — leave headroom; overlapping CIDR blocks **cannot** be peered later.
- **Multi-AZ**: always span ≥2 AZs for anything that matters; single-AZ NAT is a known SPOF (accept cost or run NAT per AZ).
- **DNS**: enable `enableDnsHostnames` + `enableDnsSupport` on VPC (required for private hosted zones and many managed services).

### CLI sanity checks

```bash
# What VPC/subnet/SG is this instance in?
aws ec2 describe-instances --instance-ids i-xxx \
  --query 'Reservations[].Instances[].{VpcId:VpcId,SubnetId:SubnetId,SGs:SecurityGroups}'

# Route table for a subnet (wrong route = black hole)
aws ec2 describe-route-tables --filters "Name=association.subnet-id,Values=subnet-xxx"

# Reachability Analyzer (when ping/traceroute lie)
aws ec2 create-network-insights-path --source i-xxx --destination i-yyy --protocol tcp --destination-port 443
```

### VPC endpoints (prefer over NAT for AWS APIs)

- **Gateway** (S3, DynamoDB): route table entry, no hourly charge.
- **Interface** (most APIs): ENI in subnet; use for ECR, Secrets Manager, STS — cuts NAT data-processing cost and keeps traffic private.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| EC2 has no public IP but "should" | Subnet auto-assign public IP; IGW attached to VPC | Enable auto-assign or attach EIP; verify public subnet route to IGW |
| Private instance can't reach internet | NAT GW in public subnet? Route `0.0.0.0/0` → NAT on **private** RT? | Fix route table association; NAT GW must sit in public subnet with IGW route |
| Works instance-to-instance in same SG, fails cross-SG | [[Security group]] inbound/outbound rules | Add SG-to-SG rule (reference SG id, not CIDR) on **both** sides if needed |
| RDS/Redis "connection timed out" from app | App in private subnet? SG allows app SG on DB port? NACL 1024-65535 return? | Open SG; verify NACL ephemeral return (NACL is stateless) |
| DNS resolves wrong / not at all | VPC DNS settings; Route53 resolver rules; hybrid DNS | Enable DNS on VPC; check PHZ association; forwarders for on-prem |
| Peering/Transit Gateway "partial" connectivity | Route tables on **both** sides; SG still independent | Add routes both directions; SG rules don't inherit from peering |
| NAT GW bill spike | CloudWatch `BytesOutToDestination`; which AZ/subnet? | VPC endpoints for S3/ECR; fix hairpin traffic; review scrapers |

## Gotchas

> [!WARNING]
> **Security Groups are stateful; NACLs are stateless.** SG "allow 443 in" implies return traffic. NACL needs explicit ephemeral port range outbound **and** inbound for return packets — classic "SG looks fine, still broken" cause.

> [!WARNING]
> **Default VPC SG often allows all outbound and may have legacy inbound.** Never rely on default SG for prod; create named SGs per tier.

> [!WARNING]
> **Deleting IGW while instances have public IPs** — blackholes egress. **Deleting NAT GW** — entire private subnet loses outbound (often silent until deploy/ apt fails).

> [!WARNING]
> **Cross-region ≠ cross-VPC.** Peering/TGW is same-region or inter-region with separate routing; SG rules don't cross VPC boundaries.

## When NOT to use

- **Default VPC for production** — no blast-radius separation, CIDR collisions when peering.
- **Public IPs on app/database tiers** — use ALB + private subnets; bastion or SSM Session Manager for admin.
- **NACL micromanagement** — start with SG-only; add NACLs for explicit deny (compliance) or subnet-level guardrails.
- **One NAT GW for multi-AZ prod HA** — AZ failure kills all private egress.

## Related

[[Route53]] · [[Security group]] · [[AWS EC2]] · [[NAT (Network Address Translation)]] · [[DNS]] · [[How to connect Godaddy domain with AWS EC2 instance]]
