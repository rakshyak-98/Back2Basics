[[Commands]] [[process]] [[Linux Process Theory]] [[top]] [[lsof]] [[Linux process commands]] [[OOM (Linux Out Of Memory)]] [[ss]]

# ps

> One-shot process snapshot — PID, state, TTY, CPU, memory, and command line from `/proc`.

## Interview Relevance

Signals that you know `ps` is a point-in-time view (vs [[top]]), can read STAT/TTY/RSS, and pick BSD (`aux`) vs UNIX (`-ef`) styles deliberately.

## Sources

- [man ps](https://man7.org/linux/man-pages/man1/ps.1.html) — deep-dive
- [Wikipedia — ps (Unix)](https://en.wikipedia.org/wiki/Ps_(Unix)) — overview

## Key Concepts

- **Snapshot:** does not refresh — live contention needs [[top]] / `pidstat` / `perf`.
- **TTY `?`:** no controlling terminal — daemons, `systemd`, `nohup`, `setsid`.
- **STAT letters:** `R` runnable, `S` sleep, `D` uninterruptible disk, `Z` zombie.
- **RSS vs VSZ:** resident RAM vs virtual mappings — high VSZ alone is not a leak.
- **Forest / tree:** parent–child view to find which supervisor owns workers.

## Technical Details

```txt
ps ──► /proc/<pid>/… ──► one snapshot
              │
     pid, stat, tty, rss, cmd, …
```

```bash
ps aux
ps -ef
ps -eo pid,ppid,user,stat,tty,rss,pcpu,cmd --sort=-rss | head
ps -p <pid> -o user,pid,ppid,stat,tty,wchan:20,cmd
ps -u "$USER" -o pid,stat,cmd
ps -efH
pstree -p <pid>
ps -L -p <pid> -o pid,tid,psr,stat,pcpu,cmd
pmap -x <pid>
kill -s TERM <pid>
```

| Knob | Why it matters |
|------|----------------|
| `-o` custom columns | Add `wchan`, `rss`, `etime` for triage |
| `--sort=-%cpu` / `-rss` | Find hogs without interactive `top` |
| `-L` / `-T` | Thread-level CPU (Java/Go storms) |
| `TTY` | Session-bound vs daemon |

No controlling TTY means no interactive I/O and no terminal-generated `SIGINT` / logout `SIGHUP` unless something else signals. Check: `ps -o pid,tty,cmd` → `?`, or `ls -l /proc/<pid>/fd/0` not linked to a tty/pts.

| Symptom | Check | Fix |
|---------|-------|-----|
| Process gone, port busy | `ps` + `lsof -i :<port>` | Child or restarted PID; kill listener |
| High CPU, unclear who | `ps -eo pid,pcpu,cmd --sort=-pcpu` | Then `top -H -p <pid>` / `perf` |
| Memory climb | `ps -o pid,rss,vsz,cmd -p <pid>` over time | Leak vs cache; `/proc/<pid>/smaps` |
| Zombies | `ps -eo pid,ppid,stat,cmd` for `Z` | Fix parent reaping |
| Ctrl-C does nothing | `TTY` is `?` | Signal by PID from another session |

## Real-World Applications

First step in “who owns this CPU/RAM?”, finding zombies, and mapping supervisor → worker trees before kill decisions.

**Example:** After SIGQUIT on a supervisor, use `ps --ppid` / `pstree` and [[lsof]] to catch leftover workers still holding a port.

## Pros/Cons or Trade-offs

- **Pro:** Scriptable, customizable columns, works over plain SSH without a TUI.
- **Con:** Stale immediately; fragile to parse across locales — prefer `pgrep` / `/proc` in automation.

## Comparison

- vs [[top]]: live refresh and sorting UI; `ps` is one shot.
- vs [[lsof]] / [[ss]]: open files and sockets — not process tables.

## Mistakes to Avoid

- Treating VSZ as “RAM used” — watch RSS (and PSS) under memory pressure.
- Using `ps` as a continuous dashboard.
- Parsing `ps` output in scripts when `pgrep`/`pidof` or `/proc` suffice.
- Expecting Ctrl-C to stop a process whose TTY is `?`.
