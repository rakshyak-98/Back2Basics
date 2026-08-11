[[GIT]]

# git guidlines

> git guidlines — feat: add new inventory endpoint

---

## Mental model

**Say it in one breath:** git guidlines — feat: add new inventory endpoint

```vbnet
feat: add new inventory endpoint
fix: correct inventory route response
docs: update inventory API documentation
refactor: improve inventory route structure
test: add inventory route tests
```
```vbnet
feat: add GET /inventory pagination support
feat: implement inventory search endpoint
fix: handle empty inventory response
perf: optimize inventory query performance
security: add authentication to inventory routes
```
```vbnet
<type>: <subject>
[optional body]
[optional footer]
Example:
feat: add inventory filtering endpoint
- Implements filtering by asset type
- Adds validation for filter parameters
- Includes error handling for invalid filters
Ticket: AT-123
```
- keep first line under 50 characters
- use imperative mood (add not added)
- include relevant ticket/issues numbers
- separate subject from body with blank line
- describe what and why, not how


## Standard config / commands

Use conventional prefixes in subject line:
- `feat:` new behavior
- `fix:` bug repair
- `docs:` documentation only
- `chore:` tooling or maintenance

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| History hard to read | Mixed message styles | Agree on prefix convention in team doc |
| Revert hard to find | No scope in subject | Add scope: `fix(auth): ...` |
| Broken bisect | WIP commits on main | Squash or rebase before merge to main |

---

## Gotchas

> [!WARNING]
> One commit should be **one logical change** — easier to revert and bisect.

---

## When NOT to use

- Do not rewrite published history on shared branches to fix message typos.


---

## Related

[[GIT]]
