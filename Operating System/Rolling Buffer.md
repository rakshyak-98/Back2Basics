[[Operating System]] [[atomic ring buffer]] [[kernel ring buffer]] [[right buffer]] [[buffer]]

# Rolling Buffer

> A rolling buffer overwrites the oldest entries when full — fixed memory for logs, metrics, and telemetry where history beyond N samples is expendable.

```txt
        Rolling Buffer ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Shows you can pick bounded in-memory history with an explicit loss policy

## Sources
- [Wikipedia — Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer) — overview
- Linux kernel ring buffer design discussions (LKML) — deep-dive

## Key Concepts
- **Fixed window:** capacity is constant; oldest data is sacrificed.
- **Policy:** drop-on-full (rolling) vs block-on-full (queue).
- **Mechanics:** usually a circular / [[atomic ring buffer]] layout.
- **Sizing:** [[right buffer]] capacity from acceptable loss horizon.

## Technical Details
- Unlike a blocking queue that stops producers, a **rolling** (circular) design…

- Application log tail in memory
- Metrics dashboards (last 15 minutes)
- Kernel printk before journald ([[kernel ring buffer]])

- Ask: “If I only keep 1 MB of logs, what incidents become unexplainable?”

## Mistakes to Avoid
- **Mistake:** Treating a rolling buffer as durable audit storage
- **Mistake:** Undersizing so that the burst that caused the outage is already …
- **Mistake:** Blocking producers “to be safe” when the product requirement was…

## Pros/Cons or Trade-offs
- **Pro:** Bounded memory; always keeps recent signal.
- **Con:** Silent loss of older history under flood.
- **Trade-off:** larger buffer vs cost of shipping/storing full history.

## Comparison
- vs [[atomic ring buffer]]: atomic ring is the lock-free structure
- vs [[kernel ring buffer]]: kernel’s concrete rolling log for printk.


### Use cases
- `dmesg` / printk ring, APM agents’ in-memory metric windows, and game/network…
