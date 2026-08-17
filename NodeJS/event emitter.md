[[NodeJS]] [[EventEmitter]] [[Stream]] [[Node events driven]] [[Stream Events]]

# event emitter

> Pub/sub inside one process — `emit` named events; listeners run synchronously in registration order.





## Interview Relevance
Interviewers use **event emitter** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **on / once**, **MaxListeners**, **error event**.

## Sources
- [Node.js — Events / EventEmitter](https://nodejs.org/api/events.html) — deep-dive
- [Wikipedia — event emitter](https://en.wikipedia.org/wiki/event_emitter) — overview

## Key Concepts
- **on / once:** Subscribe / one-shot — `once` auto-removes after fire.
- **MaxListeners:** Leak warning threshold — Default 10 — often a forgotten `on`.
- **error event:** Special — Unhandled `error` can crash the process.

## Technical Details
```txt
ee.on('data', fn) → ee.emit('data', chunk) → fn(chunk)
```

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

## Real-World Applications
In production APIs and tooling, **event emitter** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Listeners are sync** — a slow listener blocks the emit loop; don’t do heavy CPU in handlers; **`error` is special** — without a handler, Node throws.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Pub/sub inside one process — `emit` named events; listeners run synchronously in…).
- **Con / when not:** **Cross-process messaging** — use Redis/NATS/queues, not in-memory emitters.
- **Con / when not:** **Request/response APIs** — return promises; don’t invent event protocols casually.

## Comparison
vs [[EventEmitter]]: Same Node `events` module — this note is the short map; EventEmitter is the deep API note. vs [[Stream]]: know when each applies — do not treat them as interchangeable. vs [[Node events driven]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Listeners are sync** — a slow listener blocks the emit loop; don’t do heavy CPU in handlers.
- **`error` is special** — without a handler, Node throws.
- **MaxListeners exceeded:** check Duplicate `on` in hot path; fix: `once` or remove on cleanup
- **Process crash on error:** check No `error` listener; fix: Always `on('error')` for streams/sockets
- **Listener never runs:** check Typo in event name; fix: Shared const for names
- **Memory leak:** check Long-lived emitter + add forever; fix: Remove on shutdown / request end
