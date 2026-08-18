[[Commands]] [[file descriptors]] [[process]] [[ss]]

# lsof

> `lsof` lists open files — and on Linux that includes sockets, pipes, and devices — showing which process holds them.

## Mental model

**Say it in one breath:** Everything is a file; `lsof` answers “who has this path/port open?” by walking process fd tables.

```txt
PID  fd  type
app  3 → /var/log/app.log
app  4 → TCP *:8080 (LISTEN)
app  5 → pipe / anon_inode / mem fd
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Open file** | fd → kernel `struct file` | “Includes sockets, not just disk files.” |
| --- | --- | --- |
| **LISTEN** | Bound server socket | “`lsof -i :443` finds the HTTPS process.” |
| **DELETED** | File unlinked but fd held | “Disk space not freed until process closes.” |
| **cwd / txt** | Working dir / binary mapping | “`txt` is the executable itself.” |
| **NETWORK** | Internet / UNIX sockets | “Faster peer tool for sockets is often `ss`.” |
| **`-p` / `-i` / `-u`** | Filter process / net / user | “Always narrow — full-system `lsof` is heavy.” |

### “Everything is a file” (what shows up)

| Kind | Examples |
| --- | --- |
| Regular files | configs, logs, data |
| Directories | `cwd`, `rtd` |
| Devices | `/dev/null`, disks |
| Pipes / FIFOs | shell pipelines |
| Sockets | TCP/UDP/UNIX |
| anon / mem | eventfd, sync fds, mappings |

## Standard config / commands

```bash
# Port → process (classic)
sudo lsof -iTCP:8080 -sTCP:LISTEN
sudo lsof -i :5432
sudo lsof -i -P -n | grep LISTEN

# Process → everything it holds
lsof -p <pid>
ls -l /proc/<pid>/fd          # lighter cousin

# File → who
lsof /var/log/syslog
lsof +D /var/log              # expensive recursive

# Deleted-but-open (disk “leak”)
sudo lsof +L1
sudo lsof | grep '(deleted)'

# User / command filters
lsof -u deploy
lsof -c nginx
```

| Knob | Why it matters |

| `-P -n` | Skip port/name DNS — faster, stable scripts |
| --- | --- |
| `-sTCP:LISTEN` | Only servers, not every ESTABLISHED |
| `+L1` | Find unlinked files still held open |
| Prefer `ss -lptn` for sockets | Often quicker than full `lsof -i` |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `address already in use` | `lsof -i :<port>` / `ss -lptn` | Stop old process or change port |
| Disk full after log rotate | `lsof \| grep deleted` | Restart/signal process to reopen logs |
| `Too many open files` | `lsof -p <pid> \| wc -l`; `ls /proc/<pid>/fd \| wc -l` | Close leak; raise `LimitNOFILE` ([[file descriptors]]) |
| NFS / mount busy | `lsof +D /mnt/foo` | Kill holders or `fuser -vm` |
| Which binary is listening | `lsof -iTCP:PORT -sTCP:LISTEN` | Confirm unexpected path / user |
| Permission denied on `lsof` | Need root for others’ fds | `sudo`; least privilege in scripts |

## Gotchas

> [!WARNING]
> **Full-system `lsof` is expensive** — on busy hosts prefer `-p`, `-i :port`, or `ss` + `/proc/<pid>/fd`.

> [!WARNING]
> **`(deleted)` holds blocks** — rotating logs without reopen (`kill -HUP` / restart) keeps consuming disk.

> [!WARNING]
> **UNIX sockets look different** — `lsof -U` / paths under `/run`; don’t only grep TCP.

> [!WARNING]
> **Containers** — host `lsof` may not see container netns; `nsenter` / `docker exec` + `ss` inside.

## When NOT to use

- **Don’t scrape `lsof` every second for metrics** — use `/proc` exporters or eBPF.
- **Don’t use `lsof` as the only network tool** — [[ss]] is better for socket state machines.
- **Don’t `lsof +D` on huge trees in production** — can stall; target a PID or file instead.

## Related

[[file descriptors]] [[process]] [[ps]] [[ss]] [[netstat]] [[Epoll]] [[Linux process commands]]
