[[AWS EC2]] [[EBS (Elastic Block Store)]] [[AWS Networking]] [[Security group]]

# AMI (Amazon Machine Image)

> An AMI is the template for an EC2 instance — it captures the root volume snapshot, launch permissions, and block device mapping so you can launch identical machines repeatedly.

```txt
        AMI (Amazon Machin ──┬── Why it matters
               ├── Sources
               └── Mechanism
```

## Why It Matters
- **Key signal:** AMI questions check golden-image pipelines, region copy, and baking vs bootst…

## Sources
- [Amazon Machine Images](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) — overview
- [Creating an Amazon EBS-backed Linux AMI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-ebs.html) — overview

## Technical Details
### What an AMI contains

- **Root volume snapshot:** (usually EBS-backed) or instance-store template
- **Virtualization type:** — HVM (standard today) or paravirtual (legacy)
- **Architecture:** — x86_64 or arm64 (Graviton)
- **Launch permissions:** — public, explicit accounts, or private
- **Block device mapping:** — which volumes attach at boot and their sizes

- AMIs are regional.
- Copy an AMI to another region before launching there.

### AMI sources

| Source | When to use |
|--------|-------------|
| AWS marketplace / quick start | Baseline OS images |
| Your golden AMI | Hardened, pre-baked agents, compliance baseline |
| `CreateImage` from running instance | Capture configured server (mind drift and secrets) |
| EC2 Image Builder | Pipelines for reproducible images |

### Create from instance

```bash
aws ec2 create-image \
  --instance-id i-0abc123 \
  --name "web-tier-2026-08-13" \
  --no-reboot
```

- `--no-reboot` avoids restart but risks filesystem inconsistency

### Launch from AMI

- Console or:

```bash
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.small \
  --key-name my-key \
  --security-group-ids sg-0abc123 \
  --subnet-id subnet-0abc123
```

### Lifecycle hygiene

- **Version:** AMIs with dates or build numbers; deregister old ones.
- **Scan:** for CVEs before promotion; do not bake secrets into images
- **Encrypt:** EBS snapshots backing the AMI with KMS keys you control.
