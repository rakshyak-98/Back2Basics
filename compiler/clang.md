[[compiler]]

# clang

> clang — a compiler front-end for the C, C++, Objective-C and Objective C++ programming languages.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** clang — plain job, how I run it, how I know it’s broken.


- is a compiler front-end for the C, C++, Objective-C and Objective C++ programming languages.
- it is part of the LLVM (Low-Level Virtual Machine) project and is designed to offer fast compilation.
- Clang can also be used as a drop-in replacement for GCC (GNU Compiler Collection).

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **clang** | Core idea of this note | “I can explain clang without jargon.” |
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

[[compiler]]
