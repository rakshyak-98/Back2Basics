[[System Design/SOLID]] [[System Design/KISS]] [[System Design/DRY]] [[Design pattern/Dependency Injection]]

# Design Patterns

> Design patterns — reusable object designs; use only where variation is real. **Shvets**.

---

## Mental model

**Say it in one breath:** Design Patterns — I can explain the job, the configuration, and the top failure without jargon.


Patterns are **named solutions to recurring design problems**, not a checklist. In a multi-platform / multi-goal backend (e.g. Meta Marketing API), every pattern that earned its keep mapped to a **variation point**: goals change, platforms multiply, Graph quirks need adapters, launch needs a fixed algorithm with swappable steps.

Four principles always beat twenty patterns:

| Principle | Meaning in code |
|-----------|-----------------|
| **Encapsulate what varies** | Pull goals, platforms, geo, vendor quirks into modules — leave stable orchestration alone |
| **Program to an interface** | Depend on factories / strategies / adapters — not Meta field names or concrete HTTP clients |
| **Favor composition over inheritance** | Stack decorators/wrappers instead of subclassing `MetaClient` for every concern combo |
| **SOLID (esp. SRP + OCP)** | One job per handler/strategy; new goals/platforms = new class + register, not edit switches |

```
Client / REST
  → Facade (stable app API)
    → Command / Pipeline (Template Method)
      → Chain of Responsibility (validation)
      → Strategy (goal / algorithm)
      → Abstract Factory (platform service family)
      → Adapter + Decorator/Pr

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Design Patterns** | This note’s core idea | “I explain Design Patterns in plain words.” |
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
| Broken / unexpected | Reproduce + logs | Fix config or code path |
| Works only locally | Env / secrets / versions | Align environments |
| Intermittent | race / timeout / retry | Add backoff; fix shared state |

---

## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

---

## When NOT to use

- Skip when a simpler existing approach already fits.

---

## Related

[[System Design/SOLID]] [[System Design/KISS]] [[System Design/DRY]] [[Design pattern/Dependency Injection]]
