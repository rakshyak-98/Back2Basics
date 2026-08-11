[[css]]

# tailwindcss Error

> tailwindcss Error — [plugin:@tailwindcss/vite:generate:serve] Cannot apply unknown utility class w-3. Are you using CSS modules or similar and missing…

---

## Mental model

**Say it in one breath:** tailwindcss Error — plain job, how I run it, how I know it’s broken.


`[plugin:@tailwindcss/vite:generate:serve] Cannot apply unknown utility class `w-3`. Are you using CSS modules or similar and missing `@reference`? https://tailwindcss.com/docs/functions-and-directives#reference-directive`

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **tailwindcss Error** | Core idea of this note | “I can explain tailwindcss Error without jargon.” |
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

[[css]]
