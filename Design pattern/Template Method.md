[[Design pattern]] [[Design pattern/Strategy pattern]] [[Design pattern/Command]]

# Template Method

> Template Method defines the skeleton of an algorithm in a base class, deferring some steps to subclasses — fixed order, swappable details.

## Structure

```text
abstract class Base {
  run() { step1(); step2(); step3(); }
  step1() { ... fixed ... }
  abstract step2();
  step3() { ... optional hook ... }
}
```

Subclasses override `step2()` (and optional hooks) without redefining `run()`'s sequence.

## Example

Data mining pipeline: `analyze()` calls `read()`, `process()`, `send()` — subclasses implement parsing for CSV vs JSON while order stays stable.

## vs Strategy

Template Method uses **inheritance** and a **fixed pipeline**; Strategy uses **composition** and **full algorithm** swap. Prefer Strategy when runtime selection or testing isolation matters; Template Method when the sequence is invariant and only steps vary.

## Hooks

Protected empty hook methods (`beforeHook()`) let subclasses opt in without forcing abstract methods for optional behavior.

## When to use

- Framework lifecycle (`onCreate`, `onDestroy` in UI frameworks).
- Batch jobs with consistent stages.

## Pitfalls

- Fragile base class — changes to `run()` break all subclasses.
- Deep inheritance trees — consider pipeline of functions or [[Design pattern/Chain of Responsibility]].

## Sources

- Gamma et al., *Design Patterns* (Template Method)
- [Template method pattern — Wikipedia](https://en.wikipedia.org/wiki/Template_method_pattern)
