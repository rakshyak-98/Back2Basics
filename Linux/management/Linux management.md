[[Linux system management]] [[Package Manager]] [[systemctl]] [[journalctl]] [[user management]] [[file mount]]

# Linux management

> Ops umbrella for a host — packages, services, users, storage, network, and observability.

```txt
        Linux management ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Staff/ops framing: cattle vs pets, break-glass vs config management, blast ra…

## Sources
- [Google SRE book — Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) — overview
- [systemd documentation](https://www.freedesktop.org/software/systemd/man/latest/) — deep-dive

## Key Concepts
- **Desired state:** CM/image is source of truth; SSH is break-glass.
- **Blast radius:** canary one host before the fleet.
- **Break-glass kit:** apt, systemctl, journalctl, ip/ss, df/free.
- **Drift:** undocumented manual fixes become the next unknown.

## Technical Details
```txt
desired state (CM/image)
        │
        ├─ packages / units / sysctl / users
        └─ break-glass: apt, systemctl, journalctl, ip/ss
```

```bash
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

| Symptom | Check | Fix |
|---------|-------|-----|
| Drift from CM | Diff reality vs repo | Re-apply; freeze manual edits |
| Mystery reboot | journal `-b -1` | Kernel panic/OOM/watchdog |
| Network partition | `ip`/`ss`/ping | Routes/firewall/DNS |
| Auth failures | time + PAM + LDAP | NTP; getent; tickets |

## Mistakes to Avoid
- **Mistake:** Leaving undocumented manual fixes
- **Mistake:** Endless surgery on hosts that should be rebuilt from image
- **Mistake:** Managing containers by babysitting their guest OS

## Pros/Cons or Trade-offs
- **Pro:** One mental model for host health across layers.
- **Con:** Mixing app deploy and OS change in one SSH session couples blast radii.

## Comparison
- vs [[Linux system management]]: day-2 patch/observe focus under this umbrella.
- vs cloud control plane: use provider APIs for platforms you don’t own as pets.


### Use cases
- SEV response: confirm blast radius, use the break-glass kit, fix with a track…
