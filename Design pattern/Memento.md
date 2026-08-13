[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Chain of Responsibility]]

# Memento

> Memento captures and externalizes an object's internal state so it can be restored later — without exposing implementation details to outsiders.

## Roles

| Role | Role |
|------|------|
| **Originator** | Creates memento from its state; restores from memento |
| **Memento** | Stores snapshot (often immutable) |
| **Caretaker** | Holds mementos; should not inspect contents |

```
Originator.createMemento() → Caretaker.store
Caretaker.retrieve → Originator.restore(memento)
```

## vs Command undo

Command undo often stores **inverse operations**; Memento stores **state snapshots** — better when operations are hard to reverse analytically.

## When to use

- Editor undo, game save states, transactional rollback of complex objects.
- Checkpoint before risky operations.

## Pitfalls

- **Memory** — deep copies of large graphs; consider incremental snapshots.
- **Encapsulation leak** — caretaker must not mutate memento internals.
- **Versioning** — old mementos after schema change need migration or discard.

## Sources

- Gamma et al., *Design Patterns* (Memento)
- [Memento pattern — Wikipedia](https://en.wikipedia.org/wiki/Memento_pattern)
