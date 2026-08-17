[[AWS EC2]] [[AMI (Amazon Machine Image)]] [[AWS EFS (Elastic File System)]] [[AWS Billing and cost management]]

# EBS (Elastic Block Store)

> EBS provides network-attached block volumes for EC2 — durable, snapshot-backed disks you attach to one instance at a time (except Multi-Attach on io2).

```txt
        EBS (Elastic Block ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               └── Comparison
```

## Why It Matters
- **Key signal:** EBS reviews probe volume types, IOPS, snapshots, and AZ attachment constra…

## Sources
- [Amazon EBS volume types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html) — overview
- [Amazon EBS snapshots](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html) — overview

## Technical Details
### Volume types (gp3 is the default choice)

| Type | Use case | Notes |
|------|----------|-------|
| **gp3** | General purpose boot and data | Baseline 3,000 IOPS; scale IOPS/throughput independently |
| **gp2** | Legacy general purpose | IOPS tied to size |
| **io2 / io2 Block Express** | Databases, sustained IOPS | Highest durability SLA |
| **st1** | Throughput-oriented HDD | Big sequential workloads |
| **sc1** | Cold HDD | Infrequent access |
| **Instance store** | Ephemeral local NVMe | Fast, lost on stop/terminate — not EBS but often compared |

- Volumes live in an **Availability Zone**.
- Attach only to instances in the same AZ (unless using cross-AZ patterns with …

### Attach and mount

```bash
# After attaching volume in console/CLI, on Linux:
lsblk
sudo mkfs -t xfs /dev/nvme1n1    # first use only
sudo mkdir /data
sudo mount /dev/nvme1n1 /data
```

- Add `/etc/fstab` entry using UUID, not device name, for reboot safety.

### Snapshots and AMIs

- **Snapshots:** are incremental backups to S3 (managed by AWS)
- **Copy snapshots:** across regions for disaster recovery.
- **Fast Snapshot Restore:** costs extra; use for large parallel launches.

### Resize

```bash
aws ec2 modify-volume --volume-id vol-0abc --size 100
# Then grow partition and filesystem inside the OS
sudo growpart /dev/nvme0n1 1
sudo xfs_growfs /data
```

### Encryption

- Enable encryption at creation; uses AWS-managed or customer-managed KMS keys.
- Encrypted snapshots stay encrypted when copied.

## Comparison
- **vs [[AWS EFS (Elastic File System)]]**

| EBS | EFS |
|-----|-----|
| Block, one instance (usually) | POSIX file system, many instances |
| AZ-local | Regional, scales automatically |
| Lower latency for single host | Shared files, web roots, content |
