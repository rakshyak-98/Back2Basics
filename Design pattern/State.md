[[Design pattern]] [[Design pattern/Strategy pattern]] [[Design pattern/Command]]

# State

> State lets an object alter its behavior when its internal state changes — the object appears to change class by delegating to state objects instead of giant `switch` statements.

```txt
        State ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** State checks modeling behavior that changes with lifecycle

## Sources
- Gamma et al., *Design Patterns* (State) — deep-dive

## Key Concepts
```
Context (holds State reference)
  request() → state.handle()
- **Note:** ConcreteStateA, ConcreteStateB each implement handle() differently
```

- **Note:** Transitions may live in Context or in State objects (`stateA.onEvent()` sets …

## Technical Details
- TCP connection: `Closed`, `Listen`, `Established`

## Mistakes to Avoid
- **Mistake:** Too many tiny state classes for simple enums
- **Mistake:** Circular transition bugs — diagram states and events first

## Comparison
- **vs Strategy**

| | State | Strategy |
|---|-------|----------|
| Who changes behavior | Internal state transitions | Client picks strategy |
| Transitions | Often defined between states | Usually static for a given call |

- Same structure; **intent** differs.


### Use cases
- Object behavior depends on mode and transitions are explicit (workflow, connection, UI wizard).
- `if (status === …)` blocks grow across many methods.
