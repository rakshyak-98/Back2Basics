[[journalctl]] [[services/systemd]] [[etc files]] [[grep]]

# loggging

> Centralizes kernel and service messages in the journal and classic text files under `/var/log` — triage both paths in incidents.

```txt
        loggging ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows you use `journalctl` on systemd hosts, know persistent vs volatile jour…

## Sources
- [journald.conf(5)](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html) — deep-dive
- [man journalctl](https://man7.org/linux/man-pages/man1/journalctl.1.html) — deep-dive

## Key Concepts
- **journald first:** unit-scoped follow with `journalctl -u`.
- **Classic files:** still present for auth, mail, and non-journal apps.
- **Persistence:** volatile under `/run/log/journal` vs persistent `/var/log/journal`.
- **Priority filters:** `-p err` and `--since` shrink noise fast.


- **Core:** Modern systemd hosts use journald (`journalctl`) as the primary store

## Technical Details
```bash
journalctl -b
journalctl -u nginx -f
journalctl --since "1 hour ago" -p err
journalctl -k
dmesg -T
```

| Path | Typical content |
|------|-----------------|
| `/var/log/syslog` | General (Debian) |
| `/var/log/messages` | General (RHEL) |
| `/var/log/auth.log` | SSH, sudo (Debian) |
| `/var/log/secure` | Auth (RHEL) |
| `/var/log/kern.log` | Kernel |

```bash
sudo tail -F /var/log/syslog
grep -i error /var/log/syslog | tail
```

```ini
[Journal]
Storage=persistent
SystemMaxUse=1G
```

## Mistakes to Avoid
- **Mistake:** Assuming journals survive reboot when `Storage=` is still volati…
- **Mistake:** Ignoring classic `/var/log` paths on hosts that still write them
- **Mistake:** Grepping forever without `--since` / `-p` on busy hosts

## Pros/Cons or Trade-offs
- **Pro:** Structured, queryable journal with unit metadata.
- **Con:** Volatile journals lose history across reboot; disk caps need tuning.

## Comparison
- vs [[journalctl]]: that note is the CLI; this note is the logging surface (journal + files).
- vs remote SIEM: local logs are first hop; forwarders ship off-box.


### Use cases
- Follow a failing unit with `journalctl -u … -f`, then correlate with `/var/lo…
