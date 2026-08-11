[[Persistent Block Storage]] [[Buffer cache]] [[file descriptors]]

# Abstract storage location

> API that hides physical placement — callers use logical names (paths, URIs, keys) while the system maps to blocks, objects, or remote stores.

---

## Mental model

An **abstract storage location** decouples **what** you access from **where** bits live:

```txt
Application          Abstraction layer              Physical
─────────────        ─────────────────              ────────
open("s3://b/k")  →  object store driver       →   REST + erasure-coded disks
write(fd, buf)    →  VFS + page cache          →   NVMe LBA 0x4a2f…
SELECT …          →  tablespace / table        →   InnoDB files on ext4
```

Benefits: portability, migration, tiering (hot SSD → cold object store). Cost: **weaker latency predictability** unless you understand the mapping.

Layers engineers confuse:
- **Path** (`/var/lib/data`) — mount namespace + filesystem
- **URI** (`s3://`, `gs://`) — vendor API semantics
- **Key-value** (Redis, etcd) — no hierarchical byte offset
- **DB logical** (table/index) — buffer manager hides file layout

---

## Standard config / commands

### Unix path abstraction (most common)

```bash
# Logical path → inode on backing device
ls -li /var/lib/postgresql/data
findmnt /var/lib/postgresql/data
stat /var/lib/postgresql/data
```

### Object storage (location opaque)

```bash
aws s3 cp ./dump.sql s3://mybucket/backups/
aws s3 ls s3://mybucket/backups/
# No LBA — consistency model is eventual (list) vs read-after-write (new object)
```

### Bind mount — remap logical path

```bash
mount --bind /mnt/fast-disk/pgdata /var/lib/postgresql/data
# App sees same path; bits on different device
```

**Why bind mounts:** migrate data without reconfiguring app paths — common in container volume patterns.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "File not found" after migration | Path vs actual mount | `findmnt`; fix bind mount / symlink |
| Slow "local" writes | NFS/EBS/network backing | Move hot data to local NVMe; check [[disk IOPS]] |
| S3 404 on existing object | Wrong region/bucket/prefix | URI spelling; IAM scope |
| DB on wrong disk tier | Tablespace location | `SHOW data_directory`; relocate tablespace |

---

## Gotchas

> [!WARNING]
> **Abstraction ≠ durability.** Object upload "success" may be regional; DB commit needs WAL/fsync policy — see [[fsync]].

> [!WARNING]
> **Copy-by-path assumptions break** across abstraction boundaries — `cp` works on POSIX files, not always on object prefixes without tools.

> [!WARNING]
> **Container paths** — `/app/data` may be ephemeral overlay unless volume mounted; rebuild loses "logical" path.

---

## When NOT to use

Avoid stacking opaque abstractions without observability (FUSE on NFS on loopback). For latency-sensitive systems, make **one** clear mapping from logical name to physical device measurable.

---

## Related

[[Persistent Block Storage]] [[Buffer cache]] [[file descriptors]] [[one-level storage system]]
