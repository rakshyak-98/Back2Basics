[[services/systemd]] [[bash script]] [[Services commands]] [[date]] [[NTP sync]]

# crontab

> crontab schedules commands by minute — crond wakes each minute, matches the five time fields, and runs the job with a minimal environment.

```txt
        crontab ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Know the five fields, DOM/DOW OR semantics, absolute paths, logging, and when…

## Sources
- [crontab(5)](https://man7.org/linux/man-pages/man5/crontab.5.html) — deep-dive
- [cron(8)](https://man7.org/linux/man-pages/man8/cron.8.html) — overview

## Key Concepts
- **Five fields:** minute hour dom month dow.
- **DOM OR DOW:** Both set → either matches (not “first Monday” unless carefully written).
- **`@hourly` etc.:** Shortcuts for common schedules.
- **Timezone:** System TZ unless `CRON_TZ=` set.
- **Silence ≠ success:** Always log; mail may be unset.


- **Core:** User crontabs live under `/var/spool/cron/crontabs/`; system jobs in `/etc/cr…

## Technical Details
```txt
* * * * *  command
│ │ │ │ │
│ │ │ │ └── weekday (0-7, 0 and 7 = Sunday)
│ │ │ └──── month (1-12)
│ │ └────── day of month (1-31)
│ └──────── hour (0-23)
└────────── minute (0-59)
```

```bash
crontab -e
crontab -l
crontab /path/to/backup.cron
crontab -r

# Examples
5,15,25 * * * * /usr/local/bin/job.sh >>/var/log/job.log 2>&1
0 10 * * 1-5 /usr/local/bin/weekday.sh
*/15 * * * * /usr/local/bin/every15.sh
0 3 1 * * /usr/local/bin/monthly.sh
@daily /usr/local/bin/daily.sh

ls /etc/cron.d/
systemctl status cron || systemctl status crond
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Job never runs | `crontab -l`; daemon | Absolute path; PATH; cron service |
| Wrong hour | TZ / DST | `CRON_TZ=` or UTC fleet |
| Ran on wrong days | DOM/DOW OR | Rewrite schedule carefully |
| Failures unnoticed | No logs | Redirect stdout/stderr; alert |

## Mistakes to Avoid
- **Mistake:** Relative paths and assuming interactive `PATH`
- **Mistake:** Editing spool files directly instead of `crontab -e`
- **Mistake:** Assuming DOM+DOW means AND

## Pros/Cons or Trade-offs
- **Pro:** Simple, ubiquitous minute scheduling.
- **Con:** Weak env, tricky calendars, poor dependency/catch-up vs systemd timers.
- **Trade-off:** cron for simple repeats vs [[services/systemd]] timers for calendar + missed runs.

## Comparison
- vs systemd timers: better logging/dependencies/missed runs


### Use cases
- Nightly backups, certificate expiry checks, and rotating temp cleanup
