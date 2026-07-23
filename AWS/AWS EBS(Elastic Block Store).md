[[AWS/AWS EC2]] [[Operating System/Take snapshot]] [[Linux/Memory management]]

# AWS EBS (Elastic Block Store)

> Network-attached block volumes for EC2 — persistent disk, snapshots, resize, and **Delete on Termination** gotcha.

## Mental model

EBS volumes are AZ-scoped block devices attached to EC2 as `/dev/xvdf` etc. OS sees raw disk — format, mount, persist data independent of instance lifecycle **unless** volume is deleted on instance terminate. Snapshots → S3-backed incremental backups → new volume in any AZ (copy region for DR).

```
EC2 instance ← attach → EBS volume (gp3/io2)
                ↓ snapshot
              AMI / DR / clone
```

## Standard config / commands

### Create and attach (CLI sketch)

```bash
aws ec2 create-volume --availability-zone us-east-1a --size 100 --volume-type gp3
aws ec2 attach-volume --volume-id vol-xxx --instance-id i-xxx --device /dev/sdf
# inside instance: mkfs, mount, /etc/fstab by UUID
```

### Snapshot

```bash
aws ec2 create-snapshot --volume-id vol-xxx --description "pre-migration"
aws ec2 create-volume --snapshot-id snap-xxx --availability-zone us-east-1b
```

### Resize (gp3/gp2, online grow)

```bash
# AWS console or modify-volume → then grow partition + filesystem inside OS
sudo growpart /dev/nvme0n1 1
sudo resize2fs /dev/nvme0n1p1   # ext4
```

### Delete on termination

- Launch template / instance **Block device mapping** → **Delete on termination**
- **Uncheck** for data volumes you must keep when replacing instance

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Data gone after terminate | Delete on termination = true | Restore from snapshot; fix mapping before next terminate |
| Volume won't attach | AZ mismatch | Volume and instance same AZ (or detach/move) |
| Full disk | `df -h` | Extend volume + filesystem; don't just restart |
| Poor IOPS | CloudWatch `VolumeQueueLength` | gp3 provisioned IOPS; io2 for sustained |
| Snapshot slow first time | Normal | Incremental snapshots faster after |
| Corrupt FS after crash | fsck | Restore snapshot; enable fsync app-side |

## Gotchas

> [!WARNING]
> **Root volume default delete on terminate** — usually desired; data volume must opt out explicitly.
>
> **EBS ≠ backup strategy** — snapshots need lifecycle; test restore.
>
> **Encryption** — enable default EBS encryption per account/region for compliance.

## When NOT to use

- Don't use EBS for shared POSIX across many EC2 — use EFS or S3.
- Don't attach same volume to two instances simultaneously (except cluster FS products).

## Related

[[AWS/AWS EC2]] [[Operating System/fsync]] [[AWS/AWS Billing and cost management]]
