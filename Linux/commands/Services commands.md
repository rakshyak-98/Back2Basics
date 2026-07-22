[[systemctl]] [[systemd]] [[D-Bus]] [[busctl]] [[journalctl]]

# Services commands

> One-line: operator cheat sheet for **systemd units** and **D-Bus** introspection — start/stop, failed units, bus traffic. **Modern Linux service management.**

## Mental model

[[systemd]] manages **units** (service, socket, timer, mount). `systemctl` talks to PID 1 over D-Bus. Failed units stay marked until reset. D-Bus ([[busctl]], `dbus-monitor`) is the wire protocol many daemons expose beyond systemd.

```
systemctl ──D-Bus──► systemd ──► unit files ──► processes
                         │
                    busctl / dbus-monitor (other daemons on same bus)
```

| Layer | Tool | When |
|-------|------|------|
| Unit lifecycle | `systemctl` | Start/stop/enable/mask |
| Logs | [[journalctl]] | Why it failed |
| D-Bus API | [[busctl]] | Hostname, login, NM APIs |
| Legacy | `service` | SysV wrapper on some distros |

## Standard config / commands

**systemd — daily ops:**

```bash
# Status & failed inventory (first stop in incidents)
systemctl --failed
systemctl status nginx.service
systemctl list-units --type=service --state=running

# Lifecycle
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx              # if unit supports reload

# Boot persistence
sudo systemctl enable nginx
sudo systemctl disable nginx
sudo systemctl is-enabled nginx

# After unit file edit
sudo systemctl daemon-reload
sudo systemctl restart myapp.service

# Mask — hard block (stronger than disable)
sudo systemctl mask foo.service
sudo systemctl unmask foo.service

# Dependencies
systemctl list-dependencies nginx.service
```

**D-Bus introspection:**

```bash
# Services on system bus
busctl list

# Raw traffic (narrow in prod)
dbus-monitor --system
dbus-monitor --session

# Prefer busctl for structured calls — see [[busctl]]
busctl introspect org.freedesktop.systemd1 /org/freedesktop/systemd1
```

**Journal pairing:**

```bash
journalctl -u nginx.service -b --no-pager
journalctl -u nginx.service -f
journalctl -p err -b
```

**SysV compatibility (avoid for new work):**

```bash
sudo service nginx status               # often wraps systemctl
/etc/init.d/nginx status                # legacy script
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Unit not found` | Typo; not installed | `systemctl list-unit-files \| grep name`; install package |
| `failed` state persists | Old failure recorded | Fix root cause; `systemctl reset-failed` |
| Start → immediate exit | Config error | `journalctl -u svc -b -n 50`; run binary manually as svc user |
| `Job canceled` / timeout | Dependency deadlock | `systemctl list-dependencies --reverse` |
| Port in use | [[ss]] `-lntp` | Stop conflicting unit; change bind |
| D-Bus `Connection refused` | dbus daemon down | `systemctl status dbus`; start dbus |
| Enable doesn't survive reboot | Masked or generator override | `systemctl is-enabled`; check `/etc/systemd/system/` |

## Gotchas

> [!WARNING]
> **`restart` vs `reload`** — reload sends SIGHUP (or unit-specific); many apps only support full restart. Wrong choice drops connections.

> [!WARNING]
> **Forgot `daemon-reload`** after editing `.service` — systemd runs old unit definition until reload.

> [!WARNING]
> **`systemctl stop` on dbus/socket** — can break entire desktop or network stack. Know dependencies before stopping shared infrastructure.

> [!WARNING]
> **`dbus-monitor --system` on busy host** — flood. Filter by service or use [[journalctl]] first.

## When NOT to use

- **Container inner lifecycle** → `docker compose`, k8s probes — host systemctl is outer layer.
- **User session apps** → `systemctl --user` (different bus) or desktop tools.
- **Config file syntax** → edit files in `/etc`; systemctl only applies units.

## Related

[[systemctl]] [[systemd]] [[busctl]] [[D-Bus]] [[journalctl]] [[Services commands]] [[crontab]]
