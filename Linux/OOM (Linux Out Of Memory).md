[[Memory management]] [[Linux cgroup]] [[Linux out of memory daemon]] [[process]]

# OOM (Linux Out Of Memory)

> One-line: when the kernel **cannot reclaim enough RAM**, it kills processes to keep the system alive — global OOM killer, cgroup limits, or `systemd-oomd`. **Kerrisk + container on-call.**

## Mental model

Memory is not “free RAM = 0”. The kernel uses page cache aggressively. OOM fires when **allocation cannot succeed** after reclaim (swap, drop cache, shrink slabs) — not simply when `free` looks low.

```
malloc/page fault ──► reclaim (cache, swap) ──► still fail?
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
      cgroup memory.max   systemd-oomd    global OOM killer
      (kill in cgroup)    (pressure kill)  (pick process system-wide)
```

| Mechanism | Scope | Chooses victim by |
|-----------|-------|-------------------|
| Global OOM killer | Whole machine | `oom_score` / `oom_score_adj`, memory footprint, child tree |
| cgroup v2 `memory.max` | Cgroup (container/pod) | First process in cgroup over limit — often PID 1 in container |
| `systemd-oomd` | Managed cgroups | Memory pressure metrics → kills cgroup ([[Linux out of memory daemon]]) |
| `memory.high` (v2) | Throttle before hard kill | Slows allocator; may avoid OOM if tuned |

## Standard config / commands

```bash
# Did OOM happen?
dmesg -T | grep -iE 'out of memory|Killed process|oom-kill'
journalctl -k -b | grep -i oom
# Typical signature:
# oom-kill:constraint=CONSTRAINT_NONE ... task=java,pid=1234,uid=1000
# Out of memory: Killed process 1234 (java) total-vm:8388608kB, anon-rss:4194304kB

# Current memory picture
free -h
cat /proc/meminfo | grep -E 'MemAvailable|SwapFree|Dirty'
vmstat 1 5

# Per-process OOM preference (-1000 = never, +1000 = first)
cat /proc/<pid>/oom_score
cat /proc/<pid>/oom_score_adj    # writable: -1000..1000 (root)
# Production pattern: protect sshd, etcd, database
echo -17 | sudo tee /proc/<sshd-pid>/oom_score_adj   # or systemd OOMScoreAdjust=

# cgroup v2 limits (container / systemd slice)
cat /sys/fs/cgroup/<path>/memory.max      # "max" = unlimited
cat /sys/fs/cgroup/<path>/memory.current
cat /sys/fs/cgroup/<path>/memory.high     # soft throttle threshold
cat /sys/fs/cgroup/<path>/memory.events   # oom_kill, max, high events

# Find a pod/container cgroup (k8s node)
systemd-cgls | grep kubepods
cat /sys/fs/cgroup/kubepods.slice/kubepods-burstable.slice/pod<pod-uid>/memory.max

# systemd unit protection
systemctl show myservice -p OOMScoreAdjust,MemoryMax,MemoryHigh
```

**Kubernetes / container interaction:**

| Layer | What kills you |
|-------|----------------|
| Pod `memory.limits` | cgroup `memory.max` → **OOMKill** in container (often exit 137) |
| Node pressure | kubelet eviction → pod delete before kernel OOM |
| Node kernel OOM | Random host process — **never rely on this for isolation** |
| JVM / Go heap | In-container OOM before cgroup if heap > limit misconfigured |

```bash
# Exit 137 = 128 + 9 (SIGKILL) — classic cgroup OOM
kubectl describe pod <pod> | grep -A5 OOMKilled
crictl inspect <container-id> | jq .info.runtimeSpec.linux.resources.memory
```

**Avoid / mitigate (in order of leverage):**

1. **Right-size limits** — `memory.max` below working set = guaranteed OOMKill.
2. **`oom_score_adj`** — protect infra daemons; never set database to -1000 on shared nodes without understanding swapless starvation.
3. **Swap** — delays global OOM; can hide pressure (latency cliff). Containers often run swapless by design.
4. **`memory.high` + pressure** — throttle before kill (v2 + systemd-oomd).
5. **App fixes** — leaks, unbounded caches, fork bombs.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Process vanished, exit 137 | `dmesg`; `kubectl describe pod` | Raise limit or reduce working set; fix leak |
| Host sluggish then random deaths | `dmesg oom-kill`; `ps aux --sort=-%mem \| head` | Kill/runaway consumer; add RAM; tune services |
| Container dies, node “fine” | `memory.events` oom_kill in pod cgroup | JVM `-XX:MaxRAMPercentage`; app cache caps |
| OOM but `free` shows GB free | `MemAvailable`; slab: `sudo slabtop` | Unreclaimable slab / cache accounting; cgroup limit not global free |
| Database killed, app servers live | `oom_score_adj`; who used most anon-rss | Lower app scores or isolate DB on dedicated node/slice |
| Repeated OOM same PID | `pmap -x`; heap profilers | Memory leak; restart policy masks root cause |
| systemd-oomd killed slice | `journalctl -u systemd-oomd` | Adjust `ManagedOOMSwap=`, `ManagedOOMMemoryPressure=` |

**Incident playbook (first 10 minutes):**

1. **Confirm OOM** — `dmesg -T | tail -100`, not just “process gone”.
2. **Identify victim + constraint** — global vs cgroup (`oom-kill:constraint=...` in dmesg).
3. **Find hog** — `ps -eo pid,user,rss,cmd --sort=-rss | head -20`.
4. **Stabilize** — restart victim with limit; optionally `echo 3 > /proc/sys/vm/drop_caches` **only** if you know cache pressure (never substitute for fixing hog).
5. **Protect blast radius** — `MemoryMax` on slice; move critical workloads; adjust `oom_score_adj`.
6. **Post-incident** — graph RSS vs limit; enable OOM metrics (cAdvisor, node_exporter `node_vmstat_oom_kill`).

## Gotchas

> [!WARNING]
> **`oom_score_adj = -1000` on shared nodes** can cause OOM to kill *everything else* including sshd — lockout risk during memory storms.

> [!WARNING]
> **Pod limit ≠ JVM default heap.** Java 8 defaults ignored cgroup; use container-aware flags or get OOMKill at ~limit while `free` looks OK inside namespace.

- **Child inherits `oom_score_adj`** — wrapper scripts affect scoring tree.
- **Elasticsearch / mmap** — high virtual size in dmesg; victim selection uses rss/swapability, not VSS alone.
- **Swap enabled on kube nodes** — masks pressure; kubelet may not evict until too late.
- **`dmesg` rotated away** — use `journalctl -k --since today`; ship kernel logs to central store.

## When NOT to use

- **“Just add swap” as sole fix for prod OOM** — swaps latency for survival; databases and latency-sensitive services suffer.
- **Disabling OOM killer** — `panic_on_oom=2` panics host; `oom_kill_allocating_task` is niche — understand before tuning.
- **Treating `free -m` zero as emergency** — Linux uses RAM for cache; watch `MemAvailable`.

## Related

[[Memory management]] [[Linux cgroup]] [[Linux out of memory daemon]] [[process]] [[renice]]
