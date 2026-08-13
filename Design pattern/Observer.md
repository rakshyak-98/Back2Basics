[[Design pattern]] [[Design pattern/Command]] [[Design pattern/Memento]]

# Observer

> Observer defines a one-to-many dependency — when one object changes state, all dependents are notified and updated automatically.

## Structure

```
Subject
  attach(observer)
  detach(observer)
  notify() → observer.update()

Observer.update(event)
```

Push model sends full data; pull model observers query subject after notification.

## Modern variants

- **Event listeners** (DOM, Node `EventEmitter`).
- **Reactive streams** (RxJS, Observables) with backpressure.
- **Pub/sub brokers** (Kafka topics) at system scale — same idea, distributed.

## vs Mediator

Observer is **broadcast from subject**; [[Design pattern/Mediator]] is **hub routing** between peers.

## When to use

- Model-view separation (model notifies views).
- Domain events inside an application boundary.

## Pitfalls

- **Update order** undefined — observers may see inconsistent intermediate states.
- **Memory leaks** — forgotten subscriptions (always detach or use weak references).
- **Cascading notifications** — observer A updates subject B which notifies again.

## Sources

- Gamma et al., *Design Patterns* (Observer)
- [Observer pattern — Wikipedia](https://en.wikipedia.org/wiki/Observer_pattern)
