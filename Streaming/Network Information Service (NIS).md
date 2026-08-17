[[Streaming]] [[DNS]] [[Authentication command]]

# Network Information Service (NIS)

> NIS (Network Information Service) is an old shared directory for users, hosts, and maps — central admin for a LAN, not a streaming protocol.

```txt
        Network Informatio ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk Network Information Service end-to-end

## Sources
- [Wikipedia — Network Information Service](https://en.wikipedia.org/wiki/Network_Information_Service) — overview

## Key Concepts
- **NIS / yp:** Yellow Pages-style maps — “NIS centralized passwd and hosts on a LAN.”
- **NIS map:** One keyed table — “`passwd.byname` is a map.”
- **ypbind:** Client binder to NIS domain — “Client must bind to the right domain.”
- **vs DNS:** DNS ≈ names→IP; NIS ≈ broader admin data
- **vs LDAP/AD:** Modern directories — “NIS is legacy; use LDAP/SSSD today.”

- **Note:** Why this note sits under Streaming historically: naming collision / legacy op…

## Technical Details
```bash
# Classic client checks (where NIS still exists)
ypwhich
ypcat passwd
ypmatch "$USER" passwd
domainname
```

- Modern replacement: LDAP / FreeIPA / Active Directory + SSSD

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Login fails on clients | ypbind / domain | Fix domain; ensure server reachable |
| Stale users | Map push | Push maps; check `ypxfr` / make |
| Mixed with DNS confusion | Wrong mental model | Use DNS for names; directory for identities |
| Security audit fail | Cleartext NIS | Migrate off NIS; never expose to internet |

- **Mistake:** **NIS is insecure by modern standards**
- **Mistake:** **Not related to media “streams”**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Any greenfield identity** — LDAP/OIDC/SAML.
- **Con / skip when:** **Internet-facing authentication** — never.

## Real-World Applications
- **Scenario:** Used wherever Network Information Service sits in an ingest → package → CDN →…
