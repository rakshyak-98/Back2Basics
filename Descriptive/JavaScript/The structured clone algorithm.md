[[JavaScript]]

# The structured clone algorithm

> One-line: what / why for **The structured clone algorithm** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- used to serialize and deserialize data structures in JavaScript.
- it can not clone functions, Error Objects, Weak-Map or DOM nodes.
- the algorithm is designed to handle Circular References.
- `localStorage` had not been updated with this feature and there are no discussions around it happening in the future.
> [!INFO] it creates a placeholder object during serialization and properly restores the reference during deserialization.
copies complex JavaScript objects. It is used internally when invoking `structuredClone` to transfer data between `Workers` via `postMessage()` storing objects with `IndexDB` or copying objects for `other APIs`.

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
