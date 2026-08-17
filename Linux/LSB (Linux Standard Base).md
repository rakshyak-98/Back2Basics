[[SYSV (System V)]] [[apt package manager]] [[services/systemd]]

# LSB (Linux Standard Base)

> The Linux Standard Base defined cross-distribution conventions — init script headers, FHS paths, and core library ABIs — so third-party packages could target “Linux” instead of each distro.

```txt
        LSB (Linux Standar ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Rare as a deep dive, but useful to map legacy `### BEGIN INIT INFO` headers a…

## Sources
- [Linux Foundation LSB](https://refspecs.linuxfoundation.org/lsb.shtml) — overview
- [lsb_release(1)](https://manpages.debian.org/lsb_release) — overview

## Key Concepts
- **FHS:** Filesystem Hierarchy Standard
- **LSB init headers:** Metadata block telling Required-Start/Stop and runlevels.
- **ABI / libraries:** Attempted portable binary baseline (largely historical for ISVs).
- **lsb_release:** Reports distributor ID and release for scripts.


- **Core:** LSB (Linux Foundation) specified behaviors Debian, RHEL, and others could imp…

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

## Mistakes to Avoid
- **Mistake:** Writing new production services as LSB init scripts instead of s…
- **Mistake:** Treating `lsb_release` as proof of full LSB certification (it is…
- **Mistake:** Assuming runlevels still control modern boot on systemd hosts

## Pros/Cons or Trade-offs
- **Pro (historical):** One packaging story for ISVs across distros.
- **Con:** Distros diverged; containers and systemd superseded most of the value.
- **Trade-off:** Keep LSB headers only for SysV compatibility generators — prefer native units.

## Comparison
- vs [[SYSV (System V)]]: SysV is the init model


### Use cases
- Reading vendor SysV scripts still shipped for compatibility, and using `lsb_r…
