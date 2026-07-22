[[Thread]] [[context switching]] [[multi-threaded]] [[SMT threads]] [[cgroup (Control Group)]]

# Context switching

> Save running thread's CPU state, restore another's, resume execution — **scheduler tax on throughput and tail latency**.

---

## Mental model

A **context switch** happens when the CPU stops running thread A and runs thread B:

```txt
Thread A running on CPU 2
        │
   timer interrupt / syscall block / preemption
        │
   kernel saves: registers, PC, SP, thread-local state
        │
   pick next runnable thread (CFS runqueue)
        │
   restore Thread B state → B runs on CPU 2
```

**What gets saved:** general registers, program counter, stack pointer, kernel stack pointer, MMU state if address space changes (**process switch** heavier than **thread switch** within same process).

**Costs:**
- **Direct:** microseconds — save/restore, scheduler logic, TLB shootdown if ASID changes.
- **Indirect:** cold CPU caches and branch predictors — the real killer for HPC and lock-heavy Java services.

**When switches happen:**
- Time slice expired (CFS `sched_latency`).
- Blocking syscall (`read`, `mutex`, `futex`).
- Voluntary yield / `sched_yield`.
- Preemption of long-running kernel work (config dependent).

**SMT ([[SMT threads]]):** two logical CPUs share one core — switching between siblings is cheaper than cross-core, but still contends execution units.

---

## Standard config / commands

### Measure switching

```shell
# Context switches per second (whole machine)
vmstat 1
# cs column — compare idle vs load

pidstat -w 1 -p PID    # voluntary vs non-voluntary cswitch/s per thread

# perf scheduler events
perf stat -e context-switches,cpu-migrations -p PID -- sleep 5

# Run queue latency (scheduler backlog signal)
perf sched record -p PID -- sleep 10
perf sched latency
```

### Reduce unnecessary switches (design level)

| Pattern | Switch pressure |
|---------|-----------------|
| Thread per request × 10k RPS | High — prefer pool [[thread pool]] |
| Blocking I/O on thread pool | Blocks worker → switch → wake |
| Event loop + non-blocking [[non-blocking]] | Low switches, few threads |
| Spin + mutex contention | Switches + wasted CPU |

```shell
# CPU affinity (pin critical thread — use sparingly)
taskset -cp 2,3 PID

# Cgroup CPU quota forces throttling → more switches
cat /sys/fs/cgroup/.../cpu.max
```

**Node:** single main thread — low **thread** switching; still kernel switches for async I/O completion.

**Go:** GOMAXPROCS threads vs goroutines — M:N scheduler multiplexes many goroutines onto fewer OS threads.

**Java:** massive thread pools (Tomcat 500 threads) → measurable `cs` in `vmstat` under load.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Throughput drops as threads ↑ | `pidstat -w`; `perf stat cs` | Reduce threads; pool size ≈ cores × (1–2); profile locks |
| p99 latency spikes, moderate CPU | run queue; `perf sched latency` | Fewer runnable threads; fix lock contention; faster I/O |
| `cs` rate explodes | `vmstat 1` | Stop busy-wait; fix thundering herd on wake |
| One core hot, others idle | affinity; Go GOMAXPROCS | Rebalance; check accidental single-threaded bottleneck |
| Container throttled | cgroup `cpu.stat` nr_throttled | Raise quota or reduce work; bursts cause switch storms |
| After deploy, worse latency | more threads in new version | Diff pool settings; compare `pidstat -w` |
| High involuntary switches | CPU oversubscription | Reduce competing pods; right-size VM |

---

## Gotchas

> [!WARNING]
> **More threads ≠ more speed** past core count — coordination overhead and context switches dominate.

> [!WARNING]
> **False sharing + mutex** — not a "switch" bug, but looks like scheduler noise in profiles — cache line ping-pong between cores.

> [!WARNING]
> **Priority inversion** — high-priority thread runnable but not scheduled because medium threads hold CPU; see [[mutexes]].

> [!WARNING]
> **NUMA:** cross-node memory access + migration `cpu-migrations` in `perf stat` — pin memory and threads together for DB backends.

> [!WARNING]
> **strace in prod** — every syscall stops process → massive artificial switching — use BPF/off-CPU profiles instead.

**Cloud steal time:** hypervisor preempts your vCPU — looks like involuntary switches in guest; fix is bigger instance or dedicated host.

---

## When NOT to use

- Don't pin every thread to cores "for performance" without measurement — often hurts scheduler load balance.
- Don't confuse **goroutine/co-routine** scheduling with OS context switch — profile the right layer.

---

## Related

[[Thread]] [[mutexes]] [[thread pool]] [[non-blocking]] [[SMT threads]] [[CPU IO Bound Task]] [[cgroup (Control Group)]] [[kernel subsystem]]
