[[Design pattern]] [[Design pattern/Strategy pattern]] [[Design pattern/Command]]

# State

> State lets an object alter its behavior when its internal state changes — the object appears to change class by delegating to state objects instead of giant `switch` statements.

## Structure

```
Context (holds State reference)
  request() → state.handle()
ConcreteStateA, ConcreteStateB each implement handle() differently
```

Transitions may live in Context or in State objects (`stateA.onEvent()` sets `context.state = stateB`).

## vs Strategy

| | State | Strategy |
|---|-------|----------|
| Who changes behavior | Internal state transitions | Client picks strategy |
| Transitions | Often defined between states | Usually static for a given call |

Same structure; **intent** differs.

## Example

TCP connection: `Closed`, `Listen`, `Established` — each handles `open()`, `close()`, `send()` differently.

## When to use

- Object behavior depends on mode and transitions are explicit (workflow, connection, UI wizard).
- `if (status === …)` blocks grow across many methods.

## Pitfalls

- Too many tiny state classes for simple enums — a table-driven transition map may suffice.
- Circular transition bugs — diagram states and events first.

## Sources

- Gamma et al., *Design Patterns* (State)
- [State pattern — Wikipedia](https://en.wikipedia.org/wiki/State_pattern)
