[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Memento]]

# Observer

> Observer defines a one-to-many dependency — when one object changes state, all dependents are notified and updated automatically.

```txt
        Observer ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Pitfalls
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask Observer to check event-driven thinking

## Sources
- Gamma et al., *Design Patterns* (Observer) — deep-dive

## Key Concepts
```
Subject
  attach(observer)
  detach(observer)
  notify() → observer.update()

Observer.update(event)
```

- **Note:** Push model sends full data

- **Event listeners:** (DOM, Node `EventEmitter`).
- **Reactive streams:** (RxJS, Observables) with backpressure.
- **Pub/sub brokers:** (Kafka topics) at system scale — same idea, distributed.

## Mistakes to Avoid
- **Mistake:** **Update order** undefined
- **Mistake:** **Memory leaks**
- **Mistake:** **Cascading notifications**

## Comparison
- **vs Mediator**

- Observer is **broadcast from subject**


### Use cases
- Model-view separation (model notifies views).
- Domain events inside an application boundary.
