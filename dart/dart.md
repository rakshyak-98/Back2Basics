[[dart]]

# dart

> dart — factory — Unlike a normal constructor, a factory constructor can return an existing instance or even a subclass. In this context, it's used to return a

---

## Mental model

**Say it in one breath:** dart — plain job, how I run it, how I know it’s broken.


`factory ApiRoomDate.fromJson(...)`
- Factory -> Unlike a normal constructor, a `factory` constructor can return an existing instance or even a subclass. In this context, it's used to return a fully populated `ApiRoomData` object after processing the JSON.
- Map<String, dynamic>  -> This represents the structure of a standard JSON object (keys are Strings, values can by anything)

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **dart** | Core idea of this note | “I can explain dart without jargon.” |
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

[[dart]]
