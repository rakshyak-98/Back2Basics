[[buffer]] [[buffer head]] [[non-blocking]] [[file descriptors]]

# Buffer flags

> State bits on kernel or driver buffers — track lifecycle (mapped, queued, dirty, done) so producers/consumers agree on who owns the memory.

---

## Mental model

Buffers move through a **state machine**. Flags encode that state without extra syscalls:

```txt
  [FREE] ──queue──► [QUEUED] ──fill──► [DONE] ──dequeue──► [FREE]
       ▲                                      │
       └──────────── re-queue ────────────────┘
```

Flags appear at multiple layers:

| Layer | Examples | Who sets |
|-------|----------|----------|
| **Page cache / buffer head** | dirty, locked, uptodate | Kernel VFS |
| **Socket / pipe** | `O_NONBLOCK`, `MSG_DONTWAIT` | `fcntl`, send flags |
| **V4L2 / DMA drivers** | `MAPPED`, `QUEUED`, `DONE`, `ERROR` | Driver + userspace ioctl |
| **Rust / language** | `BytesMut` flags, `Vec` capacity vs len | Runtime |

Confusion usually comes from mixing **fd flags** (`O_NONBLOCK`) with **buffer flags** (driver-specific bitmask) — different namespaces.

---

## Standard config / commands

### Generic fd / socket buffer behavior

```bash
# Non-blocking mode (fd-level, not buffer struct)
fcntl(fd, F_SETFL, O_NONBLOCK)

# Socket buffer sizes (bytes)
sysctl net.core.rmem_max net.core.wmem_max
ss -tm   # shows skmem in some builds
```

### V4L2 video capture (canonical buffer-flag example)

```c
// After VIDIOC_QBUF — buffer on incoming (driver) queue
buf.flags |= V4L2_BUF_FLAG_QUEUED;

// Driver fills → DONE on outgoing (app) queue
if (buf.flags & V4L2_BUF_FLAG_DONE) { /* process frame */ }

// mmap path
buf.flags |= V4L2_BUF_FLAG_MAPPED;
```

```bash
# Inspect driver buffer state (device-specific)
v4l2-ctl -d /dev/video0 --stream-mmap --stream-count=10
```

### Linux page-cache dirty state (conceptual cousin)

```bash
grep Dirty /proc/meminfo
# See [[buffer head]] for dirty writeback policy
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Dequeue returns empty forever | Buffer never transitioned to DONE | Re-queue after consume; check driver errors (`ERROR` flag) |
| Use-after-free on mmap buffer | Dequeued while still MAPPED | Follow driver contract: unmap before free |
| `EAGAIN` on read/write | `O_NONBLOCK` set on fd | Expected for [[non-blocking]]; poll then retry |
| Stale frame / torn data | Reading buffer still QUEUED | Wait for DONE; double-buffering |

---

## Gotchas

> [!WARNING]
> **Driver buffer flags are not portable.** V4L2 flags ≠ ALSA ≠ GPU command buffers — read the subsystem docs.

> [!WARNING]
> **`O_NONBLOCK` on fd affects all operations** on that fd, not one buffer in a ring.

> [!WARNING]
> **Race: flag check without lock.** Producer sets DONE while consumer reads — use memory barriers or lockless ring design ([[Rolling Buffer]] / [[atomic ring buffer]]).

---

## When NOT to use

Do not mirror driver flag semantics in app-level enums unless you own the full queue protocol — prefer explicit state enums in your domain layer and translate at the ioctl boundary.

---

## Related

[[buffer]] [[buffer head]] [[Rolling Buffer]] [[atomic ring buffer]] [[non-blocking]] [[file descriptors]]
