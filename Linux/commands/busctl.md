[[D-Bus]] [[services/systemd]] [[Services commands]] [[systemctl]] [[systemd-hostnamed]] [[journalctl]]

# busctl

> busctl introspects and calls D-Bus APIs — the same IPC bus systemd, NetworkManager, logind, and desktop services use.

## Interview Relevance
Platform debugging: system vs session bus, introspect-before-call, and when to use busctl vs systemctl vs journalctl.

## Sources
- [busctl(1)](https://www.freedesktop.org/software/systemd/man/latest/busctl.html) — deep-dive
- [D-Bus specification](https://dbus.freedesktop.org/doc/dbus-specification.html) — overview

## Core Definition
D-Bus is the machine IPC bus. **busctl** wraps libsystemd’s bus API — list names, walk object trees, get properties, call methods, monitor traffic. Same world as `systemctl`, `hostnamectl`, `loginctl`.

## Key Concepts
- **System vs session bus:** Machine-wide vs per-user desktop (`--user`).
- **Introspect:** Discover methods/signatures before calling.
- **polkit:** Many system-bus methods need authorization.
- **monitor/capture:** Watch or pcap traffic for race hunts.
- **Not every daemon:** Some services only expose sockets/units.

## Technical Details

| Bus | Socket | Scope |
|-----|--------|-------|
| System | `/run/dbus/system_bus_socket` | Machine-wide |
| Session | `$DBUS_SESSION_BUS_ADDRESS` | Per-user desktop |

```bash
busctl list
busctl --user list
busctl tree org.freedesktop.systemd1
busctl introspect org.freedesktop.systemd1 /org/freedesktop/systemd1

busctl get-property org.freedesktop.systemd1 \
  /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager Version

busctl call org.freedesktop.systemd1 \
  /org/freedesktop/systemd1 \
  org.freedesktop.systemd1.Manager ListUnits

busctl monitor org.freedesktop.login1
busctl capture > dbus.pcap
busctl status
```

| Tool | Role |
|------|------|
| `busctl` | Structured introspect + call |
| `dbus-send` | Low-level legacy send |
| `dbus-monitor` | Raw traffic tap |
| `gdbus` | GLib/GNOME helper |

| Symptom | Check | Fix |
|---------|-------|-----|
| Failed to connect to bus | dbus down | `systemctl status dbus` |
| Session bus errors | `$DBUS_SESSION_BUS_ADDRESS` | Re-login; session for desktop |
| AccessDenied | polkit | Root or correct user session |
| Monitor floods | Broad monitor | Filter by service name |

## Real-World Applications
Confirming hostname1 properties match `hostnamectl`, debugging logind seat issues, and verifying systemd still answers on D-Bus during weird hangs.

## Pros/Cons or Trade-offs
- **Pro:** Precise API access beyond what CLI wrappers expose.
- **Con:** Verbose; wrong signatures fail opaquely; monitor is noisy.
- **Trade-off:** busctl for API debug vs [[systemctl]] for unit lifecycle.

## Comparison
vs [[systemctl]]: unit start/stop/status. vs [[journalctl]]: logs. vs raw dbus-monitor: busctl is higher-level. Cron has no session bus by default.

## Mistakes to Avoid
- Broad `busctl monitor` on busy production hosts.
- Calling methods without `introspect` for types.
- Expecting a session bus inside cron/SSH without a desktop login.
