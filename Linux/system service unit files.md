[[systemd]] [[systemctl]] [[Services commands]]

# system service unit files

> A systemd unit file declares how a service starts, restarts, and is sandboxed — `[Unit]` / `[Service]` / `[Install]`.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** vendor units in `/lib/systemd/system`; overrides in `/etc/systemd/system`; `daemon-reload` then restart.

```txt
myapp.service
  [Unit] Description=… After=network.target
  [Service] ExecStart=… User=… Restart=on-failure
  [Install] WantedBy=multi-user.target
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **unit** | systemd object | “service/socket/timer/…” |
| **drop-in** | `.d/*.conf` override | “Don’t edit vendor files.” |
| **Type=** | simple/exec/forking/notify | “How systemd tracks readiness.” |
| **WantedBy** | enable target | “Creates `.wants` symlink.” |
| **daemon-reload** | Reread units | “After every unit edit.” |

---

## Standard config / commands

```bash
# /etc/systemd/system/myapp.service
# [Unit]
# Description=My app
# After=network-online.target
# [Service]
# Type=simple
# User=myapp
# EnvironmentFile=-/etc/myapp/env
# ExecStart=/usr/local/bin/myapp
# Restart=on-failure
# [Install]
# WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl enable --now myapp
systemctl cat myapp
systemctl show myapp -p FragmentPath,DropInPaths
```

| Knob | Why it matters |
|------|----------------|
| `EnvironmentFile=-` | Optional env; `-` ignores missing |
| `Restart=` | Survive crashes |
| `ProtectSystem=` | Sandbox filesystem |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Changes ignored | Forgot daemon-reload | Reload + restart |
| exit 203/EXEC | Bad ExecStart path | `systemctl cat`; fix binary path |
| Loops restarting | Crash on boot | `journalctl -u`; fix config; `Restart=` |
| Wrong user/env | Unit vs shell | Diff `systemctl show-environment` |
| Override not applied | Wrong drop-in name | `systemctl cat` shows merged |

---

## Gotchas

> [!WARNING]
> **Editing `/lib/systemd/system`** — package upgrades overwrite; use `/etc` drop-ins.

> [!WARNING]
> **`Type=forking` without PIDFile** — systemd loses the main process.

---

## When NOT to use

- **Oneshot host tweaks** — prefer `oneshot` units or plain scripts carefully.
- **application-internal workers** — supervisors inside the application may fight Restart=.

---

## Related

[[systemd]] [[systemctl]] [[Service masking]] [[journalctl]] [[Setup Non-Login user from Running process]]
