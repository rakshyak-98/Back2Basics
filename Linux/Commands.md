[[CLI]] [[common commands]] [[Linux network commands]] [[Linux process commands]] [[Services commands]] [[management/Linux management]]

# Commands

> Hub for Linux command notes — route from symptom to the right tool instead of memorizing every flag.

```txt
        Commands ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers care less about memorizing flags and more about choosing the rig…

## Sources
- `man 1 man`, `man 1 apropos` — overview
- Leaf notes under `Linux/commands/` — deep-dive

## Key Concepts
- **Job → tool:** Map the problem (listen ports, CPU, users) before opening `man`.
- **Discovery:** `type`, `command -v`, `dpkg -S`, `apropos` find what provides a name.
- **Pipelines:** Compose small tools instead of one mega-flag binary.
- **Families:** Process, network, service, package, and auth command clusters.


- **Core:** Each leaf under `Linux/commands/` focuses on one binary or small family with …

## Technical Details
| Job | Start here |
|-----|------------|
| Find files | [[Find command]] |
| Search text in files | [[grep]], [[awk]] |
| Processes and CPU | [[ps]], [[top]], [[renice]], [[Linux process commands]] |
| Networking | [[ip]], [[ss]], [[dig]], [[Linux network commands]] |
| Services | [[systemctl]], [[journalctl]], [[Services commands]] |
| Users and groups | [[useradd]], [[usermod]], [[passwd]], [[Authentication command]] |
| Packages (Debian/Ubuntu) | [[APT policy]], [[apt package manager]] |
| Disk sync / backup | [[rsync]], [[diff]] |
| JSON in shell | [[jq]] |
| Interactive pickers | [[fzf]] |

```bash
type -a systemctl
command -v jq
dpkg -S $(which ss)
apropos "socket statistics"

ss -lntp | grep ':443'
ps aux --sort=-%mem | head
journalctl -u nginx -f
grep -rn 'PermitRootLogin' /etc/ssh/
```

## Mistakes to Avoid
- **Mistake:** Memorizing obscure flags before knowing which binary answers the…
- **Mistake:** Using deprecated tools (`ifconfig`, `netstat`) when `ip`/`ss` ar…
- **Mistake:** Ignoring `apropos` / `man -k` when you know the concept but not …

## Pros/Cons or Trade-offs
- **Pro:** A curated map beats scrolling the entire `man` tree during an outage.
- **Con:** Hubs go stale if leaf notes are not linked when new tools become standard (`nft` vs `iptables`).

## Comparison
- vs [[CLI]]: CLI is how you talk to the machine


### Use cases
- During an incident: confirm the listener with `ss`, the process with `ps`, th…
