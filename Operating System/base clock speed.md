[[SMT threads]] [[system bus]] [[TDP]] [[CPU IO Bound Task]]

# Base clock speed

> Minimum guaranteed operating frequency (GHz) under nominal thermal/power spec — not the same as turbo/boost peak.

---

## Mental model

CPUs advertise **base clock** (guaranteed all-core floor under TDP) and **max turbo** (short-burst peak on few cores):

```txt
Marketing label          Reality under load
────────────────         ──────────────────
"3.2 GHz base"      →    all cores ≥ 3.2 GHz if cooling/TDP allows
"5.0 GHz boost"     →    1–2 cores briefly; drops as power/thermal limits hit
```

**Effective frequency** varies with:
- Workload (AVX-512 draws more power → lower clock)
- [[TDP]] and cooling
- `intel_pstate` / `amd-pstate` governor
- Container CPU quota (cfs bandwidth)

**Service impact:** latency-sensitive single-thread work cares about **turbo**; batch/parallel work cares about ** sustained all-core frequency** and memory bandwidth ([[system bus]]).

---

## Standard config / commands

### Read current vs base frequency

```bash
lscpu | grep -E 'MHz|Model name|CPU max|CPU min'
watch -n1 'grep MHz /proc/cpuinfo | head'

# Detailed (if turbostat available)
sudo turbostat --Summary --show Core,CPU,Avg_MHz,Busy% --interval 1
```

### Governors

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
# performance | powersave | schedutil

echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
# Latency-sensitive bare metal — higher power bill
```

### Container CPU limits

```bash
# cgroup v2 cpu.max — quota affects effective MHz
cat /sys/fs/cgroup/myapp/cpu.max
```

**Why `performance` governor:** reduces frequency transition latency for trading/ad-tech style tail-SLA services — not default for cloud cost optimization.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Slower than "spec sheet" | Thermal throttle; `dmesg \| grep -i throttle` | Improve cooling; reduce AVX load; spread jobs |
| Variable benchmark results | Turbo + governor | Pin governor; disable turbo in BIOS for reproducibility |
| Container "3 GHz" but sluggish | CPU quota throttling | Raise `cpu.max`; check `cpu.stat` `nr_throttled` |
| All-core boost never hits | Power limit PL1/PL2 | Datacenter power cap; BIOS limits |

---

## Gotchas

> [!WARNING]
> **GHz across vendors ≠ IPC** — compare benchmarks for your workload, not clock alone.

> [!WARNING]
> **Hypervisor steals cycles** — stolen time in `top`/`vmstat` on VMs; frequency may look fine while effective CPU is low.

> [!WARNING]
> **`/proc/cpuinfo` MHz is instantaneous** — sample over time for capacity planning.

---

## When NOT to use

Don't buy CPUs on base clock alone for **parallel batch** — core count, cache, and memory channels often dominate. For **single-thread** latency, prioritize turbo behavior and cache.

---

## Related

[[TDP]] [[SMT threads]] [[system bus]] [[context switching]] [[CPU IO Bound Task]]
