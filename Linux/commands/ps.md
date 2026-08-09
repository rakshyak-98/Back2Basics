[[Commands]] [[process]] [[top]] [[lsof]]

# ps

> `ps` snapshots processes right now — PID, state, TTY, CPU, memory, and command line.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `ps` reads `/proc` once and prints a table; it is not live like `top` — re-run it when state changes.

```txt
ps ──► /proc/<pid>/… ──► one snapshot
              │
     pid, stat, tty, rss, cmd, …
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Snapshot** | One moment in time | “`ps` doesn’t refresh; `top` does.” |
| **TTY `?`** | No controlling terminal | “Daemons and `nohup`/`setsid` jobs show `?`.” |
| **STAT** | Process state letter | “`R` runnable, `S` sleep, `D` disk, `Z` zombie.” |
| **RSS vs VSZ** | Resident RAM vs virtual size | “High VSZ alone is not a leak — watch RSS.” |
| **BSD vs UNIX flags** | `ps aux` vs `ps -ef` | “Both work; pick one style and stick to it.” |
| **`forest` / tree** | Parent–child view | “Find which supervisor owns the workers.” |

### No controlling TTY

- Detached from a terminal: no interactive I/O; no terminal-generated `SIGINT` / logout `SIGHUP` (unless something else signals).
- Common for: `systemd` services, `cron`, `nohup … &`, `disown`, `setsid`.
- Check: `ps -o pid,tty,cmd` → `?`, or `ls -l /proc/<pid>/fd/0` not linked to `/dev/tty*` / `pts`.

---

## Standard config / commands

```bash
# Everyday views
ps aux                          # BSD style: USER PID %CPU %MEM … COMMAND
ps -ef                          # UNIX style: UID PID PPID C STIME TTY TIME CMD
ps -eo pid,ppid,user,stat,tty,rss,pcpu,cmd --sort=-rss | head

# One process / user / tree
ps -p <pid> -o user,pid,ppid,stat,tty,wchan:20,cmd
ps -u "$USER" -o pid,stat,cmd
ps -efH                         # hierarchy
pstree -p <pid>

# Threads of a process
ps -L -p <pid> -o pid,tid,psr,stat,pcpu,cmd

# Memory map helpers (often next after ps)
cat /proc/<pid>/maps | head
pmap -x <pid>

# Signals when you must stop something
kill -s TERM <pid>
kill -s QUIT <pid>              # SIGQUIT = 3
```

| Knob | Why it matters |
|------|----------------|
| `-o` custom columns | Add `wchan`, `rss`, `etime` for triage |
| `--sort=-%cpu` / `-rss` | Find hogs without interactive `top` |
| `-L` / `-T` | Thread-level CPU (Java/Go thread storms) |
| `TTY` | Session-bound vs daemon |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| “Process gone” but port busy | `ps` + `lsof -i :<port>` | Child or restarted PID; kill listener |
| High CPU, unclear who | `ps -eo pid,pcpu,cmd --sort=-pcpu \| head` | Then `top -H -p <pid>` / `perf` |
| Memory climb | `ps -o pid,rss,vsz,cmd -p <pid>` over time | Leak vs cache; confirm with `/proc/<pid>/smaps` |
| Zombies | `ps -eo pid,ppid,stat,cmd \| awk '$3~/Z/'` | Fix parent reaping |
| TTY signals don’t stop job | `TTY` is `?` | Send signal by PID; not Ctrl-C on another terminal |
| `grep` shows itself | Pattern matches `grep` | Use `pgrep -af` or `[g]rep` trick |

---

## Gotchas

> [!WARNING]
> **`ps` is stale the moment it prints** — for live contention use [[top]] / `pidstat` / `perf`.

> [!WARNING]
> **`VSZ` scares juniors** — virtual size includes mapped libs and reservations; **RSS** (and proportional `PSS`) matter for RAM pressure.

> [!WARNING]
> **SIGQUIT may leave children** — after quitting a supervisor, find leftover workers with `ps --ppid` / `pstree` and free the port with [[lsof]].

> [!WARNING]
> **Permissions** — other users’ full cmdlines may be hidden; use root/`CAP_SYS_PTRACE` carefully.

---

## When NOT to use

- **Don’t use `ps` as a continuous dashboard** — use [[top]], `htop`, or metrics scrapers.
- **Don’t use `ps` to find open files or sockets** — use [[lsof]] or `ss` ([[ss]]).
- **Don’t parse `ps` in scripts if `/proc` APIs suffice** — unstable columns across locales; prefer `pgrep`/`pidof` or read `/proc`.

---

## Related

[[process]] [[Linux Process Theory]] [[top]] [[lsof]] [[Linux process commands]] [[file descriptors]] [[OOM (Linux Out Of Memory)]] [[ss]] [[gdb]]
