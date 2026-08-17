[[useradd]] [[userdel]] [[passwd]] [[getent]] [[user management]] [[etc files]] [[linux groups]]

# usermod

> Mutates an existing local account — shell, home, groups, lock — in passwd/shadow/group.

```txt
        usermod ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** The classic trap: `usermod -G` **replaces** supplementary groups

## Sources
- [man usermod](https://man7.org/linux/man-pages/man8/usermod.8.html) — deep-dive
- [Wikipedia — usermod](https://en.wikipedia.org/wiki/Usermod) — overview

## Key Concepts
- **`-aG` append vs `-G` replace:** forgetting `-a` drops sudo/docker membership.
- **`-L` / `-U`:** lock/unlock password — keys may still work.
- **`-d DIR -m`:** set home and move files; `-m` required to relocate contents.
- **`-s` shell:** nologin to disable interactive login.


- **Core:** `usermod` edits `/etc/passwd`, `/etc/shadow`, `/etc/group` (and gshadow) for …

## Technical Details
```
usermod → /etc/passwd + shadow + group
Running process → still old UID until restart
NSS (sssd/LDAP) → usermod may not apply
```

| Flag | Effect | Risk |
|------|--------|------|
| `-s SHELL` | Login shell | Lock user if shell invalid |
| `-l NEW` | Rename login | Update home, cron, mail refs |
| `-d DIR -m` | Home + move | Need `-m` to move existing home |
| `-g GROUP` | Primary group | Must exist |
| `-aG GROUP` | Append supplementary | Safe add |
| `-G g1,g2` | Replace all supp groups | Drops sudo if forgotten |
| `-L` / `-U` | Lock/unlock password | PAM still applies |

```bash
sudo usermod -s /bin/bash deploy
sudo usermod -aG docker,sudo alice
id alice
sudo usermod -g developers alice
sudo usermod -d /home/alice-new -m alice
sudo usermod -l alice_new alice_old
sudo usermod -L compromised
getent passwd alice
```

- After group change: full logout (or `newgrp`) for supplementary groups to app…

| Symptom | Check | Fix |
|---------|-------|-----|
| Not in docker group | `id` after change | Re-login; use `-aG` |
| Lost sudo | `groups user` | Was wiped by `-G`; restore `-aG sudo` |
| Can’t login | Shell path | `usermod -s /bin/bash` |
| Change ignored | sssd/LDAP | Directory tools |

## Mistakes to Avoid
- **Mistake:** `usermod -G docker` without `-a`
- **Mistake:** Rename without `-m` leaving a mismatched home path
- **Mistake:** Expecting running daemons to pick up new groups without restart/…

## Pros/Cons or Trade-offs
- **Pro:** Precise local account surgery without recreate.
- **Con:** Easy group wipe; useless for directory-backed identities.

## Comparison
- vs [[useradd]]: create vs mutate.
- vs [[passwd]] `-l`: similar password lock path; usermod also covers shell/home/groups.


### Use cases
- Adding engineers to `docker`/`sudo`, locking compromised accounts, and reloca…
