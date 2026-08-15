[[services/systemd]] [[LSB (Linux Standard Base)]] [[system service unit files]] [[Services commands]]

# SYSV (System V)

> System V init was the classic sequential runlevel boot model — largely replaced by systemd on modern distributions but still referenced in legacy scripts and packaging.

## Interview Relevance
Expect a short map: runlevels → systemd targets, `/etc/init.d` → units, and how to detect PID 1. Deep SysV trivia is less valuable than migration awareness.

## Sources
- [LSB init scripts](https://refspecs.linuxfoundation.org/lsb.shtml) — overview
- [systemd-sysv-generator](https://www.freedesktop.org/software/systemd/man/latest/systemd-sysv-generator.html) — deep-dive

## Core Definition
**SysV init** used `/etc/inittab` and numbered scripts in `/etc/init.d/` with `start|stop|status` actions. **Runlevels** 0–6 selected boot mode. **LSB headers** in init scripts declared dependencies. systemd maps runlevels to **targets**.

## Key Concepts
- **Runlevels:** Halt (0), single-user (1), multi-user (2–5), reboot (6).
- **init.d scripts:** Shell wrappers with LSB headers.
- **systemd-sysv-generator:** Compatibility shim that turns old scripts into units.
- **PID 1:** Today almost always `systemd` on server distros.

## Technical Details

| Level | Typical meaning |
|-------|-----------------|
| 0 | Halt |
| 1 | Single-user |
| 2–5 | Multi-user (distro-specific; 5 often graphical) |
| 6 | Reboot |

```bash
#!/bin/sh
# /etc/init.d/example
### BEGIN INIT INFO
# Provides:          example
# Required-Start:    $network
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

case "$1" in
  start)  /usr/sbin/example --daemon ;;
  stop)   killall example ;;
  status) pgrep example ;;
  *)      echo "Usage: $0 {start|stop|status}"; exit 1 ;;
esac
```

```bash
ps -p 1 -o comm=
# systemd vs init
```

## Real-World Applications
Supporting vendor appliances that still ship `/etc/init.d` scripts, and translating “start in runlevel 3” docs into `multi-user.target` on systemd hosts.

## Pros/Cons or Trade-offs
- **Pro (historical):** Simple mental model; easy to read shell scripts.
- **Con:** Slow sequential boot; poor dependency/parallelism; fragile PID files.
- **Trade-off:** Compatibility generators vs rewriting as native [[system service unit files]].

## Comparison
vs [[services/systemd]]: systemd is socket/target-based and parallel. vs [[LSB (Linux Standard Base)]]: LSB standardized SysV script metadata. Prefer native units on modern hosts.

## Mistakes to Avoid
- Writing new services as SysV scripts on systemd fleets.
- Using `killall` in stop actions without verifying the process name.
- Assuming runlevel commands still control boot the same way under systemd.
