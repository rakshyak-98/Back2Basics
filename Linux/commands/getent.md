[[user management]] [[passwd]] [[Authentication command]] [[linux groups]]

# getent

> One-line: query **NSS** (Name Service Switch) databases the same way libc does — one command for local files, LDAP, SSSS, DNS, and hosts. **The truth for "does this account exist?"**

## Mental model

When a program calls `getpwnam("alice")`, glibc walks `/etc/nsswitch.conf` and asks each configured source (files, systemd, sss, ldap, …). `getent` exposes that same resolution path — so it beats `grep /etc/passwd alice` when accounts live in LDAP/SSSD.

```
app / login ──► libc NSS ──► files │ sss │ ldap │ ...
                                ▲
                           getent (same path)
```

| Database | Typical use |
|----------|-------------|
| `passwd` | Users (UID, home, shell) |
| `group` | Groups (GID, members) |
| `shadow` | Password aging (root only) |
| `hosts` | Hostname ↔ IP (`/etc/hosts` + DNS per nsswitch) |
| `services` | Port ↔ service name |
| `ethers`, `protocols`, `rpc` | Network tables |

## Standard config / commands

```bash
# Does user exist? Full record
getent passwd alice
# alice:x:1001:1001:Alice:/home/alice:/bin/bash

# UID lookup
getent passwd 1001

# Group + members
getent group docker
getent group 1005

# All local+remote users (can be long)
getent passwd

# Host resolution (respects nsswitch — files before dns)
getent hosts myapp.internal
getent hosts 10.0.1.50

# Service name → port
getent services http
getent services 443

# Shadow (root)
sudo getent shadow alice

# Which databases exist
getent --help
```

**vs raw file grep:**

```bash
grep alice /etc/passwd          # files only — misses SSSD/LDAP
getent passwd alice             # authoritative for login path

# Debug NSS order
cat /etc/nsswitch.conf
# passwd: files systemd sss
# group:  files systemd sss
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| User in `/etc/passwd` but can't login | Not in SSSD/LDAP view | `getent passwd user`; fix nsswitch or sync directory |
| `getent` hangs | Broken DNS/LDAP | `getent hosts badname`; `sssctl user-checks`; fix resolver |
| Empty `getent passwd` | nsswitch misconfigured | Restore `/etc/nsswitch.conf`; `authselect` / `pam-auth-update` |
| Different result than `id` | Cached sssd | `sss_cache -E`; restart `sssd` |
| Host resolves in dig but not app | nsswitch order | `getent hosts` vs `dig`; put files/dns order right |
| Shadow empty for local user | Expected on sss-only | Password in directory; use ldap/sss tools |

## Gotchas

> [!WARNING]
> **`grep /etc/passwd` lies on enterprise hosts** — always `getent` when debugging login, permissions, or automation that mirrors system users.

> [!WARNING]
> **`getent hosts` is not `dig`** — follows nsswitch (often `/etc/hosts` first). DNS-only debugging → [[dig]].

> [!WARNING]
> **Large `getent passwd` on LDAP** — can hammer directory; filter with `getent passwd username`.

> [!WARNING]
> **Shadow via getent still needs root** — same as reading `/etc/shadow`.

## When NOT to use

- **DNS-only troubleshooting** → `dig`, `resolvectl query`.
- **Active Directory admin** → `ldapsearch`, `adcli`, `realm`.
- **Edit accounts** → [[useradd]], [[usermod]], [[passwd]] — getent is read-only.

## Related

[[user management]] [[passwd]] [[useradd]] [[Authentication command]] [[linux groups]] [[dig]]
