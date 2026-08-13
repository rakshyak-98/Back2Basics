[[Streaming]] [[DNS]]

# Network Information Service (NIS)

> NIS (Network Information Service) is an old shared directory for users, hosts, and maps — central admin for a LAN, not a streaming protocol.

---

## How it works

Why this note sits under Streaming historically: naming collision / legacy operations next to media stacks — it is **not** part of HLS/WebRTC.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **NIS / yp** | Yellow Pages-style maps | “NIS centralized passwd and hosts on a LAN.” |
| **NIS map** | One keyed table | “`passwd.byname` is a map.” |
| **ypbind** | Client binder to NIS domain | “Client must bind to the right domain.” |
| **vs DNS** | DNS ≈ names→IP; NIS ≈ broader admin data | “DNS doesn’t replace NIS user maps.” |
| **vs LDAP/AD** | Modern directories | “NIS is legacy; use LDAP/SSSD today.” |

---


## Configuration and commands

```bash
# Classic client checks (where NIS still exists)
ypwhich
ypcat passwd
ypmatch "$USER" passwd
domainname
```

Modern replacement: LDAP / FreeIPA / Active Directory + SSSD — not new NIS domains.

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Login fails on clients | ypbind / domain | Fix domain; ensure server reachable |
| Stale users | Map push | Push maps; check `ypxfr` / make |
| Mixed with DNS confusion | Wrong mental model | Use DNS for names; directory for identities |
| Security audit fail | Cleartext NIS | Migrate off NIS; never expose to internet |

---


## Gotchas

> [!WARNING]
> **NIS is insecure by modern standards** — no crypto; treat as legacy LAN-only debt.

> [!WARNING]
> **Not related to media “streams”** — do not confuse with MPEG-TS or WebRTC.

---


## When not to use

- **Any greenfield identity** — LDAP/OIDC/SAML.
- **Internet-facing authentication** — never.

---


## Related

[[DNS]] [[Streaming]] [[Authentication command]]

## Sources

- [Wikipedia — Network Information Service](https://en.wikipedia.org/wiki/Network_Information_Service)
