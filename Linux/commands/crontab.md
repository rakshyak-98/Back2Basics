[[systemd]] [[bash script]] [[Linux system management]]

# crontab

> One-line: per-user job scheduler — minute/hour/day/month/weekday triggers for scripts and one-liners. **Still everywhere; systemd timers are the modern alternative on server distros.**

## Mental model

`cron` reads `/var/spool/cron/crontabs/<user>` (or `/etc/cron.d/*` for system jobs). The **crond** daemon wakes every minute, checks whether any entry's five fields match *now*, and spawns the command in a minimal environment (not your interactive shell).

```
* * * * *  command
│ │ │ │ │
│ │ │ │ └── weekday (0-7, 0 and 7 = Sunday)
│ │ │ └──── month (1-12)
│ │ └────── day of month (1-31)
│ └──────── hour (0-23)
└────────── minute (0-59)
```

| Location | Who | Typical use |
|----------|-----|-------------|
| `crontab -e` (user) | That user | Backups, reports, app maintenance |
| `/etc/cron.d/` | root-defined, can set user field | Package-installed jobs |
| `/etc/cron.{hourly,daily,weekly,monthly}/` | Scripts dropped in dir | anacron-friendly batch jobs |
| `@reboot` | Once at boot | Legacy "start my thing" — prefer [[systemd]] unit |

Environment is **sparse**: often only `HOME`, `LOGNAME`, `SHELL`, `PATH=/usr/bin:/bin`. Always use absolute paths for scripts and binaries.

## Standard config / commands

```bash
# Edit current user's crontab
crontab -e

# List installed jobs
crontab -l

# Install from file (replaces existing)
crontab /path/to/backup.cron

# Remove all jobs for user
crontab -r

# Example entries
```

```cron
# At 5, 15, 25 minutes past every hour
5,15,25 * * * * /usr/local/bin/check-disk.sh

# Weekdays at 10:00 — note absolute path
0 10 * * 1-5 /opt/app/bin/daily-report.sh >> /var/log/report.log 2>&1

# Every 15 minutes
*/15 * * * * /usr/local/bin/healthcheck.sh

# Monthly, 1st at 03:00
0 3 1 * * /usr/local/bin/monthly-archive.sh

# @ shortcuts
@reboot /usr/local/bin/start-worker.sh
@daily  /usr/local/bin/rotate-logs.sh
```

**Production-safe wrapper pattern:**

```cron
*/5 * * * * /usr/bin/flock -n /var/lock/myjob.lock /opt/app/bin/job.sh >> /var/log/myjob.log 2>&1
```

- `flock -n` — skip if previous run still going (prevents overlap pile-up).
- `>> … 2>&1` — capture stderr; cron emails root on any stdout/stderr unless redirected.

```bash
# Inspect system-wide cron
ls -la /etc/cron.d/
cat /etc/crontab                    # system crontab (has user column)
grep -r . /etc/cron.d/

# Verify cron daemon is running
systemctl status cron              # Debian/Ubuntu
systemctl status crond             # RHEL/CentOS
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Job never runs | `crontab -l`; `systemctl status cron` | Re-enable cron; fix typo in time fields |
| Runs but fails silently | Mail to root (`/var/mail/root`); add logging | Redirect `>> /var/log/job.log 2>&1`; run command manually as same user |
| "Command not found" | Minimal `PATH` in cron | Use full paths: `/usr/bin/python3`, not `python3` |
| Permission denied | Job runs as wrong user | `crontab -u www-data -e`; check file mode (`chmod +x`) |
| Works in shell, fails in cron | Missing env vars, relative paths, no `cd` | Set `SHELL`, `PATH`, `HOME` in crontab header or script; `cd /opt/app && ./run.sh` |
| Duplicate runs / overlap | Long-running job + frequent schedule | `flock`; widen interval; use systemd timer with `OnUnitActiveSec` |
| `%` in command breaks | `%` is newline in crontab | Escape as `\%` or put command in a script |

## Gotchas

> [!WARNING]
> **Cron uses the system timezone** unless `CRON_TZ=` is set in the crontab. DST transitions can skip or double-fire hours — use UTC for critical jobs.

> [!WARNING]
> **`day-of-month` and `day-of-week` are OR, not AND** — `0 10 1 * 1` runs on the 1st *or* on Mondays, not "first Monday".

> [!WARNING]
> **No output = success from cron's view** — failures that produce no stderr may go unnoticed. Always log explicitly.

> [!WARNING]
> **Editing `/var/spool/cron/` directly** — use `crontab -e`; direct edits can be overwritten or miss syntax validation.

## When NOT to use

- **Sub-minute scheduling** → systemd timer, supervisor, or app-internal scheduler.
- **Boot-order dependencies** → [[systemd]] unit with `After=` / `Requires=`.
- **One-shot delayed tasks** → `at`, not cron.
- **Complex retry/backoff** → dedicated job runner (Sidekiq, Celery, Airflow), not cron loops.

## Related

[[systemd]] [[bash script]] [[Linux system management]] [[Services commands]]
