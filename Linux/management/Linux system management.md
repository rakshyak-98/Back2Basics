[[management]] [[systemctl]] [[Package Manager]] [[loggging]]

# Linux system management

> Day-2 system management is patch, observe, control services, and recover — package updates, systemd, logs, and backups.

---

## Mental model

**Say it in one breath:** keep the box bootable, patched, observable, and reversible — prefer distro tools over one-off hacks.

```txt
patch (apt) → services (systemctl) → logs (journalctl)
                 │
            backup / snapshots before risky change
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **runbook** | Known steps | “Don’t invent under SEV.” |
| **enable vs start** | Boot vs now | “Both usually needed.” |
| **unattended-upgrades** | Auto security updates | “Know what’s automatic.” |
| **journal** | systemd logs | “`-u` + `-b` scopes noise.” |
| **blast radius** | What one change hits | “Canaries before fleet.” |

---

## Standard config / commands

```bash
sudo apt-get update && sudo apt-get upgrade
systemctl status
journalctl -p err -b
uptime; free -h; df -h
sudo needrestart   # if installed
```

| Knob | Why it matters |
|------|----------------|
| Maintenance window | Reboots for kernel |
| Config management | Idempotent desired state |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| After patch broken | journal + status | Roll back package; check changelog |
| Disk full | `df`/`du`/`journal` | Vacuum journals; clear caches |
| High load | top/iostat/psi | Find CPU vs IO vs mem |
| Can’t SSH | console/cloud serial | Fix sshd/firewall via out-of-band |

---

## Gotchas

> [!WARNING]
> **Upgrade without snapshot/backup** on snowflake hosts — have a rollback.

> [!WARNING]
> **Manual `/etc` drift** fights config management — pick a source of truth.

---

## When NOT to use

- **Pets that should be cattle** — rebuild from image instead of endless surgery.
- **App deploys** — separate from OS management pipelines.

---

## Related

[[Package Manager]] [[systemctl]] [[journalctl]] [[Linux management]]
