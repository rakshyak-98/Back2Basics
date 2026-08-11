[[GIT]]

# git commit template

> git commit template — git config to use custom commit template

---

## Mental model

**Say it in one breath:** git commit template — git config to use custom commit template

**Git configuration to use custom commit template**
```bash
git config --global commit.template ~/.config/git/commit-template
```
```text
<type>(<scope>): <short summary 50-72 chars>
<body - optional>
Explain **why** this change + **context** if needed (especially for tricky parts)
BREAKING CHANGE: <description if any>   ← only when really breaking
Resolves: #123
See also: #456
```
- feat        → new feature
- fix         → bug fix
- docs        → documentation only
- style       → formatting, missing semicolons, etc (no code change)
- refactor    → code change that neither fixes bug nor adds feature
- perf        → performance improvement
- test        → adding or correcting tests
- build       → build system, CI, external dependencies
- chore       → maintenance (gitignore, scripts, rename...)
- revert      → revert previous commit


## Standard config / commands

```bash
git config --global commit.template ~/.config/git/commit-template
cat ~/.config/git/commit-template
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Template not applied | Wrong path; not global | `git config --get commit.template`; use absolute path |
| Editor opens empty | Template path typo | Verify file exists and is readable |
| Template shows in log | Committed template file by mistake | Keep template outside repository or in dotfiles only |

---

## Gotchas

> [!WARNING]
> The template pre-fills the editor — it does not enforce format unless hooks do.

---

## When NOT to use

- Skip a template when a project mandates commitizen or another enforced format.


---

## Related

[[GIT]]
