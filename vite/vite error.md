[[vite]]

# vite error

> vite error — the issue is now 100% clear: you are running npm run build, which executes npx vite build, but npx is still trying to

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** vite error — plain job, how I run it, how I know it’s broken.


The issue is now 100% clear: **you are running npm run build**, which executes `npx vite build`, but **`npx` is still trying to use the broken `./node_modules/.bin/vite` script that has no execute permission**.
This is the classic “Permission denied” bug that hits almost everyone at least once (especially on WSL, Git-cloned repos, or when node_modules was copied from another machine).
### Exact Diagnosis from Your Output
```text
sh: 1: vite: Permission denied
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **vite error** | Core idea of this note | “I can explain vite error without jargon.” |
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

[[vite]]
