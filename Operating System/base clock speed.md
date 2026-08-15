[[Operating System]] [[SMT threads]] [[TDP]] [[CPU IO Bound Task]] [[context switching]] [[cgroup (Control Group)]] [[disk IOPS]] [[mutexes]]

# Base clock speed

> Base clock speed is the guaranteed steady-state frequency of a CPU core under nominal thermal and power limits — not the short turbo burst in marketing slides.

## Interview Relevance

Capacity planning: base vs turbo, why sustained all-core load settles near base, and how cgroup CPU limits interact with hardware P-states.

## Sources

- Intel® 64 Architecture Software Developer’s Manual — power management — deep-dive
- [Linux kernel docs — CPUFreq](https://docs.kernel.org/admin-guide/pm/cpufreq.html) — deep-dive
- [Wikipedia — Dynamic frequency scaling](https://en.wikipedia.org/wiki/Dynamic_frequency_scaling) — overview

## Key Concepts

- **Base vs turbo:** certified sustained vs opportunistic boost.
- **Governors / P-states:** OS + hardware choose frequency within [[TDP]] / PL limits.
- **Workload fit:** I/O-bound services rarely need peak GHz ([[CPU IO Bound Task]]).
- **Shared core:** [[SMT threads]] share frequency and cache budget.

## Technical Details

```txt
Workload demand → OS scheduler places threads on cores
                → hardware P-states / CPPC choose frequency
                → thermal and power limits (TDP, PL1/PL2) cap or throttle
```

Linux: `cpufreq` governors (`performance`, `powersave`, `schedutil`), `/proc/cpuinfo`, `turbostat`. [[cgroup (Control Group)]] CPU quotas limit effective compute even when hardware could turbo higher.

[[context switching]] overhead remains regardless of GHz. Memory latency, [[disk IOPS]], and [[mutexes]] contention still dominate many profiles.

## Real-World Applications

Choosing instance types, explaining “same CPU slower in production,” and setting `cpufreq` policy on latency-sensitive hosts.

## Pros/Cons or Trade-offs

- **Higher base:** predictable sustained throughput; more power/cooling.
- **Aggressive turbo marketing:** great for short bursts; misleading for 24/7 load.
- **Trade-off:** `performance` governor latency vs power/heat.

## Comparison

- vs [[TDP]]: TDP is the thermal budget; base clock is the frequency claim inside that budget.
- vs software concurrency: frequency helps single-thread work; it does not fix I/O waits.

## Mistakes to Avoid

- Sizing fleets from single-core turbo screenshots.
- Ignoring thermal throttle when comparing laptop vs server numbers.
- Expecting more GHz to fix lock-contended or disk-bound services.
