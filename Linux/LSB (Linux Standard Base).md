[[SYSV (System V)]] [[apt package manager]] [[services/systemd]]

# LSB (Linux Standard Base)

> The Linux Standard Base defined cross-distribution conventions — init script headers, FHS paths, and core library ABIs — so third-party packages could target “Linux” instead of each distro.





## Interview Relevance
Rare as a deep dive, but useful to map legacy `### BEGIN INIT INFO` headers and `lsb_release` to today’s systemd targets and FHS layout.

## Sources
- [Linux Foundation LSB](https://refspecs.linuxfoundation.org/lsb.shtml) — overview
- [lsb_release(1)](https://manpages.debian.org/lsb_release) — overview

## Core Definition
LSB (Linux Foundation) specified behaviors Debian, RHEL, and others could implement. Init script **LSB headers** fed dependency ordering on SysV systems. systemd units replaced most init integration; FHS paths and packaging ideas remain.

## Key Concepts
- **FHS:** Filesystem Hierarchy Standard — `/etc`, `/var`, `/usr` conventions LSB leaned on.
- **LSB init headers:** Metadata block telling Required-Start/Stop and runlevels.
- **ABI / libraries:** Attempted portable binary baseline (largely historical for ISVs).
- **lsb_release:** Reports distributor ID and release for scripts.

## Technical Details
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

```bash
lsb_release -a    # distribution ID and version (lsb-release package)
```

| LSB era | Today |
|---------|-------|
| Runlevels | systemd **targets** ([[services/systemd]]) |
| `/etc/init.d` | `.service` units |
| Static library ABI | Container images per distro |

## Real-World Applications
Reading vendor SysV scripts still shipped for compatibility, and using `lsb_release -si/-sr` in install scripts that branch on Ubuntu vs RHEL.

## Pros/Cons or Trade-offs
- **Pro (historical):** One packaging story for ISVs across distros.
- **Con:** Distros diverged; containers and systemd superseded most of the value.
- **Trade-off:** Keep LSB headers only for SysV compatibility generators — prefer native units.

## Comparison
vs [[SYSV (System V)]]: SysV is the init model; LSB standardized script metadata and broader ABI/FHS. vs systemd: event-driven dependencies replace runlevel scripts.

## Mistakes to Avoid
- Writing new production services as LSB init scripts instead of systemd units.
- Treating `lsb_release` as proof of full LSB certification (it is not).
- Assuming runlevels still control modern boot on systemd hosts.
