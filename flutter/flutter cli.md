[[flutter]]

# flutter cli

> flutter cli — a channel is a release stream of the Flutter SDK. Each channel receives updates at different speeds and stability levels.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** flutter cli — plain job, how I run it, how I know it’s broken.


AOT (Ahead-of-Time Compilation)
```bash
flutter bash-completion;
flutter create <DIRECTORY>; # Creates a new project
flutter install -d <DEVICE ID>; # Install flutter app on an attached device.
flutter logs; # SHow log output fo running flutter apps.
```
```bash
flutter run; # Users JIT (Just-In-Time) compilation
flutter attach -d <DEVICE ID>;
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **flutter cli** | Core idea of this note | “I can explain flutter cli without jargon.” |
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
