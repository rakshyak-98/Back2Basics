[[commands]] [[iptables]] [[Linux network commands]] [[SSH]]

# ufw

> ufw (Uncomplicated Firewall) is a thin front-end for iptables/nft — allow/deny ports without writing raw rules by hand.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Application profiles]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** default deny incoming, allow outgoing; you add numbered allow/deny rules; enabling without SSH allow can lock you out.

```txt
Packet ──► ufw rules (order matters) ──► ACCEPT / DENY / REJECT
              profiles in application.d map name → ports
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`ufw allow 22/tcp`** | Open a port | “Always allow SSH before `enable` on a remote box.” |
| **`status numbered`** | Rules with indexes | “Delete by number when comments collide.” |
| **App profile** | Named port set | “`OpenSSH` / `Nginx Full` instead of raw ports.” |
| **Default policy** | Incoming deny | “UFW’s value is sane defaults + simple syntax.” |

---

## Standard config / commands

```bash
sudo ufw status
sudo ufw status verbose
sudo ufw status numbered

# Safe bootstrap on a remote host
sudo ufw allow OpenSSH
sudo ufw allow 80,443/tcp comment 'web'
sudo ufw enable

sudo ufw allow 3000/tcp comment 'Node dev'
sudo ufw allow from 192.168.1.0/24 to any port 3000 proto tcp comment 'LAN only'

sudo ufw delete allow 3000/tcp
sudo ufw delete 3                  # by number from status numbered

sudo ufw logging on                # low/medium/high/full
sudo ufw reset                     # nuclear — re-approve SSH first
```

| Knob | Why it matters |
|------|----------------|
| Allow SSH first | Prevents lockout on `enable` |
| Comments | Future you can delete the right rule |
| `from` CIDR | Don’t expose admin ports to the world |

---

## Application profiles

Profiles live in:

- `/etc/ufw/application.d/`
- `/usr/share/ufw/application.d/` (package-shipped)

```bash
sudo ufw app list
sudo ufw app info OpenSSH
sudo ufw allow "Nginx Full"
sudo ufw deny "Apache"
sudo ufw delete allow "Nginx HTTP"
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Locked out after enable | No SSH allow | Console/IPMI; `ufw allow OpenSSH`; `ufw disable` if needed |
| Rule “there” but still blocked | Order / IPv6 | `status verbose`; check `ufw default` and v6 rules |
| App name not found | Profile missing | `app list`; install package or allow raw ports |
| Cloud still unreachable | Security group / NSG | UFW ≠ cloud firewall — open both |
| `reset` regret | All rules gone | Recreate from runbook; never reset blind on prod |

---

## Gotchas

> [!WARNING]
> **Enable without SSH allow = lockout** on remote VMs. Always `allow OpenSSH` first.

> [!WARNING]
> **UFW and Docker** — Docker manipulates iptables; published ports may bypass UFW expectations. Verify with an external probe.

> [!WARNING]
> **`ufw reset` clears everything** — including your only path in.

---

## When NOT to use

- **Complex multi-zone / conntrack policy** — nftables/iptables directly or a host firewall manager.
- **Kubernetes NetworkPolicy / cloud SG** — those are the real perimeter for pods/VMs; UFW is host-local.
- **Already managed by ansible-hardened iptables** — don’t fight two controllers.

---

## Related

[[Linux network commands]] [[SSH]] [[iptables]] [[commands]]
