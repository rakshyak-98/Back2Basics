[[Operating System]] [[Thread]] [[multi-threaded]] [[CPU IO Bound Task]]

# SMT threads

> SMT (Simultaneous Multithreading) runs two+ hardware threads on one core — Intel Hyper-Threading is the common name.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** One core shares ALUs/caches across logical CPUs; when one thread stalls on memory, the sibling can use the execution units.

```txt
Physical core
├─ logical CPU0  (thread A)
└─ logical CPU1  (thread B)  ← SMT sibling
     shared: L1/L2, execution ports
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **SMT** | Simultaneous multithreading | “Two threads share one core’s pipelines.” |
| **Hyper-Threading** | Intel’s SMT brand | “`nproc` doubles vs physical cores.” |
| **Logical CPU** | What the OS schedules on | “Appears as an extra core in `/proc/cpuinfo`.” |
| **Sibling** | Pair sharing a core | “Pinning both heavy jobs here hurts.” |
| **Throughput vs latency** | More work vs jitter | “SMT helps throughput; can hurt tail latency.” |
| **Disable SMT** | Firmware/OS toggle | “Security / HPC isolation choice.” |

### How the story goes

1. **Enumerate** — topology: cores versus threads.
2. **Schedule** — OS places tasks on logical CPUs.
3. **Contend** — siblings fight for caches/ports under load.
4. **Tune** — pin, or turn SMT off for noisy/sensitive workloads.

---

## Standard config / commands

```bash
lscpu -e
lscpu | egrep 'Thread|Core|Socket|CPU\(s\)'
cat /sys/devices/system/cpu/cpu0/topology/thread_siblings_list
# Temporarily offline SMT siblings (example — verify siblings first)
# echo 0 | sudo tee /sys/devices/system/cpu/cpuX/online
```

| Knob | Why it matters |
|------|----------------|
| BIOS SMT on/off | Global policy |
| `taskset` / cpuset | Keep hot pairs apart |
| `isolcpus` | Dedicated cores for latency |
| Power governor | Turbo + SMT interaction |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 2× CPUs but ~1.2× speedup | Sibling contention | Measure with SMT off; pin one thread/core |
| Tail latency spikes | Noisy sibling | Isolate cores; disable SMT |
| Security worry (L1TF etc.) | Kernel mitigations | Patches; consider SMT off in multi-tenant |
| Wrong capacity planning | Counted logical as physical | Size on cores, not `nproc` alone |
| Pinning “all CPUs” | Includes siblings | Use core-aware topology |
| Perf counters weird | Shared PMU | Account for SMT sharing |

---

## Gotchas

> [!WARNING]
> **`nproc` lies for capacity** — 16 logical ≠ 16 full cores of ALUs.

> [!WARNING]
> **Cache side channels** — co-tenants on siblings share microarchitecture.

> [!WARNING]
> **Licensing / K8s** — some products charge per thread; know what you expose.

> [!WARNING]
> **Offlining CPUs** — do it carefully; don’t offline the boot CPU wrongly.

---

## When NOT to use

- **Hard realtime / ultra-low jitter** — prefer SMT off + isolated cores.
- **Strict multi-tenant crypto** — many policies disable SMT.
- **Single heavy SIMD loop** — sibling often steals bandwidth; dedicate the core.

---

## Related

[[Thread]] [[multi-threaded]] [[CPU IO Bound Task]] [[Single Instruction, Multiple Data (SIMD)]] [[base clock speed]] [[TDP]]
