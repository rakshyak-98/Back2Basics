[[apt package manager]] [[FileManagement/source list file]] [[keyrings]] [[Package deferred]] [[commands/APT policy]]

# Package Manager

> Installs, upgrades, and removes software with dependency solving — APT/dpkg on Debian/Ubuntu; dnf/zypper/pacman elsewhere.

```txt
        Package Manager ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** APT vs dpkg, policy/pins, holds, and never killing mid-dpkg unpack.

## Sources
- [Debian APT guide](https://www.debian.org/doc/manuals/apt-guide/) — deep-dive
- [Wikipedia — Package manager](https://en.wikipedia.org/wiki/Package_manager) — overview

## Key Concepts
- **APT vs dpkg:** solver/front-end vs unpacker.
- **Policy / pin:** why a candidate version wins (`apt-cache policy`).
- **Hold:** block upgrades for a package.
- **Transaction safety:** don’t interrupt unpack/configure.

## Technical Details
```txt
apt update → indexes
apt install → resolve → dpkg -i unpack
                 │
            /var/lib/dpkg  /var/cache/apt
```

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
|------|----------------|
| `--no-install-recommends` | Leaner servers |
| `DEBIAN_FRONTEND=noninteractive` | CI/automation |

| Symptom | Check | Fix |
|---------|-------|-----|
| Held broken packages | `dpkg --audit` | `apt -f install`; fix deps |
| Hash sum mismatch | Mirror/cache | `apt clean`; retry mirror |
| Wrong version | Policy | Pin; disable bad repo |
| dpkg lock | Parallel apt | Wait; clear stale lock carefully |

## Mistakes to Avoid
- **Mistake:** Killing dpkg mid-unpack — repair with `dpkg --configure -a`
- **Mistake:** Mixing distro releases in sources.list
- **Mistake:** Trusting third-party repos without pins/keyrings

## Pros/Cons or Trade-offs
- **Pro:** Dependency solving and rollback-friendly package state.
- **Con:** Mixing releases/third-party repos creates dependency hell.

## Comparison
- vs language lockfiles (npm/pip): app deps belong in the image; OS packages for the platform.
- vs [[Package deferred]]: holds/pins are the deferral mechanism.


### Use cases
- Lean server bootstrap with `--no-install-recommends`, verify candidates with …
