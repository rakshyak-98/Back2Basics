[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Memento]]

# Observer

> Observer defines a one-to-many dependency — when one object changes state, all dependents are notified and updated automatically.

## Interview Relevance

Interviewers ask Observer to check event-driven thinking — subject/observer roles, push vs pull, and leak risks from forgotten unsubscribe.

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

Push model sends full data; pull model observers query subject after notification.

- **Event listeners** (DOM, Node `EventEmitter`).
- **Reactive streams** (RxJS, Observables) with backpressure.
- **Pub/sub brokers** (Kafka topics) at system scale — same idea, distributed.

## Real-World Applications

- Model-view separation (model notifies views).
- Domain events inside an application boundary.

## Comparison

**vs Mediator**

Observer is **broadcast from subject**; [[Design pattern/Mediator]] is **hub routing** between peers.

## Mistakes to Avoid

- **Update order** undefined — observers may see inconsistent intermediate states.
- **Memory leaks** — forgotten subscriptions (always detach or use weak references).
- **Cascading notifications** — observer A updates subject B which notifies again.
