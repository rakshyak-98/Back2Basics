[[Operating System]] [[MBR]] [[fsync]] [[disk IOPS]] [[Buffer cache]]

# Persistent Block Storage

> Block volumes keep bytes across VM stop/restart — attach like a disk, read/write fixed-size blocks, snapshot for backup.

---

## Mental model

**Say it in one breath:** Cloud/SAN exposes a virtual disk (EBS, Persistent Disk, Azure Disk); the guest sees `/dev/vd*` and must [[fsync]] for durability.

```txt
VM ──attach──► block volume (networked/replicated)
                 ├─ filesystem / raw DB
                 └─ snapshots → backup
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Block storage** | Disk-like volumes | “Random read/write by LBA.” |
| **Persistent** | Survives instance stop | “Unlike instance-store/ephemeral.” |
| **Attach/detach** | Map volume to VM | “One writer unless clustered FS.” |
| **IOPS/throughput** | Perf caps | “Burst vs provisioned.” |
| **Snapshot** | Point-in-time copy | “Crash-consistent unless fs freeze.” |
| **Filesystem vs raw** | ext4/xfs vs direct | “DBs often want raw or O_DIRECT.” |

### How the story goes

1. **Provision** — size, type (SSD/HDD), IOPS, zone.
2. **Attach** — hypervisor presents block device.
3. **Format/mount** — or pass raw to DB.
4. **Protect** — snapshots, replication, monitored `fsync` latency.

---

## Standard config / commands

```bash
lsblk -f
sudo mkfs.xfs /dev/nvme1n1
sudo mount /dev/nvme1n1 /data
# Cloud CLIs vary: aws ec2 attach-volume / gcloud compute disks attach …
```

| Knob | Why it matters |
|------|----------------|
| Volume type | Latency + cost |
| IOPS / MB/s caps | Tail latency under load |
| AZ attachment | Can’t attach across zones |
| Encryption keys | Compliance + restore story |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Disk “vanished” after stop | Ephemeral vs persistent | Use persistent volume type |
| High p99 write | `iostat` / cloud metrics | Bigger volume; provision IOPS; check throttle |
| Corrupt after crash | No barriers / disable flush | Never mount nobarrier in prod; fix app `fsync` |
| Can’t attach | Wrong AZ / in-use | Same zone; detach elsewhere first |
| Snapshot incomplete app state | No freeze/quiesce | `fsfreeze` / DB snapshot API |
| Multi-attach chaos | Two VMs write ext4 | One writer or clustered FS |

---

## Gotchas

> [!WARNING]
> **Persistent ≠ durable write** — guest cache + volume ack semantics still need `fsync` ([[fsync]]).

> [!WARNING]
> **Snapshot ≠ app-consistent** — without quiesce you get crash-consistent only.

> [!WARNING]
> **Resize online** — grow disk then grow partition/FS; easy to forget second step.

> [!WARNING]
> **Delete VM with “delete on termination”** — volumes can vanish with the instance.

---

## When NOT to use

- **Pure blob/object workloads** — S3/GCS cheaper for large immutable objects.
- **Scratch/cache** — local NVMe ephemeral is fine if you can rebuild.
- **Multi-writer without a cluster FS** — you’ll corrupt ext4/xfs.

---

## Related

[[fsync]] [[disk IOPS]] [[Buffer cache]] [[MBR]] [[logical partitions]] [[Take snapshot]] [[write-ahead logging]]
