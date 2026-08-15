[[apt config]] [[management/Package Manager]] [[APT policy]] [[FileManagement/source list file]]

# apt package manager

> APT (Advanced Package Tool) is Debian and Ubuntu's high-level package manager — it resolves dependencies from configured repositories and tracks installed `.deb` state.

## Interview Relevance
Core Linux ops signal: can you update indexes, install/hold packages, recover from broken `dpkg`, and explain APT vs `dpkg` without guessing flags.

## Sources
- [apt(8) man page](https://manpages.debian.org/apt) — deep-dive
- [Debian APT User's Guide](https://www.debian.org/doc/manuals/apt-guide/) — overview

## Core Definition
APT wraps `dpkg`: `apt update` refreshes indexes; `apt install` fetches and configures packages; `apt upgrade` / `full-upgrade` apply newer versions while honoring dependencies and holds.

## Key Concepts
- **Index vs package:** Update refreshes metadata; install downloads and configures.
- **Hold / pin:** `apt-mark hold` and preferences stop unwanted upgrades — [[APT policy]].
- **remove vs purge:** Remove drops binaries; purge also drops configuration files.
- **autoremove / clean:** Drop unused deps and cached `.deb` files.
- **Lock files:** Only one APT/dpkg transaction at a time (`/var/lib/dpkg/lock*`).

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

## Real-World Applications
Patching a fleet: `apt update && apt upgrade` in maintenance windows, with critical packages held so an automated upgrade cannot bump a pinned library mid-release.

## Pros/Cons or Trade-offs
- **Pro:** Dependency resolution and repository metadata beat hand-installing `.deb` files.
- **Con:** Distro versions lag upstream; mixing third-party repos without pins causes “dependency hell.”

## Comparison
vs `dpkg`: APT resolves and fetches; `dpkg -i` installs a local file without repo solving. vs yum/dnf/apk: same job on other families — different metadata and command names. See [[management/Package Manager]].

## Mistakes to Avoid
- Running `apt upgrade` without `apt update` on stale indexes.
- Using `apt remove` when you needed `purge` to clear broken config under `/etc`.
- Force-overwriting locks or killing `dpkg` mid-configure instead of `dpkg --configure -a`.
