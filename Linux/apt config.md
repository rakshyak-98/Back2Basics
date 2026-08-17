[[apt package manager]] [[FileManagement/source list file]] [[etc files]] [[APT policy]]

# apt config

> APT configuration merges defaults from `/etc/apt/apt.conf` and snippets in `/etc/apt/apt.conf.d/` — proxies, pinning, and download behavior live here.

```txt
        apt config ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows whether you know where Debian/Ubuntu package policy is set (not only `a…

## Sources
- `man 5 apt.conf` — deep-dive
- `man 5 sources.list` — deep-dive
- [Debian APT configuration](https://wiki.debian.org/AptConfiguration) — overview

## Key Concepts
- **apt.conf.d snippets:** Drop-in files (often `99*`) override defaults without editing a single monoli…
- **Acquire / Proxy:** How APT fetches indexes and packages through corporate proxies.
- **Install-Recommends:** Whether “recommended” packages come along with installs.
- **Pinning:** `/etc/apt/preferences.d/` prefers versions — see [[APT policy]].
- **sources.list:** Where packages come from — [[FileManagement/source list file]].


- **Core:** Effective APT settings are the merge of `/etc/apt/apt.conf`, `/etc/apt/apt.co…

## Technical Details
```bash
# /etc/apt/apt.conf.d/99custom
APT::Install-Recommends "false";
Acquire::http::Proxy "http://proxy.corp:8080/";
```

```
# /etc/apt/preferences.d/nginx
Package: nginx
Pin: version 1.24.*
Pin-Priority: 1001
```

```bash
apt-config dump | grep -i proxy
apt-cache policy nginx
```

## Mistakes to Avoid
- **Mistake:** Editing `/etc/apt/apt.conf` when a snippet in `apt.conf.d/` alre…
- **Mistake:** Pinning with priority below 1000 and wondering why a newer repo …
- **Mistake:** Changing `sources.list` without `apt update`, then blaming “Unab…

## Pros/Cons or Trade-offs
- **Pro:** Drop-ins are upgrade-safe and easy to ship via configuration management.
- **Con:** Mis-set pins or proxies fail obscurely (`404`, hung acquires) unless you dump effective config.

## Comparison
- vs [[apt package manager]]: daily install/upgrade commands vs the knobs that …


### Use cases
- A CI image sets `Acquire::http::Proxy` and disables recommends so builds stay…
