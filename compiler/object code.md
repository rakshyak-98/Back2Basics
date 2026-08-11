[[compiler]]

# object code

> object code — a product of a compiler.

---

## Mental model

**Say it in one breath:** object code — plain job, how I run it, how I know it’s broken.


is a product of a [[compiler]].
 - sequence of statements or instructions in a computer language.
 - a portion of machine code that has not yet been linked into a complete program.
 - require a [[linker]] to link with other modules.
### Overview
Typically, an object file can contain three kinds of symbols:
- defined "external" symbols, sometimes called "public" or "entry" symbols, which allow to be called by other modules
- undefined "external" symbols, which reference other modules where these symbols are defined.
- local symbols, used internally within the object file to facilitate relocation.
>[!INFO] linker use offset or placeholders in object code to connect everything together.
>[!INFO] where machine code is binary code that can be executed directly by the CPU, object code has the jumps partially parameterized so that a linker can fill them in.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **object code** | Core idea of this note | “I can explain object code without jargon.” |
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
