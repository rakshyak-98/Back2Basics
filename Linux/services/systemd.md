[[Linux]] [[systemctl]] [[journalctl]] [[system service unit files]] [[Service masking]] [[Error status code]] [[SYSV (System V)]] [[Services commands]] [[commands/systemctl]]

# systemd

> PID 1 on modern Linux — starts units in parallel, tracks dependencies, and restarts services declared in unit files.

```txt
        systemd ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Core Linux ops: units vs targets, enable ≠ start, Wants vs Requires, daemon-r…

## Sources
- [systemd documentation index](https://www.freedesktop.org/software/systemd/man/latest/) — deep-dive
- [Wikipedia — systemd](https://en.wikipedia.org/wiki/Systemd) — overview

## Technical Details
```txt
kernel
  └─ systemd (PID 1)
        ├─ .service   daemons
        ├─ .socket    socket activation
        ├─ .timer     cron-like
        ├─ .mount / .path / …
        └─ .target    milestones (multi-user.target ≈ “runlevel 3”)
```

1. **Boot** — reach default target; start wanted units (often parallel).
2. **Supervise** — track main PID; optional restart on crash.
3. **Operate** — [[systemctl]] for start/stop/status.
4. **Change** — unit under `/etc/systemd/system`, `daemon-reload`, enable/start.

| Path | Role |
|------|------|
| `/etc/systemd/system/` | Admin overrides — wins |
| `/run/systemd/system/` | Runtime |
| `/usr/lib/systemd/system/` | Packages (distro) |

```bash
ps -p 1 -o comm=
systemctl get-default
systemctl list-units --type=service --state=running
systemctl status ssh.service
systemctl cat ssh.service
sudo systemctl daemon-reload
sudo systemctl enable --now myapp.service
journalctl -u myapp -e
```

```ini
[Unit]
Description=My app
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/myapp
Restart=on-failure
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

| Knob | Why it matters |
|------|----------------|
| `Type=` | Wrong type → “started” but not ready |
| `Restart=` | Crash recovery policy |
| `After=` / `Wants=` | Ordering vs dependency |
| drop-ins | Override without editing package files |

- Legacy map: runlevels ≈ targets (`rescue`, `multi-user`, `graphical`, `reboot…
- Prefer targets; don’t edit `/etc/inittab` on systemd hosts.

| Symptom | Check | Fix |
|---------|-------|-----|
| Active but dead | `Type=forking` without PIDFile | Fix type; use `simple`/`notify` |
| Edit ignored | Forgot `daemon-reload` | Reload then restart |
| Won’t start on boot | `is-enabled`; WantedBy | `enable` unit |
| Exit 203/EXEC | Bad `ExecStart` path | `systemctl cat`; permissions |

## Mistakes to Avoid
- **Mistake:** Confusing enable with start
- **Mistake:** Editing package units under `/usr/lib` instead of `/etc` drop-ins
- **Mistake:** Copying Upstart recipes without checking PID 1 is systemd

## Pros/Cons or Trade-offs
- **Pro:** Parallel boot, dependency graph, consistent control/logging.
- **Con:** Complexity and surprises (`Type=`, activation, mask) for SysV veterans.

## Comparison
- vs [[SYSV (System V)]]: sequential scripts vs declarative units/targets.
- vs Kubernetes: systemd is node-local; orchestrators own multi-host scheduling.


### Use cases
- Ship a vendor app as a unit with `Restart=on-failure`, override environment v…
