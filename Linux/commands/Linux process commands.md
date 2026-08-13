[[Commands]] [[process]] [[ps]] [[top]] [[lsof]]

# Linux process commands

> The everyday toolkit to list, inspect, signal, and prioritize processes — `ps`, `top`, `pgrep`, `kill`, `lsof`.

---

## How it works

```txt
find  →  ps / pgrep / pidof
watch →  top / htop / pidstat
why   →  lsof /ls /proc/PID/{fd,status,stack}
act   →  kill / pkill / renice / systemctl
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`pgrep` / `pkill`** | Find / signal by name | “Safer than `kill $(ps \| grep)` if you check `-a` first.” |
| **Signal** | Soft ask vs hard stop | “`TERM` (15) then `KILL` (9).” |
| **Nice / renice** | CPU scheduling priority | “Lower niceness → higher priority; needs rights.” |
| **`/proc`** | Kernel’s process API as files | “Scripts should prefer `/proc` over parsing `ps`.” |
| **Job control** | `fg`/`bg`/`Ctrl-Z` in a shell | “Only for that shell’s children — not systemd services.” |
| **Service manager** | systemd owns long-running daemons | “Prefer `systemctl restart` over raw `kill`.” |

### Tool roles

| Tool | Best for |
|------|----------|
| [[ps]] | Snapshot, scripts, custom columns |
| [[top]] | Live CPU/RAM/load |
| [[lsof]] | fds, ports, deleted files |
| `pgrep`/`pkill` | Name-based select |
| `pstree` | Parent/child map |
| `pidstat` | Per-PID CPU/IO over time |
| `strace` | Syscall-level “what is it doing?” |

---


## Quick reference

| Task | Command |
|------|---------|
| … | `…` |


## Configuration and commands

```bash
# Find
pgrep -af nginx
pidof java
ps -eo pid,ppid,user,stat,pcpu,pmem,cmd --sort=-pcpu | head

# Live
top          # P=CPU M=MEM H=threads 1=per-core c=full cmd
pidstat 1 5

# Open files / ports
lsof -p <pid>
sudo lsof -iTCP:8080 -sTCP:LISTEN
ls -l /proc/<pid>/fd

# Signal
kill -TERM <pid>
kill -KILL <pid>
pkill -TERM -f 'my-worker'
kill -l

# Priority (see [[renice]])
renice -n 5 -p <pid>

# Service-aware (preferred for daemons)
systemctl status foo.service
systemctl restart foo.service
```

### `top` keys (quick)

| Key | Action |
|-----|--------|
| `P` / `M` | Sort CPU / memory |
| `1` | Per-core CPU |
| `c` | Full command path |
| `k` / `r` | Kill / renice |
| `H` | Threads |
| `q` | Quit |

| Knob | Why it matters |
|------|----------------|
| Match method (`-f`, user, exact) | Avoid killing the wrong PIDs |
| `systemctl` vs `kill` | Units restart policies / dependencies |
| `LimitNOFILE` / cgroup | Hard walls `kill` cannot fix |

---


## Options and flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |


## Examples

```bash
# …
```


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Unknown CPU burn | `top` → `P`; `ps --sort=-pcpu` | Profile (`perf`); fix hot loop |
| Port in use | `lsof -i :port` / `ss -lptn` | Stop old unit; fix socket activation |
| Won’t die | State `D`? zombies? children? | Fix I/O; kill process group; `systemctl stop` |
| Instant restart after kill | systemd `Restart=` | Stop the unit, don’t only kill PID |
| “Command not found” in service | Env differs from shell | Set `Environment=` in unit; absolute paths |
| Too many processes | `ps` count; `pids.max` | Fix fork bomb / raise cgroup pids |

---


## Gotchas

> [!WARNING]
> **`killall` / broad `pkill`** — easy to match too much on shared hosts. Always `pgrep -a` first.

> [!WARNING]
> **`KILL` skips cleanup** — prefer `TERM` and service stop hooks.

> [!WARNING]
> **Job-control signals ≠ service management** — Ctrl-C in your laptop SSH does not replace `systemctl`.

> [!WARNING]
> **Parsing `ps` in cron** — locale and column drift; use `pgrep` or `/proc`.

---


## When not to use

- **Don’t raw-signal Kubernetes/container PIDs on the host** — use the orchestrator / `docker kill` / enter the pidns.
- **Don’t use this toolkit for packet-level debugging** — use `ss`, `tcpdump`, metrics.
- **Don’t renice as a substitute for capacity planning** — fix the bottleneck or scale.

---


## Related

[[process]] [[Linux Process Theory]] [[ps]] [[top]] [[lsof]] [[renice]] [[systemctl]] [[Services commands]] [[file descriptors]] [[OOM (Linux Out Of Memory)]] [[ss]]

## Sources

- [Wikipedia — Linux process commands](https://en.wikipedia.org/wiki/Linux_process_commands)
