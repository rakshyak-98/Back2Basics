[[Operating System]] [[thread pool]] [[multi-threaded]] [[mutexes]] [[atomic ring buffer]]

# Thread-safe queue

> A thread-safe queue lets multiple producers and consumers enqueue/dequeue without corrupting structure — via locks, condition variables, or lock-free rings.

## Interview Relevance

MPMC vs SPSC, blocking vs drop-on-full, and which structure backs a [[thread pool]].

## Sources

- Herlihy & Shavit — concurrent queues — deep-dive
- [Wikipedia — Queue (abstract data type)](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)) — overview

## Key Concepts

- **Concurrent access:** many producers/consumers safely.
- **Implementations:** mutex+condvar; [[atomic ring buffer]] (often SPSC); runtime concurrent queues.
- **Full policy:** block, drop, or spin — product decision.
- **Use cases:** pools, logging pipelines, bounded work buffers.

## Technical Details

| Style | Trade-off |
|-------|-----------|
| Mutex + condvar | Simple, contended under load |
| [[atomic ring buffer]] | Fast SPSC; MPMC needs care |
| `ConcurrentLinkedQueue` | GC language runtime managed |

Backs [[thread pool]] task dispatch in [[multi-threaded]] systems; often guarded with [[mutexes]] when not lock-free.

## Real-World Applications

Executor frameworks, log shippers, and stage pipelines in stream processors.

## Pros/Cons or Trade-offs

- **Pro:** Decouples producers/consumers safely.
- **Con:** Contention; unbounded growth if misconfigured.
- **Trade-off:** lock simplicity vs lock-free complexity.

## Comparison

- vs [[atomic ring buffer]]: ring is a common bounded implementation; “thread-safe queue” is the ADT.
- vs channels: language channels are queues with waiting built in.

## Mistakes to Avoid

- Unbounded queues as load shedding “solutions.”
- Using an SPSC ring with multiple producers.
- Forgetting memory visibility (locks/atomics/barriers) when rolling your own.
