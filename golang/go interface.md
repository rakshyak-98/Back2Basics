[[golang]]

# go interface

> Go employs **structural subtyping** (implicit interface satisfaction) rather than nominal subtyping (explicit `implements` declarations). This design decision optimizes for dependency management, package decoupling, and retroactive abstraction at the compiler level.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

### Orthogonal Dependency Graphs (Decoupling)
Explicit implementations (e.g., `class A implements B`) force the package defining the concrete struct to import the package defining the interface. This creates rigid dependency chains and increases the risk of circular dependencies.
implicit interface invert this relationship : the consumer defines the interface based on the behavior it requires, and the producer remains completely unaware of the interface. The packages remain strictly orthogonal.

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
