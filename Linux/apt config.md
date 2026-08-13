[[apt package manager]] [[FileManagement/source list file]] [[etc files]]

# apt config

> APT configuration merges defaults from `/etc/apt/apt.conf` and snippets in `/etc/apt/apt.conf.d/` — proxies, pinning, and acquire behavior live here.

Main repository list: `/etc/apt/sources.list` and `/etc/apt/sources.list.d/*.list` — see [[FileManagement/source list file]].

## Common snippets

```bash
# /etc/apt/apt.conf.d/99custom
APT::Install-Recommends "false";
Acquire::http::Proxy "http://proxy.corp:8080/";
```

## Pinning (version preference)

```
# /etc/apt/preferences.d/nginx
Package: nginx
Pin: version 1.24.*
Pin-Priority: 1001
```

See [[APT policy]] for priority semantics.

## Verify effective config

```bash
apt-config dump | grep -i proxy
apt-cache policy nginx
```

## Related

[[apt package manager]] · [[APT policy]]

## Sources

- `man 5 apt.conf`
- `man 5 sources.list`
