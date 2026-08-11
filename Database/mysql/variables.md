[[mysql]] [[mysql Programmable SQL]] [[cli]]

# variables

> MySQL variables hold values for the session (`@x`) or inside a routine (`DECLARE`) — different lifetime rules.

---

## Mental model

**Say it in one breath:** `@user_var` lasts for the connection; `DECLARE` locals exist only inside a `BEGIN…END` block; server knobs use `SET` / `SET GLOBAL` (not `@`).

```txt
SET @x = 1;          ── session user variable (until disconnect)
DECLARE y INT;       ── routine local only
SET GLOBAL foo=…;    ── server variable (needs privs; may need restart for some)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **User variable `@x`** | Session-scoped | “No DECLARE; lives until disconnect.” |
| **Local `DECLARE`** | Block-scoped in routines | “Illegal outside stored programs.” |
| **SYSTEM variable** | Server/session settings | `sql_safe_updates`, `event_scheduler` |
| **GLOBAL vs SESSION** | Who sees the change | “GLOBAL for new sessions; SESSION for me.” |

---

## Standard config / commands

```sql
SET @my_var = 42;
SELECT @my_var;
SELECT * FROM users WHERE id = @user_id;

-- inside procedure/function only:
DECLARE my_var INT DEFAULT 0;
SET my_var = 100;

SET SESSION sql_safe_updates = 1;
SET GLOBAL general_log = 1;  -- SUPER/SYSTEM_VARIABLES_ADMIN
```

| Knob | Why it matters |
|------|----------------|
| `@var` | Handy for scripts; not typed strongly |
| `DECLARE` | Typed locals in procedures |
| Pool reuse | Leftover `@vars` can leak across requests on same conn |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `DECLARE` syntax error in client | Outside `BEGIN…END` | Use `@var` or wrap in procedure |
| Variable “missing” | New connection / pool | Re-SET; don’t assume persistence |
| GLOBAL set but no effect | Needs restart or SESSION | Check docs; SET SESSION too |
| Wrong row updated | `@id` NULL/stale | Initialize every script path |

---

## Gotchas

> [!WARNING]
> **Cannot DROP a user variable** — reconnect (or overwrite). Pooling makes leftover `@vars` a footgun.

> [!WARNING]
> **Assignment in SELECT** (`SELECT @a := …`) — order-dependent; prefer `SET`.

---

## When NOT to use

- **App state across HTTP requests** — use DB rows or Redis; session vars die with the connection.
- **Typed business logic** — prefer real columns / app code over `@` soup.

---

## Related

[[mysql Programmable SQL]] [[mysql function]] [[mysql connection]] [[cli]]
