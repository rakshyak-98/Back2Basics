[[Operating System]] [[Thread]] [[context switching]] [[base clock speed]] [[TDP]]

# SMT threads

> Simultaneous multithreading (Intel Hyper-Threading, AMD SMT) exposes two logical CPUs per physical core — sharing execution units while each keeps its own architectural state.

## Interview Relevance

Capacity and latency interviews: logical CPUs ≠ 2× throughput; know when to disable SMT or pin exclusive cores for tail latency.

## Sources

- Intel 64 Architecture optimization manual — Hyper-Threading — deep-dive
- [Wikipedia — Simultaneous multithreading](https://en.wikipedia.org/wiki/Simultaneous_multithreading) — overview

## Key Concepts

- **Logical processors:** OS sees more CPUs than physical cores.
- **Shared resources:** ALUs, caches, and pipelines contended by sibling threads.
- **Typical gain:** CPU-bound pairs often ~1.2–1.3×, not 2×.
- **Isolation:** pin latency-sensitive work away from noisy siblings when [[TDP]]/licensing allow.

## Technical Details

The OS schedules [[Thread]]s on logical processors; two runnable threads on sibling hyperthreads compete for the same core.

```bash
lscpu | grep -E 'Thread|Core|Socket'
cat /sys/devices/system/cpu/cpu*/topology/thread_siblings_list
```

[[context switching]] between siblings is cheaper than cross-core but still contends for execution resources. Frequency interacts with [[base clock speed]] and thermal limits.

## Real-World Applications

HPC and trading systems sometimes disable SMT for jitter. Throughput-oriented web workers often leave SMT on and size pools from measured gain.

## Pros/Cons or Trade-offs

- **Pro:** Extra logical CPUs cheaply hide some stalls.
- **Con:** Unpredictable contention; security side-channel considerations in multi-tenant hosts.
- **Trade-off:** max throughput vs tail latency / isolation.

## Comparison

- vs physical cores: true parallel execution units vs time-sharing one core’s pipes.
- vs [[multi-threaded]] software: SMT is hardware; software threads exist with or without SMT.

## Mistakes to Avoid

- Doubling thread-pool size because `nproc` doubled under SMT and expecting 2× QPS.
- Ignoring sibling topology when pinning threads for latency SLOs.
- Comparing benchmarks with turbo/SMT mixed across runs.
