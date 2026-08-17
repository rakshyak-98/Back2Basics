[[Scripting]] [[crontab]] [[NTP sync]] [[journalctl]]

# date

> date prints or sets the system clock — for scripts you care about format strings, UTC (`-u`), and GNU `-d` relative parsing.

```txt
        date ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Scripting staple: epoch vs ISO, TZ pitfalls, and knowing GNU `date -d` is not…

## Sources
- [date(1) — GNU coreutils](https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html) — deep-dive
- [timedatectl(1)](https://www.freedesktop.org/software/systemd/man/latest/timedatectl.html) — overview

## Key Concepts
- **`+%s` / `@epoch`:** Unix seconds ↔ human.
- **`-u`:** UTC output/parse — prefer on servers.
- **`-d STR`:** GNU parse (“+7 days”, ISO strings).
- **TZ env:** Overrides local timezone for one command.
- **Wall clock vs monotonic:** Don’t use date for timeout intervals in apps.


- **Core:** `date` reads (and with root can set) the **system clock**

## Technical Details
```bash
date -d "+7 days" +%s
date -d "+30 minutes" +%F\ %T
date -u -d "2026-12-31 23:59:59" +%s

date -d @1704067200
date -u -d @1704067200 +%Y-%m-%dT%H:%M:%SZ
date -u +%Y-%m-%dT%H:%M:%SZ
date +%F

date -d "yesterday" +%F
date -d "1 hour ago" +%F\ %H:%M:%S

expiry_epoch=$(date -d "$(openssl x509 -enddate -noout -in cert.pem | cut -d= -f2)" +%s)
now_epoch=$(date +%s)

timedatectl status
timedatectl set-timezone UTC
```

| Symptom | Check | Fix |
|---------|-------|-----|
| invalid date | GNU vs BusyBox | coreutils; `gdate` on macOS; Python |
| Off by hours in logs | `date +%Z`; timedatectl | Align TZ; use UTC on servers |
| Cron wrong hour | DST / localtime | UTC crontabs for global fleets |
| `@0` wrong century | ms vs s epoch | Divide ms by 1000 |

## Mistakes to Avoid
- **Mistake:** Assuming BusyBox/Alpine `date` supports GNU `-d`
- **Mistake:** Mixing local and UTC in distributed log correlation
- **Mistake:** Using millisecond timestamps with `+%s` without converting

## Pros/Cons or Trade-offs
- **Pro:** Ubiquitous formatting for shells and tickets.
- **Con:** Portability traps; DST ambiguity in local TZ.
- **Trade-off:** Set clock with `date -s` vs letting chrony/timesyncd own it.

## Comparison
- vs [[NTP sync]]/timedatectl: those discipline the clock


### Use cases
- Backup filename stamps, cert expiry checks, and converting log epochs to huma…
