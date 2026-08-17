[[GIT]]

# git commit template

> git commit template — git config to use custom commit template





## Interview Relevance
Commit templates enforce structure — interviewers care that templates aid clarity without bureaucracy.

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
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

## Technical Details
```bash
git config --global commit.template ~/.config/git/commit-template
cat ~/.config/git/commit-template
```

## Pros/Cons or Trade-offs
- Skip a template when a project mandates commitizen or another enforced format.

## Mistakes to Avoid
> [!WARNING]
> The template pre-fills the editor — it does not enforce format unless hooks do.

| Symptom | Check | Fix |
|---------|-------|-----|
| Template not applied | Wrong path; not global | `git config --get commit.template`; use absolute path |
| Editor opens empty | Template path typo | Verify file exists and is readable |
| Template shows in log | Committed template file by mistake | Keep template outside repository or in dotfiles only |
