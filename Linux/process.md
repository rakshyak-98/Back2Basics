[[Linux Process Theory]] [[Linux process commands]] [[renice]] [[OOM (Linux Out Of Memory)]] [[Linux cgroup]] [[Error status code]] [[ps]] [[top]]

# process

> A running program instance — the kernel tracks PID, memory, open files, and scheduling until exit.





## Interview Relevance
Core OS question: fork/exec, zombies, signals (TERM vs KILL), and D-state vs killable tasks.

## Sources
- [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html) — deep-dive
- `man 2 fork`, `man 2 execve`, `man 7 signal` — deep-dive

## Core Definition
Creation: `fork()` (clone address space) then often `execve()` (load new program). Parent waits with `waitpid()`; zombie children hold a PID until reaped. Threads share one process but have individual task structs.

## Key Concepts
- **PID / PPID:** identity and parent for reaping and trees.
- **Zombie:** exited child not waited — fix the parent, not the zombie.
- **Signals:** TERM polite, KILL unblockable, HUP often reload.
- **D state:** uninterruptible sleep (usually I/O) — KILL may not help until I/O completes.
- **cgroups / OOM:** resource limits and killer path beyond raw nice.

## Technical Details
```bash
ps aux
ps -eo pid,ppid,user,%cpu,%mem,cmd --sort=-%cpu | head
top
ps -p 1234 -o pid,ppid,stat,etime,cmd
cat /proc/1234/status
ls -l /proc/1234/fd
pstree -p
ps -ef --forest
kill -TERM 1234
kill -9 1234
pkill -f 'nginx: worker'
```

| Signal | Number | Effect |
|--------|--------|--------|
| SIGTERM | 15 | Polite shutdown (default `kill`) |
| SIGKILL | 9 | Immediate — cannot be caught |
| SIGHUP | 1 | Hangup / often reload |
| SIGSTOP / SIGCONT | 19 / 18 | Pause / resume |

| Symptom | Check | Action |
|---------|-------|--------|
| Zombie `<defunct>` | Parent not reaping | Fix/restart parent |
| High CPU one PID | `top -H -p PID` | Profile; [[renice]] |
| Cannot kill | D state | Fix storage/NFS I/O |
| OOM killed | `dmesg \| grep -i oom` | [[OOM (Linux Out Of Memory)]] |

## Real-World Applications
Incident “CPU pegged”: find PID with `ps`/`top`, inspect threads, signal politely, then check cgroup limits if renice does nothing.

## Pros/Cons or Trade-offs
- **Pro:** Universal mental model for services, jobs, and debugging.
- **Con:** Process view alone misses cgroup quotas and GPU/device holders.

## Comparison
- vs thread: threads share address space; processes are isolation boundaries.
- vs [[Linux cgroup]]: cgroups constrain groups of processes.

## Mistakes to Avoid
- `kill -9` as first resort — skip cleanup handlers.
- Trying to “kill the zombie” instead of fixing the parent.
- Ignoring D-state as a storage problem.
