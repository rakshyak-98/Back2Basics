[[flutter]]

# Flutter app icon change

> Flutter app icon change — instructions for replacing the default Flutter launcher icon with the green recycling trash icon (WasteManagement.png).

## Mental model

**Say it in one breath:** Flutter application icon change — I can explain the job, the configuration, and the top failure without jargon.

Instructions for replacing the default Flutter launcher icon with the green recycling trash icon (`WasteManagement.png`).

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Flutter app icon change** | This note’s core idea | “I explain Flutter app icon change in plain words.” |
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

[[flutter]]
