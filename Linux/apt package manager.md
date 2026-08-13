[[apt config]] [[management/Package Manager]] [[APT policy]] [[FileManagement/source list file]]

# apt package manager

> APT is Debian and Ubuntu's high-level package manager — it resolves dependencies from configured repositories and tracks installed `.deb` state.

**APT** (Advanced Package Tool) wraps `dpkg`. Commands: `apt update` refreshes index; `apt install` fetches and configures packages; `apt upgrade` applies newer versions.

## Daily commands

```bash
sudo apt update
sudo apt upgrade
sudo apt install nginx
apt search prometheus
apt show curl
apt list --installed | grep docker
```

## Hold / pin versions

```bash
sudo apt-mark hold package-name
apt-cache policy package-name   # see [[APT policy]]
```

## Remove and clean

```bash
sudo apt remove nginx
sudo apt purge nginx          # plus config files
sudo apt autoremove
sudo apt clean
```

## Debugging

| Symptom | Fix |
|---------|-------|
| `Unable to locate package` | `apt update`; check [[FileManagement/source list file]] |
| `dpkg was interrupted` | `sudo dpkg --configure -a` |
| Broken dependencies | `sudo apt -f install` |
| Lock held | `sudo lsof /var/lib/dpkg/lock-frontend` |

## Related

[[apt config]] · [[management/Package deferred]] · [[management/Package Manager]]

## Sources

- [apt(8) man page](https://manpages.debian.org/apt)
- [Debian APT User's Guide](https://www.debian.org/doc/manuals/apt-guide/)
