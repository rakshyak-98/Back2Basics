[[systemd]] [[busctl]] [[systemctl]] [[systemd-hostnamed]] [[Service masking]]

# D-Bus

> Linux IPC message bus — services expose methods and signals; desktop environments and systemd lean on it heavily.

```txt
        D-Bus ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Know system vs session bus, well-known names, activation-on-call, and `busctl…

## Sources
- [D-Bus Specification](https://dbus.freedesktop.org/doc/dbus-specification.html) — deep-dive
- [Wikipedia — D-Bus](https://en.wikipedia.org/wiki/D-Bus) — overview

## Key Concepts
- **System vs session:** machine-wide vs per-user login session.
- **Well-known name:** e.g. `org.freedesktop.hostname1` claimed by a service.
- **Method vs signal:** RPC call vs publish/subscribe event.
- **Activation:** first call may spawn the providing service.

## Technical Details
```txt
client ──method call──► dbus-daemon/broker ──► service
         ◄── signal ───────────────────────────┘
system bus: /run/dbus/system_bus_socket
session:    $DBUS_SESSION_BUS_ADDRESS
```

```bash
busctl list
busctl tree org.freedesktop.systemd1
busctl introspect org.freedesktop.hostname1 /org/freedesktop/hostname1
busctl call org.freedesktop.hostname1 /org/freedesktop/hostname1 \
  org.freedesktop.DBus.Properties Get ss org.freedesktop.hostname1 Hostname
echo "$DBUS_SESSION_BUS_ADDRESS"
```

| Knob | Why it matters |
|------|----------------|
| Policy in `/etc/dbus-1/` | Who may call what |
| Activation units | `.service` + `.dbus` pairing |

| Symptom | Check | Fix |
|---------|-------|-----|
| Name has no owner | Service down | Start unit; check activation |
| Access denied | Policy | Fix dbus policy / polkit |
| No session bus | Headless SSH | linger / systemd --user |
| Hang on call | Dead service | `busctl monitor`; restart provider |

## Mistakes to Avoid
- **Mistake:** Calling the session bus as root expecting system services
- **Mistake:** Triggering heavy desktop activation from a headless script unint…
- **Mistake:** Using D-Bus as a high-throughput data plane

## Pros/Cons or Trade-offs
- **Pro:** Discoverable local control plane with introspection.
- **Con:** Wrong bus address and activation side effects confuse newcomers.

## Comparison
- vs gRPC/HTTP: those are cross-host; D-Bus is local machine IPC.
- vs raw UNIX sockets: D-Bus adds naming, typing, and policy.


### Use cases
- `hostnamectl` and many desktop settings UIs are D-Bus clients
