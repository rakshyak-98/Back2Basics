[[systemctl]] [[services/systemd]] [[D-Bus]] [[busctl]] [[journalctl]] [[crontab]] [[ss]]

# Services commands

> systemd unit lifecycle plus D-Bus introspection — systemctl for start/stop/enable; journalctl for why; busctl when you need the bus API.

## Interview Relevance
Must-know: enable ≠ start, daemon-reload after unit edits, mask vs disable, and pairing `systemctl status` with `journalctl -u`.

## Sources
- [systemctl(1)](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) — deep-dive
- [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) — deep-dive

## Core Definition
[[services/systemd]] manages **units** (service, socket, timer, mount). `systemctl` talks to PID 1 over D-Bus. Failed units stay marked until reset. D-Bus ([[busctl]]) is how many daemons expose APIs beyond systemd itself.

## Key Concepts
- **start/stop vs enable/disable:** Now vs on boot.
- **daemon-reload:** Reread unit files after edits.
- **mask:** Symlink to `/dev/null` — stronger than disable.
- **reset-failed:** Clear sticky failed state after fix.
- **--user:** Per-user units on the session bus.

## Technical Details

```txt
systemctl ──D-Bus──► systemd ──► unit files ──► processes
```

```bash
systemctl --failed
systemctl status nginx.service
systemctl list-units --type=service --state=running

sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx

sudo systemctl enable nginx
sudo systemctl disable nginx
sudo systemctl is-enabled nginx

sudo systemctl daemon-reload
sudo systemctl restart myapp.service

sudo systemctl mask foo.service
sudo systemctl unmask foo.service
systemctl list-dependencies nginx.service

busctl list
journalctl -u nginx.service -b --no-pager
journalctl -u nginx.service -f
journalctl -p err -b

sudo service nginx status               # legacy wrapper
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Unit not found | Typo; not installed | `list-unit-files`; install package |
| failed persists | Old failure recorded | Fix cause; `reset-failed` |
| Start → immediate exit | Config error | `journalctl -u svc -b -n 50` |
| Port in use | [[ss]] `-lntp` | Stop conflict; change bind |
| Enable doesn't survive reboot | Masked / override | `is-enabled`; check `/etc/systemd/system/` |

## Real-World Applications
Incident first pass (`--failed` + status + journal), deploying a custom `.service`, and masking a dangerous vendor unit that keeps re-enabling.

## Pros/Cons or Trade-offs
- **Pro:** Unified control plane for services, timers, sockets.
- **Con:** Shared infrastructure units (dbus, network) are dangerous to stop casually.
- **Trade-off:** `reload` (graceful) vs `restart` (full bounce).

## Comparison
vs [[SYSV (System V)]] `service`: wrappers around systemd on modern hosts. vs containers: host systemctl is the outer layer; inner lifecycle is compose/k8s. Related: [[busctl]], [[journalctl]].

## Mistakes to Avoid
- Editing a unit and forgetting `daemon-reload`.
- Assuming `reload` works for every app (many need restart).
- Stopping dbus/networkd without understanding dependents.
