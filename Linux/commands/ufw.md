[[commands]] [[iptables]] [[Linux network commands]] [[SSH]]

# ufw

> Uncomplicated Firewall — thin front-end for iptables/nft to allow/deny ports without hand-writing raw rules.

```txt
        ufw ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Lockout question: always allow SSH before `ufw enable` on a remote box

## Sources
- [Ubuntu UFW documentation](https://documentation.ubuntu.com/server/how-to/security/firewalls/) — deep-dive
- [Wikipedia — Uncomplicated Firewall](https://en.wikipedia.org/wiki/Uncomplicated_Firewall) — overview

## Key Concepts
- **Default incoming deny:** value is sane defaults plus simple syntax.
- **App profiles:** named port sets (`OpenSSH`, `Nginx Full`) under `application.d`.
- **Order / numbered rules:** delete by number when comments collide.
- **Cloud perimeter:** UFW ≠ security group / NSG — open both layers.

## Technical Details
```txt
Packet ──► ufw rules (order matters) ──► ACCEPT / DENY / REJECT
              profiles in application.d map name → ports
```

```bash
sudo ufw status
sudo ufw status verbose
sudo ufw status numbered
sudo ufw allow OpenSSH
sudo ufw allow 80,443/tcp comment 'web'
sudo ufw enable
sudo ufw allow from 192.168.1.0/24 to any port 3000 proto tcp comment 'LAN only'
sudo ufw delete allow 3000/tcp
sudo ufw delete 3
sudo ufw logging on
sudo ufw reset
sudo ufw app list
sudo ufw app info OpenSSH
sudo ufw allow "Nginx Full"
```

- Profiles live in `/etc/ufw/application.d/` and `/usr/share/ufw/application.d/…

| Knob | Why it matters |
|------|----------------|
| Allow SSH first | Prevents lockout on `enable` |
| Comments | Future deletes hit the right rule |
| `from` CIDR | Don’t expose admin ports to the world |

| Symptom | Check | Fix |
|---------|-------|-----|
| Locked out after enable | No SSH allow | Console/IPMI; `ufw allow OpenSSH` |
| Rule present, still blocked | Order / IPv6 | `status verbose`; check defaults and v6 |
| App name not found | Profile missing | `app list`; allow raw ports |
| Cloud unreachable | Security group | Open cloud firewall too |
| `reset` regret | All rules gone | Recreate from runbook |

## Mistakes to Avoid
- **Mistake:** `ufw enable` without SSH allow on a remote VM
- **Mistake:** Assuming Docker published ports honor UFW the way you expect
- **Mistake:** Blind `ufw reset` on production

## Pros/Cons or Trade-offs
- **Pro:** Fast human-readable host firewall for Ubuntu/Debian fleets.
- **Con:** Weak for complex multi-zone/conntrack policy; fights Docker’s iptables habits.

## Comparison
- vs raw nftables/iptables: more power, more footguns — use when UFW is too blunt.
- vs Kubernetes NetworkPolicy / cloud SG: those are the real perimeter for pods/VMs.


### Use cases
- Bootstrap a new VPS: allow OpenSSH + HTTP/HTTPS, enable, then tighten with LA…
