[[Package Manager]] [[systemctl]] [[journalctl]] [[loggging]] [[Linux management]] [[commands/systemctl]]

# Linux system management

> Day-2 host work — patch, observe, control services, and recover with packages, systemd, logs, and backups.

```txt
        Linux system manag ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Runbook discipline: enable vs start, unattended upgrades awareness, journal s…

## Sources
- [Debian Reference — System maintenance](https://www.debian.org/doc/manuals/debian-reference/ch09.en.html) — overview
- [systemd documentation](https://www.freedesktop.org/software/systemd/man/latest/) — deep-dive

## Key Concepts
- **Patch → service → logs:** the daily loop.
- **Backup before risky change:** snapshots/images beat hope.
- **enable vs start:** boot persistence vs now.
- **Canaries:** one host before the fleet.

## Technical Details
```txt
patch (apt) → services (systemctl) → logs (journalctl)
                 │
            backup / snapshots before risky change
```

```bash
sudo apt-get update && sudo apt-get upgrade
systemctl status
journalctl -p err -b
uptime; free -h; df -h
sudo needrestart
```

| Knob | Why it matters |
|------|----------------|
| Maintenance window | Reboots for kernel |
| Config management | Idempotent desired state |

| Symptom | Check | Fix |
|---------|-------|-----|
| After patch broken | journal + status | Roll back package; changelog |
| Disk full | `df`/`du`/`journal` | Vacuum journals; clear caches |
| High load | top/iostat/psi | CPU vs IO vs mem |
| Can’t SSH | console/cloud serial | Fix sshd/firewall out-of-band |

## Mistakes to Avoid
- **Mistake:** Upgrading snowflake hosts without rollback
- **Mistake:** Manual `/etc` drift fighting config management
- **Mistake:** Treating application deploys as OS package upgrades casually

## Pros/Cons or Trade-offs
- **Pro:** Repeatable day-2 operations on classic VMs/bare metal.
- **Con:** Endless surgery on pets that should be cattle — rebuild instead.

## Comparison
- vs [[Linux management]]: broader philosophy; this note is the day-2 checklist.
- vs app deploy pipelines: keep OS management separate from application releases.


### Use cases
- Monthly patch window: snapshot, upgrade, `needrestart`, verify critical units…
