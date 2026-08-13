<!-- note-strategy: operational -->
[[ExpressJS]] [[express concepts]] [[XSRF (cross-site request forgery)]]

# Express HPP

> HPP (HTTP Parameter Pollution) protection — middleware that blocks/duplicates conflicting query/body params attackers use to confuse parsers.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `?id=1&id=2` may become array or last-wins depending on stack. HPP middleware removes polluted duplicates so your checks see one value.

```txt
?role=user&role=admin  →  sanitize → single role
```

---

## Standard config / commands

```js
import hpp from 'hpp'
app.use(hpp()) // after body parsers typically
// allowlists possible via options in some versions
```

| Knob | Why it matters |
|------|----------------|
| Whitelist | Multi-value params you want |
| Order | After parsers |
| Logs | Detect probes |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Legit multi values broken | HPP stripped | Whitelist keys |
| Still arrays | Wrong middleware | Confirm `hpp` mounted |
| Bypass via body | Only query cleaned | Apply consistently |

---

## Gotchas

> [!WARNING]
> **Not a full WAF** — still validate types/authz.

> [!WARNING]
> **Framework differences** — Express query parsing quirks.

---

## When NOT to use

- **APIs that require multi-value query by design** — whitelist carefully.
- **Non-Express stacks** — use their equivalents.

---

## Related

[[express concepts]] [[Express middleware]] [[XSRF (cross-site request forgery)]]
