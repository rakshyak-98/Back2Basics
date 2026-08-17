[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Chain of Responsibility]]

# Memento

> Memento captures and externalizes an object's internal state so it can be restored later — without exposing implementation details to outsiders.

```txt
        Memento ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** Memento reviews cover undo/snapshots without violating encapsulation of th…

## Sources
- Gamma et al., *Design Patterns* (Memento) — deep-dive

## Technical Details
| Role | Role |
|------|------|
| **Originator** | Creates memento from its state; restores from memento |
| **Memento** | Stores snapshot (often immutable) |
| **Caretaker** | Holds mementos; should not inspect contents |

```
Originator.createMemento() → Caretaker.store
Caretaker.retrieve → Originator.restore(memento)
```

## Mistakes to Avoid
- **Mistake:** **Memory**
- **Mistake:** **Encapsulation leak**
- **Mistake:** **Versioning**

## Comparison
- **vs Command undo**

- Command undo often stores **inverse operations**; Memento stores **state snap…


### Use cases
- Editor undo, game save states, transactional rollback of complex objects.
- Checkpoint before risky operations.
