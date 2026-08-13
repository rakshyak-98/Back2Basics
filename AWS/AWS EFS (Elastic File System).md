[[AWS EC2]] · [[EBS (Elastic Block Store)]] · [[AWS Networking]] · [[Security group]]

# AWS EFS (Elastic File System)

> EFS is a managed, regional NFS file system that multiple EC2 instances mount concurrently — ideal for shared content, not for low-latency database block I/O.

---

## How it works

EFS presents a **POSIX file system** over NFSv4.1. Mount targets (one per AZ in your VPC) provide ENIs in your subnets. Clients mount:

```bash
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 \
  fs-0abc1234.efs.us-east-1.amazonaws.com:/ /mnt/efs
```

Use **EFS mount helper** (`amazon-efs-utils`) for TLS in transit and simpler DNS.

## Performance modes and classes

| Option | Trade-off |
|--------|-----------|
| **Bursting throughput** | Scales with stored data size |
| **Provisioned throughput** | Pay for fixed throughput regardless of size |
| **Elastic throughput** | Scales automatically (default on new file systems) |
| **Standard vs Infrequent Access (IA)** | Lifecycle policy moves cold files to cheaper storage |

**General Purpose** performance suits latency-sensitive workloads; **Max I/O** (legacy) handled higher aggregate throughput with higher latency.

## Security

- Mount targets need [[Security group]] allowing NFS (TCP 2049) from clients.
- **Encryption at rest** (KMS) and **in transit** (TLS via mount helper).
- **Access points** provide application-specific POSIX user/group and root directory isolation.

## vs [[EBS (Elastic Block Store)]]

| Need | Pick |
|------|------|
| Database data directory on one host | EBS io2/gp3 |
| Shared WordPress uploads across web tier | EFS |
| Read-heavy static assets | EFS + CloudFront origin |

## Failure signals

| Symptom | Check |
|---------|-------|
| Mount timeout | Security group, subnet routing, mount target health |
| Stale file handle | Client lost connectivity; remount |
| High cost | IA lifecycle, throughput mode, data growth |

## Recall

- Why does EFS need a mount target per Availability Zone?
- When is EFS the wrong choice compared to S3?

## Sources

- [Amazon EFS User Guide](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html)
- [NFSv4.1 protocol (RFC 5661)](https://datatracker.ietf.org/doc/html/rfc5661)
