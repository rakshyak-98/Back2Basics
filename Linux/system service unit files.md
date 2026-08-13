[[services/systemd]] [[system service unit files]] [[management/systemctl]]

# system service unit files

> A systemd unit file is plain INI text that tells PID 1 how to start, supervise, and order a service, socket, timer, or mount.

Unit files live under search paths; **admin overrides in `/etc/systemd/system/` win** over vendor files in `/usr/lib/systemd/system/`. Syntax follows [systemd.syntax(7)](https://www.freedesktop.org/software/systemd/man/latest/systemd.syntax.html).

## Layout

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

## Unit types (common)

| Suffix | Purpose |
|--------|---------|
| `.service` | Daemon or oneshot |
| `.socket` | Socket activation |
| `.timer` | Calendar / monotonic triggers |
| `.target` | Boot milestone grouping |
| `.mount` / `.automount` | Filesystem mounts |

## Drop-in overrides

```bash
sudo systemctl edit myapp.service
# creates /etc/systemd/system/myapp.service.d/override.conf
sudo systemctl daemon-reload
sudo systemctl restart myapp.service
```

## `Type=` matters

| Type | Use when |
|------|----------|
| `simple` | Main process stays foreground (default guess) |
| `forking` | Classic daemon double-forks — needs `PIDFile=` |
| `notify` | Daemon calls `sd_notify(READY=1)` |
| `oneshot` | Runs once; `RemainAfterExit=yes` for setup scripts |

Wrong `Type=` → systemd thinks service is ready when it is not.

## File precedence

| Directory | Role |
|-----------|------|
| `/etc/systemd/system/` | Administrator units and overrides |
| `/run/systemd/system/` | Runtime (generators, transient units) |
| `/usr/lib/systemd/system/` | Package-shipped units |

## Related

[[services/systemd]] · [[management/systemctl]] · [[Service masking]] · [[journalctl]]

## Sources

- [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html)
- [systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)
- Red Hat RHEL 9 unit file guide
