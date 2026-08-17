[[services/systemd]] [[management/systemctl]] [[Service masking]] [[journalctl]] [[commands/systemctl]]

# system service unit files

> Plain INI text that tells PID 1 how to start, supervise, and order a service, socket, timer, or mount.

```txt
        system service uni ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Expect `Type=` pitfalls, drop-in overrides under `/etc`, `daemon-reload`, and…

## Sources
- [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) — deep-dive
- [systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) — deep-dive

## Key Concepts
- **`[Unit]` / `[Service]` / `[Install]`:** dependencies, how to run, boot enablement.
- **`Type=`:** simple vs forking vs notify vs oneshot — wrong type means “ready” lies.
- **Drop-ins:** `systemctl edit` → `.d/override.conf` without editing vendor files.
- **Precedence:** `/etc` > `/run` > `/usr/lib`.


- **Core:** Unit files live under search paths

## Technical Details
```ini
[Unit]
Description=Example API
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=app
ExecStart=/usr/local/bin/api --config /etc/api/config.yaml
Restart=on-failure
EnvironmentFile=-/etc/default/api

[Install]
WantedBy=multi-user.target
```

| Suffix | Purpose |
|--------|---------|
| `.service` | Daemon or oneshot |
| `.socket` | Socket activation |
| `.timer` | Calendar / monotonic triggers |
| `.target` | Boot milestone grouping |
| `.mount` / `.automount` | Filesystem mounts |

```bash
sudo systemctl edit myapp.service
sudo systemctl daemon-reload
sudo systemctl restart myapp.service
```

| Type | Use when |
|------|----------|
| `simple` | Main process stays foreground |
| `forking` | Classic double-fork — needs `PIDFile=` |
| `notify` | Daemon calls `sd_notify(READY=1)` |
| `oneshot` | Runs once; `RemainAfterExit=yes` for setup |

| Directory | Role |
|-----------|------|
| `/etc/systemd/system/` | Administrator units and overrides |
| `/run/systemd/system/` | Runtime (generators, transient) |
| `/usr/lib/systemd/system/` | Package-shipped units |

## Mistakes to Avoid
- **Mistake:** Editing vendor units in `/usr/lib` instead of drop-ins
- **Mistake:** Forgetting `daemon-reload` after unit changes
- **Mistake:** Using `Type=simple` for a double-forking daemon (or the reverse)

## Pros/Cons or Trade-offs
- **Pro:** Declarative dependencies, restart policy, and journal integration.
- **Con:** Wrong `Type=` and missing `daemon-reload` cause mysterious “inactive” races.

## Comparison
- vs SysV init scripts: units declare dependencies explicitly ([[SYSV (System V)]]).
- vs [[Service masking]]: mask blocks start; unit files define how start would work.


### Use cases
- Ship an app unit with `Restart=on-failure`, override `EnvironmentFile` via dr…
