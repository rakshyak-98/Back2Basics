[[D-Bus]] [[systemd]] [[Services commands]] [[systemctl]]

# busctl

> One-line: **systemd's D-Bus introspection CLI** — list services, call methods, monitor signals on system/session bus without raw `dbus-send` XML. **Ships with systemd; the operator-facing D-Bus debugger.**

## Mental model

D-Bus is the IPC bus desktop and server daemons use to expose APIs (hostname changes, login events, NetworkManager, logind). **busctl** wraps libsystemd's bus API — same world as `systemctl`, `hostnamectl`, `loginctl`.

```
Client ──► D-Bus daemon (/run/dbus/system_bus_socket)
              ▲
         busctl list / call / monitor
              │
         systemd, NetworkManager, polkit, …
```

| Bus | Socket | Scope |
|-----|--------|-------|
| System | `/run/dbus/system_bus_socket` | Machine-wide (`--system`, default for root) |
| Session | `$DBUS_SESSION_BUS_ADDRESS` | Per-user desktop (`--user`) |

**vs related tools:**

| Tool | Role |
|------|------|
| `busctl` | Structured introspect + call (systemd) |
| `dbus-send` | Low-level message send (legacy) |
| `dbus-monitor` | Raw traffic tap |
| `gdbus` | GLib helper (GNOME stack) |

## Standard config / commands

```bash
# List active bus names
busctl list
busctl --user list

# Tree of objects on a service
busctl tree org.freedesktop.systemd1

# Introspect methods/properties on an object
busctl introspect org.freedesktop.systemd1 /org/freedesktop/systemd1

# Read a property
busctl get-property org.freedesktop.systemd1 \
  /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager Version

# Call a method (unit list slice)
busctl call org.freedesktop.systemd1 \
  /org/freedesktop/systemd1 \
  org.freedesktop.systemd1.Manager ListUnits

# Monitor traffic (noisy — narrow in prod)
busctl monitor
busctl monitor org.freedesktop.login1

# Capture to pcap for wireshark
busctl capture > dbus.pcap
```

**Common incident patterns:**

```bash
# Who owns the system bus?
busctl status

# Is systemd responding on D-Bus?
busctl introspect org.freedesktop.systemd1 /org/freedesktop/systemd1 | head

# Hostname API (same backend as hostnamectl)
busctl get-property org.freedesktop.hostname1 \
  /org/freedesktop/hostname1 org.freedesktop.hostname1 Hostname
```

Pair with [[Services commands]]:

```bash
systemctl --failed
journalctl -u dbus -u NetworkManager --since "10 min ago"
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Failed to connect to bus` | dbus daemon down | `systemctl status dbus`; `systemctl start dbus` |
| Session bus errors in desktop app | `echo $DBUS_SESSION_BUS_ADDRESS` | Re-login; `dbus-launch` for bare X |
| `busctl list` empty/minimal | Wrong bus (`--user` vs system) | Add `--system` or run as session user |
| Method call AccessDenied | polkit policy | Run as root; check polkit rules; use intended user session |
| systemd D-Bus hangs | systemd overload/deadlock | [[journalctl]] `-u systemd`; safe reboot |
| Monitor floods terminal | Broad `busctl monitor` | Filter by service: `busctl monitor org.freedesktop.systemd1` |

## Gotchas

> [!WARNING]
> **`busctl monitor` on production** — high volume; can impact debugging session. Narrow service; use time bounds.

> [!WARNING]
> **Session vs system bus** — `hostnamectl` as user uses polkit → system bus; your script in cron has **no session bus**.

> [!WARNING]
> **Method signatures matter** — wrong `busctl call` types cause opaque errors. Always `introspect` first.

> [!WARNING]
> **Not every daemon is on D-Bus** — legacy services may only expose sockets or [[systemctl]] units.

## When NOT to use

- **Simple service restart** → [[systemctl]].
- **GNOME-specific APIs** → sometimes easier with `gdbus`.
- **Remote machines** → SSH + busctl locally; D-Bus doesn't tunnel by default.
- **Performance tracing** → eBPF, app metrics — not bus introspection.

## Related

[[D-Bus]] [[systemd]] [[Services commands]] [[systemctl]] [[systemd-hostnamed]]
