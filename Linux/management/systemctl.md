[[systemd]] [[journalctl]] [[system service unit files]] [[Service masking]] [[Error status code]] [[Services commands]] [[commands/systemctl]] [[services/systemd]]

# systemctl

> CLI for systemd — start/stop/enable units, inspect state, and reload after unit-file edits.

## Interview Relevance

Daily muscle memory: status first, enable ≠ start, daemon-reload after edits, mask vs disable, reload vs restart.

## Sources

- [systemctl(1)](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) — deep-dive
- [systemd documentation index](https://www.freedesktop.org/software/systemd/man/latest/) — overview

## Key Concepts

- **start/stop:** runtime only — not boot persistence.
- **enable/disable:** boot symlinks under `*.wants`.
- **reload vs restart:** config reread (needs `ExecReload=`) vs full bounce.
- **daemon-reload:** rescan units after file edits.
- **isolate:** switch target — can tear down the session.

## Technical Details

```txt
systemctl <verb> <unit>
        │
        ▼
   systemd (PID 1) ──► fork/exec, cgroup, journal
```

Story: inspect → edit unit/drop-in → `daemon-reload` → restart/enable.

```bash
systemctl status ssh.service
systemctl is-active ssh
systemctl is-enabled ssh
systemctl start ssh
systemctl stop ssh
systemctl restart ssh
systemctl reload ssh
systemctl reload-or-restart ssh
systemctl enable --now ssh
systemctl disable ssh
systemctl mask ssh
systemctl unmask ssh
sudo systemctl daemon-reload
systemctl cat ssh
systemctl edit ssh
systemctl show ssh -p FragmentPath
systemctl --failed
systemctl reset-failed
systemctl list-units --type=service --state=running
systemctl list-unit-files --type=service
systemctl get-default
systemctl list-dependencies ssh.service
systemd-analyze blame
systemd-analyze critical-chain
```

| Knob | Why it matters |
|------|----------------|
| Unit suffix | sockets/timers need full name |
| `--user` | User bus vs system bus |
| drop-ins | Package-proof overrides |
| `FragmentPath` | Which file actually loaded |

Unit search order: `/etc/systemd/system` → `/run` → `/usr/lib/systemd/system`.

| Symptom | Check | Fix |
|---------|-------|-----|
| Changes ignored | `daemon-reload`? | Reload + restart |
| Unit not found | Path/name; `cat` | Correct name; file under `/etc` |
| Failed on boot | `--failed`; journal | Fix ExecStart/deps |
| Reload no-ops | No `ExecReload=` | Use restart |
| Slow boot | `systemd-analyze blame` | Disable unused; fix slow units |

## Real-World Applications

Incident on sshd: `status` → journal → fix drop-in → `daemon-reload` → `restart`, confirm `is-enabled` for reboot survival.

## Pros/Cons or Trade-offs

- **Pro:** One CLI for lifecycle, deps, and failure inventory.
- **Con:** Wrong verb (`reload`/`isolate`) surprises operators.

## Comparison

- vs [[commands/systemctl]]: sibling command note in `commands/`; this one lives under management with deeper analyze/list coverage.
- vs SysV `service`: prefer systemctl on systemd hosts.

## Mistakes to Avoid

- Restart when reload was enough (or reload when unsupported).
- `isolate` as a casual toggle.
- Setting shell `ulimit` and expecting services to inherit — use `LimitNOFILE=` in the unit.
- Using systemctl inside minimal containers without systemd.
