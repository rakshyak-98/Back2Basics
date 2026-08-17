[[Operating System]] [[Rolling Buffer]] [[kernel ring buffer]] [[thread-safe queue]] [[mutexes]] [[multi-threaded]] [[semaphores]] [[right buffer]]

# Atomic ring buffer

> A ring buffer stores a fixed-capacity stream by wrapping read/write indices around a circular array — atomics let one producer and one consumer update those indices without a lock.

```txt
        Atomic ring buffer ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Concurrency classic: SPSC lock-free ring, memory barriers (“store data before…

## Sources
- Linux kernel: `include/linux/kfifo.h`, `lib/kfifo.c` — deep-dive
- Lamport, “Concurrent Reading and Writing” — deep-dive
- [Wikipedia — Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer) — overview

## Key Concepts
- **Circular indices:** wrap instead of shifting elements.
- **SPSC lock-free:** one producer, one consumer; atomics + barriers publish indices.
- **Full/empty:** `(write + 1) % N == read` vs `write == read` (one slot reserved or explicit c…
- **MPMC needs more:** [[mutexes]], [[semaphores]], or a [[thread-safe queue]].

## Technical Details
```txt
     read_idx ──► [ | | | | | ] ◄── write_idx
                    buffer[N]
```

- Producer advances `write_idx` after storing data.
- Consumer advances `read_idx` after reading data.

| Use | Example |
|-----|---------|
| Kernel logging | [[kernel ring buffer]] (`dmesg`) |
| Audio / DSP | Sample streams between interrupt and user thread |
| IPC | Pipe-like shared-memory channels |
| Networking | NIC driver descriptor rings |

- Failure modes: overrun

## Mistakes to Avoid
- **Mistake:** Publishing the write index before the slot data is fully written
- **Mistake:** Using one SPSC ring with multiple producers without extra sync
- **Mistake:** Putting read/write indices on the same cache line (false sharing)

## Pros/Cons or Trade-offs
- **Pro:** Bounded memory, low overhead for SPSC.
- **Con:** Fixed capacity; MPMC is harder; silent drop if overwrite policy.
- **Trade-off:** drop-oldest ([[Rolling Buffer]] policy) vs block producer.

## Comparison
- vs [[Rolling Buffer]]: rolling emphasizes overwrite policy
- vs [[thread-safe queue]]: queues often grow or block; rings are typically fixed-size.


### Use cases
- `dmesg` rings, audio pipelines, DPDK/NIC descriptor rings, and user-space log…
