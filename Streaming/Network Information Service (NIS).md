[[Streaming]] [[DNS]] [[Authentication command]]

# Network Information Service (NIS)

> NIS (Network Information Service) is an old shared directory for users, hosts, and maps — central admin for a LAN, not a streaming protocol.





## Interview Relevance
Interviewers probe whether you can walk Network Information Service end-to-end — not just name it. Signal fluency with **NIS / yp**, **NIS map**, **ypbind**, **vs DNS** and when you would pick a different path.

## Sources
- [Wikipedia — Network Information Service](https://en.wikipedia.org/wiki/Network_Information_Service) — overview

## Key Concepts
- **NIS / yp:** Yellow Pages-style maps — “NIS centralized passwd and hosts on a LAN.”
- **NIS map:** One keyed table — “`passwd.byname` is a map.”
- **ypbind:** Client binder to NIS domain — “Client must bind to the right domain.”
- **vs DNS:** DNS ≈ names→IP; NIS ≈ broader admin data — “DNS doesn’t replace NIS user maps.”
- **vs LDAP/AD:** Modern directories — “NIS is legacy; use LDAP/SSSD today.”

Why this note sits under Streaming historically: naming collision / legacy operations next to media stacks — it is **not** part of HLS/WebRTC.

## Technical Details
```bash
# Classic client checks (where NIS still exists)
ypwhich
ypcat passwd
ypmatch "$USER" passwd
domainname
```

Modern replacement: LDAP / FreeIPA / Active Directory + SSSD — not new NIS domains.

## Real-World Applications
Used wherever Network Information Service sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Any greenfield identity** — LDAP/OIDC/SAML.
- **Con / skip when:** **Internet-facing authentication** — never.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Login fails on clients | ypbind / domain | Fix domain; ensure server reachable |
| Stale users | Map push | Push maps; check `ypxfr` / make |
| Mixed with DNS confusion | Wrong mental model | Use DNS for names; directory for identities |
| Security audit fail | Cleartext NIS | Migrate off NIS; never expose to internet |

- **NIS is insecure by modern standards** — no crypto; treat as legacy LAN-only debt.
- **Not related to media “streams”** — do not confuse with MPEG-TS or WebRTC.
