[[flutter]]

# flutter widget

> flutter widget — if MaterialPageRoute took a direct widget instance instead of a builder, you would have to create that screen's widget in memory before you…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** flutter widget — plain job, how I run it, how I know it’s broken.


If `MaterialPageRoute` took a direct widget instance instead of a builder, you would have to create that screen's widget in memory before you even navigated to it.
By using `builder`, you are essentially giving Flutter a "recipe" rather than the "backed cake". Flutter will hold onto that recipe and only execute it (build the widget) at the exact moment the user navigates to that route.
The `builder` function provides a `BuildContext`
```dart
builder: (BuildContext context) => MyNewScreen(),
```
- every widget in Flutter need a `BuildContext` to know where it lives in the overall Widget tree. The context provide by the `builder` is the context of the new route, not the screen you are leaving.
- Because the `builder` is a function executed at runtime, it allows you to pass dynamic arguments to your new screen exactly when it is being created.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **flutter widget** | Core idea of this note | “I can explain flutter widget without jargon.” |
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

[[flutter]]
