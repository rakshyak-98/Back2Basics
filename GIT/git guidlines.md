[[GIT]]

# git guidlines

> git guidlines — feat: add new inventory endpoint

```txt
        git guidlines ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Guideline questions check team conventions

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
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
- **Implements filtering:** Implements filtering by asset type
- **Adds validation:** Adds validation for filter parameters
- **Includes error:** Includes error handling for invalid filters
Ticket: AT-123
```
- **keep first:** keep first line under 50 characters
- **use imperative:** use imperative mood (add not added)
- **include relevant:** include relevant ticket/issues numbers
- **separate subject:** separate subject from body with blank line
- **describe what:** describe what and why, not how

## Technical Details
- Use conventional prefixes in subject line:

- `feat:` new behavior
- `fix:` bug repair
- `docs:` documentation only
- `chore:` tooling or maintenance

## Mistakes to Avoid
> [!WARNING]
> One commit should be **one logical change** — easier to revert and bisect.

| Symptom | Check | Fix |
|---------|-------|-----|
| History hard to read | Mixed message styles | Agree on prefix convention in team doc |
| Revert hard to find | No scope in subject | Add scope: `fix(auth): ...` |
| Broken bisect | WIP commits on main | Squash or rebase before merge to main |

## Pros/Cons or Trade-offs
- Do not rewrite published history on shared branches to fix message typos.
