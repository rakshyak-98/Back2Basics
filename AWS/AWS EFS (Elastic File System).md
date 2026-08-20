[[AWS]] [[AWS EC2]] [[EBS (Elastic Block Store)]] [[AWS S3]] [[Security group]] [[AWS Networking]] [[NFS (Network File System)]]

# AWS EFS (Elastic File System)

> Managed **NFS** file system that grows with data and mounts on many Linux clients across AZs — shared POSIX for EC2/ECS/Lambda-in-VPC. Not a block disk; not object storage.

## Mental model

EFS is a **regional** filesystem with **mount targets** (ENIs) in subnets. Clients mount via NFSv4 over the mount-target IP/DNS. Throughput and IOPS scale with size (or provisioned / Elastic modes). Security = **mount-target SG** + IAM auth (optional) + encryption in transit (`tls` mount option).

```
EC2-a (AZ-a) ──► mount target ENI ──┐
EC2-b (AZ-b) ──► mount target ENI ──┼──► EFS (regional)
ECS task     ──► mount target ENI ──┘
```

| vs | Use EFS when | Prefer instead |
|----|--------------|----------------|
| EBS | Shared files across instances | Single-instance disk → [[EBS (Elastic Block Store)]] |
| S3 | POSIX semantics / append / locks | Immutable objects / CDN → [[AWS S3]] |

## Standard config / commands

### Create + mount (Amazon Linux / Ubuntu)

```bash
# Console/CLI: create filesystem, mount targets in each app subnet, SG allowing NFS 2049 from client SG
sudo yum install -y amazon-efs-utils   # or nfs-common + stunnel for tls
sudo mkdir -p /mnt/efs
sudo mount -t efs -o tls fs-xxxx:/ /mnt/efs
# fstab: fs-xxxx:/ /mnt/efs efs _netdev,tls 0 0
```

### SG pattern

| SG | Inbound |
|----|---------|
| `efs-mt` | TCP **2049** from `app-sg` (SG id, not `0.0.0.0/0`) |
| `app-sg` | (no special for EFS beyond egress to mount target) |

### Performance modes (pick at create; some are immutable)

| Mode | When |
|------|------|
| **General Purpose** | Default latency-sensitive |
| **Max I/O** | Legacy high-parallelism (higher latency) |
| **Elastic / Provisioned throughput** | Burst-credit exhaustion or known steady MB/s |

```bash
aws efs describe-file-systems --file-system-id fs-xxx
aws efs describe-mount-targets --file-system-id fs-xxx
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `mount.nfs: Connection timed out` | Mount target in client VPC/subnet? SG 2049? | Fix SG; mount from same VPC; NACL |
| Hang / slow writes | Burst credits; throughput mode; AZ mismatch | Elastic/Provisioned; mount same-AZ target |
| Permission denied | POSIX uid/gid; IAM policy (if IAM auth) | Align uid; EFS access points |
| Lambda timeout mounting EFS | Cold start + ENI + NFS | Prefer /tmp or S3; provision concurrency carefully |
| Cost spike | Infrequent Access mistier; unused GB | Lifecycle to IA; delete unused FS |

## Gotchas

> [!WARNING]
> **Mount from wrong AZ** works but adds cross-AZ data charges and latency — prefer per-AZ mount targets + same-AZ clients.

> [!WARNING]
> **Bursting mode** — idle FS earns credits; sustained write after idle can throttle. Watch `BurstCreditBalance`.

> [!WARNING]
> **Not multi-writer database storage** — databases want EBS/local; EFS is for shared configs, uploads, CMS content.

> [!WARNING]
> **Encryption in transit** needs `amazon-efs-utils` (`tls` option), not plain `nfs-common` alone.

## When NOT to use

- **Single EC2 disk** — EBS is cheaper and lower latency.
- **Static assets for the internet** — S3 + CloudFront.
- **Windows SMB shares** — FSx for Windows / NetApp, not EFS.
- **High-IOPS transactional DB** — RDS / EBS io2.

## Related

[[AWS EC2]] · [[EBS (Elastic Block Store)]] · [[AWS S3]] · [[Security group]] · [[AWS Networking]] · [[NFS (Network File System)]] · [[AWS]]
