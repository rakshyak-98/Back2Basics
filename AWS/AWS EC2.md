[[AWS Networking]] [[Security group]] [[AMI (Amazon Machine Image)]] [[EBS (Elastic Block Store)]] [[ARN (Amazon Resource Name)]]

# AWS EC2

> **Virtual machines in a VPC** — pick AMI, instance type, subnet/SG, and know what still bills after `terminate`. **AWS EC2 User Guide** + finance surprises from orphaned EIPs/NAT.

## Mental model

An EC2 instance is compute on shared hardware (or Dedicated Host) with **ENI(s)** in a subnet. Launch = AMI + instance type + key pair/instance profile + [[Security group]]. Storage = root + optional [[EBS (Elastic Block Store)]] volumes. **Terminate ≠ delete all billable artifacts.**

```
Launch template ──► AMI + type + subnet + SG + user-data
                         │
                         ├── instance profile (IAM role → STS creds)
                         └── EBS volumes (persist after terminate unless delete_on_termination)
```

Every instance needs a **VPC** (default or custom) — networking is not optional ([[AWS Networking]]).

## Standard config / commands

### Launch checklist (prod)

| Setting | Typical choice | Why |
|---------|----------------|-----|
| Subnet | Private app tier | No direct internet exposure |
| Public IP | Off (use ALB) | Smaller attack surface |
| SG | Tier-specific (`app-sg`) | Not `default` |
| IAM | Instance profile with least privilege | No keys on disk |
| IMDS | v2 required, hop limit 1 (2 for containers) | SSRF credential theft mitigation |
| EBS | `gp3`, encrypted, `delete_on_termination` tuned | Cost + compliance |
| User-data | cloud-init bootstrap | Idempotent; log to `/var/log/cloud-init-output.log` |

```bash
aws ec2 describe-instances --filters "Name=tag:Env,Values=prod" \
  --query 'Reservations[].Instances[].{Id:InstanceId,State:State.Name,Type:InstanceType,Subnet:SubnetId}'

aws ec2 terminate-instances --instance-ids i-xxx
# THEN verify orphans:
aws ec2 describe-volumes --filters "Name=status,Values=available"
aws ec2 describe-addresses --query 'Addresses[?AssociationId==null]'
```

### AZ awareness

- Check **subnet AZ** matches resilience plan — `describe-instances` → `Placement.AvailabilityZone`.
- Multi-AZ ASG: one subnet per AZ in LT/ASG.

### Budget / billing visibility

- IAM: allow billing console for finance role (not every developer).
- **AWS Budgets** + Cost Anomaly Detection on EC2/NAT/EIP line items.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Instance unreachable (SSH/app) | SG, NACL, route, public IP/subnet | Full path debug ([[AWS Networking]], [[Security group]]) |
| Status checks failed | System vs instance check in console | Reboot; migrate if hardware; fix disk full (instance check) |
| Out of CPU credits (T-family) | CloudWatch `CPUCreditBalance` | Unlimited mode or resize to M/C family |
| User-data didn't run | `/var/log/cloud-init-output.log`; MIME multipart | Fix script; re-run with `cloud-init clean` |
| IAM role calls fail on instance | Profile attached? IMDS reachable? | Attach profile; curl IMDSv2 token flow |
| Bill after terminate | EBS volumes, EIP, NAT GW, snapshots | Delete orphans (see WARNING below) |
| Wrong region/AZ capacity | `InsufficientInstanceCapacity` | Retry another AZ/type; use capacity reservations |

## Gotchas

> [!WARNING]
> **Terminate EC2, then manually delete EBS volumes, Elastic IPs, and NAT gateways** — terminate stops compute; **EBS/EIP/NAT keep charging** if left behind.

> [!WARNING]
> **Don't attach EIP + NAT casually** — each EIP costs when unassociated; NAT GW hourly + per-GB.

> [!WARNING]
> **Default VPC placement** — fine for sandbox; prod needs explicit subnet tiering.

> [!WARNING]
> **Stopping vs terminating** — stop preserves EBS; terminate (with default delete_on_termination) removes root volume per setting.

## When NOT to use

- **Long-running stateless web at scale without ASG** — use Auto Scaling Group + ALB.
- **Batch/analytics** — consider Fargate, Lambda, or Spot Fleet for cost.
- **Bare metal driver/hardware timing needs** — consider Dedicated Hosts or on-prem.

## Related

[[AWS Networking]] · [[Security group]] · [[AMI (Amazon Machine Image)]] · [[EBS (Elastic Block Store)]] · [[aws STS (Security Token Service)]]
