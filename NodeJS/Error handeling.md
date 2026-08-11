[[NodeJS]]

# Error handeling

> Error handeling — create errors with a custom name is to extend the built-in Error class using ES6 class syntax

---

## Mental model

**Say it in one breath:** Error handeling — I can explain the job, the config, and the top failure without jargon.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Error handeling** | This note’s core idea | “I explain Error handeling in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

---

## Standard config / commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Runtime error | stack / overlay | Null-check; fix import |
| Build fail | deps / tsconfig | Align versions; clear cache |
| Auth/CORS | network tab | Headers and tokens |

---

## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

---

## When NOT to use

- Skip when a simpler existing approach already fits.

---

## Related

[[NodeJS]]
