[[Linux configuration]] [[etc files]] [[apt config]]

# Linux Templates Directory

> Distribution packages ship template files under `/usr/share` and `/etc` — copy or use `debconf`/`systemd` drop-ins instead of editing vendor copies that upgrades overwrite.

Debian-family packages often place **conffiles** in `/etc` and pristine templates in `/usr/share/doc/` or `/usr/share/<package>/`. Red Hat uses `%config` RPM semantics similarly.

## Patterns

| Pattern | Example |
|---------|---------|
| `*.dpkg-dist` / `*.rpmnew` | Left after package manager merge conflict |
| `/etc/skel/` | Template for new user home directories |
| `/usr/lib/tmpfiles.d/` | systemd path creation rules |
| `/usr/share/alsa/` | Default ALSA card profiles — [[alsa]] |

## Safe customization

```bash
# systemd: never edit /usr/lib unit directly
sudo systemctl edit nginx.service

# Apache-style
# /etc/nginx/nginx.conf includes sites-enabled/
```

## After package upgrade

```bash
sudo apt list --upgradable
# Resolve .dpkg-* diffs with vimdiff or dpkg --configure -a
```

## Related

[[etc files]] · [[Linux configuration]] · [[management/Package Manager]]

## Sources

- Debian Policy Manual — conffiles
- `man 5 tmpfiles.d`
