[[AWS]] [[AWS EC2]] [[AWS Billing and cost management]] [[fsync]] [[Take snapshot]]

# EBS (Elastic Block Store)

> Network-attached **block volumes** for EC2 — persistent disk, snapshots, resize, and the **Delete on Termination** gotcha. **AWS EC2 User Guide (EBS)** + orphaned-volume bill stories.

## Mental model

EBS volumes are **AZ-scoped** block devices attached to EC2 (`/dev/xvdf`, NVMe names on Nitro). The OS sees raw disk — format, mount, persist data **independent of instance lifecycle** unless the volume is deleted on terminate. Snapshots are **incremental**, S3-backed (not browsable as objects), and can create new volumes in any AZ (copy region for DR).

```
EC2 instance ← attach → EBS volume (gp3 / io2 / …)
                │
                └── snapshot → AMI / clone / DR volume
```

| Type | When |
|------|------|
| **gp3** | Default prod — set IOPS/throughput independently of size |
| **io2** | Sustained high IOPS databases |
| **st1 / sc1** | Throughput / cold HDD (rare for apps) |
| **Instance store** | Ephemeral local NVMe — not EBS; dies with instance |

## Standard config / commands

### Create and attach

```bash
aws ec2 create-volume \
  --availability-zone us-east-1a \
  --size 100 \
  --volume-type gp3 \
  --iops 3000 \
  --throughput 125 \
  --encrypted \
  --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=app-data}]'

aws ec2 attach-volume --volume-id vol-xxx --instance-id i-xxx --device /dev/sdf
# Inside instance: mkfs, mount, /etc/fstab by UUID (not device name)
```

### Snapshot + restore

```bash
aws ec2 create-snapshot --volume-id vol-xxx --description "pre-migration"
aws ec2 create-volume --snapshot-id snap-xxx --availability-zone us-east-1b --volume-type gp3
```

**Lifecycle / automation:** use **AWS Backup** or **Data Lifecycle Manager (DLM)** policies for schedule + retention — do not rely on ad-hoc snapshots. Recycle Bin can retain accidentally deleted snapshots/volumes for a recovery window.

```bash
# Archive old snapshots (cheaper cold tier) via console Storage tier or ModifySnapshotTier
aws ec2 describe-snapshots --owner-ids self --query 'Snapshots[?StartTime<=`2025-01-01`].[SnapshotId,VolumeSize,StorageTier]'
```

### Resize (online grow)

```bash
aws ec2 modify-volume --volume-id vol-xxx --size 200
# Then inside OS:
sudo growpart /dev/nvme0n1 1
sudo resize2fs /dev/nvme0n1p1   # ext4
# xfs: xfs_growfs /mountpoint
```

### Delete on termination

- Launch template / **Block device mapping** → **Delete on termination**
- **Uncheck** for data volumes you must keep when replacing the instance
- Root volume usually delete-on-terminate = true; data volumes often false

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Data gone after terminate | Delete on termination = true | Restore from snapshot; fix mapping before next terminate |
| Volume won't attach | AZ mismatch | Volume and instance **same AZ** |
| Full disk | `df -h`; CloudWatch `VolumeQueueLength` | Extend volume + filesystem; don't just reboot |
| Poor IOPS | CW `VolumeReadOps` / queue length | Raise gp3 IOPS/throughput; io2 for sustained |
| First snapshot slow | Full copy of used blocks | Normal; later snaps are incremental |
| Corrupt FS after crash | fsck; app fsync behavior | Restore snapshot; fix write barriers ([[fsync]]) |
| Encrypted volume copy fails | KMS key policy / region | Grant `kms:CreateGrant` for EC2; copy key or re-encrypt |

## Gotchas

> [!WARNING]
> **Root volume default delete on terminate** — usually desired; **data volumes must opt out** explicitly or you lose them on replace.

> [!WARNING]
> **EBS ≠ backup strategy** — snapshots need lifecycle (DLM / AWS Backup) and **tested restores**.

> [!WARNING]
> **Encryption** — enable **default EBS encryption** per account/region; encrypted snapshots need KMS access to share/copy.

> [!WARNING]
> **Snapshots live in S3 but are not S3 objects** — you cannot `aws s3 ls` them; only create volumes / AMIs / copy.

> [!WARNING]
> **Terminate EC2 does not delete unattached volumes** left with delete-on-termination false — they keep billing ([[AWS Billing and cost management]]).

## When NOT to use

- **Shared POSIX across many EC2** — use [[AWS EFS (Elastic File System)]] or [[AWS S3]], not multi-attach EBS (except specialized io2 Multi-Attach + cluster FS).
- **Object / CDN assets** — S3 + CloudFront, not a mounted volume.
- **Ephemeral scratch that can die with the instance** — instance store may be cheaper/faster.

## Related

[[AWS EC2]] · [[AMI (Amazon Machine Image)]] · [[AWS Billing and cost management]] · [[AWS EFS (Elastic File System)]] · [[fsync]] · [[Take snapshot]] · [[KMS (Key Management Service)]] · [[AWS]]
