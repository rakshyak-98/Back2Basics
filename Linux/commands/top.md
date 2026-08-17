[[Commands]] [[process]] [[ps]] [[renice]] [[OOM (Linux Out Of Memory)]] [[Memory management]] [[Linux resource management]] [[lsof]]

# top

> Live process monitor — CPU, RAM, and load, refreshing until you quit.





## Interview Relevance
Tests load average vs CPU %, iowait (`wa`), RES vs VIRT, and whether you sort with `P`/`M` instead of guessing.

## Sources
- [man top](https://man7.org/linux/man-pages/man1/top.1.html) — deep-dive
- [Wikipedia — top (software)](https://en.wikipedia.org/wiki/Top_(software)) — overview

## Key Concepts
- **Load average:** runnable + uninterruptible tasks (1/5/15 min) — compare to `nproc`, not to “100%.”
- **`id` / `wa` / `st`:** idle, I/O wait, steal (hypervisor) — diagnose CPU-bound vs disk vs noisy neighbor.
- **RES vs VIRT:** chase RES for pressure; scary VIRT is often mappings.
- **`%CPU` > 100:** multi-threaded process summing cores.
- **Irix mode:** `%CPU` as % of one core vs whole machine — know the mode before comparing hosts.

## Technical Details
```txt
┌─ load avg │ Tasks │ %Cpu(s) │ MiB Mem / Swap ─┐
│  us sy id wa …     total/used/free/buff-cache   │
└────────────────────────────────────────────────┘
 PID USER %CPU %MEM … COMMAND   ← sort with P / M
```

| Field | Meaning |
|-------|---------|
| `us` | User-space |
| `sy` | Kernel/system |
| `id` | Idle |
| `wa` | I/O wait |
| `st` | Steal (VM) |
| `buff/cache` | Reclaimable page cache |

Drive it: `P` CPU hog → `M` RAM hog → `1` per-core → `H` threads → `k` kill → `c` full command.

```bash
top
top -bn1 | head -n 20
top -p <pid>
top -u <user>
mpstat 1
vmstat 1
nproc
```

| Key | Action |
|-----|--------|
| `P` / `M` / `N` / `T` | Sort CPU / mem / PID / time |
| `1` | Per-CPU lines |
| `H` / `V` | Threads / process tree |
| `k` / `r` | Kill / [[renice]] |
| `d` / Space / `q` | Interval / refresh / quit |

| Symptom | Check | Fix |
|---------|-------|-----|
| Load high, CPU idle-ish | `wa`, `iostat`, NFS | Fix I/O; load counts `D` state |
| One core 100%, others idle | Press `1` | Single-thread bottleneck |
| `%MEM` high, little `free` | `buff/cache` vs RES | Don’t panic on cache; check [[OOM (Linux Out Of Memory)]] |
| VM slow, `st` high | Steal in header | Resize hypervisor / noisy neighbor |

## Real-World Applications
Live incident triage on a SSH session, batch `-bn1` in Ansible one-liners, and spotting steal time on noisy cloud neighbors.

## Pros/Cons or Trade-offs
- **Pro:** Always available in rescue shells; interactive sorting.
- **Con:** Not a multi-day trend tool — use `sar`/metrics for history.

## Comparison
- vs [[ps]]: snapshot vs live refresh.
- vs `htop`: nicer UX; still learn stock `top` for busybox/rescue.

## Mistakes to Avoid
- Equating load with CPU % — disk wait raises load while CPUs look idle.
- Panicking because “used” RAM includes reclaimable cache.
- Renicing randomly in production — cgroups are the real limiter.
