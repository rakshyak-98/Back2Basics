[[SYSV (System V)]] [[apt package manager]]

# LSB (Linux Standard Base)

> The Linux Standard Base defined cross-distribution conventions — init script headers, FHS paths, and core library ABIs — so third-party packages could target "Linux" instead of each distro.

**LSB** (Linux Foundation) specified behaviors Debian, RHEL, and others could implement. Init script **LSB headers** (`### BEGIN INIT INFO`) fed dependency ordering on SysV systems. Today systemd units replaced most init integration, but LSB ideas persist in **FHS** layout and packaging metadata.

## LSB init headers (still in old packages)

```bash
### BEGIN INIT INFO
# Provides:          myservice
# Required-Start:    $remote_fs $network
# Required-Stop:     $remote_fs $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Example service
### END INIT INFO
```

## Check LSB compliance (legacy tool)

```bash
lsb_release -a    # distribution ID and version (lsb-release package)
```

## Modern replacement concepts

| LSB era | Today |
|---------|-------|
| Runlevels | systemd **targets** ([[systemd]]) |
| `/etc/init.d` | `.service` units |
| Static library ABI | Container images per distro |

## Related

[[SYSV (System V)]] · [[apt package manager]] · [[management/Package Manager]]

## Sources

- [Linux Foundation LSB](https://refspecs.linuxfoundation.org/lsb.shtml)
- `man 1 lsb_release`
