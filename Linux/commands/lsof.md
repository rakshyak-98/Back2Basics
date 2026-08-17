[[Commands]] [[process]] [[ps]] [[ss]] [[netstat]] [[Epoll]] [[Linux process commands]]

# lsof

> lsof lists open files — and on Linux that includes sockets, pipes, and devices — showing which process holds them.





## Interview Relevance
Classic: who holds this port/file, deleted-but-open disk leaks, and when to prefer `ss` + `/proc/<pid>/fd` on busy hosts.

## Sources
- [lsof(8)](https://man7.org/linux/man-pages/man8/lsof.8.html) — deep-dive
- [proc(5) — fd](https://man7.org/linux/man-pages/man5/proc.5.html) — overview

## Core Definition
Everything is a file descriptor. `lsof` maps PID ↔ path/socket. Use it to find listeners, who has a mount busy, and processes holding deleted files that still consume disk blocks.

## Key Concepts
- **Port → process:** `-iTCP:port -sTCP:LISTEN`.
- **File → who:** `lsof /path` or `+D` (expensive).
- **`(deleted)`:** Unlinked but still open — space freed only after close.
- **`-p` scope:** Cheaper than full-system scans.
- **Namespaces:** Host lsof may miss container netns.

## Technical Details
```bash
sudo lsof -iTCP:8080 -sTCP:LISTEN
sudo lsof -i :5432
sudo lsof -i -P -n | grep LISTEN

lsof -p <pid>
ls -l /proc/<pid>/fd

lsof /var/log/syslog
lsof +D /var/log

sudo lsof +L1
sudo lsof | grep '(deleted)'

lsof -u deploy
lsof -c nginx
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Can’t umount | `lsof +D /mnt` | Stop holders; `fuser -mv` |
| df full, du small | `(deleted)` | Restart/HUP writers |
| Port busy, no process in ss? | netns / race | Check container ns; retry |
| Slow lsof | Full scan | Narrow `-p` / `-i` |

## Real-World Applications
Finding which process blocks a volume umount, reclaiming disk after logrotate left deleted handles open, and mapping :5432 to a postgres PID.

## Pros/Cons or Trade-offs
- **Pro:** Unified view of files and sockets.
- **Con:** Full-system scans are expensive; output is dense.
- **Trade-off:** `ss -lntp` for ports vs lsof when you need file paths too.

## Comparison
vs [[ss]]: faster socket focus. vs `/proc/<pid>/fd`: lighter per-PID. vs [[ps]]: process table without FD detail.

## Mistakes to Avoid
- Running unscoped `lsof` on huge multi-tenant hosts as first step.
- Ignoring `(deleted)` after log rotation.
- Assuming host lsof sees every container socket.
