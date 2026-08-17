[[Operating System]] [[Thread]] [[context switching]] [[base clock speed]] [[TDP]]

# SMT threads

> Simultaneous multithreading (Intel Hyper-Threading, AMD SMT) exposes two logical CPUs per physical core — sharing execution units while each keeps its own architectural state.

```txt
        SMT threads ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Capacity and latency reviews: logical CPUs ≠ 2× throughput

## Sources
- Intel 64 Architecture optimization manual — Hyper-Threading — deep-dive
- [Wikipedia — Simultaneous multithreading](https://en.wikipedia.org/wiki/Simultaneous_multithreading) — overview

## Key Concepts
- **Logical processors:** OS sees more CPUs than physical cores.
- **Shared resources:** ALUs, caches, and pipelines contended by sibling threads.
- **Typical gain:** CPU-bound pairs often ~1.2–1.3×, not 2×.
- **Isolation:** pin latency-sensitive work away from noisy siblings when [[TDP]]/licensing al…

## Technical Details
- The OS schedules [[Thread]]s on logical processors

```bash
lscpu | grep -E 'Thread|Core|Socket'
cat /sys/devices/system/cpu/cpu*/topology/thread_siblings_list
```

- [[context switching]] between siblings is cheaper than cross-core but still c…
- Frequency interacts with [[base clock speed]] and thermal limits.

## Mistakes to Avoid
- **Mistake:** Doubling thread-pool size because `nproc` doubled under SMT and …
- **Mistake:** Ignoring sibling topology when pinning threads for latency SLOs
- **Mistake:** Comparing benchmarks with turbo/SMT mixed across runs

## Pros/Cons or Trade-offs
- **Pro:** Extra logical CPUs cheaply hide some stalls.
- **Con:** Unpredictable contention; security side-channel considerations in multi-tenant hosts.
- **Trade-off:** max throughput vs tail latency / isolation.

## Comparison
- vs physical cores: true parallel execution units vs time-sharing one core’s pipes.
- vs [[multi-threaded]] software: SMT is hardware; software threads exist with or without SMT.


### Use cases
- HPC and trading systems sometimes disable SMT for jitter
