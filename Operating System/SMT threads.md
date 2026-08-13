[[Operating System]] [[Thread]] [[context switching]] [[base clock speed]] [[TDP]]

# SMT threads

> Simultaneous multithreading (Intel Hyper-Threading, AMD SMT) exposes two logical CPUs per physical core — sharing execution units while each has its own architectural state.

The OS schedules [[Thread]]s on **logical processors**; two runnable threads on sibling hyperthreads compete for the same core’s ALUs and caches.

## Implications

- CPU-bound pairs on one core rarely yield 2× throughput — often ~1.2–1.3× depending on workload.
- [[context switching]] between siblings is cheaper than cross-core but still contends.
- Pin latency-sensitive threads to exclusive cores when [[TDP]] and licensing allow.

```bash
lscpu | grep -E 'Thread|Core|Socket'
cat /sys/devices/system/cpu/cpu*/topology/thread_siblings_list
```

## Sources

- Intel 64 Architecture optimization manual — Hyper-Threading
- Wikipedia: [Simultaneous multithreading](https://en.wikipedia.org/wiki/Simultaneous_multithreading)
