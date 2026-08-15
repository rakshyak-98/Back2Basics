[[commands]] [[user management]] [[userdel]] [[usermod]] [[passwd]] [[linux groups]] [[visudo]]

# useradd

> Creates an account record — UID, home, shell, groups — usually lower-level than `adduser` on Debian/Ubuntu.

## Interview Relevance

Expect `-m` for home, `--system` for service accounts, and `adduser` vs `useradd` on Ubuntu.

## Sources

- [man useradd](https://man7.org/linux/man-pages/man8/useradd.8.html) — deep-dive
- [Wikipedia — useradd](https://en.wikipedia.org/wiki/Useradd) — overview

## Key Concepts

- **`-m` home:** without it you get an account with no home tree from `/etc/skel`.
- **`adduser` vs `useradd`:** Ubuntu’s `adduser` wraps policy; `useradd` is the primitive.
- **`--system`:** low UID, often nologin, no password aging — service accounts.
- **No password by default:** account may stay locked until `passwd`.

## Technical Details

```txt
useradd ──► passwd/shadow/group entries
   -m        create home from /etc/skel
   -s        login shell
   -G / -g   supplementary / primary group
   --system  low UID, often nologin
```

```bash
sudo useradd -m -s /bin/bash -c "SDE team" alice
sudo passwd alice
sudo usermod -aG sudo alice
sudo useradd --system --home /var/lib/myapp --shell /usr/sbin/nologin myapp
sudo usermod -d /home/alice -m alice
sudo cp -a /etc/skel/. /home/alice/
sudo chown -R alice:alice /home/alice
sudo adduser bob
```

Defaults live in `/etc/default/useradd` and `/etc/login.defs` (UID ranges).

| Symptom | Check | Fix |
|---------|-------|-----|
| User exists, no home | Forgot `-m` | Copy skel + `chown` / mkhomedir helper |
| Cannot log in | nologin / locked | `usermod -s`; `passwd -u` |
| UID conflict | Explicit `-u` clash | Free UID; `getent passwd` |
| Groups missing later | Used `-G` wrong | `usermod -aG` (append) |

## Real-World Applications

Provisioning human logins and daemon users on bare metal or classic VMs before configuration management takes over.

## Pros/Cons or Trade-offs

- **Pro:** Precise, scriptable control of UID/home/shell.
- **Con:** Easy to forget `-m`/password; wrong tool for directory/IdP users.

## Comparison

- vs `adduser`: friendlier Debian wrapper for interactive humans.
- vs [[usermod]]: create vs mutate.

## Mistakes to Avoid

- `usermod -G` without `-a` later — wipes supplementary groups.
- Creating system users without a home path some daemons still need.
- Duplicating LDAP/SSSD users locally.
