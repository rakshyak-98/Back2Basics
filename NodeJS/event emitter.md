<!-- note-strategy: operational -->
[[NodeJS]] [[EventEmitter]] [[Stream]] [[Node events driven]]

# event emitter

> Pub/sub inside one process — `emit` named events; listeners run synchronously in registration order.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Many Node objects (streams, sockets, processes) *are* EventEmitters. `on`/`once` subscribe; `emit` calls listeners now (same tick).

```txt
ee.on('data', fn) → ee.emit('data', chunk) → fn(chunk)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **on / once** | Subscribe / one-shot | “`once` auto-removes after fire.” |
| **MaxListeners** | Leak warning threshold | “Default 10 — often a forgotten `on`.” |
| **error event** | Special | “Unhandled `error` can crash the process.” |

## Standard config / commands

```js
import { EventEmitter } from 'node:events'

const bus = new EventEmitter()
bus.on('job', (id) => console.log(id))
bus.emit('job', 42)

ee.setMaxListeners(20) // only if intentional fan-out
```

| Knob | Why it matters |
|------|----------------|
| `off` / `removeListener` | Prevent leaks |
| `rawListeners` | Debug who is subscribed |
| `captureRejections` | Async listener promise rejections |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| MaxListeners exceeded | Duplicate `on` in hot path | `once` or remove on cleanup |
| Process crash on error | No `error` listener | Always `on('error')` for streams/sockets |
| Listener never runs | Typo in event name | Shared const for names |
| Memory leak | Long-lived emitter + add forever | Remove on shutdown / request end |

---

## Gotchas

> [!WARNING]
> **Listeners are sync** — a slow listener blocks the emit loop; don’t do heavy CPU in handlers.

> [!WARNING]
> **`error` is special** — without a handler, Node throws.

---

## When NOT to use

- **Cross-process messaging** — use Redis/NATS/queues, not in-memory emitters.
- **Request/response APIs** — return promises; don’t invent event protocols casually.

---

## Related

[[EventEmitter]] [[Stream]] [[Node events driven]] [[Stream Events]]
