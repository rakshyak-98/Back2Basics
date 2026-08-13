[[commands]] [[sudo]]

# tee

> tee splits the pipe — write the same bytes to a file and still pass them downstream (and to your screen).

---

## How it works

```txt
command ──► tee file.log ──► next | stage
              └── also writes file.log
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`tee file`** | Save + show | “I keep a log without losing the pipeline.” |
| **`-a`** | Append | “Don’t truncate the log on each run.” |
| **`sudo tee`** | Root write, user command | “Redirect `>` as root fails after sudo; tee fixes it.” |
| **Multiple files** | Fan-out | “One stream, many copies.” |

---


## Configuration and commands

```bash
# See + save
ls -la | tee listing.txt

# Pipeline: save full log, filter on screen
docker logs myapp 2>&1 | tee docker.log | grep ERROR

# Append
journalctl -f | tee -a journal-backup.log

# Write as root from a non-root producer
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf >/dev/null

# Many files
echo "Hello" | tee a.txt b.txt c.txt

# Peek without breaking the pipe
curl -s https://api.example.com | tee /dev/stderr | jq .
```

| What you want | Command shape |
|---------------|---------------|
| Save + continue pipeline | `cmd \| tee log \| next` |
| Root-owned destination | `cmd \| sudo tee /etc/file` |
| Quiet screen, only file | `cmd \| tee file >/dev/null` |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `Permission denied` on `/etc/...` | Used `sudo cmd > file` | `cmd \| sudo tee file` (sudo only elevates left of `>`) |
| Log truncated unexpectedly | Missing `-a` | `tee -a` |
| Colors gone in file | ANSI codes | Often still there; viewers may strip — use `script` if you need tty fidelity |
| Pipeline exits early | `tee` got SIGPIPE | Ensure consumers read; or `tee` last if you only need the file |

---


## Gotchas

> [!WARNING]
> **`sudo cmd > /root/file` does not write as root** — the shell opens the file *before* sudo. Use `sudo tee`.

> [!WARNING]
> **`tee` overwrites by default** — same footgun as `>`. Prefer `-a` for rotating incident logs.

---


## When not to use

- **Only save, never show** — plain `>` / `>>`.
- **Structured logging in apps** — application logger + log shipper, not ad-hoc tee in production entrypoints.
- **Binary streams you must not duplicate** — tee copies bytes; watch disk.

---


## Related

[[commands]] [[Bash syntax]] [[visudo]]

## Sources

- [Wikipedia — tee](https://en.wikipedia.org/wiki/tee)
