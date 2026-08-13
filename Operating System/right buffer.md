[[Operating System]] [[buffer]] [[Rolling Buffer]] [[kernel ring buffer]] [[atomic ring buffer]]

# Right buffer

> Choosing the right buffer size balances latency, memory, and drop behavior — too small causes syscalls or overruns; too large hides backpressure until memory pressure hits.

No universal constant: audio streams want low latency (small ring), bulk export wants large TCP windows, kernel logs use fixed [[kernel ring buffer]] capacity.

## Sizing questions

| Question | If wrong |
|----------|----------|
| Producer burst rate? | Overrun in [[atomic ring buffer]] |
| Consumer steady drain? | [[Blocking]] producer |
| Memory budget per connection? | OOM under fan-in |
| Durability need? | Large RAM buffer loses data on crash |

Tune with measurement: `strace` syscall counts, drop counters, `perf`.

Related patterns: [[Rolling Buffer]], [[multiple levels of buffering]].

## Sources

- Stevens, *UNIX Network Programming* — socket buffer tuning
- Linux `socket(7)` — SO_SNDBUF, SO_RCVBUF
