[[user management]] [[passwd]] [[Authentication command]] [[linux groups]] [[useradd]] [[dig]]

# getent

> getent queries Name Service Switch (NSS) databases — the same path login and libc use — so it sees files, SSSD, LDAP, not just `/etc/passwd`.

```txt
        getent ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Enterprise Linux signal: `getent` vs `grep /etc/passwd`, `getent hosts` vs `d…

## Sources
- [getent(1)](https://man7.org/linux/man-pages/man1/getent.1.html) — deep-dive
- [nsswitch.conf(5)](https://man7.org/linux/man-pages/man5/nsswitch.conf.5.html) — deep-dive

## Key Concepts
- **NSS:** Pluggable lookup order for passwd, group, hosts, services, …
- **passwd / group:** User and group records including directory-backed accounts.
- **hosts:** Name→IP via nsswitch (often files before DNS) — not pure DNS.
- **shadow:** Password aging; usually root-only.
- **Read-only:** getent does not create or edit accounts.


- **Core:** When a program calls `getpwnam("alice")`, glibc walks `/etc/nsswitch.conf` an…

## Technical Details
```txt
app / login ──► libc NSS ──► files │ sss │ ldap │ ...
                           ▲
                      getent (same path)
```

```bash
getent passwd alice
getent passwd 1001
getent group docker
getent group 1005
getent passwd

getent hosts myapp.internal
getent hosts 10.0.1.50
getent services http
sudo getent shadow alice

cat /etc/nsswitch.conf
# passwd: files systemd sss
```

| Symptom | Check | Fix |
|---------|-------|-----|
| User in `/etc/passwd` but can't login | NSS view | `getent passwd user`; fix nsswitch/directory |
| `getent` hangs | Broken DNS/LDAP | Fix resolver; `sssctl` / restart sssd |
| Different than `id` | Cached sssd | `sss_cache -E`; restart `sssd` |
| Host resolves in dig not app | nsswitch order | Compare `getent hosts` vs [[dig]] |

## Mistakes to Avoid
- **Mistake:** Debugging login with file greps on enterprise hosts
- **Mistake:** Treating `getent hosts` as equivalent to `dig`
- **Mistake:** Dumping entire directory passwd databases in scripts

## Pros/Cons or Trade-offs
- **Pro:** Authoritative for “will login see this user?”
- **Con:** Full `getent passwd` on large LDAP can hammer the directory.
- **Trade-off:** Fast local files vs slower networked NSS sources.

## Comparison
- vs `grep /etc/passwd`: files only


### Use cases
- Confirming an LDAP user exists before debugging SSH, verifying `docker` group…
