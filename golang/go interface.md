[[golang]]

# go interface

> Go interface — a method set; any type with those methods satisfies it implicitly.

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
