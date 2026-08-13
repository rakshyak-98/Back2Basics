<!-- note-strategy: operational -->
[[commands]] [[user management]] [[useradd]] [[groupadd]] [[gpasswd]] [[getent]]

# linux groups

> Groups bundle users for shared file access and sudo — one primary GID plus optional supplementary memberships.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** primary group lives in `/etc/passwd`; supplementary members are listed in `/etc/group` — both phrases “add user to group” / “add group to user” mean the same `usermod -aG`.

```txt
/etc/passwd  → user:…:UID:GID:…     (primary)
/etc/group   → group:…:GID:u1,u2    (supplementary members)

effective access = owner | group | other  (plus ACLs)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Primary GID** | Default group for new files | “New files get this group unless setgid/ACL says else.” |
| **Supplementary** | Extra groups | “docker, sudo, adm — privileges without changing primary.” |
| **`usermod -aG`** | Append groups | “`-a` is mandatory or you wipe existing groups.” |
| **`getent group`** | NSS view of members | “Shows supplementary list — not who has it as primary.” |
| **`newgrp` / re-login** | Refresh creds | “Group changes apply on next session.” |

---

## Standard config / commands

```bash
# Inspect
id
id alice
groups
groups alice
getent group docker
getent group | head

# Create / membership
sudo groupadd developers
sudo usermod -aG developers alice
sudo gpasswd -a alice developers
sudo gpasswd -d alice developers

# Activate in current shell (or logout/login)
newgrp developers
```

| Phrase people say | Same action |
|-------------------|-------------|
| “Add group to user” | `usermod -aG group user` |
| “Add user to group” | `usermod -aG group user` / `gpasswd -a user group` |

Common groups: `sudo`/`wheel` (administrator), `docker`, `adm` (logs), `users`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| In group but access denied | `id` in *this* session | Re-login or `newgrp`; services need restart |
| Lost other groups | Used `-G` without `-a` | Restore with `-aG` list |
| `getent group X` empty of user | User has X as *primary* only | Check `id -gn`; primary isn’t always listed as member |
| Nested “group of groups” | Linux doesn’t nest | Use ACLs or roles elsewhere |
| File group wrong | Primary vs setgid dir | `chgrp`; `chmod g+s` on shared dirs |

---

## Gotchas

> [!WARNING]
> **`usermod -G a,b` replaces the whole supplementary set** — always `-aG` to append.

> [!WARNING]
> **`getent group` omits users who only have that GID as primary** — use `getent passwd` / `id` to see the full picture.

> [!WARNING]
> **Daemons don’t pick up new groups until restart** — docker socket access is a classic.

---

## When NOT to use

- **Fine-grained per-file exceptions** — ACLs (`setfacl`) or shared service users.
- **Cross-host identity** — LDAP/IdP groups via SSSD.
- **Kubernetes RBAC** — not Linux `/etc/group`.

---

## Related

[[user management]] [[useradd]] [[groupadd]] [[gpasswd]] [[getent]] [[visudo]] [[commands]]
