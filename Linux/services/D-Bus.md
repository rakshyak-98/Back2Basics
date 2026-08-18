[[systemd]] [[busctl]] [[systemctl]]

# D-Bus

> D-Bus is the Linux IPC message bus — services expose methods/signals; desktop and systemd lean on it heavily.

## Mental model

**Say it in one breath:** system bus is machine-wide; session bus is per-login; clients call well-known names.

```txt
client ──method call──► dbus-daemon/broker ──► service
         ◄── signal ───────────────────────────┘
system bus: /run/dbus/system_bus_socket
session:    $DBUS_SESSION_BUS_ADDRESS
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **system vs session** | Machine vs user | “systemd on system; apps on session.” |
| --- | --- | --- |
| **well-known name** | e.g. `org.freedesktop…` | “Claimed by the service.” |
| **method / signal** | RPC vs event | “Call vs subscribe.” |
| **busctl / gdbus** | Introspect/call | “Discover APIs live.” |
| **activation** | Start on demand | “First call may spawn the service.” |

## Standard config / commands

```bash
busctl list
busctl tree org.freedesktop.systemd1
busctl introspect org.freedesktop.hostname1 /org/freedesktop/hostname1
busctl call org.freedesktop.hostname1 /org/freedesktop/hostname1 \
  org.freedesktop.DBus.Properties Get ss org.freedesktop.hostname1 Hostname
echo "$DBUS_SESSION_BUS_ADDRESS"
```

| Knob | Why it matters |

| Policy in `/etc/dbus-1/` | Who may call what |
| --- | --- |
| Activation units | `.service` + `.dbus` pairing |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Name has no owner | Service down | Start unit; check activation |
| Access denied | Policy | Fix dbus policy / polkit |
| No session bus | Headless SSH | `loginctl enable-linger` / systemd --user |
| Hang on call | Dead service | `busctl monitor`; restart provider |

## Gotchas

> [!WARNING]
> **Root on session bus** ≠ system bus — pick the right address.

> [!WARNING]
> **Activation surprises** — a method call may start heavy desktop components.

## When NOT to use

- **Cross-host RPC** — use gRPC/HTTP; D-Bus is local.
- **High-throughput data plane** — use shared memory/sockets; D-Bus is control plane.

## Related

[[busctl]] [[systemd]] [[systemd-hostnamed]] [[Service masking]]
