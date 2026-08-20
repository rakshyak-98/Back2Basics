[[AWS]] [[AWS EC2]] [[EBS (Elastic Block Store)]] [[ARN (Amazon Resource Name)]] [[KMS]]

# AMI (Amazon Machine Image)

> **Launch template for EC2** — OS + root volume snapshot (+ optional extra volumes) baked into a regional image. Pick the wrong AMI (arch / virtualization / permissions) and launch fails or boots unusable.

## Mental model

An AMI is a **region-scoped blueprint**: kernel/boot config + **EBS snapshots** (root and optional data) + block device mapping + architecture (`x86_64` / `arm64`). Launch = copy snapshots into volumes in the target AZ, attach, boot. Marketplace AMIs add license/product codes.

```
Bake EC2 → create-image → AMI (snap-xxx …)
                              │
                              ├── launch in same region
                              └── copy-image → other region (DR)
```

| Source | Notes |
|--------|-------|
| AWS / partner public | Amazon Linux, Ubuntu, Windows |
| Marketplace | Paid / BYOL software stacks |
| Private / shared | Your account or `launchPermission` to another account |

## Standard config / commands

### Find and launch

```bash
aws ec2 describe-images --owners amazon \
  --filters "Name=name,Values=al2023-ami-*-x86_64" "Name=state,Values=available" \
  --query 'sort_by(Images,&CreationDate)[-1].[ImageId,Name,Architecture]'

aws ec2 run-instances --image-id ami-xxx --instance-type t3.medium \
  --subnet-id subnet-xxx --security-group-ids sg-xxx
```

### Bake from running instance

```bash
aws ec2 create-image --instance-id i-xxx --name "app-$(date +%Y%m%d)" --no-reboot
# Prefer --reboot for consistent filesystem unless you quiesce I/O yourself
```

### Copy for DR / multi-region

```bash
aws ec2 copy-image --source-region us-east-1 --source-image-id ami-xxx \
  --name "app-dr" --encrypted --kms-key-id alias/ami-copy
```

### Share with another account

```bash
aws ec2 modify-image-attribute --image-id ami-xxx \
  --launch-permission "Add=[{UserId=123456789012}]"
# Encrypted AMIs also need KMS key grants to the consumer account
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `InvalidAMIID.NotFound` | Wrong region | Use AMI id from **this** region |
| Instance won't start / wrong arch | AMI `Architecture` vs instance type | Match arm64↔Graviton, x86↔Intel/AMD |
| Shared AMI invisible | Launch permission; encrypted + KMS | Share AMI + grant KMS |
| Boot fails after bake | Cloud-init / fstab UUID; no-reboot inconsistency | Bake with reboot; fix fstab by UUID |
| Marketplace launch denied | Subscription / product code | Accept Marketplace terms |
| Copy stuck / AccessDenied | Snapshot encryption KMS | Key policy for `ec2` + dest account |

## Gotchas

> [!WARNING]
> **AMIs are regional** — ids do not travel; always `copy-image` for DR.

> [!WARNING]
> **`--no-reboot` bake** can capture inconsistent filesystem state for busy disks.

> [!WARNING]
> **Public AMI hygiene** — never bake secrets into AMI (keys in `/home`, `.env`, agent tokens). Use instance profiles + Secrets Manager at boot.

> [!WARNING]
> **Deprecate old AMIs** — `deprecate-image` / deregister + delete snapshots to stop storage bills.

## When NOT to use

- **Mutable snowflake VMs** — prefer immutable AMIs / launch templates + ASG instance refresh.
- **Container-only workloads** — ECR + ECS/EKS/Lambda images, not AMIs.
- **Cross-account golden images without KMS plan** — encrypted share is the hard part.

## Related

[[AWS EC2]] · [[EBS (Elastic Block Store)]] · [[AWS Auto Scaling]] · [[KMS]] · [[AWS]] · [[Advanced RISC Machine (ARM)]]
