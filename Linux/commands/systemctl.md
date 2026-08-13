<!-- note-strategy: operational -->
[[commands]] [[systemd]] [[Services commands]] [[journalctl]] [[Service masking]]

# systemctl

> `systemctl` controls systemd units — start/stop/enable/status — the everyday service remote control.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `start` is now; `enable` is boot; `status` + `journalctl -u` is debug; `daemon-reload` after unit edits.

```txt
systemctl start|stop|restart UNIT
systemctl enable|disable UNIT     # boot links
systemctl status UNIT             # active + recent logs
systemctl daemon-reload           # reread units
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **enable ≠ start** | Boot vs now | “Need both for ‘always on’.” |
| **active / failed** | Runtime state | “`status` shows the last lines.” |
| **mask** | Block start | “Stronger than disable.” |
| **daemon-reload** | Reload unit files | “After every unit change.” |
| **--user** | User manager | “Session services, not system.” |

---

## Standard config / commands

```bash
systemctl status nginx --no-pager
sudo systemctl restart nginx
sudo systemctl enable --now nginx
systemctl is-enabled nginx
systemctl list-units --failed
sudo systemctl daemon-reload
systemctl cat nginx
journalctl -u nginx -b --no-pager | tail
```

| Knob | Why it matters |
|------|----------------|
| `--now` | enable/disable + start/stop together |
| `--no-pager` | Scripts and SSH |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| inactive (dead) | `status` + journal | Fix ExecStart/env; start |
| failed | exit code in status | Read journal; fix config |
| Changes ignored | unit edit | `daemon-reload` + restart |
| Starts then dies | Restart loop | `Restart=` storm; fix crash |
| masked | `is-enabled` | `unmask` if intentional undo |

---

## Gotchas

> [!WARNING]
> **`restart` during package unpack** can race dpkg — wait for apt to finish.

> [!WARNING]
> **`--user` units** need linger for headless: `loginctl enable-linger`.

---

## When NOT to use

- **Non-systemd systems** — OpenRC/sysv use other tools.
- **Inside application containers without systemd** — use the orchestrator, not systemctl.

---

## Related

[[systemd]] [[Services commands]] [[journalctl]] [[Service masking]] [[system service unit files]]
