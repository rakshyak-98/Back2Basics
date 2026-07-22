[[Inter Process Communication]] [[mutexes]] [[semaphores]] [[Linux]]

# Shared memory

> Mapped RAM visible to multiple processes — fastest IPC when you accept explicit synchronization and lifetime rules.

---

## Mental model

**Shared memory** maps the same physical pages into multiple address spaces. After setup, reads/writes are normal memory ops — **no kernel copy per access** (unlike pipe/socket).

```txt
Process A                Process B
┌─────────────┐         ┌─────────────┐
│ 0x7f..1000  │────────►│ 0x7f..8000  │   same physical page
│  (mapped)   │         │  (mapped)   │
└─────────────┘         └─────────────┘
         ▲                       ▲
         └──── shm segment / memfd / mmap file ────┘
```

API families:
- **POSIX** `shm_open` + `mmap`
- **System V** `shmget` / `shmat` (legacy; isolated by [[IPC namespace]])
- **Anonymous** `mmap(MAP_SHARED | MAP_ANONYMOUS)` after `fork`
- **memfd** + pass fd via `SCM_RIGHTS` socket

**No implicit locking** — concurrent writers require [[mutexes]], atomics, or ring buffers ([[atomic ring buffer]]).

---

## Standard config / commands

### POSIX shared memory

```c
// Create / open
int fd = shm_open("/myseg", O_CREAT | O_RDWR, 0600);
ftruncate(fd, size);
void *p = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
```

```bash
# Inspect SysV segments
ipcs -m
# Remove stale
ipcrm -m SHMID
```

### Linux memfd (common in containers)

```c
int fd = memfd_create("buf", MFD_CLOEXEC);
ftruncate(fd, size);
void *p = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
// send fd to peer via unix socket SCM_RIGHTS
```

### Size and limits

```bash
sysctl kernel.shmmax kernel.shmall   # SysV limits
cat /proc/sys/kernel/shmmni
```

**Why `0600` on `shm_open`:** world-readable shared memory leaks cross-user data on multi-tenant hosts.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Random corruption | Missing lock; struct padding races | Mutex or lock-free ring; align structs; `volatile` is not a lock |
| `EINVAL` on shmat | Size mismatch; destroyed segment | Recreate with agreed size; lifecycle protocol |
| Leaked SysV segments after crash | `ipcs -m` | `ipcrm`; use POSIX names + `shm_unlink` on shutdown |
| Container can't see host shm | [[IPC namespace]] isolation | `--ipc=host` (careful) or named volume/socket design |

---

## Gotchas

> [!WARNING]
> **Cache coherency is CPU-level, not magic** — still need memory barriers for lock-free structures.

> [!WARNING]
> **`MAP_SHARED` writes visible immediately** to other mappers — no flush — but not durable across reboot (RAM).

> [!WARNING]
> **Orphan segments** persist until reboot or explicit destroy — long-running servers leak `ipcs` entries without cleanup handlers.

---

## When NOT to use

Prefer **message passing** (socket, pipe) when you need clear ownership boundaries, cross-machine IPC, or untrusted peers. Shared memory shines for **high-throughput same-machine** data (video frames, ring buffers, DB buffer pools).

---

## Related

[[Inter Process Communication]] [[IPC namespace]] [[mutexes]] [[atomic ring buffer]] [[Rolling Buffer]]
