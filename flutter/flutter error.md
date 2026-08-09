[[flutter]]

# flutter error

> flutter error — try flutter pub outdated for more information.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** flutter error — plain job, how I run it, how I know it’s broken.


```text
Try `flutter pub outdated` for more information.
Launching lib/main.dart on motorola edge 50 fusion in debug mode...
FAILURE: Build failed with an exception.
* What went wrong:
Value '/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home' given for org.gradle.java.home Gradle property is invalid (Java home supplied is invalid)
* Try:
Running Gradle task 'assembleDebug'...                           1,099ms
```
- installed at macOS location `/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home`
- you are on linux ubuntu, Gradle cannot start JVM
Why people add this:
- multiple JDK versions installed
- Android Studio using different JDK
- lock project to specific Java version

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **flutter error** | Core idea of this note | “I can explain flutter error without jargon.” |
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
