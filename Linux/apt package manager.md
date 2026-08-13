[[Linux]] [[apt configuration]] [[APT policy]] [[gpg]]

# apt package manager

> apt installs and upgrades `.deb` software from repositories — resolve deps, fetch, unpack, configure.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Holds, marks, and logs]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `update` refreshes index metadata; `install`/`upgrade` change packages; `dpkg` is the lower-level unpacker apt drives.

```txt
sources + keyrings ──► apt update ──► lists in /var/lib/apt
                              ↓
                     apt install/upgrade
                              ↓
                          dpkg configure
                              ↓
                     /var/log/dpkg.log
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`apt update`** | Refresh package lists | “Doesn’t upgrade software — only the catalog.” |
| **`apt upgrade` vs `full-upgrade`** | Safe vs allow removals | “full-upgrade may remove packages to satisfy deps.” |
| **Candidate** | Version that would install | “See [[APT policy]].” |
| **Hold** | Block automatic upgrade | “`apt-mark hold` for pinned production packages.” |
| **`apt-get -f install`** | Fix broken deps | “When dpkg is half-configured.” |

---

## Standard config / commands

```bash
sudo apt update
sudo apt install curl jq htop
sudo apt upgrade
sudo apt full-upgrade              # distro upgrades / tough deps

apt show nginx
apt search dnsutils
apt depends nginx
apt list --installed | grep nginx
dpkg -l | grep nginx

# Common tool metapackages
sudo apt install iproute2          # ip, ss
sudo apt install dnsutils          # dig, nslookup
sudo apt install net-tools         # netstat (legacy)
sudo apt install build-essential   # gcc, make
sudo apt install --reinstall pkg   # replace corrupted files
```

Third-party repository sketch (Docker-style):

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `404 Not Found` on update | Wrong codename / stale list | Fix [[apt config]] sources; `apt update` |
| `NO_PUBKEY` / signature | Missing keyring | Dearmor key + `signed-by=` ([[gpg]]) |
| Held back packages | `apt-mark showhold`; phasing | Unhold or wait; check policy |
| Broken half-install | `dpkg -l \| grep ^..r` | `sudo apt -f install`; `dpkg --configure -a` |
| “Package available but not installed” | `apt list` vs `dpkg -l` | `apt list` ≠ installed — use `--installed` |

---

## Holds, marks, and logs

```bash
apt-mark showmanual
apt-mark showauto
apt-mark showhold
sudo apt-mark hold nginx
sudo apt-mark unhold nginx

# Reverse depends
apt-cache rdepends nginx

# What actually happened
less /var/log/dpkg.log
less /var/log/apt/history.log
```

---

## Gotchas

> [!WARNING]
> **`apt list \| grep foo` shows availability, not install state** — use `dpkg -l` or `apt list --installed`.

> [!WARNING]
> **Unattended upgrades + holds** — document why a package is held or the next person will force it.

> [!WARNING]
> **Mixing random PPAs** — dependency hell; prefer official pockets + rare signed vendors.

---

## When NOT to use

- **Language application deps inside a project** — npm/pip/cargo with lockfiles; system packages for *system* tools.
- **Immutable images** — bake packages in the image build; don’t `apt upgrade` live pets without policy.
- **RPM distros** — dnf/yum.

---

## Related

[[apt configuration]] [[APT policy]] [[gpg]] [[Package Manager]] [[Linux]]
