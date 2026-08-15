[[apt package manager]] [[FileManagement/source list file]] [[etc files]] [[APT policy]]

# apt config

> APT configuration merges defaults from `/etc/apt/apt.conf` and snippets in `/etc/apt/apt.conf.d/` — proxies, pinning, and download behavior live here.

## Interview Relevance
Shows whether you know where Debian/Ubuntu package policy is set (not only `apt install`) — proxies, recommends, and pin priorities show up in air-gapped and enterprise fleets.

## Sources
- `man 5 apt.conf` — deep-dive
- `man 5 sources.list` — deep-dive
- [Debian APT configuration](https://wiki.debian.org/AptConfiguration) — overview

## Core Definition
Effective APT settings are the merge of `/etc/apt/apt.conf`, `/etc/apt/apt.conf.d/*`, preferences under `/etc/apt/preferences.d/`, and repository lists in `sources.list` / `sources.list.d/`.

## Key Concepts
- **apt.conf.d snippets:** Drop-in files (often `99*`) override defaults without editing a single monolith.
- **Acquire / Proxy:** How APT fetches indexes and packages through corporate proxies.
- **Install-Recommends:** Whether “recommended” packages come along with installs.
- **Pinning:** `/etc/apt/preferences.d/` prefers versions — see [[APT policy]].
- **sources.list:** Where packages come from — [[FileManagement/source list file]].

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

## Real-World Applications
A CI image sets `Acquire::http::Proxy` and disables recommends so builds stay small and reach the mirror through a corporate proxy.

## Pros/Cons or Trade-offs
- **Pro:** Drop-ins are upgrade-safe and easy to ship via configuration management.
- **Con:** Mis-set pins or proxies fail obscurely (`404`, hung acquires) unless you dump effective config.

## Comparison
vs [[apt package manager]]: daily install/upgrade commands vs the knobs that change how those commands resolve and fetch. vs `dpkg`: APT is the resolver/fetcher; `dpkg` applies `.deb` files locally.

## Mistakes to Avoid
- Editing `/etc/apt/apt.conf` when a snippet in `apt.conf.d/` already overrides the same key.
- Pinning with priority below 1000 and wondering why a newer repo still wins.
- Changing `sources.list` without `apt update`, then blaming “Unable to locate package.”
