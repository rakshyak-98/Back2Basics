[[Operating System]] [[buffer]] [[Rolling Buffer]] [[kernel ring buffer]] [[atomic ring buffer]] [[Blocking]] [[multiple levels of buffering]]

# Right buffer

> Choosing the right buffer size balances latency, memory, and drop behavior — too small causes syscalls or overruns; too large hides backpressure until memory pressure hits.

## Interview Relevance

Capacity interviews: how you pick socket/ring sizes, what you measure (drops, syscall rate), and full-queue policy.

## Sources

- Stevens, *UNIX Network Programming* — socket buffer tuning — deep-dive
- Linux `socket(7)` — SO_SNDBUF, SO_RCVBUF — deep-dive

## Key Concepts

- **No universal constant:** depends on burst, drain rate, memory budget, durability.
- **Too small:** overruns ([[atomic ring buffer]]) or syscall storms.
- **Too large:** hides backpressure; crash loses more RAM-buffered data.
- **Policy:** block ([[Blocking]]), drop, or spin when full.

## Technical Details

| Question | If wrong |
|----------|----------|
| Producer burst rate? | Overrun in [[atomic ring buffer]] |
| Consumer steady drain? | [[Blocking]] producer |
| Memory budget per connection? | OOM under fan-in |
| Durability need? | Large RAM buffer loses data on crash |

Tune with `strace` syscall counts, drop counters, `perf`. Related: [[Rolling Buffer]], [[kernel ring buffer]], [[multiple levels of buffering]].

## Real-World Applications

Audio low-latency rings, bulk TCP windows, and kernel log_buf sizing.

## Pros/Cons or Trade-offs

- **Small buffers:** low latency; fragile under bursts.
- **Large buffers:** absorb bursts; more memory and delayed backpressure.
- **Trade-off:** drop-oldest vs block-producer product requirements.

## Comparison

- vs [[buffer]]: buffer is the object; “right buffer” is the sizing decision.
- vs unlimited queues: bounded buffers force an explicit policy.

## Mistakes to Avoid

- Copying a blog’s `SO_RCVBUF` without measuring.
- Unlimited in-memory queues “to never block.”
- Ignoring per-connection buffer memory under C10k fan-in.
