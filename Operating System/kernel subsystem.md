[[Buffer cache]] [[system call]] [[kernel ring buffer]] [[cgroup (Control Group)]] [[context switching]]

# Kernel subsystem

> Major in-kernel modules (VFS, MM, scheduler, net stack, block layer) that user space reaches only via [[system call]] — **Kerrisk / Love**.

---

## Mental model

The Linux kernel is not one blob — it's **subsystems** with defined boundaries, sharing locks, caches, and the same address space (kernel mode).

```txt
                    user process
                         │ syscalls
    ┌────────────────────┼────────────────────┐
    │                    ▼                    │
    │  ┌─────────┐  ┌──────────┐  ┌─────────┐ │
    │  │ VFS /   │  │ Memory   │  │ Scheduler│ │
    │  │ FS      │  │ (MM)     │  │ (CFS)   │ │
    │  └────┬────┘  └────┬─────┘  └────┬────┘ │
    │       │            │             │      │
    │  [[Buffer cache]]   page cache     runqueue│
    │       │            │             │      │
    │  ┌────┴────────────┴─────────────┴────┐ │
    │  │        Block layer / drivers        │ │
    │  └──────────────────┬─────────────────┘ │
    │                     │                    │
    │  ┌──────────────────┴─────────────────┐ │
    │  │   Network stack (TCP/IP, sockets)   │ │
    │  └────────────────────────────────────┘ │
    │  [[cgroup (Control Group)]] · namespaces │
    └──────────────────────────────────────────┘
```

**How this maps to debugging:**
| Subsystem | You notice when… | First tools |
|-----------|------------------|-------------|
| VFS / FS | wrong file, slow I/O, `EMFILE` | `lsof`, `strace`, `iostat` |
| MM | OOM, swap storm, high `Cached` | `dmesg`, `/proc/meminfo`, cgroup memory |
| Scheduler | run queue latency, stolen time | `perf`, `vmstat`, `pidstat` |
| Network | drops, retrans, listen overflow | `ss`, `tcpdump`, `nstat` |
| Block | iowait, fsync p99 | `iostat -x`, `blktrace` |

**Containers:** cgroups/namespaces hook into these subsystems — limits are **kernel policy**, not Docker magic.

---

## Standard config / commands

### Which subsystem is hot?

```shell
# CPU vs I/O wait
vmstat 1
pidstat -u -r -d 1 -p PID

# Kernel ring buffer — OOM, NIC, FS errors
dmesg -T | tail -50
# or [[kernel ring buffer]] via journalctl -k

# Loaded modules / drivers
lsmod | grep nvme
ls /sys/block/

# Syscall → subsystem guess
strace -c -p PID          # % time in read/write → VFS; sendmsg → net

# Cgroup v2 limits (systemd slice)
systemd-cgtop
cat /sys/fs/cgroup/my.slice/memory.current
```

### Tunables (change with care)

```shell
# VM / page cache writeback
sysctl vm.dirty_ratio vm.swappiness

# Network
sysctl net.core.somaxconn net.ipv4.tcp_max_syn_backlog

# Block scheduler (NVMe often "none")
cat /sys/block/nvme0n1/queue/scheduler
```

**Service angle:**
- **Node/Go/Java** — mostly VFS + net + scheduler; profile before sysctl roulette.
- **Postgres/Redis** — MM + block + fsync path dominate tail latency.
- **K8s pod** — cgroup limits on memory/CPU/pids hit MM and scheduler first.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Random slow requests | `vmstat 1` iowait; `perf top` | Separate disk; tune cache; fix sync I/O in app |
| OOM killed container | `dmesg`; cgroup `memory.events` | Raise limit or fix leak; tune JVM heap vs cgroup |
| TCP resets under load | `ss -s`; `netstat -s` drops | `somaxconn`; app accept rate; [[file descriptors]] |
| Disk full, app hangs | writeback + ENOSPC in dmesg | Free space; quota; rotate logs |
| High steal time (VM) | `top` `%st` | Noisy neighbor; resize instance; dedicated nodes |
| Works as root, not app | capabilities, namespaces | SELinux/AppArmor audit; correct permissions |
| After kernel upgrade, NIC gone | `dmesg`; `modprobe` | DKMS driver rebuild; pin kernel version |

---

## Gotchas

> [!WARNING]
> **Cross-subsystem blame games.** App sees "slow API" — root cause is block layer fsync + another pod's flush storm sharing EBS.

> [!WARNING]
> **Page cache is MM + VFS** — `echo 3 > /proc/sys/vm/drop_caches` is a **debug hammer**, not production tuning — causes latency spike for everyone.

> [!WARNING]
> **Network sysctl without app backlog fix** — raising `somaxconn` alone doesn't help if event loop accepts slower than SYN rate.

> [!WARNING]
> **cgroup v1 vs v2** — memory limits behave differently (swap, OOM order). Mixed hierarchies on old hosts still exist.

> [!WARNING]
> **eBPF/bpf** hooks subsystems dynamically — great for observability; bad BPF can panic kernel (test on canary).

---

## When NOT to use

- Don't treat "kernel subsystem" as something you micro-manage daily — fix app + config first, kernel tunables second, custom modules last.
- Don't load out-of-tree drivers on production without rollback kernel.

---

## Related

[[system call]] [[Buffer cache]] [[kernel ring buffer]] [[cgroup (Control Group)]] [[context switching]] [[file descriptors]] [[fsync]] [[IPC namespace]]
