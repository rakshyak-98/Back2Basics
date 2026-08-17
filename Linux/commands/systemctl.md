[[systemd]] [[Services commands]] [[journalctl]] [[Service masking]] [[system service unit files]] [[Linux CLI]]

# systemctl

> systemctl is the primary command-line interface to systemd — it starts and stops services, enables boot persistence, reloads unit files, and reports failure state for every managed unit on the host.

---

## Why It Matters

On any Linux server running systemd (RHEL 7+, Debian 8+, Ubuntu 15.04+, most cloud images), `systemctl` is how you answer "is the service running?", "will it survive reboot?", and "why did it fail?". The most common production trap is confusing **enable** (create boot symlinks) with **start** (run now) — a service can be enabled but dead, or running but not enabled. The second trap is editing a unit file without `daemon-reload`, which means systemd keeps using the old definition until you explicitly tell it to rescan.

---

## Sources

- [systemctl(1) — systemd manual](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) — Authoritative reference for every subcommand, flag, and exit code.
- [systemd.unit(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) — Unit file format that systemctl operates on — essential for interpreting `status` and `cat` output.
- [Wikipedia — systemd](https://en.wikipedia.org/wiki/Systemd) — Historical context and architectural overview of PID 1, targets, and the unit dependency graph.

---

## Key Concepts

| Concept | Meaning |
|---------|---------|
| **Unit** | A managed object — `.service`, `.socket`, `.timer`, `.mount`, `.target`, etc. |
| **start / stop / restart** | Runtime only — affects the process right now, not boot behavior. |
| **enable / disable** | Boot persistence — creates or removes symlinks in `*.wants` directories. |
| **enable --now** | Both enable and start in one command — the safe default after install. |
| **reload** | Ask a running service to reread config without full restart — only works if `ExecReload=` is defined. |
| **daemon-reload** | Rescan all unit files on disk — required after every unit file edit. |
| **mask** | Symlink unit to `/dev/null` — stronger than disable; blocks even manual start. |
| **--user** | Operate on the per-user systemd instance — needs `linger` for headless user services. |
| **FragmentPath** | Which file on disk actually loaded — critical when drop-ins override package defaults. |

```txt
systemctl <verb> <unit>
        │
        ▼
   systemd (PID 1) ──► fork/exec, cgroup, journal
        │
        ▼
   journald captures stdout/stderr + structured logs
```

Unit file search order (later wins): `/etc/systemd/system/` → `/run/systemd/system/` → `/usr/lib/systemd/system/`.

---

## Technical Details

### Lifecycle commands

```bash
systemctl status nginx.service --no-pager
systemctl is-active nginx
systemctl is-enabled nginx
systemctl is-failed nginx

sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx              # only if unit defines ExecReload=
sudo systemctl reload-or-restart nginx   # reload if supported, else restart

sudo systemctl enable nginx              # boot symlink only
sudo systemctl enable --now nginx        # enable + start — preferred after install
sudo systemctl disable nginx
```

### After editing unit files

```bash
sudo systemctl edit nginx                # opens drop-in under /etc/systemd/system/nginx.service.d/
sudo systemctl daemon-reload             # MANDATORY after any unit file change
sudo systemctl restart nginx
systemctl cat nginx                      # show effective merged unit
systemctl show nginx -p FragmentPath     # which file loaded
```

### Failure investigation

```bash
systemctl --failed
systemctl reset-failed                   # clear sticky failed state after fix
journalctl -u nginx -b --no-pager | tail -50
journalctl -u nginx -f                   # follow live
systemctl list-dependencies nginx.service
```

### Boot analysis

```bash
systemctl get-default
systemctl list-unit-files --type=service
systemd-analyze blame                    # slowest units at boot
systemd-analyze critical-chain           # dependency chain to default target
```

### Masking (hard block)

```bash
sudo systemctl mask foo.service          # blocks start even manually
sudo systemctl unmask foo.service
```

### Symptom table

| Symptom | Check | Fix |
|---------|-------|-----|
| inactive (dead) | `status` + journal | Fix `ExecStart`/environment; `start` |
| failed (exit code in status) | `journalctl -u UNIT -b` | Fix config or binary path |
| Changes ignored | Did you `daemon-reload`? | `daemon-reload` + restart |
| Starts then dies immediately | Restart loop; watch `Restart=` storms | Fix crash cause in journal |
| masked | `is-enabled` shows masked | `unmask` if intentional undo |
| Unit not found | Typo or not installed | `list-unit-files`; install package |
| reload no-ops | No `ExecReload=` in unit | Use `restart` instead |

---

## Mistakes to Avoid

- Enabling without starting (or starting without enabling) and calling it done.
- Editing a unit file and forgetting `daemon-reload` before restart.
- Using `reload` when the unit does not define `ExecReload=` — it silently does nothing useful.
- Restarting services mid-`apt` unpack — can race with dpkg file replacement.
- Forgetting `loginctl enable-linger` for `--user` units on headless servers.
- Running `systemctl` inside minimal Docker containers that have no systemd — use the container orchestrator instead.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| One CLI for lifecycle, dependencies, and failure inventory | Useless inside containers without systemd |
| Integrates with journald for immediate log context | Wrong verb (`reload` vs `restart`) surprises operators |
| Drop-in overrides survive package upgrades | `isolate` and `emergency` targets can tear down the session |

---

## Comparison

| Tool | Role |
|------|------|
| [[journalctl]] | Read logs — pair with systemctl during incidents |
| [[Service masking]] | Deep dive on mask vs disable semantics |
| `service` (SysV wrapper) | Legacy wrapper that calls systemctl on systemd hosts |
| [[SYSV (System V)]] | Pre-systemd init — different tools entirely |
| Kubernetes / Docker | Orchestrator manages containers — not systemd units inside them |

---

## Use cases

- Deploy nginx or PostgreSQL: `apt install` → `enable --now` → verify with `status`.
- Incident on sshd: `status` → journal → fix drop-in → `daemon-reload` → `restart`.
- Boot regression: `systemd-analyze blame` to find a slow unit delaying multi-user target.
