[[Operating System]] [[buffer lifecycle]] [[Buffer cache]] [[fsync]] [[file descriptors]] [[multiple levels of buffering]]

# buffer

> A buffer is temporary memory that holds bytes between a fast producer and a slower consumer — smooths rate mismatches.

## Mental model

**Say it in one breath:** You copy or accumulate data into a chunk, then flush it when full, timed, or explicitly asked — user-space and kernel each have their own.

```txt
App write(buf)
    │
    ▼
User-space buffer  ──syscall──►  Kernel page/buffer cache  ──►  Device
                                      ▲
read() ◄──────────────────────────────┘
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Buffer** | Staging area for bytes | “Decouples producer speed from consumer speed.” |
| --- | --- | --- |
| **User buffer** | Memory in the process | “My `write()` pointer lives here until the syscall copies.” |
| **Kernel buffer / page cache** | Kernel-owned staging | “`write` returning OK ≠ durable on disk.” |
| **Flush** | Push buffered data down | “`fflush` / `fsync` / TCP_NODELAY — know which layer.” |
| **Backpressure** | Slow consumer stops producer | “Full buffer must block, drop, or apply control.” |
| **Zero-copy** | Avoid extra copies | “`sendfile` / `splice` skip user buffer copies.” |

### How the story goes (4 steps)

1. **Fill** — producer writes into the buffer.
2. **Hold** — absorb bursts while consumer catches up.
3. **Drain** — consumer reads, or kernel flushes to device.
4. **Reuse / free** — return the buffer to a pool or free it — see [[buffer lifecycle]].

## Standard config / commands

```c
char buf[8192];
ssize_t n = read(fd, buf, sizeof buf);
write(out, buf, n);
```

```bash
# stdio buffering: line-buffered on TTY, fully buffered on pipes
stdio_setvbuf / stdbuf -o0 ./app   # force unbuffered stdout for logs

# See socket buffer sizes
ss -m
sysctl net.core.rmem_max net.core.wmem_max

# Durability past page cache
fsync(fd)   # see [[fsync]]
```

| Knob | Why it matters |

| Buffer size | Too small → syscall thrash; too big → latency / RAM |
| --- | --- |
| `O_DIRECT` | Bypass page cache — alignment rules apply |
| `TCP_NODELAY` | Disable Nagle coalescing for small messages |
| `stdbuf` / `fflush` | “Where did my log line go?” is often user-space stdio |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Truncated last log line | stdio full buffering | `fflush`, line buffering, or `-u` |
| Data lost after crash | No `fsync` | [[fsync]] on commit points |
| Huge RSS | Giant buffers / unbounded queues | Cap size; pool + backpressure |
| High syscall rate | 1-byte reads/writes | Larger buffers; `readv`/`writev` |
| Stall on write | Downstream buffer full | Expected backpressure — tune timeouts |

## Gotchas

> [!WARNING]
> **Every layer buffers.** User stdio → kernel page cache → device cache. Flushing one does not flush all.

> [!WARNING]
> **`write()` success ≠ on disk.** It usually means “accepted into kernel memory.”

> [!WARNING]
> **Shared buffer without sync** is a race — treat buffer metadata as a [[critical sections|critical section]].

> [!WARNING]
> **Fixed buffer + unbounded message** → truncation or overflow bugs. Always track length.

## When NOT to use

- **Single small syscall already coalesced** — extra buffering adds latency for little gain.
- **Need immediate durability** — write + [[fsync]], not “bigger buffer.”
- **Security-sensitive zeroization** — clear buffers; avoid leaving secrets in pools.

## Related

[[buffer lifecycle]] [[Buffer cache]] [[multiple levels of buffering]] [[fsync]] [[file descriptors]] [[atomic ring buffer]] [[Rolling Buffer]] [[non-blocking]]
