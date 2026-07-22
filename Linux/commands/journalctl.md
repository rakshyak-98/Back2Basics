[[loggging]] [[systemd]] [[Services commands]] [[grep]]

# journalctl

> One-line: query **systemd-journald** — indexed, structured logs for units, boots, kernel, and priorities. **Default first tool for "why did the service die?"**

## Mental model

journald collects logs from systemd units (stdout/stderr), syslog forwarding, kernel, and structured `journal` API calls. Entries are keyed by **unit**, **boot ID**, **priority**, **executable**, and custom fields (`_PID`, `_UID`, `_SYSTEMD_CGROUP`). Binary store — use `journalctl` to read, not raw `cat`.

```
systemd unit ──► journald ──► /var/log/journal/ (or /run/log/journal/)
                                    │
                               journalctl filters
```

| Filter | Flag / syntax |
|--------|----------------|
| Unit | `-u nginx.service` |
| Boot | `-b`, `-b -1`, `--list-boots` |
| Time | `--since`, `--until` |
| Priority | `-p err`, `-p warning..alert` |
| Kernel | `-k` |
| Follow | `-f` |
| Field | `_EXE=`, `_UID=`, `_COMM=` |

## Standard config / commands

```bash
# Service since this boot — baseline incident command
journalctl -u nginx.service -b --no-pager

# Live tail
journalctl -u myapp.service -f

# Last N lines
journalctl -u myapp -n 100 --no-pager

# Time bounds
journalctl -u sshd --since "1 hour ago"
journalctl --since "2024-03-01" --until "2024-03-18"
journalctl -u cron --since today

# Priority (err = error and above: err, crit, alert, emerg)
journalctl -p err -b
journalctl -u myapp -p err..crit

# Boot navigation
journalctl -b                      # current boot
journalctl -b -1                   # previous boot (crash analysis)
journalctl --list-boots

# Kernel only
journalctl -k
journalctl -k -p err

# Process / executable filters
journalctl _EXE=/usr/bin/nginx
journalctl _UID=1000 --since today
journalctl _COMM=sshd

# cgroup (slice/service hierarchy)
journalctl _SYSTEMD_CGROUP=/system.slice/ssh.service

# Output formats
journalctl -u myapp -o short-precise    # timestamps with μs
journalctl -u myapp -o verbose          # all fields
journalctl -u myapp -o json | jq .
journalctl --no-pager                   # scripts / CI
```

**Retention & disk:**

```bash
journalctl --disk-usage
sudo journalctl --vacuum-size=500M
sudo journalctl --vacuum-time=1week
# Persistent config: /etc/systemd/journald.conf → SystemMaxUse=, MaxRetentionSec=
```

**Dangerous vacuum (almost everything gone):**

```bash
sudo journalctl --vacuum-time=1s -u myapp.service   # narrow if possible; prefer --vacuum-size
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `-- No entries --` | Wrong unit name; wrong boot | `systemctl status`; `journalctl --list-boots`; `-b -1` |
| Logs vanished after reboot | Volatile storage | [[loggging]] — `Storage=persistent` in journald.conf |
| Permission denied | Non-privileged user | `sudo` or `usermod -aG systemd-journal user` |
| Flood hides signal | Too broad query | `-p err`, `--since`, `-u` single unit |
| Timestamps don't match UTC tools | Local TZ display | `journalctl --utc` |
| Unit logs empty but app logs files | Not connected to stdout | Fix unit `StandardOutput=journal`; or read app log path |
| Disk full from journal | Unbounded debug | `--vacuum-size`; lower app log level; tune journald |

## Gotchas

> [!WARNING]
> **Unit names need `.service` suffix** sometimes — `nginx` vs `nginx.service`; tab-complete helps.

> [!WARNING]
> **`--vacuum-time=1s` on whole journal** — deletes nearly all history. Prefer size caps or unit-scoped export first.

> [!WARNING]
> **Pager eats automation** — always `--no-pager` in scripts; or `export SYSTEMD_COLORS=0`.

> [!WARNING]
> **Docker/k8s** — container logs may be in docker/k8s driver, not host journal for that process name.

## When NOT to use

- **Application log files only** (legacy nginx file) → tail/grep path from config.
- **Years of retention** → ship to SIEM; journal is local ring buffer.
- **Cross-host correlation** → centralized logging; journal is per-host.

## Related

[[loggging]] [[systemd]] [[Services commands]] [[grep]] [[systemctl]]
