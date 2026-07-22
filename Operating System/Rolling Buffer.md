[[atomic ring buffer]] [[buffer]] [[kernel ring buffer]] [[shared memory]]

# Rolling buffer

> Fixed-capacity circular queue — new writes advance the head and overwrite the oldest slot; bounded memory for streams without realloc/GC churn.

---

## Mental model

Also called **ring buffer** or **circular buffer**. One contiguous array + read/write indices modulo capacity:

```txt
capacity N=8
        read_idx → 2
        write_idx → 6
[_|_|X|X|X|X|X|X]
      └── oldest live ──┘  └── newest ──┘
When write catches read → full (drop, block, or expand policy)
When read catches write → empty
```

Use cases:
- Audio/video jitter buffers
- Serial/UART DMA
- Log tail windows ([[kernel ring buffer]] pattern)
- IPC between threads ([[atomic ring buffer]] for lock-free)

**Policy when full:** overwrite (lossy telemetry), block producer, or drop newest — pick explicitly.

---

## Standard config / commands

### Linux `kfifo` (kernel)

```c
// Conceptual API
DECLARE_KFIFO(fifo, typeof(data), SIZE);
kfifo_in(&fifo, &item, 1);
kfifo_out(&fifo, &item, 1);
```

### Userspace pattern (single-threaded)

```c
typedef struct {
    uint8_t *buf;
    size_t cap, head, tail;
} ring_t;

size_t next = (head + 1) % cap;
if (next != tail) { buf[head] = byte; head = next; }
```

### Inspect as pattern in tools

```bash
# Many daemons expose ring-backed logs — e.g. trace ring buffer
perf record -e syscalls:sys_enter_write -a sleep 1
# Design: fixed alloc at init — no malloc in steady state
```

**Why static allocation:** predictable latency in embedded/real-time — avoids allocator locks and fragmentation under load.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Corrupt data | TOCTOU head/tail race | Mutex or [[atomic ring buffer]] with memory barriers |
| Lost events | Overwrite policy | Increase capacity; back-pressure producer |
| Deadlock | Block when full + consumer stuck | Timeouts; separate drop metric |
| Off-by-one full/empty | `(head+1)%N == tail` vs count | Unit test boundary; use sentinel slot |

---

## Gotchas

> [!WARNING]
> **Power-of-two capacity** enables mask instead of modulo — faster but constrains size choice.

> [!WARNING]
> **False sharing** — head/tail on same cache line kills MP performance; pad to cache line.

> [!WARNING]
> **"Rolling" in logs often means time window**, not strict ring — clarify retention policy.

---

## When NOT to use

If you need **unbounded history** or random access by key, use a deque + disk spill, not a ring. Rings fit **streaming FIFO** with known max lag.

---

## Related

[[atomic ring buffer]] [[buffer flags]] [[kernel ring buffer]] [[shared memory]] [[buffer]]
