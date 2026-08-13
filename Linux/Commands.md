[[CLI]] [[common commands]] [[Linux network commands]] [[Linux process commands]] [[Services commands]]

# Commands

> Hub for Linux command notes — route from symptom to the right tool instead of memorizing every flag.

This note routes to leaf command pages under `Linux/commands/`. Each leaf focuses on one binary or small family with runnable examples and failure signals.

## By job

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

## Command discovery

```bash
# What provides this name?
type -a systemctl
command -v jq

# Search installed packages for a binary (Debian family)
dpkg -S $(which ss)

# Brief description from man database
apropos "socket statistics"
```

## Pipelines worth remembering

```bash
# Who listens on 443?
ss -lntp | grep ':443'

# Top memory consumers
ps aux --sort=-%mem | head

# Follow service logs
journalctl -u nginx -f

# Config audit
grep -rn 'PermitRootLogin' /etc/ssh/
```

## Related

[[CLI]] · [[common commands]] · [[management/Linux management]]

## Sources

- `man 1 man`, `man 1 apropos`
