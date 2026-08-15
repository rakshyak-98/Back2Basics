[[systemd]] [[Services commands]] [[journalctl]] [[Service masking]] [[system service unit files]] [[commands]]

# systemctl

> Controls systemd units — start/stop/enable/status — the everyday service remote control.

## Interview Relevance

Classic trap: **enable ≠ start**. Interviewers also want mask vs disable and `daemon-reload` after unit edits.

## Sources

- [systemd.systemctl(1)](https://www.freedesktop.org/software/systemd/man/systemctl.html) — deep-dive
- [Wikipedia — systemd](https://en.wikipedia.org/wiki/Systemd) — overview

## Key Concepts

- **enable vs start:** enable links for boot; start runs now — use `--now` for both.
- **active / failed:** runtime state; `status` shows recent journal lines.
- **mask:** stronger than disable — blocks start (even manually) until unmask.
- **daemon-reload:** reread unit files after every change on disk.
- **`--user`:** session/user manager — needs linger for headless user services.

## Technical Details

```txt
systemctl start|stop|restart UNIT
systemctl enable|disable UNIT     # boot links
systemctl status UNIT             # active + recent logs
systemctl daemon-reload           # reread units
```

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

| Symptom | Check | Fix |
|---------|-------|-----|
| inactive (dead) | `status` + journal | Fix ExecStart/environment; start |
| failed | exit code in status | Read journal; fix configuration |
| Changes ignored | unit edit | `daemon-reload` + restart |
| Starts then dies | Restart loop | Fix crash; watch `Restart=` storms |
| masked | `is-enabled` | `unmask` if undo is intentional |

## Real-World Applications

Deploying nginx/postgres as units, enabling on boot after install, and triaging `list-units --failed` after a reboot.

**Example:** After editing a drop-in under `/etc/systemd/system/foo.service.d/`, always `daemon-reload` then `restart`.

## Pros/Cons or Trade-offs

- **Pro:** One CLI for lifecycle, dependencies, and status across the fleet.
- **Con:** Useless inside app containers without systemd — use the orchestrator there.

## Comparison

- vs [[journalctl]]: logs vs control plane — use both in incidents.
- vs [[Service masking]]: mask is the hard block; disable only skips boot start.
- vs OpenRC/SysV: other init systems use different tools ([[SYSV (System V)]]).

## Mistakes to Avoid

- Enabling without starting (or the reverse) and calling the service “on.”
- Restarting mid-`apt` unpack and racing dpkg.
- Forgetting linger for `--user` units on headless hosts: `loginctl enable-linger`.
