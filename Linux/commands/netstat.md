[[commands]] [[ss]] [[Linux network commands]] [[lsof]]

# netstat

> netstat lists sockets, listeners, and some interface/protocol stats — legacy; prefer [[ss]] on modern Linux.

## Mental model

**Say it in one breath:** snapshot of who is listening and who is connected — same questions as `ss`, slower path.

```txt
LISTEN  ← servers ( -l )
ESTABLISHED / TIME_WAIT / …  ← connections ( -a / -t )
-p adds PID/program (needs priv for others’ sockets)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`-luntp`** | Listen + UDP/TCP + numeric + process | “My default inventory one-liner.” |
| --- | --- | --- |
| **`-tuln`** | Listeners without DNS | “Fast ‘what ports are open’.” |
| **`-s`** | Protocol counters | “Retransmits / errors at a glance.” |
| **`ss` vs netstat** | Same job, newer tool | “I use `ss`; netstat is deprecated on many distros.” |

## Standard config / commands

```bash
# Classic inventory
sudo netstat -luntp
sudo netstat -tulnp | grep :8080

# Connections (no listeners)
netstat -ant

# Protocol statistics
netstat -s

# Process column
sudo netstat -p
```

| Flag | Meaning |
| --- | --- |
| `-l` | Listening |
| `-a` | All sockets |
| `-t` / `-u` | TCP / UDP |
| `-n` | Numeric (no DNS) |
| `-p` | PID/program |
| `-s` | Statistics |

Prefer the [[ss]] equivalents: `ss -luntp`, `ss -s`, `ss -tan state time-wait`.

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `netstat: command not found` | net-tools missing | `apt install net-tools` **or** switch to `ss` (iproute2) |
| Slow on busy hosts | DNS lookups | Always `-n`; better: `ss` |
| No process names | Not root | `sudo`; or `ss -p` |
| “Port free” but bind fails | IPv6 / other user | Check `ss -lntup` fully |

## Gotchas

> [!WARNING]
> **net-tools is legacy** — many minimal images omit it. Learn `ss` / `ip`.

> [!WARNING]
> **Without `-n`**, reverse DNS stalls make netstat look “hung”.

## When NOT to use

- **Any modern host with `ss`** — use [[ss]].
- **Packet capture** — `tcpdump` / wireshark.
- **Firewall policy** — [[ufw]] / nftables / iptables.

## Related

[[ss]] [[Linux network commands]] [[lsof]] [[ip]] [[commands]]
