[[Operating System]] [[buffer]] [[buffer head]] [[buffer flags]] [[Buffer cache]] [[multiple levels of buffering]] [[fsync]]

# Buffer lifecycle

> A kernel or application buffer moves through allocate → fill → optionally dirty → flush → reclaim — each step fails differently if the next stage is slower than the producer.

```txt
        Buffer lifecycle ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Design-review prompt: power loss mid-lifecycle, which layer blocks the produc…

## Sources
- Linux kernel: `mm/page-writeback.c`, block layer writeback — deep-dive
- Robert Love, *Linux Kernel Development* — deep-dive
- Tanenbaum, *Modern Operating Systems* — I/O and buffering — overview

## Technical Details
```txt
1. Allocate buffer head + attach to page ([[buffer head]])
2. Read or write fills memory — set uptodate / dirty ([[buffer flags]])
3. Background or explicit flush schedules I/O toward disk
4. I/O completion clears dirty, unlocks
5. Page reclaimed under memory pressure if clean
```

- [[multiple levels of buffering]]: `fflush()` does not [[fsync]]

- Clean [[Buffer cache]] pages are cheap to drop.
- Dirty pages must be written carefully
- Under OOM, prefer dropping cache before killing processes.

## Mistakes to Avoid
- **Mistake:** Unbounded dirty memory without backpressure
- **Mistake:** Equating `fflush` with disk durability
- **Mistake:** Discarding dirty pages as if they were clean cache

## Pros/Cons or Trade-offs
- **Pro:** Predictable stages make failure modes discussable.
- **Con:** Easy to “flush” the wrong layer and believe you are durable.
- **Trade-off:** aggressive writeback (lower peak dirty) vs bursty disk load.

## Comparison
- vs [[buffer]]: buffer is the object; lifecycle is its state machine over time.
- vs [[fsync]]: fsync forces a late lifecycle stage for durability.


### Use cases
- Tuning dirty ratios, diagnosing writeback storms, and designing app-level flu…
