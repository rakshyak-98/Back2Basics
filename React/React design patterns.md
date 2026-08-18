[[React]]

# React design patterns

> React design patterns — a function that takes a component and returns an enhanced version. Less common now due to hooks, but still useful for legacy code or

## Mental model

**Say it in one breath:** React design patterns — I can explain the job, the configuration, and the top failure without jargon.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **React design patterns** | This note’s core idea | “I explain React design patterns in plain words.” |
| --- | --- | --- |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

## Standard config / commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Runtime error | stack / overlay | Null-check; fix import |
| Build fail | deps / tsconfig | Align versions; clear cache |
| Auth/CORS | network tab | Headers and tokens |

## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

## When NOT to use

- Skip when a simpler existing approach already fits.

## Related

[[React]]
