[[Linux Process Theory]] [[Linux process commands]] [[renice]] [[OOM (Linux Out Of Memory)]] [[Linux cgroup]]

# process

> A process is a running program instance — the kernel tracks its PID, memory, open files, and scheduling class until it exits.

Creation: `fork()` (clone address space) then often `execve()` (load new program). Parent waits with `waitpid()`; zombie children hold a PID until reaped. Threads share one process but have individual task structs.

## Inspect processes

```bash
# Snapshot
ps aux
ps -eo pid,ppid,user,%cpu,%mem,cmd --sort=-%cpu | head

# Live view
top
htop    # if installed

# One PID in depth
ps -p 1234 -o pid,ppid,stat,etime,cmd
cat /proc/1234/status
ls -l /proc/1234/fd
```

## Signals operators use

| Signal | Number | Effect |
|--------|--------|--------|
| SIGTERM | 15 | Polite shutdown (default `kill`) |
| SIGKILL | 9 | Immediate kill — cannot be caught |
| SIGHUP | 1 | Reload or hangup — daemons often reload config |
| SIGSTOP / SIGCONT | 19 / 18 | Pause / resume |

```bash
kill -TERM 1234
kill -9 1234          # last resort
pkill -f 'nginx: worker'
```

## Parent / child tree

```bash
pstree -p
ps -ef --forest
```

## When things go wrong

| Symptom | Check | Action |
|---------|-------|--------|
| Zombie `<defunct>` | Parent not reaping | Fix parent or restart parent service |
| High CPU one PID | `top -H -p PID` | Profile; lower priority with [[renice]] |
| Cannot kill | Kernel D state (uninterruptible sleep) | Usually I/O — fix underlying storage/NFS |
| OOM killed | `dmesg \| grep -i oom` | [[OOM (Linux Out Of Memory)]] |

## Related

[[Linux Process Theory]] · [[Linux process commands]] · [[Linux cgroup]] · [[Error status code]]

## Sources

- `man 2 fork`, `man 2 execve`, `man 7 signal`
- [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html)
