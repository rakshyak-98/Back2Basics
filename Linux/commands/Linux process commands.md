[[Commands]] [[process]] [[Linux Process Theory]] [[ps]] [[top]] [[lsof]] [[renice]] [[systemctl]] [[Services commands]]

# Linux process commands

> The everyday toolkit to list, inspect, signal, and prioritize processes — ps, top, pgrep, kill, lsof.





## Interview Relevance
Incident flow: find → watch → explain (fds/ports) → act (TERM then service restart) — without reckless `killall`.

## Sources
- [ps(1)](https://man7.org/linux/man-pages/man1/ps.1.html) — deep-dive
- [kill(1)](https://man7.org/linux/man-pages/man1/kill.1.html) — overview

## Core Definition
Use [[ps]]/`pgrep` to find, [[top]]/`pidstat` to watch, [[lsof]]/`/proc` to explain opens, and `kill`/`systemctl` to act. Prefer service-aware restarts for daemons over raw signals when units exist.

## Key Concepts
- **pgrep/pidof:** Name → PIDs without fragile `ps | grep`.
- **Signals:** TERM first; KILL last (no cleanup).
- **Priority:** `renice` / nice — see [[renice]].
- **STAT letters:** R/S/D/Z — see [[ps]].
- **Service layer:** `systemctl` for managed daemons.

## Technical Details
```txt
find  →  ps / pgrep / pidof
watch →  top / htop / pidstat
why   →  lsof / /proc/PID/{fd,status,stack}
act   →  kill / pkill / renice / systemctl
```

```bash
pgrep -af nginx
pidof java
ps -eo pid,ppid,user,stat,pcpu,pmem,cmd --sort=-pcpu | head

top
pidstat 1 5

lsof -p <pid>
sudo lsof -iTCP:8080 -sTCP:LISTEN
ls -l /proc/<pid>/fd

kill -TERM <pid>
kill -KILL <pid>
pkill -TERM -f 'my-worker'
kill -l

renice -n 5 -p <pid>

systemctl status foo.service
systemctl restart foo.service
```

| Symptom | Check | Fix |
|---------|-------|-----|
| High CPU mystery | `ps --sort=-pcpu`; `top -H` | Profile; fix hot loop |
| Port held after kill | `lsof`/`ss` | Child still alive; kill tree |
| Zombies | `STAT Z`; PPID | Fix parent reaping |
| Permission denied signal | Ownership | Correct user; systemd unit |

## Real-World Applications
Finding a runaway worker, gracefully stopping it with TERM, and restarting via systemd so dependencies and restart policy stay correct.

## Pros/Cons or Trade-offs
- **Pro:** Universal toolbox on every Linux host.
- **Con:** Easy to over-match with `pkill -f`; KILL skips cleanup.
- **Trade-off:** Raw signals for one-offs vs systemctl for daemons.

## Comparison
vs [[Services commands]]: unit lifecycle. vs [[gdb]]: deep crash inspect. vs cgroup/OOM: resource limits vs process signals.

## Mistakes to Avoid
- Broad `killall`/`pkill` without `pgrep -a` first.
- Jumping to KILL before TERM/service stop.
- Parsing `ps` in cron instead of `pgrep`/`/proc`.
