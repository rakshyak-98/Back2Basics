[[AWS EC2]] [[AWS EFS (Elastic File System)]] [[AWS Billing and cost management]] [[AWS CLI]] [[Persistent Block Storage]]

# AWS EBS(Elastic Block Store)

> Amazon EBS provides network-attached block storage volumes for EC2 instances — persistent disks you attach, format, mount, snapshot, and resize independently of the instance lifecycle.

---

## Why It Matters

EBS is the default durable storage for EC2. Unlike instance store (ephemeral), EBS volumes survive instance stop/start and can be detached and reattached to another instance in the same Availability Zone. Choosing the wrong volume type (gp2 vs gp3), attaching across AZs, or forgetting to grow the filesystem after volume expansion are common production incidents. EBS snapshots underpin backup, AMI creation, and cross-region disaster recovery.

---

## Sources

- [Amazon EBS User Guide](https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html) — Volume types, IOPS/throughput models, encryption, and multi-attach features.
- [Amazon EBS — Volume types](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html) — gp3, io2, st1, sc1 characteristics and when to use each.
- [Amazon EBS — Snapshots](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-snapshots.html) — Incremental snapshot mechanics, lifecycle policies, and cross-region copy.
- [Amazon EBS — Encrypt volumes](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-encryption.html) — KMS integration and encryption-by-default account settings.

---

## Key Concepts

```txt
EC2 instance (AZ-a)
    │
    ├── /dev/nvme0n1  ← root volume (gp3)
    └── /dev/nvme1n1  ← data volume (io2) — must be same AZ as instance
```

| Concept | Detail |
|---------|--------|
| **AZ-bound** | Volume and instance must be in the same Availability Zone to attach. |
| **Block storage** | Raw block device — you partition, format (ext4/xfs), and mount. |
| **Snapshots** | Incremental backups to S3 — point-in-time, cross-region copyable. |
| **Encryption** | AES-256 via AWS KMS — encrypt at rest; minimal performance impact on Nitro. |
| **Nitro mapping** | Attach as `/dev/sdf` in API; appears as `/dev/nvme1n1` inside instance. |

### Volume types (2026 defaults)

| Type | Use case | IOPS | Throughput |
|------|----------|------|------------|
| **gp3** | General purpose (default) | 3,000–16,000 baseline | 125–1,000 MB/s |
| **io2** | Mission-critical databases | Up to 64,000 | Provisioning required |
| **st1** | Throughput-optimized HDD | Low | Cheap sequential reads |
| **sc1** | Cold HDD | Lowest | Infrequent access |

**gp3** replaced gp2 as default — provision IOPS and throughput independently without size coupling.

---

## Technical Details

### Create and attach (CLI)

```bash
aws ec2 create-volume \
  --availability-zone us-east-1a \
  --size 100 \
  --volume-type gp3 \
  --encrypted

aws ec2 attach-volume \
  --volume-id vol-0abc123 \
  --instance-id i-0def456 \
  --device /dev/sdf

# Inside instance — first time only
lsblk
sudo mkfs -t xfs /dev/nvme1n1
sudo mkdir /data
sudo mount /dev/nvme1n1 /data
echo '/dev/nvme1n1 /data xfs defaults,nofail 0 2' | sudo tee -a /etc/fstab
```

### Operations checklist

| Task | Command |
|------|---------|
| List volumes | `aws ec2 describe-volumes --filters Name=attachment.instance-id,Values=i-0def456` |
| Snapshot | `aws ec2 create-snapshot --volume-id vol-0abc123 --description "pre-migration"` |
| Detach safely | `umount /data` → `aws ec2 detach-volume --volume-id vol-0abc123` |
| Expand volume | `modify-volume --size 200` → grow partition → `xfs_growfs` or `resize2fs` |
| Delete | Detach first; snapshots persist until deleted separately |

### Expand workflow

```bash
aws ec2 modify-volume --volume-id vol-0abc123 --size 200
# Wait for "optimizing" → "completed"
sudo growpart /dev/nvme1n1 1        # if partitioned
sudo xfs_growfs /data               # xfs
# OR: sudo resize2fs /dev/nvme1n1p1  # ext4
```

### Failure signals

| Symptom | Cause | Fix |
|---------|-------|-----|
| Volume stuck attaching | Wrong AZ; instance stopping | Match AZ; wait for instance state |
| Device not visible | Nitro naming | Check `lsblk` for `nvme*` not `sd*` |
| Full disk after expand | Filesystem not grown | `growpart` + `xfs_growfs` / `resize2fs` |
| Poor DB performance | gp2 with low IOPS | Migrate to gp3 or io2; check burst balance |

---

## Mistakes to Avoid

- Attaching a volume created in `us-east-1b` to an instance in `us-east-1a`.
- Formatting on every boot — `mkfs` destroys data; only on first attach.
- Deleting a volume while snapshots exist — snapshots remain and incur cost.
- Assuming instance store and EBS behave the same — instance store is lost on stop/terminate.
- Skipping encryption on volumes containing PII or credentials.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Persistent across instance lifecycle | AZ-bound — no cross-AZ attach |
| Snapshots for backup and DR | Network latency vs local NVMe instance store |
| Independent resize and type change | Costs accumulate — monitor unattached volumes |
| Encryption with KMS | Snapshot sharing requires careful KMS key policy |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[AWS EFS (Elastic File System)]] | EFS = shared NFS file system across AZs; EBS = block device per instance |
| Instance store | Local NVMe — faster but ephemeral |
| S3 | Object storage — not a mountable block device |

---

## Use cases

- PostgreSQL data directory on io2 with provisioned IOPS.
- Application logs on gp3 with Lifecycle Manager daily snapshots.
- Root volume snapshot before AMI bake or major OS upgrade.
