[[Operating System]] [[thread pool]] [[multi-threaded]] [[mutexes]] [[atomic ring buffer]]

# Thread-safe queue

> A thread-safe queue lets multiple producers and consumers enqueue and dequeue without corrupting linked structure — locks, condition variables, or lock-free rings inside.

Backs [[thread pool]] task dispatch, logging pipelines, and bounded work buffers. Implementation choices:

| Style | Trade-off |
|-------|-----------|
| Mutex + condvar | Simple, contended under load |
| [[atomic ring buffer]] | Fast SPSC; MPMC needs care |
| `ConcurrentLinkedQueue` | GC language runtime managed |

Full queue policy: block producers, drop, or spin — product decision.

## Sources

- Herlihy & Shavit — concurrent queues
- Wikipedia: [Concurrent queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type))
