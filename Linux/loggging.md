[[journalctl]] [[services/systemd]] [[etc files]]

# loggging

> Linux logging centralizes kernel and service messages in the journal and traditional text files under `/var/log` — know both paths when triaging incidents.

Modern **systemd** hosts use **journald** (`journalctl`) as the primary store; legacy apps still append to `/var/log/*.log`. **rsyslog** / **syslog-ng** may forward to remote collectors.

## journald (primary on systemd)

```bash
# Boot messages
journalctl -b

# Follow unit
journalctl -u nginx -f

# Since time window
journalctl --since "1 hour ago" -p err

# Kernel ring
journalctl -k
dmesg -T
```

## Classic log files

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

## Persistence

Journal may be volatile (`/run/log/journal`) or persistent (`/var/log/journal`). Check `/etc/systemd/journald.conf`:

```ini
[Journal]
Storage=persistent
SystemMaxUse=1G
```

## Related

[[journalctl]] · [[grep]] · [[etc files]]

## Sources

- [journald.conf(5)](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html)
- `man 1 journalctl`
