[[Operating System]] [[SMT threads]] [[TDP]] [[CPU IO Bound Task]] [[context switching]]

# Base clock speed

> Base clock speed is the guaranteed steady-state frequency of a CPU core under nominal thermal and power limits — not the short turbo burst you see in marketing.

Modern processors expose **base** and **maximum turbo** frequencies (GHz). The **base clock** is the speed the vendor certifies when all cores run a typical workload within thermal design power ([[TDP]]). Turbo raises frequency when headroom exists; under sustained load the core often settles near base or an intermediate all-core frequency.

## What actually sets frequency

```txt
Workload demand → OS scheduler places threads on cores
                → hardware P-states / CPPC choose frequency
                → thermal and power limits (TDP, PL1/PL2) cap or throttle
```

Linux exposes this through `cpufreq` governors (`performance`, `powersave`, `schedutil`), `/proc/cpuinfo`, and tools like `turbostat`. Container CPU quotas ([[cgroup (Control Group)]]) limit effective compute even when the hardware could turbo higher.

## Why it matters for systems work

- **[[CPU IO Bound Task]]** — an I/O-bound service rarely needs peak GHz; wrong-sizing leads to paying for idle turbo headroom.
- **[[context switching]]** — higher frequency reduces time per quantum but does not remove scheduler overhead.
- **[[SMT threads]]** — two logical CPUs share one core’s execution units; both compete for the same frequency and cache budget.

Base clock is a hardware specification; observed performance still depends on memory latency, disk ([[disk IOPS]]), and lock contention ([[mutexes]]).

## Sources

- Intel® 64 Architecture Software Developer’s Manual — power management
- Linux kernel documentation: [CPUFreq](https://docs.kernel.org/admin-guide/pm/cpufreq.html)
- Wikipedia: [CPU multiplier](https://en.wikipedia.org/wiki/CPU_multiplier), [Dynamic frequency scaling](https://en.wikipedia.org/wiki/Dynamic_frequency_scaling)
