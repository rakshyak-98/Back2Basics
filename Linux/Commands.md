[[commands]] [[common commands]] [[CLI]] [[Find command]]

# Commands

> A compact map of high-leverage Linux commands — inventory, control, and debug without living in man pages.

## Mental model

**Say it in one breath:** classify the question (process, disk, net, logs, packages) then pick one sharp tool — don’t spray flags.

```txt
process → ps/top/pidstat
disk    → df/du/lsblk/iostat
net     → ss/ip/dig/nc
logs    → journalctl/tail
pkgs    → apt/dpkg
files   → find/rg/stat
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **ss** | Socket truth | “Replaces netstat.” |
| --- | --- | --- |
| **journalctl** | systemd logs | “`-u` + `-b` first.” |
| **ip** | Links/addrs/routes | “Replaces ifconfig/route.” |
| **systemctl** | Service control | “status → logs → restart.” |
| **strace/lsof** | Syscalls / open files | “When ‘permission’ lies.” |

## Standard config / commands

```bash
# host pulse
uptime; free -h; df -h; who -b
# process
ps aux --sort=-%mem | head
# network
ss -luntp
ip -br a
# logs
journalctl -p err -b --no-pager | tail -50
# packages
apt-cache policy $pkg
# files
find /var -xdev -type f -size +1G 2>/dev/null | head
```

| Knob | Why it matters |

| `--no-pager` | Scripts/CI |
| --- | --- |
| `-xdev` | Stay on one filesystem |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Slow box | load vs CPU vs IO vs PSI | Match tool to bottleneck |
| Can’t bind port | `ss -lntp` | Kill holder / change port |
| Disk full | `df` + `du -x` | Clear journals/logs |
| DNS weird | `dig` vs `getent` | Fix resolvers / nsswitch |
| Service dead | `systemctl status` + journal | Fix unit/env; restart |

## Gotchas

> [!WARNING]
> **Cheat sheets without mental models** — memorize categories, not 500 flags.

> [!WARNING]
> **Running destructive commands from memory** — dry-run / echo first.

## When NOT to use

- **This note as a deep dive** — jump to [[ss]], [[journalctl]], [[ip]], etc.
- **Windows-only workflows** — different toolchain.

## Related

[[common commands]] [[ss]] [[ip]] [[journalctl]] [[systemctl]] [[Find command]] [[CLI]]
