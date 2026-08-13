[[Operating System]] [[Rolling Buffer]] [[kernel ring buffer]] [[thread-safe queue]] [[mutexes]] [[multi-threaded]]

# Atomic ring buffer

> A ring buffer stores a fixed-capacity stream by wrapping a read index and write index around a circular array — atomics let one producer and one consumer update those indices without a lock.

A **ring buffer** (circular buffer) avoids shifting elements: when the write index reaches the end, it wraps to zero. **Atomic** operations (C11 `atomic_load`/`atomic_store`, or kernel `READ_ONCE`/`WRITE_ONCE` with memory barriers) publish index updates so the other side sees a consistent snapshot.

## Single-producer, single-consumer (SPSC)

The classic lock-free pattern:

```txt
     read_idx ──► [ | | | | | ] ◄── write_idx
                    buffer[N]
```

- Producer advances `write_idx` after storing data.
- Consumer advances `read_idx` after reading data.
- Full when `(write + 1) % N == read`; empty when `write == read`.

Only one writer and one reader may touch each index without additional synchronization. Multiple producers require [[mutexes]], semaphores ([[semaphores]]), or a [[thread-safe queue]].

## Where it appears

| Use | Example |
|-----|---------|
| Kernel logging | [[kernel ring buffer]] (`dmesg`) |
| Audio / DSP | Sample streams between interrupt and user thread |
| IPC | Pipe-like shared-memory channels |
| Networking | NIC driver descriptor rings |

## Failure modes

- **Overrun** — producer faster than consumer; oldest data is dropped or the write blocks.
- **Torn reads** — without proper barriers, consumer sees new index but old slot contents (fix: store data before publishing index).
- **False sharing** — read and write indices on the same cache line ping-pong between cores.

Compare with a generic [[Rolling Buffer]] used for logging semantics and [[right buffer]] sizing for latency versus memory.

## Sources

- Linux kernel: `include/linux/kfifo.h`, `lib/kfifo.c`
- Lamport, “Concurrent Reading and Writing” (ring buffer foundations)
- Wikipedia: [Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer)
