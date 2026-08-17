[[loggging]] [[services/systemd]] [[Services commands]] [[grep]] [[systemctl]]

# journalctl

> journalctl queries journald’s binary logs — filter by unit, boot, time, and priority instead of grepping flat files blindly.

```txt
        journalctl ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Must-know ops: `-u` + `-b`, `--since`, `-p err`, vacuum retention, and persis…

## Sources
- [journalctl(1)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html) — deep-dive
- [systemd-journald.service(8)](https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html) — overview

## Key Concepts
- **`-u` / `-b` / `--since`:** Unit, boot, time windows.
- **`-p`:** Priority (err and above, ranges).
- **`-f`:** Follow like `tail -f`.
- **Fields:** `_EXE=`, `_COMM=`, `_UID=` for precise filters.
- **Vacuum:** Size/time caps so journals don’t fill the disk.


- **Core:** journald collects unit stdout/stderr, syslog forwarding, kernel messages, and…

## Technical Details
```bash
journalctl -u nginx.service -b --no-pager
journalctl -u myapp.service -f
journalctl -u myapp -n 100 --no-pager

journalctl -u sshd --since "1 hour ago"
journalctl --since "2024-03-01" --until "2024-03-18"
journalctl -p err -b
journalctl -u myapp -p err..crit

# Boot navigation
journalctl -b -1                   # previous boot (crash analysis)
journalctl --list-boots
journalctl -b <boot id>            # specific boot id

# Kernel only
journalctl -k

journalctl _EXE=/usr/bin/nginx
journalctl _UID=1000 --since today

journalctl -u myapp -o json | jq .
journalctl --utc --no-pager

journalctl --disk-usage
sudo journalctl --vacuum-size=500M
sudo journalctl --vacuum-time=1week
```

| Symptom | Check | Fix |
|---------|-------|-----|
| No entries | Wrong unit/boot | `systemctl status`; `--list-boots`; `-b -1` |
| Logs gone after reboot | Volatile storage | `Storage=persistent` in journald.conf |
| Permission denied | Not in group | `sudo` or `systemd-journal` group |
| Disk full from journal | Unbounded debug | vacuum; tune `SystemMaxUse=` |

## Mistakes to Avoid
- **Mistake:** `--vacuum-time=1s` on the whole journal without export
- **Mistake:** Forgetting `--no-pager` in automation
- **Mistake:** Expecting Docker/k8s app logs under the host process name always

## Pros/Cons or Trade-offs
- **Pro:** Structured, filterable, boot-aware.
- **Con:** Local ring buffer — not long-term SIEM; pager breaks scripts.
- **Trade-off:** Persistent journal vs disk budget.

## Comparison
- vs flat `/var/log` files: journal is unit-keyed binary


### Use cases
- First look after a failed unit (`-u … -b -p err`), crash analysis on previous…
