[[process]] [[Linux Process Theory]] [[Linux resource management]] [[OOM (Linux Out Of Memory)]]

# renice

> One-line: **Adjust CPU scheduling priority of running processes** — give batch jobs less CPU or unstick a critical worker without reboot. Nice only affects **CPU**; not I/O, not memory, not realtime.

## Mental model

Linux CFS scheduler uses **nice** (-20 to 19) as a weight hint: lower number = more CPU time when contended. Default nice is 0. **`renice` changes running processes**; `nice` launches new ones. Root can lower nice (raise priority); unprivileged users can only increase nice (be nicer to others).

```
CPU contention → scheduler picks lower nice first
renice +10 batch_job  →  interactive shell stays snappy
nice -n 19 cpu_hog    →  start heavy job deprioritized
```

| Range | Who can set | Effect |
|-------|-------------|--------|
| -20 to -1 | root (CAP_SYS_NICE) | Higher CPU priority |
| 0 | default | Normal |
| 1 to 19 | any user (own processes) | Lower CPU priority |

**Separate knobs:** `ionice` for disk; `chrt` for realtime scheduling; cgroups for hard limits ([[Linux cgroup]]).

## Standard config / commands

```bash
# Lower priority of running PID (root)
sudo renice -n 10 -p 12345

# Multiple PIDs
sudo renice -n 5 -p 1234 -p 5678

# By user — all their processes
sudo renice -n 15 -u batchuser

# Verify
ps -o pid,ni,comm,args -p 12345
top -o NI    # sort by nice in top

# Start new process with nice (not renice)
nice -n 19 ./long_running_job.sh

# Negative nice (higher priority) — root only
sudo renice -n -5 -p $(pgrep -f 'critical-worker')
```

**systemd service nice:**

```ini
# /etc/systemd/system/app.service.d/nice.conf
[Service]
Nice=10
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart app
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| renice: permission denied | Target PID owner; negative nice | Use sudo; only root lowers nice |
| No perceived effect | I/O bound not CPU | Check `iostat`, `ionice`; not CPU scheduler |
| System still sluggish | Memory pressure | [[OOM (Linux Out Of Memory)]]; renice won't free RAM |
| Critical job starved | Others at negative nice | Raise misbehaving PIDs; use cgroups CPUQuota |
| renice works until restart | Service unit lacks Nice= | systemd drop-in Nice= |
| Batch job hogs despite renice 19 | Too many cores idle | Expected when CPU not contended |

## Gotchas

> [!WARNING]
> **Negative nice on shared prod** — one `-20` process can starve sshd, monitoring, and kubelet. Cap with cgroups instead of nice wars.

> [!WARNING]
> **renice ≠ realtime** — for audio/low-latency use `chrt` and RT limits (`/etc/security/limits.d`); misuse freezes system.

- **Containers** — renice inside container affects host-visible nice of cgroup processes; limits may clamp.
- **Short-lived workers** — renice parent; forked children may inherit nice (verify).
- **NUMA** — nice doesn't pin cores; use `taskset` for affinity.

## When NOT to use

- **Memory exhaustion** — renice doesn't reduce RSS; fix leak or add RAM/cgroup limit.
- **Disk thrashing** — use `ionice -c 3` or cgroup blkio.
- **Hard multi-tenant isolation** — use [[Linux cgroup]] CPUQuota/CPUs, not nice hints.

## Related

[[process]] [[Linux Process Theory]] [[Linux resource management]] [[OOM (Linux Out Of Memory)]] [[Linux cgroup]] [[top]]
