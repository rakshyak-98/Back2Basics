[[staff engineer.md]]

# staff engineer

> Staff engineer — technical leadership through scope, influence, and craft over titles.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** staff engineer — I can explain the job, the configuration, and the top failure without jargon.


As a Staff Engineer with 30 years in the industry, I have seen technologies rise and fall, but the path to the "Staff-plus" level remains anchored in one truth: **Your value is no longer measured by your output, but by your impact on the output of others.**
To reach this level as a self-taught programmer, you must move from being a "solver of problems" to a "shaper of the environment" where problems get solved.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **staff engineer** | This note’s core idea | “I explain staff engineer in plain words.” |
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
| Hotspot | metrics by key | Shard or cache |
| Cascade fail | timeouts | Bulkheads and backoff |
| Unclear ownership | diagram actors | Name the single writer |

---

## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

---

## When NOT to use

- Skip when a simpler existing approach already fits.

---

## Related

[[staff engineer.md]]
