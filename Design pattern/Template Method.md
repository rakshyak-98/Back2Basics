[[Design pattern]] [[Design pattern/Strategy pattern]] [[Design pattern/Command]]

# Template Method

> Template Method defines the skeleton of an algorithm in a base class, deferring some steps to subclasses — fixed order, swappable details.

```txt
        Template Method ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** Template Method checks skeleton algorithms with overridable steps

## Sources
- Gamma et al., *Design Patterns* (Template Method) — deep-dive

## Key Concepts
```text
abstract class Base {
  run() { step1(); step2(); step3(); }
  step1() { ... fixed ... }
  abstract step2();
  step3() { ... optional hook ... }
}
```

- **Note:** Subclasses override `step2()` (and optional hooks) without redefining `run()`…

## Technical Details
- Data mining pipeline: `analyze()` calls `read()`, `process()`, `send()`

- Protected empty hook methods (`beforeHook()`) let subclasses opt in without f…

## Mistakes to Avoid
- **Mistake:** Fragile base class — changes to `run()` break all subclasses
- **Mistake:** Deep inheritance trees

## Comparison
- **vs Strategy**

- Template Method uses **inheritance** and a **fixed pipeline**


### Use cases
- Framework lifecycle (`onCreate`, `onDestroy` in UI frameworks).
- Batch jobs with consistent stages.
