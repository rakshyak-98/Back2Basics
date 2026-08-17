[[FileManagement]] [[apt package manager]] [[apt config]] [[keyrings]] [[APT policy]]

# source list file

> An APT sources line tells apt where packages come from — URI, suite, components, and which key verifies them.





## Interview Relevance
Debian/Ubuntu ops staple: parse a `deb` line, explain `signed-by`, and debug `apt update` failures (404, NO_PUBKEY) without guessing.

## Sources
- [sources.list(5)](https://manpages.debian.org/sources.list.5) — deep-dive
- [Debian — Setting up apt repositories](https://wiki.debian.org/DebianRepository/UseThirdParty) — overview

## Core Definition
Each `deb`/`deb-src` line names a repository type, optional options (`arch=`, `signed-by=`), a URI, a **suite** (codename or `stable`), and **components** (`main`, `universe`, …). `apt update` fetches `Release`/`Packages` indexes from those lines.

## Key Concepts
- **deb vs deb-src:** Binaries vs source packages — servers rarely need `deb-src`.
- **suite:** Codename (`jammy`, `bookworm`) or suite name; must exist under `/dists/<suite>/`.
- **component:** Selects which package indexes to fetch.
- **signed-by:** Path to keyring; replaces deprecated `apt-key add`.
- **.list vs .sources:** Classic one-line format vs deb822 stanzas (newer style).

## Technical Details
```txt
deb [arch=amd64 signed-by=/usr/share/keyrings/foo.gpg] https://ex/apt jammy main
 │    options                                           suite          component
 type
```

```bash
# /etc/apt/sources.list.d/nginx.list
deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
  http://nginx.org/packages/debian bookworm nginx

sudo apt-get update
apt-cache policy nginx
sudo mv /etc/apt/sources.list.d/bad.list{,.disabled}
```

| Knob | Why it matters |
|------|----------------|
| `signed-by=` | Modern trust pin |
| `arch=` | Avoid foreign-arch noise |
| `trusted=yes` | Disables signature checks — never on production |

| Symptom | Check | Fix |
|---------|-------|-----|
| `NO_PUBKEY` / signed-by errors | Keyring path | Install keyring; fix path |
| 404 on update | Suite/URI | Match codename; check vendor docs |
| Wrong version | Multiple repos | `apt-cache policy`; pin preferences |
| apt-key warnings | Legacy trust | Migrate to keyrings + signed-by |

## Real-World Applications
Adding a vendor Nginx/Docker apt repo with a pinned keyring, and quickly disabling a bad `.list` that blocks all updates.

## Pros/Cons or Trade-offs
- **Pro:** Simple, auditable package provenance.
- **Con:** One bad line can break `apt update` for the whole system.
- **Trade-off:** Third-party repos vs distro packages — freshness vs trust surface.

## Comparison
vs [[APT policy]]: sources define *where*; policy/preferences decide *which version wins*. vs containers: image layers instead of host apt lines. See [[apt package manager]], [[keyrings]].

## Mistakes to Avoid
- Using `trusted=yes` to “make the error go away.”
- Leaving `apt-key add` workflows on modern Debian/Ubuntu.
- Editing suite names after a distro upgrade without updating third-party lists.
