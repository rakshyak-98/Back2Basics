[[cookies]]

# cookies lifecycle

> cookies lifecycle — session — deleted when tab/session ends

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** cookies lifecycle — plain job, how I run it, how I know it’s broken.


**Cookies types**
- Session -> deleted when tab/session ends
- Persistent -> stored until expiration
- Host-only -> not shared with subdomains
**Storage rules**
- Stored per domain + path scope
- Public suffix protection (cannot set `.com` etc)
- Attributes control visibility/security
`Path` -> Which routes auto-send this cookie
`Domain` -> Which subdomains can access it
`Max-Age/Expires` -> Defines **persistence**
`HttpOnly` -> JavaScript **cannot** read it
`Secure` -> Only over **HTTPS**
`SameSite` -> Controls cross-site sending
`Priority` -> Browser eviction order
**Automatic sending in requests**
- Browser checks domain + path + security flag
- If matched -> adds to `Cookie:` request header
`SameSite=Lax/strict` -> blocks many cross-site sends (CSRF defence).
`HttpOnly` -> protects from [[XSS cookie]]
**Phases**: `Client Request → Server Response (Set-Cookie) → Client Stores → Subsequent Requests → Server Reads → Expiry / Manual Deletion`

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **cookies lifecycle** | Core idea of this note | “I can explain cookies lifecycle without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[cookies]]
