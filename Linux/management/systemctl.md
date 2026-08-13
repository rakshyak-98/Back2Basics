[[Linux]] [[systemd]] [[journalctl]] [[system service unit files]] [[Service masking]] [[Error status code]]

# systemctl

> `systemctl` is the CLI for systemd — start/stop/enable units, inspect state, and reload after unit-file edits.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** You don’t send signals by hand; you ask systemd to change a unit’s desired state and it handles dependencies and restarts.

```txt
systemctl <verb> <unit>
        │
        ▼
   systemd (PID 1) ──► fork/exec, cgroup, journal
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **start / stop** | Immediate runtime change | “Doesn’t change boot persistence.” |
| **enable / disable** | Boot persistence | “Symlinks under `multi-user.target.wants`.” |
| **restart vs reload** | Full bounce vs config reread | “Reload needs daemon support (`ExecReload`).” |
| **status** | State + recent logs | “First command on an incident.” |
| **daemon-reload** | Rescan units | “Required after editing unit files.” |
| **isolate** | Switch target | “Dangerous — can kill the GUI session.” |

### How the story goes (4 steps)

1. **Inspect** — `status`, `is-active`, `cat`.
2. **Change configuration** — edit unit or drop-in.
3. **daemon-reload** — teach systemd the new text.
4. **restart / enable** — apply runtime and boot policy.

---

## Standard config / commands

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
systemctl mask ssh          # stronger — see [[Service masking]]
systemctl unmask ssh

sudo systemctl daemon-reload
systemctl cat ssh
systemctl edit ssh          # drop-in override
systemctl show ssh -p FragmentPath

systemctl --failed
systemctl reset-failed
systemctl list-units --type=service --state=running
systemctl list-unit-files --type=service

systemctl get-default
systemctl set-default multi-user.target
systemctl list-dependencies ssh.service

systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain
```

| Knob | Why it matters |
|------|----------------|
| Unit name suffix | `.service` assumed often; sockets/timers need full name |
| `--user` | User bus vs system bus |
| drop-ins `*.d/override.conf` | Safe package-proof overrides |
| `FragmentPath` | Which file actually loaded |

Unit search order: `/etc/systemd/system` → `/run` → `/usr/lib/systemd/system`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Changes ignored | `daemon-reload`? | Reload + restart |
| `Unit not found` | Path/name; `cat` | Correct name; put file under `/etc` |
| Failed on boot | `systemctl --failed`; journal | Fix ExecStart/deps |
| Reload no-ops | No `ExecReload=` | Use restart |
| Slow boot | `systemd-analyze blame` | Disable unused; fix slow units |

---

## Gotchas

> [!WARNING]
> **`restart` drops connections; `reload` may not exist.** Know what the vendor unit supports.

> [!WARNING]
> **`isolate graphical.target` / `multi-user.target`** can tear down the running session — not a casual toggle.

> [!WARNING]
> **Typos in overrides** fail at reload — always `status` after.

> [!WARNING]
> **Shell `ulimit` ≠ service limits.** Set `LimitNOFILE=` in the unit / drop-in.

---

## When NOT to use

- **Non-systemd hosts** (old SysV/OpenRC) — use `service`/`rc-service` for that platform.
- **Inside a minimal container without systemd** — supervise with the orchestrator, not nested systemctl.
- **Ad-hoc one-liners** — don’t wrap every cron tick as a transient unit unless you need deps/journal.

---

## Related

[[systemd]] [[journalctl]] [[system service unit files]] [[Service masking]] [[Error status code]] [[Services commands]]
