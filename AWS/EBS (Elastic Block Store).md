[[AWS]] [[AWS EC2]] [[AWS EBS(Elastic Block Store)]] [[AMI (Amazon Machine Image)]]

# EBS (Elastic Block Store)

> EBS — network-attached block disk for one EC2 instance in one AZ; survives stop; snapshots for backup/clone.

---

## Mental model

**Say it in one breath:** Like a remote SSD/HDD plugged into the instance. Format/mount in the OS. Snapshot → incremental backup in S3 (API-only, not a browsable bucket). Prefer the sibling note [[AWS EBS(Elastic Block Store)]] for deeper ops — this is the field card.

```txt
EC2 (AZ-a) ──attach──► EBS vol (AZ-a)
                          │ snapshot
                          ▼
                     New vol (any AZ in region after create)
```

| Type (common) | Fit |
|---------------|-----|
| **gp3** | Default general purpose |
| **io2** | Sustained high IOPS (DBs) |
| **st1/sc1** | Throughput HDD / cold |

---

## Standard config / commands

```bash
aws ec2 create-volume --availability-zone us-east-1a --size 100 --volume-type gp3
aws ec2 attach-volume --volume-id vol-… --instance-id i-… --device /dev/xvdf

# Snapshot + DLM/AWS Backup for retention
aws ec2 create-snapshot --volume-id vol-… --description "pre-migrate"
```

| Knob | Why it matters |
|------|----------------|
| Same AZ | Attach requires volume AZ = instance AZ |
| Delete on termination | Root often true — data gone with instance |
| Encrypt | KMS CMK; snapshots inherit |
| Recycle Bin | Soft-delete protection for vols/snaps |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Attach fails | AZ mismatch | Create/copy volume in instance AZ |
| Disk full | `df -h` | Grow volume + `growpart`/`resize2fs` |
| Data gone after terminate | DeleteOnTermination | Restore snapshot; fix LT mapping |
| Slow IO | `VolumeQueueLength` | gp3 IOPS/throughput; io2 for DB |
| Snapshot “stuck” | First full snap | Wait; later snaps incremental |
| Can’t mount | Need filesystem | `mkfs` once; then mount + fstab/UUID |

---

## Gotchas

> [!WARNING]
> **EBS ≠ multi-attach by default** — one instance (io2 multi-attach is special-case).

> [!WARNING]
> **Snapshots aren’t S3 objects you ls** — only volume create/restore APIs.

> [!WARNING]
> **Unencrypted → encrypted** needs copy/migrate path; plan ahead.

---

## When NOT to use

- **Shared POSIX across many instances** — use [[AWS EFS (Elastic File System)]].
- **Object / CDN content** — S3.
- **Ephemeral scratch only** — instance store (faster, dies with instance).

---

## Related

[[AWS EBS(Elastic Block Store)]] [[AWS EC2]] [[AMI (Amazon Machine Image)]] [[AWS EFS (Elastic File System)]]
