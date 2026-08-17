[[Operating System]] [[buffer]] [[buffer head]] [[buffer flags]] [[Buffer cache]] [[multiple levels of buffering]] [[fsync]]

# Buffer lifecycle

> A kernel or application buffer moves through allocate → fill → optionally dirty → flush → reclaim — each step fails differently if the next stage is slower than the producer.





## Interview Relevance
Design-review prompt: power loss mid-lifecycle, which layer blocks the producer when full, and whether buffered bytes are bounded (backpressure).

## Sources
- Linux kernel: `mm/page-writeback.c`, block layer writeback — deep-dive
- Robert Love, *Linux Kernel Development* — deep-dive
- Tanenbaum, *Modern Operating Systems* — I/O and buffering — overview

## Recall Cues
- Why do interviewers care about Design-review prompt: power loss mid-lifecycle, which layer blocks the producer when full, and whether buffered bytes are bounded (backpressure)?
- What is step 1: Allocate buffer head + attach to page ([[buffer head]])?
- What is step 3: Background or explicit flush schedules I/O toward disk?
- What is step 4: I/O completion clears dirty, unlocks?
- What is step 5: Page reclaimed under memory pressure if clean?
- What mistake is **Unbounded dirty memory without backpressure**?
- What mistake is **Equating `fflush` with disk durability**?
- What mistake is **Discarding dirty pages as if they were clean cache**?

## Technical Details
```txt
1. Allocate buffer head + attach to page ([[buffer head]])
2. Read or write fills memory — set uptodate / dirty ([[buffer flags]])
3. Background or explicit flush schedules I/O toward disk
4. I/O completion clears dirty, unlocks
5. Page reclaimed under memory pressure if clean
```

[[multiple levels of buffering]]: `fflush()` does not [[fsync]]; TCP `close()` does not guarantee the peer persisted data.

Clean [[Buffer cache]] pages are cheap to drop. Dirty pages must be written carefully — writeback throttling prevents flooding slow disks. Under OOM, prefer dropping cache before killing processes.

## Mistakes to Avoid
- Unbounded dirty memory without backpressure.
- Equating `fflush` with disk durability.
- Discarding dirty pages as if they were clean cache.

## Comparison
- vs [[buffer]]: buffer is the object; lifecycle is its state machine over time.
- vs [[fsync]]: fsync forces a late lifecycle stage for durability.

## Real-World Applications
Tuning dirty ratios, diagnosing writeback storms, and designing app-level flush policies for logs and databases.

## Pros/Cons or Trade-offs
- **Pro:** Predictable stages make failure modes discussable.
- **Con:** Easy to “flush” the wrong layer and believe you are durable.
- **Trade-off:** aggressive writeback (lower peak dirty) vs bursty disk load.
