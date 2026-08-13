[[management]] [[Linux system management]] [[Package Manager]] [[systemctl]]

# Linux management

> Linux management is the ops umbrella — packages, services, users, storage, network, and observability on a host.

---

## How it works

```txt
desired state (CM/image)
        │
        ├─ packages / units / sysctl / users
        └─ break-glass: apt, systemctl, journalctl, ip/ss
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **cattle vs pets** | Rebuild vs nurse | “Prefer immutable images.” |
| **break-glass** | Emergency manual | “Document and revert to CM.” |
| **blast radius** | Change scope | “Canary one host first.” |
| **SSO/source of truth** | Where config lives | “Git > SSH snowflakes.” |
| **SLOs** | What “healthy” means | “Manage to signals, not vibes.” |

---


## Configuration and commands

```bash
# break-glass kit
sudo apt-get update
systemctl status
journalctl -p err -b --no-pager | tail
ip -br a; ss -luntp | head
df -h; free -h
```

| Knob | Why it matters |
|------|----------------|
| CM tool (Ansible/Puppet/…) | Drift control |
| Golden image pipeline | Faster recovery |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Drift from CM | Diff reality vs repo | Re-apply; freeze manual edits |
| Mystery reboot | journal `-b -1` | Kernel panic/OOM/watchdog |
| Network partition | `ip`/`ss`/ping | Routes/firewall/DNS |
| Auth failures | time + PAM + LDAP | NTP; getent; tickets |

---


## Gotchas

> [!WARNING]
> **Undocumented manual fixes** become the next outage’s unknown.

> [!WARNING]
> **Managing apps and OS in one SSH session** mixes blast radii — split pipelines.

---


## When not to use

- **Platforms you don’t own** — use the cloud control plane.
- **Per-container OS babysitting** — rebuild images.

---


## Related

[[Linux system management]] [[Package Manager]] [[systemctl]] [[user management]] [[Linux resource management]]

## Sources

- [Wikipedia — Linux management](https://en.wikipedia.org/wiki/Linux_management)
