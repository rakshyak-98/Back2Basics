[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Chain of Responsibility]]

# Memento

> Memento captures and externalizes an object's internal state so it can be restored later — without exposing implementation details to outsiders.

## Interview Relevance

Memento interviews cover undo/snapshots without violating encapsulation of the originator.

## Sources

- Gamma et al., *Design Patterns* (Memento) — deep-dive

## Technical Details

**Roles**

| Role | Role |
|------|------|
| **Originator** | Creates memento from its state; restores from memento |
| **Memento** | Stores snapshot (often immutable) |
| **Caretaker** | Holds mementos; should not inspect contents |

```
Originator.createMemento() → Caretaker.store
Caretaker.retrieve → Originator.restore(memento)
```

## Real-World Applications

- Editor undo, game save states, transactional rollback of complex objects.
- Checkpoint before risky operations.

## Comparison

**vs Command undo**

Command undo often stores **inverse operations**; Memento stores **state snapshots** — better when operations are hard to reverse analytically.

## Mistakes to Avoid

- **Memory** — deep copies of large graphs; consider incremental snapshots.
- **Encapsulation leak** — caretaker must not mutate memento internals.
- **Versioning** — old mementos after schema change need migration or discard.
