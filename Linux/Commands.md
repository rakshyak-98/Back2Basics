[[CLI]] [[common commands]] [[Linux network commands]] [[Linux process commands]] [[Services commands]] [[management/Linux management]]

# Commands

> Hub for Linux command notes — route from symptom to the right tool instead of memorizing every flag.

## Interview Relevance
Interviewers care less about memorizing flags and more about choosing the right tool (`ss` vs `netstat`, `systemctl` vs init scripts). This map is how you show structured recall under pressure.

## Sources
- `man 1 man`, `man 1 apropos` — overview
- Leaf notes under `Linux/commands/` — deep-dive

## Core Definition
Each leaf under `Linux/commands/` focuses on one binary or small family with runnable examples and failure signals. Start here by job, then drill into the leaf.

## Key Concepts
- **Job → tool:** Map the problem (listen ports, CPU, users) before opening `man`.
- **Discovery:** `type`, `command -v`, `dpkg -S`, `apropos` find what provides a name.
- **Pipelines:** Compose small tools instead of one mega-flag binary.
- **Families:** Process, network, service, package, and auth command clusters.

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

## Real-World Applications
During an incident: confirm the listener with `ss`, the process with `ps`, the service with `systemctl`/`journalctl`, then the package that owns the binary with `dpkg -S`.

## Pros/Cons or Trade-offs
- **Pro:** A curated map beats scrolling the entire `man` tree during an outage.
- **Con:** Hubs go stale if leaf notes are not linked when new tools become standard (`nft` vs `iptables`).

## Comparison
vs [[CLI]]: CLI is how you talk to the machine; this note is a directory of which programs to run. vs distro “cheat sheets”: here each command has a vault leaf with failure modes.

## Mistakes to Avoid
- Memorizing obscure flags before knowing which binary answers the question.
- Using deprecated tools (`ifconfig`, `netstat`) when `ip`/`ss` are available — unless the environment is ancient.
- Ignoring `apropos` / `man -k` when you know the concept but not the name.
