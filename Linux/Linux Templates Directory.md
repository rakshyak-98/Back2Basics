[[Linux configuration]] [[etc files]] [[apt config]] [[alsa]] [[management/Package Manager]]

# Linux Templates Directory

> Distribution packages ship template and default files under `/usr/share` and related paths — copy or use drop-ins instead of editing vendor copies that upgrades overwrite.





## Interview Relevance
Package-hygiene question: explain `.dpkg-dist` / `.rpmnew`, `/etc/skel`, and why `systemctl edit` beats editing units under `/usr/lib`.

## Sources
- Debian Policy Manual — conffiles — deep-dive
- `man 5 tmpfiles.d` — overview

## Core Definition
Debian-family packages place **conffiles** in `/etc` and pristine examples/templates under `/usr/share/doc/` or `/usr/share/<package>/`. Red Hat uses `%config` RPM semantics similarly. Local policy should live in `/etc` overrides, not forked vendor trees.

## Key Concepts
- **Vendor template vs local config:** `/usr` examples vs `/etc` authority.
- **Merge artifacts:** `*.dpkg-dist`, `*.rpmnew`, `*.rpmsave` after upgrades.
- **/etc/skel:** Blueprint for new user home directories.
- **tmpfiles.d:** systemd path creation rules under `/usr/lib/tmpfiles.d/` with `/etc` overrides.
- **Drop-ins:** Preferred customization pattern for systemd and many daemons.

## Technical Details
| Pattern | Example |
|---------|---------|
| `*.dpkg-dist` / `*.rpmnew` | Left after package manager merge conflict |
| `/etc/skel/` | Template for new user home directories |
| `/usr/lib/tmpfiles.d/` | systemd path creation rules |
| `/usr/share/alsa/` | Default ALSA card profiles — [[alsa]] |

```bash
# systemd: never edit /usr/lib unit directly
sudo systemctl edit nginx.service

# Apache-style includes under /etc
# /etc/nginx/nginx.conf includes sites-enabled/
```

```bash
sudo apt list --upgradable
# Resolve .dpkg-* diffs with vimdiff or dpkg --configure -a
```

## Real-World Applications
After `apt upgrade` leaves `/etc/ssh/sshd_config.dpkg-dist`, diff against the live file, merge needed defaults, and keep local hardened settings in place.

## Pros/Cons or Trade-offs
- **Pro:** Upgrades can refresh templates without silently clobbering admin policy when conffile rules are respected.
- **Con:** Ignoring `.dpkg-dist` / `.rpmnew` leaves security defaults unmerged for years.

## Comparison
vs [[etc files]]: `/etc` is what runs; templates are starting points and package examples. vs [[Linux configuration]]: templates are one source layer in the wider config stack. vs editing in `/usr`: forbidden for durable local policy.

## Mistakes to Avoid
- Editing files under `/usr/share` or `/usr/lib` “because that is where the example lived.”
- Deleting `.rpmnew` / `.dpkg-dist` unread after upgrades.
- Copying `/etc/skel` contents into existing homes without understanding it only affects *new* users by default.
