[[buffer]] [[Buffer cache]] [[fsync]] [[file descriptors]] [[kernel subsystem]]

# Multiple levels of buffering

> Data copies and queues between app, libc, kernel page cache, block layer, and device — each layer trades latency for throughput — **Stevens / Kleppmann**.

---

## Mental model

I/O is rarely one hop. A single `write()` may touch **five buffers** before bits reach NAND:

```txt
┌─────────────┐   ┌─────────────┐   ┌──────────────┐   ┌─────────────┐   ┌──────┐
│ app buffer  │──►│ stdio/      │──►│ kernel page  │──►│ block queue │──►│ disk │
│ (user heap) │   │ socket buf  │   │ cache (dirty)│   │ + device WC │   │      │
└─────────────┘   └─────────────┘   └──────────────┘   └─────────────┘   └──────┘
     Node Buffer       TCP sndbuf         [[Buffer cache]]      NVMe cache
```

| Layer | Who owns it | Flush / visibility |
|-------|-------------|-------------------|
| User-space buffer | Process | `fflush()` (stdio); language flush |
| Socket send buffer | Kernel TCP | ACK from peer ≠ durable on disk |
| Page cache | Kernel VFS | `fsync()` [[fsync]] |
| Block layer queue | Kernel | Ordered with flush/FUA commands |
| Device write cache | Drive/RAID | `hdparm -W`; BBU; power loss window |

**Why layers exist:** speed mismatch (CPU vs network vs disk), batching (fewer syscalls), and copy avoidance where possible (`sendfile`, `splice`).

**Durability rule:** success at layer N does **not** imply durability at layer N+k. DBs use [[WAL (Write-Ahead Log)]] + ordered fsync precisely because of this stack.

---

## Standard config / commands

### See buffering in action

```shell
# Kernel dirty memory (page cache not yet flushed)
grep -E 'Dirty|Writeback|Cached' /proc/meminfo

# Per-process I/O (includes cache writeback attribution — interpret carefully)
cat /proc/PID/io

# TCP buffer sizes
ss -tmni | head
sysctl net.ipv4.tcp_rmem net.ipv4.tcp_wmem

# Disable stdio buffering (debug)
stdbuf -o0 -e0 mycommand

# Trace copy path
strace -e write,sendfile,splice,fsync -p PID
```

### Bypass / control layers

```c
// stdio full buffering — surprise on crash
setbuf(stdout, NULL);           // line-buffered or unbuffered for tty
write(STDOUT_FILENO, ..., n);   // skip stdio layer

// socket: reduce buffering for low-latency (trade throughput)
int sz = 4096;
setsockopt(fd, SOL_SOCKET, SO_SNDBUF, &sz, sizeof sz);

// disk: O_DIRECT — user buffer aligned, skips page cache (not device cache)
open(path, O_WRONLY | O_DIRECT);
```

**Node:** `socket.setNoDelay(true)` (Nagle off) vs kernel TCP buffers still apply. `fs.writeFile` → libuv → page cache.

**Go:** `bufio.Writer` — explicit `Flush()`. `TCPConn` buffer sizes via `SetWriteBuffer`.

**Java:** Netty `WRITE_BUFFER_WATER_MARK`; `FileOutputStream` buffered wrappers.

### Container / DB tuning

```shell
# Postgres: shared_buffers (cache) vs OS page cache double-buffering awareness
# Put WAL on separate disk — fsync flushes bypass read-heavy cache pollution

# Linux writeback tuning (know before touching prod)
sysctl vm.dirty_ratio vm.dirty_background_ratio
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Wrote file" missing after crash | Which layers flushed? `fsync`? | [[fsync]] on commit points; don't trust `write()` alone |
| Log lines appear late / out of order | stdio block buffering | Line-buffer logs; `PYTHONUNBUFFERED=1`; journald |
| Memory grows, disk idle | Dirty page cache high | Normal under write load; tune dirty_ratio if needed |
| Network throughput low, CPU ok | Small writes; Nagle on | Batch writes; `TCP_NODELAY`; increase sndbuf cautiously |
| Double memory use (DB) | DB buffer pool + OS cache same pages | Linux `O_DIRECT` for some engines; cgroup memory limit |
| O_DIRECT EINVAL | Buffer alignment / size | 512-byte aligned buffers; read man page |
| NFS "fast" writes, data gone | Client + server cache | `sync` mount; local SSD for state |

---

## Gotchas

> [!WARNING]
> **`write()` returning n bytes** only guarantees delivery to the **next** layer (usually page cache), not disk — see [[fsync]].

> [!WARNING]
> **stdio buffering + fork** — child inherits full buffer; output interleaves oddly. Flush before fork or use `write()`.

> [!WARNING]
> **O_DIRECT doesn't mean durable.** Device write cache still lies until flush/FUA/fsync completes to media (hardware dependent).

> [!WARNING]
> **NFS fsync lies** — client may think data is stable when server has only cached it. Not a buffering tuning problem — architectural.

> [!WARNING]
> **Epoll + partial reads** — kernel socket buffer holds unread bytes; app must drain or LT keeps signaling.

**Metrics trap:** high `Cached` in `free -m` is often healthy page cache, not leak.

---

## When NOT to use

- Don't disable all buffering for throughput workloads — you'll syscall yourself to death.
- Don't use `O_DIRECT` without measuring — misalignment penalties hurt; DB engines know their path.
- Don't stack redundant app buffers (256KB user buffer + 256KB stdio + huge TCP window) without reason.

---

## Related

[[buffer]] [[buffer lifecycle]] [[Buffer cache]] [[fsync]] [[file descriptors]] [[non-blocking]] [[Persistent Block Storage]] [[kernel subsystem]]
