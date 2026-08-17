[[apt config]] [[management/Package Manager]] [[APT policy]] [[FileManagement/source list file]]

# apt package manager

> APT (Advanced Package Tool) is Debian and Ubuntu's high-level package manager — it resolves dependencies from configured repositories and tracks installed `.deb` state.

```txt
        apt package manage ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Core Linux ops signal: can you update indexes, install/hold packages, recover…

## Sources
- [apt(8) man page](https://manpages.debian.org/apt) — deep-dive
- [Debian APT User's Guide](https://www.debian.org/doc/manuals/apt-guide/) — overview

## Key Concepts
- **Index vs package:** Update refreshes metadata; install downloads and configures.
- **Hold / pin:** `apt-mark hold` and preferences stop unwanted upgrades — [[APT policy]].
- **remove vs purge:** Remove drops binaries; purge also drops configuration files.
- **autoremove / clean:** Drop unused deps and cached `.deb` files.
- **Lock files:** Only one APT/dpkg transaction at a time (`/var/lib/dpkg/lock*`).


- **Core:** APT wraps `dpkg`: `apt update` refreshes indexes

## Technical Details
```bash
sudo apt update
sudo apt upgrade
sudo apt install nginx
apt search prometheus
apt show curl
apt list --installed | grep docker

sudo apt-mark hold package-name
apt-cache policy package-name

sudo apt remove nginx
sudo apt purge nginx
sudo apt autoremove
sudo apt clean
```

| Symptom | Fix |
|---------|-------|
| `Unable to locate package` | `apt update`; check [[FileManagement/source list file]] |
| `dpkg was interrupted` | `sudo dpkg --configure -a` |
| Broken dependencies | `sudo apt -f install` |
| Lock held | `sudo lsof /var/lib/dpkg/lock-frontend` |

## Mistakes to Avoid
- **Mistake:** Running `apt upgrade` without `apt update` on stale indexes
- **Mistake:** Using `apt remove` when you needed `purge` to clear broken confi…
- **Mistake:** Force-overwriting locks or killing `dpkg` mid-configure instead …

## Pros/Cons or Trade-offs
- **Pro:** Dependency resolution and repository metadata beat hand-installing `.deb` files.
- **Con:** Distro versions lag upstream; mixing third-party repos without pins causes “dependency hell.”

## Comparison
- vs `dpkg`: APT resolves and fetches; `dpkg -i` installs a local file without …


### Use cases
- Patching a fleet: `apt update && apt upgrade` in maintenance windows, with cr…
