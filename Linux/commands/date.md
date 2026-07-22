[[Scripting]] [[crontab]] [[Linux system management]]

# date

> One-line: **GNU date arithmetic and formatting** — compute timestamps for certs, TTLs, cron windows, and log correlation. `-d` is GNU-specific; don't assume on Alpine/BusyBox.

## Mental model

`date` reads/writes the **system clock** (via `timedatectl` / NTP underneath). For scripting, you care about **format strings** (`+%s`, `+%Y-%m-%d`) and **relative parsing** (`-d "+7 days"`). Wrong timezone assumption is the #1 bug — always know if you need UTC (`-u`) or local.

```
Human string ──date -d──► epoch (+%s) ──► compare in bash/jq
epoch ──date -d @N──► human (debug logs)
```

| Flag / format | Meaning |
|---------------|---------|
| `-d STR` | Parse STR (GNU); relative or absolute |
| `-u` | UTC for output/parsing |
| `+%s` | Unix epoch seconds |
| `+%Y-%m-%dT%H:%M:%SZ` | ISO-8601 UTC (with `-u`) |
| `-d @EPOCH` | Epoch → human |

## Standard config / commands

```bash
# Relative future (expiry checks, cookie TTL)
date -d "+7 days" +%s
date -d "+30 minutes" +%F\ %T
date -d "+1 year" +%Y-%m-%d

# Absolute → epoch (UTC)
date -u -d "2026-12-31 23:59:59" +%s

# Epoch → human (log correlation)
date -d @1704067200
date -u -d @1704067200 +%Y-%m-%dT%H:%M:%SZ

# ISO now for ticket IDs / backup names
date -u +%Y-%m-%dT%H:%M:%SZ
date +%F   # local date only: 2026-07-22

# Yesterday / last hour (reporting windows)
date -d "yesterday" +%F
date -d "1 hour ago" +%F\ %H:%M:%S

# Compare cert expiry (example)
expiry_epoch=$(date -d "$(openssl x509 -enddate -noout -in cert.pem | cut -d= -f2)" +%s)
now_epoch=$(date +%s)
(( expiry_epoch - now_epoch < 86400*14 )) && echo "renew within 14 days"
```

**System time (not date(1) but paired):**

```bash
timedatectl status              # NTP sync state — fix before trusting date math
timedatectl set-timezone UTC    # Servers: usually UTC; apps convert for users
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `date: invalid date` | GNU vs BusyBox | Install `coreutils`; on macOS use `gdate` or python |
| Off by hours in logs | `timedatectl`; `date +%Z` | TZ mismatch; set UTC on servers |
| Cron ran "wrong" hour | `/etc/localtime`, DST | Use UTC in crontab for global fleets |
| `-d @0` wrong century | Epoch unit (s vs ms) | Divide ms timestamps by 1000 |
| Future date parses as past | Locale date order | Use ISO `2026-07-22` form |

## Gotchas

> [!WARNING]
> **GNU `-d` on non-GNU** — Alpine `busybox date` lacks `-d`. Scripts need `python3 -c` or portable checks.

> [!WARNING]
> **Leap seconds / DST boundaries** — `date -d "2026-03-29 02:30"` may be ambiguous in local TZ. Use UTC for automation.

- **`date -s` sets clock** — requires root; can break NTP/chrony if abused.
- **Subsecond** — `+%s` is seconds only; use `%3N` (GNU) for milliseconds in filenames.

## When NOT to use

- **Durations in application logic** — use language/stdlib (monotonic clocks for timeouts).
- **Distributed ordering** — wall clock skew across nodes; use logical clocks or NTP discipline first.

## Related

[[Scripting]] [[crontab]] [[Linux system management]] [[journalctl]]
