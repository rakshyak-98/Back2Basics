[[management]] [[apt package manager]] [[source list file]] [[keyrings]]

# Package Manager

> A package manager installs/upgrades/removes software with dependency solving — on Debian/Ubuntu that’s APT/dpkg; elsewhere dnf/zypper/pacman.

## Mental model

**Say it in one breath:** indexes declare versions; solver picks a set; unpacker puts files on disk; configuration under `/etc`.

```txt
apt update → indexes
apt install → resolve → dpkg -i unpack
                 │
            /var/lib/dpkg  /var/cache/apt
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **APT vs dpkg** | Solver vs unpacker | “apt calls dpkg.” |
| --- | --- | --- |
| **pin / policy** | Version preference | “`apt-cache policy` shows why.” |
| **held packages** | Block upgrades | “`apt-mark hold`.” |
| **transaction** | Atomic-ish change set | “Avoid killing mid-dpkg.” |
| **third-party repo** | Extra sources | “Trust + pin carefully.” |

## Standard config / commands

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends pkg
apt-cache policy pkg
dpkg -l 'pkg*'
sudo apt-get remove pkg
sudo apt-get purge pkg
sudo apt-get autoremove
```

| Knob | Why it matters |

| `--no-install-recommends` | Leaner servers |
| --- | --- |
| `DEBIAN_FRONTEND=noninteractive` | CI/automation |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Held broken packages | `dpkg --audit` | `apt -f install`; fix deps |
| Hash sum mismatch | Mirror/cache | `apt clean`; retry mirror |
| Wrong version | Policy | Pin; disable bad repo |
| dpkg lock | Parallel apt | Wait or clear stale lock carefully |

## Gotchas

> [!WARNING]
> **Killing dpkg mid-unpack** leaves the system half-configured — repair with `dpkg --configure -a`.

> [!WARNING]
> **Mixing distro releases** in sources = dependency hell.

## When NOT to use

- **Language application deps** — prefer language lockfiles in the application image.
- **Kernel live patches** — use vendor livepatch tooling, not random .debs.

## Related

[[apt package manager]] [[apt configuration]] [[Package deferred]] [[source list file]]
