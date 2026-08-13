[[Operating System]] [[atomic ring buffer]] [[kernel ring buffer]] [[right buffer]] [[buffer]]

# Rolling Buffer

> A rolling buffer overwrites the oldest entries when full — fixed memory for logs, metrics, and telemetry where history beyond N samples is expendable.

Unlike a blocking queue that stops producers, a **rolling** (circular) design keeps the most recent window. Implementation matches [[atomic ring buffer]] mechanics with policy: drop-on-full versus block-on-full.

## Uses

- Application log tail in memory
- Metrics dashboards (last 15 minutes)
- Kernel printk before journald ([[kernel ring buffer]])

Choose [[right buffer]] capacity from acceptable loss horizon — “if I only keep 1 MB of logs, what incidents become unexplainable?”

## Sources

- Wikipedia: [Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer)
- Linux kernel ring buffer design discussions (LKML)
