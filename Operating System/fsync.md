[[system call]] [[Buffer cache]] [[WAL (Write-Ahead Log)]] [[Persistent Block Storage]] [[multiple levels of buffering]]

# fsync

> Force dirty data (and often metadata) for a file from kernel buffers to stable storage — **Stevens / Kleppmann**.

---

## Mental model

`write()` returning success means data reached **kernel page cache**, not necessarily the **physical medium**. `fsync(fd)` (or `fdatasync`, `sync_file_range`) is the contract boundary: "make this file's persisted state recoverable after crash/power loss."

```txt
app write() ──► user buffer ──► copy_to_user ──► page cache (dirty)
                                                    │
                    fsync(fd) ◄─────────────────────┘
                         │
              block layer + device cache + disk/NVMe
                         │
                    "stable" (fs-dependent definition)
```

**Layers that may still lie:**
- Disk/NVMe **write cache** (enabled by default on many drives).
- **RAID controller** BBU cache.
- **NFS** — server may ack before platter (see gotchas).
- **VM hypervisor** — flush semantics depend on cache mode (`writethrough` vs `writeback`).

**DB mental model:** PostgreSQL `COMMIT` → WAL `fsync` before ack; SQLite `PRAGMA synchronous`; RocksDB `SyncWal`. Application `fsync` on a data file without WAL ordering is usually wrong — see [[WAL (Write-Ahead Log)]].

---

## Standard config / commands

### Syscall variants (Linux)

| Call | Flushes | Typical use |
|------|---------|-------------|
| `fsync(fd)` | Data + enough metadata (size, mtime) | Default durability promise |
| `fdatasync(fd)` | Data only (metadata later if not needed for read) | Slightly cheaper when inode attrs can lag |
| `sync()` | **Global** — all dirty buffers | Shutdown scripts; avoid in hot paths |
| `sync_file_range()` | Byte range, nuanced ordering | Custom DB engines; read man page carefully |

### Observe behavior

```shell
# Trace fsync latency (common p99 killer)
strace -e trace=fsync,fdatasync,sync -T -p PID

# Per-process writeback pressure
grep -E 'Dirty|Writeback' /proc/meminfo

# Block layer stats
iostat -x 1
ionice -c 3 -p PID    # see if fsync-heavy process is starving others (best-effort)
```

### Mount / filesystem knobs

```shell
mount | grep /data
# ext4/xfs: no mount flag replaces fsync for single-file durability
# nfs: actimeo, sync mount option — see gotchas

# Disable drive write cache (DANGEROUS without BBU — know your hardware)
hdparm -W 0 /dev/sda          # SATA; verify with vendor tools for NVMe
```

### Application patterns

```c
write(fd, buf, len);
if (fsync(fd) == -1) { /* handle — disk full, EIO, NFS stale */ }
```

**Go:** `file.Sync()` → `fsync`. **Java:** `FileChannel.force(true)`. **Node:** `fs.fsync(fd, cb)` — `fs.writeFile` does **not** fsync by default.

**Postgres (operator view):** `synchronous_commit=on` (default) fsyncs WAL each commit; `off` trades durability for speed. `full_page_writes` + WAL is why random data-page fsync on crash recovery differs from app-level file fsync.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Commit latency p99 spikes | `strace -T -e fsync`; `iostat -x`; disk queue depth | Faster disk; group commits; `synchronous_commit=remote_apply`/off (accept risk); tune checkpointing |
| "Saved" file lost after crash | App only `write()`, no fsync; container ephemerality | fsync on critical paths; durable volume; WAL pattern for DBs |
| fsync fast on laptop, slow in prod | NFS? network storage? cloud volume type | Local SSD/NVMe; `fio`; check NFS mount options; avoid EBS stutter |
| Database corrupt after power loss | FS mount options; `synchronous_commit`; RAID cache | Journaling FS; BBU-backed RAID; restore from backup |
| Disk busy, low throughput | `iotop -o`; writeback storm | Spread fsync (batch commits); `ionice`; separate WAL volume |
| fsync returns 0 but data missing | NFS client cache; replica lag | `sync` mount; direct-attached storage; verify cloud SLA |

---

## Gotchas

> [!WARNING]
> **NFS `fsync` is not local disk fsync.** Many setups guarantee close-to-open consistency, not single-file durability semantics your DB expects. Running SQLite/Postgres data dir on NFS without reading vendor docs is a career event.

> [!WARNING]
> **`write()` success + crash ≠ durable.** Kernel can reorder; only ordered durability story is WAL + fsync in defined order, or fsync after each logical commit point.

> [!WARNING]
> **Double caching kills latency.** Page cache + disk write cache + RAID cache — each layer can absorb writes until fsync forces flush. `O_DIRECT` bypasses page cache but **not** device cache; still need fsync semantics for full durability unless hardware guarantees writethrough.

> [!WARNING]
> **fsync storms during checkpoint.** Postgres, MySQL InnoDB, etcd — periodic fsync of large dirty sets looks like "random I/O death" on shared EBS. Put WAL on separate volume.

> [!WARNING]
> **Containers without volume sync.** Overlay FS on ephemeral container layer — fsync on a "file" inside writable layer may not mean what you think across host crash. Mount a volume for stateful data.

**ext4/xfs:** generally sane fsync; **btrfs/zfs:** COW can amplify write amplification on fsync-heavy workloads.

---

## When NOT to use

- Don't `fsync` every row insert on a high-QPS path — batch, WAL, or accept bounded loss with explicit product decision.
- Don't call global `sync()` in application hot loops — freezes the whole machine's writeback.
- Don't assume `O_DIRECT` removes need for fsync when durability matters.

---

## Related

[[multiple levels of buffering]] [[Buffer cache]] [[WAL (Write-Ahead Log)]] [[Persistent Block Storage]] [[disk IOPS]] [[system call]] [[file descriptors]]
