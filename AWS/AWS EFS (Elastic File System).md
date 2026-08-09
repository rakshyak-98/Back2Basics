[[AWS]] [[AWS EC2]] [[EBS (Elastic Block Store)]] [[NFS (Network File System)]]

# AWS EFS (Elastic File System)

> EFS — managed NFS that many Linux EC2/containers mount at once; grows/shrinks with data across AZs.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Create filesystem → mount targets in subnets → `mount -t nfs4`. Shared home dirs, CMS uploads, lift-and-shift apps that need a real filesystem — not a block device.

```txt
EC2-a ─┐
EC2-b ─┼── NFSv4 ──► EFS (multi-AZ)
ECS   ─┘
```

| Mode | Tradeoff |
|------|----------|
| General Purpose | Default latency |
| Max I/O | Higher aggregate throughput, more latency |
| Bursting vs Elastic/Provisioned | Throughput accounting / cost |

---

## Standard config / commands

```bash
# Mount (Amazon Linux helper often available)
sudo mount -t nfs4 -o nfsvers=4.1 fs-….efs.region.amazonaws.com:/ /mnt/efs

# Security: NFS port 2049 from clients’ SG → EFS SG
```

| Knob | Why it matters |
|------|----------------|
| Mount targets | One per AZ you use; private subnets |
| SG on EFS | Inbound 2049 from instance SG |
| Encryption in transit | TLS mount helper / stunnel |
| Access points | Enforce path + POSIX uid/gid for apps |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Connection timed out` | SG/NACL/mount target subnet | Open 2049; fix route to mount target |
| `access denied` | Policy / AP uid | Fix filesystem policy; access point identity |
| Slow under load | Throughput mode / credits | Elastic throughput or provisioned |
| Permission weirdness | NFS root squash / uid | Align container user with AP |
| Mount works one AZ only | Missing mount target | Create MT in each AZ used |

---

## Gotchas

> [!WARNING]
> **Not a Windows first-class FS** — Linux/NFS oriented.

> [!WARNING]
> **Small-file heavy workloads** — EFS can look expensive/slow vs local SSD or S3.

> [!WARNING]
> **Delete filesystem = delete data** — backups via AWS Backup.

---

## When NOT to use

- **Single-instance DB data dir** — [[EBS (Elastic Block Store)]] is lower latency.
- **Static website / blob store** — S3.
- **Windows SMB shares** — FSx for Windows / NetApp.

---

## Related

[[EBS (Elastic Block Store)]] [[AWS EC2]] [[Security group]] [[AWS Networking]]
