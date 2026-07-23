[[journalctl]] [[systemd]] [[Services commands]] [[etc files]]

# Logging (journal & syslog)

> One-line: Linux **log aggregation** — systemd-journald (structured, indexed) plus legacy syslog files under `/var/log`. **Start every service incident with journalctl, not grep of random files.**

## Mental model

Applications log to **stdout/stderr** (captured by journald for systemd units), **syslog** (`/dev/log` socket), or directly to files (`/var/log/app/`). journald stores binary journals under `/var/log/journal/` (persistent) or `/run/log/journal/` (volatile). Priority follows syslog severity: emerg → alert → crit → err → warning → notice → info → debug.

```
app ──stdout──► systemd ──► journald ──► journalctl
app ──syslog──► rsyslog/syslog-ng ──► /var/log/*.log
kernel ──► journald (-k) / dmesg
```

| Source | Tool | Best for |
|--------|------|----------|
| systemd units | [[journalctl]] | Services, boots, priorities |
| Plain files | `less`, [[grep]] | Legacy apps, nginx access.log |
| Kernel | `journalctl -k`, `dmesg` | OOM, driver, hardware |
| Live follow | `journalctl -f` | Deploy watch, incident stream |

## Standard config / commands

**journalctl — primary interface (see [[journalctl]] for full playbook):**

```bash
# Service logs since boot
journalctl -u nginx.service -b --no-pager

# Follow live
journalctl -u myapp.service -f

# Time window
journalctl -u myapp --since "1 hour ago"
journalctl --since "2024-03-01" --until "2024-03-18"

# Errors only (err and above)
journalctl -p err -b
journalctl -u sshd -p err..crit

# Previous boot (crash post-mortem)
journalctl -b -1
journalctl --list-boots

# Kernel ring
journalctl -k
journalctl -k -p err

# JSON for scripts
journalctl -u myapp -o json --no-pager | jq .
```

**Disk usage & retention:**

```bash
journalctl --disk-usage
sudo journalctl --vacuum-size=500M
sudo journalctl --vacuum-time=1week
# /etc/systemd/journald.conf → SystemMaxUse=
```

**Classic file logs:**

```bash
sudo tail -f /var/log/syslog              # Debian rsyslog aggregate
sudo tail -f /var/log/messages            # RHEL
sudo less /var/log/auth.log               # SSH/auth (Debian)
grep -i error /var/log/nginx/error.log
```

**Persistent journal (if missing after reboot):**

```bash
# /etc/systemd/journald.conf
# [Journal]
# Storage=persistent
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
sudo systemctl restart systemd-journald
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No logs for service | Not systemd-managed | Find file path in unit or app config; `lsof \| grep log` |
| Empty after reboot | Volatile journal | Enable `Storage=persistent` |
| Disk full | journal size | `journalctl --vacuum-size`; tune journald.conf |
| Logs stop mid-incident | Rate limit | journald `RateLimitInterval`; app crashed — check `-b -1` |
| Timestamps wrong | RTC/timezone | `timedatectl`; NTP sync |
| `permission denied` | Non-root reading restricted unit | `sudo journalctl` or add user to `systemd-journal` group |
| Duplicate lines | app + rsyslog both file and journal | Normalize logging driver |

## Gotchas

> [!WARNING]
> **Not everything is in journald** — docker default json-file, cron mail to root, custom `/var/log` paths. Know your app's sink.

> [!WARNING]
> **`journalctl --vacuum-time=1s` nukes almost everything** — use size/time vacuum deliberately in prod.

> [!WARNING]
> **UTC vs local** — journalctl displays local by default; correlate with UTC in multi-region incidents (`--utc`).

> [!WARNING]
> **High-volume debug in prod** — filling disk faster than vacuum; revert log level after triage.

## When NOT to use

- **Long-term retention / compliance** → central SIEM (Loki, ELK, CloudWatch), not single-host journal forever.
- **Metrics & traces** → Prometheus/OpenTelemetry — logs are one pillar.
- **Structured query at scale** → export JSON; don't grep huge journals repeatedly.

## Related

[[journalctl]] [[systemd]] [[Services commands]] [[grep]] [[etc files]] [[OOM (Linux Out Of Memory)]]
