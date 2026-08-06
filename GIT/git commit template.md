[[GIT]]

# git commit template

> One-line: what / why for **git commit template** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Git config to use custom commit template**
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

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
