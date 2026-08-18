[[Operating System]] [[buffer]] [[Rolling Buffer]] [[multi-threaded]]

# Atomic ring buffer

> Fixed-size circular queue with atomic head/tail — lock-free handoff between producer and consumer threads.

## Mental model

**Say it in one breath:** One array, wrap indices with `% capacity`; publish with release stores so the other side sees data before the index moves.

```txt
        read ──►  [ A | B | C | _ ]
                        ▲
                      write
  full when next_write == read
  empty when read == write
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Ring / circular buffer** | Reuse a fixed slot array | “Write wraps; no malloc per message.” |
| --- | --- | --- |
| **SPSC** | One producer, one consumer | “Simplest lock-free design — one owner per index.” |
| **MPMC** | Many producers/consumers | “Needs CAS on both ends; much harder.” |
| **CAS / FAA** | Atomic update primitives | “Claim a slot without a mutex.” |
| **Acquire / release** | Memory ordering | “Write data, then release-store the index.” |
| **False sharing** | Contended cache line | “Pad head/tail onto separate lines.” |

### How the story goes

1. **Reserve** — load write index; compute next; if full, fail/block/overwrite.
2. **Write** — store payload into `buffer[slot]`.
3. **Publish** — `store(next, release)` so consumer sees data.
4. **Consume** — load read; if empty fail; copy out; `store(read+1, release)`.

## Standard config / commands

```cpp
// SPSC sketch (C++ atomics)
template<typename T, size_t N>
struct Ring {
  std::array<T, N> buf{};
  alignas(64) std::atomic<size_t> w{0};
  alignas(64) std::atomic<size_t> r{0};
  bool push(const T& x) {
    auto cur = w.load(std::memory_order_relaxed);
    auto nxt = (cur + 1) % N;
    if (nxt == r.load(std::memory_order_acquire)) return false;
    buf[cur] = x;
    w.store(nxt, std::memory_order_release);
    return true;
  }
  bool pop(T& out) {
    auto cur = r.load(std::memory_order_relaxed);
    if (cur == w.load(std::memory_order_acquire)) return false;
    out = buf[cur];
    r.store((cur + 1) % N, std::memory_order_release);
    return true;
  }
};
```

| Knob | Why it matters |

| Capacity power-of-two | Fast mask instead of `%` |
| --- | --- |
| Cache-line pad indices | Avoid false sharing under load |
| Full policy | Drop, block, or overwrite oldest |
| SPSC vs MPMC | Complexity / correctness risk |

Libs: Boost.Lockfree `spsc_queue`, LMAX Disruptor (Java), liblfds.

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Lost / torn messages | Write after index publish | Data then release-store index |
| “Full” forever | Consumer stuck; wrong empty/full test | Leave one slot empty; fix wrap |
| High CPU CAS fails | MPMC contention | Shard rings or use mutex queue |
| Wrong data under load | Relaxed loads without acquire | Use acquire/release pairs |
| Latency spikes | False sharing on head/tail | `alignas(64)` separate atomics |
| Overwrite surprises | Full policy = clobber | Document; metrics on drops |

## Gotchas

> [!WARNING]
> **SPSC code is not MPMC** — two producers racing `write_index` corrupt the ring.

> [!WARNING]
> **Capacity N holds N−1** — classic design keeps one slot empty to distinguish full vs empty.

> [!WARNING]
> **ABA / wrap** — huge counters or generation tags if you reuse slots carefully in MPMC.

> [!WARNING]
> **Language memory model** — “volatile” in Java ≠ C++ `atomic`; pick the real atomics API.

## When NOT to use

- **Need blocking + priorities** — use a proper concurrent queue / channel.
- **Variable-size huge messages** — ring of pointers + pool, or different structure.
- **Cross-process without shared memory setup** — use pipes/sockets ([[Inter Process Communication]]).

## Related

[[buffer]] [[Rolling Buffer]] [[kernel ring buffer]] [[thread-safe queue]] [[multi-threaded]] [[critical sections]]
