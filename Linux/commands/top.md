[[Commands]] [[process]] [[ps]] [[renice]] [[OOM (Linux Out Of Memory)]]

# top

> `top` is a live process monitor — CPU, RAM, and load, refreshing until you quit.

## Mental model

**Say it in one breath:** Header = machine health (load, CPU breakdown, memory); table = who is spending CPU/RAM right now.

```txt
┌─ load avg │ Tasks │ %Cpu(s) │ MiB Mem / Swap ─┐
│  us sy id wa …     total/used/free/buff-cache   │
└────────────────────────────────────────────────┘
 PID USER %CPU %MEM … COMMAND   ← sort with P / M
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Load average** | Runnable + uninterruptible tasks (1/5/15 min) | “Compare load to `nproc`, not to 100%.” |
| --- | --- | --- |
| **`id` idle** | CPU doing nothing | “Busy ≈ `100 - id` (all cores averaged).” |
| **`wa` iowait** | Idle but waiting on disk I/O | “High `wa` → storage, not CPU-bound code.” |
| **`%CPU` > 100** | Multi-core process | “One thread per core can sum past 100%.” |
| **RES vs VIRT** | Real RAM vs virtual mapping | “Chase RES for pressure; ignore scary VIRT.” |
| **Irix mode** | `%CPU` as % of one core vs whole machine | “Know which mode before comparing hosts.” |

### Header fields that matter

| Field | Meaning |
| --- | --- |
| `us` | User-space |
| `sy` | Kernel/system |
| `id` | Idle |
| `wa` | I/O wait |
| `st` | Steal (VM — hypervisor took time) |
| `buff/cache` | Reclaimable page cache — not “used up forever” |

### How engineers drive it

1. **CPU hog** → press `P`
2. **RAM hog / leak** → press `M`
3. **Per-core** → press `1`
4. **Threads** → `H`; tree → `V`
5. **Kill** → `k` → PID → signal (`15` then `9`)
6. **Full command** → `c`

## Standard config / commands

```bash
# Interactive
top

# Batch one shot (scripts / SSH one-liners)
top -bn1 | head -n 20
top -bn1 | grep '%Cpu'

# Focus one process / user
top -p <pid>
top -u <user>

# Related one-liners
mpstat 1
vmstat 1
nproc
ps aux --sort=-%mem | head
ps aux --sort=-%cpu | head
```

### Interactive keys (cheat sheet)

| Key | Action |
| --- | --- |
| `P` / `M` / `N` / `T` | Sort CPU / mem / PID / time |
| `1` | Per-CPU lines |
| `H` / `V` | Threads / process tree |
| `u` / `o` | Filter user / field |
| `k` / `r` | Kill / [[renice]] |
| `d` / Space / `q` | Interval / refresh / quit |
| `c` / `t` / `m` / `l` | Toggle command / CPU / mem / load |

| Knob | Why it matters |

| Refresh `d` | Catch short spikes vs calm steady state |
| --- | --- |
| `H` threads | Java/Node “one PID” hiding a hot TID |
| Batch `-bn1` | Safe in ansible/CI without a TTY UI |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Load high, `%Cpu` idle-ish | `wa`, disk `iostat`, NFS | Fix I/O; load counts `D` state tasks |
| One core 100%, others idle | Press `1`; find PID | Fix single-thread bottleneck / pin |
| `%MEM` high, little `free` | `buff/cache` vs RES of apps | Don’t panic on cache; kill real RSS hogs / check [[OOM (Linux Out Of Memory)]] |
| Process `%CPU` > 100 | Multi-threaded | Expected on multi-core; use `H` for TID |
| VM feels slow, `st` high | Steal time in header | Resize hypervisor / noisy neighbor |
| Need history, not now | `top` alone | Use `sar`, metrics, or `pidstat 1` |

## Gotchas

> [!WARNING]
> **Load ≠ CPU %** — load includes tasks waiting on disk (`D`). A spinning disk can raise load while CPUs look idle.

> [!WARNING]
> **Linux “used” RAM includes cache** — reclaimable `buff/cache` is normal; OOM cares about anon RSS + reclaim failure.

> [!WARNING]
> **Zombies show in task counts** — they are dead waiting for `wait`; don’t “optimize CPU” on `Z`.

> [!WARNING]
> **`htop` is nicer UX** — same ideas; still learn stock `top` for rescue shells and busybox.

## When NOT to use

- **Don’t rely on `top` for multi-day trends** — use Prometheus/Node exporter, `sar`, or cloud metrics.
- **Don’t debug socket/file leaks in `top`** — use [[lsof]] / [[file descriptors]].
- **Don’t renice randomly in production** — document policy; cgroups are the real limiter ([[cgroup (Control Group)]]).

## Related

[[ps]] [[process]] [[Linux process commands]] [[renice]] [[OOM (Linux Out Of Memory)]] [[Memory management]] [[Linux resource management]] [[cgroup (Control Group)]] [[lsof]]
