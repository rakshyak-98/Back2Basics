[[Linux]] [[systemctl]] [[journalctl]] [[system service unit files]] [[Service masking]] [[Error status code]]

# systemd

> systemd is PID 1 on modern Linux — it starts units in parallel, tracks deps, and restarts services you declare in unit files.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Everything is a unit; targets group units; `systemctl` asks systemd to start/stop/enable them without the old SysV runlevel maze.

```txt
kernel
  └─ systemd (PID 1)
        ├─ .service   daemons
        ├─ .socket    socket activation
        ├─ .timer     cron-like
        ├─ .mount / .path / …
        └─ .target    milestones (multi-user.target ≈ “runlevel 3”)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Unit** | One managed object + config | “A service is a unit file systemd supervises.” |
| **Target** | Group / milestone | “`multi-user.target` is our default non-graphical goal.” |
| **Wants vs Requires** | Soft vs hard dependency | “Requires fails the parent if the child fails.” |
| **Enable** | Start on boot | “Enable creates symlinks under `*.wants`.” |
| **daemon-reload** | Rescan unit files | “After editing units, reload then restart.” |
| **Journal** | Central logs | “`journalctl -u foo` beats hunting `/var/log`.” |

### How the story goes (4 steps)

1. **Boot** — systemd reaches default target; starts wanted units (often in parallel).
2. **Supervise** — tracks main PID; optional restart on crash.
3. **Operate** — admins use [[systemctl]] for start/stop/status.
4. **Change** — drop unit in `/etc/systemd/system`, `daemon-reload`, enable/start.

### Unit file locations (precedence)

| Path | Role |
|------|------|
| `/etc/systemd/system/` | Admin overrides — wins |
| `/run/systemd/system/` | Runtime |
| `/usr/lib/systemd/system/` | Packages (distro) |

---

## Standard config / commands

```bash
# Which init?
ps -p 1 -o comm=
strings /sbin/init | grep -i systemd

systemctl get-default
systemctl list-units --type=service --state=running
systemctl status ssh.service
systemctl cat ssh.service

# New service sketch → /etc/systemd/system/myapp.service
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

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now myapp.service
journalctl -u myapp -e
```

| Knob | Why it matters |
|------|----------------|
| `Type=` | `simple`/`forking`/`notify` — wrong type → “started” but not ready |
| `Restart=` | Crash recovery policy |
| `After=` / `Wants=` | Ordering vs dependency |
| drop-ins `foo.service.d/*.conf` | Override without editing package files |

Legacy map: runlevels ≈ targets (`rescue.target`, `multi-user.target`, `graphical.target`, `reboot.target`). Prefer targets; don’t edit `/etc/inittab` on systemd hosts.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Service “active” but dead | `Type=forking` without PIDFile | Fix type; use `simple`/`notify` |
| Edit ignored | Forgot `daemon-reload` | Reload then restart |
| Won’t start on boot | `is-enabled`; WantedBy | `enable` unit |
| Exit 203/EXEC | Bad `ExecStart` path | `systemctl cat`; permissions |
| Black hole logs | Logging to tty only | Journal + `StandardOutput=journal` |

---

## Gotchas

> [!WARNING]
> **`enable` ≠ `start`.** Enable only links for boot; use `enable --now` or start separately.

> [!WARNING]
> **Package files get overwritten.** Put custom units/overrides under `/etc`, not `/usr/lib`.

> [!WARNING]
> **Mask is stronger than disable** — symlink to `/dev/null`; see [[Service masking]].

> [!WARNING]
> **Upstart/`/etc/init` jobs** on ancient Ubuntu are not systemd units — detect PID 1 before copying recipes.

---

## When NOT to use

- **One-shot user scripts in a desktop session** — user timers/services or cron may be simpler.
- **Orchestrating containers across hosts** — Kubernetes/Nomad own that plane; systemd stays node-local.
- **Non-Linux** — launchd/SMF/etc.; don’t assume unit files.

---

## Related

[[systemctl]] [[journalctl]] [[system service unit files]] [[Service masking]] [[Error status code]] [[SYSV (System V)]] [[Services commands]]
