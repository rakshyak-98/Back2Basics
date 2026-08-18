[[commands]] [[user management]] [[userdel]] [[usermod]] [[passwd]] [[linux groups]]

# useradd

> useradd creates an account record — UID, home, shell, groups — usually lower-level than `adduser` on Debian/Ubuntu.

## Mental model

**Say it in one breath:** writes `/etc/passwd` (+ shadow/group); flags decide home, shell, system versus login user.

```txt
useradd ──► passwd/shadow/group entries
   -m        create home from /etc/skel
   -s        login shell
   -G / -g   supplementary / primary group
   --system  low UID, often nologin
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`useradd -m`** | Create home | “Without `-m` you get an account with no home tree.” |
| --- | --- | --- |
| **`adduser` vs `useradd`** | Friendly vs raw | “Ubuntu: `adduser` wraps policy; `useradd` is the primitive.” |
| **`--system`** | Service account | “No aging, low UID, often `/usr/sbin/nologin`.” |
| **`usermod -s`** | Change shell later | “Flip nologin → bash when a human needs a shell.” |
| **`/etc/skel`** | Home template | “Dotfiles copied into new homes.” |

## Standard config / commands

```bash
# Typical login user
sudo useradd -m -s /bin/bash -c "SDE team" alice
sudo passwd alice
sudo usermod -aG sudo alice          # if admin

# Service account
sudo useradd --system --home /var/lib/myapp --shell /usr/sbin/nologin myapp

# Fix / adjust
sudo usermod -d /home/alice -m alice # set home (careful)
sudo usermod -s /bin/bash alice
sudo cp -a /etc/skel/. /home/alice/
sudo chown -R alice:alice /home/alice

# Debian/Ubuntu comfort wrapper
sudo adduser bob
```

Defaults live in `/etc/default/useradd` and `/etc/login.defs` (UID ranges).

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| User exists, no home | Forgot `-m` | `mkhomedir_helper` / copy skel + `chown` |
| Cannot log in | Shell nologin / locked | `usermod -s`; `passwd -u` |
| UID conflict | Explicit `-u` clash | Pick free UID; check `getent passwd` |
| Groups missing after create | Used `-G` wrong later | `usermod -aG` (append!) |
| `useradd: group exists` | Primary group name taken | `-g` existing GID or different username |

## Gotchas

> [!WARNING]
> **`usermod -G` replaces all supplementary groups** — always `-aG` to append.

> [!WARNING]
> **`useradd` does not set a password** — account may be locked until `passwd`.

> [!WARNING]
> **System users still need a home path** for some daemons — create it even with nologin.

## When NOT to use

- **Directory/IdP users** — SSSD/LDAP; don’t duplicate locally.
- **Kubernetes service identity** — ServiceAccounts, not Linux users on every node.
- **Quick interactive Ubuntu user** — `adduser` is friendlier.

## Related

[[user management]] [[usermod]] [[userdel]] [[passwd]] [[linux groups]] [[visudo]] [[commands]]
