[[NodeJS]] [[EventEmitter]] [[Stream]] [[Node events driven]] [[Stream Events]]

# event emitter

> Pub/sub inside one process — `emit` named events; listeners run synchronously in registration order.

```txt
        event emitter ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **event emitter** to check whether you can explain the mecha…

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

## Mistakes to Avoid
- **Mistake:** **Listeners are sync**
- **Mistake:** **`error` is special** — without a handler, Node throws
- **Mistake:** **MaxListeners exceeded:** check Duplicate `on` in hot path
- **Mistake:** **Process crash on error:** check No `error` listener
- **Mistake:** **Listener never runs:** check Typo in event name
- **Mistake:** **Memory leak:** check Long-lived emitter + add forever

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Pub/sub inside one process — `emit` named events; listeners run synchronously in…).
- **Con / when not:** **Cross-process messaging**
- **Con / when not:** **Request/response APIs**

## Comparison
- vs [[EventEmitter]]: Same Node `events` module


### Use cases
- In production APIs and tooling, **event emitter** shows up whenever teams shi…
