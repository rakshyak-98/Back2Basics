[[ss]] [[Linux network commands]] [[lsof]] [[ip]] [[commands]]

# netstat

> Lists sockets, listeners, and some interface stats — legacy on modern Linux; prefer [[ss]].





## Interview Relevance
Interviewers check whether you reach for `ss` first and treat netstat as a legacy net-tools fallback, not the default inventory tool.

## Sources
- [Wikipedia — netstat](https://en.wikipedia.org/wiki/netstat) — overview
- [man netstat](https://man7.org/linux/man-pages/man8/netstat.8.html) — deep-dive

## Key Concepts
- **Listeners vs connections:** `-l` shows servers; `-a` / `-t` include established and TIME-WAIT.
- **`-p` process column:** needs privilege for other users' sockets → same rule as `ss -p`.
- **`-n` numeric:** skips reverse DNS → avoids hangs on broken resolvers.
- **net-tools vs iproute2:** netstat ships with net-tools; [[ss]] / [[ip]] are the modern defaults.

## Technical Details
```txt
LISTEN  ← servers ( -l )
ESTABLISHED / TIME_WAIT / …  ← connections ( -a / -t )
-p adds PID/program (needs priv for others’ sockets)
```

```bash
sudo netstat -luntp
sudo netstat -tulnp | grep :8080
netstat -ant
netstat -s
sudo netstat -p
```

| Flag | Meaning |
|------|---------|
| `-l` | Listening |
| `-a` | All sockets |
| `-t` / `-u` | TCP / UDP |
| `-n` | Numeric (no DNS) |
| `-p` | PID/program |
| `-s` | Statistics |

Prefer [[ss]] equivalents: `ss -luntp`, `ss -s`, `ss -tan state time-wait`.

| Symptom | Check | Fix |
|---------|-------|-----|
| `netstat: command not found` | net-tools missing | Install net-tools **or** switch to `ss` |
| Slow on busy hosts | DNS lookups | Always `-n`; better: `ss` |
| No process names | Not root | `sudo`; or `ss -p` |
| “Port free” but bind fails | IPv6 / other user | Check `ss -lntup` fully |

## Real-World Applications
Quick port inventory on older hosts that still ship net-tools, or reading legacy runbooks that have not migrated to `ss`.

**Example:** A minimal container image has no `netstat` — use `ss -luntp` from iproute2 instead of installing net-tools.

## Pros/Cons or Trade-offs
- **Pro:** Familiar flags for operators trained on classic Unix.
- **Con:** Often absent on minimal images; slower and thinner than `ss` on busy hosts.

## Comparison
- vs [[ss]]: same job, newer kernel/netlink path — use `ss` on modern Linux.
- vs [[lsof]]: `lsof -i` is file-descriptor oriented; `ss`/`netstat` are socket-table oriented.

## Mistakes to Avoid
- Assuming netstat is installed — many images omit net-tools.
- Omitting `-n` so reverse DNS makes the tool look hung.
- Using netstat for packet capture or firewall policy — use tcpdump / nftables / [[ufw]] instead.
