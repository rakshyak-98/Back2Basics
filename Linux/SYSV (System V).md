[[SYSV (System V)]] [[systemd]] [[services/systemd]] [[management/systemctl]]

# SYSV (System V)

> System V init was the classic sequential runlevel boot model — largely replaced by systemd on modern distributions but still referenced in legacy scripts and packaging.

**SysV init** used `/etc/inittab` and numbered scripts in `/etc/init.d/` with `start|stop|status` actions. **Runlevels** 0–6 selected boot mode (single-user, multi-user, reboot, etc.). **LSB headers** in init scripts told the boot system dependencies and ordering.

## Runlevel map (historical)

| Level | Typical meaning |
|-------|-----------------|
| 0 | Halt |
| 1 | Single-user |
| 2–5 | Multi-user (distro-specific; 5 often graphical) |
| 6 | Reboot |

systemd maps these to **targets** (`rescue.target`, `multi-user.target`, `graphical.target`).

## Legacy script pattern

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

## Detect what PID 1 is

```bash
ps -p 1 -o comm=
# systemd vs init
```

On systemd hosts, `/etc/init.d/foo` may still exist via **systemd-sysv-generator** compatibility — prefer native units ([[system service unit files]]).

## Related

[[systemd]] · [[LSB (Linux Standard Base)]] · [[system service unit files]] · [[Services commands]]

## Sources

- [LSB init scripts spec](https://refspecs.linuxfoundation.org/lsb.shtml)
- `man 8 init` (where still shipped)
